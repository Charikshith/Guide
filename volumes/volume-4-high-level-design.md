# Volume 4 — High-Level Design

> Goal: Design systems that scale and stay reliable. Requires Volume 1 (Parts 7–9) and Volume 3.
>
> **Chapters 1–17.** Each chapter ends by designing one or more real-world systems; by the end you will have designed **30+ systems**.

---

## Chapter 1 — Capacity Planning

**Concept:** QPS, latency percentiles (p50/p99), throughput, storage sizing, and translating requirements into hardware/tier estimates.

**Prereqs:** Vol 1 Ch 44, Vol 2 Ch 9.

**Diagram:** A capacity worksheet: QPS → servers → storage → cost.

**Example:** estimate servers for 10M DAU with 50 req/user/day and 1000 QPS/server.

**Exercises:** (1) Size storage for a chat app (messages/user/day). (2) Estimate peak QPS with a 5× daily peak factor.

**Mini project:** A capacity calculator that turns product assumptions into a resource plan.

**Design:** Design the data model and capacity plan for a URL shortener.

**Open source:** [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer).

**Interview:** "How do you estimate QPS from DAU?" / "What percentile matters most for latency?"

**Checklist:** ☐ use back-of-envelope math ☐ plan for peak, not average ☐ state assumptions explicitly

---

## Chapter 2 — Scalability & Reliability Fundamentals

**Concept:** Vertical vs horizontal scaling, statelessness, redundancy, failure domains, availability math (N nines).

**Prereqs:** Ch 1.

**Diagram:** Scale-up vs scale-out; a redundancy diagram with an availability formula.

**Example:** computing availability of 2×99.9% in series vs parallel.

**Exercises:** (1) Compute availability of three nines across 5 services. (2) Make a stateful service horizontally scalable.

**Mini project:** An availability/reliability calculator with failure-domain modeling.

**Design:** Design a highly available stateless API tier.

**Open source:** [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer).

**Interview:** "Horizontal vs vertical scaling?" / "What does 99.99% allow per year?"

**Checklist:** ☐ design for statelessness ☐ spread across failure domains ☐ compute availability correctly

---

## Chapter 3 — Distributed Systems Patterns

**Concept:** Replication, partitioning, leader/follower, quorums, idempotency, and the failure modes that shape every design.

**Prereqs:** Vol 1 Ch 47 (distributed/ACID), Ch 49.

**Diagram:** A leader-follower replication diagram; a quorum read/write diagram.

**Example:** a 3-node quorum (R+W > N) for consistency.

**Exercises:** (1) Explain a split-brain and its prevention. (2) Design a replicated KV store with quorum reads.

**Mini project:** A small replicated KV store simulator with leader election and quorum.

**Design:** Design a distributed cache.

**Open source:** [`etcd-io/etcd`](https://github.com/etcd-io/etcd); [`redis/redis`](https://github.com/redis/redis) (replication).

**Interview:** "How do quorums give consistency?" / "What is split-brain?"

**Checklist:** ☐ choose replication strategy ☐ use quorums deliberately ☐ handle partial failures

---

## Chapter 4 — Load Balancing

**Concept:** L4 vs L7, algorithms (round-robin, least-conn, consistent hashing), health checks, and sticky sessions.

**Prereqs:** Vol 1 Ch 44.

**Diagram:** An LB distributing to backends with a consistent-hash ring.

**Example:** consistent hashing to keep cache affinity; least-connections for long-lived requests.

**Exercises:** (1) Implement consistent hashing and show minimal remapping. (2) Add health-check-based removal.

**Mini project:** A consistent-hashing LB simulator.

**Design:** Design the load-balancing layer for a global service.

**Open source:** [`envoyproxy/envoy`](https://github.com/envoyproxy/envoy); [`nginx/nginx`](https://github.com/nginx/nginx).

**Interview:** "Consistent hashing — why?" / "L4 vs L7 LB?"

**Checklist:** ☐ pick an algorithm per workload ☐ health-check everything ☐ plan for LB itself failing

---

## Chapter 5 — Caching Strategies

**Concept:** Cache-aside, write-through/write-around/write-back, invalidation, TTLs, stampedes, and cache coherence.

**Prereqs:** Vol 1 Ch 49 (Redis).

**Diagram:** Cache-aside read/write paths; a cache-stampede mitigation diagram.

**Example:** `get → cache → miss → db → set`; a lock/jitter to prevent a stampede.

**Exercises:** (1) Implement cache-aside. (2) Fix a cache-stampede with locking or jitter.

**Mini project:** A cache layer with invalidation + stampede protection.

**Design:** Design a caching layer for a product feed.

**Open source:** [`redis/redis`](https://github.com/redis/redis); [`memcached/memcached`](https://github.com/memcached/memcached).

**Interview:** "Cache-aside vs write-through?" / "How do you invalidate safely?"

**Checklist:** ☐ set TTLs with jitter ☐ avoid stampedes ☐ treat cache as a coherence problem

---

## Chapter 6 — Rate Limiting, Throttling & Backpressure

**Concept:** Token bucket, leaky bucket, sliding window; distributed limits; backpressure upstream.

**Prereqs:** Vol 1 Ch 44.

**Diagram:** A token bucket filling/draining; a backpressure signal flowing upstream.

**Example:** a token-bucket limiter; a 429 + retry-after response.

**Exercises:** (1) Implement a token bucket. (2) Design a distributed rate limiter with Redis.

**Mini project:** A rate limiter library with multiple algorithms.

**Design:** Design a rate limiter for a public API.

**Open source:** [`envoyproxy/envoy`](https://github.com/envoyproxy/envoy) (rate limiting); [`redis/redis`](https://github.com/redis/redis) (INCR+EXPIRE).

**Interview:** "Token bucket vs sliding window?" / "How do you rate-limit across nodes?"

**Checklist:** ☐ bound every public endpoint ☐ return clear 429s ☐ propagate backpressure

---

## Chapter 7 — Message Queues & Streaming (Kafka, SQS, Pub/Sub)

**Concept:** Queues vs logs, at-least/at-most/exactly-once, ordering, DLQs, and stream processing.

**Prereqs:** Vol 1 Ch 43, Ch 49.

**Diagram:** A producer → broker → consumer group with partitions and offsets.

**Example:** a Kafka topic with a consumer group; an SQS queue with a DLQ.

**Exercises:** (1) Design exactly-once processing for a payment. (2) Explain a consumer-group rebalance.

**Mini project:** A producer/consumer pipeline with retries and a dead-letter queue.

**Design:** Design an order-processing pipeline on a queue.

**Open source:** [`apache/kafka`](https://github.com/apache/kafka); [`aws/aws-sdk`](https://github.com/aws/aws-sdk) (SQS).

**Interview:** "Queue vs stream (Kafka vs SQS)?" / "How do you guarantee ordering?"

**Checklist:** ☐ pick delivery semantics explicitly ☐ use DLQs ☐ keep consumers idempotent

---

## Chapter 8 — Service Mesh & Service Discovery

**Concept:** Sidecars, discovery, mTLS, retries/timeouts/circuit breaking at the mesh layer; when a mesh earns its cost.

**Prereqs:** Ch 4, Vol 3 Ch 14.

**Diagram:** A service mesh with sidecars intercepting traffic; a discovery registry.

**Example:** Istio/Linkerd mTLS + retries configured per route.

**Exercises:** (1) Explain how mTLS works in a mesh. (2) Configure retries/timeouts at the mesh layer.

**Mini project:** A toy sidecar that adds a timeout + retry to a service.

**Design:** Design service discovery + resilience for a microservice fleet.

**Open source:** [`linkerd/linkerd2`](https://github.com/linkerd/linkerd2); [`istio/istio`](https://github.com/istio/istio).

**Interview:** "What does a service mesh give you?" / "Sidecar pros/cons?"

**Checklist:** ☐ standardize mTLS ☐ centralize retries/timeouts ☐ know when *not* to use a mesh

---

## Chapter 9 — Database Scaling

**Concept:** Read replicas, caching, sharding (key selection), partitioning, and the read/write split.

**Prereqs:** Vol 1 Ch 45–47.

**Diagram:** A primary + replicas diagram; a sharded database with a routing layer.

**Example:** sharding by `user_id`; a read replica for reporting.

**Exercises:** (1) Choose a shard key and explain hot spots. (2) Add a read replica and route reads to it.

**Mini project:** A sharded-store simulator with a consistent-hashing router.

**Design:** Design the data tier for a social feed (sharding + replicas).

**Open source:** [`vitessio/vitess`](https://github.com/vitessio/vitess); [`postgres/postgres`](https://github.com/postgres/postgres) (replication).

**Interview:** "How do you choose a shard key?" / "Read replicas — consistency cost?"

**Checklist:** ☐ avoid hot shards ☐ handle cross-shard queries ☐ balance read scale vs staleness

---

## Chapter 10 — Event-Driven Systems

**Concept:** Event producers/consumers, event schemas, ordering, idempotency, and eventual consistency.

**Prereqs:** Ch 7, Vol 3 Ch 12.

**Diagram:** An event flow across services with a schema registry.

**Example:** an `OrderPlaced` event consumed by billing, shipping, and analytics.

**Exercises:** (1) Design an event schema with versioning. (2) Make a consumer idempotent across redeliveries.

**Mini project:** An event-driven workflow with two consumers and a schema registry.

**Design:** Design an event-driven checkout pipeline.

**Open source:** [`apache/kafka`](https://github.com/apache/kafka); [`confluentinc/schema-registry`](https://github.com/confluentinc/schema-registry).

**Interview:** "Event-driven vs request/response?" / "How do you handle event ordering?"

**Checklist:** ☐ version event schemas ☐ idempotent consumers ☐ accept eventual consistency

---

## Chapter 11 — CDN, Edge & Geo-Distribution

**Concept:** Caching at the edge, geo-routing, data residency, and multi-region consistency.

**Prereqs:** Vol 1 Ch 44.

**Diagram:** A global CDN with edge PoPs and origin shielding.

**Example:** a CDN cache rule; geo-DNS routing to the nearest region.

**Exercises:** (1) Explain cache-busting for static assets. (2) Design multi-region with a primary/secondary.

**Mini project:** A simulated CDN with edge caches and origin fetch.

**Design:** Design a globally distributed image-serving system.

**Open source:** [`traefik/traefik`](https://github.com/traefik/traefik); [`envoyproxy/envoy`](https://github.com/envoyproxy/envoy) (edge).

**Interview:** "How does a CDN reduce origin load?" / "Multi-region consistency — how?"

**Checklist:** ☐ cache immutable assets forever ☐ route by geo with fallback ☐ design for data residency

---

## Chapter 12 — Multi-Tenancy

**Concept:** Tenant isolation models (pool, bridge, silo), data isolation, and tenant-aware routing/security.

**Prereqs:** Vol 1 Ch 45, Vol 2 Ch 10.

**Diagram:** Shared-table vs schema-per-tenant vs DB-per-tenant.

**Example:** a `tenant_id` column + row-level security (RLS).

**Exercises:** (1) Implement tenant isolation with RLS. (2) Compare the three models' cost/scale.

**Mini project:** A multi-tenant SaaS schema with RLS and tenant-scoped queries.

**Design:** Design multi-tenant architecture for a SaaS app.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres) (RLS).

**Interview:** "Pool vs silo multi-tenancy?" / "How do you prevent tenant data leaks?"

**Checklist:** ☐ isolate data per tenant ☐ test cross-tenant access ☐ plan per-tenant scaling

---

## Chapter 13 — Disaster Recovery (Backups, RTO/RPO)

**Concept:** Backup strategies, restore testing, RTO/RPO, and multi-region failover.

**Prereqs:** Ch 9.

**Diagram:** A backup/recovery timeline showing RPO (data loss) and RTO (downtime).

**Example:** nightly snapshots + WAL streaming; a failover drill.

**Exercises:** (1) Define RTO/RPO for a service and pick a strategy. (2) Test a restore from backup.

**Mini project:** A backup + restore script with verification and a measured RTO/RPO.

**Design:** Design DR for a payments database.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres) (WAL/PITR); [`velero/velero`](https://github.com/velero/velero).

**Interview:** "RTO vs RPO?" / "Why test restores, not just backups?"

**Checklist:** ☐ state RTO/RPO explicitly ☐ automate + verify restores ☐ run failover drills

---

## Chapter 14 — Security at the System Level

**Concept:** Zero-trust, IAM, secrets, encryption in transit/at rest, and blast-radius reduction.

**Prereqs:** Vol 2 Ch 10.

**Diagram:** A zero-trust architecture with identity-aware access and mTLS.

**Example:** short-lived credentials; KMS-managed keys; least-privilege IAM policies.

**Exercises:** (1) Design least-privilege IAM for a service. (2) Encrypt data at rest and in transit.

**Mini project:** A threat model + least-privilege IAM + encryption for a small system.

**Design:** Design the security posture for a multi-service platform.

**Open source:** [`hashicorp/vault`](https://github.com/hashicorp/vault); [`spiffe/spire`](https://github.com/spiffe/spire).

**Interview:** "Zero trust — what changes?" / "How do you manage secrets at scale?"

**Checklist:** ☐ least privilege everywhere ☐ encrypt transit + rest ☐ rotate credentials automatically

---

## Chapter 15 — Cloud Architecture

**Concept:** Cloud building blocks (compute, storage, networking, managed services), serverless vs containers, and cost-aware design.

**Prereqs:** Ch 1–2, Vol 1 Ch 44.

**Diagram:** A reference architecture on a cloud provider with managed services.

**Example:** API gateway → serverless/containers → managed DB/cache.

**Exercises:** (1) Map a monolith to cloud services. (2) Compare serverless vs container costs for a workload.

**Mini project:** A cost-estimate + architecture diagram for a service on a cloud provider.

**Design:** Design a serverless image-processing pipeline.

**Open source:** [`serverless/serverless`](https://github.com/serverless/serverless); [`aws/aws-sdk`](https://github.com/aws/aws-sdk).

**Interview:** "Serverless vs containers — when each?" / "How do you control cloud cost?"

**Checklist:** ☐ use managed services where sensible ☐ design for cost ☐ avoid vendor lock-in where it matters

---

## Chapter 16 — Cost & Capacity Economics

**Concept:** Unit economics, cloud cost drivers, right-sizing, and cost as a design constraint.

**Prereqs:** Ch 15.

**Diagram:** A cost breakdown by service with the top spenders highlighted.

**Example:** right-sizing an over-provisioned cluster; reserving capacity for steady load.

**Exercises:** (1) Find and fix the top cost driver in a sample bill. (2) Compute unit cost per request.

**Mini project:** A cost model + dashboard tracking cost per endpoint.

**Design:** Design a cost-optimization plan for a growing service.

**Open source:** [`opencost/opencost`](https://github.com/opencost/opencost).

**Interview:** "How do you reduce cloud spend without hurting reliability?" / "What's unit economics for infra?"

**Checklist:** ☐ track cost per unit of value ☐ right-size continuously ☐ treat cost as a first-class requirement

---

## Chapter 17 — The 30-System Design Portfolio

**Concept:** Applying every prior chapter to a portfolio of canonical designs; pattern recognition across systems.

**Prereqs:** Ch 1–16.

**Diagram:** A "system design zoo" — one diagram each for 30 systems, grouped by family.

**Example:** the canonical URL-shortener design as a template.

**Exercises:** (1) Pick any system and draw its full design. (2) For each, list the top 3 scaling bottlenecks.

**Mini project:** A personal design journal with diagrams + trade-off notes for each system.

**Design:** Design these 30+ systems (a running portfolio): URL shortener, pastebin, rate limiter, web crawler, notification service, news feed, chat system, search autocomplete, YouTube-like video platform, Google Drive-like storage, Dropbox-like sync, Twitter-like feed, Instagram-like media, WhatsApp-like messenger, Uber-like dispatch, food-delivery app, ticket booking, stock exchange, payments, e-commerce, hotel booking, map service, distributed cache, distributed queue, distributed KV store, distributed unique-ID generator, analytics/clickstream pipeline, monitoring/alerting, job scheduler, load balancer, CDN, and one system of your own choice.

**Open source:** [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer); [`ByteByteGoHq/system-design-101`](https://github.com/ByteByteGoHq/system-design-101).

**Interview:** "How do you approach an unfamiliar system-design question?" / "What's your design process?"

**Checklist:** ☐ 30+ designs with diagrams ☐ each states trade-offs ☐ can whiteboard any of them cold

---

**Exit criteria:** Design **30+ real-world systems** (chapter 17 portfolio).
