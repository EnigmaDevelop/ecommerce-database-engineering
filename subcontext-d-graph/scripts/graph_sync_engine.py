import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# =========================================================================
# PHASE 4: GLOBAL INFRASTRUCTURE ROUTING CONFIGURATIONS
# =========================================================================
# Connecting locally from host machine via exposed container ports
PG_URL = "jdbc:postgresql://localhost:5433/ecommerce_db"
PG_PROPERTIES = {
    "user": "data_engineer",
    "password": "de_password123",
    "driver": "org.postgresql.Driver"
}

# Target local Neo4j Bolt port directly - bypassing container naming errors
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "graph_password123"

# =========================================================================
# STEP 1: INITIALIZE SPARK SESSION WITH LOCAL CLASS DEPENDENCIES
# =========================================================================
SUBMIT_PACKAGES = (
    "io.delta:delta-spark_2.12:3.0.0,"
    "org.apache.hadoop:hadoop-aws:3.3.4,"
    "org.postgresql:postgresql:42.6.0,"
    "org.neo4j:neo4j-connector-apache-spark_2.12:5.3.1_for_spark_3"
)
os.environ["PYSPARK_SUBMIT_ARGS"] = f"--packages {SUBMIT_PACKAGES} pyspark-shell"
os.environ["AWS_ACCESS_KEY_ID"] = "admin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password123"

spark = SparkSession.builder \
    .appName("Ecommerce_Graph_Topology_Sync_Engine") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .getOrCreate()

print("🏁 Local PySpark Session successfully awakened under version 3.5.0.")

# =========================================================================
# STEP 2: STAGING OPERATIONAL DATA FRAMES FROM MULTI-MODEL SOURCES
# =========================================================================
print("\n📥 Extracting user matrix from PostgreSQL via JDBC...")
pg_users_df = spark.read.jdbc(url=PG_URL, table="users", properties=PG_PROPERTIES)

print("📥 Extracting refined clickstream footprints from Delta Lake Silver tier...")
# Dynamic tracking straight down to your local workspace staging repository
delta_silver_path = "../subcontext-c-lakehouse/notebooks/data/silver/clickstream"
delta_silver_df = spark.read.format("delta").load(delta_silver_path)

# =========================================================================
# STEP 3: EXECUTING IDEMPOTENT GRAPH WRITE PASSES 
# =========================================================================
print("\n🚀 Commencing topological graph sync operations inside Neo4j engine...")

# Pass A: Write (:User) Nodes safely using official 'url' options
pg_users_df.write \
    .format("org.neo4j.spark.DataSource") \
    .option("url", NEO4J_URI) \
    .option("authentication.type", "basic") \
    .option("authentication.basic.username", NEO4J_USER) \
    .option("authentication.basic.password", NEO4J_PASSWORD) \
    .option("labels", "User") \
    .option("node.properties", "user_id,first_name,email") \
    .option("node.keys", "user_id") \
    .mode("Append") \
    .save()
print("✅ Identifiable (:User) Node vectors securely mapped.")

# Pass B: Extract unique (:IPAddress) footprints from the telemetry layers
unique_ips_df = delta_silver_df.select("ip_address").distinct().withColumnRenamed("ip_address", "ip_string")

unique_ips_df.write \
    .format("org.neo4j.spark.DataSource") \
    .option("url", NEO4J_URI) \
    .option("authentication.type", "basic") \
    .option("authentication.basic.username", NEO4J_USER) \
    .option("authentication.basic.password", NEO4J_PASSWORD) \
    .option("labels", "IPAddress") \
    .option("node.properties", "ip_string") \
    .option("node.keys", "ip_string") \
    .mode("Append") \
    .save()
print("✅ Architectural (:IPAddress) Node networks established.")

# Pass C: Map directional edges linking Users directly to their device locations
delta_silver_df.write \
    .format("org.neo4j.spark.DataSource") \
    .option("url", NEO4J_URI) \
    .option("authentication.type", "basic") \
    .option("authentication.basic.username", NEO4J_USER) \
    .option("authentication.basic.password", NEO4J_PASSWORD) \
    .option("relationship", "CLICKED_FROM") \
    .option("relationship.save.strategy", "keys") \
    .option("source.labels", "User") \
    .option("source.keys", "user_id") \
    .option("source.properties", "user_id") \
    .option("target.labels", "IPAddress") \
    .option("target.keys", "ip_address:ip_string") \
    .option("target.properties", "ip_address") \
    .option("relationship.properties", "device_type,ingested_at") \
    .mode("Append") \
    .save()
print("✅ Directional [:CLICKED_FROM] edges successfully locked into disk blocks.")

print("\n🎉 Graph Ingestion Engine finished execution. PoC State Sync Completed!")
