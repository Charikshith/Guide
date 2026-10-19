# Chapter 3 — Scalability & Reliability Fundamentals

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 2 — Capacity Planning](ch02-capacity-planning.md) · Next → [Chapter 4 — Distributed Systems Patterns](ch04-distributed-systems-patterns.md)

---

## Concept

Vertical vs horizontal scaling, statelessness, redundancy, failure domains, availability math (N nines).

**In one sentence:** you scale by buying a bigger machine (vertical) or more machines (horizontal); horizontal scaling needs stateless servers; and reliability comes from redundancy spread across independent failure domains, which you can reason about with simple probability.

**Read the full explanation in the AI Library** (it is explained there once, so this chapter does not repeat it):

* [Chapter 6 — Types of Scalability](https://charikshith.github.io/AI_Library/notes/system-design/chapters/6%20-%20Scalability%20in%20System%20Design.html#64-types-of-scalability)
* [Chapter 6 — Stateless Service Design](https://charikshith.github.io/AI_Library/notes/system-design/chapters/6%20-%20Scalability%20in%20System%20Design.html#613-stateless-service-design)
* [Chapter 9 — The 9s of Availability — What "Five Nines" Actually Means](https://charikshith.github.io/AI_Library/notes/system-design/chapters/9%20-%20Reliability%2C%20Availability%20%26%20Disaster%20Recovery.html#913-the-9s-of-availability--what-five-nines-actually-means)
* [Chapter 9 — Availability Math and Failure Domains](https://charikshith.github.io/AI_Library/notes/system-design/chapters/9%20-%20Reliability%2C%20Availability%20%26%20Disaster%20Recovery.html#9132-availability-math-and-failure-domains)
* [Chapter 9 — High Availability, Fault Tolerance & Failover](https://charikshith.github.io/AI_Library/notes/system-design/chapters/9%20-%20Reliability%2C%20Availability%20%26%20Disaster%20Recovery.html#96-high-availability-fault-tolerance--failover)

This chapter is the **practice layer**: the diagram, worked example, exercises, mini-project, design prompt, open-source reading, interview questions and checklist below.

---

## Prereqs

* [Chapter 2 — Capacity Planning](ch02-capacity-planning.md)

---

## Diagram

**Scale-up vs scale-out**

```
 SCALE UP                                SCALE OUT
 ┌──────────────┐                        ┌────┐ ┌────┐ ┌────┐ ┌────┐
 │              │                        │ 4c │ │ 4c │ │ 4c │ │ 4c │  … add more
 │   64 cores   │                        └────┘ └────┘ └────┘ └────┘
 │   512 GB     │                             ▲      ▲      ▲
 │              │                        ┌────┴──────┴──────┴────┐
 └──────────────┘                        │     load balancer     │
 one box, one failure = outage           └───────────────────────┘
```

**Redundancy across failure domains, with the availability formula**

```mermaid
flowchart TB
    LB["load balancer (multi-AZ, managed)"]
    subgraph AZa["Zone A"]
      A1["api"] & A2["api"]
    end
    subgraph AZb["Zone B"]
      B1["api"] & B2["api"]
    end
    subgraph AZc["Zone C"]
      C1["api"] & C2["api"]
    end
    LB --> A1 & A2 & B1 & B2 & C1 & C2
    A1 & B1 & C1 --> DB[("DB primary (Zone A)<br/>+ sync standby (Zone B)")]
```

```
 zone availability 99.9%, 3 zones in parallel:   1 − (0.001)³ = 99.9999999%  (if independent)
 in series with the DB pair (99.99%):             ≈ 99.99%  ← the DB now limits the system
```

**Series vs parallel**

```
 SERIES    [A 99.9%]──[B 99.9%]           = 0.999 × 0.999        = 99.80%
 PARALLEL  ┌─[A 99.9%]─┐
           └─[B 99.9%]─┘                  = 1 − 0.001 × 0.001    = 99.9999%
```

---

## Example

```python
from functools import reduce

def series(*parts):   return reduce(lambda a, b: a * b, parts, 1.0)
def parallel(a, n):   return 1 - (1 - a) ** n

print(f"{series(0.999, 0.999):.4%}")          # 99.8001%
print(f"{parallel(0.999, 2):.6%}")            # 99.999900%
print(f"{series(*[0.999] * 5):.4%}")          # 99.5010% — 5 services in a chain

def downtime(avail, period_h=24 * 365):
    return (1 - avail) * period_h * 60        # minutes
for a in (0.99, 0.999, 0.9999, 0.99999):
    print(f"{a:.3%}: {downtime(a):8.1f} min/year")
```

**Making a stateful service horizontally scalable**

```
 BEFORE: sessions in process memory      AFTER: sessions in Redis
 user → LB → api-2 (has the session)     user → LB → any api node → Redis session:abc
 api-2 dies → the user is logged out     node dies → the next request goes elsewhere, still logged in
 sticky sessions needed                  no stickiness needed; autoscale freely
```

---

## Exercises

1. Compute availability of three nines across 5 services.

   <details><summary>Solution</summary>In series: 0.999⁵ ≈ 99.50%, about 44 hours of downtime a year — much worse than any single service. Fixes: remove dependencies from the critical path, make calls optional (degrade gracefully), add redundancy per service, or use async processing.</details>

2. Make a stateful service horizontally scalable.

   <details><summary>Solution</summary>Find all state held in memory or on local disk: sessions, uploads, caches, scheduled jobs, in-memory queues. Move sessions to Redis or signed tokens, files to object storage, caches to a shared cache (or accept per-node caches), queues to a broker, and cron to a single scheduler with leader election. Then any node can serve any request.</details>

3. Why doesn't running 3 replicas in the same rack give "three nines times three"?

   <details><summary>Solution</summary>The parallel formula needs independent failures. A rack power or switch failure takes all three down together. Spread across racks, zones, or regions to make failures independent.</details>

---

## Mini project

**An availability/reliability calculator with failure-domain modeling.**

```mermaid
flowchart LR
    Y["system.yaml:<br/>components (availability, zone)<br/>dependencies (series)<br/>replica groups (parallel)"] --> G["build a dependency graph"]
    G --> CALC["compute end-to-end availability"]
    G --> SIM["Monte Carlo: fail zones / hosts<br/>with correlated probabilities"]
    CALC & SIM --> R["report: availability, downtime/year,<br/>weakest component, what-if (add a replica, remove a dependency)"]
```

**Steps**

1. Describe components, their availability, their failure domain (zone), and how they combine.
2. Compute availability analytically for series/parallel groups.
3. Monte Carlo simulation where a zone failure takes down all components in it; compare with the analytic (independent) result.
4. Report the weakest link and the effect of each "what-if".

**Done when:** the simulation shows how correlated zone failures lower availability compared with the naive formula.

---

## Design

**Design a highly available stateless API tier.**

Target: 99.99% for the API tier, 20,000 peak QPS, zero-downtime deploys.

```mermaid
flowchart TB
    DNS["DNS (health-checked)"] --> GLB["regional load balancer<br/>(managed, multi-AZ)"]
    GLB --> ASG1["API nodes, zone A<br/>autoscaling group"]
    GLB --> ASG2["API nodes, zone B"]
    GLB --> ASG3["API nodes, zone C"]
    ASG1 & ASG2 & ASG3 --> R[("Redis (sessions)<br/>multi-AZ replicas")]
    ASG1 & ASG2 & ASG3 --> DB[("Postgres primary +<br/>sync standby in another zone")]
    ASG1 & ASG2 & ASG3 --> OBJ[("object storage")]
```

**Capacity:** 20,000 QPS ÷ (1,000 QPS/node × 0.7) ≈ 29 nodes; to survive losing a whole zone, the remaining two zones must carry the peak, so 29 ÷ 2 ≈ 15 per zone → **45 nodes** (15 × 3).

**Decisions to justify**

* **Stateless nodes** (sessions in Redis, files in object storage), so the autoscaler can replace nodes freely.
* **N+1 zones:** each zone holds enough capacity to lose one zone at peak.
* **Health checks** (readiness vs liveness) and connection draining for zero-downtime rolling deploys.
* **Timeouts, retries with jitter, and circuit breakers** around the DB and cache; serve degraded responses if a non-critical dependency fails.
* **The DB is the availability bottleneck:** synchronous standby in another zone with automatic failover; read replicas for scale.

---

## Open source

* [`donnemartin/system-design-primer`](https://github.com/donnemartin/system-design-primer) — sections on "Availability vs consistency", "Availability in numbers", and scaling a web app step by step. See also Google's *Site Reliability Engineering* book.

---

## Interview

1. **"Horizontal vs vertical scaling?"**
   <details><summary>Answer</summary>Vertical: a bigger machine — simple, no code change, but it has a ceiling and remains a single point of failure. Horizontal: more machines behind a load balancer — no hard ceiling and tolerant of node loss, but it requires stateless design, data partitioning, and coordination. Typically scale the stateless tier horizontally from the start and scale the database vertically first, then with replicas and sharding.</details>

2. **"What does 99.99% allow per year?"**
   <details><summary>Answer</summary>About 52.6 minutes of downtime per year (~4.4 minutes per month). That is too little time for a human to notice, diagnose, and fix most problems, so it requires automatic failover, redundancy across zones, safe deploys, and fast rollbacks.</details>

---

## Checklist

- [ ] design for statelessness
- [ ] spread across failure domains
- [ ] compute availability correctly

---

> [Contents](index.md) · ← [Chapter 2 — Capacity Planning](ch02-capacity-planning.md) · Next → [Chapter 4 — Distributed Systems Patterns](ch04-distributed-systems-patterns.md)
