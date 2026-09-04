# Volume 0 — Math & Mental Models

> Goal: The math the rest of the book silently assumes. Load-bearing for algorithms (Vol 1 Part 4) and all of AI (Vol 5).
>
> Hard prerequisite gate. Don't start Volume 1 Part 4 (algorithms) or any of Volume 5 (AI) without it.
>>
> Hard prerequisite gate. Don't start Volume 1 Part 4 (algorithms) or any of Volume 5 (AI) without it.

---

## Part 0.1 — Discrete Math

* Logic & Boolean Algebra
* Sets, Relations, Functions
* Combinatorics & Counting
* Graph Theory (foundations)
* Proof by Induction

---

## Part 0.2 — Complexity

* Asymptotic Notation (Big-O, Θ, Ω)
* Time vs Space Complexity
* Amortized Analysis

---

## Part 0.3 — Probability & Statistics

* Probability Basics
* Distributions
* Expectation & Variance
* Bayes' Theorem
* Sampling & Estimation

---

## Part 0.4 — Linear Algebra (for AI)

* Vectors & Vector Spaces
* Matrices & Operations
* Dot Products & Similarity
* Eigenvalues / Eigenvectors (intuition)
* Gradients & Derivatives (calculus intuition for backprop)

---


> Goal: Understand how computers work from the hardware up to applications.

---

## Part 1 — Programming Fundamentals

### Module 1.1 Programming Basics

* Variables
* Primitive Data Types
* Complex Data Types
* Operators
* Expressions
* Statements
* Control Flow

  * if
  * switch/match
  * loops
* Functions
* Parameters
* Return Values
* Scope
* Namespaces

---

### Module 1.2 Data Structures in Programming

* Arrays
* Lists
* Tuples
* Dictionaries / HashMaps
* Sets
* Queues
* Stacks

---

### Module 1.3 Modular Programming

* Modules
* Packages
* Libraries
* Imports
* Dependency Management

---

### Module 1.4 Error Handling

* Exceptions
* Panic
* Result Types
* Option Types
* Error Propagation
* Custom Errors

---

### Module 1.5 File Handling & Data Formats

* Reading Files
* Writing Files
* Binary Files
* JSON
* CSV
* XML
* YAML
* TOML
* Character Encoding (ASCII, Unicode, UTF-8)
* Binary Serialization (Protobuf, MessagePack, Avro)

---

### Module 1.6 Advanced Language Features

* Generics
* Traits
* Interfaces
* Abstract Classes
* Reflection
* Metaprogramming
* Decorators
* Context Managers
* Closures
* Lambdas
* Iterators
* Generators
* Regular Expressions

---

### Module 1.7 Memory

* Stack
* Heap
* References
* Ownership
* Borrowing
* Lifetimes
* Garbage Collection
* Reference Counting

---

### Module 1.8 Concurrency Basics

* Threads
* Processes
* Async
* Await
* Futures
* Coroutines

---

### Module 1.9 Programming Paradigms

* Imperative
* Declarative
* Object-Oriented
* Functional
* Reactive
* Event-Driven

---

### Module 1.10 Correctness Traps

* Floating Point / IEEE-754
* Integer Overflow & Signedness
* Date, Time & Timezones

---

## Part 2 — Developer Environment

### Module 2.1 Linux

* Linux Filesystem
* Shell
* Bash
* Permissions
* Users
* Groups
* Processes
* Signals
* Services
* Networking
* SSH
* Cron
* systemd

---

### Module 2.2 Terminal Tools

* grep
* sed
* awk
* jq
* curl
* wget
* find
* xargs
* tmux
* rsync

---

### Module 2.3 Git

* Git Basics
* Branches
* Merge
* Rebase
* Cherry Pick
* Tags
* Stash
* Hooks
* Git Internals

---

### Module 2.4 Build Systems

* Cargo
* pip
* uv
* Poetry
* npm
* pnpm
* Make
* CMake
* Taskfiles

---

### Module 2.5 Package Management

* Python Packaging
* Rust Crates
* Node Packages
* Semantic Versioning

---

## Part 3 — Software Engineering Fundamentals

### Module 3.1 Clean Code

* Naming
* Functions
* Classes
* Readability
* Refactoring

---

### Module 3.2 Documentation

* Markdown
* API Docs
* Docstrings
* ADRs
* README Design

---

### Module 3.3 Logging

* Log Levels
* Structured Logging
* Correlation IDs

---

### Module 3.4 Configuration

* Environment Variables
* dotenv
* YAML
* TOML
* JSON Config
* Secrets Management

---

### Module 3.5 Testing Basics

* Unit Tests
* Integration Tests
* Mocking
* Coverage

---

### Module 3.6 Debugging

* Debuggers
* Profiling
* Memory Debugging
* Stack Traces

---

### Module 3.7 Static Analysis

* Linters
* Formatters
* Type Checkers

---

> Requires Volume 0 (complexity).

### Basic

* Arrays
* Linked Lists
* Stack
* Queue

### Intermediate

* Trees
* BST
* Heap
* Trie
* Hash Table

### Advanced

* Graph
* Segment Tree
* Fenwick Tree
* Union Find

Algorithms

* Sorting
* Searching
* Binary Search
* DFS
* BFS
* Dynamic Programming
* Greedy
* Divide & Conquer
* Sliding Window
* Two Pointer
* Topological Sort
* Backtracking

---

## Part 5 — Computer Architecture

* Binary
* Number Representation (two's complement, floats)
* CPU
* Registers
* Cache
* Memory Hierarchy
* Instruction Cycle
* Pipelining
* SIMD
* Virtual Memory

---

## Part 6 — Operating Systems

* Processes
* Threads
* Scheduling
* Synchronization
* Deadlocks
* Memory Management
* File Systems
* System Calls
* Virtual Memory
* IPC

---

## Part 7 — Networking

### Fundamentals

* OSI
* TCP/IP
* IP
* Ports
* DNS
* NAT

### Transport

* TCP
* UDP
* QUIC

### Security

* TLS
* HTTPS

### Application

* HTTP (methods, status codes, headers, caching, cookies)
* CORS
* REST
* GraphQL
* JSON-RPC
* WebSockets
* gRPC
* MQTT
* SSE

### Delivery

* Load Balancing (L4/L7)
* Reverse Proxies
* CDN & Edge

---

## Part 8 — Databases

### SQL

* PostgreSQL
* MySQL

Topics

* Schema Design
* Indexing
* ACID
* Transactions
* Isolation Levels
* Normalization
* Query Planning / EXPLAIN
* Connection Pooling
* Migrations

### NoSQL

* MongoDB
* Cassandra
* DynamoDB

### Cache

* Redis

### Search

* Elasticsearch

### Graph

* Neo4j

### Vector

* Qdrant
* Milvus

---

## Part 9 — Distributed Systems

* CAP
* Consistency
* Consensus
* Raft
* Paxos
* Replication
* Sharding
* Partitioning
* Event Sourcing
* CQRS
* Distributed Locks
* Gossip
* Leader Election

---

## Part 10 — Data Engineering

* ETL / ELT
* Batch vs Stream Processing
* Data Lakes & Warehouses
* Data Pipelines & Orchestration (Airflow-style)
* Schema Evolution

---

## Part 11 — Cloud & Ops

* Docker
* Kubernetes
* Helm
* Terraform
* IaC State & Config Drift
* CI/CD
* GitHub Actions
* Observability (Logs, Metrics, Traces — the three pillars)
* OpenTelemetry
* Cost Awareness

---


> Goal: Everything beyond writing code that ships and survives production.

* Professional Git Workflow
* Monorepos
* Dependency Injection
* Testing Pyramid
* CI/CD
* Packaging
* Release Engineering (feature flags, blue-green, canary)
* Code Reviews
* Static Analysis
* Performance Engineering
* Security & Threat Modeling
* Licensing & OSS Compliance
* API Design & Versioning
* Documentation
* Observability
* Incident Response (on-call, postmortems, production debugging)

---


> Goal: Design clean, correct, maintainable components. Requires Volume 2.

* OOP
* SOLID
* Design Principles
* GoF Patterns
* UML
* Clean Architecture
* Hexagonal
* DDD
* Repository Pattern
* Event Bus
* CQRS
* Concurrency Patterns
* Thread Safety & Race Conditions
* Resilience Patterns (idempotency, retries, backoff, circuit breakers)

---

**Exit criteria:** Implement **30+ production-quality components**.


> Goal: Design systems that scale and stay reliable. Requires Volume 1 (Parts 7–9) and Volume 3.

* Capacity Planning
* Scalability
* Reliability
* Distributed Systems Patterns
* Load Balancing
* Caching
* Rate Limiting / Throttling / Backpressure
* Message Queues & Streaming (Kafka, SQS, pub/sub)
* Service Mesh
* Database Scaling
* Event-Driven Systems
* CDN / Edge / Geo-Distribution
* Multi-Tenancy
* Disaster Recovery (backups, RTO/RPO)
* Security
* Cost & Capacity Economics
* Cloud Architecture

---

**Exit criteria:** Design **30+ real-world systems**.

# Volume 5 — AI Systems Engineering

> Goal: Where all previous knowledge converges. Requires Volume 0 (linear algebra, probability) and Volume 1.5 (encoding).

### Foundations

* LLM Internals
* Tokenization
* Transformers
* Inference
* Quantization

### Adapting Models

* Prompt Engineering
* Fine-Tuning / LoRA / PEFT
* RLHF / Alignment
* Structured Output / Function Calling / Tool Use

### Retrieval

* RAG
* Embeddings
* Chunking Strategies
* Reranking
* Vector Databases
* Context Management

### Agents

* Agent Frameworks
* Agent Memory
* MCP
* A2A
* Multi-Agent Systems

### Ops & Quality

* AI Observability
* Evaluation (LLM-as-judge, golden datasets, offline vs online)
* Cost & Latency Optimization (caching, batching, streaming)
* Guardrails
* AI Security (prompt injection, jailbreaks, data exfiltration)

### Infrastructure

* Model Serving
* GPU Infrastructure

---

## Progressive Builds

1. AI Chatbot
2. RAG Platform
3. AI Coding Assistant
4. AI Workflow Engine
5. Voice Agent
6. Multi-Agent Framework (similar to Pi Mono Agents)
7. AI Operating System

---

# Guide

A mastery roadmap — from computer science foundations to AI systems engineering — organized as six volumes and delivered as 100–120 single-concept chapters.

Start at **[roadmap.md](roadmap.md)** for the index, prerequisite ordering, and per-volume exit criteria.

# Mastery Roadmap

> Structure: six **volumes**, each complete enough that finishing it means you genuinely master the area. Delivered as **100–120 chapters**, one concept each, with prerequisites, diagrams, examples, exercises, a mini project, real open-source references, interview questions, and a checklist.

## Volumes

| # | Volume | File |
|---|--------|------|
| 0 | Math & Mental Models | [volumes/volume-0-math.md](volumes/volume-0-math.md) |
| 1 | Computer Science Foundations | [volumes/volume-1-cs-foundations.md](volumes/volume-1-cs-foundations.md) |
| 2 | Software Engineering | [volumes/volume-2-software-engineering.md](volumes/volume-2-software-engineering.md) |
| 3 | Low-Level Design | [volumes/volume-3-low-level-design.md](volumes/volume-3-low-level-design.md) |
| 4 | High-Level Design | [volumes/volume-4-high-level-design.md](volumes/volume-4-high-level-design.md) |
| 5 | AI Systems Engineering | [volumes/volume-5-ai-systems.md](volumes/volume-5-ai-systems.md) |

---


* **Volume 0** → gates Vol 1 Part 4 (algorithms) and *all* of Vol 5.
* **Vol 1 Part 1–3** → everything.
* **Vol 1 Part 5–6** (architecture, OS) → Vol 1 Part 9 (distributed) and Vol 4.
* **Vol 1 Part 7–8** (networking, DB) → Vol 4 (HLD).
* **Vol 1 Part 10** (data engineering) → Vol 5 retrieval + training data.
* **Vol 3** (LLD) → Vol 4 (HLD).
* **Vol 0.4** (linear algebra) + **Vol 1.5** (encoding) → Vol 5 foundations.

Each chapter declares its own prerequisites explicitly; treat the above as the volume-level skeleton.

## Chapter format

Each of the 100–120 chapters:

* teaches exactly one concept,
* has prerequisites,

> **Chapters 1–9.**

---

## Chapter 1 — Logic & Boolean Algebra

**Concept:** Propositional logic, truth tables, De Morgan's laws; how boolean algebra maps to `and`/`or`/`not` and bitwise operators.

**Prereqs:** none.

**Diagram:** Truth tables for AND/OR/NOT/XOR, plus a Venn diagram of De Morgan's `¬(A∧B) = ¬A∨¬B`.

**Example:** `assert (not (a and b)) == (not a or not b)` — De Morgan.

**Exercises:** (1) Build the truth table for `(A → B) ∧ ¬B` and show it forces `¬A` (modus tollens). (2) Simplify `¬(¬A ∨ (B ∧ ¬C))` to a form using only AND and NOT.

**Mini project:** A boolean-expression simplifier that reduces small expressions via De Morgan and distributivity.

**Open source:** [`sympy/sympy`](https://github.com/sympy/sympy) — the `sympy.logic` module.

**Interview:** "Why does `x & (x - 1) == 0` test for a power of two?" / "Prove De Morgan's laws with a truth table."

**Checklist:** ☐ derive every gate from NAND alone ☐ negate a compound condition correctly ☐ know short-circuit evaluation order ☐ convert `if/else` chains into boolean expressions

---

## Chapter 2 — Sets, Relations & Functions

**Concept:** Sets, subsets, unions/intersections/differences, Cartesian products; relations (reflexive/symmetric/transitive); functions (injective/surjective/bijective).

**Prereqs:** Ch 1.

**Diagram:** Two overlapping sets + an arrow diagram of a function mapping domain → codomain.

**Example:** `set("mississippi")` → `{'m','i','s','p'}`; a bijection maps each key to one value.

**Exercises:** (1) Prove `|A ∪ B| = |A| + |B| − |A ∩ B|`. (2) Which relation properties does "divides" have on integers?

**Mini project:** A set-operations calculator with a visualization of two overlapping sets.

**Open source:** [`python/cpython`](https://github.com/python/cpython) — Python's built-in `set`/`frozenset`.

**Interview:** "What's the difference between a function and a relation?" / "Give an example of a relation that's symmetric but not transitive."

**Checklist:** ☐ state the inclusion-exclusion principle ☐ classify a relation's properties ☐ explain why hash sets give O(1) membership

---

## Chapter 3 — Combinatorics & Counting

**Concept:** Permutations, combinations, the multiplication/addition rules, binomial coefficients, pigeonhole principle.

**Prereqs:** Ch 1.

**Diagram:** A decision tree showing n·(n−1)·… choices for permutations.

**Example:** `math.comb(10, 3) == 120` — choosing 3 from 10 without order.

**Exercises:** (1) How many distinct words can be made from the letters of "BANANA"? (2) Prove that among 13 people, two share a birth month (pigeonhole).

**Mini project:** A password-strength estimator that computes the size of the search space.

**Open source:** [`scipy/scipy`](https://github.com/scipy/scipy) — `scipy.special.comb`.

**Interview:** "How many unique orderings of a deck of 52 cards?" / "Explain the pigeonhole principle with an example."

**Checklist:** ☐ know when order matters ☐ compute permutations with duplicates ☐ apply the pigeonhole principle

---

## Chapter 4 — Graph Theory Foundations

**Concept:** Vertices, edges, directed vs undirected, degree, paths/cycles, connectivity, trees (n−1 edges, acyclic).

**Prereqs:** Ch 2.

**Diagram:** A small graph with labels for degree, a path, a cycle, and a spanning tree.

**Example:** `G = {0:{1,2}, 1:{0,2}, 2:{0,1}}` — an undirected triangle.

**Exercises:** (1) Prove a tree with n vertices has n−1 edges. (2) Show the handshaking lemma: sum of degrees = 2·|E|.

**Mini project:** A graph class with degree, path-existence, and cycle-detection helpers.

**Open source:** [`networkx/networkx`](https://github.com/networkx/networkx).

**Interview:** "What's the difference between a path and a walk?" / "When is a graph a tree?"

**Checklist:** ☐ state the handshaking lemma ☐ detect a cycle ☐ explain connectivity vs biconnectivity

---

## Chapter 5 — Proof by Induction

**Concept:** Base case + inductive step; strong induction; using induction to prove loop invariants and recursion correctness.

**Prereqs:** Ch 1.

**Diagram:** A domino-chain drawing: first domino falls, and each topples the next.

**Example:** Prove `1+2+…+n = n(n+1)/2`: base n=1, then assume for k and add k+1.

**Exercises:** (1) Prove `2^n > n` for all n ≥ 1. (2) Prove a binary tree of height h has at most `2^h − 1` nodes.

**Mini project:** A recursive factorial/power function with a written inductive proof of correctness.

**Open source:** [`leanprover/lean4`](https://github.com/leanprover/lean4) — theorem prover, induction is the core tool.

**Interview:** "Prove by induction that the sum of the first n odd numbers is n²." / "What's strong induction vs weak?"

**Checklist:** ☐ identify base case ☐ write the inductive step ☐ use induction to justify a loop invariant

---

## Chapter 6 — Asymptotic Notation (Big-O, Θ, Ω)

**Concept:** Big-O (upper bound), Ω (lower bound), Θ (tight); growth classes (1, log n, n, n log n, n², 2ⁿ); worst vs average vs best case.

**Prereqs:** Ch 3.

**Diagram:** A graph of growth curves crossing at some n₀, with f(n) shaded under c·g(n).

**Example:** A loop over n items doing O(1) work each is O(n); a nested loop is O(n²).

**Exercises:** (1) Classify `3n² + 100n + 7` as Θ(n²) with witnesses c and n₀. (2) Order `log n, n log n, 2ⁿ, n², √n` by growth.

**Mini project:** A tiny benchmark script that plots measured runtime vs n and fits the Big-O curve.

**Open source:** [`sympy/sympy`](https://github.com/sympy/sympy) — `sympy.series.Order`.

**Interview:** "What's the difference between O(n) and Ω(n)?" / "Is O(log n) always faster than O(n)?"

**Checklist:** ☐ give formal c/n₀ witnesses ☐ rank common growth classes ☐ distinguish worst/average case

---

## Chapter 7 — Time/Space Complexity & Amortized Analysis

**Concept:** Counting operations; space complexity incl. recursion stack; amortized cost via aggregate/accounting (dynamic-array doubling).

**Prereqs:** Ch 6.

**Diagram:** A dynamic array's doubling steps drawn as a staircase of copies totaling O(n).

**Example:** Python list `append` is amortized O(1) — occasional O(n) reallocations average out.

**Exercises:** (1) Show that n pushes on a doubling vector cost O(n) total. (2) Compute the space complexity of a recursive DFS (stack depth).

**Mini project:** Implement a doubling dynamic array and instrument the number of element copies across n appends.

**Open source:** [`python/cpython`](https://github.com/python/cpython) — `list` growth strategy in `listobject.c`.

**Interview:** "Why is hash table insertion 'amortized' O(1)?" / "Explain amortized analysis with a bank-account argument."

**Checklist:** ☐ do aggregate amortized math ☐ count auxiliary space ☐ explain why amortized ≠ average-case

---

## Chapter 8 — Probability, Distributions & Bayes

**Concept:** Sample spaces, independence, expectation, variance, common distributions (uniform, binomial, normal), Bayes' theorem.

**Prereqs:** Ch 3.

**Diagram:** A Bayes two-branch tree: P(A|B) computed from P(B|A), P(A), P(B).

**Example:** `P(disease|positive) = P(positive|disease)·P(disease) / P(positive)` — the classic false-positive trap.

**Exercises:** (1) Compute expectation of a fair six-sided die. (2) A test is 99% accurate, disease prevalence 1% — what's P(disease|positive)?

**Mini project:** A Monte Carlo simulation of a false-positive diagnosis and a die-roll expectation.

**Open source:** [`numpy/numpy`](https://github.com/numpy/numpy) — `numpy.random`.

**Interview:** "Explain Bayes' theorem in plain words." / "What's the difference between expectation and variance?"

**Checklist:** ☐ compute expectation/variance ☐ apply Bayes to a real example ☐ recognize independence vs conditional dependence

---

## Chapter 9 — Linear Algebra for AI

**Concept:** Vectors, vector spaces, matrices & operations, dot product as similarity, eigenvalues/eigenvectors (intuition), gradients & derivatives as the engine of backprop.

**Prereqs:** Ch 2, Ch 8.

**Diagram:** Two vectors with the angle showing dot-product similarity; a matrix as a linear transformation of space.

**Example:** `cosine = (a @ b) / (norm(a) * norm(b))` — similarity used everywhere in embeddings.

**Exercises:** (1) Compute a dot product by hand and interpret the sign. (2) Compute the gradient of `f(x)=x²` and `f(x,y)=x²+y²` at a point.

**Mini project:** A 2D embedding visualizer that computes cosine similarity and nearest neighbors for a small vector set.

**Open source:** [`numpy/numpy`](https://github.com/numpy/numpy) and [`pytorch/pytorch`](https://github.com/pytorch/pytorch) (`torch.autograd`).

**Interview:** "Why does the dot product measure similarity?" / "What does an eigenvector represent?"

**Checklist:** ☐ multiply matrices correctly ☐ explain dot-product similarity ☐ state what a gradient tells you ☐ intuit eigenvalues as scaling directions

---

**Exit criteria:** Solve a set of Big-O, probability, and linear-algebra problems from scratch.
