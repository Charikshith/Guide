# Chapter 58 — Observability: Logs, Metrics, Traces & OpenTelemetry

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 57 — CI/CD & GitHub Actions](ch57-ci-cd-and-github-actions.md) · Next → [Chapter 59 — Cost Awareness in the Cloud](ch59-cost-awareness-in-the-cloud.md)

---

## Concept

The three pillars, instrumentation, and OpenTelemetry as the standard for collecting them.

**In one sentence:** metrics tell you *that* something is wrong, traces tell you *where* in a chain of services it's wrong, logs tell you *why* — and OpenTelemetry is the vendor-neutral standard for producing all three with shared IDs so you can jump between them.

**Mental model — a hospital patient.** Metrics are the vital-signs monitor: heart rate and temperature over time, cheap to record, great for alarms. A trace is the patient's journey through the hospital: reception → triage → X-ray → surgery, with the time spent at each step. Logs are the doctors' detailed notes at each step. The patient ID wristband (trace ID) links all three.

**The three signals**

| | Metrics | Traces | Logs |
|-|---------|--------|------|
| Is | numbers aggregated over time | a tree of timed *spans* for one request across services | timestamped events with fields |
| Answers | "is it broken? how much? trending?" | "where did this request spend its time? which service failed?" | "what exactly happened here?" |
| Cost | cheap (fixed size per series) | medium (usually sampled) | expensive at volume |
| Cardinality | must be **low** (no user IDs as labels!) | high is fine (attributes per span) | high is fine |
| Tools | Prometheus, Grafana Mimir, Datadog | Jaeger, Tempo, Zipkin, Honeycomb | Loki, Elasticsearch, CloudWatch |

**Metric types**

| Type | Example | Query |
|------|---------|-------|
| Counter (only goes up) | `http_requests_total{route,status}` | `rate(http_requests_total[5m])` |
| Gauge (up and down) | `queue_depth`, `memory_bytes` | the current value |
| Histogram (bucketed distribution) | `http_request_duration_seconds` | `histogram_quantile(0.99, …)` → p99 |

**Golden signals / RED / USE**

| Method | For | Measure |
|--------|-----|---------|
| **RED** | request-driven services | **R**ate, **E**rrors, **D**uration |
| **USE** | resources (CPU, disk, pools) | **U**tilization, **S**aturation, **E**rrors |
| Four golden signals (Google SRE) | any user-facing service | latency, traffic, errors, saturation |

**Traces** — a *trace* is one request; a *span* is one operation within it (an HTTP call, a DB query) with a start, a duration, attributes, and a parent. Context is propagated between services in the W3C `traceparent` header: `00-<trace_id>-<span_id>-01`.

**What OpenTelemetry standardizes**

| Piece | Role |
|-------|------|
| API + SDKs (every major language) | create spans, metrics, and logs in code |
| Semantic conventions | standard attribute names: `http.request.method`, `db.system`, `service.name` |
| Context propagation | `traceparent` / baggage across HTTP, gRPC, and queues |
| Auto-instrumentation | patch popular libraries (FastAPI, requests, psycopg, Django) with no code changes |
| **OTLP** | one wire protocol for all signals |
| **Collector** | receive → process (batch, sample, redact, enrich) → export to any backend |

OTel standardizes *collection*, not storage or UI — you can switch vendors without re-instrumenting.

**Alert on symptoms, not causes** — page on what users feel (error rate, latency SLO burn), not on "CPU at 80%". Use causes (CPU, GC, queue depth) on dashboards for diagnosis.

---

## Prereqs

* [Chapter 24 — Logging](ch24-logging.md)

---

## Diagram

**App emitting logs/metrics/traces → collector → backends**

```mermaid
flowchart LR
    subgraph Services
      A["checkout (OTel SDK)"]
      B["payments (OTel SDK)"]
      C["inventory (auto-instrumented)"]
    end
    A & B & C -->|OTLP| COL["OTel Collector<br/>batch · tail sampling ·<br/>redact PII · add k8s attrs"]
    COL -->|metrics| PROM[("Prometheus / Mimir")]
    COL -->|traces| TEMPO[("Tempo / Jaeger")]
    COL -->|logs| LOKI[("Loki / ES")]
    PROM & TEMPO & LOKI --> GRAF["Grafana:<br/>metric → exemplar → trace → logs"]
    PROM --> AM["Alertmanager → on-call"]
```

**One trace across services**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" role="img" aria-label="Trace waterfall: checkout takes 812 ms, of which payments 701 ms and the provider charge call 672 ms is the root cause" style="width:100%;max-width:820px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="20" y="24" font-size="13" text-anchor="start" fill="var(--text)" font-weight="600">trace 4bf92f3577b34da6a3ce929d0e0e4736</text><text x="800" y="24" font-size="13" text-anchor="end" fill="var(--text-muted)">total 812 ms</text><text x="20" y="61" font-size="12" text-anchor="start" fill="var(--text)">checkout   POST /checkout</text><rect x="330.0" y="48" width="380.0" height="20" rx="3" fill="var(--primary)" fill-opacity=".45" stroke="var(--primary)" stroke-width="1"/><text x="722" y="62" font-size="12" text-anchor="start" fill="var(--text-muted)">812 ms</text><text x="40" y="97" font-size="12" text-anchor="start" fill="var(--text)">inventory   GET /reserve</text><rect x="330.0" y="84" width="29.950738916256157" height="20" rx="3" fill="var(--success)" fill-opacity=".45" stroke="var(--success)" stroke-width="1"/><text x="722" y="98" font-size="12" text-anchor="start" fill="var(--text-muted)">64 ms</text><text x="40" y="133" font-size="12" text-anchor="start" fill="var(--text)">payments   POST /charge</text><rect x="359.95073891625617" y="120" width="328.0541871921182" height="20" rx="3" fill="var(--danger)" fill-opacity=".45" stroke="var(--danger)" stroke-width="1"/><text x="722" y="134" font-size="12" text-anchor="start" fill="var(--danger)" font-weight="600">701 ms   ← slow</text><text x="60" y="169" font-size="12" text-anchor="start" fill="var(--text)">db   SELECT … FROM cards</text><rect x="362.7586206896552" y="156" width="4.211822660098522" height="20" rx="3" fill="#8b5cf6" fill-opacity=".45" stroke="#8b5cf6" stroke-width="1"/><text x="722" y="170" font-size="12" text-anchor="start" fill="var(--text-muted)">9 ms</text><text x="60" y="205" font-size="12" text-anchor="start" fill="var(--text)">http   POST provider.com/v1/charges</text><rect x="372.1182266009852" y="192" width="314.48275862068965" height="20" rx="3" fill="var(--danger)" fill-opacity=".45" stroke="var(--danger)" stroke-width="1"/><text x="722" y="206" font-size="12" text-anchor="start" fill="var(--danger)" font-weight="600">672 ms   ← root cause</text><text x="40" y="241" font-size="12" text-anchor="start" fill="var(--text)">db   INSERT INTO orders</text><rect x="704.8522167487686" y="228" width="5.147783251231528" height="20" rx="3" fill="#8b5cf6" fill-opacity=".45" stroke="#8b5cf6" stroke-width="1"/><text x="722" y="242" font-size="12" text-anchor="start" fill="var(--text-muted)">11 ms</text><text x="20" y="278" font-size="12.5" text-anchor="start" fill="var(--text-muted)">logs with trace_id=4bf92f… show: "provider latency spike, retry 1/3"</text></svg>
</div>

**From an alert to a root cause**

```mermaid
flowchart LR
    AL["🔔 alert: p99 checkout > 500 ms<br/>(metric)"] --> DB["dashboard: only /checkout,<br/>only the payments dependency"] --> EX["click an exemplar<br/>→ a slow trace"] --> SP["span: provider call 672 ms"] --> LG["logs for that trace_id:<br/>'retry 1/3, 429 from provider'"]
```

---

## Example

```python
# Auto + manual instrumentation with OpenTelemetry (Python)
# pip install opentelemetry-distro opentelemetry-exporter-otlp
# opentelemetry-bootstrap -a install
# run: OTEL_SERVICE_NAME=checkout opentelemetry-instrument uvicorn app:app
from opentelemetry import trace, metrics

tracer = trace.get_tracer("checkout")
meter = metrics.get_meter("checkout")
orders = meter.create_counter("orders_total", description="orders placed")
latency = meter.create_histogram("checkout_duration_seconds", unit="s")

def checkout(cart):
    with tracer.start_as_current_span("checkout") as span:
        span.set_attribute("cart.items", len(cart.items))       # high cardinality is OK on spans
        with tracer.start_as_current_span("reserve_inventory"):
            reserve(cart)
        with tracer.start_as_current_span("charge") as s:
            try:
                charge(cart)
            except PaymentError as e:
                s.record_exception(e)
                s.set_status(trace.Status(trace.StatusCode.ERROR))
                raise
        orders.add(1, {"payment_method": cart.method})          # LOW cardinality labels only
```

```python
# Prometheus client directly
from prometheus_client import Counter, Histogram, start_http_server
REQS = Counter("http_requests_total", "requests", ["route", "status"])
DUR = Histogram("http_request_duration_seconds", "latency", ["route"],
                buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5])
start_http_server(9100)                                          # scrape target: /metrics
with DUR.labels("/checkout").time():
    ...
REQS.labels("/checkout", "200").inc()
```

```promql
# Error ratio over 5 minutes
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
# p99 latency per route
histogram_quantile(0.99, sum by (le, route) (rate(http_request_duration_seconds_bucket[5m])))
```

---

## Exercises

1. Instrument a service with metrics + traces.

   <details><summary>Solution</summary>Run it under <code>opentelemetry-instrument</code> for automatic HTTP and DB spans; add manual spans around business steps; expose RED metrics (a request counter by route and status, a latency histogram); export via OTLP to a local Collector feeding Jaeger and Prometheus (a docker-compose file). Check a trace in Jaeger and a p99 panel in Grafana.</details>

2. Correlate a slow request across services via trace ID.

   <details><summary>Solution</summary>Make sure both services propagate <code>traceparent</code> (auto-instrumented HTTP clients do). Include <code>trace_id</code> in every log line (the OTel logging integration or a log formatter). Find a slow trace in Jaeger, then search logs for its <code>trace_id</code>. Enable exemplars so latency histograms link straight to example traces.</details>

3. Why is `http_requests_total{user_id="…"}` a bad metric?

   <details><summary>Solution</summary>Each distinct label combination creates a new time series. Millions of users create millions of series (cardinality explosion) and overload the metrics database. Put <code>user_id</code> on spans or logs instead, and keep metric labels bounded (route, status class, method).</details>

---

## Mini project

**Add OpenTelemetry to a service and view a trace across two services.**

```mermaid
flowchart LR
    U["k6 load"] --> F["frontend-api (FastAPI)"] -->|"HTTP + traceparent"| B["pricing-svc (FastAPI)"] --> R[("Redis")]
    F & B -->|OTLP| C["otel-collector"]
    C --> J["Jaeger"]
    C --> P["Prometheus"] --> G["Grafana<br/>RED dashboard + alert rule"]
    C --> L["Loki (logs with trace_id)"]
```

**Steps**

1. Two small services; one calls the other, and the second uses Redis.
2. docker-compose with the Collector, Jaeger, Prometheus, Grafana, and Loki.
3. Auto-instrument both; add one manual span and one business metric each; add `trace_id` to logs.
4. Inject latency (a random 500 ms sleep in 5% of pricing calls) and find it through dashboard → trace → logs.
5. An alert rule: p99 > 300 ms for 5 minutes, or an error ratio > 2%.
6. Tail sampling in the Collector: keep 100% of error and slow traces, and 10% of the rest.

**Done when:** starting from the alert, you reach the exact slow span and its log lines in under a minute.

---

## Open source

* [`open-telemetry/opentelemetry-python`](https://github.com/open-telemetry/opentelemetry-python) — the SDK; the `opentelemetry-python-contrib` repo holds the auto-instrumentations; `opentelemetry-collector-contrib` has the processors and exporters.
* [`prometheus/prometheus`](https://github.com/prometheus/prometheus) — a pull-based metrics database with PromQL; read the "Instrumentation" and "Histograms and summaries" docs pages.

---

## Interview

1. **"Logs vs metrics vs traces?"**
   <details><summary>Answer</summary>Metrics are cheap aggregated numbers over time: best for dashboards, trends, and alerting, but no per-request detail and labels must stay low-cardinality. Traces show one request's path and timing across services: best for finding which hop is slow or failing; usually sampled. Logs are detailed discrete events: best for the exact why, but expensive at volume. Link them with trace IDs and exemplars.</details>

2. **"What does OTel standardize?"**
   <details><summary>Answer</summary>The APIs and SDKs to produce traces, metrics, and logs; semantic conventions for attribute names; context propagation (W3C Trace Context and baggage); the OTLP wire protocol; and the Collector for processing and routing. It deliberately doesn't standardize storage or UI, so you instrument once and choose or switch backends freely.</details>

---

## Checklist

- [ ] emit all three signals
- [ ] correlate via trace IDs
- [ ] alert on real symptoms

---

> [Contents](index.md) · ← [Chapter 57 — CI/CD & GitHub Actions](ch57-ci-cd-and-github-actions.md) · Next → [Chapter 59 — Cost Awareness in the Cloud](ch59-cost-awareness-in-the-cloud.md)
