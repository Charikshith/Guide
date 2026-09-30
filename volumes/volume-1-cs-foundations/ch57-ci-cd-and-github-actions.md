# Chapter 57 — CI/CD & GitHub Actions

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 56 — IaC: Terraform, State & Config Drift](ch56-iac-terraform-state-and-config-drift.md) · Next → [Chapter 58 — Observability: Logs, Metrics, Traces & OpenTelemetry](ch58-observability-logs-metrics-traces-and-opentelemetry.md)

---

## Concept

Automating build/test/deploy pipelines with GitHub Actions and deployment gates.

**In one sentence:** continuous integration automatically builds and tests every change so the main branch is always working, continuous delivery keeps every passing build ready to release, and continuous deployment releases it automatically — with GitHub Actions as a common place to write those pipelines.

**Mental model — an airport security line.** Every bag (commit) goes through the same scanners (lint, test, build) before it can board. Nobody gets a personal exemption. Delivery is the plane being ready at the gate; deployment is the plane actually taking off — sometimes only after a pilot's final check (a manual approval gate).

**CI vs CD vs CD**

| | Continuous Integration | Continuous Delivery | Continuous Deployment |
|-|------------------------|---------------------|-----------------------|
| Trigger | every push / PR | every merge to main | every merge to main |
| Does | build, lint, test, security scans | + produce a versioned, deployable artifact; deploy to staging | + deploy to production automatically |
| Human step | code review | a click to release to prod | none (guarded by tests, canaries, and rollbacks) |

**GitHub Actions vocabulary**

| Term | Meaning |
|------|---------|
| Workflow | a YAML file in `.github/workflows/`, triggered by events (`push`, `pull_request`, `schedule`, `workflow_dispatch`) |
| Job | runs on one runner; jobs run in parallel unless linked with `needs:` |
| Step | a shell command (`run:`) or a reusable action (`uses:`) |
| Runner | a VM or container that executes jobs (GitHub-hosted or self-hosted) |
| Matrix | run a job for each combination (Python 3.11/3.12 × Linux/macOS) |
| Cache / artifacts | reuse dependencies between runs / pass files between jobs or keep them |
| Environment | a deployment target (`staging`, `production`) with protection rules: required reviewers, wait timers, branch limits, scoped secrets |
| OIDC | short-lived cloud credentials for the job, instead of stored long-lived keys |

**Keeping pipelines fast**

| Technique | Effect |
|-----------|--------|
| Cache dependencies (`actions/setup-python` with `cache: pip`, `setup-uv`, `setup-node` with `cache: npm`) | minutes → seconds |
| Run fast checks first; fail fast | feedback in under 2 minutes |
| Parallel jobs and test sharding | wall time ÷ N |
| Path filters (`paths:`) | skip unrelated work in monorepos |
| `concurrency:` with `cancel-in-progress` | stop outdated runs on the same branch |
| Build once, deploy the *same* artifact everywhere | no rebuild drift between staging and prod |
| Docker layer caching (`cache-from: type=gha`) | fast image builds |

**Security** — pin third-party actions to a commit SHA; set `permissions:` to least privilege (default `contents: read`); never print secrets; don't run untrusted fork code with secrets (`pull_request_target` is dangerous); use OIDC for clouds.

---

## Prereqs

* [Chapter 21 — Build Systems & Package Management](ch21-build-systems-and-package-management.md)
* [Vol 2 Ch 5 — CI/CD](../volume-2-software-engineering/ch05-ci-cd.md)

---

## Diagram

**A workflow: push → build → test → deploy with a manual approval gate**

```mermaid
flowchart LR
    PUSH["push / PR"] --> LINT["lint + typecheck<br/>~30 s"]
    PUSH --> TEST["test matrix<br/>py3.11 · py3.12<br/>~2 min"]
    LINT & TEST --> BUILD["build image<br/>tag = git SHA<br/>push to GHCR"]
    BUILD -->|"main only"| STG["deploy: staging<br/>(automatic)"]
    STG --> SMOKE["smoke tests"]
    SMOKE --> GATE{{"environment: production<br/>required reviewer ✋"}}
    GATE -->|approved| PROD["deploy: production<br/>(same image digest)"]
    PROD --> VERIFY["post-deploy checks<br/>→ auto-rollback on failure"]
```

**Parallel jobs and `needs:`**

```
 time →    0s        30s       2m        3m        4m
 lint      ████
 test-3.11 ██████████████
 test-3.12 ██████████████
 build                    ██████
 staging                        ████
 prod                               ⏸ waiting for approval … ████
```

---

## Example

```yaml
# .github/workflows/ci-cd.yml
name: ci-cd
on:
  push: { branches: [main] }
  pull_request:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with: { enable-cache: true }
      - run: uv sync --frozen
      - run: uv run ruff check . && uv run ruff format --check . && uv run mypy src

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { python: ["3.11", "3.12"] }
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test }
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 5s --health-retries 10
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with: { enable-cache: true, python-version: "${{ matrix.python }}" }
      - run: uv sync --frozen
      - run: uv run pytest -q --cov=src
        env: { DATABASE_URL: "postgresql://postgres:test@localhost:5432/postgres" }

  build:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    outputs: { image: "${{ steps.meta.outputs.image }}" }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: "${{ github.actor }}", password: "${{ secrets.GITHUB_TOKEN }}" }
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - id: meta
        run: echo "image=ghcr.io/${{ github.repository }}:${{ github.sha }}" >> "$GITHUB_OUTPUT"

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./scripts/deploy.sh staging "${{ needs.build.outputs.image }}"

  deploy-prod:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    environment: production          # protection rule: required reviewers → manual gate
    permissions: { id-token: write, contents: read }   # OIDC to the cloud, no stored keys
    steps:
      - run: ./scripts/deploy.sh production "${{ needs.build.outputs.image }}"
```

---

## Exercises

1. Write a CI workflow with build + test + lint.

   <details><summary>Solution</summary>The <code>lint</code> and <code>test</code> jobs above: triggered on <code>pull_request</code>, least-privilege <code>permissions</code>, cached dependencies, a matrix across versions, and a service container for the database. Make them required status checks in branch protection so a PR can't merge while red.</details>

2. Add a manual approval + deploy job.

   <details><summary>Solution</summary>Create a <code>production</code> environment in repository settings with required reviewers (and optionally a wait timer and a <code>main</code>-only branch rule). A job with <code>environment: production</code> pauses until approved; its secrets are only available after approval. Deploy the exact image digest built earlier, never a rebuild.</details>

3. Your CI takes 25 minutes. List five changes to cut it below 5.

   <details><summary>Solution</summary>(1) Cache dependencies and Docker layers. (2) Split lint, unit, and integration tests into parallel jobs and shard slow suites. (3) Path filters so docs-only changes skip tests. (4) Cancel superseded runs with <code>concurrency</code>. (5) Profile the slowest tests: replace <code>sleep</code>s with fakes, share expensive fixtures, move slow E2E tests to a nightly job. Also use bigger runners for CPU-bound builds.</details>

---

## Mini project

**A full CI/CD pipeline for a service, deployed on every merge.**

```mermaid
flowchart LR
    PR["pull request"] --> CI["lint · types · tests · coverage ·<br/>dependency and secret scan"]
    CI --> REQ["required checks + 1 review"] --> MERGE["merge to main"]
    MERGE --> IMG["build + sign image (digest)"] --> STG["auto-deploy staging (kind / Fly / Render)"]
    STG --> E2E["smoke / E2E tests"] --> APP{{"production approval"}} --> PROD["deploy prod"]
    PROD --> HC["health check → rollback on failure"]
    PROD --> TAG["create a GitHub release + changelog"]
```

**Steps**

1. Use the service from an earlier chapter (e.g. the [Ch 26](ch26-testing-unit-integration-mocking-and-coverage.md) to-do API).
2. PR workflow: lint, types, tests with a coverage threshold, `pip-audit`/`osv-scanner`, and `gitleaks`.
3. Branch protection: required checks plus a review.
4. On merge: build the image once, tag it with the SHA, deploy to staging, and run smoke tests.
5. A production environment with an approval gate; the deploy script waits for health and rolls back automatically.
6. Record a before/after of pipeline duration after adding caching and parallelism.

**Done when:** a merged PR reaches staging with no human action, reaches production after one approval, and a deliberately broken release rolls back by itself.

---

## Open source

* [`actions/runner`](https://github.com/actions/runner) — the agent that executes jobs (useful for self-hosting); see also `actions/cache`, `actions/checkout`, and `nektos/act` to run workflows locally.

---

## Interview

1. **"CI vs CD?"**
   <details><summary>Answer</summary>CI is merging small changes often and automatically building and testing each one, so integration problems appear within minutes. Continuous Delivery keeps every passing build releasable, with a push-button deploy. Continuous Deployment removes the button: every passing change goes to production automatically, relying on strong tests, progressive rollout, monitoring, and automatic rollback.</details>

2. **"How do you keep pipelines fast?"**
   <details><summary>Answer</summary>Cache dependencies and build layers; fail fast with cheap checks first; parallelize jobs and shard tests; skip unaffected work with path filters or build-graph tools; cancel superseded runs; build once and promote the same artifact; move slow suites to nightly runs; and treat the pipeline's duration as a metric you keep watching.</details>

---

## Checklist

- [ ] validate every commit
- [ ] gate deploys
- [ ] cache dependencies

---

> [Contents](index.md) · ← [Chapter 56 — IaC: Terraform, State & Config Drift](ch56-iac-terraform-state-and-config-drift.md) · Next → [Chapter 58 — Observability: Logs, Metrics, Traces & OpenTelemetry](ch58-observability-logs-metrics-traces-and-opentelemetry.md)
