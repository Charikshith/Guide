# Gap analysis: my plan vs roadmap.sh vs GeeksforGeeks

Sources:
- roadmap.sh: https://roadmap.sh/system-design
- GFG: https://www.geeksforgeeks.org/system-design/getting-started-with-system-design/

"My plan" means this repo. Results come from keyword search over the `.md` chapters. Chapters were not read in full. A "No" can mean "only a passing mention".

| Topic | My plan | Roadmap | GFG |
|---|---|---|---|
| Intro / what is system design | No | Yes | Yes |
| How to approach a design problem | No | Yes | Yes |
| Requirements, functional vs non-functional | No | No | Yes |
| SDLC, system analysis vs design | No | No | Yes |
| HLD vs LLD difference | No | No | Yes |
| Monolith vs distributed | No | No | Yes |
| Capacity estimation | Yes | No | Yes |
| Performance vs scalability | No | Yes | No |
| Latency vs throughput | No | Yes | No |
| Scalability and bottlenecks | Yes | Yes | Yes |
| Availability, reliability, consistency | Yes | Yes | Yes |
| CAP theorem | Yes | Yes | Yes |
| Failover, active-active | Yes | Yes | No |
| Availability numbers (99.9%) | Yes | Yes | No |
| DNS | Yes | Yes | No |
| CDN (push vs pull) | Yes (push/pull: No) | Yes | Yes |
| Load balancing | Yes | Yes | Yes |
| Reverse proxy, web server | No | Yes | Yes |
| API gateway | No | Yes | Yes |
| Microservices | Yes | Yes | No |
| Service discovery, sidecar | Yes | Yes | No |
| Service mesh | Yes | No | No |
| SQL vs NoSQL | Yes | Yes | Yes |
| Database design | Yes | No | Yes |
| Sharding | Yes | Yes | Yes |
| Replication | Yes | Yes | Yes |
| Federation | No | Yes | No |
| Denormalization, SQL tuning | Yes | Yes | No |
| NoSQL types (KV, doc, wide-column) | Yes | Yes | No |
| Graph databases | No | Yes | No |
| Block, object, file storage | No | No | Yes |
| File vs database storage | No | No | Yes |
| Data partitioning | Yes | No | Yes |
| Caching strategies | Yes | Yes | Yes |
| Message queues | Yes | Yes | Yes |
| Back pressure | Yes | Yes | No |
| Rate limiting, throttling | Yes | Yes | No |
| Background jobs | Yes | Yes | No |
| Idempotency | Yes | Yes | No |
| Communication (HTTP, TCP, UDP, REST, gRPC, GraphQL) | Yes | Yes | Yes |
| Performance antipatterns | No | Yes | No |
| Monitoring and alerts | No | Yes | No |
| Event-driven, event sourcing, CQRS | Yes | Yes | No |
| Saga, compensating transaction | Yes | Yes | No |
| Pub/sub, competing consumers | Yes | Yes | No |
| Claim check, pipes and filters, sequential convoy | No | Yes | No |
| Strangler fig | No | Yes | No |
| Gateway routing/offloading/aggregation, BFF | No | Yes | No |
| Valet key, static content hosting | No | Yes | No |
| Deployment stamps, geodes | No | Yes | No |
| Leader election | Yes | Yes | No |
| Circuit breaker, retry, bulkhead | Yes (bulkhead: No) | Yes | No |
| Anti-corruption layer | Yes | Yes | No |
| Security, auth, federated identity | Yes (federated identity: No) | Yes | Yes |
| Containerization | Yes | No | Yes |
| OOP, OOAD, SOLID | Yes | No | Yes |
| UML (activity diagrams: No) | Yes | No | Yes |
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
| Optimization, DSA for design, modularity | No | No | Yes |

## Summary

- Rows where "My plan" is No: 22.
- Roadmap supplies most of them: cloud design patterns, performance antipatterns, monitoring.
- GFG supplies the rest: requirements, SDLC, HLD vs LLD, storage types, optimization.
- Not on either site, but in this repo: service mesh, multi-tenancy, DR, cloud architecture, cost, concurrency, DDD, clean/hexagonal architecture, the 30 full designs.

## Suggested chapters

1. Vol 4: "Approaching a design problem" (requirements, functional vs non-functional, HLD vs LLD, monolith vs distributed, latency vs throughput).
2. Vol 4: "Cloud design patterns and performance antipatterns" (strangler fig, claim check, valet key, gateway patterns, BFF, bulkhead, deployment stamps, antipatterns, monitoring).
3. Small additions: block/object/file storage, graph databases, federation, push vs pull CDN, web servers and proxies, activity diagrams.
