# Chapter 11 — Database Scaling

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 10 — Service Mesh & Service Discovery](ch10-service-mesh-and-service-discovery.md) · Next → [Chapter 12 — Event-Driven Systems](ch12-event-driven-systems.md)

---

## Concept

Read replicas, caching, sharding (key selection), partitioning, and the read/write split.

**In one sentence:** you scale a database in steps — tune queries and indexes, scale the machine up, add a cache and read replicas for reads, partition large tables, and only then shard writes across many databases by a carefully chosen key — because each step adds complexity the previous one didn't.

### Advanced Database Topics

#### Scaling Strategies — A Recap

##### Vertical Scaling (Scale-Up)

- **Definition:** Boost the capacity of a single server (more CPU, RAM, SSD).
- **Typical with:** Relational/SQL databases.
- **Pros:** Simpler setup; strong consistency via ACID.
- **Cons:** Limited by hardware ceilings; cost grows non-linearly; single point of failure.

```mermaid
graph TD
    A[Application Server] --> B[(SQL Database)]
    B -.-> |Scale Up| C[Add CPU/RAM/SSD]
```

##### Horizontal Scaling (Scale-Out)

- **Definition:** Add more servers/nodes to distribute load and data.
- **Typical with:** NoSQL databases.
- **Pros:** Elastic scalability; handles large-scale traffic and big data; better fault tolerance.
- **Cons:** Increased operational complexity; weaker consistency (often eventual).

```mermaid
graph TD
    A[App Server] --> B1[(NoSQL Node 1)]
    A --> B2[(NoSQL Node 2)]
    A --> B3[(NoSQL Node 3)]
    B1 -. Replicated Data .-> B2
    B1 -. Replicated Data .-> B3
```

**When to use which?**

- **SQL / Vertical:** Banking, ERP, transactional systems.
- **NoSQL / Horizontal:** Social feeds, product catalogs, IoT, analytics.

#### The Database Scaling Ladder

Scale a database in steps, because each step adds complexity the previous one did not. Climb in order:

| Step | Helps | Cost |
|------|-------|------|
| 1. Query and index tuning, connection pooling (for example PgBouncer) | everything | engineering time |
| 2. Vertical scaling | everything, instantly | money; there is a ceiling |
| 3. Caching | read-heavy hot data | invalidation and staleness |
| 4. **Read replicas** | read throughput; isolating reports | replication lag, so stale reads |
| 5. Table **partitioning** (inside one database) | huge tables: time-based retention, index size | queries must know the partition key |
| 6. Functional split | different domains on different databases | joins across domains disappear |
| 7. **Sharding** | write throughput and data size beyond one node | cross-shard queries and transactions, resharding, operations |

**The read/write split and its consistency cost.** Writes go to the primary and reads go to replicas. Asynchronous replicas lag (milliseconds, sometimes seconds under load), so a user who just saved a profile may read the old one. Fixes: **read-your-writes routing** (read from the primary for a few seconds after a write, or wait until the replica has reached the write's log position), sticky routing for critical reads, and monitoring replica lag.

#### Replication

**Replication** copies data across multiple database nodes for redundancy and increased throughput.

**Benefits:**

- **Fault Tolerance:** If one node fails, others can serve data.
- **Read Scalability:** Distribute read load across replicas.
- **Data Availability:** Users access data despite node failures.

##### Leader-Follower (Primary-Replica) Replication

(See `image-7.png` for a primary-replica diagram.)

- **All writes** go to the **Leader**.
- **Reads** can go to **Followers** (replicas).
- **Asynchronous replication** may cause followers to lag (eventual consistency).
- **Synchronous replication** offers strong consistency but can impact availability.

```mermaid
graph TD
    Leader[Leader Node] --Writes--> Leader
    Leader --Replicates--> F1[Follower 1]
    Leader --Replicates--> F2[Follower 2]
    Clients -->|Reads| F1
    Clients -->|Reads| F2
```

```
           +------------+
           |  Leader    |
           +-----+------+
                 |
         +-------+--------+
         |                |
     +---+----+      +----+---+
     |Follower|      |Follower|
     +--------+      +--------+
```

A wider topology view:

```
      +-------+         +--------+      +--------+
      |Leader |  --->   |Follower| ...  |Follower|
      +-------+         +--------+      +--------+
        (writes)           (reads)         (reads)
```

##### Read Replicas

(See `image-6.png` for a read-replica diagram.)

- **Purpose:** Scale read-heavy workloads.
- **All writes** go to the primary; **reads** are balanced across replicas.
- **Trade-off:** Potential for stale reads if replication lags.

##### Multi-Leader Replication and Conflict Resolution

In leader-follower replication, only the leader accepts writes. In **multi-leader** (also called leader-leader or multi-master) replication, **several nodes accept writes** and copy them to each other.

**Why use it:**

- **Multi-region writes:** each region writes to a nearby leader for low latency.
- **No single write bottleneck or single point of failure** for writes.
- **Offline-capable clients:** a phone or laptop acts like a small leader that syncs later.

**The price: write conflicts.** Two leaders can change the same row at the same time, and each only learns of the other's change after replication lag.

```mermaid
sequenceDiagram
    participant A as Leader A (Europe)
    participant B as Leader B (US)
    Note over A,B: both start with title = "Draft"
    A->>A: set title = "Plan"
    B->>B: set title = "Roadmap"
    A-->>B: replicate "Plan"
    B-->>A: replicate "Roadmap"
    Note over A,B: conflict: which value wins?
```

**Ways to resolve a conflict:**

| Strategy | How | Trade-off |
|----------|-----|-----------|
| **Last write wins (LWW)** | keep the change with the latest timestamp | simple, but silently **loses** the other write, and clocks differ between machines |
| **Version vectors / vector clocks** | track causality to detect which changes were truly concurrent | detects conflicts precisely; something still has to decide |
| **Application-level merge** | store both versions and let the app, or the user, merge them | correct but more code |
| **CRDTs** | data types designed to merge automatically (counters, sets, text) | no lost updates; limited to suitable data shapes |
| **Avoid conflicts** | route all writes for a given record to one leader (by user, region or key) | simplest and most common; gives up some of the multi-leader benefit |

**Rule of thumb:** use multi-leader only when you truly need multi-region writes or offline sync, and design around conflicts from the start. Otherwise prefer leader-follower plus read replicas.

##### Example: Configuring Read Replicas in PostgreSQL

```bash
# On the primary server (postgresql.conf)
wal_level = replica
max_wal_senders = 10
hot_standby = on

# On the replica server
standby_mode = 'on'
primary_conninfo = 'host=primary_ip user=replicator password=secret'
```

#### Sharding

As systems outgrow the capacity of a single node, **sharding** divides data across multiple databases or nodes.

##### Types of Sharding

- **Horizontal sharding:** Split data by rows — e.g., user_id ranges.
- **Vertical sharding:** Split by feature/domain — e.g., profiles vs. analytics.

##### Sharding Strategies

**a) Range-Based Sharding:**

- **How:** Data split by value ranges (e.g., user_id 1-1000 → Shard A).
- **Pro:** Simple, intuitive.
- **Con:** Risk of hotspots if data is skewed.

**b) Hash-Based Sharding:**

- **How:** Apply a hash function to a key (e.g., user_id) for shard assignment.
- **Pro:** Even distribution.
- **Con:** Range queries are hard; re-sharding is painful.

```python
def get_shard(user_id, num_shards):
    return hash(user_id) % num_shards

# Usage example
shard_index = get_shard(12345, 4)  # returns shard index 0-3
```

**c) Consistent Hashing:**

Solves the re-sharding problem: only a small subset of keys move when adding/removing nodes.

```mermaid
graph TD
    C1[Node A]
    C2[Node B]
    C3[Node C]
    Ring((Hash Ring))
    Ring --> C1
    Ring --> C2
    Ring --> C3
```

```
[Node1]---[Node2]---[Node3]---[Node1]
   |          |        |        |
[Key1]    [Key2]   [Key3]   [Key4]
```

> Only a subset of keys are remapped when nodes are added/removed.

**d) Geo-Based Sharding:**

- **How:** Shard by geographic region for latency/compliance.
- **Use Case:** Social media, CDN, regionally regulated data.

##### Choosing a Shard Key, Hot Spots and Cross-Shard Queries

| Good key | Why | Watch out for |
|----------|-----|---------------|
| `tenant_id` or `user_id` | most queries are "for this user"; spreads evenly | very large tenants ("whales") need dedicated shards |
| a hash of an entity ID | even distribution | range queries across the whole set need scatter-gather |
| composite `(user_id, time bucket)` | bounds the growth per key | more complex routing |
| **Bad:** `created_at`, `country`, `status` | all new writes hit one shard; low cardinality | **hot shards** |

**Hot spots.** A celebrity account, a viral post, or a steadily increasing key concentrates load on one shard. Mitigate by hashing the key, adding salt or suffix buckets for hot keys, giving whales dedicated shards, and caching hot reads.

**Cross-shard queries.** Scatter the query to all shards and merge the results (slower, and tail latencies add up); maintain global secondary indexes or denormalized lookup tables; send analytics to a warehouse instead; and avoid cross-shard transactions, using sagas instead.

**Routing.** Either the application computes the shard (through a library), or a proxy does it (Vitess, Citus, ProxySQL), using consistent hashing or a **directory** (a key-to-shard map) that makes moving data easier.

##### Hands-On Lab: Sharding MongoDB on One Machine

This lab builds the real architecture of a sharded MongoDB cluster. For learning, every process runs on one machine with a single member per replica set; production uses three or more members per set and separate hosts.

**The pieces:**

| Component | Job |
|-----------|-----|
| **Config server** (a replica set) | stores the cluster's metadata: which key ranges live on which shard |
| **Shards** (each a replica set) | hold the actual data |
| **`mongos` router** | the entry point applications talk to; it routes each query to the right shard(s) |

**1. Start the processes** (each in its own terminal, with its own data folder):

```bash
mkdir -p data/cfg data/shardA data/shardB
mongod --configsvr --replSet cfg    --port 27019 --dbpath data/cfg
mongod --shardsvr  --replSet shardA --port 27018 --dbpath data/shardA
mongod --shardsvr  --replSet shardB --port 27028 --dbpath data/shardB
```

**2. Initiate each replica set:**

```bash
mongosh --port 27019 --eval 'rs.initiate({_id:"cfg", configsvr:true, members:[{_id:0, host:"localhost:27019"}]})'
mongosh --port 27018 --eval 'rs.initiate({_id:"shardA", members:[{_id:0, host:"localhost:27018"}]})'
mongosh --port 27028 --eval 'rs.initiate({_id:"shardB", members:[{_id:0, host:"localhost:27028"}]})'
```

**3. Start the router and connect to it:**

```bash
mongos --configdb cfg/localhost:27019 --port 27017
mongosh --port 27017
```

**4. Add the shards, enable sharding and choose a shard key:**

```javascript
sh.addShard("shardA/localhost:27018")
sh.addShard("shardB/localhost:27028")
sh.enableSharding("shop")
sh.shardCollection("shop.orders", { user_id: "hashed" })   // hash-based: even spread
```

**5. Load data and see how it spread:**

```javascript
use shop
for (let i = 0; i < 20000; i++) db.orders.insertOne({ user_id: i, total: i % 100 })
db.orders.getShardDistribution()   // roughly half the documents on each shard
sh.status()
```

**What to notice:**

- A **hashed** key spreads writes evenly but makes **range queries** on `user_id` hit every shard. A **ranged** key (`{ user_id: 1 }`) keeps neighbours together but can create a **hot shard** if new ids always increase.
- A query that includes the shard key goes to one shard; one that does not is **scattered** to all shards. This is why shard-key choice is the most important sharding decision (see Sharding Strategies above).
- Clean up by stopping the processes and deleting the `data` folder.

#### Polyglot Persistence

**Polyglot persistence** means using multiple database types in one architecture, choosing the best tool for each job.

**Why:** Each DB excels at different tasks (search, analytics, relationships).

**Benefit:** Better performance, optimized storage.

| Data Need           | Recommended DB           | Example Use Case            |
|---------------------|--------------------------|-----------------------------|
| Relationships       | Relational (PostgreSQL)  | User profiles, transactions |
| Flexible Documents  | Document (MongoDB)       | Product catalogs            |
| Fast Key Access     | Key-Value (Redis)        | Caching, session storage    |
| Full-Text Search    | Search Engine (Elastic)  | Search functionality        |
| Analytics           | Columnar (Cassandra)     | Log/metrics pipelines       |

##### Example: Microservices with Polyglot Persistence

```mermaid
graph LR
    A[User Service] --> SQL[(PostgreSQL)]
    B[Product Service] --> DOC[(MongoDB)]
    C[Search Service] --> ES[(Elasticsearch)]
    D[Analytics Service] --> CASS[(Cassandra)]
```

*(From AI Library chapter 7.)*

### Database Performance Optimization Techniques

#### Replication

**Replication** is the process of copying and maintaining database objects in multiple places. Critical for:

- **High availability:** If one node fails, replicas ensure continued service.
- **Load balancing:** Distribute read traffic among replicas.
- **Disaster recovery:** Data is safe even if a site goes down.

**Types of replication:**

- **Master-Slave Replication:** One primary (master) handles writes, read-only slaves handle queries.
- **Master-Master Replication:** Multiple primaries handle reads and writes, offering redundancy.

(See `image-19.png` for Master-Slave vs Master-Master diagram.)

> **Tip:** Use master-slave for simple read scaling; master-master for HA and fault tolerance, but beware of write conflicts.

#### Sharding & Partitioning

##### Sharding

**Sharding** splits large datasets across multiple servers (shards), each holding a subset of the data. Enables horizontal scaling.

**Example:** Users partitioned by geographic region.

```mermaid
graph LR
    A[Client] --> B[Shard 1: US]
    A[Client] --> C[Shard 2: EU]
    A[Client] --> D[Shard 3: ASIA]
```

##### Partitioning

**Partitioning** divides data inside a single database:

- **Range partitioning:** e.g., Orders partitioned by order date.
- **Hash partitioning:** Each record assigned to a partition based on a hash of a key (e.g., user_id).

```sql
-- Example: Range Partitioning by Order Date (Postgres)
CREATE TABLE orders (
  id serial PRIMARY KEY,
  created_at date NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2023 PARTITION OF orders
  FOR VALUES FROM ('2023-01-01') TO ('2023-12-31');
```

> **Tip:** Sharding is for scaling *across servers*; partitioning is for organizing data *within a server*.

#### CAP Theorem (Performance Perspective)

The **CAP Theorem** states that in a distributed system, you can only guarantee two of:

- **Consistency:** All nodes see the same data at the same time.
- **Availability:** Every request gets a response (even if not the latest).
- **Partition Tolerance:** System works even if network splits occur.

| Type | Guarantees                       | Use When…                            |
|------|----------------------------------|--------------------------------------|
| CP   | Consistency + Partition Tolerance | Banking, strong consistency needed   |
| AP   | Availability + Partition Tolerance | Social feeds, eventual consistency OK |

> **Performance note:** Prioritizing availability (AP) often improves performance at scale but may introduce temporary inconsistencies.

#### Indexes

An **index** is a data structure (like a B-tree or hash table) that lets the database quickly find data without scanning every row.

(See `image-20.png` for index types.)

**Types of indexes:**

- **B-Tree:** Default in most DBs; supports range and exact queries.
- **Hash:** Fast for equality lookups; no range support.
- **Full-Text:** For searching large blocks of text.
- **Bitmap:** Efficient for columns with few unique values (low cardinality).

**When to use:**

- **Read-heavy operations:** Indexes speed up query performance.
- **Write-heavy systems:** Be cautious — indexes can slow down inserts and updates.

```sql
-- B-Tree index (default)
CREATE INDEX idx_user_id ON users (id);

-- Hash index (Postgres)
CREATE INDEX idx_user_email_hash ON users USING hash (email);

-- Full text (Postgres)
CREATE INDEX idx_article_content ON articles USING GIN (to_tsvector('english', content));

-- Adding a regular email index
CREATE INDEX idx_user_email ON users(email);
```

> **Tip:** Indexes accelerate reads but slow down writes. Use them judiciously.

#### Normalization vs. Denormalization

(See `image-21.png` for diagram.)

##### Normalization

- **Goal:** Reduce data redundancy by organizing data into tables.
- **Benefits:** Minimizes storage costs and eliminates anomalies.
- **Drawback:** Can lead to complex joins and slower read performance.
- Splits data into related tables to reduce redundancy. Ideal for transactional (OLTP) systems.

##### Denormalization

- **Goal:** Introduce redundancy to reduce join operations and speed up reads.
- **Benefits:** Faster read performance.
- **Drawback:** Increased storage and potential data anomalies.
- Best for reporting/analytics (OLAP).

##### When to Use Each

- **Normalization:** For transactional systems (OLTP).
- **Denormalization:** For reporting systems or read-heavy workloads.

**Example:**

- *Normalized:* Separate `users` and `orders` tables, joined by `user_id`.
- *Denormalized:* Store user info directly in `orders` for faster reporting.

```sql
-- Normalized
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id;

-- Denormalized: No join needed
SELECT customer_name, amount
FROM orders_denormalized;
```

> **Tip:** Normalize for consistency; denormalize for read performance (especially in reporting / data warehouse scenarios).

#### Connection Pooling

(See `image-22.png` for diagram.)

**Definition:** A technique to manage database connections efficiently by **reusing established connections** instead of creating new ones each time.

**Why use it?**

- **Reduces overhead** caused by frequent connection creation and teardown.
- **Helps handle** a large number of concurrent connections effectively.

```python
# Python with SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=20, max_overflow=0
)
```

A `psycopg2` example:

```python
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(1, 20, user='user', password='pass', database='db')

def get_conn():
    return db_pool.getconn()
```

A Node.js + Postgres example:

```javascript
const { Pool } = require('pg');
const pool = new Pool({ max: 10 });

pool.query('SELECT * FROM products', (err, res) => { /* ... */ });
```

> **Tip:** Always use connection pooling for web apps and microservices to avoid exhausting DB resources under load.

#### Query Optimization

Techniques to make queries run faster:

- **Use indexes** (as above).
- **Avoid N+1 queries:** Fetch all needed data in one query using joins or batching.
- **Optimize joins:** Join only necessary tables, and ensure join columns are indexed.

```sql
-- Bad: N+1
SELECT * FROM orders WHERE user_id = 123;
-- Then for each order...
SELECT * FROM order_items WHERE order_id = ?;

-- Good: Use JOIN
SELECT o.*, oi.*
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = 123;
```

#### Materialized Views

(See `image-23.png` for diagram.)

**Definition:** A precomputed query result stored as a table.

**Benefits:**

- **Speeds up query performance** by avoiding real-time computation.
- Useful in **reporting** and **data warehousing**.

**Use cases:**

- Data aggregation or summary data that doesn't change frequently.
- Reporting systems where fast retrieval is critical.

```sql
CREATE MATERIALIZED VIEW sales_summary AS
SELECT region, SUM(total)
FROM sales
GROUP BY region;

-- Refresh periodically as needed
REFRESH MATERIALIZED VIEW sales_summary;
```

#### Batching & Pagination

##### Batching

- **Definition:** Sending multiple operations in a single request or transaction to reduce overhead.
- **Use case:** Bulk inserts or updates.

##### Pagination

- **Definition:** Breaking large sets of data into smaller chunks for efficient retrieval.
- **Prevents** large queries that could lead to timeouts or memory issues.
- **Ensures** responsive UI by fetching data incrementally.

```sql
-- Batch Insert (Postgres)
INSERT INTO users (name, email)
VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com');

-- Pagination
SELECT * FROM products ORDER BY id LIMIT 50 OFFSET 100;
```

> **Tip:** Always paginate API and UI queries to prevent performance bottlenecks.

#### Database Optimization — Quick Reference

| Technique           | Use For                       | Caution / Trade-off                     |
|---------------------|-------------------------------|------------------------------------------|
| Replication         | HA, load balancing            | Data sync lag, write conflicts (multi-master) |
| Sharding            | Scale-out large datasets      | Complexity in resharding, cross-shard queries |
| Indexing            | Fast reads                    | Slower writes, increased storage         |
| Normalization       | Consistency, OLTP             | Slower complex reads                     |
| Denormalization     | Fast analytics/OLAP           | Data redundancy, integrity risk          |
| Connection Pooling  | Reducing connection overhead  | Pool exhaustion under huge spikes        |
| Query Optimization  | Fast queries                  | Over-optimization can add complexity     |
| Materialized Views  | Fast reporting queries        | Stale data unless refreshed              |
| Batching            | Bulk inserts/updates          | Transaction size limits                  |
| Pagination          | UI, API data navigation       | Inaccurate results on data change        |

#### Database Optimization — Layered Architecture Diagram

```mermaid
graph TD
  A[Client/API]
    --> B[Connection Pool]
    --> C[App Server]
    --> D[Database]
    D --> E[Replication / Sharding]
    D --> F[Indexes]
    D --> G[Partitioning]
    D --> H[Materialized Views]
```

*(From AI Library chapter 8.)*

The diagram, worked example, exercises, mini-project, design prompt, open-source reading, interview questions and checklist below are this chapter's practice layer.

---

## Prereqs

* [Vol 1 Ch 45 — SQL & the Relational Model](../volume-1-cs-foundations/ch45-sql-and-the-relational-model.md)
* [Vol 1 Ch 46 — Schema Design, Normalization & Indexing](../volume-1-cs-foundations/ch46-schema-design-normalization-and-indexing.md)
* [Vol 1 Ch 47 — ACID, Transactions & Isolation](../volume-1-cs-foundations/ch47-acid-transactions-and-isolation.md)

---

## Diagram

**A primary + replicas diagram**

```mermaid
flowchart LR
    APP["app"] -->|"writes"| P[("primary")]
    APP -->|"reads (may lag)"| RP["read pool / proxy"]
    RP --> R1[("replica 1")]
    RP --> R2[("replica 2")]
    P -->|"WAL streaming (async)"| R1 & R2
    P -->|"sync standby (failover)"| SB[("standby, other zone")]
    P -->|"logical replication"| AN[("analytics replica")]
```

**Replication lag and read-your-writes**

```
 t=0 ms   user saves name "Ada"  → primary (LSN 1000)
 t=5 ms   user reloads            → replica at LSN 990 → shows the OLD name ✗
 fix: after a write, remember LSN 1000 in the session; route reads to a replica only
      once it has replayed ≥ 1000 (or read from the primary for ~2 s)
```

**A sharded database with a routing layer**

```mermaid
flowchart LR
    APP["app"] --> ROUTER["router (Vitess / library)<br/>shard = hash(user_id) → vshard map"]
    ROUTER --> S1[("shard 1<br/>users A…<br/>primary + replicas")]
    ROUTER --> S2[("shard 2")]
    ROUTER --> S3[("shard 3")]
    ROUTER --> S4[("shard 4")]
    ROUTER -. "scatter-gather for<br/>cross-shard queries" .-> S1 & S2 & S3 & S4
```

**A hot shard**

```
 shard key = created_date      today's shard  ████████████████████  (100% of writes)
                               other shards   ░                      (idle)
 shard key = hash(user_id)     shard 1..4     █████ █████ █████ █████  (even)
```

---

## Example

```sql
-- Declarative partitioning in Postgres (one database, many partitions)
CREATE TABLE events (
  id          bigint GENERATED ALWAYS AS IDENTITY,
  user_id     bigint NOT NULL,
  occurred_at timestamptz NOT NULL,
  payload     jsonb,
  PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2024_05 PARTITION OF events FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
CREATE TABLE events_2024_06 PARTITION OF events FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
-- retention: DROP TABLE events_2023_05;   (instant, instead of a huge DELETE)
-- queries with WHERE occurred_at … touch only the relevant partitions (partition pruning)
```

```python
# Application-level shard routing with a directory of virtual shards
import hashlib

N_VSHARDS = 1024                                 # fixed; many more than physical shards
VSHARD_TO_DB = {v: f"db{v % 4}" for v in range(N_VSHARDS)}   # directory: move vshards to rebalance

def vshard(user_id: int) -> int:
    return int.from_bytes(hashlib.md5(str(user_id).encode()).digest()[:4], "big") % N_VSHARDS

def db_for(user_id: int) -> str:
    return VSHARD_TO_DB[vshard(user_id)]

print(db_for(42), db_for(43))
# Adding db4: move some vshards' data, then update the directory entries — no global rehash.
```

```python
# Read-your-writes with replicas
def read_profile(session, user_id):
    recent_write = session.get("last_write_ts", 0) > time.time() - 2
    conn = primary if recent_write else replicas.pick()
    return conn.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,)).fetchone()
```

---

## Exercises

1. Choose a shard key and explain hot spots.

   <details><summary>Solution</summary>For a multi-tenant SaaS: <code>tenant_id</code> — nearly every query filters by tenant, so queries stay on one shard and a tenant's data is co-located for joins. Hot spot: one huge tenant can overwhelm its shard; mitigate by giving whales dedicated shards (directory-based placement) or by sub-sharding them by <code>(tenant_id, hash(entity_id))</code>. Avoid time-based keys (all writes go to the newest shard) and low-cardinality keys.</details>

2. Add a read replica and route reads to it.

   <details><summary>Solution</summary>Create a streaming replica; send writes and "must be fresh" reads (right after a write, checkout, balances) to the primary, and everything else (feeds, search, reports) to the replica pool via a proxy or two connection pools. Monitor replica lag and remove a replica from the pool when lag exceeds a threshold. Put heavy analytics on a separate replica so it can't slow user reads.</details>

3. Why is `SELECT … ORDER BY created_at LIMIT 20` across 16 shards expensive?

   <details><summary>Solution</summary>The router must ask all 16 shards for their top 20 (320 rows), merge-sort, and return 20. Latency is set by the slowest shard, and deep pagination (<code>OFFSET 10000</code>) multiplies the work on every shard. Use keyset pagination, a denormalized global timeline or index, or a search or analytics system for global queries.</details>

---

## Mini project

**A sharded-store simulator with a consistent-hashing router.**

```mermaid
flowchart LR
    W["workload generator<br/>Zipf users, reads/writes,<br/>1 celebrity user"] --> R["router<br/>modes: modulo · ring · vshard directory"]
    R --> S1["shard sim 1 (SQLite)"] & S2["shard 2"] & S3["shard 3"] & S4["shard 4"]
    OPS["ops: add shard, move vshards,<br/>replica lag injection"] --> R
    R --> M["metrics: load per shard,<br/>keys moved on resize,<br/>cross-shard query latency,<br/>stale reads"]
```

**Steps**

1. Four SQLite files as shards; a router that implements modulo, a consistent-hash ring, and a virtual-shard directory.
2. A workload with Zipf-distributed users plus one celebrity.
3. Add a fifth shard under each mode and count the rows that must move.
4. Implement scatter-gather for a global "latest 20" query and measure its latency vs a single-shard query.
5. Simulate replica lag and show stale reads with and without read-your-writes routing.

**Done when:** the metrics show modulo moving ~80% of keys on resize vs ~20% for the ring or directory, the celebrity creates a visible hot shard, and read-your-writes eliminates stale reads.

---

## Design

**Design the data tier for a social feed (sharding + replicas).**

Requirements: 200 M users, 50 M DAU, 100 M posts/day, 10 B feed reads/day, p99 feed read < 100 ms.

```mermaid
flowchart LR
    API["feed API"] --> CACHE[("Redis: precomputed timelines<br/>user_id → last 800 post IDs")]
    API --> POSTS["posts store<br/>sharded by author_id (vshards)<br/>primary + 2 replicas per shard"]
    API --> SOCIAL[("follow graph<br/>sharded by user_id")]
    WRITE["new post"] --> POSTS
    WRITE --> FAN["fan-out workers (Kafka)<br/>push post ID to followers' timelines"]
    FAN --> CACHE
    CELEB["authors with > 1 M followers:<br/>no fan-out; merge at read time"] -.-> API
```

**Capacity**

| Item | Estimate |
|------|----------|
| Post writes | 100 M/day ≈ 1,160/s avg, ~6,000/s peak |
| Feed reads | 10 B/day ≈ 116k/s avg, ~580k/s peak → served from the timeline cache |
| Post storage | 100 M × 1 KB = 100 GB/day ≈ 36 TB/year (× 3 replicas ≈ 110 TB) |
| Shards | ~2 TB per shard → ~18 shards for one year; plan 32 physical, 4,096 virtual shards |
| Timeline cache | 50 M active users × 800 IDs × 8 B ≈ 320 GB → a Redis cluster of ~10 × 64 GB nodes with replicas |

**Decisions to justify**

* **Shard posts by `author_id`** — writes and "a user's own posts" stay on one shard; virtual shards allow rebalancing.
* **Feeds come from precomputed timelines in Redis** (fan-out on write), so reads never scatter across post shards; posts are then fetched by ID in batches.
* **Hybrid fan-out:** celebrities are excluded from fan-out and merged at read time to avoid millions of writes per post.
* **Read replicas** per shard for post lookups; read-your-writes for a user's own new post.
* **Analytics and search** go to separate systems fed by CDC, not the OLTP shards.

---

## Open source

* [`vitessio/vitess`](https://github.com/vitessio/vitess) — sharding middleware for MySQL (used by YouTube, Slack): vindexes, resharding workflows, and query routing.
* [`postgres/postgres`](https://github.com/postgres/postgres) (replication) — streaming and logical replication, declarative partitioning; see also Citus for distributed Postgres.

---

## Interview

1. **"How do you choose a shard key?"**
   <details><summary>Answer</summary>Pick the key most queries filter on, so each query touches one shard; with high cardinality and even distribution of load (not just data); that keeps related data together for joins and transactions; and that doesn't concentrate new writes (avoid time or monotonic keys). Plan for hot keys (dedicated shards or salting) and use virtual shards or a directory so you can rebalance later.</details>

2. **"Read replicas — consistency cost?"**
   <details><summary>Answer</summary>Replicas usually replicate asynchronously, so reads can be stale by milliseconds to seconds (more under load or during long transactions). That breaks read-your-writes, monotonic reads across replicas, and uniqueness checks done on a replica. Mitigate with primary reads after writes, LSN-aware routing, sticky replica selection, lag monitoring and ejection, and sending only lag-tolerant reads to replicas.</details>

---

## Checklist

- [ ] avoid hot shards
- [ ] handle cross-shard queries
- [ ] balance read scale vs staleness

---

> [Contents](index.md) · ← [Chapter 10 — Service Mesh & Service Discovery](ch10-service-mesh-and-service-discovery.md) · Next → [Chapter 12 — Event-Driven Systems](ch12-event-driven-systems.md)
