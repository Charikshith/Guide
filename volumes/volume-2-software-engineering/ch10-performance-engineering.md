# Chapter 10 — Performance Engineering

> **Volume 2 — Software Engineering** · [Contents](index.md) · ← [Chapter 9 — Static Analysis & Type Safety at Scale](ch09-static-analysis-and-type-safety-at-scale.md) · Next → [Chapter 11 — Security & Threat Modeling](ch11-security-and-threat-modeling.md)

---

## Concept

Profiling-driven optimization, benchmarking, caching strategies, and avoiding premature optimization.

**In one sentence:** performance engineering is a loop — set a target, measure where time actually goes, fix the biggest real bottleneck, prove the gain with a trustworthy benchmark, and stop when the target is met.

### Mental model — a traffic jam

Widening a road that's already empty doesn't help; only the bottleneck matters. If 80% of travel time is spent at one broken traffic light, repaving the rest of the road is wasted effort. Profilers show you the broken light. Benchmarks prove the repair worked.

### The loop

```
 1. define the goal     "p99 of /search < 200 ms at 500 rps"   (not "make it faster")
 2. measure end to end  load test + traces: where is the time?  (CPU? DB? network? locks?)
 3. profile the hot path  flame graph of the slow component
 4. hypothesize + change ONE thing
 5. benchmark           before/after, repeated runs, statistics
 6. verify in production-like conditions; keep a regression benchmark in CI
 7. goal met? stop.     otherwise → 2
```

### Where time usually goes (check in this order)

| Suspect | Symptom | Typical fix |
|---------|---------|-------------|
| I/O waits: DB, network, disk | low CPU, high latency; long spans on DB/HTTP | fix N+1 queries, add indexes ([Vol 1 Ch 46](../volume-1-cs-foundations/ch46-schema-design-normalization-and-indexing.md)), batch, cache, parallelize calls, connection pools |
| Algorithmic complexity | time grows super-linearly with input size | a better algorithm or data structure (O(n²) → O(n log n); list → set) |
| Contention | throughput plateaus as you add threads; lock wait time | shard locks, reduce critical sections, lock-free or per-thread state |
| Memory / GC | GC pauses, high allocation rate, swapping | fewer allocations, object reuse, streaming instead of loading all |
| CPU hot loops | high CPU; one function dominates the flame graph | vectorize (NumPy), move to Rust/C, reduce work per item |
| Serialization | JSON encode/decode in the flame graph | faster libraries (`orjson`), binary formats, smaller payloads |

### Latency vs throughput

Latency is how long one request takes (report p50, **p95, p99**, not averages); throughput is requests per second. Queueing theory: as utilization approaches 100%, latency explodes, so leave headroom (~60–70% utilization for latency-sensitive services).

### Benchmarking with rigor

| Rule | Why |
|------|-----|
| Warm up first | JITs, caches, and connection pools distort the first runs |
| Run many iterations; report the distribution and a confidence interval | single runs are noise |
| Control the environment: same machine, CPU frequency pinned, nothing else running | noise hides small real differences |
| Benchmark realistic data sizes and distributions | a 10-element test says nothing about 10M |
| Prevent dead-code elimination (`black_box`) | the compiler may delete the work you're timing |
| Compare A/B with a statistical test | criterion and pyperf report significance |
| Keep benchmarks in CI with thresholds | catch regressions early |

### Premature optimization

Knuth's full quote: "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%." Optimization is premature when there's no measured problem, no target, and the change costs readability. It is *not* premature to choose sane data structures, avoid N+1 queries, or design for known scale.

---

## Prereqs

* [Vol 1 Ch 27 — Debugging & Profiling](../volume-1-cs-foundations/ch27-debugging-and-profiling.md)

---

## Diagram

### A flame graph pointing at the hot path

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 260" role="img" aria-label="Flame graph of handle_search: tokenize takes 48 percent because it re-tokenizes every document and compiles a regex on each call" style="width:100%;max-width:780px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><rect x="20" y="20" width="700" height="40" rx="3" fill="var(--primary)" fill-opacity=".25" stroke="var(--primary)" stroke-width="1.6"/><text x="370.0" y="45" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">handle_search (100%)</text><rect x="20" y="66" width="504.0" height="40" rx="3" fill="var(--primary)" fill-opacity=".25" stroke="var(--primary)" stroke-width="1.6"/><text x="272.0" y="91" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">rank_results (72%)</text><rect x="524.0" y="66" width="168.0" height="40" rx="3" fill="var(--success)" fill-opacity=".25" stroke="var(--success)" stroke-width="1.6"/><text x="608.0" y="91" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">fetch_docs (24%)</text><rect x="20" y="112" width="427.0" height="40" rx="3" fill="var(--primary)" fill-opacity=".25" stroke="var(--primary)" stroke-width="1.6"/><text x="233.5" y="137" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">score (61%)</text><rect x="447.0" y="112" width="62.99999999999998" height="40" rx="3" fill="var(--primary)" fill-opacity=".25" stroke="var(--primary)" stroke-width="1.6"/><text x="478.5" y="137" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">sort (9%)</text><rect x="524.0" y="112" width="153.99999999999997" height="40" rx="3" fill="var(--success)" fill-opacity=".25" stroke="var(--success)" stroke-width="1.6"/><text x="601.0" y="137" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">db.query (22%)</text><rect x="20" y="158" width="336.0" height="40" rx="3" fill="var(--danger)" fill-opacity=".45" stroke="var(--danger)" stroke-width="1.6"/><text x="188.0" y="183" font-size="12.5" text-anchor="middle" fill="var(--text)" font-weight="600">tokenize (48%)</text><text x="368.0" y="176" font-size="12.5" text-anchor="start" fill="var(--danger)" font-weight="600">← re-tokenizes every doc</text><text x="368.0" y="192" font-size="12.5" text-anchor="start" fill="var(--text-muted)">re.findall: compiled on every call</text><text x="405.00000000000006" y="235" font-size="13" text-anchor="start" fill="var(--success)" font-weight="700">fix: pre-tokenize at index time + compile the regex once</text></svg>
</div>

### A benchmark comparison chart

```mermaid
xychart-beta
    title "p99 latency of /search at 500 rps (ms)"
    x-axis ["baseline", "+ regex compiled once", "+ pre-tokenized docs", "+ DB index", "+ result cache"]
    y-axis "ms" 0 --> 900
    bar [840, 610, 260, 150, 45]
```

### Latency vs utilization (why headroom matters)

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 310" role="img" aria-label="Latency stays flat at low utilization, bends upward near 70 percent and shoots up past 90 percent" style="width:100%;max-width:700px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><line x1="70" y1="250" x2="70" y2="24" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="70" y1="250" x2="670" y2="250" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><text x="62" y="34" font-size="12.5" text-anchor="end" fill="var(--text-muted)">latency</text><text x="660" y="290" font-size="12.5" text-anchor="end" fill="var(--text-muted)">utilization</text><path d="M70.0,238.0 L75.9,237.9 L81.8,237.8 L87.7,237.7 L93.6,237.6 L99.5,237.5 L105.4,237.4 L111.3,237.3 L117.2,237.2 L123.1,237.1 L129.0,237.0 L134.9,236.9 L140.8,236.8 L146.7,236.7 L152.6,236.6 L158.5,236.5 L164.4,236.3 L170.3,236.2 L176.2,236.1 L182.1,236.0 L188.0,235.8 L193.9,235.7 L199.8,235.6 L205.7,235.4 L211.6,235.3 L217.5,235.1 L223.4,235.0 L229.3,234.8 L235.2,234.6 L241.1,234.5 L247.0,234.3 L252.9,234.1 L258.8,233.9 L264.7,233.8 L270.6,233.6 L276.5,233.4 L282.4,233.2 L288.3,233.0 L294.2,232.7 L300.1,232.5 L306.0,232.3 L311.9,232.1 L317.8,231.8 L323.7,231.6 L329.6,231.3 L335.5,231.0 L341.4,230.7 L347.3,230.5 L353.2,230.2 L359.1,229.8 L365.0,229.5 L370.9,229.2 L376.8,228.8 L382.7,228.5 L388.6,228.1 L394.5,227.7 L400.4,227.3 L406.3,226.9 L412.2,226.4 L418.1,226.0 L424.0,225.5 L429.9,225.0 L435.8,224.4 L441.7,223.9 L447.6,223.3 L453.5,222.6 L459.4,222.0 L465.3,221.3 L471.2,220.6 L477.1,219.8 L483.0,219.0 L488.9,218.1 L494.8,217.2 L500.7,216.2 L506.6,215.1 L512.5,214.0 L518.4,212.8 L524.3,211.4 L530.2,210.0 L536.1,208.5 L542.0,206.8 L547.9,205.0 L553.8,203.0 L559.7,200.8 L565.6,198.4 L571.5,195.7 L577.4,192.7 L583.3,189.3 L589.2,185.5 L595.1,181.2 L601.0,176.1 L606.9,170.3 L612.8,163.4 L618.7,155.1 L624.6,145.0 L630.5,132.4 L636.4,116.2 L642.3,94.7 L648.2,64.8 L654.1,30.0 L660.0,30.0" stroke="var(--danger)" stroke-width="2.6" fill="none"/><line x1="70.0" y1="250" x2="70.0" y2="255" stroke="var(--text-muted)" stroke-width="1"/><text x="70.0" y="270" font-size="12.5" text-anchor="middle" fill="var(--text)">0%</text><line x1="365.0" y1="250" x2="365.0" y2="255" stroke="var(--text-muted)" stroke-width="1"/><text x="365.0" y="270" font-size="12.5" text-anchor="middle" fill="var(--text)">50%</text><line x1="483.0" y1="250" x2="483.0" y2="255" stroke="var(--text-muted)" stroke-width="1"/><text x="483.0" y="270" font-size="12.5" text-anchor="middle" fill="var(--text)">70%</text><line x1="601.0" y1="250" x2="601.0" y2="255" stroke="var(--text-muted)" stroke-width="1"/><text x="601.0" y="270" font-size="12.5" text-anchor="middle" fill="var(--text)">90%</text><line x1="660.0" y1="250" x2="660.0" y2="255" stroke="var(--text-muted)" stroke-width="1"/><text x="660.0" y="270" font-size="12.5" text-anchor="middle" fill="var(--text)">100%</text><line x1="483.0" y1="250" x2="483.0" y2="120" stroke="var(--accent)" stroke-width="1.6" stroke-dasharray="4 4"/></svg>
</div>

---

## Example

```bash
# 1. Measure end to end
k6 run --vus 100 --duration 2m search.js          # p95/p99 and rps
# 2. Profile the running service (no code changes needed)
py-spy record -o flame.svg --pid $(pgrep -f uvicorn) --duration 30
perf record -g -p <pid> -- sleep 30 && perf script | stackcollapse-perf.pl | flamegraph.pl > cpu.svg
```

```python
# Before: the regex is compiled and the docs re-tokenized on every request
import re
def score(query, doc):
    words = set(re.findall(r"\w+", doc.lower()))
    return sum(w in words for w in re.findall(r"\w+", query.lower()))

# After: compile once; tokenize documents once at index time
WORD = re.compile(r"\w+")
def tokenize(s): return frozenset(WORD.findall(s.lower()))
INDEX = {doc_id: tokenize(text) for doc_id, text in corpus.items()}   # built once
def score_fast(query_tokens, doc_tokens): return len(query_tokens & doc_tokens)
```

```python
# A benchmark with statistics (pytest-benchmark, or pyperf for serious work)
def test_score_speed(benchmark):
    q = tokenize("fast red running shoes")
    result = benchmark(lambda: [score_fast(q, t) for t in INDEX.values()])
    assert result                         # prevents "optimizing away" the work
# pytest --benchmark-compare --benchmark-compare-fail=mean:10%   ← fail CI on a 10% regression
```

```rust
// criterion.rs: warm-up, many samples, confidence intervals, change detection
use criterion::{black_box, criterion_group, criterion_main, Criterion};
fn bench(c: &mut Criterion) {
    let data: Vec<u64> = (0..100_000).collect();
    c.bench_function("sum", |b| b.iter(|| black_box(&data).iter().sum::<u64>()));
}
criterion_group!(benches, bench);
criterion_main!(benches);
// output: time: [41.2 µs 41.5 µs 41.9 µs]  change: -38.1% (p = 0.00 < 0.05) Performance has improved.
```

---

## Exercises

1. Profile a slow service and optimize the real bottleneck.

   <details><summary>Solution</summary>Load test to reproduce the slowness and record p99. Look at traces first: if most time is in DB spans, it's I/O (check for N+1 queries and missing indexes). If CPU-bound, take a flame graph and look at the widest frames. Change one thing, re-measure the same way, and keep the change only if the target metric improved. Record before and after numbers in the PR.</details>

2. Write a benchmark that proves an optimization helps.

   <details><summary>Solution</summary>Use pytest-benchmark, pyperf, or criterion with realistic input sizes; warm up; run enough rounds for a tight confidence interval; compare against the saved baseline and check the change is statistically significant; guard against dead-code elimination. Commit the benchmark so CI can detect future regressions.</details>

3. A teammate proposes rewriting a service in Rust "for performance". What do you ask first?

   <details><summary>Solution</summary>What's the target and the current measurement? Where does the time go — if 90% is waiting on the database, a faster language changes almost nothing. Have cheaper fixes (queries, caching, algorithms) been tried? What does the rewrite cost in time and risk? A profile should drive the decision.</details>

---

## Mini project

**Take a naive implementation, profile it, optimize it, and document the speedup with benchmarks.**

```mermaid
flowchart TD
    N["naive log analyzer:<br/>read 1 GB, parse with regex per line,<br/>list lookups, string concat,<br/>json.loads everything"] --> BASE["baseline: time + memory<br/>+ flame graph"]
    BASE --> O1["fix 1 (from the graph)"] --> M1["re-measure"]
    M1 --> O2["fix 2"] --> M2["re-measure"]
    M2 --> O3["fix 3: streaming / multiprocessing"] --> M3["re-measure"]
    M3 --> REP["PERF.md: table + graphs + what didn't help"]
```

### Steps

1. Write (or take) a deliberately naive analyzer for a big log file with realistic inefficiencies.
2. Record the baseline: wall time, peak memory (`/usr/bin/time -v` or `memray`), and a flame graph.
3. Apply one optimization at a time, guided only by the profile; re-measure after each.
4. Include at least one change that *didn't* help, and say why (evidence beats intuition).
5. Add a benchmark to CI with a regression threshold.

**Done when:** `PERF.md` shows each step's measured effect (for example 10× total), with before/after flame graphs, and the CI benchmark catches a reintroduced slowdown.

---

## Open source

* [`google/benchmark`](https://github.com/google/benchmark) — a C++ microbenchmark library: repetitions, statistics, and `DoNotOptimize`.
* [`bheisler/criterion.rs`](https://github.com/bheisler/criterion.rs) — statistics-driven Rust benchmarking with change detection and HTML reports. See also Brendan Gregg's *Systems Performance* and the USE method.

---

## Interview

1. **"How do you find a performance bottleneck?"**
   <details><summary>Answer</summary>Start from a concrete goal and a reproducible load. Measure end to end with metrics and traces to see which component or dependency dominates latency. If it's a dependency (DB, network), inspect those calls: query plans, N+1 queries, round trips. If it's CPU, profile with a sampling profiler and read the flame graph for the widest frames. Check for contention (lock waits) and GC. Change one thing and re-measure. Never guess.</details>

2. **"When is optimization premature?"**
   <details><summary>Answer</summary>When there's no measured problem or performance target, when the code isn't on a hot path, or when the change trades clarity for gains nobody needs. It's not premature to choose appropriate algorithms and data structures, avoid known anti-patterns (N+1 queries, unbounded loads), or design for known scale requirements — those are cheap early and expensive later.</details>

---

## Checklist

- [ ] measure before optimizing
- [ ] benchmark with statistical rigor
- [ ] optimize the hot path, not the noise

---

> [Contents](index.md) · ← [Chapter 9 — Static Analysis & Type Safety at Scale](ch09-static-analysis-and-type-safety-at-scale.md) · Next → [Chapter 11 — Security & Threat Modeling](ch11-security-and-threat-modeling.md)
