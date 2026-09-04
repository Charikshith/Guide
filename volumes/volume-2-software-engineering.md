# Volume 2 — Software Engineering

> Goal: Everything beyond writing code that ships and survives production.
>
> **Chapters 1–16.**

# Contents

1. Professional Git Workflow
2. Monorepos
3. Dependency Injection & Inversion of Control
4. The Testing Pyramid & Test Strategy
5. CI/CD
6. Packaging & Release Engineering
7. Code Reviews
8. Static Analysis & Type Safety at Scale
9. Performance Engineering
10. Security & Threat Modeling
11. Licensing & OSS Compliance
12. API Design & Versioning
13. Documentation as a System
14. Observability: Logs, Metrics & Traces
15. Incident Response & Postmortems
16. Production Debugging

---

## Chapter 1 — Professional Git Workflow

**Concept:** Trunk-based vs GitFlow, PRs, code review flow, conventional commits, and recovering from mistakes (revert, reflog).

**Prereqs:** Vol 1 Ch 19–20.

**Diagram:** A trunk-based flow: short-lived branches → PR → review → squash-merge → tag.

**Example:** `git switch -c feat/x`, `git commit -m "feat: add x"`, `git revert`, `git reflog`.

**Exercises:** (1) Recover a commit deleted by a bad rebase using reflog. (2) Write conventional commits for a multi-change PR.

**Mini project:** Script a release: bump version → changelog → tag → signed push.

**Open source:** [`git/git`](https://github.com/git/git); [`conventional-commits/conventionalcommits.org`](https://github.com/conventional-commits/conventionalcommits.org).

**Interview:** "Trunk-based vs GitFlow?" / "How do you undo a pushed commit safely?"

**Checklist:** ☐ keep branches short-lived ☐ write meaningful commit messages ☐ never force-push shared branches

---

## Chapter 2 — Monorepos

**Concept:** One repo, many projects — benefits (atomic changes, shared code) and costs (scaling, tooling); workspace tooling.

**Prereqs:** Ch 1.

**Diagram:** A monorepo tree with shared packages and a dependency graph across them.

**Example:** Rust `[workspace]` members; npm/pnpm workspaces; a shared CI build graph.

**Exercises:** (1) Set up a two-crate Rust workspace. (2) Make one change that updates a shared package and all consumers.

**Mini project:** A small monorepo with a shared library + two apps built by one command.

**Open source:** [`rust-lang/cargo`](https://github.com/rust-lang/cargo) workspaces; [`pnpm/pnpm`](https://github.com/pnpm/pnpm).

**Interview:** "Monorepo vs polyrepo — trade-offs?" / "How do you keep CI fast in a monorepo?"

**Checklist:** ☐ share code without copy-paste ☐ build only what changed ☐ pin internal deps by path/version

---

## Chapter 3 — Dependency Injection & Inversion of Control

**Concept:** Inject dependencies instead of constructing them; interfaces at seams; why DI enables testing and swapping implementations.

**Prereqs:** Vol 1 Ch 10, Ch 22.

**Diagram:** A component with dependencies injected vs hardcoded `new` calls.

**Example:** `class Service: def __init__(self, db: Database): ...`; a Rust `trait Db` passed in.

**Exercises:** (1) Refactor a hardcoded dependency to constructor injection. (2) Swap a real client for a fake in a test with zero production changes.

**Mini project:** A service wired via constructor injection with a config-chosen backend.

**Open source:** [`spring-projects/spring-framework`](https://github.com/spring-projects/spring-framework); manual DI in [`rust-lang/rust`](https://github.com/rust-lang/rust) (traits).

**Interview:** "Why does DI help testing?" / "What's inversion of control?"

**Checklist:** ☐ no hidden `new` in constructors ☐ depend on interfaces, not concretions ☐ wire at the composition root

---

## Chapter 4 — The Testing Pyramid & Test Strategy

**Concept:** Unit/integration/e2e proportions, test doubles, property-based testing, and flaky-test hygiene.

**Prereqs:** Vol 1 Ch 26.

**Diagram:** The testing pyramid with effort/count annotations.

**Example:** `pytest` unit tests + `hypothesis` property tests + a single e2e suite.

**Exercises:** (1) Write a property-based test for a sorting invariant. (2) Find and fix a flaky test's root cause.

**Mini project:** A test suite for a small API with the pyramid proportions enforced by CI.

**Open source:** [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest); [`HypothesisWorks/hypothesis`](https://github.com/HypothesisWorks/hypothesis).

**Interview:** "What's the right unit:integration ratio?" / "How do you handle flaky tests?"

**Checklist:** ☐ keep tests fast & deterministic ☐ isolate I/O in tests ☐ use property tests for pure logic

---

## Chapter 5 — CI/CD

**Concept:** Continuous integration (validate every change) and delivery/deployment (ship safely); pipelines as code.

**Prereqs:** Ch 1.

**Diagram:** A pipeline: commit → build → test → lint → stage → deploy → verify.

**Example:** a GitHub Actions workflow with jobs, caching, and a deploy gate.

**Exercises:** (1) Write a CI workflow that runs tests + lints. (2) Add caching and a manual deploy approval.

**Mini project:** Full CI/CD for a toy service: automated tests + deploy to a staging environment.

**Open source:** [`actions/runner`](https://github.com/actions/runner); [`gitlab-org/gitlab-runner`](https://github.com/gitlab-org/gitlab-runner).

**Interview:** "CI vs CD?" / "How do you make CI fast?"

**Checklist:** ☐ every commit is validated ☐ deploys are repeatable ☐ cache dependencies

---

## Chapter 6 — Packaging & Release Engineering

**Concept:** Versioning, changelogs, artifacts, feature flags, and progressive delivery (blue-green, canary, rollbacks).

**Prereqs:** Ch 5.

**Diagram:** A canary ramp: 1% → 10% → 100% with rollback trigger.

**Example:** `poetry build`/`cargo package`; a feature flag `if flag_enabled("x")`; a canary deployment.

**Exercises:** (1) Package a library and publish it to a local index. (2) Implement a feature flag with a kill switch.

**Mini project:** A release pipeline with version bump, artifact, canary deploy, and rollback.

**Open source:** [`open-feature/open-feature`](https://github.com/open-feature/open-feature); [`semver/semver`](https://github.com/semver/semver).

**Interview:** "Blue-green vs canary?" / "Why feature flags for releases?"

**Checklist:** ☐ automate versioning ☐ ship behind flags ☐ always be able to roll back

---

## Chapter 7 — Code Reviews

**Concept:** Reviewing for correctness, maintainability, security, and performance; giving and receiving feedback effectively.

**Prereqs:** Vol 1 Ch 22.

**Diagram:** A review checklist flow: diff → correctness → design → tests → style.

**Example:** A PR comment separating "must fix" from "nice to have".

**Exercises:** (1) Review a PR with a bug and write actionable feedback. (2) Fix a PR based on review comments and re-request.

**Mini project:** Establish a review checklist and apply it to a real (or sample) PR.

**Open source:** [`google/eng-practices`](https://github.com/google/eng-practices).

**Interview:** "What do you look for in a code review?" / "How do you handle disagreeing reviewers?"

**Checklist:** ☐ review for bugs, not just style ☐ keep PRs small ☐ give actionable, non-personal feedback

---

## Chapter 8 — Static Analysis & Type Safety at Scale

**Concept:** Linters/formatters/type checkers as CI gates; gradually typing a legacy codebase; design-by-contract.

**Prereqs:** Vol 1 Ch 28.

**Diagram:** A gradual-typing adoption map (typed core vs untyped edges).

**Example:** `mypy --strict`, `ruff`, `eslint` wired into CI; `#[deny(warnings)]`.

**Exercises:** (1) Add a type checker to a legacy module and fix the findings. (2) Configure a linter rule set for a team.

**Mini project:** Introduce strict static analysis to a small codebase with a baseline + incremental adoption.

**Open source:** [`python/mypy`](https://github.com/python/mypy); [`astral-sh/ruff`](https://github.com/astral-sh/ruff).

**Interview:** "How do you adopt typing in a large codebase?" / "What do static tools catch that tests don't?"

**Checklist:** ☐ gate on static analysis in CI ☐ type the public API first ☐ let tools, not humans, enforce style

---

## Chapter 9 — Performance Engineering

**Concept:** Profiling-driven optimization, benchmarking, caching strategies, and avoiding premature optimization.

**Prereqs:** Vol 1 Ch 27.

**Diagram:** A flame graph pointing at the hot path; a benchmark comparison chart.

**Example:** `py-spy` / `perf` finding a hotspot; a benchmark with `criterion`.

**Exercises:** (1) Profile a slow service and optimize the real bottleneck. (2) Write a benchmark that proves an optimization helps.

**Mini project:** Take a naive implementation, profile it, optimize it, and document the speedup with benchmarks.

**Open source:** [`google/benchmark`](https://github.com/google/benchmark); [`bheisler/criterion.rs`](https://github.com/bheisler/criterion.rs).

**Interview:** "How do you find a performance bottleneck?" / "When is optimization premature?"

**Checklist:** ☐ measure before optimizing ☐ benchmark with statistical rigor ☐ optimize the hot path, not the noise

---

## Chapter 10 — Security & Threat Modeling

**Concept:** STRIDE/attack trees, the OWASP Top 10, secure defaults, secrets handling, and supply-chain security.

**Prereqs:** Vol 1 Ch 25, Ch 41.

**Diagram:** A data-flow diagram with trust boundaries and threat annotations.

**Example:** a SQL-injection fix via parameterized queries; a secret moved to a vault.

**Exercises:** (1) Threat-model a login flow and list mitigations. (2) Find and fix an injection vulnerability.

**Mini project:** A security review of a small app: threat model + fix the top 3 findings.

**Open source:** [`OWASP/CheatSheetSeries`](https://github.com/OWASP/CheatSheetSeries); [`OWASP/Top10`](https://github.com/OWASP/Top10).

**Interview:** "How do you threat-model a feature?" / "What's the most common web vuln and its fix?"

**Checklist:** ☐ draw trust boundaries ☐ parameterize all queries ☐ rotate secrets automatically

---

## Chapter 11 — Licensing & OSS Compliance

**Concept:** Licenses (MIT/Apache/GPL/AGPL), attribution, and scanning dependencies for license/security issues.

**Prereqs:** Vol 1 Ch 21.

**Diagram:** A permissive → copyleft spectrum diagram.

**Example:** adding a NOTICE for Apache-2.0; a `pip-licenses`/`cargo-deny` scan.

**Exercises:** (1) Classify a set of licenses by obligation. (2) Scan a project's dependencies and flag a GPL violation risk.

**Mini project:** Add a license + NOTICE + dependency license scan to a project's CI.

**Open source:** [`EmbarkStudios/cargo-deny`](https://github.com/EmbarkStudios/cargo-deny); [`nexB/scancode-toolkit`](https://github.com/nexB/scancode-toolkit).

**Interview:** "MIT vs GPL obligations?" / "Why track dependency licenses?"

**Checklist:** ☐ pick a license deliberately ☐ attribute correctly ☐ scan deps in CI

---

## Chapter 12 — API Design & Versioning

**Concept:** Designing clean, evolvable APIs; naming, error contracts, pagination, idempotency; versioning (URI vs header vs field).

**Prereqs:** Vol 1 Ch 42.

**Diagram:** An API evolution timeline showing additive vs breaking changes.

**Example:** a REST resource with pagination and `Idempotency-Key`; `POST /v2/orders` vs `Accept: version=2`.

**Exercises:** (1) Design an API for a resource with filtering/pagination. (2) Evolve an API additively without breaking clients.

**Mini project:** A versioned REST API with a documented deprecation policy and a test matrix.

**Open source:** [`stripe/stripe-python`](https://github.com/stripe/stripe-python) (API design reference); [`googleapis/googleapis`](https://github.com/googleapis/googleapis).

**Interview:** "How do you version an API?" / "What makes an API idempotent?"

**Checklist:** ☐ return consistent error shapes ☐ paginate large lists ☐ support idempotent writes

---

## Chapter 13 — Documentation as a System

**Concept:** Docs that stay current — doc-as-code, API references, runbooks, ADRs, and onboarding guides.

**Prereqs:** Vol 1 Ch 23.

**Diagram:** A documentation site architecture: guides → reference → how-to → explanation.

**Example:** mkdocs with auto-generated API reference + a runbook with commands.

**Exercises:** (1) Turn scattered notes into the four doc types. (2) Write a runbook that a new on-call could follow.

**Mini project:** A doc site with generated API docs, a runbook, and a contribution guide.

**Open source:** [`mkdocs/mkdocs`](https://github.com/mkdocs/mkdocs); [`squidfunk/mkdocs-material`](https://github.com/squidfunk/mkdocs-material).

**Interview:** "How do you keep docs from rotting?" / "What belongs in a runbook?"

**Checklist:** ☐ docs are generated where possible ☐ write runbooks for incidents ☐ review docs in PRs

---

## Chapter 14 — Observability: Logs, Metrics & Traces

**Concept:** The three pillars, instrumentation, dashboards, SLOs/SLIs, and debugging with traces.

**Prereqs:** Vol 1 Ch 24.

**Diagram:** A trace spanning services with spans; a RED/USE dashboard.

**Example:** OpenTelemetry spans with trace IDs; a Prometheus counter; structured logs.

**Exercises:** (1) Instrument a service with metrics + traces. (2) Define an SLO and the SLI that measures it.

**Mini project:** Add OpenTelemetry to a service and produce a trace view + a latency dashboard.

**Open source:** [`open-telemetry/opentelemetry-python`](https://github.com/open-telemetry/opentelemetry-python); [`prometheus/prometheus`](https://github.com/prometheus/prometheus).

**Interview:** "Logs vs metrics vs traces?" / "What's an SLO vs SLA?"

**Checklist:** ☐ emit all three signals ☐ correlate via trace IDs ☐ alert on SLO burn

---

## Chapter 15 — Incident Response & Postmortems

**Concept:** On-call hygiene, detection→response→remediation, blameless postmortems, and driving action items.

**Prereqs:** Ch 14.

**Diagram:** An incident timeline (detect → mitigate → resolve → learn).

**Example:** a blameless postmortem template; an on-call runbook escalation path.

**Exercises:** (1) Write a postmortem for a simulated outage with a clear root cause and action items. (2) Design a severity + escalation matrix.

**Mini project:** Run a tabletop incident drill and produce a postmortem with follow-ups.

**Open source:** [`dastergon/awesome-sre`](https://github.com/dastergon/awesome-sre); [`grafana/oncall`](https://github.com/grafana/oncall).

**Interview:** "How do you run a blameless postmortem?" / "What do you do first during an incident?"

**Checklist:** ☐ mitigate before root-causing ☐ keep a timeline ☐ track action items to completion

---

## Chapter 16 — Production Debugging

**Concept:** Debugging live systems safely — read-only access, replicating in staging, graceful degradation, and forensics.

**Prereqs:** Ch 15, Vol 1 Ch 27.

**Diagram:** A decision flow: observe → hypothesize → reproduce in staging → fix → verify.

**Example:** `kubectl logs`, `strace`, heap dumps, and a feature flag to degrade a failing path.

**Exercises:** (1) Diagnose a simulated production failure using only logs/metrics/traces. (2) Add a graceful-degradation path with a circuit breaker.

**Mini project:** Inject a failure into a running service, debug it read-only, fix, and write up the forensic trail.

**Open source:** [`async-profiler`](https://github.com/async-profiler/async-profiler); [`brendangregg/perf-tools`](https://github.com/brendangregg/perf-tools).

**Interview:** "How do you debug a production-only issue?" / "What's a circuit breaker for?"

**Checklist:** ☐ never mutate prod state carelessly ☐ reproduce in staging ☐ add degradation knobs

---

**Exit criteria:** Ship a project with full CI/CD, tests, observability, and a postmortem for one induced failure.
