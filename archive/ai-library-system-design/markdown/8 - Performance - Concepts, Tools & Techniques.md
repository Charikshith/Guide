# Mastering System Design: Performance Concepts, Tools & Techniques

Performance is the heart of modern system design. It's not just about how fast your system runs — it's about how well it scales, how it responds under pressure, and how efficiently it utilizes resources. In this chapter, we'll break down the essential pillars of performance: latency, throughput, caching, messaging queues, concurrency, and database optimization.

---

## 8.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Reason about **p50, p95, p99** latency and explain why averages lie.
2. Pick the right caching strategy (cache-aside, write-through, write-back) for a workload.
3. Diagnose and prevent **cache stampedes** and the **thundering herd** problem.
4. Spot the **N+1 query** problem in code and fix it.
5. Size a database connection pool correctly (smaller than you think).

---

## Table of Contents

- [8.2 Introduction to System Performance](#82-introduction-to-system-performance)
- [8.3 Key Metrics — Latency, Throughput, Scalability & Responsiveness](#83-key-metrics--latency-throughput-scalability--responsiveness)
- [8.4 Measuring Performance — SLAs, SLOs, SLIs, and Percentiles](#84-measuring-performance--slas-slos-slis-and-percentiles)
- [8.5 Performance Testing & Monitoring](#85-performance-testing--monitoring)
- [8.6 Caching for Speed Optimization](#86-caching-for-speed-optimization)
- [8.7 Messaging & Queues for Decoupling](#87-messaging--queues-for-decoupling)
- [8.8 Concurrency & Parallelism](#88-concurrency--parallelism)
- [8.9 Database Performance Optimization Techniques](#89-database-performance-optimization-techniques)
- [8.13 Combined Tips & Tricks](#813-combined-tips--tricks)
- [8.14 Sample Interview Questions](#814-sample-interview-questions)
- [8.15 Summary & Key Takeaways](#815-summary--key-takeaways)
- [8.16 Further Reading](#816-further-reading)

---

## 8.2 Introduction to System Performance

Performance in system design is a **multidimensional goal** — balancing speed, scalability, and efficiency:

- **Speed:** How quickly does your system respond? (Measured as latency.)
- **Capacity:** How much work can it handle at once? (Measured as throughput.)
- **Efficiency:** How well does it use resources under stress? (CPU, memory, network.)

> **Performance is not a single metric — it's about achieving the right balance for your application.**

### 8.2.1 Why Performance Matters

- **User expectations:** Slow systems lose users and revenue.
- **Business impact:** Performance affects drop-offs, bounce rates, and costs.
- **System stability:** Poor performance leads to instability and outages.

> **Performance is a feature, not an afterthought.**

---

## 8.3 Key Metrics — Latency, Throughput, Scalability & Responsiveness

### 8.3.1 Latency vs. Throughput

| Metric      | Description                          | Unit       | Affects                |
|-------------|--------------------------------------|------------|------------------------|
| Latency     | Time to process a single request     | ms, s      | Responsiveness         |
| Throughput  | Requests processed per second        | RPS, TPS   | Scalability            |

> **Note:** Low latency ≠ high throughput. Both must be balanced per use case.

### 8.3.2 Code: Measuring Latency and Throughput (Python)

```python
import time
import requests

def measure_latency(url):
    start = time.time()
    response = requests.get(url)
    latency = time.time() - start
    return latency

def measure_throughput(url, n_requests):
    start = time.time()
    for _ in range(n_requests):
        requests.get(url)
    total_time = time.time() - start
    return n_requests / total_time

print("Latency:", measure_latency("https://example.com"))
print("Throughput:", measure_throughput("https://example.com", 100), "req/sec")
```

### 8.3.3 Diagram: Latency vs. Throughput

```
|--- Latency ---|
[Client]----request---->[Server]----response---->[Client]
            (1 request)
Throughput = Requests handled in 1 second
```

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: Request 1
    Server-->>Client: Response 1 (Latency)
    Client->>Server: Request 2
    Server-->>Client: Response 2
    Note over Server: Throughput = Total requests/time
```

### 8.3.4 Scalability vs. Responsiveness

- **Scalability:** Can the system handle more load as users/data grow?
  - **Horizontal scaling:** Adding more servers.
  - **Vertical scaling:** Increasing resources of existing servers.
- **Responsiveness:** How quickly the system replies, even under heavy load. Tightly linked to latency.

> **Goal:** Good design should ensure responsiveness at scale.

---

## 8.4 Measuring Performance — SLAs, SLOs, SLIs, and Percentiles

### 8.4.1 SLAs, SLOs, and SLIs

- **SLA (Service Level Agreement):** External contractual performance guarantee.
- **SLO (Service Level Objective):** Internal performance target.
- **SLI (Service Level Indicator):** Actual measured value.

**Example:**

```
SLA: 99.9% uptime for customers
SLO: 95% of requests < 300ms latency
SLI: Actual: 93% of requests < 300ms (need improvement!)
```

### 8.4.2 Percentiles: P50, P95, P99

**Why not just use averages?** Because averages hide outliers.

- **P50:** 50% (median) requests are faster.
- **P95:** 95% of requests are faster; 5% are slower.
- **P99:** The slowest 1% (tail latency) — critical for user experience.

**Visualization:**

```
|----|------------------|------------------|------------------|----|
  0%   50% (P50)         95% (P95)          99% (P99)         100%
```

---

## 8.5 Performance Testing & Monitoring

### 8.5.1 Performance Testing Types

| Type             | Description               | Goal                        |
|------------------|---------------------------|-----------------------------|
| Load Testing     | Normal expected load      | Baseline performance        |
| Stress Testing   | Beyond normal load        | Graceful degradation/crash  |
| Spike Testing    | Sudden burst load         | Absorb traffic spikes       |
| Endurance (Soak) | Extended duration load    | Memory leaks / fatigue      |

**Goal:** Identify bottlenecks & ensure reliability.

#### 8.5.1.1 CLI Example: Load Testing with `wrk`

```bash
wrk -t8 -c400 -d30s https://yourapi.com/api/endpoint
```

### 8.5.2 Performance Monitoring

- **Testing** is pre-deployment; **monitoring** is continuous in production.
- **APM tools:** New Relic, Datadog.
- **Logs & metrics:** ELK stack, Prometheus + Grafana.

**What to track:**

- Latency & throughput.
- Error rates.
- Resource usage (CPU, memory, DB queries).

---

## 8.6 Caching for Speed Optimization

Caching is one of the most powerful levers for reducing latency, easing backend load, and scaling systems.

### 8.6.1 Why Caching Matters

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

### 8.6.2 Types of Caching

| Type                | Where it Lives             | Example Tools / Tech                   | Use Case                                  |
|---------------------|----------------------------|----------------------------------------|--------------------------------------------|
| **Client-side**     | User's browser/device      | localStorage, Service Workers, IndexedDB | Offline support, quick navigation        |
| **Server-side**     | Application server memory  | Redis, Memcached                       | Session tokens, user data, computed results|
| **CDN caching**     | Content Delivery Networks  | Cloudflare, Akamai                     | Static assets (JS, CSS, images), API responses |
| **Database caching**| Database result-set cache  | Redis, Materialized Views              | Expensive queries, analytics              |

### 8.6.3 Caching Strategies

#### 8.6.3.1 Write-Through Caching

(See `image-10.png` for diagram.)

- **How it works:** Data is written to both the cache and the database at the same time.
- **Pro:** Consistency is guaranteed; cache is always fresh.
- **Con:** Adds latency to write operations.

```python
def write(key, value):
    cache.set(key, value)  # Update cache
    db.save(key, value)    # Update database
```

#### 8.6.3.2 Write-Back (Write-Behind) Caching

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

#### 8.6.3.3 Lazy Loading (Cache-Aside)

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

#### 8.6.3.4 Explicit / Manual Caching

- **How it works:** Developers decide explicitly when and what to cache.
- **Pro:** Maximum flexibility.
- **Con:** Higher complexity, risk of staleness if not managed well.

### 8.6.4 Cache Eviction Policies

(See `image-13.png`.)

Caches have limited memory, so old or less useful data must be evicted.

| Policy                          | Description                              | When to Use                              |
|---------------------------------|------------------------------------------|------------------------------------------|
| **LRU (Least Recently Used)**   | Remove the least recently accessed item  | Default choice, general use              |
| **LFU (Least Frequently Used)** | Remove item with fewest access hits      | When some items are rarely used          |
| **FIFO (First In, First Out)**  | Remove oldest item added                 | Simplicity, but less intelligent         |
| **TTL (Time To Live)**          | Expire items after a fixed time          | Time-sensitive data (API responses, sessions) |

### 8.6.5 Redis: The Caching Powerhouse

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

### 8.6.6 Real-World Caching Examples

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

### 8.6.7 Caching — Tips & Tricks

- **Always measure:** Use metrics to identify what should be cached (hot queries).
- **Apply TTL smartly:** Especially on volatile or time-sensitive data.
- **Prevent cache stampede:** Use locks or request coalescing to avoid thundering herd problems.
- **Monitor cache health:** Watch hit/miss rates, eviction rates, memory usage.
- **Automate cache invalidation:** Design carefully for dynamic content (on writes or updates).
- **Choose the right cache layer:** Not all data should be cached everywhere.
- **Secure your caches:** Protect against unauthorized access for sensitive data.
- **Combine eviction policies:** E.g., LRU + TTL for the best of both worlds.

---

### 8.6.8 Choosing a Write Strategy and Reading the Numbers

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

## 8.7 Messaging & Queues for Decoupling

Asynchronous messaging **decouples** services, boosts scalability, and enhances resilience.

### 8.7.1 Why Use Asynchronous Messaging?

Traditional synchronous calls force producers (e.g., APIs) to wait for consumers (e.g., email sender, payment processor) to finish their work. This **tightly couples** services and limits scalability.

(See `image-14.png` for sync vs. async comparison.)

**Asynchronous messaging decouples these components:**

- **Loose coupling:** Producers and consumers don't need to know about each other.
- **Performance:** Producers can send messages and move on immediately.
- **Scalability:** Consumers can scale independently.
- **Resilience:** If a consumer fails, messages are not lost.
- **Flexibility:** Add new consumers without touching producers.

### 8.7.2 Core Concepts

(See `image-15.png` for architecture overview.)

| Concept       | Description                                                 |
|---------------|-------------------------------------------------------------|
| **Message**   | Packet of data (JSON, binary, etc.)                         |
| **Producer**  | Sends message (e.g., order service)                         |
| **Consumer**  | Receives and processes messages (e.g., inventory updater)   |
| **Broker**    | Middleware that stores and routes messages (RabbitMQ, Kafka)|
| **Queue/Topic** | Logical channel for delivery                              |
| **Ack**       | Acknowledgement from consumer after successful processing   |

### 8.7.3 Typical Flow

```mermaid
sequenceDiagram
    participant Producer
    participant Broker
    participant Consumer
    Producer->>Broker: Send message (e.g., "OrderPlaced")
    Broker->>Consumer: Deliver message
    Consumer->>Broker: Ack (after processing)
```

For a **pub/sub event bus**:

```mermaid
graph TD
    Producer["Producer (Catalog Service)"] -->|Publish Event| Broker["Event Bus (e.g., Kafka)"]
    Broker -->|Subscribed| Consumer1["Basket Service"]
    Broker -->|Subscribed| Consumer2["Billing Service"]
    Broker -->|Subscribed| Consumer3["Analytics Service"]
```

A simpler view:

```mermaid
graph TD
    A[Producer] -- Sends Message --> B[Message Broker / Queue]
    B -- Delivers --> C[Consumer 1]
    B -- Delivers --> D[Consumer 2]
```

### 8.7.4 Real-World Example: Decoupled Order Processing

(See `image-16.png` for diagram.)

1. **Catalog Service** updates a product price.
2. After DB update, it publishes a `PriceUpdated` event to the broker.
3. **Basket Service** receives the event and updates any cart items with the old price.
4. **Billing** and **Analytics** services also subscribe to the event and trigger their own logic.
5. If any consumer is down, the message stays in the queue until it's back.

**Benefits:**

- **No direct calls** between services = no tight coupling.
- **Downstream failures** don't block the producer.
- **Easy to add new consumers** (e.g., promotions service).

### 8.7.5 When to Use Queues?

- **Bursty workloads:** Traffic spikes (flash sales), batch imports.
- **Background jobs:** Emails, processing, report generation, exports.
- **Rate limiting / expensive ops:** Spreading out heavy API calls or processing.
- **Buffering:** Smoothing out peaks to avoid overloading downstream systems.
- **Decoupling between services.**

### 8.7.6 Popular Message Brokers: RabbitMQ vs. Kafka

#### 8.7.6.1 RabbitMQ — Traditional Message Broker

- Built on AMQP, designed for reliable message delivery.
- Follows a **push-based model:** messages are pushed to consumers.
- Supports acknowledgements, retries, and dead-letter queues.
- Great for task distribution, background jobs, and real-time notifications.
- Focuses on **routing flexibility** (direct, topic, fanout exchanges).
- Messages are **removed after consumption.**

#### 8.7.6.2 Kafka — Distributed Event Streaming Platform

- Built for **high-throughput**, durable, distributed event logs.
- Uses a **pull-based model:** consumers read at their own pace.
- Stores messages in **partitioned logs;** supports message replay.
- Ideal for **event sourcing**, **real-time analytics**, and **stream processing**.
- Highly **scalable and fault-tolerant.**
- Messages are **retained for configurable durations** (even after consumption).

#### 8.7.6.3 RabbitMQ vs Kafka

| Feature        | RabbitMQ                          | Kafka                                |
|----------------|-----------------------------------|--------------------------------------|
| **Type**       | Message broker (AMQP)             | Event streaming platform             |
| **Model**      | Push-based                        | Pull-based                           |
| **Delivery**   | Messages delivered to consumers   | Consumers fetch from log             |
| **Use Case**   | Task queues, notifications, jobs  | Event sourcing, analytics, ETL       |
| **Retention**  | Message gone after consumption    | Retained for days; supports replay   |
| **Routing**    | Flexible (direct, topic, fanout)  | Partitioned topics                   |
| **Scale**      | Good                              | Excellent (built for high throughput)|

### 8.7.7 Delivery Guarantees

- **At-least-once** (default): Message retried until acknowledged; possible duplicates. *Consumer must be idempotent* (processing the same message twice has the same effect as once; see Chapter 9, Idempotency Keys).
- **At-most-once:** Message delivered only once (no retries); possible loss.
- **Exactly-once:** Processed once and only once; hardest to implement, supported by Kafka under constraints.

### 8.7.8 Delivery Semantics in Practice and the Outbox Pattern

| Semantic | How it works | Risk |
|----------|--------------|------|
| **At most once** | acknowledge **before** processing | a crash loses the message |
| **At least once** (the usual default) | acknowledge **after** processing | a crash after processing causes redelivery, so duplicates |
| **"Exactly once"** | at-least-once delivery **plus idempotent processing** (deduplicate by message ID, use upserts, store offsets together with results), or Kafka transactions for read-process-write inside Kafka | it holds end to end only if every side effect is idempotent or transactional |

**Rule:** design every consumer to be idempotent. True exactly-once *delivery* cannot be had across a network, so aim for exactly-once *effect*. "Exactly once" at the broker does not cover your database write or the email you sent.

**Failures and retries.** After N failed attempts, move the message to a **dead-letter queue** so one poison message cannot block the rest. Alert on its depth and provide a redrive tool. Use exponential backoff between retries (delay queues or retry topics).

**Consumer-group rebalance (Kafka).** When a consumer joins, leaves or stops sending heartbeats, partitions are reassigned within the group. Consumption pauses, and uncommitted work may be redone, which is one more reason for idempotency. Cooperative-sticky assignment and static membership reduce the disruption.

**The outbox pattern (solving the dual-write problem).** A service that updates its database *and* publishes an event can fail between the two steps. Instead, write the event to an **outbox table in the same database transaction** as the business change, and let a separate relay (or change-data-capture) publish rows from the outbox to the broker. The database and the event stream can then never disagree.

### 8.7.9 Ordering, FIFO Queues and Visibility Timeout

**Order is not free.** With several consumers working in parallel, messages can finish out of order even if they were sent in order.

| Setup | Ordering you get | Trade-off |
|-------|------------------|-----------|
| **Standard queue** (for example Amazon SQS standard) | best effort, may deliver out of order and more than once | very high throughput |
| **FIFO queue** (SQS FIFO) | strict first-in-first-out **within a message group** | lower throughput; ordering is per group, not global |
| **Partitioned log** (Kafka) | strict order **within a partition**; a key (such as a user ID) always lands in the same partition | no ordering across partitions; parallelism = number of partitions |

**Design rule:** order only what must be ordered. Pick the key (account ID, order ID) whose events must stay in sequence and route by it, so different keys can still be processed in parallel. If strict order is impossible, put a **sequence number** in each message and let the consumer discard or reorder stale ones.

**Visibility timeout.** When a consumer receives a message, the broker hides it from other consumers for a set time. If the consumer acknowledges before the timeout, the message is deleted. If it crashes or is too slow, the message becomes visible again and is retried. Set the timeout **longer than your slowest normal processing time**; too short causes duplicate work, too long delays retries after a crash. Messages that keep failing go to a **dead-letter queue** (see the queue primer in Chapter 4).

### 8.7.10 Queue Types: Standard, FIFO, Priority and Delay

| Queue type | Behaviour | Typical use |
|------------|-----------|-------------|
| **Standard** | best-effort ordering, at-least-once delivery | high-volume background work |
| **FIFO** | strict order within a group, exactly-once processing options | payments, ledger updates |
| **Priority** | higher-priority messages are delivered first, even if they arrived later | urgent notifications ahead of bulk email |
| **Delay** | a message becomes visible only after a set wait | reminders, retry after a pause |
| **Dead-letter** | receives messages that keep failing | inspection and replay of poison messages |

**Priority queues in practice:** some brokers support priorities natively (RabbitMQ does); others, such as Amazon SQS, do not, so the common pattern is **one queue per priority** with consumers polling the urgent queue first.

**Watch for starvation:** if urgent messages never stop arriving, low-priority ones may wait forever. Reserve some capacity for the low-priority queue, or **age** messages so their priority rises the longer they wait.

### 8.7.11 Sample Code: Publishing & Consuming Messages

#### 8.7.11.1 Example 1: RabbitMQ (Python with `pika`)

**Producer:**

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tasks')
channel.basic_publish(exchange='', routing_key='tasks', body='Hello World!')
connection.close()
```

A second producer variant:

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='orders')

channel.basic_publish(exchange='', routing_key='orders', body='{"order_id": 123}')
print("Sent order message.")
connection.close()
```

**Consumer (auto-ack):**

```python
def callback(ch, method, properties, body):
    print(f"Received {body}")

channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

**Consumer (with explicit ack):**

```python
import pika

def callback(ch, method, properties, body):
    print(f"Received {body}")
    # process order...
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='orders')
channel.basic_consume(queue='orders', on_message_callback=callback)

print('Waiting for messages...')
channel.start_consuming()
```

**Consumer with durable queue:**

```python
import pika

def callback(ch, method, properties, body):
    print("Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
```

#### 8.7.11.2 Example 2: Kafka (Node.js with `kafkajs`)

**Producer:**

```js
const { Kafka } = require('kafkajs');
const kafka = new Kafka({ clientId: 'producer', brokers: ['localhost:9092'] });

const producer = kafka.producer();
await producer.connect();
await producer.send({
  topic: 'order-events',
  messages: [{ value: JSON.stringify({ orderId: 123 }) }],
});
await producer.disconnect();
```

**Consumer:**

```js
const { Kafka } = require('kafkajs');
const kafka = new Kafka({ clientId: 'consumer', brokers: ['localhost:9092'] });

const consumer = kafka.consumer({ groupId: 'order-group' });
await consumer.connect();
await consumer.subscribe({ topic: 'order-events', fromBeginning: true });

await consumer.run({
  eachMessage: async ({ message }) => {
    const order = JSON.parse(message.value.toString());
    console.log('Received order:', order);
    // process order...
  }
});
```

### 8.7.12 Messaging — Best Practices

- **Idempotent consumers:** Ensure re-processing a message doesn't cause incorrect results.
- **Dead-letter queues (DLQ):** Capture and inspect messages that fail multiple times.
- **Monitor queues:** Track length and processing time to detect bottlenecks.
- **Graceful retries:** Use exponential backoff or circuit breakers.
- **Choose guarantees wisely:** At-least-once is common, but know your requirements.
- **Security:** Encrypt messages, use authentication & authorization.

### 8.7.13 Messaging — Tips & Tricks

- **Make operations idempotent:** Store processed message IDs or use database upserts.
- **Use DLQs:** Never silently drop or lose failing messages.
- **Monitor and alert:** Set up alerts for queue length, processing failures, and latency.
- **Don't block consumers:** Design consumers to be fast and non-blocking.
- **Automate scaling:** Use auto-scaling for consumer groups based on queue depth.
- **Tune prefetch/batch sizes:** For RabbitMQ, set channel prefetch; for Kafka, tune consumer batch size.

---

## 8.8 Concurrency & Parallelism

Unlocking performance often means handling **many tasks at once** — but how?

### 8.8.1 Concurrency vs. Parallelism

(See `image-17.png` for diagram.)

| Aspect        | Concurrency                                       | Parallelism                            |
|---------------|---------------------------------------------------|----------------------------------------|
| Definition    | Multiple tasks start/run/complete in overlapping time | Multiple tasks executed *simultaneously* |
| Hardware      | Single or multi-core                              | Multi-core required                    |
| Focus         | Task management (responsiveness)                  | Task execution (throughput)            |
| Example       | Async web server                                  | Matrix computation on threads          |

**Concurrency** is about *managing* multiple tasks at the same time. These tasks may overlap in their execution, but do not necessarily run simultaneously. It allows a system to handle multiple things at once, improving responsiveness, even on a single CPU core.

- Task management, not simultaneous execution.
- Can be achieved on a single-core CPU.
- Gives the *illusion* of doing many things at once by rapidly switching context.

**Example:** A web server handling multiple HTTP requests using asynchronous I/O.

```python
# Python asyncio concurrent server (single-threaded, concurrent)
import asyncio

async def handle_request(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    print(f"Received {message}")
    writer.write(data)
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_request, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

**Parallelism** is about *executing* multiple tasks at the same time. It requires multiple CPU cores. The goal is to increase *throughput* and speed.

- Actual simultaneous execution.
- Requires multi-core CPUs.
- Improves throughput and computational speed.

**Example:** Parallel matrix computation.

```python
from multiprocessing import Pool

def compute_square(x):
    return x * x

if __name__ == '__main__':
    with Pool(4) as p:  # 4 parallel processes
        results = p.map(compute_square, [1,2,3,4,5,6,7,8])
    print(results)
```

**Concurrency vs. Parallelism ASCII:**

```
Concurrency (Task Management)        Parallelism (Task Execution)
+------------------------------+     +--------------------------+
| Task A  | Task B | Task C    |     | Task A | Task B | Task C |
|========>|========|=========> |     |========|========|========|
|    (Interleaved, Overlapping)|     |(Executed Simultaneously)|
+------------------------------+     +--------------------------+
```

### 8.8.2 Processes vs. Threads

(See `image-18.png` for diagram.)

|                 | Process                          | Thread                       |
|-----------------|----------------------------------|------------------------------|
| **Memory**      | Own memory space                 | Shared memory within process |
| **Creation**    | Heavy, slow                      | Lightweight, fast            |
| **Isolation**   | Fully isolated                   | Less isolated, share data    |
| **Safety**      | Safer, one crash ≠ all crash     | Prone to race conditions     |
| **Use Case**    | Separate apps (browser, editor)  | Multiple tasks in app        |

**Examples:**

- **Processes:** Chrome and Word, each with its memory.
- **Threads:** Multiple HTTP request handlers in a web server, sharing cache.

### 8.8.3 Thread Pools & Worker Models

#### 8.8.3.1 Thread Pools

- **What:** Pre-created pool of threads reused for multiple tasks.
- **Why:** Avoids the overhead of creating/destroying threads per task.
- **Where:** Web servers (ASP.NET Core, Java, Python), database connection pooling.

```java
ExecutorService pool = Executors.newFixedThreadPool(8);
pool.submit(() -> {
    // handle request
});
```

```python
from concurrent.futures import ThreadPoolExecutor

def process_task(task_id):
    print(f"Processing {task_id}")

with ThreadPoolExecutor(max_workers=4) as executor:
    for i in range(10):
        executor.submit(process_task, i)
```

A simpler variant for a request handler:

```python
from concurrent.futures import ThreadPoolExecutor

def process_request(request):
    # Handle request
    pass

with ThreadPoolExecutor(max_workers=10) as executor:
    for req in incoming_requests:
        executor.submit(process_request, req)
```

#### 8.8.3.2 Worker Model

- **What:** Tasks are distributed to idle workers from a shared queue.
- **Why:** Improves scalability and balances CPU utilization.
- **Where:** Background job processing, e.g., RabbitMQ workers.

```javascript
const { Worker } = require('worker_threads');
const tasks = [/* ... */]; // some task list

tasks.forEach(task => {
  const worker = new Worker('./worker.js', { workerData: task });
  worker.on('message', result => console.log(result));
});
```

### 8.8.4 Asynchronous Processing

**Why Async?**

- Avoids blocking threads on I/O (file, DB, network).
- Boosts throughput, keeps system responsive.

**Techniques:**

- Async/await (C#, JS, Python).
- Promises/Futures.
- Message Queues (RabbitMQ, Kafka).

```javascript
async function getUserData(id) {
  const user = await db.findUserById(id); // Non-blocking I/O
  return user;
}
```

### 8.8.5 Concurrency in Web Servers

| Traditional Servers          | Modern Servers                         |
|------------------------------|----------------------------------------|
| Spawn thread/process/request | Use async / non-blocking I/O           |
| High resource usage          | Event loop or thread pool models       |
| Hard to scale                | Efficient, handles more with less      |

**Modern examples:**

- **Node.js:** Event-loop, non-blocking I/O.
- **ASP.NET Core / Nginx:** Thread pools + async I/O.

### 8.8.6 Common Pitfalls: Race Conditions & Deadlocks

#### 8.8.6.1 Race Condition

- Occurs when multiple threads access/modify shared data unsafely.
- Can corrupt data or cause unpredictable bugs.
- **Fix:** Synchronize access (locks, mutexes).

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1
```

#### 8.8.6.2 Deadlock

- Threads stuck waiting for each other's resources.
- System can freeze.
- **Fix:** Lock ordering, timeouts, avoiding nested locks.

### 8.8.7 Concurrency — Best Practices

- Prefer async/non-blocking I/O for I/O-bound tasks.
- Use thread pools for CPU-bound work, not raw threads.
- Always synchronize access to shared data.
- Detect & avoid deadlocks (consistent lock ordering).
- Monitor performance with appropriate metrics.

**Real-world scenarios:**

- Web servers (Node.js/ASP.NET): Thread pool + async I/O.
- Background jobs (RabbitMQ, Kafka): Worker model.
- Parallel image rendering: Each frame on different core.

### 8.8.8 Concurrency — Summary Table

| Concept             | Purpose              | Typical Tools/Techniques        | Example                        |
|---------------------|----------------------|---------------------------------|--------------------------------|
| Concurrency         | Task management      | Async/await, event loop, coros  | Node.js HTTP server            |
| Parallelism         | Task execution       | Thread pool, multiprocessing    | Java ThreadPool, Python Pool   |
| Thread Pool         | Reduce overhead      | Executors, Pool, Task queue     | ASP.NET Core, Java Executors   |
| Worker Model        | Distribute workload  | Queues + workers                | RabbitMQ, Celery, Sidekiq      |
| Async Processing    | Non-blocking I/O     | Promises, Futures, async/await  | JS async functions, C# await   |
| Synchronization     | Prevent race bugs    | Locks, mutexes, semaphores      | threading.Lock (Python)        |
| Deadlock Avoidance  | System stability     | Lock ordering, timeouts         | Consistent lock strategy       |

### 8.8.9 Event Loop (Simplified)

```mermaid
flowchart TB
    R(["Incoming HTTP requests"]) --> EL["Event loop"]
    EL --> IO["Async I/O and callbacks"]
    EL --> TP["Thread pool for CPU-heavy tasks"]
```


---

## 8.9 Database Performance Optimization Techniques

### 8.9.1 Replication

**Replication** is the process of copying and maintaining database objects in multiple places. Critical for:

- **High availability:** If one node fails, replicas ensure continued service.
- **Load balancing:** Distribute read traffic among replicas.
- **Disaster recovery:** Data is safe even if a site goes down.

**Types of replication:**

- **Master-Slave Replication:** One primary (master) handles writes, read-only slaves handle queries.
- **Master-Master Replication:** Multiple primaries handle reads and writes, offering redundancy.

(See `image-19.png` for Master-Slave vs Master-Master diagram.)

> **Tip:** Use master-slave for simple read scaling; master-master for HA and fault tolerance, but beware of write conflicts.

### 8.9.2 Sharding & Partitioning

#### 8.9.2.1 Sharding

**Sharding** splits large datasets across multiple servers (shards), each holding a subset of the data. Enables horizontal scaling.

**Example:** Users partitioned by geographic region.

```mermaid
graph LR
    A[Client] --> B[Shard 1: US]
    A[Client] --> C[Shard 2: EU]
    A[Client] --> D[Shard 3: ASIA]
```

#### 8.9.2.2 Partitioning

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

### 8.9.3 CAP Theorem (Performance Perspective)

The **CAP Theorem** states that in a distributed system, you can only guarantee two of:

- **Consistency:** All nodes see the same data at the same time.
- **Availability:** Every request gets a response (even if not the latest).
- **Partition Tolerance:** System works even if network splits occur.

| Type | Guarantees                       | Use When…                            |
|------|----------------------------------|--------------------------------------|
| CP   | Consistency + Partition Tolerance | Banking, strong consistency needed   |
| AP   | Availability + Partition Tolerance | Social feeds, eventual consistency OK |

> **Performance note:** Prioritizing availability (AP) often improves performance at scale but may introduce temporary inconsistencies.

### 8.9.4 Indexes

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

### 8.9.5 Normalization vs. Denormalization

(See `image-21.png` for diagram.)

#### 8.9.5.1 Normalization

- **Goal:** Reduce data redundancy by organizing data into tables.
- **Benefits:** Minimizes storage costs and eliminates anomalies.
- **Drawback:** Can lead to complex joins and slower read performance.
- Splits data into related tables to reduce redundancy. Ideal for transactional (OLTP) systems.

#### 8.9.5.2 Denormalization

- **Goal:** Introduce redundancy to reduce join operations and speed up reads.
- **Benefits:** Faster read performance.
- **Drawback:** Increased storage and potential data anomalies.
- Best for reporting/analytics (OLAP).

#### 8.9.5.3 When to Use Each

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

### 8.9.6 Connection Pooling

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

### 8.9.7 Query Optimization

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

### 8.9.8 Materialized Views

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

### 8.9.9 Batching & Pagination

#### 8.9.9.1 Batching

- **Definition:** Sending multiple operations in a single request or transaction to reduce overhead.
- **Use case:** Bulk inserts or updates.

#### 8.9.9.2 Pagination

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

### 8.9.10 Database Optimization — Quick Reference

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

### 8.9.11 Database Optimization — Layered Architecture Diagram

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

---

## 8.10 Performance Anti-Patterns (and How to Fix Them)

### 8.10.1 Cache Stampede / Thundering Herd

A popular key expires. **1,000 concurrent requests** all miss the cache simultaneously and all hit the database. The DB falls over.

**Fixes (in order of complexity):**
1. **Randomized TTL** — instead of `TTL = 60s`, use `TTL = 60s ± 5s` so keys don't all expire at the same moment.
2. **Lock on regeneration** — first request that misses takes a lock, regenerates the value, others wait. Use Redis SETNX or distributed locks.
3. **Probabilistic early expiration** — regenerate slightly before expiry, in the background. Avoids the cliff entirely.

### 8.10.2 N+1 Query Problem

You fetch 100 users, then loop and run `SELECT * FROM orders WHERE user_id = ?` for each. That's **1 + 100 = 101 queries** instead of 1.

```python
# BAD
users = db.query("SELECT * FROM users LIMIT 100")
for user in users:
    user.orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)

# GOOD — single JOIN
results = db.query("""
    SELECT u.*, o.*
    FROM users u LEFT JOIN orders o ON u.id = o.user_id
    LIMIT 100
""")
```

> **Most ORMs make this easy to hit accidentally.** Use eager loading (`.includes` in Rails, `selectinload` in SQLAlchemy, `Include` in EF).

### 8.10.3 Database Connection Pool Sized Wrong

Common mistake: setting pool size to a huge number like 500, assuming "more is better."

**Reality:** PostgreSQL recommends `connections ≈ ((core_count × 2) + effective_spindle_count)`. For an 8-core SSD-backed DB that's about **20 connections.** Past that, context-switching overhead and lock contention slow things down.

**Use a pooler** (PgBouncer, ProxySQL) if you have many app servers. App-level pool stays small; pooler multiplexes.

### 8.10.4 Blocking I/O on Hot Path

A 5 ms log-to-disk call doesn't sound bad — until you do it on every request and your p99 doubles.

**Fix:** offload I/O to a background queue or async logger. The hot path should *never* block on disk/network for non-essential work.

### 8.10.5 Synchronous Calls in a Chain

Service A → Service B → Service C, all synchronous. Total latency = sum of all three; failure of any one fails the whole request.

**Fix:** parallelize where possible (call B and C concurrently); make non-essential calls async; use circuit breakers.

---

## 8.11 Cache Patterns — The Full Picture

| Pattern        | How it works                                                           | Use when                                  |
|----------------|-------------------------------------------------------------------------|-------------------------------------------|
| **Cache-aside** (lazy loading) | App reads cache; on miss, reads DB and populates cache | Default for read-heavy data with infrequent writes |
| **Read-through** | App always reads cache; cache itself fetches from DB on miss          | When you want app code to not know about the DB |
| **Write-through** | Writes go to cache and DB at the same time                            | Strong consistency requirement; OK with write latency |
| **Write-back** (write-behind) | Writes go to cache; DB updated async                         | Write-heavy; can tolerate data loss on cache crash |
| **Write-around** | Writes go directly to DB, bypassing cache                              | Writes rarely re-read soon (cold data) |

> **For most apps, cache-aside is the right default.** Simple, predictable, doesn't require special cache libraries.

---

## 8.12 Performance Antipatterns Catalog and Monitoring

The ten classic performance antipatterns, the bulkhead fix, and the five kinds of monitoring: health, availability, performance, security, usage.

**In one sentence:** most slow or fragile systems are slow in one of ten well-known ways, and you only find which one by instrumenting the system (metrics, logs, traces), watching the right signals, and alerting on user-visible symptoms rather than every internal blip.

**Mental model — a restaurant kitchen.** An antipattern is a kitchen habit that works at lunch for four tables and collapses at dinner for forty: one cook doing every dish (busy frontend), a trip to the market for each egg (chatty I/O), buying the whole cow to use one steak (extraneous fetching). Monitoring is the pass where the head chef sees ticket times, which stations are backed up, and whether the fridge is still cold — and the alarm should ring when customers wait too long, not whenever a pan clatters.

#### 8.12.1 Part 1 — Performance antipatterns

These ten come from the Azure Architecture Center's performance antipatterns catalogue: recurring mistakes that are invisible at low load and dominate at scale.

**1. Busy Database**

* **Symptom and cause:** DB CPU and I/O saturate while app servers idle, because too much work (formatting, business logic in stored procedures, heavy reports on the primary) runs inside the database.
* **Detect:** high DB CPU with low app CPU; slow-query log; long statements in `pg_stat_activity`.
* **Fix:** move formatting and logic to the app tier, send reports to read replicas (Ch 11), cache hot results (Ch 7).

**2. Busy Frontend**

* **Symptom and cause:** request threads are all occupied, so even trivial requests queue, because CPU-heavy or long work (image resizing, PDF generation) runs on the threads that serve users.
* **Detect:** high CPU on web nodes, worker-pool saturation, cheap endpoints slow only while expensive ones run.
* **Fix:** return `202 Accepted`, enqueue the job (Ch 9) and process it on a separate worker pool.

**3. Chatty I/O**

* **Symptom and cause:** latency is the sum of round trips, not of work, because of N+1 queries, one HTTP call per item or one write per row.
* **Detect:** traces showing a "comb" of short spans; query count per request; call rate to a dependency far above the user request rate.
* **Fix:** batch, join or use `IN (...)`, paginate, offer coarser endpoints, prefetch or cache.

```python
# BAD: 1 + N queries
orders = db.query("SELECT * FROM orders WHERE user_id = %s", uid)
for o in orders:
    o.items = db.query("SELECT * FROM items WHERE order_id = %s", o.id)

# GOOD: 2 queries total
orders = db.query("SELECT * FROM orders WHERE user_id = %s", uid)
items = db.query("SELECT * FROM items WHERE order_id = ANY(%s)", [o.id for o in orders])
```

**4. Extraneous Fetching**

* **Symptom and cause:** high bandwidth, memory and DB I/O for little output, because of `SELECT *`, filtering a whole table in the app, or no pagination.
* **Detect:** rows fetched vs rows used; response sizes in traces; egress per request.
* **Fix:** select only needed columns, filter and aggregate in the query, paginate, use covering indexes.

```python
# BAD: pull everything, filter in memory
recent = [r for r in db.query("SELECT * FROM events") if r.ts > cutoff][:50]
# GOOD: let the database do it
recent = db.query("SELECT id, ts, kind FROM events WHERE ts > %s ORDER BY ts DESC LIMIT 50", cutoff)
```

**5. Improper Instantiation**

* **Symptom and cause:** socket exhaustion, a TLS handshake on every call, memory churn, because shareable objects (HTTP clients, DB connections, compiled regexes) are created per request.
* **Detect:** many `TIME_WAIT` sockets, connections near limits, high connect time in traces.
* **Fix:** create once and reuse (singletons, dependency injection, pools, keep-alive).

```python
# BAD: a new client (new TCP + TLS handshake) per call
def get_price(sku): return requests.get(f"https://prices.internal/{sku}").json()
# GOOD: one pooled session per process
session = requests.Session()
def get_price(sku): return session.get(f"https://prices.internal/{sku}", timeout=2).json()
```

**6. Monolithic Persistence**

* **Symptom and cause:** one database is too slow for search, too costly for blobs and too contended for sessions, because every kind of data lives in one store.
* **Detect:** wildly different access patterns inside one cluster; one workload's spikes slow another's.
* **Fix:** polyglot persistence: relational for transactions, object storage for blobs, a search engine for text, a cache for sessions. The cost is more systems to run and keep consistent (Ch 12).

**7. No Caching**

* **Symptom and cause:** identical expensive reads repeat and hammer the database or an upstream API, because there is no cache or its hit ratio is near zero (bad keys or TTLs).
* **Detect:** cache hit ratio; identical queries in the slow-query log; high read QPS on rarely changing data.
* **Fix:** cache at the right layer (CDN, app, Redis), choose the pattern and TTL deliberately, protect against stampedes (Ch 7).

**8. Noisy Neighbor**

* **Symptom and cause:** one tenant, job or service degrades everyone sharing a resource, because shared pools, CPUs, disks or queues have no per-tenant limit.
* **Detect:** per-tenant breakdown of latency and resource use; one tenant's spikes correlating with others' errors.
* **Fix:** quotas and rate limits (Ch 8), multi-tenancy isolation, and bulkheads (below).

**9. Retry Storm**

* **Symptom and cause:** a brief dependency blip becomes a long outage, because clients retry at once, without backoff, jitter or a budget, often at several layers.
* **Detect:** request rate to a dependency exceeds user request rate; synchronized retry waves right after errors begin.
* **Fix:** timeouts, exponential backoff with jitter, retry budgets, retry at one layer, circuit breakers, idempotency (Vol 3 Ch 14).

```
 retry amplification: 3 layers, each makes up to 3 attempts
 client ──×3──► gateway ──×3──► service ──×3──► database (already failing)
 one user request can become 3 × 3 × 3 = 27 database attempts
```

**10. Synchronous I/O**

* **Symptom and cause:** low CPU but high latency and low throughput, because calling threads block on network or disk and a small pool caps concurrency.
* **Detect:** worker pool fully busy with idle CPU; threads parked in socket reads in a thread dump.
* **Fix:** async/non-blocking I/O, a sized pool for blocking calls, and run independent calls concurrently.

```python
# BAD: sequential (latency = a + b + c)
user = fetch_user(uid); orders = fetch_orders(uid); recs = fetch_recs(uid)
# GOOD: concurrent (latency ≈ max(a, b, c))
user, orders, recs = await asyncio.gather(fetch_user(uid), fetch_orders(uid), fetch_recs(uid))
```

**Summary**

| Antipattern | Typical symptom | Usual cause | Main fix |
|-------------|-----------------|-------------|----------|
| Busy Database | DB CPU/I/O saturated | logic and formatting in the DB | move work to app tier, replicas, cache |
| Busy Frontend | request threads exhausted | heavy work on request threads | queue + background workers |
| Chatty I/O | latency = sum of round trips | N+1, one call per item | batch, join, coarser APIs |
| Extraneous Fetching | high bandwidth and memory | `SELECT *`, filter in app | project, filter in query, paginate |
| Improper Instantiation | socket exhaustion, handshakes | new client per request | reuse pooled clients |
| Monolithic Persistence | one store fits no workload | everything in one database | polyglot persistence |
| No Caching | repeated identical reads | no cache, or bad keys/TTLs | layered caching |
| Noisy Neighbor | one tenant hurts others | shared resource, no limits | quotas, isolation, bulkheads |
| Retry Storm | blip becomes outage | immediate unbounded retries | backoff + jitter + budget + breaker |
| Synchronous I/O | idle CPU, low throughput | blocking calls on few threads | async, concurrency |

#### 8.12.2 Bulkhead

**Bulkhead** — named after the watertight compartments of a ship's hull: partition resources so a failure or overload in one compartment cannot sink the rest. It is the structural fix for noisy neighbors and cascading failure: give each tenant, endpoint or dependency its own pool (threads, connections, semaphore permits, queue slots) with a hard cap.

| Variant | Isolates | Example |
|---------|----------|---------|
| Semaphore bulkhead | concurrent calls | max 20 in-flight calls to the payments API |
| Thread-pool bulkhead | threads plus a queue | a separate pool per downstream dependency |
| Connection-pool partition | DB connections | reporting gets 5 connections, checkout gets 30 |
| Per-tenant / per-tier | tenant traffic | premium and free tenants on separate pools or cells |
| Deployment-level | whole stacks | separate clusters or cells per region or customer group |

Combine it with timeouts and a circuit breaker (Vol 3 Ch 14); per-tenant limits are in Ch 8 and Ch 15. The cost is lower utilization: idle capacity in one compartment cannot be lent to another.

#### 8.12.3 Part 2 — Monitoring

Each kind of monitoring answers a different question.

| Kind | Question it answers | Example signals | Typical tools |
|------|---------------------|-----------------|---------------|
| Health monitoring | Is each component alive and able to serve? | liveness/readiness probes, dependency checks, restarts | Kubernetes probes, load balancer health checks |
| Availability monitoring | Can users actually reach and use it? | synthetic checks from outside, success ratio, uptime vs SLO | `blackbox_exporter`, uptime services |
| Performance monitoring | How fast and how efficiently? | latency percentiles, throughput, saturation, queue depth, cache hit ratio | Prometheus + Grafana, APM, traces |
| Security monitoring | Is something hostile or unexpected happening? | failed logins, permission denials, unusual egress, audit-log anomalies | SIEM, audit logs, Falco |
| Usage monitoring | What do users do, and what does it cost? | active users, feature adoption, requests per tenant, quota use | product analytics, billing metering |

**Health endpoint monitoring.** Expose cheap HTTP endpoints that monitors and orchestrators poll.

| Probe | Question | On failure | Should check |
|-------|----------|------------|--------------|
| Liveness (`/healthz`) | Is the process stuck and in need of a restart? | restart the container | only the process itself, never dependencies |
| Readiness (`/readyz`) | Can this instance take traffic right now? | remove from the load balancer, do not restart | warm-up done, critical dependencies reachable |
| Startup | Has a slow-starting app finished booting? | hold off the other probes | initialization |

Gotcha: if liveness checks the database, a database outage restarts every pod at once and turns a partial failure into a total one. Keep health checks cheap and fast, and separate from deep dependency checks.

#### 8.12.4 Part 3 — Instrumentation, visualization and alerting

**Instrumentation** means emitting metrics, logs and traces (Vol 1 Ch 58, Vol 2 Ch 16; using them in an incident: Vol 2 Ch 18) — not repeated here.

| Method | For | Signals |
|--------|-----|---------|
| RED | request-driven services | **R**ate, **E**rrors, **D**uration |
| USE | resources (CPU, disk, pools, queues) | **U**tilization, **S**aturation, **E**rrors |
| Four golden signals (Google SRE) | any user-facing system | latency, traffic, errors, saturation |

Rules: counters for events, gauges for current values, histograms for latency (percentiles can be computed from buckets and aggregated across instances); label only by low-cardinality dimensions (route template, status code), never user ID or raw URL — every distinct label combination is a new time series.

**Visualization.** A dashboard answers "is it healthy?" in five seconds: SLIs on top (success rate, p99), then RED per service, then USE per resource, with deploy markers; link panels to runbooks and traces.

**Alerting** — alert on symptoms, investigate causes.

| Practice | Why |
|----------|-----|
| Symptom alerts page, cause alerts only inform | "error rate above SLO" matters to users; "CPU 85%" may not |
| Every page is actionable and urgent | otherwise it is noise |
| SLO-based, multi-window burn-rate alerts | catch fast burns quickly and slow burns before the budget is gone |
| Route by severity and ownership | page for urgent, ticket for slow, dashboard for informational |

**Alert fatigue** — too many low-value alerts train people to ignore pages, so a real one is missed. Delete or demote alerts nobody acts on, group and deduplicate (Alertmanager), add `for:` durations, and review pages in every post-incident review.

**Burn rate** = error rate ÷ (1 − SLO); 1 uses the error budget exactly over the SLO window. For a 30-day window the Google SRE Workbook suggests paging at 14.4× over 1 hour (2% of budget) and 6× over 6 hours (5%), and a ticket at 1× over 3 days (10%), each paired with a window about 1/12 as long so the alert clears quickly.

```yaml
# 99.9% SLO: page on fast burn (14.4 x budget) over 1h AND 5m
- alert: HighErrorBudgetBurn
  expr: |
    ( sum(rate(http_requests_total{code=~"5.."}[1h])) / sum(rate(http_requests_total[1h])) ) > (14.4 * 0.001)
    and
    ( sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) ) > (14.4 * 0.001)
  labels: { severity: page }
```

## 8.13 Combined Tips & Tricks

A consolidated master list drawn from all sections.

### 8.13.1 Monitoring & Metrics

- **Always monitor:** Use tools like Prometheus, Grafana, DataDog.
- **Set SLOs/SLAs:** Make performance measurable and accountable.
- **Track percentiles:** P95 and P99 are often more important than the average.
- **Watch for bottlenecks:** They often hide until your system is under stress.
- **Document your performance strategy:** Make it part of your architecture, not an afterthought.

### 8.13.2 Testing

- **Test under real conditions:** Simulate both steady load and traffic spikes.
- **Test under load:** Locust, JMeter, k6 to simulate concurrency issues before production.

### 8.13.3 Caching

- **Cache wisely:** Cache only what's expensive or slow to compute, and ensure consistency.
- **Apply TTL smartly:** Especially on volatile or time-sensitive data.
- **Prevent cache stampede:** Use locks or request coalescing.
- **Automate cache invalidation:** Design carefully for dynamic content.

### 8.13.4 Messaging

- **Design for failure:** Ensure your queue/message broker can handle spikes and outages.
- **Make consumers idempotent:** Especially in queuing systems with at-least-once delivery.

### 8.13.5 Concurrency

- **Use thread pools:** Avoid creating/destroying threads for each task.
- **Async for I/O-bound, thread pool for CPU-bound.**
- **Always use locks for shared data:** Protect shared variables with mutexes/locks.
- **Avoid nested locks:** Keep locking hierarchy simple to reduce deadlock risk.
- **Prefer async/non-blocking I/O:** Especially for I/O-bound tasks.

### 8.13.6 Database

- **Tune your DB:** Indexes, sharding, connection pooling, and query optimization all matter.
- **Use prepared statements:** Prevent SQL injection and improve plan caching.
- **Minimize data transfer:** Fetch only required columns.
- **Use connection pools:** For efficient database access.
- **Batch writes:** Aggregate writes where possible to reduce DB round-trips.
- **Async processing:** Offload heavy/slow tasks to background workers.
- **Paginate large datasets:** Never fetch "all" in production APIs.
- **Profile & test:** Use `EXPLAIN` in SQL to analyze query plans.
- **Automate index management:** Remove unused indexes and tune existing ones.

---

## 8.14 Sample Interview Questions

1. What is the difference between latency and throughput?
2. Explain SLAs, SLOs, and SLIs. Why use P95/P99 instead of average?
3. What are the four main caching strategies? Compare them.
4. Compare LRU, LFU, FIFO, and TTL eviction policies.
5. Why use asynchronous messaging? When would you use queues?
6. Compare RabbitMQ and Kafka. When to use which?
7. Explain at-least-once, at-most-once, and exactly-once delivery.
8. How do queues improve scalability and fault tolerance?
9. How would you design an order processing system with queues?
10. How do you ensure idempotency in consumers?
11. What is the difference between concurrency and parallelism?
12. How do threads differ from processes?
13. What is a thread pool, and why is it preferred over creating new threads?
14. How would you design a web server for thousands of concurrent requests?
15. What is a race condition? How do you prevent it?
16. How do you debug and resolve a deadlock?
17. How does the event loop work in Node.js?
18. Explain master-slave vs. master-master replication trade-offs.
19. How does sharding differ from partitioning?
20. When would you denormalize a database schema?
21. Why use connection pooling?
22. When would you use a materialized view?

---

## 8.15 Summary & Key Takeaways

- Performance = speed, scalability, and efficiency under real-world load.
- Use **caching** to reduce latency and load.
- Employ **asynchronous messaging** for decoupling and resilience.
- Harness **concurrency and parallelism** for better resource usage.
- Optimize **database** layers with replication, sharding, indexing, and smart queries.
- **Monitor, test, and prioritize performance** at every stage.
- **Concurrency ≠ Parallelism:** Concurrency manages tasks; parallelism executes them simultaneously.
- **Use the right tool:** Async for I/O-bound, thread pool for CPU-bound.
- **Threads are lighter than processes** but require careful handling (race conditions, deadlocks).

> **Performance isn't a luxury. It's a core feature for modern, user-friendly, and scalable systems.**

---

## 8.16 Further Reading

- [System Design Interview – Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [Google SRE Book: SLIs, SLOs, SLAs](https://sre.google/sre-book/service-level-objectives/)
- [Redis Documentation](https://redis.io/documentation)
- [RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
- [Apache Kafka Docs](https://kafka.apache.org/documentation/)
- [RabbitMQ vs Kafka](https://www.cloudamqp.com/blog/when-to-use-rabbitmq-or-apache-kafka.html)
- [Martin Fowler: Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [Java Concurrency (Oracle)](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [Node.js Event Loop](https://nodejs.dev/learn/the-nodejs-event-loop)
- [Thread Pool Pattern](https://en.wikipedia.org/wiki/Thread_pool_pattern)
- [RabbitMQ Worker Model](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)
- [Cache-Aside Pattern — Microsoft docs](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
- [PostgreSQL Indexing Documentation](https://www.postgresql.org/docs/current/indexes.html)
- [Database Sharding Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/sharding)
- [CAP Theorem Explained (Martin Kleppmann)](https://martin.kleppmann.com/2012/04/09/cap-theorem.html)

---

**Next Up:** [Chapter 9 — Reliability, Availability & Disaster Recovery →](./9%20-%20Reliability%2C%20Availability%20%26%20Disaster%20Recovery.md) — how to ensure your systems remain robust and resilient in the face of failures.
