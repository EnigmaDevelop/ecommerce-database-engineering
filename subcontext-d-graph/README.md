# Phase 4: Advanced Graph Engineering Sandbox (Identity Overlay Plane)

This subdirectory houses the isolated prototype infrastructure, storage constraint assertions, and data federation workflows for the Graph Persistence Tier of our hybrid architecture.

## 🏗️ Architectural Objectives

The primary objective of this module is to deliver a pure **Data Engineering Proof of Concept (PoC)** to validate multi-model data pipeline federation. By capturing user metadata states from PostgreSQL (OLTP Core) via JDBC and loading high-velocity telemetry access logs from Delta Lake Silver blocks (OLAP Core) via PySpark, this plane materializes relational and log datasets into connected graph structures inside **Neo4j 5**. 

This overlay plane is engineered strictly for topological connection lookups and structural entity tracing; it does not deploy automated machine learning or real-time predictive analytics workflows.

---

## 📁 Repository Structure

*   `docker-compose.yml`: Provisions the isolated Neo4j 5 Community container mounted with persistent data volumes and the APOC plugin framework.
*   `scripts/graph_sync_engine.py`: Hardened standalone automated production fallback script for scheduled cron data execution passes.
*   `notebooks/graph_sync_lab.ipynb`: The interactive exploration staging workspace driving containerized PySpark `coalesce(1)` ingestion queries.

---

## 🛠️ Infrastructure Provisioning and Workspace Launch

### Prerequisites
Before initializing the graph persistence plane, confirm that the Phase 3 analytics stack (`subcontext-c-lakehouse`) is active and its underlying container network bridge (`subcontext-c-lakehouse_lh_network`) is live.

### Step 1: Initialize the Graph Container Instance
Navigate to this subdirectory and trigger the container lifecycle loops via the host shell:
```bash
cd subcontext-d-graph
docker compose up -d
```

### Step 2: Establish Unique Schema Keys (Mandatory Deadlock Prevention)
To protect the underlying storage engine from parallel transaction lock contentions, navigate your browser to `http://localhost:7474`, authenticate with user `neo4j` and password `graph_password123`, and execute these key index assertions sequentially inside the query bar:

```cypher
CREATE CONSTRAINT FOR (u:User) REQUIRE u.user_id IS UNIQUE;
CREATE CONSTRAINT FOR (ip:IPAddress) REQUIRE ip.ip_string IS UNIQUE;
```

### Step 3: Run the Ingestion Pipeline
1. Connect to the containerized Jupyter Lab instance running at `http://localhost:8888`.
2. Locate and launch the `graph_sync_lab.ipynb` workbook.
3. Run the validation cell blocks to populate the topological database blocks safely.

---

## 🔬 Documented Infrastructure Workarounds & Trade-offs

### 1. The Java RFC Hostname Validation Invariant
The native `org.neo4j.spark.DataSource` connector relies on standard `java.net.URI` classes to parse input endpoints. Under strict RFC requirements, using underscores (`_`) within domain hostnames is an invalid format syntax, throwing immediate deployment failures when routing directly to the default `lh_neo4j` endpoint. We bypass this runtime parser restriction cleanly by injecting a dedicated, underscore-free network alias (**`neo4jhost`**) into the shared bridge network layer.

### 2. Resolving Multi-Threaded Batch Write Contentions
When dividing high-volume log inputs across multiple parallel processing tasks (`local[*]`), concurrent threads attempt to execute idempotent Cypher `MERGE` commands inside overlapping batches (`batch.size: 1000`) simultaneously. This causes multiple threads to request competing *Node Exclusive Locks* over identical entity records, forcing the internal **ForsetiClient** engine to throw runtime deadlock aborts. 

In this prototype sandbox environment, we eliminate write racing completely by dropping parallel execution steps and using **`.coalesce(1)`** to channel records through a single serialized write tunnel. 

*(Production note: At scale, this issue must be addressed by partitioning data blocks explicitly via a hash key array or implementing application-level exponential backoff retries to preserve throughput).*

### 3. Synthetic Data Uniformity Limitations
Because our synthetic telemetry log data lake is generated via homogenic uniform randomness models (`Faker` random streams), the connection profiles across multi-tenant locations map out with a flat frequency weight of exactly 1. To bypass this baseline gürültüsü and extract meaningful node patterns, engineers must run multi-entity composite filters—matching identical device fingerprints alongside network endpoints concurrently.
