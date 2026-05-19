# End-to-End Relational-Document Hybrid Core & Real-Time Medallion Lakehouse Pipeline

This repository serves as a production-grade engineering sandbox simulating a high-volume enterprise e-commerce data platform. The architecture bridges a hardened relational-document hybrid transaction hub (OLTP) natively with a multi-tiered distributed stream-processing Delta Lakehouse pipeline (OLAP) entirely within a local containerized sandbox.

## 🏗️ System Architecture Overview

```text
  [ Active Web Users ] ➔ Telemetry Generation
         │
         ├── (Writes Checked Transactions) ➔ [ PostgreSQL 16 Node (OLTP) ]
         │                                          │
         └── (Streams In-App Click Log Strings)     │ (Distributed JDBC Sync)
                     │                              │
                     ▼                              ▼
        [ Apache Kafka Broker (29092) ] ➔ ➔ [ PySpark Computing Engine ]
                                                    │
                                                    ▼ (Medallion Pipeline ETL)
                                       [ MinIO S3 Object Storage ]
                                         ├── bronze/ (Raw Append Log)
                                         ├── silver/ (Cleaned & Parsed)
                                         └── gold/   (Data Mart Aggregates)
```
## 📁 Repository Directory Structure

```text
ecommerce-database-engineering/
│
├── README.md                       # Master Engineering Landing Page Documentation
│
├── subcontext-a-modeling/          # PHASE 1: Core Hybrid Database Design
│   ├── README.md                   # Relational-Document validation & schema boundaries playbook
│   └── ddl_schema.sql              # Invariant SQL columns + Dynamic JSONB Catalog Ingestion DDL
│
├── subcontext-b-optimization/      # PHASE 2: Performance Engineering & Stress Testing Labs
│   ├── scripts/
│   │   ├── generate_mock_data.py   # 1M Row Data Generation Pipeline (HashSet Unique Ingestion)
│   │   └── query_performance_tracker.py # Query Planner Telemetry (EXPLAIN PLAN Extractor JSON parser)
│   ├── slow_queries.sql            # Unindexed Baseline Queries (Forcing Disk Sorts/Seq Scans)
│   ├── optimized_queries.sql       # GIN, Expression, Covered, and Trigram Index Layouts
│   └── performance_report.md       # Automated Benchmarking Output Telemetry Matrix
│
└── subcontext-c-lakehouse/         # PHASE 3: Stream-Processing Data Lakehouse Architecture
    ├── docker-compose.yml          # Container Orchestration (Kafka, Zookeeper, MinIO, PySpark JVM)
    └── notebooks/
        ├── bronze_to_gold_etl.ipynb # Real-Time Streaming Medallion ETL & Multi-Model Join Engine
        └── kafka_data_injector.ipynb # High-Velocity Clickstream Event Producer Script
```

---

## 🏛️ Phase-by-Phase Technical Blueprint

### Phase 1: Relational-Document Hybrid Modeling (`subcontext-a-modeling/`)
* **Objective:** Solve Object-Relational Impedance Mismatch without microservice network partitioning overhead.
* **Core Mechanics:** Implements targeted validation boundaries inside **PostgreSQL 16**. Uses rigid relational fields (`Schema-on-Write`) for core immutable data assets paired with binary `JSONB` components (`Hybrid Schema Enforcement`) for polymorphic category metadata. Freezes financial transaction histories into an immutable fixed checkout price layout matching **IFRS 15** and **US GAAP ASC 606** specifications.

### Phase 2: Query Optimization Engineering (`subcontext-b-optimization/`)
* **Objective:** Stress-test database layout boundaries under 1,000,000 transaction row thresholds and bypass the Index Scan Trap.
* **Core Mechanics:** Programmatic indexing benchmarks analyzing interior execution variables (`Shared Hit / Read` pages). Features specialized GIN containment indices (`jsonb_path_ops`), expression indexing on nested JSON fields, and covered index layouts (`INCLUDE`) to transform sequential memory crawls into high-speed **Index Only Scans**.

### Phase 3: Real-Time Medallion Data Lakehouse (`subcontext-c-lakehouse/`)
* **Objective:** Decouple analytic lookups from transaction nodes using stream-processing architecture.
* **Core Mechanics:** Real-time event capture via **Apache Kafka**. Parallel micro-batch workloads orchestrated on **PySpark** routing datasets inside **Delta Lake** transaction tables mapped on **MinIO Object Storage**:
  * **Bronze:** Append-only replication tracking raw payload telemetry with strict `earliest` offset pointers.
  * **Silver:** Micro-batch evaluation (`from_json`) schema validation, and null-tracking quality fences.
  * **Gold:** Stateful aggregations using complete output modes forced via strict compute trigger intervals.
* **Multi-Model Memory Brokerage:** Merges operational user configurations natively inside cluster memory using distributed JDBC driver parameters targeting the PostgreSQL 16 loopback bridge interface (`host.docker.internal:5433`) to shield the relational core from transactional processing overhead.

---

## 🛠️ Local Environment Sandbox Deployment

### Prerequisites
* Ensure you have [Docker Desktop](https://docker.com) initialized and active.
* Python 3.10+ with active Python virtual environments (`venv`) for localized data stress testing scripts.

### 1. Activating the Operational Core (Phase 1 & 2)
Provision an active PostgreSQL instance exposed locally on port `5433`. Run the database schema migrations located inside `subcontext-a-modeling/ddl_schema.sql`.

To inject 1,000,000 mock transactions and evaluate the query planner telemetry:
```bash
cd subcontext-b-optimization
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_mock_data.py
python scripts/query_performance_tracker.py
```

### 2. Spinning Up the Distributed Big Data Stack (Phase 3)
To mount your local S3 storage layers, real-time message brokers, and parallel computing workers, execute the orchestration blueprint:
```bash
cd subcontext-c-lakehouse
docker compose up -d
```

Verify your active sandbox endpoints using local browser proxies:
* **MinIO Object Storage Console UI:** `http://localhost:9001` (User: `admin` / Password: `minio_password123`)
* **Jupyter Lab Spark Interface Workspace:** `http://localhost:8888` (Secure Token: `lakehouse_secret_2026`)
* **Spark Live Tracking Engine UI Console:** `http://localhost:4040`

Open your Jupyter Lab interface, navigate to the `work/notebooks/` workspace directory, launch `kafka_data_injector.ipynb` to simulate real-time user clickstream traffic, and initiate the core ingestion loop via `bronze_to_gold_etl.ipynb`.

---

## 📚 Documented Publications

This data engineering workspace maps directly to our step-by-step architectural technical series on Medium. Review the articles for comprehensive runtime telemetry analyses, internal memory breakdowns, and structural deep dives:

* **Part 1:** [Relational-Document Hybrid Modeling inside PostgreSQL 16](YOUR_MEDIUM_LINK_1)
* **Part 2:** [Beyond the Basics: GIN Indexes, In-Memory Telemetry, and the Query Planner Paradox](YOUR_MEDIUM_LINK_2)
* **Part 3:** [Shifting Scales: Implementing Multi-Tiered Real-Time Delta Lakehouse Patterns in a Local Sandbox](YOUR_MEDIUM_LINK_3)