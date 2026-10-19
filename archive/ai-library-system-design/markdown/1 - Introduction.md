# Mastering System Design: From Basics to Cracking Interviews

*By Charikshith*

---

Welcome to your journey in **Mastering System Design**! Whether you're new to the topic or preparing for tough interviews, this guide will help you build a rock-solid foundation and give you the tools to design robust, scalable systems.

System design is a cornerstone skill for software engineers, architects, and anyone building large-scale, robust software solutions. It is often viewed through the narrow lens of interview preparation — but its true value lies in being able to architect real-world solutions effectively. In this chapter, we'll break down what system design is, why it has become so crucial in the tech industry, how it has evolved, and practical ways to master it.

---

## 1.1 Learning Outcomes

After reading this chapter, you will be able to:

1. Define what system design is and explain why it matters beyond interviews.
2. Distinguish **functional** from **non-functional** requirements and name the most common non-functional dimensions (latency, throughput, availability, durability, scalability, consistency, security, maintainability, observability, cost).
3. Apply the **4-step design framework** (Requirements → Estimate → High-Level Design → Tech Decisions) to a new problem.
4. Reason about latency intuitively using the **"numbers every programmer should know"** reference table.
5. Recognize common beginner anti-patterns (premature scaling, cargo-cult architecture, distributed monolith).

---

## 1.2 Prerequisites

Before starting, you should be comfortable with:

- Basic programming in any language (Python, JavaScript, Java, Go, etc.).
- How a web request/response works at a high level (browser → server → response).
- Basic command-line usage (helpful, not required: only a few commands such as `curl` appear, and each is explained where it is used).

That is all. **SQL and databases, how a computer stores data, and hashing/encryption are taught from scratch** in *Start Here: Primers for Beginners* below, so you do not need them beforehand.

You **don't need** prior distributed-systems experience, prior cloud experience, or to have used Kubernetes/Kafka/Redis. Every term will be defined as it appears.

---

## 1.3 How to Use This Course

- **Foundations (Chapters 1–15):** Read in order. Each chapter builds on the previous.
- **Case studies (Chapters 16–28):** Read in any order after the foundations. Each is self-contained.
- **Expect to revisit.** Caching only fully clicks after you've seen it used in three different case studies. That's normal.
- **Build a toy project alongside.** A blog, a URL shortener, a chat app — anything. Reading without building is like reading swimming books on dry land.
- **Read real post-mortems.** [danluu.com/postmortem-lessons](https://danluu.com/postmortem-lessons/) is the best curated list. Real failures teach more than any textbook.
- **Pace:** Each foundational chapter takes 1–2 hours to read carefully. Case studies take 30–60 minutes.

### 1.3.1 Tools You'll See in This Course

- **Diagramming:** [Mermaid](https://mermaid-js.github.io/) (renders in GitHub/most Markdown viewers), [Excalidraw](https://excalidraw.com/), [draw.io](https://app.diagrams.net/).
- **API testing:** [Postman](https://www.postman.com/), `curl`.
- **Load testing:** [`wrk`](https://github.com/wg/wrk), [`k6`](https://k6.io/), [JMeter](https://jmeter.apache.org/), [Locust](https://locust.io/).
- **Observability:** [Prometheus](https://prometheus.io/), [Grafana](https://grafana.com/), [Jaeger](https://www.jaegertracing.io/), Datadog, New Relic.

You don't need to install any of these now — they'll be introduced where used.

---

## 1.4 Start Here: Primers for Beginners

> **New to this?** Read these three short primers first. They teach the few ideas that later chapters use all the time: how a computer stores data, what a database and SQL are, and what hashing, encryption and signing mean. Already comfortable with all three? Skip to the next section.
>
> Each primer ends with a pointer to the chapter that goes deeper.

### 1.4.1 Primer A: How a Computer Stores and Processes Data

Every system you will design runs on real machines, and their physical limits explain most design choices later in the course.

#### 1.4.1.1 Bits, Bytes and Sizes

- A **bit** is a single 0 or 1. A **byte** is 8 bits and holds one character of plain text, such as the letter `A`.
- Sizes grow by roughly a factor of 1,000 at each step:

| Unit | Size | A feel for it |
|------|------|---------------|
| KB (kilobyte) | about 1,000 bytes | a short text file |
| MB (megabyte) | about 1,000 KB | a photo, a minute of music |
| GB (gigabyte) | about 1,000 MB | a movie, the RAM of a phone |
| TB (terabyte) | about 1,000 GB | a large hard drive |
| PB (petabyte) | about 1,000 TB | what a big company stores |

#### 1.4.1.2 The Four Parts That Matter

| Part | Job | Speed | Size | Survives power-off? |
|------|-----|-------|------|---------------------|
| **CPU** | executes instructions; modern chips have several **cores** that work in parallel | n/a | n/a | n/a |
| **CPU cache** | tiny memory on the chip that holds what the CPU is using right now | fastest | kilobytes to megabytes | no |
| **RAM** (memory) | the working space for running programs and their data | very fast | gigabytes | **no** (volatile) |
| **Disk** (SSD or hard drive) | long-term storage for files and databases | much slower | hundreds of GB to TB | **yes** (non-volatile) |

The **motherboard** is the circuit board that connects all of these. A program starts as **source code**, which a *compiler* or *interpreter* turns into the machine instructions the CPU executes.

#### 1.4.1.3 Why Speed Differences Matter

Each step down the list is roughly 100 to 1,000 times slower than the one above it. Rough orders of magnitude:

| Operation | Rough time |
|-----------|-----------|
| Read from CPU cache | about 1 nanosecond |
| Read from RAM | about 100 nanoseconds |
| Read from an SSD | about 100 microseconds |
| Read from a hard drive | about 10 milliseconds |
| Network round trip inside one data center | about 0.5 milliseconds |

(1 millisecond = 1,000 microseconds = 1,000,000 nanoseconds. See "Numbers Every Programmer Should Know" later in this chapter.)

**Throughput matters too (rough figures).** A hard drive moves about 80 to 160 MB per second; a solid-state drive about 500 to 3,500 MB per second (SSDs cost more per GB); RAM moves many thousands of MB per second, faster than any SSD. Capacities run the other way: disks hold hundreds of GB to several TB, RAM a few GB to hundreds of GB on a large server, and the CPU cache only a few MB.

**The cache hierarchy.** The CPU keeps tiny, very fast caches on the chip: **L1** (smallest and fastest, one per core), **L2**, and **L3** (larger, shared between cores). To read a value the CPU looks in L1, then L2, then L3, then RAM, and only then goes to disk; finding it early is a **cache hit** and missing is a **cache miss**. The same idea, keeping a copy of popular data in a faster place, appears all through this course.

**What this means for system design:**

- Data in RAM is fast but disappears when power is lost, so anything that must survive goes to disk. This is why **databases write to disk** and **caches live in RAM**.
- A **cache** is simply a copy of popular data kept in a faster place so it need not be fetched from a slower one.
- One machine has limits: a fixed number of CPU cores, a fixed amount of RAM, a fixed disk size. When you outgrow them you buy a bigger machine (**vertical scaling**) or add more machines (**horizontal scaling**). Chapter 6 covers this.

*Goes deeper in:* Chapter 6 (scalability), Chapter 7 (storage categories), Chapter 8 (caching).

### 1.4.2 Primer B: Databases and SQL in Ten Minutes

A **database** is software that stores data so it can be found, changed and protected. The most common kind is **relational**: data lives in **tables**, and the language used to ask questions is **SQL** (Structured Query Language). MySQL, PostgreSQL, SQL Server, Oracle and SQLite all speak it.

#### 1.4.2.1 Tables, Rows and Columns

A table is like a spreadsheet with a fixed set of columns. Each **row** is one record. Each **column** has a **data type**, so a number column cannot hold text.

```sql
CREATE TABLE customers (
  id    INTEGER PRIMARY KEY,
  name  VARCHAR(100) NOT NULL,
  city  VARCHAR(100),
  email VARCHAR(255) UNIQUE
);
```

The **schema** is the blueprint: which tables exist, their columns and types, and how they relate.

#### 1.4.2.2 Keys and Relationships

- A **primary key** uniquely identifies each row (`customers.id`).
- A **foreign key** stores another table's primary key, which is how rows point at each other (`orders.customer_id` points to `customers.id`).

| Relationship | Meaning | Example |
|--------------|---------|---------|
| One-to-one | one row matches exactly one row | user and profile |
| One-to-many | one row matches many rows | one customer, many orders |
| Many-to-many | many rows match many rows, via a **junction table** | orders and products |

#### 1.4.2.3 The Four Everyday Operations

```sql
INSERT INTO customers (id, name, city) VALUES (1, 'Asha', 'Pune');   -- create
SELECT name, city FROM customers WHERE city = 'Pune';                  -- read
UPDATE customers SET city = 'Delhi' WHERE id = 1;                      -- update
DELETE FROM customers WHERE id = 1;                                    -- delete
```

`WHERE` chooses which rows are affected. **Always write the `WHERE` on an `UPDATE` or `DELETE`; without it every row is changed.**

#### 1.4.2.4 Combining Tables and Summarising

A **join** combines rows from two tables where their keys match:

```sql
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

`INNER JOIN` keeps only rows that match on both sides. `LEFT JOIN` keeps every row of the left table and fills the missing right-hand values with `NULL` (meaning "unknown").

`GROUP BY` plus an aggregate such as `COUNT`, `SUM` or `AVG` summarises many rows into one per group:

```sql
SELECT city, COUNT(*) AS customers
FROM customers
GROUP BY city;
```

#### 1.4.2.5 Indexes: Why Some Queries Are Fast

Without help, finding `city = 'Pune'` makes the database read **every row** (a *full table scan*). An **index** is a separate sorted lookup structure, like the index at the back of a book, that lets it jump straight to the matches.

```sql
CREATE INDEX idx_customers_city ON customers (city);
```

The trade-off: an index takes disk space and slows down writes, because every insert and update must also update it.

#### 1.4.2.6 Transactions

A **transaction** groups several statements so that **all of them succeed or none of them do**, such as moving money between two accounts:

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

If anything fails midway, the database undoes the first step, so money is never lost or created.

*Goes deeper in:* Chapter 7 (SQL vs NoSQL, ACID, replication, sharding) and Chapter 8 (indexing and query optimisation).

### 1.4.3 Primer C: Hashing, Encryption and Signing

Security vocabulary shows up from the networking chapter onward, so here are the three ideas in plain terms. They are often confused, and the differences matter.

| | **Hashing** | **Encryption** | **Signing** |
|--|-------------|----------------|-------------|
| What it does | turns any input into a fixed-size "fingerprint" | scrambles data so only a key holder can read it | proves who created data and that it was not altered |
| Reversible? | **no** (one-way) | **yes**, with the right key | not applicable: you *verify*, you do not decrypt |
| Needs a key? | no | yes | yes (a private key to sign, a public key to verify) |
| Same input gives | the same output every time | different output if you use random parts | a signature that only matches the original data |
| Typical use | store passwords, check file integrity, spread requests across servers | keep traffic and stored data private | prove a token or message is genuine |

#### 1.4.3.1 Hashing

```python
import hashlib
hashlib.sha256(b"hello").hexdigest()
# '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
```

A one-letter change in the input gives a completely different output, and you cannot work backwards from the output to the input. Uses you will meet later: password storage, checking that a file was not corrupted, and **IP hashing** or **consistent hashing**, where a hash decides which server handles a request.

> **Passwords:** never store them in plain text and never use encryption for them. Store a **slow, salted hash** (bcrypt, scrypt or Argon2). A *salt* is a random value added to each password so identical passwords produce different hashes.

#### 1.4.3.2 Encryption

- **Symmetric** encryption uses one shared key for both locking and unlocking. It is fast, so it protects bulk data.
- **Asymmetric** encryption uses a **key pair**: a public key that anyone may have and a private key kept secret. What one key locks, only the other opens. It is slower and mostly used to exchange a symmetric key safely.

**TLS** (the "S" in **HTTPS**) combines both: asymmetric cryptography sets up a secure channel, then symmetric encryption protects the traffic. That padlock in the browser means the data between you and the server is encrypted and the server's identity was checked against a **certificate**.

#### 1.4.3.3 Signing

To sign, the sender computes a hash of the data and encrypts it with their **private key**. Anyone with the matching **public key** can check that the data came from the sender and was not changed. **JSON Web Tokens (JWT)**, which you will meet in the web and security chapters, work this way.

#### 1.4.3.4 Three Things People Mix Up

- **Encoding is not encryption.** Base64 only changes the data's format; anyone can reverse it. It protects nothing.
- **Hashing is not encryption.** You cannot get a hash back to the original.
- **Do not invent your own cryptography.** Use well-tested libraries and standard algorithms.

*Goes deeper in:* Chapter 3 (HTTPS), Chapter 5 (sessions, JWT, CORS) and Chapter 10 (security).

---

## Table of Contents

- [1.4 Start Here: Primers for Beginners](#14-start-here-primers-for-beginners)
- [1.5 What is System Design?](#15-what-is-system-design)
- [1.6 Why System Design Matters](#16-why-system-design-matters)
- [1.7 Functional vs. Non-Functional Requirements](#17-functional-vs-non-functional-requirements)
- [1.8 Numbers Every Programmer Should Know](#18-numbers-every-programmer-should-know)
- [1.9 The Evolution of System Design (1995–Present)](#19-the-evolution-of-system-design-1995present)
- [1.10 Course Structure](#110-course-structure)
- [1.11 The 4-Step Design Framework](#111-the-4-step-design-framework)
- [1.12 Worked Example: A URL Shortener](#112-worked-example-a-url-shortener)
- [1.13 Architectural Patterns: A Preview](#113-architectural-patterns-a-preview)
- [1.14 Communication & Load Balancing: A Preview](#114-communication--load-balancing-a-preview)
- [1.15 Performance Boosters](#115-performance-boosters)
- [1.16 Security Essentials](#116-security-essentials)
- [1.17 Common Beginner Anti-Patterns](#117-common-beginner-anti-patterns)
- [1.18 Tips and Tricks for Mastering System Design](#118-tips-and-tricks-for-mastering-system-design)
- [1.19 Navigating This Course Effectively](#119-navigating-this-course-effectively)
- [1.20 Further Reading](#120-further-reading)
- [1.21 Conclusion](#121-conclusion)

---

## 1.5 What is System Design?

> **System Design is the process of defining the architecture, components, modules, interfaces, and data flow for a system to meet specific requirements.**

System design is much more than just drawing boxes and arrows on a whiteboard — it's about making critical high-level decisions that determine not only how a system works, but also how it scales, performs, and remains reliable and maintainable.

> "System design isn't just about diagrams. It's about thinking through architecture — making trade-offs that impact both functional and non-functional requirements like scalability, reliability, performance, and maintainability."

You'll encounter system design in real-world applications like scalable web apps, distributed systems, databases, and cloud infrastructures.

### 1.5.1 Key Aspects of System Design

- **Architecture:** Overall structure, including how components interact — Monoliths, microservices, serverless, etc.
- **Components / Modules:** The building blocks — Databases, caches, message queues, etc.
- **Interfaces:** How different parts of the system communicate — REST APIs, gRPC, GraphQL.
- **Data Flow:** How information travels through and between components.
- **Scalability:** Can the system handle a growing number of users?
- **Reliability & Performance:** Can the system recover from failure and remain fast?
- **Maintainability:** How easy is it to update or fix the system?

### 1.5.2 A First Look: High-Level Architecture

A classic web application architecture, showing how a load balancer distributes traffic to multiple servers that use caching and a database to serve requests efficiently:

```mermaid
graph TD
    User[User]
    LB[Load Balancer]
    WS[Web Servers]
    Cache["Cache (Redis/Memcached)"]
    DB[("Database (SQL/NoSQL)")]
    MQ[Message Queue]
    SVC[Microservices]

    User --> LB
    LB --> WS
    WS --> Cache
    WS --> SVC
    SVC --> DB
    WS --> MQ
    MQ --> SVC
```

**Explanation of the components:**

- **Load Balancer:** Distributes traffic to web servers.
- **Cache:** Stores frequently accessed data to reduce database load.
- **Microservices:** Modularize business logic.
- **Database:** Stores persistent data.
- **Message Queue:** For asynchronous processing (e.g., order processing, emails).

A simpler view of the same architecture, showing the bidirectional relationship between cache and database:

```mermaid
flowchart TD
    User[User]
    LB[Load Balancer]
    App[Application Servers]
    Cache["Cache (Redis/Memcached)"]
    DB[("Database")]

    User --> LB
    LB --> App
    App --> Cache
    App --> DB
    Cache <--> DB
```

---

## 1.6 Why System Design Matters

Let's break down the core reasons, weaving in lecture material:

### 1.6.1 Scalability & Reliability

> *"Think about modern applications we use daily. These platforms handle millions, even billions of users without any problem. A good system design is crucial for such systems."*

A well-designed system ensures high availability, fault tolerance, and seamless scaling. Imagine a system that crashes during peak load — good design prevents this scenario.

**Example: Load Balancing**

```mermaid
flowchart LR
    Clients([Clients]) --> LB["Load balancer"]
    LB --> A1["App server 1"]
    LB --> A2["App server 2"]
    LB --> A3["App server 3"]
```


### 1.6.2 Architectural Thinking

> *"When you study system design, you are actually going beyond coding. You are thinking at an architectural level."*

This means making informed decisions and trade-offs, such as:

- SQL vs. NoSQL databases
- Microservices vs. Monolith architectures
- Consistency vs. Availability (CAP theorem)

**Trade-off Example: CAP Theorem**

```mermaid
flowchart TB
    CAP{{"CAP theorem: pick any two"}}
    CAP --> Cn["C: Consistency"]
    CAP --> Av["A: Availability"]
    CAP --> Pt["P: Partition tolerance"]
```


> **A nuance worth knowing:** the "pick any two" framing is the classic teaching, but in practice, network partitions in a distributed system are unavoidable — so P is essentially a given. The real choice you make during a partition is between **C and A**: do you serve stale data (favor availability) or refuse the request (favor consistency)? We'll dive deeper in Chapter 7 (Storage).

> **Vocabulary preview:** terms you'll see throughout this course before they're formally defined:
> - **Eventual consistency:** replicas converge to the same value *eventually*, not immediately. (Chapter 7)
> - **Idempotency:** processing the same request twice has the same effect as processing it once. Critical for retries. (Chapter 8)
> - **Consensus:** a group of nodes agreeing on a single value despite failures (Paxos, Raft). (Chapter 9)
> - **Backpressure:** a downstream system telling upstream to slow down to avoid being overwhelmed.
>
> Don't worry about mastering these now — just know the words exist.

### 1.6.3 Career Growth

> *"It is also important to become a senior level engineer or architect to focus on system design."*

Junior engineers focus on code; senior engineers design for scalability, maintainability, and system health. Mastery of system design is a must for tech leads and architects.

### 1.6.4 Real-World Problem Solving

> *"System design is about solving real-world engineering challenges and not just passing interviews."*

Memorizing patterns isn't enough. You must deeply understand *why* certain design choices are made. It enables you to design systems that solve actual business needs, not just interview questions.

### 1.6.5 Trade-Offs & Decision Making

> *"There is no such thing as a perfect system design. Only well-reasoned trade-offs are there in a good system design."*

You must balance scalability, cost, speed, and complexity. For example, the choice between SQL and NoSQL depends on your application's consistency and scalability needs.

### 1.6.6 Future-Proofing

> *"Poorly designed systems become bottlenecks over time. A well-designed system can adapt to growing traffic, new features and emerging technologies."*

Netflix and eBay, for instance, started with monolithic architectures but migrated to microservices as they scaled. A good design prevents bottlenecks and supports software evolution.

### 1.6.7 Cost

A system that "works" but costs $50K/month when it could have cost $5K is a failed design. Cloud bills are real, and architectural choices directly drive them:

- Choosing a fancy database when SQLite would do.
- Running 24/7 servers for workloads that could be serverless.
- Storing video in hot storage when 99% of it is rarely watched.

**Cost is a first-class design dimension.** Throughout this course, when we discuss trade-offs, cost will be one of them.

> **Note:** Many learners approach system design as an interview hurdle, but its true value is in building scalable, reliable, and efficient software. Master it for real-world impact, and interviews will naturally become easier.

> *"If you deeply understand system design principles, interviews will naturally become easier for you to crack. But more importantly, you will be able to architect real world solutions effectively."*

---

## 1.7 Functional vs. Non-Functional Requirements

You'll see these terms constantly. Pin them down now:

| Type           | Question it answers          | Examples                                              |
|----------------|------------------------------|--------------------------------------------------------|
| **Functional** | *What does the system do?*   | "Users can shorten a URL", "Send email on signup", "Show recommended videos" |
| **Non-functional** | *How well does it do it?* | "p99 latency < 100ms", "99.99% uptime", "10K req/sec", "Encrypt all PII" |

> **Rule of thumb:** if removing the requirement still gives you a *working* system that's just slower, less reliable, or more expensive, it's non-functional.

### 1.7.1 The Common Non-Functional Requirements

These ten are the "dimensions" along which every system can be measured. Every real-world system has to make trade-offs between them.

| Dimension          | What it measures                                                          | Common metric              |
|--------------------|---------------------------------------------------------------------------|----------------------------|
| **Latency**        | How long one request takes                                                | p50, p95, p99 in ms        |
| **Throughput**     | How many requests per unit time                                           | requests/sec, QPS, MB/s    |
| **Availability**   | % of time the system is up and serving                                    | 99.9% = "three nines"      |
| **Durability**     | Probability data is never lost once written                               | 11 nines (S3-style)        |
| **Scalability**    | Ability to grow to handle more load                                       | Linear vs. sub-linear cost |
| **Consistency**    | All readers see the same data at the same time                            | Strong / eventual          |
| **Security**       | Protection from unauthorized access, tampering                            | OWASP top 10 coverage      |
| **Maintainability**| How easy it is to change, debug, deploy                                   | Deploy frequency, MTTR     |
| **Observability**  | How easy it is to know what the system is doing                           | Logs, metrics, traces      |
| **Cost**           | Dollars per request, per user, per month                                  | $/req, $/user/mo           |

> **You cannot maximize all of these simultaneously.** Design *is* picking which ones matter most for your problem.

---

## 1.8 Numbers Every Programmer Should Know

This table is the single most important reference in this course. **Memorize the orders of magnitude.** They will let you reason about why caching helps, why a cross-region call is bad, why disk seek is to be avoided, and why "just put it in memory" works.

Adapted from Jeff Dean's classic talk:

| Operation                                  | Time                | Mental shorthand                 |
|--------------------------------------------|---------------------|----------------------------------|
| L1 cache reference                         | 0.5 ns              | basically free                   |
| Branch mispredict                          | 5 ns                |                                  |
| L2 cache reference                         | 7 ns                | 14× L1                           |
| Mutex lock/unlock                          | 25 ns               |                                  |
| Main memory reference                      | 100 ns              | 200× L1, 20× L2                  |
| Compress 1 KB with Snappy                  | 3,000 ns (3 µs)     |                                  |
| Send 2 KB over commodity network           | ~1,000 ns (1 µs)    |                                  |
| Read 1 MB sequentially from memory         | 250,000 ns (250 µs) |                                  |
| Round trip within same datacenter          | 500,000 ns (0.5 ms) | network within a datacenter      |
| Read 4 KB randomly from SSD                | 150,000 ns (150 µs) |                                  |
| Read 1 MB sequentially from SSD            | 1,000,000 ns (1 ms) |                                  |
| Disk seek                                  | 10,000,000 ns (10 ms) | always avoid if possible       |
| Read 1 MB sequentially from disk           | 20,000,000 ns (20 ms) |                                |
| Round trip CA → Netherlands → CA           | 150,000,000 ns (150 ms) | speed of light over fiber     |

### 1.8.1 What this means in practice

- **Memory is ~100× faster than SSD, ~100,000× faster than disk seek.** That's why caches exist.
- **Same-datacenter round trip (0.5 ms) is ~300× faster than cross-continent (150 ms).** That's why CDNs and regional replicas matter.
- **Compression often pays off:** 3 µs to compress vs. saving network/disk time later.
- **A modern API endpoint that takes >100 ms has spent most of its time on something *other* than CPU.** It's usually network or disk.

> **Whenever you propose a design, sanity-check it against this table.** If your design has 5 sequential cross-region calls in a hot path, your p99 is already ≥ 750 ms — no amount of code optimization will fix that.

---

## 1.9 The Evolution of System Design (1995–Present)

System design is not static — it has evolved rapidly over the last 25 years. Let's trace the journey, highlighting key architectural shifts and technologies. We'll look at it in three formats: a summary table, a timeline diagram, and an era-by-era deep dive with code samples.

### 1.9.1 Summary Table

| Era               | Key Trends                                       | Technologies & Patterns                                                               |
|-------------------|--------------------------------------------------|----------------------------------------------------------------------------------------|
| **1995–2005**     | Early monolithic web apps                        | LAMP stack, MVC, stateless servers, server-side rendering, single-node databases       |
| **2005–2010**     | Distributed systems, scaling challenges          | Caching (Memcached, Redis), CDNs, database replication, load balancing                 |
| **2010–2015**     | Cloud revolution                                 | AWS, Azure, GCP, virtualization, containers, NoSQL databases, on-demand scaling        |
| **2015–2020**     | Microservices & event-driven architectures       | API gateways, service meshes, event brokers (Kafka, RabbitMQ), CI/CD pipelines         |
| **2020–Present**  | Real-time, AI-driven & edge computing            | Serverless, Kubernetes, streaming, edge computing, observability, security, compliance |

### 1.9.2 Timeline Diagram

```mermaid
flowchart TB
    E1["1995-2005<br/><b>Monolithic apps</b><br/>LAMP, MVC, single-node DB"] --> E2["2005-2010<br/><b>Distributed systems</b><br/>caching, CDNs, replication"]
    E2 --> E3["2010-2015<br/><b>Cloud revolution</b><br/>AWS, containerization, NoSQL"]
    E3 --> E4["2015-2020<br/><b>Microservices</b><br/>API gateways, event-driven, CI/CD"]
    E4 --> E5["2020-present<br/><b>Real-time, edge, AI</b><br/>Kubernetes, serverless, observability"]
```

### 1.9.3 ASCII Timeline (for plain-text viewers)

```plaintext
1995-2005   2005-2010   2010-2015   2015-2020   2020+
|-----------|-----------|-----------|-----------|-----------|
Monolith    Distributed Cloud       Micro-      Real-time,
LAMP stack  Caching,    Revolution  services,   AI-driven,
MVC         Replication AWS, GCP,   Event       Edge,
            CDNs        NoSQL       Driven      Serverless
```

### 1.9.4 Era-by-Era Deep Dive

#### 1.9.4.1 1995–2005: Early Monolithic Web Applications

- **Stack:** LAMP (Linux, Apache, MySQL, PHP)
- **Architecture:** Monolithic — front-end, back-end, and DB bundled together
- **Features:** Stateless servers, server-side rendering, no real-time interactions

```mermaid
flowchart TD
    User -->|HTTP| WebServer
    WebServer --> AppLogic
    AppLogic --> Database
```

```php
<?php
echo "Hello, World!";
?>
```

#### 1.9.4.2 2005–2010: Distributed Systems & Scaling

- **Challenges:** Social media and e-commerce scale (Facebook, Amazon)
- **Solutions:** Caching (Memcached, Redis), CDNs, database replication, load balancers

```mermaid
flowchart TD
    User --> LoadBalancer
    LoadBalancer --> AppServer1
    LoadBalancer --> AppServer2
    AppServer1 & AppServer2 -->|Cache| Redis
    AppServer1 & AppServer2 --> Database
```

```python
import random

servers = ['app_server_1', 'app_server_2', 'app_server_3']

def handle_request(request):
    server = random.choice(servers)
    print(f"Forwarding {request} to {server}")
```

#### 1.9.4.3 2010–2015: The Cloud Revolution

- **Cloud Providers:** AWS, Azure, GCP
- **Deployment:** Virtualized, containerized (Docker)
- **Databases:** NoSQL (MongoDB, Cassandra)
- **Techniques:** Database sharding, on-demand scaling

```mermaid
flowchart TD
    User --> CloudLB
    CloudLB --> Container1
    CloudLB --> Container2
    Container1 & Container2 -->|Sharded| NoSQLDB
    subgraph CloudProvider
        CloudLB
        Container1
        Container2
        NoSQLDB
    end
```

```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

#### 1.9.4.4 2015–2020: Microservices & Event-Driven Architectures

- **Shift:** Monoliths → Microservices
- **Tech:** API gateways, service meshes, event brokers (Kafka, RabbitMQ)
- **Practices:** CI/CD pipelines

```mermaid
flowchart TD
    API_Gateway --> MS1[Microservice 1]
    API_Gateway --> MS2[Microservice 2]
    API_Gateway --> MS3[Microservice 3]
    MS1 -->|Events| Kafka
    MS2 -->|Events| Kafka
    MS3 -->|Events| Kafka
```

```js
const { Kafka } = require('kafkajs');
const kafka = new Kafka({ clientId: 'my-app', brokers: ['kafka1:9092'] });
const producer = kafka.producer();

async function sendMessage() {
  await producer.connect();
  await producer.send({ topic: 'logs', messages: [{ value: 'Hello Kafka' }] });
  await producer.disconnect();
}
sendMessage();
```

#### 1.9.4.5 2020–Present: Real-Time, AI-Driven, and Edge Computing

- **Demands:** Low latency, real-time, AI recommendations, streaming, instant messaging
- **Tech:** Serverless, Kubernetes, edge computing, observability, security, compliance

```mermaid
flowchart TD
    User --> EdgeNode
    EdgeNode -->|Low latency| K8sCluster
    EdgeNode --> AIModel
    K8sCluster --> ServerlessFn
    ServerlessFn --> Database
```

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from the Edge!'
    }
```

Each leap brought new challenges and solutions around scalability, reliability, and speed. Understanding this evolution helps us appreciate why certain choices are made today.

---

## 1.10 Course Structure

This 29-chapter course is designed to take you from beginner to confident architect. It is organized into **foundational chapters (1–15)** followed by **deep-dive case studies (16–28)** and **interview preparation (29)**.

### 1.10.1 Foundations

1. **Introduction** — System design fundamentals, importance, the evolution of the discipline, and beginner primers (computer basics, databases and SQL, hashing and encryption) *(you are here)*
2. **Networking & Communication** — IP, DNS, proxies, load balancers, API gateways, CDNs
3. **Protocols** — UDP, TCP, HTTP, REST, WebSockets, gRPC, GraphQL
4. **Architectural Patterns** — Monolithic, layered, microservices, event-driven, plus message-queue and container primers
5. **Web Concepts** — Authentication primer, sessions, cookies, JWT, serialization formats, CORS
6. **Scalability** — Horizontal vs. vertical scaling, auto-scaling, load balancing strategies, an AWS service map, a hands-on load-balancer lab
7. **Storage** — SQL vs. NoSQL, SQL in practice, CAP theorem, sharding (with a hands-on lab), replication, object storage and signed URLs, big data and MapReduce, vector databases
8. **Performance** — Caching, message queues, concurrency, indexing, query optimization
9. **Reliability, Availability & Disaster Recovery** — Fault tolerance, redundancy, multi-data-center design, RTO/RPO, backups, CI/CD and safe deployment
10. **Security** — CIA triad, authentication, authorization, encryption, threat modeling
11. **Distributed Systems Fundamentals** *(coming soon)*
12. **Cloud Design Patterns** *(coming soon)*
13. **Multi-Tenancy** *(coming soon)*
14. **Cloud Architecture & Cost** *(coming soon)*
15. **The System Design Blueprint** — A 4-step methodology for tackling any design problem

### 1.10.2 Case Studies

16. **URL Shortener** (TinyURL)
17. **Chat / Messaging App** (WhatsApp) *(coming soon)*
18. **News Feed** (Twitter / Instagram) *(coming soon)*
19. **Distributed Key-Value Store & Cache** *(coming soon)*
20. **Payment System** *(coming soon)*
21. **Auction Platform** (eBay)
22. **Ticket Booking System** (Ticketmaster) *(coming soon)*
23. **Cloud Storage** (Google Drive / Dropbox)
24. **Video Sharing Platform** (YouTube)
25. **Search Engine** (Google)
26. **E-Commerce Platform** (Amazon)
27. **Taxi Hailing App** (Uber)
28. **Collaborative Document Editor** (Google Docs)

> **About the gaps in numbering:** chapters 11–14, 17–20 and 22 are reserved for planned chapters that haven't been written yet (marked *coming soon* above). They're not missing content — they're TBD slots.

### 1.10.3 Wrap-Up

29. **Final Prep, Mindset & Moving Forward** — Interview strategies, frameworks, and continuous learning

> **Note on chapter naming:** Earlier drafts of the course used slightly different labels — for example, what is now "The System Design Blueprint" was sometimes called "Putting It All Together" or "Comprehensive Design," and "Networking & Communication" was occasionally folded into "Fundamentals." The structure above reflects the current course as it exists in the repository.

---

## 1.11 The 4-Step Design Framework

When approaching any system design problem — whether in an interview or in real life — use this structured methodology. Each step builds on the previous one. (Chapter 15 expands on this framework in depth; this section is the preview.)

```text
1. Understand the requirements
2. Estimate the scale
3. Design high-level components
4. Make strategic technology decisions
```

In more detail:

- **Step 1 — Requirements Clarification (Functional & Non-functional):**
  - Functional: What does the system do? (e.g., shorten URLs, support redirects)
  - Non-functional: How well must it do it? (latency, availability, throughput, durability)
- **Step 2 — Estimate the scale:**
  - How many users, requests/sec, data volume, growth rate
  - Identify likely bottlenecks early
- **Step 3 — High-Level Design (Draw block diagrams):**
  - Identify core services, data stores, communication patterns
  - Sketch components and how data flows between them
- **Step 4 — Detailed Components & Trade-offs:**
  - Databases, caching, scaling, partitioning, replication
  - Discuss pros/cons and alternatives
  - Justify every choice

> **Pro Tip:** When approaching any system design problem, start by clarifying requirements and constraints. Ask questions, outline assumptions, and only *then* move to architecture. This mirrors how real-world engineering happens.

---

## 1.12 Worked Example: A URL Shortener

Let's apply the framework to a simplified example — designing a URL shortener like bit.ly. (Chapter 16 covers this case study in full detail.)

### 1.12.1 Requirements

- Shorten long URLs
- Redirect users from short URLs to the originals
- Handle high read/write traffic
- Optional: analytics

### 1.12.2 High-Level Steps

1. Generate a unique short code for each URL.
2. Store the mapping in a database.
3. Redirect incoming requests to the original URL.

### 1.12.3 High-Level Architecture

```mermaid
flowchart LR
    U([User]) --> API["API"]
    API <--> DB[("Database")]
    API <--> Ca[("Cache")]
```


### 1.12.4 Request Flow (Mermaid)

```mermaid
graph TD
    A[User] -->|POST Long URL| B[API Server]
    B -->|Generate Code| C[Key-Value Store]
    C -->|Return Short URL| B
    B -->|Return Short URL| A
    A -->|GET Short URL| B
    B -->|Lookup Code| C
    C -->|Return Long URL| B
    B -->|302 Redirect| A
```

### 1.12.5 Simple Pseudocode

```python
import hashlib

def shorten_url(long_url):
    # Generate a short code using hash
    code = hashlib.md5(long_url.encode()).hexdigest()[:6]
    db.save(code, long_url)
    return f"https://sho.rt/{code}"

def redirect(code):
    long_url = db.get(code)
    if long_url:
        return redirect_to(long_url)
    else:
        return 404
```

### 1.12.6 A Flask Implementation

```python
# Example: Flask REST API for a TinyURL service

import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
url_map = {}

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.json['url']
    short_id = hashlib.md5(original_url.encode()).hexdigest()[:6]
    url_map[short_id] = original_url
    return jsonify({'short_url': f"https://tiny.url/{short_id}"})

@app.route('/<short_id>')
def redirect(short_id):
    original_url = url_map.get(short_id)
    if original_url:
        return f"Redirecting to {original_url}"
    return "URL not found", 404

if __name__ == "__main__":
    app.run()
```

- **API Design:** RESTful endpoints, stateless, scalable.
- **Data Management:** Hashing for the short URL; in-memory store (for illustration only — production would use Redis or DynamoDB).

### 1.12.7 Trade-Offs to Consider

- **Database choice:** Use a key-value store (e.g., Redis or DynamoDB) for high throughput; SQL for transactional needs.
- **Cache:** Add caching for popular short URLs to reduce DB reads.
- **Partition strategy:** Partition the database based on code prefix for scalability.
- **High availability:** Run multiple API servers behind a load balancer.

> **A note on the MD5-truncate approach:** Using the first 6 characters of an MD5 hash is fine as a teaching example, but it's collision-prone — two different long URLs can map to the same short code. Production-grade URL shorteners use **base62 encoding of a monotonically increasing counter** (often coordinated via Zookeeper or a similar service) to guarantee uniqueness. We cover this in detail in Chapter 16.

---

## 1.13 Architectural Patterns: A Preview

A glimpse of what's to come in Chapter 4.

### 1.13.1 Monolithic vs. Microservices Architecture

```mermaid
flowchart LR
    subgraph Mono["Monolith: one deployable unit"]
        M["UI + business logic + one shared database"]
    end
    subgraph Micro["Microservices: many small units"]
        SA["Service A<br/>own logic, own DB"]
        SB["Service B<br/>own logic, own DB"]
    end
    Mono -. versus .- Micro
```


- **Monolith:** Single codebase, tight coupling, easy to start, hard to scale.
- **Microservices:** Decomposed, independent deployability, language-agnostic, scales better.

---

## 1.14 Communication & Load Balancing: A Preview

A preview of Chapter 2 (Networking) and Chapter 6 (Scalability).

### 1.14.1 NGINX as a Reverse Proxy / Load Balancer

```nginx
http {
  upstream app_servers {
    server appserver1.example.com;
    server appserver2.example.com;
  }
  server {
    listen 80;
    location / {
      proxy_pass http://app_servers;
    }
  }
}
```

### 1.14.2 A Round-Robin Load Balancer in Python

```python
class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0

    def get_server(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

# Usage
lb = LoadBalancer(['AppServer1', 'AppServer2', 'AppServer3'])
for _ in range(6):
    print(lb.get_server())
```

Output:

```
AppServer1
AppServer2
AppServer3
AppServer1
AppServer2
AppServer3
```

---

## 1.15 Performance Boosters

A preview of Chapter 8.

- **Caching:** Use Redis or Memcached to speed up repeated requests.
- **Message Queues:** Offload processing using Kafka or RabbitMQ.
- **Database Sharding:** Split big databases for better throughput.
- **CDNs:** Serve static assets closer to users for lower latency.

### 1.15.1 Caching Example: User Profile Lookup

```python
import redis

# Connect to Redis
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_user_profile(user_id):
    # Check cache first
    profile = cache.get(f"user:{user_id}")
    if profile:
        return profile

    # If not in cache, fetch from DB (simulated)
    profile = fetch_from_db(user_id)
    cache.set(f"user:{user_id}", profile, ex=60*5)  # cache for 5 minutes
    return profile

def fetch_from_db(user_id):
    # Simulate DB fetch
    return {"user_id": user_id, "name": "John Doe"}
```

---

## 1.16 Security Essentials

A preview of Chapter 10. Security is **never** an afterthought.

- **Authentication & Authorization:** OAuth, JWT, role-based access control.
- **Encryption:** HTTPS in transit, data-at-rest encryption.
- **Firewalls & API Gateways:** Control access, mitigate attacks (rate limiting, IP filtering).

---

## 1.17 Common Beginner Anti-Patterns

Before you absorb the patterns, learn the **anti-patterns** — the predictable mistakes that turn good intentions into bad systems.

### 1.17.1 Premature Scaling

Designing for 1 billion users when you have 100. Sharding a database that fits on a single laptop. Building a Kafka pipeline for 50 events per day.

> **Rule of thumb:** Don't optimize for a scale you haven't reached. *Reaching* that scale will teach you what your real bottlenecks are. They are almost never what you predicted.

### 1.17.2 Cargo-Cult Architecture

"Netflix uses microservices, so we will too." Netflix has 4,000 engineers and a custom platform; you have 4 engineers and an MVP. Copying their architecture without their constraints gives you all the complexity and none of the benefits.

> **Rule of thumb:** Choose architecture for *your* constraints. The right answer for a 5-person startup is rarely the same as the right answer for FAANG.

### 1.17.3 Distributed Monolith

Splitting your code into 20 microservices that all share one database, all deploy together, and all break together. You get microservices' complexity (network calls, debugging across services) with monolith's coupling (shared schema, lockstep deploys). The worst of both worlds.

> **Rule of thumb:** Microservices need *independent deploys* and *independent data ownership.* If you don't have both, you have a distributed monolith.

### 1.17.4 Over-Rotating on Tech Choices

Spending three weeks debating PostgreSQL vs. MySQL when both would work. Switching to MongoDB to be "more scalable" when your data is highly relational.

> **Rule of thumb:** Your data model and query patterns matter 10× more than which DB you pick from the same category. Use Postgres unless you have a specific reason not to.

### 1.17.5 Ignoring Day-2 Operations

Designing the happy path beautifully. Forgetting backups, monitoring, alerting, on-call runbooks, capacity planning, cost dashboards. Then waking up at 3 AM with no way to diagnose what's wrong.

> **Rule of thumb:** A system that's hard to operate is a system that will fail. Operations is a design concern, not a deployment concern.

### 1.17.6 Big Up-Front Design

Spending 6 months designing the perfect architecture before writing a line of code. Real requirements are discovered by *using* the system, not by thinking about it.

> **Rule of thumb:** Design enough to get unstuck, then build, then design more. Iterate.

---

## 1.18 Tips and Tricks for Mastering System Design

A merged master list, drawn from across the lecture material.

### 1.18.1 Approach & Mindset

- **Build from Fundamentals.** Don't just memorize patterns — understand *why* they exist. Whether it's protocols, APIs, consistency models, or scaling techniques, building a strong foundation is critical.
- **Don't Memorize — Understand.** Focus on underlying principles, not just patterns.
- **Ask "Why?" Often.** For every decision, know the trade-offs (latency vs. consistency, cost vs. performance, etc.).
- **Stay Curious.** The field evolves — keep learning about new technologies and paradigms.

### 1.18.2 Practice & Frameworks

- **Use the 4-Step Design Framework:**
  1. Requirements clarification (functional & non-functional)
  2. High-level design (draw block diagrams)
  3. Detailed components (databases, caching, scaling)
  4. Bottlenecks & trade-offs (discuss pros/cons, alternatives)
- **Practice Real-World Case Studies.** Analyze the architectures of Netflix, WhatsApp, Uber, Airbnb. Simulate real interview discussions.
- **Simulate Interview Discussions.** Practice articulating your design decisions and trade-offs out loud, to a peer or to yourself.

### 1.18.3 Trade-Offs & Detail

- **Think in Trade-Offs.** There's never a perfect solution — always justify your choices (latency vs. consistency, cost vs. reliability). Practice discussing pros/cons.
- **Don't Skip the Details.** Dive into network protocols, database indexing, consistency models, sharding, replication, and failover.
- **Connect the Dots.** Realize how components like caching, load balancing, and sharding interrelate.

### 1.18.4 Visualization & Communication

- **Draw Diagrams.** Communicate your design visually — use sequence diagrams, flowcharts, and component diagrams. Start with the big picture before drilling into details.
- **Diagram First, Details Later.** High-level diagrams help you communicate the architecture before specifics.

### 1.18.5 Learning Discipline

- **Pause and Research.** If you hit an unfamiliar term (like *TF-IDF* in search systems), pause and read up before continuing. Don't gloss over.
- **Revisit & Iterate.** Topics are interconnected. Revisit sections to deepen your understanding. Do the course twice — the second run fills gaps you missed the first time.
- **Don't Rush.** Pause, research, and resume if you hit roadblocks.

### 1.18.6 Other Essentials

- **Security First.** Never treat security as an afterthought.
- **Prepare for Interviews Methodically.** Practice explaining your design, drawing diagrams, and defending your choices.

---

## 1.19 Navigating This Course Effectively

- **Start with Fundamentals** — build depth and clarity before jumping to advanced topics.
- **Use Case Studies** to simulate interview discussions and learn from real-world designs.
- **Apply the 4-Step Design Framework** for structured thinking.
- **Don't Skip Details** — pause, research, and revisit as needed.
- **Understand Interconnections** — system design topics are highly interrelated.

> **Diagrams note:** Mermaid diagrams render in supported Markdown viewers. If you're in an interview using pen and paper, sketch hand-drawn versions of the same.

---

## 1.20 Further Reading

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications by Martin Kleppmann](https://dataintensive.net/)

---

## 1.21 Conclusion

Mastering system design is not just about cracking interviews — it's about building scalable, reliable, and maintainable software that powers the world's largest applications. By mastering it, you'll be equipped to build scalable, efficient, and future-proof systems while naturally excelling in interviews.

System design isn't about memorizing buzzwords — it's about understanding the *why* behind every architectural choice. Start with the fundamentals, embrace the interconnections, and design one thoughtful step at a time.

Ready to dive in? Let's start this journey together!

---

**Next up:** [Chapter 2 — Networking & Communication →](./2%20-%20Networking%20%26%20Communication.md)

*Keep learning, keep building!*
