# Phase 3: Real-Time Medallion Data Lakehouse Pipeline (OLAP Core)

This subdirectory contains the container orchestration configurations, stream-processing pipelines, and multi-model federation notebooks for the analytical (OLAP) plane of our enterprise data platform.

## 🏗️ Architectural Objectives

The primary milestone of this tier is to physically decouple high-velocity web telemetry traffic from our operational PostgreSQL nucleus. This architecture mitigates disk I/O degradation and memory pool buffer contention by routing clickstream logs down an asynchronous **Medallion Data Lifecycle Pipeline** powered by **Apache Kafka**, **MinIO Local Object Storage**, and **PySpark JVM workers**.

---

## 📁 Repository Manifest

*   `docker-compose.yml`: Multi-container provisioning map orchestrating the local big data stack (Kafka Broker, Zookeeper Coordinator, MinIO Storage Bucket Engine, and PySpark Standalone Node).
*   `notebooks/kafka_data_injector.ipynb`: High-speed telemetry mock stream producer injecting real-time user event JSON frames onto the message broker at an operational frequency of 5 payloads/sec.
*   `notebooks/bronze_to_gold_etl.ipynb`: The primary stream processing engine unpacking JSON shapes, applying quality barriers via Delta Lake ACID tables, and executing Multi-Model JDBC memory joins against the primary transactional database node.

---

## 🛠️ Local Sandbox Execution & Pipeline Deployment

### Prerequisites
* Ensure [Docker Desktop](https://docker.com) is active and allocated with a minimum of 4GB RAM resource boundaries.
* Ensure the Phase 1 & 2 PostgreSQL primary node is active locally on port `5433`.

### Step 1: Spin Up the Big Data Infrastructure
Navigate to this directory inside your terminal and initiate the core container configurations in detached mode:
```bash
cd subcontext-c-lakehouse
docker compose up -d
```

### Step 2: Access the Processing Lab
Once the network bridge (`lh_network`) finishes component handshakes, open your browser and access the development endpoints:
* **MinIO Storage Console:** `http://localhost:9001` (User: `admin` / Password: `minio_password123`)
* **Jupyter Lab Notebook Workspace:** `http://localhost:8888` (Secure Token: `lakehouse_secret_2026`)

### Step 3: Launch Ingestion Streams
1. Open the Jupyter Lab workspace link in your browser.
2. Initialize and run all cells inside `notebooks/kafka_data_injector.ipynb` to seed continuous message traffic into the `clickstream_events` topic.
3. Open `notebooks/bronze_to_gold_etl.ipynb` and trigger the multi-tiered streaming queries sequentially.

---

## 📈 Documented Infrastructure Workarounds

### 1. Breaking the Streaming Empty Table Deadlock
Delta Lake prohibits schema inference queries on an un-initialized, empty filesystem space during active streaming reads (`readStream`). To resolve this, the processing pipeline implements an automated **Schema Seeding** block that writes a single structured mock row down to disk, generating the initial transactional logs (`_delta_log/000...00.json`) prior to starting continuous stream listeners.

### 2. File Locking Resolution via `HDFSLogStore`
Local object storages (such as MinIO) are eventually consistent and lack atomic file renaming capabilities natively. When multiple concurrent thread processes execute transactional commits over S3 protocols, immediate file locking collisions and hostname null errors trigger pipeline crashes. We resolve this by binding `spark.delta.logStore.class` directly to **`org.apache.spark.sql.delta.storage.HDFSLogStore`**, forcing Spark to handle transaction log serialization via local storage driver layers.

---

## 📚 Corresponding Publication
This sub-context maps directly to the third installment of our technical engineering series on Medium:  
🔗 **[Building a Multi-Tiered Real-Time Delta Lakehouse Pipeline](YOUR_MEDIUM_LINK_HERE)**
