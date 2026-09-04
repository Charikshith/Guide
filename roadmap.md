# Mastery Roadmap

> Structure: six **volumes**, each complete enough that finishing it means you genuinely master the area. Delivered as **125 chapters**, one concept each, with prerequisites, diagrams, examples, exercises, a mini project, real open-source references, interview questions, and a checklist.

## Volumes

| # | Volume | File | Chapters |
|---|--------|------|----------|
| 0 | Math & Mental Models | [volumes/volume-0-math.md](volumes/volume-0-math.md) | 1–9 (9) |
| 1 | Computer Science Foundations | [volumes/volume-1-cs-foundations.md](volumes/volume-1-cs-foundations.md) | 1–49 (49) |
| 2 | Software Engineering | [volumes/volume-2-software-engineering.md](volumes/volume-2-software-engineering.md) | 1–16 (16) |
| 3 | Low-Level Design | [volumes/volume-3-low-level-design.md](volumes/volume-3-low-level-design.md) | 1–14 (14) |
| 4 | High-Level Design | [volumes/volume-4-high-level-design.md](volumes/volume-4-high-level-design.md) | 1–17 (17) |
| 5 | AI Systems Engineering | [volumes/volume-5-ai-systems.md](volumes/volume-5-ai-systems.md) | 1–20 (20) |

**Total: 125 chapters** across the six volumes.

---

## Prerequisite Ordering

The volumes are **not** strictly linear. Key cross-volume dependencies:

* **Volume 0** → gates Vol 1 Part 4 (algorithms) and *all* of Vol 5.
* **Vol 1 Part 1–3** (programming, dev env, SE fundamentals) → everything.
* **Vol 1 Part 5–6** (architecture, OS) → Vol 1 Part 9 (distributed) and Vol 4.
* **Vol 1 Part 7–8** (networking, DB) → Vol 4 (HLD).
* **Vol 1 Part 9** (distributed systems) + **Vol 1 Part 11** (cloud/ops) → Vol 4 (HLD) and Vol 5 serving/GPU infra.
* **Vol 3** (LLD) → Vol 4 (HLD).
* **Vol 0 Ch 9** (linear algebra) + **Vol 1 Ch 9** (encoding) → Vol 5 foundations.

Each chapter declares its own prerequisites explicitly; treat the above as the volume-level skeleton.

---

## Exit Criteria (per volume)

* **Vol 0** — Solve a set of Big-O, probability, and linear-algebra problems from scratch.
* **Vol 1** — Build one non-trivial CLI/service touching files, network, and a database.
* **Vol 2** — Ship a project with full CI/CD, tests, observability, and a postmortem for one induced failure.
* **Vol 3** — 30+ production-quality components.
* **Vol 4** — 30+ real-world system designs.
* **Vol 5** — The 7 progressive builds, ending at the AI Operating System.

---

## Chapter format

Each chapter:

* teaches exactly one concept,
* has prerequisites,
* includes diagrams,
* provides simple examples,
* includes coding exercises,
* has a mini project,
* points to real open-source code,
* ends with interview questions and a checklist.
