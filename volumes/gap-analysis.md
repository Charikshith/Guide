# Gap analysis: my plan vs roadmap.sh vs GeeksforGeeks

Sources:
- roadmap.sh: https://roadmap.sh/system-design
- GFG: https://www.geeksforgeeks.org/system-design/getting-started-with-system-design/

"My plan" means this repo. **[NEW chN]** marks a topic added in Vol 4 chapter N, to close a gap. Coverage was checked by keyword search over the `.md` chapters.

## New chapters (Vol 4)

| Tag | Chapter | Fills |
|---|---|---|
| **[NEW ch01]** | [Approaching a System Design Problem](volume-4-high-level-design/ch01-approaching-a-system-design-problem.md) | requirements, FR/NFR, SDLC, HLD vs LLD, monolith vs distributed, method, latency/throughput, optimization, modularity, DSA, activity diagrams |
| **[NEW ch05]** | [Proxies, Gateways, Web Servers & Storage Types](volume-4-high-level-design/ch05-proxies-gateways-web-servers-and-storage-types.md) | proxies, web servers, API gateway patterns, BFF, push/pull CDN, block/object/file storage, federation, graph databases |
| **[NEW ch13]** | [Cloud Design Patterns](volume-4-high-level-design/ch13-cloud-design-patterns.md) | the full cloud design pattern catalog (messaging, data, design, reliability, security) |
| **[NEW ch16]** | [Performance Antipatterns & Monitoring](volume-4-high-level-design/ch16-performance-antipatterns-and-monitoring.md) | 10 antipatterns, bulkhead, monitoring types, instrumentation, alerting |

## Table

| Topic | My plan | Roadmap | GFG |
|---|---|---|---|
| Intro / what is system design | Yes **[NEW ch01]** | Yes | Yes |
| How to approach a design problem | Yes **[NEW ch01]** | Yes | Yes |
| Requirements, functional vs non-functional | Yes **[NEW ch01]** | No | Yes |
| SDLC, system analysis vs design | Yes **[NEW ch01]** | No | Yes |
| HLD vs LLD difference | Yes **[NEW ch01]** | No | Yes |
| Monolith vs distributed | Yes **[NEW ch01]** | No | Yes |
| Capacity estimation | Yes | No | Yes |
| Performance vs scalability | Yes **[NEW ch01]** | Yes | No |
| Latency vs throughput | Yes **[NEW ch01]** | Yes | No |
| Scalability and bottlenecks | Yes | Yes | Yes |
| Availability, reliability, consistency | Yes | Yes | Yes |
| CAP theorem | Yes | Yes | Yes |
| Failover, active-active | Yes | Yes | No |
| Availability numbers (99.9%) | Yes | Yes | No |
| DNS | Yes | Yes | No |
| CDN (push vs pull) | Yes (push/pull: **[NEW ch05]**) | Yes | Yes |
| Load balancing | Yes | Yes | Yes |
| Reverse proxy, web server | Yes **[NEW ch05]** | Yes | Yes |
| API gateway | Yes **[NEW ch05]** | Yes | Yes |
| Microservices | Yes | Yes | No |
| Service discovery, sidecar | Yes | Yes | No |
| Service mesh | Yes | No | No |
| SQL vs NoSQL | Yes | Yes | Yes |
| Database design | Yes | No | Yes |
| Sharding | Yes | Yes | Yes |
| Replication | Yes | Yes | Yes |
| Federation | Yes **[NEW ch05]** | Yes | No |
| Denormalization, SQL tuning | Yes | Yes | No |
| NoSQL types (KV, doc, wide-column) | Yes | Yes | No |
| Graph databases | Yes **[NEW ch05]** | Yes | No |
| Block, object, file storage | Yes **[NEW ch05]** | No | Yes |
| File vs database storage | Yes **[NEW ch05]** | No | Yes |
| Data partitioning | Yes | No | Yes |
| Caching strategies | Yes | Yes | Yes |
| Message queues | Yes | Yes | Yes |
| Back pressure | Yes | Yes | No |
| Rate limiting, throttling | Yes | Yes | No |
| Background jobs | Yes | Yes | No |
| Idempotency | Yes | Yes | No |
| Communication (HTTP, TCP, UDP, REST, gRPC, GraphQL) | Yes | Yes | Yes |
| Performance antipatterns | Yes **[NEW ch16]** | Yes | No |
| Monitoring and alerts | Yes **[NEW ch16]** | Yes | No |
| Event-driven, event sourcing, CQRS | Yes | Yes | No |
| Saga, compensating transaction | Yes | Yes | No |
| Pub/sub, competing consumers | Yes | Yes | No |
| Claim check, pipes and filters, sequential convoy | Yes **[NEW ch13]** | Yes | No |
| Strangler fig | Yes **[NEW ch13]** | Yes | No |
| Gateway routing/offloading/aggregation, BFF | Yes **[NEW ch07, ch13]** | Yes | No |
| Valet key, static content hosting | Yes **[NEW ch13]** | Yes | No |
| Deployment stamps, geodes | Yes **[NEW ch13]** | Yes | No |
| Leader election | Yes | Yes | No |
| Circuit breaker, retry, bulkhead | Yes (bulkhead: **[NEW ch17, ch16]**) | Yes | No |
| Anti-corruption layer | Yes | Yes | No |
| Security, auth, federated identity | Yes (federated identity: **[NEW ch13]**) | Yes | Yes |
| Containerization | Yes | No | Yes |
| OOP, OOAD, SOLID | Yes | No | Yes |
| UML and activity diagrams | Yes (activity diagrams: **[NEW ch01]**) | No | Yes |
| Creational, structural, behavioral patterns | Yes | No | Yes |
| Clean, hexagonal architecture, DDD | Yes | No | No |
| Concurrency, thread safety | Yes | No | No |
| Multi-tenancy | Yes | No | No |
| Disaster recovery, RTO/RPO | Yes | No | No |
| Cloud architecture | Yes | No | No |
| Cost economics | Yes | No | No |
| Design Dropbox, Twitter, Netflix, Uber, etc. | Yes | No | Yes |
| 30 full system designs | Yes | No | No |
| Interview prep | Yes | No | Yes |
| Optimization, DSA for design, modularity | Yes **[NEW ch01]** | No | Yes |
| Other performance antipatterns: retry storm, noisy neighbor, No Caching | Yes **[NEW ch16]** | Yes | No |
| Async request-reply, index table, materialized view, compute resource consolidation, external config, scheduler agent supervisor, queue-based load leveling, gatekeeper | Yes **[NEW ch13]** | Yes | No |
| Interoperability, usability, maintainability, optimization techniques | Yes **[NEW ch01]** | No | Yes |
| DSA for system design, activity diagrams | Yes **[NEW ch01]** | No | Yes |

## Summary

- Rows where "My plan" was No before: 22. All 22 are now Yes.
- Total chapters: 139 (Vol 4 now has 21).
- Not on either site, but in this repo: service mesh, multi-tenancy, DR, cloud architecture, cost, concurrency, DDD, clean/hexagonal architecture, the 30 full designs.
