# Phase 1: Relational-Document Hybrid Architecture (OLTP Core)

This subdirectory contains the database migration scripts and structural blueprints for the core transactional (OLTP) engine of our enterprise e-commerce platform.

## 🏛️ Architectural Overview

This tier establishes a **Relational-Document Hybrid Layout** inside a single **PostgreSQL 16** primary node. It balances two conflicting data velocities to resolve Object-Relational Impedance Mismatch:

1. **Relational Schema-on-Write Invariants:** Applied to high-compliance static zones (`users`, `order_items`) where strict transactional attributes are enforced at the write boundary.
2. **Hybrid Schema Enforcement:** Applied to highly polymorphic, sparse catalog metadata and logistical telemetry arrays (`products.attributes`, `orders.payment_details`) using optimized binary `JSONB` formats.

---

## 📁 File Manifest

*   `ddl_schema.sql`: The hardened production DDL migration script containing full relational data types, primary/foreign key hierarchies, and cascading deletion structures.

---

## 🛠️ Local Ingestion & Validation Steps

### Prerequisites
* An operational instance of **PostgreSQL 16** exposed locally on port `5433`.
* A database client tool (e.g., pgAdmin, DBeaver, or the VS Code Database Client extension).

### Step 1: Initialize Database Target
Connect to your local PostgreSQL instance and provision a dedicated logical database cluster core:
```sql
CREATE DATABASE ecommerce_db;
```

### Step 2: Execute Schema Migration
Run the contents of `ddl_schema.sql` against the active `ecommerce_db` context to establish the tables.

---

## 📈 Key Engineering Decisions Documented Here

### 1. Financial Snapshot Pattern (IFRS 15 / US GAAP ASC 606)
The table `order_items` includes an explicit, immutable `purchased_price DECIMAL(10,2)` column. Catalog base prices change continuously due to marketing promotions or inflation metrics. To comply with regulatory revenue recognition rules, the transaction price is permanently determined and frozen at the exact millisecond of checkout completion, preventing historical transaction records from modifying retroactively.

### 2. The Decentralized Consistency Shift
Nesting dynamic properties inside a `JSONB` matrix shifts structural consistency verification boundaries. While PostgreSQL guarantees absolute Atomicity, Isolation, and Durability (WAL logs), structural validation logic is split. Malformed JSON segments (e.g., missing currency components) will pass database-level ingestion checks, shifting complex data constraint filtering workflows upstream to high-performance application validation frameworks (`Pydantic` / `Zod`).

---

## 📚 Corresponding Publication
This sub-context maps directly to the first installment of our technical engineering series on Medium:  
🔗 **[Relational-Document Hybrid Modeling inside PostgreSQL 16](YOUR_MEDIUM_LINK_HERE)**
