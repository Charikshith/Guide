# Chapter 16 — Observability: Logs, Metrics & Traces

> **Volume 2 — Software Engineering** · [Contents](index.md) · ← [Chapter 15 — Documentation as a System](ch15-documentation-as-a-system.md) · Next → [Chapter 17 — Incident Response & Postmortems](ch17-incident-response-and-postmortems.md)

---

## Concept

The three pillars, instrumentation, dashboards, SLOs/SLIs, and debugging with traces.

**In one sentence:** observability is being able to answer new questions about your running system without shipping new code — and at team scale that means agreeing on what "working" means (SLIs and SLOs), alerting only when users are actually hurt (error-budget burn), and building dashboards and traces that lead from a symptom to a cause in minutes.

**Mental model — a car's dashboard and a mechanic's toolkit.** The speedometer and fuel gauge (SLIs) tell you what you care about while driving. The "check engine" light should come on only when something needs attention (SLO-based alerts), not every time you brake. When it does come on, the mechanic plugs in a diagnostic tool (traces, logs) to find the exact failing part.

The mechanics of emitting the three signals with OpenTelemetry are in [Vol 1 Ch 58](../volume-1-cs-foundations/ch58-observability-logs-metrics-traces-and-opentelemetry.md). This chapter is about **using** them: SLOs, dashboards, alerting, and debugging practice.

**SLI, SLO, SLA, error budget**

| Term | Meaning | Example |
|------|---------|---------|
| **SLI** (indicator) | a measured ratio of good events to all events | `good requests / all requests`, where good = status < 500 AND latency < 300 ms |
| **SLO** (objective) | the target for an SLI over a window | 99.9% of checkout requests are good over 30 days |
| **Error budget** | `1 − SLO` — how much failure is allowed | 0.1% of requests ≈ 43 minutes of full outage per 30 days |
| **SLA** (agreement) | a contract with customers, with penalties | 99.5% monthly, or service credits — always *looser* than the SLO |

**How many nines?**

| SLO | Allowed downtime per 30 days |
|-----|-----------------------------:|
| 99% | 7 h 12 min |
| 99.5% | 3 h 36 min |
| 99.9% | 43 min 12 s |
| 99.95% | 21 min 36 s |
| 99.99% | 4 min 19 s |

Each extra nine costs a lot more engineering. Choose the SLO from what users need, not from pride.

**Error budget policy** — if the budget is healthy, ship faster and take risks; if it's burning fast, freeze risky changes and prioritize reliability work. This turns "reliability vs features" arguments into a number.

**Alert on burn rate, not on every blip** — *burn rate* = how fast you consume the budget (1× = exactly on budget over the window). Multi-window, multi-burn-rate alerts (Google SRE Workbook):

| Severity | Burn rate | Long window | Short window | Budget spent when it fires |
|----------|:-:|:-:|:-:|:-:|
| Page | 14.4× | 1 h | 5 min | 2% |
| Page | 6× | 6 h | 30 min | 5% |
| Ticket | 1× | 3 days | 6 h | 10% |

The short window makes the alert stop quickly once the problem is fixed.

**Dashboards that work**

| Dashboard | For | Contents |
|-----------|-----|----------|
| Service overview (RED) | "is my service OK?" | request **R**ate, **E**rror ratio, **D**uration p50/p95/p99, per route; SLO and budget remaining |
| Resources (USE) | "is it saturated?" | **U**tilization, **S**aturation (queues, pool waits), **E**rrors for CPU, memory, DB pool, disk |
| Dependencies | "is it them?" | latency and errors per downstream call |
| Business | "are users succeeding?" | orders per minute, sign-ups, payment success |

Put SLO status at the top, show deploys as annotations, and keep the same layout for every service.

**Debugging with traces** — start from the symptom (an SLO alert or a slow p99), use an *exemplar* to jump from the latency histogram to a real slow trace, find the span that dominates (critical path), then read that span's logs via the trace ID. Compare slow traces with normal ones: what attribute is different (a tenant, a region, a payload size, a cache miss)?

---

## Prereqs

* [Vol 1 Ch 24 — Logging](../volume-1-cs-foundations/ch24-logging.md)

---

## Diagram

**A trace spanning services with spans**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 280" role="img" aria-label="Trace waterfall: the provider API call at 465 ms is the critical path inside payments, inside a 640 ms checkout" style="width:100%;max-width:840px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="20" y="22" font-size="13" text-anchor="start" fill="var(--text)" font-weight="600">trace 7f3a… POST /checkout</text><text x="820" y="22" font-size="12.5" text-anchor="end" fill="var(--text-muted)">0 ms ────── 640 ms</text><text x="20" y="57" font-size="12" text-anchor="start" fill="var(--text)">gateway   POST /checkout</text><rect x="360.0" y="44" width="360.0" height="20" rx="3" fill="var(--primary)" fill-opacity=".45" stroke="var(--primary)" stroke-width="1"/><text x="732" y="58" font-size="12" text-anchor="start" fill="var(--text-muted)">640 ms</text><text x="38" y="93" font-size="12" text-anchor="start" fill="var(--text)">orders   create_order</text><rect x="371.25" y="80" width="342.0" height="20" rx="3" fill="var(--primary)" fill-opacity=".45" stroke="var(--primary)" stroke-width="1"/><text x="732" y="94" font-size="12" text-anchor="start" fill="var(--text-muted)">608 ms</text><text x="56" y="129" font-size="12" text-anchor="start" fill="var(--text)">orders   SELECT cart (db)</text><rect x="372.375" y="116" width="11.25" height="20" rx="3" fill="#8b5cf6" fill-opacity=".45" stroke="#8b5cf6" stroke-width="1"/><text x="732" y="130" font-size="12" text-anchor="start" fill="var(--text-muted)">20 ms</text><text x="56" y="165" font-size="12" text-anchor="start" fill="var(--text)">payments   POST /charge</text><rect x="399.375" y="152" width="281.25" height="20" rx="3" fill="var(--danger)" fill-opacity=".45" stroke="var(--danger)" stroke-width="1"/><text x="732" y="166" font-size="12" text-anchor="start" fill="var(--text-muted)">500 ms</text><text x="74" y="201" font-size="12" text-anchor="start" fill="var(--text)">payments   provider API call</text><rect x="416.25" y="188" width="261.5625" height="20" rx="3" fill="var(--danger)" fill-opacity=".45" stroke="var(--danger)" stroke-width="1"/><text x="732" y="202" font-size="12" text-anchor="start" fill="var(--danger)" font-weight="600">465 ms   ← critical path</text><text x="56" y="237" font-size="12" text-anchor="start" fill="var(--text)">inventory   reserve stock</text><rect x="691.875" y="224" width="22.5" height="20" rx="3" fill="var(--success)" fill-opacity=".45" stroke="var(--success)" stroke-width="1"/><text x="732" y="238" font-size="12" text-anchor="start" fill="var(--text-muted)">40 ms</text></svg>
</div>

The critical path is `payments → provider API call` (465 ms of 640 ms).

**A RED/USE dashboard layout**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 360" role="img" aria-label="Service dashboard for checkout-api: SLO budget, request rate, errors, latency, resource USE metrics and dependency latency" style="width:100%;max-width:820px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><rect x="10" y="10" width="800" height="340" rx="10" fill="var(--border)" fill-opacity=".15" stroke="var(--border)" stroke-width="1.4"/><text x="30" y="36" font-size="14" text-anchor="start" fill="var(--text)" font-weight="700">checkout-api</text><text x="30" y="62" font-size="12.5" text-anchor="start" fill="var(--text)">SLO 99.9% good (30d)    current 99.93%    budget left</text><rect x="380" y="50" width="200" height="16" rx="4" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1"/><rect x="380" y="50" width="142" height="16" rx="4" fill="var(--success)" fill-opacity=".7" stroke="var(--success)" stroke-width="0"/><text x="592" y="63" font-size="12.5" text-anchor="start" fill="var(--success)" font-weight="700">71%</text><rect x="30.0" y="148" width="20.0" height="12" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="53.0" y="142" width="20.0" height="18" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="76.0" y="130" width="20.0" height="30" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="99.0" y="124" width="20.0" height="36" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="122.0" y="124" width="20.0" height="36" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="145.0" y="130" width="20.0" height="30" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="168.0" y="124" width="20.0" height="36" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="191.0" y="118" width="20.0" height="42" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="214.0" y="124" width="20.0" height="36" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><rect x="237.0" y="130" width="20.0" height="30" rx="1" fill="var(--primary)" fill-opacity=".6" stroke="var(--primary)" stroke-width="0"/><text x="30" y="102" font-size="12.5" text-anchor="start" fill="var(--text)" font-weight="600">Rate (rps)</text><text x="122.0" y="176" font-size="11.5" text-anchor="start" fill="var(--danger)" font-weight="600">▲ deploy</text><rect x="300.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="323.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="346.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="369.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="392.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="415.0" y="124" width="20.0" height="36" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="438.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="461.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="484.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><rect x="507.0" y="154" width="20.0" height="6" rx="1" fill="var(--danger)" fill-opacity=".6" stroke="var(--danger)" stroke-width="0"/><text x="300" y="102" font-size="12.5" text-anchor="start" fill="var(--text)" font-weight="600">Errors (%)</text><text x="415.0" y="176" font-size="11.5" text-anchor="start" fill="var(--danger)" font-weight="600">▲ spike</text><rect x="570.0" y="154" width="22.555555555555557" height="6" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="595.5555555555555" y="154" width="22.555555555555557" height="6" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="621.1111111111111" y="154" width="22.555555555555557" height="6" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="646.6666666666666" y="148" width="22.555555555555557" height="12" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="672.2222222222222" y="148" width="22.555555555555557" height="12" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="697.7777777777778" y="130" width="22.555555555555557" height="30" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="723.3333333333334" y="148" width="22.555555555555557" height="12" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="748.8888888888889" y="148" width="22.555555555555557" height="12" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><rect x="774.4444444444445" y="148" width="22.555555555555557" height="12" rx="1" fill="var(--accent)" fill-opacity=".6" stroke="var(--accent)" stroke-width="0"/><text x="570" y="102" font-size="12.5" text-anchor="start" fill="var(--text)" font-weight="600">Duration p50 / p95 / p99  (p99 shown)</text><line x1="20" y1="196" x2="800" y2="196" stroke="var(--border)" stroke-width="1"/><text x="30" y="224" font-size="12.5" text-anchor="start" fill="var(--text)">USE:  CPU 45%  ·  memory 60%  ·  DB pool waits ▁▁▅▁  ·  queue depth ▁▁▂▁</text><line x1="20" y1="244" x2="800" y2="244" stroke="var(--border)" stroke-width="1"/><text x="30" y="272" font-size="12.5" text-anchor="start" fill="var(--text)">Dependencies:  payments p99 ▁▁▇▁  ·  inventory p99 ▁▁▁▁  ·  redis ▁▁▁▁</text></svg>
</div>

**Error budget over a 30-day window**

```mermaid
xychart-beta
    title "Error budget remaining (%)"
    x-axis ["d1", "d5", "d10", "d12", "d15", "d20", "d25", "d30"]
    y-axis "%" 0 --> 100
    line [100, 96, 91, 62, 58, 52, 47, 44]
```

The drop on day 12 is an incident. After it, the team slows risky releases until the budget recovers.

---

## Example

```yaml
# Prometheus recording + alerting rules for a 99.9% availability SLO
groups:
  - name: checkout-slo
    rules:
      - record: sli:checkout_errors:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{route="/checkout",status=~"5.."}[5m]))
          / sum(rate(http_requests_total{route="/checkout"}[5m]))
      - record: sli:checkout_errors:ratio_rate1h
        expr: |
          sum(rate(http_requests_total{route="/checkout",status=~"5.."}[1h]))
          / sum(rate(http_requests_total{route="/checkout"}[1h]))

      - alert: CheckoutErrorBudgetFastBurn
        expr: |
          sli:checkout_errors:ratio_rate1h > (14.4 * 0.001)
          and
          sli:checkout_errors:ratio_rate5m > (14.4 * 0.001)
        labels: { severity: page }
        annotations:
          summary: "Checkout is burning its 30-day error budget 14x too fast"
          runbook_url: https://docs.acme.dev/runbooks/checkout/#fast-burn
```

```python
# Error-budget math you should be able to do on a whiteboard
slo = 0.999
window_min = 30 * 24 * 60
budget_min = (1 - slo) * window_min
print(round(budget_min, 1))                 # 43.2 minutes of full outage allowed

burn_rate = 14.4
print(round(window_min / burn_rate / 60, 1))   # 50.0 hours to exhaust the whole budget at 14.4x
print(round(burn_rate * 60 / window_min * 100, 1))   # 2.0 % of the budget spent in 1 hour
```

```python
# Latency SLI with an exemplar link to traces (prometheus_client)
from prometheus_client import Histogram
from opentelemetry import trace
LAT = Histogram("http_request_duration_seconds", "latency", ["route"],
                buckets=[0.05, 0.1, 0.2, 0.3, 0.5, 1, 2])

def observe(route, seconds):
    ctx = trace.get_current_span().get_span_context()
    LAT.labels(route).observe(seconds, exemplar={"trace_id": format(ctx.trace_id, "032x")})
```

---

## Exercises

1. Instrument a service with metrics + traces.

   <details><summary>Solution</summary>Auto-instrument HTTP and DB with OpenTelemetry; expose RED metrics per route (a counter by status class, a latency histogram with buckets around your SLO threshold); add manual spans for key business steps; put <code>trace_id</code> in logs; attach exemplars to the latency histogram. Build the RED dashboard with deploy annotations. See <a href="../volume-1-cs-foundations/ch58-observability-logs-metrics-traces-and-opentelemetry.md">Vol 1 Ch 58</a> for the setup.</details>

2. Define an SLO and the SLI that measures it.

   <details><summary>Solution</summary>User journey: "a customer completes checkout". SLI: the proportion of <code>POST /checkout</code> requests, measured at the load balancer, that return a non-5xx status within 800 ms. SLO: 99.9% over a rolling 30 days. Error budget: 0.1% ≈ 43 minutes equivalent. Alerting: 14.4×/6× burn-rate pages and a 1× ticket. Policy: freeze risky deploys if more than 50% of the budget is spent in the first week.</details>

3. Why is "CPU > 80% for 5 minutes" a poor page?

   <details><summary>Solution</summary>High CPU isn't user pain: the service may be fine at 80% (efficient!) or broken at 20% (deadlocked). It pages people for non-problems and misses real ones. Page on symptoms (SLO burn: errors and latency users feel); keep CPU on dashboards for diagnosis and for capacity-planning tickets.</details>

---

## Mini project

**Add OpenTelemetry to a service and produce a trace view + a latency dashboard.**

```mermaid
flowchart LR
    SVC["checkout service + 2 dependencies"] -->|OTLP| COL["OTel Collector"]
    COL --> PROM[("Prometheus")] --> GRAF["Grafana:<br/>RED + USE + SLO panels,<br/>deploy annotations"]
    COL --> TEMPO[("Tempo / Jaeger")] --> GRAF
    PROM --> RULES["recording rules (SLIs) +<br/>burn-rate alerts"] --> AM["Alertmanager → your phone"]
    CHAOS["fault injection:<br/>+300 ms, 5% errors"] --> SVC
```

**Steps**

1. Instrument the service and its dependencies; docker-compose for the Collector, Prometheus, Tempo/Jaeger, and Grafana.
2. Define one availability SLI and one latency SLI with recording rules.
3. Build the dashboard: SLO status and budget remaining on top, RED per route, USE for resources, dependency panels, deploy annotations.
4. Add multi-window burn-rate alerts with runbook links.
5. Inject faults (latency in one dependency, errors on 5% of requests) and practice: alert → dashboard → exemplar → trace → logs → cause.
6. Write down the time from alert to root cause for each drill.

**Done when:** the injected fault pages you within the expected window, and you can reach the guilty span from the alert in under 2 minutes.

---

## Open source

* [`open-telemetry/opentelemetry-python`](https://github.com/open-telemetry/opentelemetry-python) — SDK plus auto-instrumentation.
* [`prometheus/prometheus`](https://github.com/prometheus/prometheus) — recording and alerting rules. See also the Google *SRE Book* (chapters on SLOs and monitoring) and the *SRE Workbook* chapter "Alerting on SLOs"; `pyrra-dev/pyrra` and `slok/sloth` generate SLO rules for you.

---

## Interview

1. **"Logs vs metrics vs traces?"**
   <details><summary>Answer</summary>Metrics are cheap, aggregated numbers over time — best for dashboards, SLOs, and alerting, but no per-request detail and labels must stay low-cardinality. Traces follow individual requests across services with timed spans — best for finding which hop is slow or failing. Logs are detailed events — best for the exact why at a given point. In practice: alert on metrics, localize with traces, explain with logs, all joined by the trace ID.</details>

2. **"What's an SLO vs SLA?"**
   <details><summary>Answer</summary>An SLO is an internal reliability target for a user-centric indicator (e.g. 99.9% of checkouts succeed within 800 ms over 30 days); it drives alerting and the error-budget policy. An SLA is an external contract with customers that specifies consequences (credits, refunds) if a level isn't met. SLAs are set looser than SLOs, so you're alerted and act well before a contractual breach.</details>

---

## Checklist

- [ ] emit all three signals
- [ ] correlate via trace IDs
- [ ] alert on SLO burn

---

> [Contents](index.md) · ← [Chapter 15 — Documentation as a System](ch15-documentation-as-a-system.md) · Next → [Chapter 17 — Incident Response & Postmortems](ch17-incident-response-and-postmortems.md)
