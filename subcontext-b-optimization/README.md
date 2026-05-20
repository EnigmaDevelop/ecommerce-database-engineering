# Phase 2: Query Optimization & Performance Engineering Labs

This subdirectory contains the automated benchmarking scripts, data stress pipelines, and optimization profiles executed against our 1,000,000 transaction row database.

## 🏗️ Architectural Objectives

This lab stress-tests our unified Relational-Document Hybrid database core under high-volume duress. The primary engineering milestone is to analyze the internal cost metrics of the **PostgreSQL 16 Query Planner**, document structural indexing anti-patterns (The Index Scan Trap), and configuration limits (`work_mem`, Visibility Maps).

---

## 📁 Repository Manifest

*   `scripts/generate_mock_data.py`: High-speed data generation engine injecting controlled relational and document data skew via the native Postgres `COPY` framework.
*   `scripts/query_performance_tracker.py`: Real-time benchmark monitor extracting background telemetry metrics (`Shared Hit/Read` buffers) into localized JSON checkpoints.
*   `scripts/compile_ultimate_report.py`: Aggregation script compiling separate iteration runs into a unified markdown telemetry matrix.
*   `slow_queries.sql`: Raw unindexed wildcard matching and deep hierarchical JSONB pointer searches.
*   `optimized_queries.sql`: GIN containment, Expression B-Tree, and Covered Index (`INCLUDE`) fine-tuning scripts.
*   `performance_report.md`: The dynamic, empirical output file generated directly by the hardware execution cluster.

---

## 📊 Iterative Benchmarking Workflow Execution Yönergesi

To reproduce the exact sub-millisecond execution times and capture the structural database paradox loops cleanly:

### Step 1: Initialize Database Schema & Data Generation
Ensure your core relational DDL schema inside Phase 1 is fully active. Execute the bulk ingestion pipeline to inject 100,000 unique users and 1,000,000 orders:
```bash
python scripts/generate_mock_data.py
```

### Step 2: Capture Unindexed Baseline Telemetry
Execute the tracker engine with the baseline arg to stamp your raw metrics onto disk:
```bash
python scripts/query_performance_tracker.py "Before Optimization"
```

### Step 3: Trigger the Index Trap Paradox (Phase 2.1)
Run the textbook indexing scripts inside `optimized_queries.sql` (Standard B-Tree + Expression Index + GIN `jsonb_path_ops`). Recalculate your catalog statistics via `ANALYZE;` and capture the performance degradation:
```bash
python scripts/query_performance_tracker.py "First Index Attempt"
```

### Step 4: Deploy Advanced Trigram & Covered Structs (Phase 2.2)
Drop the non-performing B-Tree layout. Initialize the `pg_trgm` module, construct the Covered Index pattern, allocate `SET work_mem = '64MB';`, and execute a full database `VACUUM ANALYZE;`. Run the final telemetry cycle:
```bash
python scripts/query_performance_tracker.py "Covered Final Fine Tuning"
```

### Step 5: Compile the Final Engineering Matrix Report
```bash
python scripts/compile_ultimate_report.py
```

---

## 📚 Corresponding Publication
This sub-context maps directly to the second installment of our technical engineering series on Medium:  
🔗 **[Beyond the Basics: GIN Indexes, In-Memory Telemetry, and the Query Planner Paradox in PostgreSQL](YOUR_MEDIUM_LINK_HERE)**
