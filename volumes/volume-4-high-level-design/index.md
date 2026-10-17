# Volume 4 — High-Level Design

> Goal: Design systems that scale and stay reliable. Requires Volume 1 (Parts 7–9) and Volume 3.
>
> **Chapters 1–24.** Each chapter ends by designing one or more real-world systems; by the end you will have designed **30+ systems**.

# Contents

**Part 1 — Approach & Estimation**
1. [Approaching a System Design Problem](ch01-approaching-a-system-design-problem.md)
2. [Capacity Planning](ch02-capacity-planning.md)

**Part 2 — Scalability & Distributed Foundations**
3. [Scalability & Reliability Fundamentals](ch03-scalability-and-reliability-fundamentals.md)
4. [Distributed Systems Patterns](ch04-distributed-systems-patterns.md)

**Part 3 — The Traffic Layer**
5. [Proxies, Gateways, Web Servers & Storage Types](ch05-proxies-gateways-web-servers-and-storage-types.md)
6. [Load Balancing](ch06-load-balancing.md)
7. [Caching Strategies](ch07-caching-strategies.md)
8. [Rate Limiting, Throttling & Backpressure](ch08-rate-limiting-throttling-and-backpressure.md)

**Part 4 — Messaging, Data & Events**
9. [Message Queues & Streaming (Kafka, SQS, Pub/Sub)](ch09-message-queues-and-streaming-kafka-sqs-pub.md)
10. [Service Mesh & Service Discovery](ch10-service-mesh-and-service-discovery.md)
11. [Database Scaling](ch11-database-scaling.md)
12. [Event-Driven Systems](ch12-event-driven-systems.md)

**Part 5 — Cloud Patterns, Edge & Tenancy**
13. [Cloud Design Patterns](ch13-cloud-design-patterns.md)
14. [CDN, Edge & Geo-Distribution](ch14-cdn-edge-and-geo-distribution.md)
15. [Multi-Tenancy](ch15-multi-tenancy.md)

**Part 6 — Operating & Protecting Systems**
16. [Performance Antipatterns & Monitoring](ch16-performance-antipatterns-and-monitoring.md)
17. [Disaster Recovery (Backups, RTO/RPO)](ch17-disaster-recovery-backups-rto-rpo.md)
18. [Security at the System Level](ch18-security-at-the-system-level.md)
19. [Authentication & Authorization in System Design](ch19-authentication-and-authorization-in-system-design.md)

**Part 7 — Cloud, Cost & Case Studies**
20. [Cloud Architecture](ch20-cloud-architecture.md)
21. [Cost & Capacity Economics](ch21-cost-and-capacity-economics.md)
22. [The 30-System Design Portfolio](ch22-the-30-system-design-portfolio.md)
23. [Design a Collaborative Document Editor (Google Docs)](ch23-design-a-collaborative-document-editor-google-docs.md)
24. [Design an Auction Platform (eBay)](ch24-design-an-auction-platform-ebay.md)

---

## Part 1 — Approach & Estimation

### Chapter 1 — Approaching a System Design Problem

**Concept:** What system design is, how HLD differs from LLD, and a repeatable method — requirements, estimates, API, data, architecture, deep dive, trade-offs — for starting any design problem.

**Design:** Design a URL shortener, using the 7 steps.

---

### Chapter 2 — Capacity Planning

**Concept:** QPS, latency percentiles (p50/p99), throughput, storage sizing, and translating requirements into hardware/tier estimates.

**Prereqs:** Vol 1 Ch 44, Vol 2 Ch 10.

**Diagram:** A capacity worksheet: QPS → servers → storage → cost.

**Example:** estimate servers for 10M DAU with 50 req/user/day and 1000 QPS/server.

**Exercises:** (1) Size storage for a chat app (messages/user/day). (2) Estimate peak QPS with a 5× daily peak factor.

**Mini project:** A capacity calculator that turns product assumptions into a resource plan.

**Design:** Design the data model and capacity plan for a URL shortener.

**Open source:** [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer).

**Interview:** "How do you estimate QPS from DAU?" / "What percentile matters most for latency?"

**Checklist:** ☐ use back-of-envelope math ☐ plan for peak, not average ☐ state assumptions explicitly

---

## Part 2 — Scalability & Distributed Foundations

### Chapter 3 — Scalability & Reliability Fundamentals

**Concept:** Vertical vs horizontal scaling, statelessness, redundancy, failure domains, availability math (N nines).

**Prereqs:** Ch 2.

**Diagram:** Scale-up vs scale-out; a redundancy diagram with an availability formula.

**Example:** computing availability of 2×99.9% in series vs parallel.

**Exercises:** (1) Compute availability of three nines across 5 services. (2) Make a stateful service horizontally scalable.

**Mini project:** An availability/reliability calculator with failure-domain modeling.

**Design:** Design a highly available stateless API tier.

**Open source:** [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer).

**Interview:** "Horizontal vs vertical scaling?" / "What does 99.99% allow per year?"

**Checklist:** ☐ design for statelessness ☐ spread across failure domains ☐ compute availability correctly

---

### Chapter 4 — Distributed Systems Patterns

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

## Part 3 — The Traffic Layer

### Chapter 5 — Proxies, Gateways, Web Servers & Storage Types

**Concept:** Forward vs reverse proxy, API gateway patterns, web vs app servers, CDN push vs pull, block/object/file storage, federation, graph databases.

**Design:** Design the edge and storage tier of an online shop.

---

### Chapter 6 — Load Balancing

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

### Chapter 7 — Caching Strategies

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

### Chapter 8 — Rate Limiting, Throttling & Backpressure

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

## Part 4 — Messaging, Data & Events

### Chapter 9 — Message Queues & Streaming (Kafka, SQS, Pub/Sub)

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

### Chapter 10 — Service Mesh & Service Discovery

**Concept:** Sidecars, discovery, mTLS, retries/timeouts/circuit breaking at the mesh layer; when a mesh earns its cost.

**Prereqs:** Ch 6, Vol 3 Ch 14.

**Diagram:** A service mesh with sidecars intercepting traffic; a discovery registry.

**Example:** Istio/Linkerd mTLS + retries configured per route.

**Exercises:** (1) Explain how mTLS works in a mesh. (2) Configure retries/timeouts at the mesh layer.

**Mini project:** A toy sidecar that adds a timeout + retry to a service.

**Design:** Design service discovery + resilience for a microservice fleet.

**Open source:** [`linkerd/linkerd2`](https://github.com/linkerd/linkerd2); [`istio/istio`](https://github.com/istio/istio).

**Interview:** "What does a service mesh give you?" / "Sidecar pros/cons?"

**Checklist:** ☐ standardize mTLS ☐ centralize retries/timeouts ☐ know when *not* to use a mesh

---

### Chapter 11 — Database Scaling

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

### Chapter 12 — Event-Driven Systems

**Concept:** Event producers/consumers, event schemas, ordering, idempotency, and eventual consistency.

**Prereqs:** Ch 9, Vol 3 Ch 12.

**Diagram:** An event flow across services with a schema registry.

**Example:** an `OrderPlaced` event consumed by billing, shipping, and analytics.

**Exercises:** (1) Design an event schema with versioning. (2) Make a consumer idempotent across redeliveries.

**Mini project:** An event-driven workflow with two consumers and a schema registry.

**Design:** Design an event-driven checkout pipeline.

**Open source:** [`apache/kafka`](https://github.com/apache/kafka); [`confluentinc/schema-registry`](https://github.com/confluentinc/schema-registry).

**Interview:** "Event-driven vs request/response?" / "How do you handle event ordering?"

**Checklist:** ☐ version event schemas ☐ idempotent consumers ☐ accept eventual consistency

---

## Part 5 — Cloud Patterns, Edge & Tenancy

### Chapter 13 — Cloud Design Patterns

**Concept:** A catalog of the named patterns for building reliable, scalable distributed applications in the cloud: messaging, data management, design and implementation, reliability, and security.

**Design:** Design an incremental migration of a monolith using Strangler Fig and an Anti-Corruption Layer.

---

### Chapter 14 — CDN, Edge & Geo-Distribution

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

### Chapter 15 — Multi-Tenancy

**Concept:** Tenant isolation models (pool, bridge, silo), data isolation, and tenant-aware routing/security.

**Prereqs:** Vol 1 Ch 45, Vol 2 Ch 11.

**Diagram:** Shared-table vs schema-per-tenant vs DB-per-tenant.

**Example:** a `tenant_id` column + row-level security (RLS).

**Exercises:** (1) Implement tenant isolation with RLS. (2) Compare the three models' cost/scale.

**Mini project:** A multi-tenant SaaS schema with RLS and tenant-scoped queries.

**Design:** Design multi-tenant architecture for a SaaS app.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres) (RLS).

**Interview:** "Pool vs silo multi-tenancy?" / "How do you prevent tenant data leaks?"

**Checklist:** ☐ isolate data per tenant ☐ test cross-tenant access ☐ plan per-tenant scaling

---

## Part 6 — Operating & Protecting Systems

### Chapter 16 — Performance Antipatterns & Monitoring

**Concept:** The ten classic performance antipatterns, the bulkhead fix, and the five kinds of monitoring: health, availability, performance, security, usage.

**Design:** Design a metrics and alerting pipeline for a company with about 300 services.

---

### Chapter 17 — Disaster Recovery (Backups, RTO/RPO)

**Concept:** Backup strategies, restore testing, RTO/RPO, and multi-region failover.

**Prereqs:** Ch 11.

**Diagram:** A backup/recovery timeline showing RPO (data loss) and RTO (downtime).

**Example:** nightly snapshots + WAL streaming; a failover drill.

**Exercises:** (1) Define RTO/RPO for a service and pick a strategy. (2) Test a restore from backup.

**Mini project:** A backup + restore script with verification and a measured RTO/RPO.

**Design:** Design DR for a payments database.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres) (WAL/PITR); [`velero/velero`](https://github.com/velero/velero).

**Interview:** "RTO vs RPO?" / "Why test restores, not just backups?"

**Checklist:** ☐ state RTO/RPO explicitly ☐ automate + verify restores ☐ run failover drills

---

### Chapter 18 — Security at the System Level

**Concept:** Zero-trust, IAM, secrets, encryption in transit/at rest, and blast-radius reduction.

**Prereqs:** Vol 2 Ch 11.

**Diagram:** A zero-trust architecture with identity-aware access and mTLS.

**Example:** short-lived credentials; KMS-managed keys; least-privilege IAM policies.

**Exercises:** (1) Design least-privilege IAM for a service. (2) Encrypt data at rest and in transit.

**Mini project:** A threat model + least-privilege IAM + encryption for a small system.

**Design:** Design the security posture for a multi-service platform.

**Open source:** [`hashicorp/vault`](https://github.com/hashicorp/vault); [`spiffe/spire`](https://github.com/spiffe/spire).

**Interview:** "Zero trust — what changes?" / "How do you manage secrets at scale?"

**Checklist:** ☐ least privilege everywhere ☐ encrypt transit + rest ☐ rotate credentials automatically

---

### Chapter 19 — Authentication & Authorization in System Design

**Concept:** Where identity is checked in a large system, how it travels between services, how tokens are issued, verified, rotated, and revoked at scale, how services trust each other, how permissions are decided, and how it all survives failure.

**Prereqs:** Vol 2 Ch 12, Ch 5, Ch 10, Ch 15, Ch 18.

**Diagram:** Edge authentication with token exchange and service-to-service trust; the login and token lifecycle with revocation.

**Example:** An Envoy `jwt_authn` filter, an Istio `AuthorizationPolicy`, an OPA policy, and a Redis revocation check.

**Exercises:** (1) Why do inner services verify identity again? (2) Fix a service that trusts an `X-User-Id` header. (3) Choose a revocation design for a 10-second target.

**Mini project:** A gateway, an auth service, and two services with token exchange, mTLS allow rules, and key rotation.

**Design:** Design authentication for a multi-tenant B2B SaaS with enterprise SSO; for a public API platform; for a 100M-user consumer login.

**Open source:** [`keycloak/keycloak`](https://github.com/keycloak/keycloak); [`spiffe/spire`](https://github.com/spiffe/spire); [`open-policy-agent/opa`](https://github.com/open-policy-agent/opa); [`authzed/spicedb`](https://github.com/authzed/spicedb).

**Interview:** "Where would you authenticate in microservices?" / "How do you revoke a JWT at scale?"

**Checklist:** ☐ authenticate at the edge and verify again inside ☐ default-deny service-to-service calls ☐ rotate keys with overlap ☐ keep the identity service off the per-request path

---

## Part 7 — Cloud, Cost & Case Studies

### Chapter 20 — Cloud Architecture

**Concept:** Cloud building blocks (compute, storage, networking, managed services), serverless vs containers, and cost-aware design.

**Prereqs:** Ch 2–3, Vol 1 Ch 44.

**Diagram:** A reference architecture on a cloud provider with managed services.

**Example:** API gateway → serverless/containers → managed DB/cache.

**Exercises:** (1) Map a monolith to cloud services. (2) Compare serverless vs container costs for a workload.

**Mini project:** A cost-estimate + architecture diagram for a service on a cloud provider.

**Design:** Design a serverless image-processing pipeline.

**Open source:** [`serverless/serverless`](https://github.com/serverless/serverless); [`aws/aws-sdk`](https://github.com/aws/aws-sdk).

**Interview:** "Serverless vs containers — when each?" / "How do you control cloud cost?"

**Checklist:** ☐ use managed services where sensible ☐ design for cost ☐ avoid vendor lock-in where it matters

---

### Chapter 21 — Cost & Capacity Economics

**Concept:** Unit economics, cloud cost drivers, right-sizing, and cost as a design constraint.

**Prereqs:** Ch 20.

**Diagram:** A cost breakdown by service with the top spenders highlighted.

**Example:** right-sizing an over-provisioned cluster; reserving capacity for steady load.

**Exercises:** (1) Find and fix the top cost driver in a sample bill. (2) Compute unit cost per request.

**Mini project:** A cost model + dashboard tracking cost per endpoint.

**Design:** Design a cost-optimization plan for a growing service.

**Open source:** [`opencost/opencost`](https://github.com/opencost/opencost).

**Interview:** "How do you reduce cloud spend without hurting reliability?" / "What's unit economics for infra?"

**Checklist:** ☐ track cost per unit of value ☐ right-size continuously ☐ treat cost as a first-class requirement

---

### Chapter 22 — The 30-System Design Portfolio

**Concept:** Applying every prior chapter to a portfolio of canonical designs; pattern recognition across systems.

**Prereqs:** Ch 1–20.

**Diagram:** A "system design zoo" — one diagram each for 30 systems, grouped by family.

**Example:** the canonical URL-shortener design as a template.

**Exercises:** (1) Pick any system and draw its full design. (2) For each, list the top 3 scaling bottlenecks.

**Mini project:** A personal design journal with diagrams + trade-off notes for each system.

**Design:** Design these 30+ systems (a running portfolio): URL shortener, pastebin, rate limiter, web crawler, notification service, news feed, chat system, search autocomplete, YouTube-like video platform, Google Drive-like storage, Dropbox-like sync, Twitter-like feed, Instagram-like media, WhatsApp-like messenger, Uber-like dispatch, food-delivery app, ticket booking, stock exchange, payments, e-commerce, hotel booking, map service, distributed cache, distributed queue, distributed KV store, distributed unique-ID generator, analytics/clickstream pipeline, monitoring/alerting, job scheduler, load balancer, CDN, and one system of your own choice.

**Open source:** [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer); [`ByteByteGoHq/system-design-101`](https://github.com/ByteByteGoHq/system-design-101).

**Interview:** "How do you approach an unfamiliar system-design question?" / "What's your design process?"

**Checklist:** ☐ 30+ designs with diagrams ☐ each states trade-offs ☐ can whiteboard any of them cold

---

### Chapter 23 — Design a Collaborative Document Editor (Google Docs)

**Concept:** Real-time multi-user editing: why locks and last-write-wins fail, operational transformation (OT) versus sequence CRDTs versus Figma-style property-level last-writer-wins, one owner server per document, operation log and snapshots, presence, comments, offline, undo.

**Prereqs:** Ch 4, Ch 9, Ch 19, Vol 1 Ch 43, Vol 1 Ch 50, Vol 3 Ch 12.

**Diagram:** The architecture; the "abc" insert/delete worked example as a sequence diagram; a chooser between OT, CRDT, and property-level last-writer-wins.

**Example:** A working OT engine with a central server and a tiny sequence CRDT, both property-tested (exhaustive pair check plus thousands of random runs).

**Exercises:** (1) Walk the `abc` example by hand. (2) How OT and a CRDT order two inserts at the same spot. (3) Why tombstones exist. (4) Offline for an hour. (5) Why presence stays out of the log. (6) An overloaded hot document.

**Mini project:** An OT server with three clients, snapshots, operation IDs, comments, multi-character edits, and per-user undo.

**Design:** Design a collaborative editor for 10M daily users: API, data model, estimates, and the decisions to justify.

**Open source:** [`yjs/yjs`](https://github.com/yjs/yjs); [`automerge/automerge`](https://github.com/automerge/automerge); [`share/sharedb`](https://github.com/share/sharedb); [`ether/etherpad-lite`](https://github.com/ether/etherpad-lite).

**Interview:** "How do two people edit the same document at once?" / "OT versus CRDT?" / "What is a tombstone?"

**Checklist:** ☐ apply edits locally first ☐ choose OT, CRDT, or property-level LWW on purpose ☐ one owner per document orders operations ☐ log before acknowledging ☐ test convergence with randomized edits

---

### Chapter 24 — Design an Auction Platform (eBay)

**Concept:** A timed auction with proxy (maximum) bidding: bid increments and the visible price, soft close against sniping, why simultaneous bids need one serialization point per auction (conditional update, atomic script, single writer), server-clock fairness, closing exactly once, fan-out to watchers, abuse.

**Prereqs:** Ch 7, Ch 8, Ch 9, Ch 12, Ch 19, Vol 1 Ch 47.

**Diagram:** The architecture; two bids at the same moment and a conditional update; closing with a soft-close extension.

**Example:** A working auction engine (proxy bidding, soft close, duplicate protection, optimistic concurrency, closing scheduler) with tests, including a deliberately broken blind-write version that loses a bid.

**Exercises:** (1) The $12 versus $15 example. (2) Two simultaneous bids and conditional updates. (3) Retried bids. (4) A hot auction with retry storms. (5) Whose clock decides. (6) Closing after a soft-close extension.

**Mini project:** A bid owner with a scheduler, a coalesced price feed, an outbox, and chaos tests.

**Design:** Design an auction platform for 10 million live auctions: API, data model, estimates, and the decisions to justify.

**Open source:** [`redis/redis`](https://github.com/redis/redis); [`apache/kafka`](https://github.com/apache/kafka); [`temporalio/temporal`](https://github.com/temporalio/temporal).

**Interview:** "Two people bid at the same time; how does the highest win?" / "What is proxy bidding?" / "How do you stop sniping?"

**Checklist:** ☐ one serialization point per auction ☐ the maximum bid is secret ☐ unique bid IDs ☐ server clock decides ☐ close exactly once ☐ test duplicates, races, extensions, crashes

---

**Exit criteria:** Design **30+ real-world systems** (chapter 22 portfolio).
