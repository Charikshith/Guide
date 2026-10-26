# Chapter 5 — The Testing Pyramid & Test Strategy

> **Volume 2 — Software Engineering** · [Contents](index.md) · ← [Chapter 4 — Dependency Injection & Inversion of Control](ch04-dependency-injection-and-inversion-of-control.md) · Next → [Chapter 6 — CI/CD](ch06-ci-cd.md)

---

## Concept

Unit/integration/e2e proportions, test doubles, property-based testing, and flaky-test hygiene.

**In one sentence:** a test strategy decides *what* to test at *which* level so the suite catches real bugs quickly and cheaply — lots of fast unit and property tests for logic, fewer integration tests for wiring, a thin layer of end-to-end tests for critical journeys — and treats flaky tests as bugs.

**Mental model — a building inspection.** You check every brick and beam at the factory (unit), then check that walls join properly on site (integration), then walk through the finished house once (end-to-end). Walking through the whole house to check each brick would be absurdly slow — that's a suite made only of E2E tests (the "ice-cream cone" anti-pattern).

**Proportions (a guide, not a law)**

| Level | Share | Speed per test | What it proves | Owner |
|-------|:-:|---------------|----------------|-------|
| Unit + property | ~70% | < 10 ms | logic, edge cases, invariants | every dev, every PR |
| Integration / component | ~20% | 100 ms – 2 s | DB queries, serialization, one service with real dependencies in containers | every PR |
| Contract | a few per API | fast | producer and consumer agree on the interface | both teams |
| E2E | ~5–10% | seconds – minutes | critical user journeys work end to end | CI on main / pre-release |
| Manual / exploratory | ad hoc | — | usability, surprises | QA / product |

Shapes you'll hear about: the **pyramid** (this one); the **testing trophy** (integration-heavy, popular for frontends where "unit" means little); the **ice-cream cone** (mostly E2E and manual — an anti-pattern: slow and flaky).

**Right ratio?** The one where most bugs are caught by the cheapest test that *can* catch them. Pure logic → unit. SQL correctness → integration against a real DB (mocks can't catch SQL bugs). Cross-service contracts → contract tests. "The checkout button works" → one E2E.

**Property-based testing** — instead of listing examples, state a *property* that must hold for all inputs and let the tool generate hundreds of inputs, including nasty edge cases, then *shrink* any failure to a minimal counterexample.

| Property type | Example |
|---------------|---------|
| Invariant | `sorted(xs)` is ordered and has the same elements as `xs` |
| Round trip | `decode(encode(x)) == x` |
| Oracle | a fast implementation equals a slow, obviously correct one |
| Idempotence | `normalize(normalize(s)) == normalize(s)` |
| Metamorphic | `search(q) ⊇ search(q + " extra filter")` |

**Flaky tests** — tests that pass and fail without code changes. Common causes and fixes:

| Cause | Fix |
|-------|-----|
| Time: `now()`, sleeps, timezones, DST | inject a clock; freeze time; never `sleep` to "wait" — poll for a condition |
| Order dependence / shared state | isolate: fresh fixtures, transactions rolled back per test, random test order (`pytest-randomly`) |
| Concurrency / async races | await real completion signals; deterministic schedulers |
| Randomness | seed it; log the seed |
| Network / external services | fakes, or containers pinned to a version |
| Resource leaks, ports in use | ephemeral ports, cleanup fixtures |

Policy: **quarantine** a flaky test immediately (don't let it train people to ignore red), file a ticket with an owner, fix or delete within days, and track the flake rate.

**Scope and size are different questions**

*Scope* is **what code a test verifies**: a *unit* test checks one small piece through its public interface (test behaviour and resulting state, not the exact sequence of internal calls, so refactoring doesn't break it); a *narrow integration* test checks one service's adapter against one real dependency (the repository against a real Postgres); a *broad* or *end-to-end* test checks a user scenario across several live services. *Size* is **what it needs to run** (Google's terms):

| Size | Runs | Speed and flakiness |
|------|------|---------------------|
| **Small** | one process, no I/O, no sleeping, no network | milliseconds, deterministic |
| **Medium** | one machine; local disk, `localhost` network, a database in a container | seconds; some timing risk |
| **Large** | several machines or a shared environment | minutes; most flaky |

Write the *smallest* test that can catch the bug at the scope you need. End-to-end tests are the most brittle and the hardest to diagnose (which of five services broke?), so keep them few and make each one a **user journey** — create an order, change it, cancel it — rather than many separate one-step tests.

**Choosing a test double** — to shrink a test you replace a dependency:

| Double | What it is | Resemblance to the real thing |
|--------|-----------|-------------------------------|
| **Real implementation** | the actual library or service | full — prefer it when it is fast, deterministic, and has no external dependencies |
| **Fake** | a working lightweight version (an in-memory database, a local S3 emulator), ideally maintained by the dependency's owners | good |
| **Stub** | returns canned answers whatever you pass | low |
| **Mock** | records calls and asserts *how* it was called | low, and couples the test to implementation details |

The less a double resembles reality, the less a passing test proves. Pair mocks with **contract tests**: the consumer records the request it sends and the response it expects; the provider's own test suite replays those contracts against the real implementation, so the mock can't silently drift from reality.

**When the stakes are high, test the real thing in production.** Some behaviour is too costly to get wrong to trust doubles — for example "delete all of a user's data" under GDPR, where a silent failure can mean fines of up to 4% of annual turnover. Run an end-to-end check periodically *in production* against live services (create a synthetic user, purge it, verify nothing remains anywhere).

**Check the design before writing code: formal specifications.** Tests only explore the cases people think of. A system at scale will eventually hit the rare interleavings nobody imagined. A *formal specification* in a language like **TLA+** describes the system as states and the steps between them; a **model checker** then explores *every* reachable interleaving and checks your properties — *safety* ("the two stores never disagree permanently") and *liveness* ("every write is eventually applied") — returning a step-by-step counterexample when one fails. Amazon used it on S3 and DynamoDB, Microsoft on Cosmos DB. Specify only the risky core (a replication or migration protocol), at a level of detail that still catches the bug.

Example: migrating from store X to store Y with **dual writes** (write both, read X, backfill Y, then switch reads to Y). A model checker quickly finds two failures: a process that crashes between the two writes leaves them permanently different, and two instances writing concurrently can have their writes land in *opposite orders* in the two stores:

```mermaid
sequenceDiagram
    participant I1 as Instance 1
    participant X as Store X
    participant Y as Store Y
    participant I2 as Instance 2
    I1->>X: write "bar"
    I2->>X: write "foo"
    I2->>Y: write "foo"
    I1->>Y: write "bar"
    Note over X,Y: X ends with "foo", Y ends with "bar" — they disagree forever
```

The fix is to stop writing to two places directly: write once to a log or queue that fixes a single global order, and have both stores apply it in that order (the [outbox / change-data-capture](../volume-4-high-level-design/ch12-event-driven-systems.md) pattern).

---

## Prereqs

* [Vol 1 Ch 26 — Testing: Unit, Integration, Mocking & Coverage](../volume-1-cs-foundations/ch26-testing-unit-integration-mocking-and-coverage.md)

---

## Diagram

**The testing pyramid with effort/count annotations**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 338" role="img" aria-label="Test pyramid with counts, run times and tools for end-to-end, contract, integration and unit-plus-property tests" style="width:100%;max-width:800px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><polygon points="210.0,40 250.0,40 287.5,98 172.5,98" fill="var(--danger)" fill-opacity=".28" stroke="var(--danger)" stroke-width="1.8"/><text x="230" y="74" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">E2E</text><text x="440" y="66" font-size="13.5" text-anchor="start" fill="var(--text)" font-weight="700">~15 tests · 6 min · Playwright</text><text x="440" y="84" font-size="12.5" text-anchor="start" fill="var(--text-muted)">critical journeys: sign up, checkout, refund</text><polygon points="172.5,102 287.5,102 325.0,160 135.0,160" fill="var(--accent)" fill-opacity=".28" stroke="var(--accent)" stroke-width="1.8"/><text x="230" y="136" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">Contract</text><text x="440" y="128" font-size="13.5" text-anchor="start" fill="var(--text)" font-weight="700">~10 · 20 s · Pact</text><polygon points="135.0,164 325.0,164 362.5,222 97.5,222" fill="var(--primary)" fill-opacity=".28" stroke="var(--primary)" stroke-width="1.8"/><text x="230" y="198" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">Integration</text><text x="440" y="190" font-size="13.5" text-anchor="start" fill="var(--text)" font-weight="700">~150 · 90 s · Postgres + Redis in containers</text><polygon points="97.5,226 362.5,226 400.0,284 60.0,284" fill="var(--success)" fill-opacity=".28" stroke="var(--success)" stroke-width="1.8"/><text x="230" y="260" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">Unit + property</text><text x="440" y="252" font-size="13.5" text-anchor="start" fill="var(--text)" font-weight="700">~1,500 · 20 s · pure logic, fakes</text><text x="230" y="22" font-size="12.5" text-anchor="middle" fill="var(--text-muted)" font-weight="600">▲ cost to write &amp; maintain, run time, flakiness</text><text x="230" y="310" font-size="12.5" text-anchor="middle" fill="var(--text-muted)" font-weight="600">▼ count, speed, precision of failure messages</text></svg>
</div>

**Pick the cheapest level that can catch the bug**

```mermaid
flowchart TD
    B["What could break?"] --> L{"pure logic?<br/>(pricing, parsing, rules)"}
    L -- yes --> U["unit / property test"]
    L -- no --> I{"our code + a real dependency?<br/>(SQL, queue, file format)"}
    I -- yes --> IT["integration test with a container"]
    I -- no --> C{"an interface between teams/services?"}
    C -- yes --> CT["contract test"]
    C -- no --> E["E2E test (only if it is a critical journey)"]
```

**Property-based testing: generate → check → shrink**

```
 property: for all lists xs, my_sort(xs) == sorted(xs)
 generated:  [], [0], [3, -1], [5, 5, 2], [2147483648, -0.0, …] …   (200 cases)
 failure found:  [3, 1, 2, 1, 0, 9, 1]
 shrunk to:      [1, 0, 1]          ← the minimal failing example (a duplicate-handling bug)
```

---

## Example

```python
# Property-based tests with Hypothesis
from hypothesis import given, strategies as st
from collections import Counter

def my_sort(xs):                       # the function under test
    return sorted(xs)

@given(st.lists(st.integers()))
def test_sort_is_ordered_and_a_permutation(xs):
    out = my_sort(xs)
    assert all(a <= b for a, b in zip(out, out[1:]))      # invariant: ordered
    assert Counter(out) == Counter(xs)                    # invariant: same elements

@given(st.dictionaries(st.text(), st.integers()))
def test_json_round_trip(d):
    import json
    assert json.loads(json.dumps(d)) == d                 # round trip

@given(st.text())
def test_slugify_is_idempotent(s):
    assert slugify(slugify(s)) == slugify(s)
```

```python
# A flaky test and its fix
import time

def test_cache_expires_FLAKY():
    cache.set("k", 1, ttl=1)
    time.sleep(1)                        # sometimes 0.999 s elapses → still cached → fails
    assert cache.get("k") is None

def test_cache_expires(fake_clock):      # deterministic
    cache = Cache(clock=fake_clock)
    cache.set("k", 1, ttl=1)
    fake_clock.advance(seconds=1.001)
    assert cache.get("k") is None
```

```ini
# pytest.ini — markers keep the levels separate
[pytest]
markers =
    integration: needs containers
    e2e: full stack, slow
addopts = -p randomly --strict-markers
# PR:      pytest -m "not e2e"          (unit + integration, < 3 min)
# nightly: pytest -m e2e
```

---

## Exercises

1. Write a property-based test for a sorting invariant.

   <details><summary>Solution</summary>See <code>test_sort_is_ordered_and_a_permutation</code>. Add stability as a property: sort pairs by key and check that items with equal keys keep their input order. Break <code>my_sort</code> on purpose (drop duplicates) and watch Hypothesis shrink to <code>[0, 0]</code>.</details>

2. Find and fix a flaky test's root cause.

   <details><summary>Solution</summary>Reproduce: run it 200 times (<code>pytest --count=200</code>) and in random order. Look for time, shared state, ordering, concurrency, or network. Typical fix: replace a <code>sleep</code> with an injected fake clock or polling for a condition; give each test its own fixture or DB transaction; seed randomness. Rerunning the test until it passes is not a fix.</details>

3. Which level would you use to test: (a) VAT calculation rules, (b) a SQL query with a window function, (c) "a user can buy and receive a confirmation email", (d) the JSON shape service A sends to service B?

   <details><summary>Solution</summary>(a) Unit plus property tests. (b) Integration against real Postgres. (c) One E2E test, with a fake email inbox. (d) A contract test (consumer-driven, e.g. Pact).</details>

---

## Mini project

**A test suite for a small API with the pyramid proportions enforced by CI.**

```mermaid
flowchart LR
    API["shop-api<br/>pricing · carts · orders"] --> U["unit + Hypothesis<br/>pricing, discount rules"]
    API --> I["integration<br/>repo + Postgres container"]
    API --> E["E2E<br/>2 journeys via httpx"]
    U & I & E --> REP["junit.xml per level"] --> GATE["CI script: fail if<br/>E2E > 10% of tests,<br/>unit runtime > 30 s,<br/>any test marked flaky > 7 days"]
```

**Steps**

1. A small API with pricing rules, carts, and orders.
2. Unit tests + at least 3 properties (round trip, invariant, oracle) for pricing.
3. Integration tests against Postgres with a per-test transaction rollback.
4. Two E2E journeys; mark them `e2e`.
5. A CI step that counts tests per marker from the JUnit XML and fails if the shape drifts (e.g. E2E > 10% or unit tests too slow).
6. A `flaky` marker with an expiry date; CI fails when a quarantine expires.

**Done when:** CI shows the three levels with their counts and durations, and the proportion gate fails if someone adds E2E tests for pure logic.

---

## Open source

* [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest) — markers, fixtures, and plugins (`pytest-xdist`, `pytest-randomly`, `pytest-rerunfailures` for *detecting* flakes).
* [`HypothesisWorks/hypothesis`](https://github.com/HypothesisWorks/hypothesis) — property-based testing with shrinking, stateful testing (`RuleBasedStateMachine`), and a failure database.

---

## Interview

1. **"What's the right unit:integration ratio?"**
   <details><summary>Answer</summary>There's no universal number; roughly 70/20/10 is a starting point. The real rule: test each behavior at the cheapest level that can actually catch its bugs. Logic-heavy code leans unit; data-access code needs real-DB integration tests; frontends often lean toward component and integration tests (the "trophy"). Watch the outcomes: fast feedback, low flake rate, and bugs caught before production.</details>

2. **"How do you handle flaky tests?"**
   <details><summary>Answer</summary>Treat them as bugs. Detect them (run failures again, track flake rate per test); quarantine immediately so the main signal stays trustworthy; assign an owner and a deadline; find the root cause (time, shared state, ordering, concurrency, network, randomness) and fix it with determinism (injected clocks, isolated fixtures, awaiting real conditions); delete tests that provide no value. Never normalize "just rerun it".</details>

3. **"Fake, stub or mock — which do you prefer?"**
   <details><summary>Answer</summary>In order: the real implementation if it is fast and deterministic, then a fake (a working lightweight version, ideally maintained by the dependency's owners), and only then stubs or mocks. Stubs and mocks resemble the real thing least, so tests that rely on them prove less and break on refactors. If you do mock a service, back the mock with a contract test that the provider runs against its real implementation.</details>

4. **"Can formal methods replace tests?"**
   <details><summary>Answer</summary>No — they complement them. A model checker such as TLC for TLA+ explores every interleaving of a design and finds rare concurrency or failure bugs (a crash between two writes, writes applied in different orders) before code exists, which tests rarely catch. But it checks the model, not the code, so you still need tests to show the implementation matches it. Use formal specs for the small, risky core: replication, migrations, locking protocols.</details>

---

## Checklist

- [ ] keep tests fast & deterministic
- [ ] isolate I/O in tests
- [ ] use property tests for pure logic
- [ ] choose the smallest test size and the most realistic double for each behavior
- [ ] model-check risky designs (dual writes, migrations) before coding them

---

> [Contents](index.md) · ← [Chapter 4 — Dependency Injection & Inversion of Control](ch04-dependency-injection-and-inversion-of-control.md) · Next → [Chapter 6 — CI/CD](ch06-ci-cd.md)
