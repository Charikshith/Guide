# Cloud Architecture & Cost

Every architectural choice has a price. This chapter covers the cloud choices that shape a design (managed vs self-run, serverless vs containers vs VMs) and how to reason about cost per request, per tenant and per customer.

---

## 14.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Apply the cloud well-architected pillars to a design.
2. Choose between serverless, containers and virtual machines with a break-even sketch.
3. Reason about cost per request, per active customer and per tenant.
4. Right-size continuously instead of once.

---

## 14.2 Cloud Architecture Choices

Cloud building blocks (compute, storage, networking, managed services), serverless vs containers, and cost-aware design.

**In one sentence:** cloud architecture is choosing and connecting rented building blocks — compute, storage, networking, and managed services — so the system meets its reliability, performance, security, and cost goals with the least undifferentiated work for your team.

**Mental model — building with LEGO Technic vs carving wood.** On-premises you carve every part yourself: servers, racks, databases, backups. In the cloud you snap together ready-made parts (a managed database, a queue, a load balancer) that someone else maintains. The skill moves from making parts to choosing the right parts, connecting them safely, and not buying far more bricks than you need.

**The building blocks (AWS / GCP / Azure names)**

| Category | Options | Use |
|----------|---------|-----|
| **Compute** | VMs (EC2 / Compute Engine / VMs); containers (EKS/ECS, GKE, Cloud Run, AKS, Container Apps); functions (Lambda, Cloud Functions, Azure Functions) | run code |
| **Storage** | object (S3 / GCS / Blob); block (EBS / PD / Managed Disks); file (EFS / Filestore / Files) | files, volumes, shared file systems |
| **Databases** | relational (RDS/Aurora, Cloud SQL/AlloyDB, Azure SQL); NoSQL (DynamoDB, Firestore/Bigtable, Cosmos DB); caches (ElastiCache, Memorystore); warehouses (Redshift, BigQuery, Synapse) | data |
| **Networking** | VPC/VNet, subnets, NAT, load balancers, DNS, CDN, private endpoints, transit gateways | connectivity and isolation |
| **Integration** | queues (SQS, Pub/Sub, Service Bus), streams (Kinesis, managed Kafka), workflows (Step Functions, Workflows), API gateways, event buses (EventBridge) | decoupling |
| **Identity & security** | IAM, KMS, secrets managers, WAF | Ch 18 |
| **Observability** | CloudWatch, Cloud Monitoring/Logging, Azure Monitor, managed Prometheus/Grafana | operations |

**Serverless vs containers vs VMs**

| | Functions (Lambda) | Serverless containers (Cloud Run, Fargate) | Kubernetes / VMs |
|-|--------------------|-------------------------------------------|------------------|
| Unit | a function per event | a container, scaled per request | pods/processes you manage |
| Scaling | per request, to zero, very fast | per request/concurrency, to zero (Cloud Run) | autoscalers you configure; rarely to zero |
| Max run time | ~15 min (Lambda) | long (up to 60 min per request on Cloud Run; unlimited on Fargate tasks) | unlimited |
| Cold starts | yes (100 ms–seconds) | yes, smaller with min instances | none |
| Ops burden | lowest | low | highest |
| Cost at low/bursty traffic | **lowest** (pay per ms) | low | idle capacity costs money |
| Cost at high steady traffic | can be **highest** | moderate | **lowest** per unit (with commitments) |
| Portability / control | lowest | high (it's a container) | highest |
| Fits | event glue, webhooks, cron, spiky APIs | most web APIs and workers | large platforms, special hardware/networking, steady heavy load |

**Break-even sketch:** Lambda at 512 MB, 100 ms per request ≈ $0.00000083 compute + $0.0000002 request ≈ **$1.03 per million requests**. A 2-vCPU container at ~$50/month handling 200 req/s sustained ≈ 518M requests/month ≈ **$0.10 per million**. Serverless wins at low or spiky volume; containers win at high steady volume. Always model your own numbers.

**Managed services — when sensible:** use managed databases, queues, caches, and object storage unless you have a strong reason not to (special performance, cost at huge scale, portability requirements). Running your own Postgres HA with backups, patching, and failover is a full-time job.

**Lock-in, sensibly** — lock-in isn't binary; it's a cost you weigh. Low-regret choices: standard interfaces (Postgres, Kafka API, S3 API, OCI containers, Kubernetes, OpenTelemetry, Terraform). Accept deep lock-in where the service gives a big advantage (DynamoDB, BigQuery), and keep your domain logic behind your own interfaces (Vol 3 Ch 9) so a later migration touches adapters, not everything.

**Well-architected pillars** (shared by the major clouds): operational excellence, security, reliability, performance efficiency, cost optimization, sustainability.

---

## 14.3 Cost and Capacity Economics

Unit economics, cloud cost drivers, right-sizing, and cost as a design constraint.

**In one sentence:** at the design level, cost is a requirement like latency — you estimate the cost of an architecture before building it, express it per unit of business value, find which components dominate as scale grows, and choose designs whose cost grows slower than revenue.

**Mental model — running a restaurant.** You don't just look at the monthly total. You know the *cost per plate*: ingredients, staff minutes, a share of rent. If a dish costs €9 to make and sells for €8, selling more of it makes things worse. Architecture decisions set your cost per plate.

This chapter is the **design-time** view. For operational cost hygiene (tagging, right-sizing a running cluster, purchase models), see Vol 1 Ch 59.

**Unit economics**

| Metric | Formula | Use |
|--------|---------|-----|
| Cost per request | infra cost ÷ requests | API efficiency; compare services |
| **Cost per active customer / tenant** | infra cost ÷ monthly active customers (or tenants) | pricing, margins, plan design |
| Cost per transaction / order | infra cost ÷ orders | e-commerce, payments |
| Cost per GB stored / processed | storage or pipeline cost ÷ GB | data platforms |
| Infra cost as % of revenue (COGS) | infra ÷ revenue | SaaS gross margin (healthy SaaS: infra ≈ 5–15% of revenue) |
| Marginal cost | Δcost ÷ Δunits | does the next customer cost less than the average? |

**How costs scale with design choices**

| Design choice | Cost behavior |
|---------------|---------------|
| Per-tenant silos | fixed cost per tenant → bad for many small tenants (Ch 15) |
| Fan-out on write for feeds | writes × followers: celebrities explode cost |
| Synchronous calls to paid APIs per request | linear in traffic × price; cache or batch |
| Keeping all logs / traces | linear in traffic × retention; sample and tier |
| Multi-region active-active | ~2–3× infra + cross-region transfer |
| Chatty microservices across AZs | transfer charges per GB on every hop |
| LLM calls per request | often the *largest* cost line; see Vol 5 Ch 18 |

**Right-sizing, continuously** — compare provisioned capacity with p95 usage (CPU, memory, IOPS, connections); keep headroom for SLOs (e.g. target 60–70% CPU at peak); autoscale; review monthly because usage drifts; pick newer, cheaper instance families (ARM).

**Reducing spend without hurting reliability**

1. Measure unit cost and the SLOs *together* on one dashboard.
2. Remove pure waste first (idle, orphaned, over-retained) — no reliability impact.
3. Right-size with load tests, one change at a time; watch p99 and errors.
4. Buy commitments only for the proven steady baseline.
5. Architectural changes (caching, batching, tiered storage, fewer cross-zone hops) — with ADRs.
6. Never cut redundancy that the SLO depends on (multi-AZ, backups) without an explicit decision.

---

## 14.4 Key Takeaways

- Managed services trade money for operational load; use them unless a constraint says otherwise.
- Cost is a design-time property: estimate unit economics before you build.
- Lock-in is a cost to weigh, not a sin to avoid.

## 14.5 Sample Interview Questions

- When is serverless cheaper than containers, and when is it not?
- How would you estimate cost per active customer?
- What does right-sizing mean in practice?
- How do you weigh lock-in against managed-service convenience?

## 14.6 Further Reading

- AWS Well-Architected Framework, Cost Optimization pillar
- J.R. Storment and Mike Fuller, *Cloud FinOps*

---

**Next Up:** [Chapter 15 — The System Design Blueprint →](./15%20-%20The%20System%20Design%20Blueprint.md)
