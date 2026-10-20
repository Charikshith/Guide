# Distributed Systems Fundamentals

Almost every large system is a handful of distributed-systems ideas combined: copy data for safety, split it for scale, and agree on what is true when machines and networks fail. This chapter collects those ideas, the failure modes they create, and how event-driven designs put them to work.

---

## 11.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Explain replication, partitioning and quorums, and choose R and W for a target consistency level.
2. Name the failure modes (partial failure, partitions, clock skew, duplicates, reordering) that every design must tolerate.
3. Compare choreography with orchestration and pick event types, schemas and delivery guarantees deliberately.
4. Apply the standard fixes: idempotency, outbox, schema registry, dead-letter queues and replay.

---

## 11.2 Distributed Systems Patterns and Failure Modes

Replication, partitioning, leader/follower, quorums, idempotency, and the failure modes that shape every design.

**In one sentence:** almost every large system combines a few patterns — copy data for safety (replication), split data for scale (partitioning), let one node decide writes (leader/follower), require overlapping majorities (quorums), and make repeated requests harmless (idempotency) — because networks lose, delay, and duplicate messages and nodes fail in partial, confusing ways.

**Mental model — a team spread across cities.** Each office keeps copies of important files (replication), each office owns certain customers (partitioning), one manager signs off changes (leader), big decisions need a majority vote (quorum), and every instruction has a reference number so doing it twice doesn't double-pay anyone (idempotency). The phone lines are unreliable, so every rule assumes a message may be lost or arrive twice.

**The patterns**

| Pattern | Solves | Key trade-off | Deep dive |
|---------|--------|---------------|-----------|
| Replication | durability, availability, read scale | consistency lag (async) vs latency (sync) | Vol 1 Ch 51 |
| Partitioning / sharding | write scale, data size | cross-partition queries, hot spots, resharding | Ch 11 |
| Leader / follower | a single place to order writes | failover time; leader bottleneck | |
| Leader election / consensus | exactly one leader, even after failures | needs a majority; slower writes | Raft, etcd |
| **Quorums** | tunable consistency without a single leader | R + W > N for overlap | Dynamo, Cassandra |
| **Idempotency** | safe retries in a world of duplicates | storing keys / dedup state | Vol 3 Ch 14 |
| Leases + fencing tokens | safe locks despite pauses | clock assumptions | |
| Heartbeats + timeouts | failure detection | false positives vs slow detection | |

**Quorums** — with N replicas, a write waits for W acknowledgments and a read asks R replicas. If **R + W > N**, every read set overlaps every write set in at least one replica, so a read sees the latest acknowledged write (use version numbers to pick it). Common: N = 3, W = 2, R = 2. Trade: W = 1 is fast writes but weak durability; R = 1 is fast reads but possibly stale.

**Failure modes that shape every design**

| Failure | What it looks like | Defense |
|---------|--------------------|---------|
| Crash | a node stops | replication + failover |
| **Partial failure** | a node is slow, or some requests fail | timeouts, retries with backoff, hedging, circuit breakers |
| Network partition | two groups can't talk | quorums; the minority side refuses writes |
| **Split-brain** | two nodes both think they are leader | majority-based election, fencing tokens, STONITH |
| Message loss / duplication / reordering | retries create duplicates | idempotency keys, sequence numbers |
| Clock skew | timestamps disagree across nodes | logical clocks, avoid last-write-wins on wall time |
| Gray failure | health checks pass but real traffic fails | health checks that exercise real paths; outlier detection |
| Cascading failure | retries and overload spread to neighbors | load shedding, backpressure (Ch 8), retry budgets |

**The eight fallacies of distributed computing** — the network is reliable; latency is zero; bandwidth is infinite; the network is secure; topology doesn't change; there is one administrator; transport cost is zero; the network is homogeneous. Every one is false.

---

## 11.3 Event-Driven Systems in Practice

Event producers/consumers, event schemas, ordering, idempotency, and eventual consistency.

**In one sentence:** in an event-driven system, services announce facts ("an order was placed") instead of calling each other directly, and any number of other services react on their own schedule — which decouples teams and absorbs load spikes, at the price of eventual consistency and careful handling of order and duplicates.

**Mental model — a town crier vs phone calls.** In request/response, the order clerk must phone billing, shipping, and analytics one by one, and if shipping doesn't answer, the order is stuck. With events, the clerk shouts "Order 123 placed!" in the square once; whoever cares writes it down and acts. New listeners can join without the clerk changing anything. But nobody knows exactly *when* each listener acted.

**Event-driven vs request/response**

| | Request/response (sync) | Event-driven (async) |
|-|-------------------------|----------------------|
| Coupling | caller knows every callee, their API, and their availability | the producer knows only the event schema |
| Failure | a callee failure fails the caller (cascades) | consumers fail independently; the log buffers |
| Latency to the user | the sum of the chain | fast acknowledgment; work finishes later |
| Consistency | immediate (if every step succeeded) | **eventual** |
| Adding a new reaction | change the caller | add a consumer |
| Debugging | a stack trace / one trace | distributed: needs correlation IDs and tracing |
| Best for | queries; things the user needs *now* | side effects, integration, fan-out, analytics, workflows |

**Kinds of events**

| Kind | Payload | Example | Trade-off |
|------|---------|---------|-----------|
| Notification | just the ID | `OrderPlaced {order_id}` | small; consumers call back for details (coupling + load) |
| **Event-carried state transfer** | the data consumers need | `OrderPlaced {order_id, customer, items, total}` | consumers are autonomous; bigger events; schema is a contract |
| Domain event (event sourcing) | the state change itself | Vol 1 Ch 52 | full history |

**Choreography vs orchestration**

| | Choreography | Orchestration |
|-|--------------|---------------|
| How | each service reacts to events and emits its own | a central orchestrator (a saga coordinator, Temporal, Step Functions) tells each step what to do |
| Pros | fully decoupled; no central point | the flow is visible in one place; easy timeouts and compensation |
| Cons | the overall flow is implicit and hard to follow | the orchestrator knows every participant |
| Use | simple fan-out reactions | multi-step business processes with compensation (sagas) |

**The hard parts and their fixes**

| Problem | Fix |
|---------|-----|
| Duplicates (at-least-once delivery) | **idempotent consumers**: dedup by `event_id` in the same transaction as the side effect |
| Ordering | partition by the entity key (`order_id`); rely on per-key order only; use sequence numbers to detect gaps |
| Writing to the DB *and* publishing the event atomically | the **transactional outbox**: write the event to an `outbox` table in the same DB transaction; a relay publishes it (or CDC with Debezium) |
| Poison messages | bounded retries → a **dead-letter queue**, with alerting and replay tooling |
| Schema evolution | versioned schemas in a **schema registry** with compatibility rules (backward/forward) |
| Eventual consistency in the UI | show "processing"; return a version; read your own writes from the source |
| Tracing a flow | carry `correlation_id` and `causation_id` in every event; propagate trace context |

---

## 11.4 Key Takeaways

- Distributed systems fail partially, so every call needs a timeout, a retry policy and an idempotent handler.
- Quorums (R + W > N) trade latency and availability for consistency; choose them per use case.
- Events decouple services but move complexity into schemas, ordering, duplicates and observability.
- Choreography suits small stable flows; orchestration suits long business processes you must monitor.

## 11.5 Sample Interview Questions

- What does R + W > N guarantee, and what does it not?
- Why can a network partition not be told apart from a slow node?
- Choreography or orchestration for an order-fulfilment flow, and why?
- How do you make an event consumer safe against duplicates?
- What problem does an outbox solve?

## 11.6 Further Reading

- Martin Kleppmann, *Designing Data-Intensive Applications* (chapters on replication, partitioning and consistency)
- Peter Deutsch and others, *The Eight Fallacies of Distributed Computing*
- Chris Richardson, *Microservices Patterns* (sagas and the outbox)

---

**Next Up:** [Chapter 12 — Cloud Design Patterns →](./12%20-%20Cloud%20Design%20Patterns.md)
