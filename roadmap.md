# Mastery Roadmap

> Structure: five **volumes**, each complete enough that finishing it means you genuinely master the area. Delivered as **100–120 chapters**, one concept each, with prerequisites, diagrams, examples, exercises, a mini project, real open-source references, interview questions, and a checklist.

> Volume 0 is a hard prerequisite gate. Don't start Volume 1 Part 4 (algorithms) or any of Volume 5 (AI) without it.

---

# Volume 0 — Math & Mental Models

> Goal: The math the rest of the book silently assumes. Load-bearing for algorithms (Vol 1.4) and all of AI (Vol 5).

## Part 0.1 — Discrete Math

* Logic & Boolean Algebra
* Sets, Relations, Functions
* Combinatorics & Counting
* Graph Theory (foundations)
* Proof by Induction

## Part 0.2 — Complexity

* Asymptotic Notation (Big-O, Θ, Ω)
* Time vs Space Complexity
* Amortized Analysis

## Part 0.3 — Probability & Statistics

* Probability Basics
* Distributions
* Expectation & Variance
* Bayes' Theorem
* Sampling & Estimation

## Part 0.4 — Linear Algebra (for AI)

* Vectors & Vector Spaces
* Matrices & Operations
* Dot Products & Similarity
* Eigenvalues / Eigenvectors (intuition)
* Gradients & Derivatives (calculus intuition for backprop)

---

# Volume 1 — Computer Science Foundations

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
* **Character Encoding (ASCII, Unicode, UTF-8)**

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
* **Regular Expressions**

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

* **Floating Point / IEEE-754**
* **Integer Overflow & Signedness**
* **Date, Time & Timezones**

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
* **Secrets Management**

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

## Part 4 — Data Structures & Algorithms

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
* **Isolation Levels**
* Normalization
* **Query Planning / EXPLAIN**
* **Connection Pooling**
* **Migrations**

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

# Volume 2 — Software Engineering

This becomes much deeper.

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

# Volume 3 — Low-Level Design

Everything related to:

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

Then implement **30+ production-quality components**.

---

# Volume 4 — High-Level Design

Everything related to:

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

Then design **30+ real-world systems**.

---

# Volume 5 — AI Systems Engineering

This is where all previous knowledge converges. (Requires Volume 0 math.)

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

Then build progressively:

1. AI Chatbot
2. RAG Platform
3. AI Coding Assistant
4. AI Workflow Engine
5. Voice Agent
6. Multi-Agent Framework (similar to Pi Mono Agents)
7. AI Operating System

---

# Prerequisite Ordering

The volumes are **not** strictly linear. Key cross-volume dependencies:

* **Volume 0** → gates Vol 1 Part 4 (algorithms) and *all* of Vol 5.
* **Vol 1 Part 1–3** → everything.
* **Vol 1 Part 5–6** (architecture, OS) → Vol 1 Part 9 (distributed) and Vol 4.
* **Vol 1 Part 7–8** (networking, DB) → Vol 4 (HLD).
* **Vol 1 Part 10** (data engineering) → Vol 5 retrieval + training data.
* **Vol 3** (LLD) → Vol 4 (HLD).
* **Vol 0.4** (linear algebra) + **Vol 1.5** (encoding) → Vol 5 foundations.

Each chapter declares its own prerequisites explicitly; treat the above as the volume-level skeleton.

---

# Exit Criteria (per volume)

* **Vol 0** — Solve a set of Big-O, probability, and linear-algebra problems from scratch.
* **Vol 1** — Build one non-trivial CLI/service touching files, network, and a database.
* **Vol 2** — Ship a project with full CI/CD, tests, observability, and a postmortem for one induced failure.
* **Vol 3** — 30+ production-quality components.
* **Vol 4** — 30+ real-world system designs.
* **Vol 5** — The 7 progressive builds, ending at the AI Operating System.

---

## Chapter format

Each of the 100–120 chapters:

* teaches exactly one concept,
* has prerequisites,
* includes diagrams,
* provides simple examples,
* includes coding exercises,
* has a mini project,
* points to real open-source code,
* ends with interview questions and a checklist.
