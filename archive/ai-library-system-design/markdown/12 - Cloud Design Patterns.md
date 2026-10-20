# Cloud Design Patterns

A cloud design pattern is a named, reusable answer to a recurring distributed-systems problem. This chapter is the catalog: what each pattern solves, when to use it, and what to watch out for.

---

## 12.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Use pattern names (Circuit Breaker, Cache-Aside, CQRS, Sidecar, Strangler Fig) precisely in a design discussion.
2. Match a problem to a pattern with the trade-off you accept.
3. Recognise the seven patterns that appear in almost every real system and interview.

---

## 12.2 Cloud Design Patterns Catalog

A catalog of the named patterns for building reliable, scalable distributed applications in the cloud: messaging, data management, design and implementation, reliability, and security.

**In one sentence:** a cloud design pattern is a named, reusable answer to a recurring distributed-systems problem — it tells you the problem, the shape of the solution, and the trade-off you accept — so you can say "put a bulkhead there" instead of re-deriving it in every design review.

**Mental model — a toolbox, not a checklist.** Each pattern is one tool with one job (a queue absorbs bursts, a breaker stops a retry storm, a sidecar bolts on a capability). Good designs use a handful of them where a real problem exists; a design that uses all of them is over-engineered. Always ask "which problem does this solve here?" before reaching for the tool.

**Where this catalog comes from.** The grouping and names follow the cloud design patterns catalog in the Azure Architecture Center, which roadmap.sh also lists. The ideas are not Azure-specific: every pattern maps to AWS, GCP, Kubernetes or plain open source. Where a pattern is covered in depth elsewhere in this guide, the entry here is short and links to that chapter.

**Not all patterns are equally important.** Learn these seven first — they appear in almost every real system and interview: **Circuit Breaker, Retry, Cache-Aside, CQRS, Publisher/Subscriber, Strangler Fig, Sidecar.** The rest are good vocabulary; look them up when the problem shows up.

#### 12.2.1 Messaging patterns

| Pattern | What it is / problem it solves | Use when | Watch out |
|---------|--------------------------------|----------|-----------|
| Sequential Convoy | Process related messages in order (per session, account or key) while unrelated groups still run in parallel. Solves ordering without a single-threaded bottleneck. | Order matters within a group (events for one order, one user, one device). | Needs a partition or session key; one hot key becomes a bottleneck; a poison message blocks its group. |
| Scheduler Agent Supervisor | A scheduler runs a multi-step job by dispatching each step to an agent; a supervisor watches for failed or stuck steps and recovers or retries them. Solves long workflows that span services. | Distributed workflows that must self-heal (provisioning, onboarding, order fulfilment). | Steps must be idempotent; state must be durable; this is basically a workflow engine, so consider buying one (Temporal, Step Functions). |
| Queue-Based Load Leveling | A queue between producers and a service buffers bursts so the service consumes at its own steady pace. Solves overload from spiky traffic. | Bursty writes to a slower backend; work that can finish later. | Adds latency; the caller gets no immediate result; the queue must be bounded and monitored (depth, age) — see Ch 8. |
| Publisher/Subscriber | A publisher announces events to a channel; any number of subscribers receive them without the publisher knowing who they are. Solves tight coupling and fan-out. | One event, many independent reactions (email, analytics, search index). | Delivery is usually at-least-once, so consumers must be idempotent; harder to trace who reacted; schema evolution. See Ch 9. |
| Priority Queue | Messages carry a priority so urgent work is processed before bulk work. Solves starvation of important requests behind a backlog. | Mixed workloads (paid vs free tier, interactive vs batch). | Low priority can starve forever (add aging); not every broker supports it natively — separate queues per priority also work. |
| Pipes and Filters | Break a complex task into independent steps (filters) connected by channels (pipes). Solves monolithic processing that cannot be reused or scaled per step. | Multi-stage transformations (ingest, validate, enrich, store); steps that scale differently. | Latency of every hop; failures between stages need a retry or dead-letter plan; too many tiny stages hurts throughput. |
| Competing Consumers | Several consumers read from one queue and each message goes to exactly one of them. Solves throughput and availability of a single consumer. | A queue backlog grows; you want to scale workers horizontally. | Ordering is lost across consumers (see Sequential Convoy); needs idempotency and a visibility timeout or ack; poison messages need a dead-letter queue. |
| Choreography | Services react to each other's events with no central controller; each service knows only its own step. Solves central coordinator bottlenecks and coupling. | Small, stable flows across a few teams. | The overall flow is implicit and hard to see or debug; cyclic event chains; compare with orchestration (a coordinator that calls each step) as flows grow. |
| Claim Check | Store the large payload in an external store and send only a small reference (the claim check) through the messaging system. Solves message-size limits and expensive large messages. | Payloads exceed the broker limit, or most consumers do not need the body. | Two systems to keep consistent; orphaned payloads need a lifecycle or TTL; the consumer needs access to the store. |
| Asynchronous Request-Reply | The client sends a request, gets an immediate acknowledgement (for example `202 Accepted` plus a status URL), and polls or is called back for the result. Solves long-running operations over HTTP. | Work takes longer than a normal request timeout. | Clients must poll or expose a callback; you must store job state and expire it; make the status endpoint cheap. |

#### 12.2.2 Data management patterns

| Pattern | What it is / problem it solves | Use when | Watch out |
|---------|--------------------------------|----------|-----------|
| Valet Key | Give the client a short-lived, narrowly scoped token (a pre-signed URL, SAS token) to access one resource directly. Solves proxying large transfers through your servers. | Direct upload or download from object storage. | Tokens are bearer secrets: keep them short-lived, scoped to one object and one action; you lose the proxy as a validation point. |
| Static Content Hosting | Serve static files (HTML, JS, images) from object storage behind a CDN instead of the web servers. Solves wasted compute and slow delivery. | Any site with static assets or a single-page app. See Ch 14. | Cache invalidation and versioned file names; CORS and access rules. |
| Sharding | Split a dataset into partitions (shards) across nodes by a key. Solves a data set or write rate that no single node can hold. | One node's storage or write throughput is exhausted. See Ch 11. | Shard-key choice, hot shards, cross-shard queries and transactions, resharding cost. |
| Materialized View | Pre-compute and store the result of a complex query in a shape ready to read. Solves slow, expensive read queries. | Read-heavy dashboards, search pages, denormalised read models. | The view is stale until refreshed; you need a refresh strategy (on write, scheduled, event-driven). |
| Index Table | Create your own lookup table keyed by a non-key field in a store that has no secondary indexes. Solves slow queries on non-key attributes in NoSQL stores. | Querying by a field other than the partition key (for example find user by email). | You maintain it yourself, so it can drift from the base table; extra writes. |
| Event Sourcing | Store every state change as an immutable event; current state is derived by replaying events. Solves lost history and hard auditing. | Audit-critical domains, temporal queries, rebuilding read models. See Vol 3 Ch 12. | Event schema versioning, replay time (use snapshots), eventual consistency, a steep learning curve. |
| CQRS | Separate the model that handles writes (commands) from the model that serves reads (queries). Solves read and write needs that pull one model in opposite directions. | Very different read and write loads or shapes; often paired with Event Sourcing. See Vol 3 Ch 12. | More moving parts; the read side is eventually consistent; overkill for simple CRUD. |
| Cache-Aside | The application checks the cache first, loads from the database on a miss, then fills the cache. Solves repeated expensive reads. | Read-heavy data that tolerates brief staleness. See Ch 7. | Stale data, invalidation, stampedes on a cold or expiring key. |

#### 12.2.3 Design and implementation patterns

| Pattern | What it is / problem it solves | Use when | Watch out |
|---------|--------------------------------|----------|-----------|
| Strangler Fig | Put a facade in front of a legacy system and route one feature at a time to new code until the old system can be switched off. Solves risky big-bang rewrites. | Migrating a monolith or legacy system incrementally. | Two systems run for a long time; the facade is a single point of failure; shared data is the hard part; set an end date or the migration never finishes. |
| Sidecar | Deploy a helper process next to the main app (same pod or host) to provide cross-cutting capability — logging, proxying, config, mTLS. Solves duplicating that code in every language. | A service mesh proxy, log shipper, or secrets agent. See Ch 10. | Extra resource use per instance; the sidecar lifecycle is coupled to the app; one more thing to upgrade. |
| Leader Election | Instances choose one coordinator to own a task, using a consensus store or lease. Solves duplicated work and conflicting writers. | Singleton jobs, partition ownership, scheduled tasks across replicas. | Split brain if leases are mishandled (use fencing tokens); failover delay; prefer a managed lock or lease service over rolling your own. |
| External Configuration Store | Move configuration out of the deployed package into a central store the app reads at startup or at runtime. Solves redeploying to change a setting. | Many services or environments share settings; feature flags. | The store becomes a dependency (cache the last good value); access control and audit; secrets belong in a secrets manager. |
| Compute Resource Consolidation | Run several small tasks or services in one compute unit. Solves wasted cost and overhead of many tiny deployments. | Many low-utilisation components with similar scaling and security needs. | Noisy neighbours, shared failure domain, harder independent scaling and deploys. |
| Backends for Frontend (BFF) | One backend per kind of client (web, mobile) shaped to that client's needs. Solves a one-size-fits-all API that suits no one. | Web and mobile need very different payloads or flows. | More services to maintain; shared logic can be duplicated — push it down into shared services. |
| Anti-Corruption Layer | A translation layer between a new system and a legacy or foreign one so the old model does not leak into the new design. Solves legacy concepts polluting the new domain. | Integrating with or migrating from a legacy system; third-party APIs with awkward models. See Vol 3 Ch 9. | Extra latency and code to maintain; can become a permanent crutch; keep it thin and tested. |
| Ambassador | A helper proxy beside a client that handles outbound network concerns — retries, timeouts, routing, TLS, monitoring. Solves repeating client-side connectivity logic. | Legacy or polyglot clients that need resilience without code changes. | An extra hop; it is a sidecar specialised for the client side of calls. |
| Gateway Routing / Offloading / Aggregation | One entry point that routes requests to services (routing), takes over shared work such as TLS, auth and rate limits (offloading), and combines several backend calls into one response (aggregation). Solves clients that must know every service and every cross-cutting concern. | Many services behind one public API. See Ch 5. | A single point of failure and bottleneck; keep business logic out of the gateway. |

#### 12.2.4 Reliability patterns

| Pattern | What it is / problem it solves | Use when | Watch out |
|---------|--------------------------------|----------|-----------|
| Deployment Stamps | Deploy independent, identical copies (stamps or scale units) of the whole application and data to serve a subset of tenants or a region. Solves scale limits and blast radius. | Multi-tenant SaaS, regional or compliance isolation. See Ch 15. | Cost and operational overhead per stamp; a routing layer to map tenant to stamp; global data. |
| Geodes | Geographically distributed nodes, each able to serve any request, with data replicated between them (active-active). Solves latency and regional failure. | Global users who need low latency and regional resilience. | Replicating and reconciling data across regions; conflict resolution; consistency trade-offs. See Ch 14. |
| Health Endpoint Monitoring | The service exposes a health endpoint that checks its own dependencies; external tools probe it. Solves discovering failures only when users complain. | Load balancers, orchestrators and monitors need liveness or readiness. | Shallow checks lie, deep checks can cause cascading failures; protect the endpoint; separate liveness from readiness. |
| Bulkhead | Isolate resources (thread pools, connection pools, instances) per dependency or per tenant so one failure cannot drain everything. Solves cascading resource exhaustion. | Calling several dependencies of unequal reliability; protecting a critical path. | Resources are partitioned and so less efficiently used; sizing each pool. |
| Circuit Breaker | Wrap a remote call and, after repeated failures, stop calling it for a while (open), then probe (half-open) before resuming. Solves retry storms against a failing dependency. See Vol 3 Ch 14. | Any remote call that can fail or hang. | Threshold and timeout tuning; needs a sensible fallback; per-instance state versus shared state. |
| Compensating Transaction | Undo earlier completed steps of a multi-step process with explicit reverse operations when a later step fails. Solves consistency without distributed locks (the basis of the saga). | Workflows across services with no shared transaction. | Compensations must be idempotent and may themselves fail; some actions cannot be undone (an email already sent); intermediate states are visible. |
| Retry | Retry a transient failure, with backoff and jitter, a limited number of times. Solves brief network or service blips. See Vol 3 Ch 14. | Transient faults on idempotent operations. | Retrying non-idempotent calls duplicates effects; retries multiply load during an outage (use budgets and a breaker); stack of retries across layers. |
| Throttling | Control how much of a resource a consumer may use, and reject, delay or degrade the excess. Solves overload and noisy neighbours. See Ch 8. | Shared services, multi-tenant APIs, autoscaling lag. | Return clear 429s with `Retry-After`; unfair limits; clients must back off. |

#### 12.2.5 Security patterns

| Pattern | What it is / problem it solves | Use when | Watch out |
|---------|--------------------------------|----------|-----------|
| Federated Identity | Delegate authentication to an external identity provider (OIDC, SAML) instead of storing credentials yourself. Solves password management and single sign-on across apps. | Enterprise SSO, social login, partner access. See Ch 18. | The identity provider becomes a critical dependency; token validation, claim mapping and logout are subtle. |
| Gatekeeper | A dedicated front-end host validates and sanitises requests, then forwards only the clean ones to the trusted back end. Solves exposing the component that holds data or privileges. | Sensitive workloads; limiting the damage of a compromised front end. | Another hop and component; it must hold no secrets and have minimal privileges; do not make it a bottleneck. |
| Valet Key | A scoped, short-lived token for direct access to one resource (listed under data management above). Solves granting access without proxying or sharing full credentials. | Pre-signed uploads and downloads, delegated access. | Treat the token as a secret; keep the scope and lifetime small. |

#### 12.2.6 Which pattern for which problem

| Problem | Reach for |
|---------|-----------|
| Traffic spikes overwhelm a backend | Queue-Based Load Leveling, Throttling, Competing Consumers |
| Remote dependency is failing or slow | Circuit Breaker, Retry (with backoff), Bulkhead |
| Messages too large for the broker | Claim Check |
| Operation takes minutes, caller is HTTP | Asynchronous Request-Reply |
| Many systems react to one event | Publisher/Subscriber, Choreography |
| Related messages must stay in order | Sequential Convoy |
| Urgent work stuck behind bulk work | Priority Queue |
| Reads are slow or expensive | Cache-Aside, Materialized View, CQRS |
| One database node is full | Sharding, Index Table (for secondary lookups) |
| Need full history and audit | Event Sourcing |
| Rewriting a legacy system safely | Strangler Fig + Anti-Corruption Layer |
| Cross-cutting concerns in many services | Sidecar, Ambassador, Gateway Offloading |
| Different clients need different APIs | Backends for Frontend, Gateway Aggregation |
| Only one instance may do a job | Leader Election |
| Multi-step workflow across services fails halfway | Compensating Transaction, Scheduler Agent Supervisor |
| Tenant or regional isolation and scale | Deployment Stamps, Geodes |
| Upload or download without proxying | Valet Key, Static Content Hosting |
| Do not store passwords or sessions yourself | Federated Identity |
| Protect the trusted back end from raw input | Gatekeeper |
| Change settings without redeploying | External Configuration Store |
| Know whether an instance is healthy | Health Endpoint Monitoring |

---

## 12.3 Key Takeaways

- Learn Circuit Breaker, Retry, Cache-Aside, CQRS, Publisher/Subscriber, Strangler Fig and Sidecar first.
- A pattern is a tool with a cost; use a handful where a real problem exists.
- Most patterns are provider-neutral and map to AWS, GCP, Azure and Kubernetes equivalents.

## 12.4 Sample Interview Questions

- When would you use Queue-Based Load Leveling instead of autoscaling?
- How does a Strangler Fig migration reduce risk?
- What does a Sidecar give you that a library does not?
- Compare Cache-Aside with Materialized View.
- What is a Claim Check and when do you need one?

## 12.5 Further Reading

- Azure Architecture Center, *Cloud Design Patterns*
- Sam Newman, *Building Microservices*
- AWS Well-Architected Framework

---

**Next Up:** [Chapter 13 — Multi-Tenancy →](./13%20-%20Multi-Tenancy.md)
