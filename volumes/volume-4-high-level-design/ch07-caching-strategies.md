# Chapter 7 — Caching Strategies

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 6 — Load Balancing](ch06-load-balancing.md) · Next → [Chapter 8 — Rate Limiting, Throttling & Backpressure](ch08-rate-limiting-throttling-and-backpressure.md)

---

## Concept

Cache-aside, write-through/write-around/write-back, invalidation, TTLs, stampedes, cache coherence.

**In one sentence:** a cache is a small, fast copy of slow data, and every caching strategy is a different answer to one question — *when the data changes, who updates the copy?*

### Caching for Speed Optimization

Caching is one of the most powerful levers for reducing latency, easing backend load, and scaling systems.

#### Why Caching Matters

- **Reducing latency:** Serve requests in milliseconds by avoiding repeated trips to databases or recomputing results.
- **Easing backend load:** Offload expensive queries or computations from databases.
- **Improving scalability:** Handle more users with the same infrastructure.
- **Enhancing user experience:** Faster response times = happier users.

**Diagram: Caching in a Web Application**

```mermaid
flowchart LR
    User-->|HTTP Request| WebServer
    WebServer-->|Check Cache| Cache[(In-memory Cache)]
    WebServer-->|Cache Miss| DB[(Database)]
    DB-->|Return Data| WebServer
    Cache-->|Cache Hit| WebServer
    WebServer-->|HTTP Response| User
```

```
[User] --> [App Server] --> [Cache (Redis)] --> [DB]
                  ^             |
                  |<-- cache hit|
```

#### Types of Caching

| Type                | Where it Lives             | Example Tools / Tech                   | Use Case                                  |
|---------------------|----------------------------|----------------------------------------|--------------------------------------------|
| **Client-side**     | User's browser/device      | localStorage, Service Workers, IndexedDB | Offline support, quick navigation        |
| **Server-side**     | Application server memory  | Redis, Memcached                       | Session tokens, user data, computed results|
| **CDN caching**     | Content Delivery Networks  | Cloudflare, Akamai                     | Static assets (JS, CSS, images), API responses |
| **Database caching**| Database result-set cache  | Redis, Materialized Views              | Expensive queries, analytics              |

#### Caching Strategies

##### Write-Through Caching

(See `image-10.png` for diagram.)

- **How it works:** Data is written to both the cache and the database at the same time.
- **Pro:** Consistency is guaranteed; cache is always fresh.
- **Con:** Adds latency to write operations.

```python
def write(key, value):
    cache.set(key, value)  # Update cache
    db.save(key, value)    # Update database
```

##### Write-Back (Write-Behind) Caching

(See `image-11.png`.)

- **How it works:** Data is written to the cache first and asynchronously persisted to the database later.
- **Pro:** Fast write performance.
- **Con:** Risk of data loss if cache fails before DB is updated.

```python
def write(key, value):
    cache.set(key, value)
    # Schedule async write to DB
    schedule_async_db_write(key, value)
```

##### Lazy Loading (Cache-Aside)

(See `image-12.png`.)

- **How it works:** On reads, check cache first. If not found (cache miss), fetch from DB, return, and populate cache.
- **Pro:** Only hot (frequently accessed) data is cached.
- **Con:** First access is slow ("cold" cache).

```python
def read(key):
    value = cache.get(key)
    if value is None:
        value = db.get(key)
        cache.set(key, value)
    return value
```

##### Explicit / Manual Caching

- **How it works:** Developers decide explicitly when and what to cache.
- **Pro:** Maximum flexibility.
- **Con:** Higher complexity, risk of staleness if not managed well.

#### Cache Eviction Policies

(See `image-13.png`.)

Caches have limited memory, so old or less useful data must be evicted.

| Policy                          | Description                              | When to Use                              |
|---------------------------------|------------------------------------------|------------------------------------------|
| **LRU (Least Recently Used)**   | Remove the least recently accessed item  | Default choice, general use              |
| **LFU (Least Frequently Used)** | Remove item with fewest access hits      | When some items are rarely used          |
| **FIFO (First In, First Out)**  | Remove oldest item added                 | Simplicity, but less intelligent         |
| **TTL (Time To Live)**          | Expire items after a fixed time          | Time-sensitive data (API responses, sessions) |

#### Redis: The Caching Powerhouse

[Redis](https://redis.io/) is an open-source, in-memory key-value store, renowned for its blazing speed:

- **Ultra-fast access:** Everything is in RAM.
- **Supports TTL:** Automatic expiry of keys.
- **Persistence:** Can save cache to disk for durability.
- **Pub/Sub messaging:** For real-time event systems.
- **Versatile:** Caching, queues, session storage, leaderboards.

**Redis caching in Python:**

```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_user_profile(user_id):
    cached = cache.get(f"profile:{user_id}")
    if cached:
        return cached
    profile = db_get_profile(user_id)
    cache.setex(f"profile:{user_id}", 60, profile)  # 60s TTL
    return profile
```

A simpler version:

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Set cache with 10-minute TTL
r.setex('user:123', 600, '{"name": "Alice", "age": 30}')

# Get cache
user_data = r.get('user:123')
```

**LRU cache in Python (`functools`):**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_product(product_id):
    # Simulate DB fetch
    return fetch_product_from_db(product_id)
```

**Redis caching in Node.js + Express:**

```javascript
const express = require('express');
const redis = require('redis');
const app = express();

const redisClient = redis.createClient(); // default localhost:6379

app.get('/api/product/:id', async (req, res) => {
    const productId = req.params.id;

    redisClient.get(`product:${productId}`, async (err, cached) => {
        if (cached) {
            return res.json(JSON.parse(cached)); // Cache hit
        }

        // Simulate DB fetch
        const product = await fetchProductFromDB(productId);

        // Cache with TTL of 10 minutes
        redisClient.setex(`product:${productId}`, 600, JSON.stringify(product));

        res.json(product);
    });
});

function fetchProductFromDB(productId) {
    return Promise.resolve({ id: productId, name: "Sample Product" });
}

app.listen(3000, () => console.log("Server running on port 3000"));
```

#### Real-World Caching Examples

- **CDN:** Static assets (images, JS, CSS) cached near users for instant load times.
- **E-commerce:** Product catalog queries cached to avoid repeated expensive DB hits.
- **User sessions:** Session data stored in Redis for quick login checks.
- **Search:** Frequently searched keywords/results cached to save compute cycles.
- **Microservices:** API responses cached to reduce downstream service load.

| Use Case               | Cache Type   | Tool             |
|------------------------|--------------|------------------|
| Static assets (images) | CDN          | Cloudflare       |
| User sessions          | Server-side  | Redis            |
| Product page data      | Server-side  | Redis/Memcached  |
| API responses          | Server-side  | Redis            |

#### Caching — Tips & Tricks

- **Always measure:** Use metrics to identify what should be cached (hot queries).
- **Apply TTL smartly:** Especially on volatile or time-sensitive data.
- **Prevent cache stampede:** Use locks or request coalescing to avoid thundering herd problems.
- **Monitor cache health:** Watch hit/miss rates, eviction rates, memory usage.
- **Automate cache invalidation:** Design carefully for dynamic content (on writes or updates).
- **Choose the right cache layer:** Not all data should be cached everywhere.
- **Secure your caches:** Protect against unauthorized access for sensitive data.
- **Combine eviction policies:** E.g., LRU + TTL for the best of both worlds.

---

#### Choosing a Write Strategy and Reading the Numbers

**The latency ladder.** Why caching pays off:

| Source | Typical latency | Relative to an in-process cache |
|--------|-----------------|---------------------------------|
| In-process memory (dictionary, LRU) | about 100 ns | 1× |
| Redis or Memcached, same region | about 0.5 ms | about 5,000× |
| Database query, indexed | about 5 ms | about 50,000× |
| Database query, complex join | about 50–500 ms | about 1,000,000× |
| Cross-region call | about 70–150 ms | about 1,000,000× |

**Hit rate is the number to watch.** A 95% hit rate turns a 50 ms average read into roughly `0.95 × 0.5 + 0.05 × 50 ≈ 3 ms`.

**The four write strategies side by side**

| Strategy | Read path | Write path | Good for | Risk |
|----------|-----------|------------|----------|------|
| **Cache-aside** (lazy loading) | check the cache, on a miss read the database and fill the cache | write the database, then **delete** the cache key | most read-heavy apps; the default choice | the first read after a change is slow; race windows |
| **Write-through** | read from the cache | write the cache **and** the database together | data read right after it is written | every write pays double latency; caches cold data |
| **Write-around** | like cache-aside | write the database only; the cache fills on the next read | write-once, read-rarely data (logs, uploads) | recent writes always miss |
| **Write-back** (write-behind) | read from the cache | write the cache only; flush to the database later | a very high write rate (counters, metrics) | **data loss** if the cache dies before the flush |

**Key terms:** **TTL** (a safety net for missed invalidations); **invalidation** (removing or updating a value when its source changes); **stampede** (a hot key expires and thousands of requests miss at once and hit the database; stop it with a lock or single-flight, TTL jitter, or early refresh); **cache coherence** (keeping many copies, such as several cache nodes or per-server local caches, in agreement); **eviction** (what is thrown out when the cache is full: LRU, LFU, random).

*(From AI Library chapter 8.)*

### Cache Patterns — The Full Picture

| Pattern        | How it works                                                           | Use when                                  |
|----------------|-------------------------------------------------------------------------|-------------------------------------------|
| **Cache-aside** (lazy loading) | App reads cache; on miss, reads DB and populates cache | Default for read-heavy data with infrequent writes |
| **Read-through** | App always reads cache; cache itself fetches from DB on miss          | When you want app code to not know about the DB |
| **Write-through** | Writes go to cache and DB at the same time                            | Strong consistency requirement; OK with write latency |
| **Write-back** (write-behind) | Writes go to cache; DB updated async                         | Write-heavy; can tolerate data loss on cache crash |
| **Write-around** | Writes go directly to DB, bypassing cache                              | Writes rarely re-read soon (cold data) |

> **For most apps, cache-aside is the right default.** Simple, predictable, doesn't require special cache libraries.

*(From AI Library chapter 8.)*

The diagram, worked example, exercises, mini-project, design prompt, open-source reading, interview questions and checklist below are this chapter's practice layer.

---

## Prereqs

* [Vol 1 Ch 49 — Redis, Elasticsearch, Neo4j & Vector Databases](../volume-1-cs-foundations/ch49-redis-elasticsearch-neo4j-and-vector-databases.md) (Redis).

---

## Diagram

**Cache-aside: read path**

```mermaid
sequenceDiagram
    participant App
    participant Cache as Redis
    participant DB as Database
    App->>Cache: GET product:42
    alt hit
        Cache-->>App: value ✅ (~0.5 ms)
    else miss
        Cache-->>App: nil
        App->>DB: SELECT * FROM products WHERE id = 42
        DB-->>App: row (~20 ms)
        App->>Cache: SET product:42 row EX 300
    end
```

**Cache-aside: write path** — update the DB, then *delete* (not update) the key.

```mermaid
sequenceDiagram
    participant App
    participant DB as Database
    participant Cache as Redis
    App->>DB: UPDATE products SET price = 9.99 WHERE id = 42
    DB-->>App: ok
    App->>Cache: DEL product:42
    Note over Cache: next read misses and reloads fresh data
```

**Where each write strategy sends data**

```
 Cache-aside            Write-through          Write-around           Write-back
 ───────────            ─────────────          ────────────           ──────────
   App                     App                    App                    App
   │  write               │  write               │  write               │  write
   ▼                      ▼                      │                      ▼
   DB ──► DEL cache      Cache ──sync──► DB      ▼                     Cache
                                                 DB   (cache untouched)  │ async, batched
                                                                         ▼
                                                                         DB (later)
```

**The stampede, and three ways to stop it**

```
  t = 0          hot key "feed:home" expires
  t = 0 + 1 ms   ┌──────────────────────────────────────────────┐
                 │ 5,000 requests ── miss ── miss ── miss ──►   │ DB 💥
                 └──────────────────────────────────────────────┘
```

```mermaid
flowchart TD
    M[Cache miss on hot key] --> L{"Got lock?<br/>SET lock NX EX 5"}
    L -->|yes, 1 request| R[Rebuild from DB] --> S[SET value] --> U[Release lock]
    L -->|no, 4,999 requests| W[Wait 50 ms, retry cache] --> H[Hit fresh value]
```

| Fix | Idea |
|-----|------|
| **Lock / single-flight** | Only one request rebuilds; the rest wait for its result. |
| **TTL jitter** | `ttl = 300 + random(0, 60)` so keys created together don't expire together. |
| **Early refresh** (probabilistic) | Refresh slightly *before* expiry; the closer to expiry, the more likely a request refreshes it. |

---

## Example

**Cache-aside in Python with Redis**

```python
import json, random
import redis

r = redis.Redis()
BASE_TTL = 300  # seconds

def get_product(product_id: int) -> dict:
    key = f"product:{product_id}"

    cached = r.get(key)
    if cached is not None:                       # 1. hit
        return json.loads(cached)

    row = db.fetch_product(product_id)           # 2. miss → go to DB
    ttl = BASE_TTL + random.randint(0, 60)       # 3. jitter the TTL
    r.set(key, json.dumps(row), ex=ttl)          # 4. fill the cache
    return row

def update_price(product_id: int, price: float) -> None:
    db.update_price(product_id, price)           # 1. source of truth first
    r.delete(f"product:{product_id}")            # 2. then invalidate
```

**Stampede protection with a lock**

```python
import time

def get_product_safe(product_id: int) -> dict:
    key, lock = f"product:{product_id}", f"lock:product:{product_id}"

    for _ in range(20):                          # ~1 s of retries
        cached = r.get(key)
        if cached is not None:
            return json.loads(cached)

        if r.set(lock, "1", nx=True, ex=5):      # only one caller wins
            try:
                row = db.fetch_product(product_id)
                r.set(key, json.dumps(row), ex=BASE_TTL + random.randint(0, 60))
                return row
            finally:
                r.delete(lock)

        time.sleep(0.05)                          # losers wait, then re-check

    return db.fetch_product(product_id)           # fallback: never fail the read
```

**Why "delete" beats "update" on write** — two writers racing:

```
 Writer A: UPDATE db price=10      Writer B: UPDATE db price=12
 Writer B: SET cache price=12
 Writer A: SET cache price=10      ← cache now says 10, DB says 12 ❌ (stale forever, until TTL)

 With DEL instead of SET, both writers just delete. The next read loads 12 from the DB. ✅
```

---

## Exercises

1. **Implement cache-aside.** Wrap a slow function (`time.sleep(0.2)` then return a value) with cache-aside using a Python `dict` plus expiry timestamps. Measure average latency for 1,000 reads over 50 keys.

   <details><summary>Hint</summary>Store <code>(value, expires_at)</code>. On read, treat <code>time.time() &gt; expires_at</code> as a miss. You should see the average drop from ~200 ms to under 10 ms.</details>

2. **Fix cache stampede with locking or jitter.** Start 200 threads that all read the same expired key. Count how many reach the "database". Then add a lock and count again.

   <details><summary>Solution sketch</summary>Without protection the count is close to 200. With a <code>threading.Lock</code> per key plus a second cache check after acquiring the lock (double-checked locking), the count drops to 1.</details>

3. **Pick a strategy.** For each, choose cache-aside, write-through, write-around, or write-back: (a) product catalog, (b) page-view counter, (c) uploaded audit logs, (d) user profile shown right after editing.

   <details><summary>Answer</summary>(a) cache-aside · (b) write-back · (c) write-around · (d) write-through.</details>

---

## Mini project

**A cache layer with invalidation + stampede protection.**

```mermaid
flowchart LR
    C[Client] --> A[API]
    A --> CL[Cache layer<br/>get / set / invalidate]
    CL -->|hit| A
    CL -->|miss + lock| DB[(Postgres)]
    DB -->|change event| INV[Invalidator] -->|DEL key| CL
    CL --> MET[Metrics:<br/>hit rate, p99, DB QPS]
```

**Steps**

1. Build a `CacheLayer` class with `get(key, loader)`, `invalidate(key)`, and a configurable TTL + jitter.
2. Add single-flight locking so concurrent misses on one key call `loader` once.
3. Invalidate on write: every DB update calls `invalidate`.
4. Export three numbers: hit rate, p99 latency, DB queries per second.
5. Load-test with 10,000 requests where 20% of keys get 80% of traffic.

**Done when:** hit rate stays above 90%, and killing a hot key under load causes exactly one DB query.

---

## Design

**Design a caching layer for a product feed.**

Requirements: 10 M daily users; the home feed shows 50 products; prices change a few times a day; the feed must load in under 100 ms p99.

```mermaid
flowchart LR
    U[Users] --> CDN[CDN<br/>static images]
    U --> LB[Load balancer] --> API[Feed API x N]
    API --> L1[L1: in-process LRU<br/>TTL 5 s]
    L1 -->|miss| L2[L2: Redis cluster<br/>TTL 5 min + jitter]
    L2 -->|miss + lock| DB[(Product DB<br/>read replicas)]
    DB -. CDC price change .-> K[Kafka] -.-> INV[Invalidator] -. DEL .-> L2
```

**Decisions to justify**

* **Two layers.** L1 absorbs hot-key traffic with no network hop. A short TTL keeps its staleness bounded.
* **Cache the feed *and* the products separately.** `feed:home → [ids]` and `product:{id} → details`. A price change invalidates one product, not every feed.
* **Invalidation via change-data-capture (CDC).** The DB change stream drives deletes, so no code path can "forget" to invalidate.
* **Capacity.** 1 M products × ~2 KB ≈ 2 GB. That fits in a small Redis cluster, with replicas for reads and failover.
* **Failure mode.** If Redis is down, fall back to replicas with a circuit breaker, and serve a stale L1 copy rather than an error.

---

## Open source

* [`redis/redis`](https://github.com/redis/redis) — read `src/expire.c` to see how Redis expires keys (lazy on access + active sampling), and `src/evict.c` for approximated LRU/LFU.
* [`memcached/memcached`](https://github.com/memcached/memcached) — read `items.c` and the slab allocator to see a pure cache with no persistence at all.

---

## Interview

1. **"Cache-aside vs write-through?"**
   <details><summary>Answer</summary>Cache-aside: the app manages the cache, loads lazily on miss, and deletes on write. It is simple, only caches what is read, and survives cache failure, but the first read is slow and there are race windows. Write-through: every write updates cache and DB together, so reads after writes are always fresh, but writes are slower and the cache fills with data nobody reads. Default to cache-aside; use write-through where read-after-write freshness matters.</details>

2. **"How do you invalidate safely?"**
   <details><summary>Answer</summary>Write the DB first, then delete (not set) the key. Always keep a TTL as a safety net. Drive invalidation from the DB's change stream (CDC) so no code path is missed. For strict cases, use versioned keys (<code>product:42:v7</code>) so old values can never be read as new. Add jitter and single-flight to survive the resulting misses.</details>

---

## Checklist

- [ ] set TTLs with jitter
- [ ] avoid stampedes
- [ ] treat cache coherence as a problem to solve, not ignore

---

> [Contents](index.md) · ← [Chapter 6 — Load Balancing](ch06-load-balancing.md) · Next → [Chapter 8 — Rate Limiting, Throttling & Backpressure](ch08-rate-limiting-throttling-and-backpressure.md)
