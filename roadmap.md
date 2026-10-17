# Mastery Roadmap

> Structure: six **volumes**, each complete enough that finishing it means you genuinely master the area. Delivered as **142 chapters**, one concept each, with prerequisites, diagrams, examples, exercises, a mini project, real open-source references, interview questions, and a checklist.

## Volumes

| # | Volume | File | Chapters |
|---|--------|------|----------|
| 0 | Math & Mental Models | [volumes/volume-0-math/index.md](volumes/volume-0-math/index.md) | 1–9 (9) |
| 1 | Computer Science Foundations | [volumes/volume-1-cs-foundations/index.md](volumes/volume-1-cs-foundations/index.md) | 1–59 (59) |
| 2 | Software Engineering | [volumes/volume-2-software-engineering/index.md](volumes/volume-2-software-engineering/index.md) | 1–18 (18) |
| 3 | Low-Level Design | [volumes/volume-3-low-level-design/index.md](volumes/volume-3-low-level-design/index.md) | 1–14 (14) |
| 4 | High-Level Design | [volumes/volume-4-high-level-design/index.md](volumes/volume-4-high-level-design/index.md) | 1–22 (22) |
| 5 | AI Systems Engineering | [volumes/volume-5-ai-systems/index.md](volumes/volume-5-ai-systems/index.md) | 1–20 (20) |

**Total: 142 chapters** across the six volumes.

---

## Prerequisite Ordering

The volumes are **not** strictly linear. Key cross-volume dependencies:

* **Volume 0** → gates Vol 1 Part 4 (algorithms) and *all* of Vol 5.
* **Vol 1 Part 1–3** (programming, dev env, SE fundamentals) → everything.
* **Vol 1 Part 5–6** (architecture, OS) → Vol 1 Part 9 (distributed) and Vol 4.
* **Vol 1 Part 7–8** (networking, DB) → Vol 4 (HLD).
* **Vol 1 Part 9** (distributed systems) + **Vol 1 Part 11** (cloud/ops) → Vol 4 (HLD) and Vol 5 serving/GPU infra.
* **Vol 3** (LLD) → Vol 4 (HLD).
* **Vol 0 Ch 9** (linear algebra) + **Vol 1 Ch 9** (encoding) → Vol 5 foundations.

Each chapter declares its own prerequisites explicitly; treat the above as the volume-level skeleton.

---

## System Design Track

The volumes teach in learning order, so system design topics sit in several volumes. This track lists them again in **11 themed sections** (the usual system-design course layout), then the case studies. Each row links to chapters that already exist; nothing is duplicated or moved.

| # | Section | Read, in order | Not written yet |
|---|---------|----------------|-----------------|
| 1 | Introduction & method | [V4 Ch1 Approach](volumes/volume-4-high-level-design/ch01-approaching-a-system-design-problem.md) · [V4 Ch2 Capacity](volumes/volume-4-high-level-design/ch02-capacity-planning.md) | history timeline (low value) |
| 2 | Networking & communication | [V1 Ch40 Networking](volumes/volume-1-cs-foundations/ch40-networking-fundamentals-osi-tcp-ip-ip-ports.md) · [V1 Ch44 LB, proxies, CDN](volumes/volume-1-cs-foundations/ch44-delivery-load-balancing-reverse-proxies-and-cdn.md) · [V4 Ch5 Proxies & gateways](volumes/volume-4-high-level-design/ch05-proxies-gateways-web-servers-and-storage-types.md) · [V4 Ch6 Load balancing](volumes/volume-4-high-level-design/ch06-load-balancing.md) · [V4 Ch14 CDN & edge](volumes/volume-4-high-level-design/ch14-cdn-edge-and-geo-distribution.md) | "type google.com" walkthrough; DNS security |
| 3 | Protocols | [V1 Ch41 TCP/UDP/QUIC/TLS](volumes/volume-1-cs-foundations/ch41-transport-and-security-tcp-udp-quic-tls.md) · [V1 Ch42 HTTP/REST/GraphQL](volumes/volume-1-cs-foundations/ch42-http-rest-graphql-and-json-rpc.md) · [V1 Ch43 WebSocket/gRPC/SSE](volumes/volume-1-cs-foundations/ch43-websockets-grpc-mqtt-and-sse.md) | long polling; WebRTC |
| 4 | Architectural patterns | [V4 Ch4 Distributed patterns](volumes/volume-4-high-level-design/ch04-distributed-systems-patterns.md) · [V4 Ch12 Event-driven](volumes/volume-4-high-level-design/ch12-event-driven-systems.md) · [V4 Ch13 Cloud patterns](volumes/volume-4-high-level-design/ch13-cloud-design-patterns.md) · [V3 Ch8 Clean arch.](volumes/volume-3-low-level-design/ch08-clean-architecture.md) · [V3 Ch9 Hexagonal](volumes/volume-3-low-level-design/ch09-hexagonal-architecture-ports-and-adapters.md) · [V3 Ch12 CQRS & event sourcing](volumes/volume-3-low-level-design/ch12-event-bus-cqrs-and-event-sourcing.md) | N-tier / 3-tier names; "when not to use microservices" table |
| 5 | Web concepts | [V1 Ch8 Data formats](volumes/volume-1-cs-foundations/ch08-data-formats-text-json-csv-xml-yaml.md) · [V1 Ch9 Encoding & serialization](volumes/volume-1-cs-foundations/ch09-character-encoding-and-binary-serialization.md) · [V1 Ch42 HTTP](volumes/volume-1-cs-foundations/ch42-http-rest-graphql-and-json-rpc.md) · [V2 Ch12 AuthN & AuthZ](volumes/volume-2-software-engineering/ch12-authentication-and-authorization.md) · [V2 Ch14 API design](volumes/volume-2-software-engineering/ch14-api-design-and-versioning.md) | same-origin policy; XSS vs CSRF; security headers |
| 6 | Scalability | [V4 Ch3 Scalability & reliability](volumes/volume-4-high-level-design/ch03-scalability-and-reliability-fundamentals.md) · [V4 Ch7 Caching](volumes/volume-4-high-level-design/ch07-caching-strategies.md) · [V4 Ch8 Rate limiting](volumes/volume-4-high-level-design/ch08-rate-limiting-throttling-and-backpressure.md) · [V4 Ch9 Queues & streaming](volumes/volume-4-high-level-design/ch09-message-queues-and-streaming-kafka-sqs-pub.md) · [V4 Ch10 Mesh & discovery](volumes/volume-4-high-level-design/ch10-service-mesh-and-service-discovery.md) · [V4 Ch15 Multi-tenancy](volumes/volume-4-high-level-design/ch15-multi-tenancy.md) | Amdahl's Law; Universal Scalability Law; diagonal scaling |
| 7 | Storage | [V1 Ch45 SQL](volumes/volume-1-cs-foundations/ch45-sql-and-the-relational-model.md) · [V1 Ch46 Schema & indexing](volumes/volume-1-cs-foundations/ch46-schema-design-normalization-and-indexing.md) · [V1 Ch47 ACID](volumes/volume-1-cs-foundations/ch47-acid-transactions-and-isolation.md) · [V1 Ch48 NoSQL](volumes/volume-1-cs-foundations/ch48-nosql-mongodb-cassandra-and-dynamodb.md) · [V1 Ch49 Redis/Search/Graph](volumes/volume-1-cs-foundations/ch49-redis-elasticsearch-neo4j-and-vector-databases.md) · [V1 Ch50 CAP & consensus](volumes/volume-1-cs-foundations/ch50-cap-consistency-and-consensus.md) · [V1 Ch51 Replication & sharding](volumes/volume-1-cs-foundations/ch51-replication-sharding-raft-and-paxos.md) · [V1 Ch53 ETL & streams](volumes/volume-1-cs-foundations/ch53-etl-elt-batch-and-stream-processing.md) · [V1 Ch54 Lakes & warehouses](volumes/volume-1-cs-foundations/ch54-data-lakes-warehouses-and-orchestration.md) · [V4 Ch11 DB scaling](volumes/volume-4-high-level-design/ch11-database-scaling.md) | HDFS / distributed file systems; Lambda & Kappa; block vs file vs object comparison |
| 8 | Performance | [V4 Ch16 Antipatterns & monitoring](volumes/volume-4-high-level-design/ch16-performance-antipatterns-and-monitoring.md) · [V2 Ch10 Performance engineering](volumes/volume-2-software-engineering/ch10-performance-engineering.md) · [V1 Ch58 Observability](volumes/volume-1-cs-foundations/ch58-observability-logs-metrics-traces-and-opentelemetry.md) · [V2 Ch16 Observability](volumes/volume-2-software-engineering/ch16-observability-logs-metrics-and-traces.md) | soak / spike / stress test types |
| 9 | Reliability, availability & DR | [V4 Ch17 Disaster recovery](volumes/volume-4-high-level-design/ch17-disaster-recovery-backups-rto-rpo.md) · [V3 Ch14 Resilience patterns](volumes/volume-3-low-level-design/ch14-resilience-patterns-idempotency-retries-backoff-circuit-breakers.md) · [V2 Ch17 Incidents](volumes/volume-2-software-engineering/ch17-incident-response-and-postmortems.md) · [V2 Ch18 Production debugging](volumes/volume-2-software-engineering/ch18-production-debugging.md) | MTBF / MTTR |
| 10 | Security | [V2 Ch11 Threat modeling](volumes/volume-2-software-engineering/ch11-security-and-threat-modeling.md) · [V2 Ch12 AuthN & AuthZ](volumes/volume-2-software-engineering/ch12-authentication-and-authorization.md) · [V4 Ch18 Security at system level](volumes/volume-4-high-level-design/ch18-security-at-the-system-level.md) · [V4 Ch19 AuthN & AuthZ in design](volumes/volume-4-high-level-design/ch19-authentication-and-authorization-in-system-design.md) | CIA triad; shared responsibility model; container & serverless security |
| 11 | The blueprint (method & interviews) | [V4 Ch1 Approach](volumes/volume-4-high-level-design/ch01-approaching-a-system-design-problem.md) · [V4 Ch22 Portfolio](volumes/volume-4-high-level-design/ch22-the-30-system-design-portfolio.md) | interviewer soft skills; "when you get stuck" script |
| – | Cloud & cost (extra) | [V4 Ch20 Cloud architecture](volumes/volume-4-high-level-design/ch20-cloud-architecture.md) · [V4 Ch21 Cost economics](volumes/volume-4-high-level-design/ch21-cost-and-capacity-economics.md) · [V1 Ch59 Cloud cost](volumes/volume-1-cs-foundations/ch59-cost-awareness-in-the-cloud.md) | – |

### Case studies

All designs live in [V4 Ch22 — The 30-System Design Portfolio](volumes/volume-4-high-level-design/ch22-the-30-system-design-portfolio.md).

| Typical case study | In our portfolio? | Note |
|--------------------|-------------------|------|
| URL shortener | yes | worked example; add a key-generation comparison |
| Cloud storage (Drive, Dropbox) | yes (#16, #17) | thin: block-level dedup and sync conflicts |
| Video platform | yes (#15) | thin: encoding cost, recommendations |
| E-commerce | yes (#27) | thin: concrete checkout saga |
| Taxi hailing | yes (#21) | thin: surge pricing |
| Search engine | partial (#10 autocomplete, #11 crawler) | **not written yet:** inverted index and ranking |
| Collaborative editor | no | **not written yet:** OT / CRDT design |
| Auction platform | no | **not written yet:** bid concurrency, closing timers |

---

## Exit Criteria (per volume)

* **Vol 0** — Solve a set of Big-O, probability, and linear-algebra problems from scratch.
* **Vol 1** — Build one non-trivial CLI/service touching files, network, and a database.
* **Vol 2** — Ship a project with full CI/CD, tests, observability, and a postmortem for one induced failure.
* **Vol 3** — 30+ production-quality components.
* **Vol 4** — 30+ real-world system designs.
* **Vol 5** — The 7 progressive builds, ending at the AI Operating System.

---

## Chapter format

Each chapter:

* teaches exactly one concept,
* has prerequisites,
* includes diagrams,
* provides simple examples,
* includes coding exercises,
* has a mini project,
* points to real open-source code,
* ends with interview questions and a checklist.
