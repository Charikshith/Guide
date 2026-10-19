# Chapter 10 — Service Mesh & Service Discovery

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 9 — Message Queues & Streaming (Kafka, SQS, Pub/Sub)](ch09-message-queues-and-streaming-kafka-sqs-pub.md) · Next → [Chapter 11 — Database Scaling](ch11-database-scaling.md)

---

## Concept

Sidecars, discovery, mTLS, retries/timeouts/circuit breaking at the mesh layer; when a mesh earns its cost.

**In one sentence:** service discovery answers "where are the healthy instances of service X right now?", and a service mesh moves the networking plumbing every service needs — encryption, identity, retries, timeouts, circuit breaking, metrics — out of application code into a proxy next to each service, configured centrally.

**Read the full explanation in the AI Library** (it is explained there once, so this chapter does not repeat it):

* [Chapter 2 — Service Mesh and Service Discovery](https://charikshith.github.io/AI_Library/notes/system-design/chapters/2%20-%20Networking%20%26%20Communication.html#210-service-mesh-and-service-discovery)

This chapter is the **practice layer**: the diagram, worked example, exercises, mini-project, design prompt, open-source reading, interview questions and checklist below.

---

## Prereqs

* [Chapter 6 — Load Balancing](ch06-load-balancing.md)
* [Vol 3 Ch 14 — Resilience Patterns (Idempotency, Retries, Backoff, Circuit Breakers)](../volume-3-low-level-design/ch14-resilience-patterns-idempotency-retries-backoff-circuit-breakers.md)

---

## Diagram

**A service mesh with sidecars intercepting traffic**

```mermaid
flowchart LR
    subgraph PodA["pod: orders"]
      A["orders app"] -->|"plaintext localhost"| SA["sidecar proxy"]
    end
    subgraph PodB["pod: payments"]
      SB["sidecar proxy"] -->|"plaintext localhost"| B["payments app"]
    end
    SA ==>|"mTLS<br/>identity: sa/orders<br/>retries, timeout 2 s"| SB
    CP["control plane<br/>(config, certificates, endpoints)"] -.->|xDS| SA & SB
    SA & SB -.->|"metrics, traces"| OBS["telemetry backend"]
```

**A discovery registry**

```mermaid
sequenceDiagram
    participant P as payments instance (new)
    participant R as Registry / K8s endpoints
    participant O as orders sidecar
    P->>R: register 10.1.4.7:8080 (ready)
    R-->>O: endpoints update: payments = [10.1.4.5, 10.1.4.6, 10.1.4.7]
    O->>P: route requests (P2C across the healthy set)
    Note over P,R: missed heartbeats / failed readiness
    R-->>O: remove 10.1.4.7
```

**Retries at the mesh layer need budgets**

```
 without budgets: A → B → C, each layer retries 3×  → one failing call at C = 3 × 3 = 9+ calls
 with a retry budget (e.g. retries ≤ 20% of requests) and retries only at one layer → bounded load
```

---

## Example

```yaml
# Istio: strict mTLS in the namespace
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: { name: default, namespace: shop }
spec: { mtls: { mode: STRICT } }
---
# Only 'orders' may POST to payments' /charge
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: { name: payments-allow-orders, namespace: shop }
spec:
  selector: { matchLabels: { app: payments } }
  rules:
    - from: [{ source: { principals: ["cluster.local/ns/shop/sa/orders"] } }]
      to:   [{ operation: { methods: ["POST"], paths: ["/charge"] } }]
---
# Timeouts + retries per route
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: { name: payments, namespace: shop }
spec:
  hosts: [payments]
  http:
    - timeout: 2s
      retries: { attempts: 2, perTryTimeout: 800ms, retryOn: "5xx,reset,connect-failure" }
      route: [{ destination: { host: payments } }]
---
# Circuit breaking + outlier detection
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata: { name: payments, namespace: shop }
spec:
  host: payments
  trafficPolicy:
    connectionPool: { http: { http1MaxPendingRequests: 100, maxRequestsPerConnection: 100 } }
    outlierDetection: { consecutive5xxErrors: 5, interval: 10s, baseEjectionTime: 30s, maxEjectionPercent: 50 }
```

```bash
linkerd install --crds | kubectl apply -f - && linkerd install | kubectl apply -f -
kubectl annotate ns shop linkerd.io/inject=enabled      # sidecars injected on the next rollout
linkerd viz stat deploy -n shop                         # success rate, RPS, p50/p95/p99 per service
```

---

## Exercises

1. Explain how mTLS works in a mesh.

   <details><summary>Solution</summary>The mesh CA issues each workload a short-lived certificate encoding its identity (SPIFFE ID derived from the service account). Apps send plaintext to the local sidecar; sidecars establish mutual TLS, each verifying the other's certificate chain against the mesh CA; the server side checks authorization policies against the caller's identity. Certificates rotate automatically, so no one handles keys by hand, and the network itself is no longer trusted (zero trust).</details>

2. Configure retries/timeouts at the mesh layer.

   <details><summary>Solution</summary>See the VirtualService: an overall timeout of 2 s, 2 attempts with an 800 ms per-try timeout, retrying only on 5xx, resets, and connect failures — only for idempotent routes. Remove retries from application code (or the mesh) so they don't multiply, and add a retry budget. Verify with fault injection (<code>fault.abort</code> 20% of requests) that callers still succeed.</details>

3. Why can retries at several layers turn a small outage into a big one?

   <details><summary>Solution</summary>Retries multiply: 3 retries at each of 3 layers means up to 27 attempts reaching the deepest service for one user request, exactly when it is struggling. Retry at one layer, use budgets, add jittered backoff, and let circuit breakers stop the flood.</details>

---

## Mini project

**A toy sidecar that adds a timeout + retry to a service.**

```mermaid
flowchart LR
    APP["client app<br/>(calls localhost:15001)"] --> SC["your sidecar (asyncio proxy)<br/>timeout · retries with jitter ·<br/>circuit breaker · metrics"]
    SC --> DISC["discovery: reads endpoints<br/>from a registry file / Consul"]
    SC --> UP1["upstream instance 1"] & UP2["upstream instance 2 (flaky)"]
    SC --> MET["/metrics: requests, retries,<br/>open circuits, latency histogram"]
```

**Steps**

1. An HTTP proxy listening on localhost that forwards to an upstream picked from a registry (a JSON file you edit, or Consul).
2. Per-try timeout, total timeout, and up to 2 retries with jittered backoff for GET only.
3. A circuit breaker per upstream instance (open after 5 consecutive failures, half-open after 10 s).
4. Prometheus metrics for requests, retries, ejected endpoints, and latency.
5. Make one upstream flaky and slow; show the client's success rate with and without the sidecar.

**Done when:** the client's code is unchanged, and the sidecar alone raises its success rate from ~80% to >99% against a flaky upstream.

---

## Design

**Design service discovery + resilience for a microservice fleet.**

Scope: 60 services, 3 languages, 2,000 pods across 3 zones, 50k internal RPS; compliance requires encryption and identity on every internal call.

```mermaid
flowchart TB
    subgraph K8s["Kubernetes cluster (3 zones)"]
      CP["mesh control plane (HA, 3 replicas)<br/>CA · config · endpoint discovery"]
      subgraph NS1["namespace: checkout"]
        S1["orders + proxy"] --> S2["payments + proxy"]
      end
      subgraph NS2["namespace: catalog"]
        S3["search + proxy"] --> S4["inventory + proxy"]
      end
      S1 --> S4
      CP -.-> S1 & S2 & S3 & S4
    end
    GW["ingress gateway (mTLS inside)"] --> S1 & S3
    OBS["metrics · traces · access logs"] -.- S1 & S2 & S3 & S4
```

**Capacity:** ~0.5–1 ms added latency per hop and ~50–100 MB RAM plus ~0.1–0.2 vCPU per sidecar at this traffic: 2,000 pods × 75 MB ≈ 150 GB RAM and ~300 vCPU for proxies — a real cost to compare against building the same features into three language libraries. Ambient or node-level proxies cut this substantially.

**Decisions to justify**

* **Kubernetes DNS + mesh xDS** for discovery; no separate registry to operate.
* **A mesh (Linkerd for simplicity, or Istio for richer policy)** because of 60 services in 3 languages plus a mandatory mTLS requirement; one team owns it.
* **STRICT mTLS + default-deny authorization**, allow-listing call paths by service identity.
* **Timeouts on every route; retries only for idempotent routes, only at the mesh, with budgets;** outlier detection and connection limits for circuit breaking.
* **Progressive delivery** via mesh traffic splitting; fault-injection drills per quarter.

---

## Open source

* [`linkerd/linkerd2`](https://github.com/linkerd/linkerd2) — a lightweight mesh with a Rust micro-proxy; automatic mTLS with nearly zero config.
* [`istio/istio`](https://github.com/istio/istio) — an Envoy-based mesh with rich traffic and security policy, and a sidecarless "ambient" mode. See also SPIFFE/SPIRE for workload identity.

---

## Interview

1. **"What does a service mesh give you?"**
   <details><summary>Answer</summary>Consistent, language-independent networking features without app code changes: mutual TLS and workload identity, service-to-service authorization, timeouts, retries, circuit breaking, load balancing, traffic shifting for canaries, fault injection, and uniform metrics and traces for every hop — all configured centrally by the control plane.</details>

2. **"Sidecar pros/cons?"**
   <details><summary>Answer</summary>Pros: transparent to the app, works for any language, isolates networking logic, and upgrades independently of the service. Cons: an extra proxy hop per call (latency), CPU and memory per pod (multiplied across the fleet), startup and shutdown ordering issues, more moving parts to debug and upgrade. Node-level or sidecarless designs (ambient, eBPF) trade some isolation for lower overhead.</details>

---

## Checklist

- [ ] standardize mTLS
- [ ] centralize retries/timeouts
- [ ] know when *not* to use a mesh

---

> [Contents](index.md) · ← [Chapter 9 — Message Queues & Streaming (Kafka, SQS, Pub/Sub)](ch09-message-queues-and-streaming-kafka-sqs-pub.md) · Next → [Chapter 11 — Database Scaling](ch11-database-scaling.md)
