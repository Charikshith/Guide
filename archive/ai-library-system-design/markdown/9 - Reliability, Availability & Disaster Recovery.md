# Reliability, Availability & Disaster Recovery

Welcome to one of the most critical aspects of modern system design: **Reliability, Availability, and Disaster Recovery**. Whether you're designing a high-traffic web application, building cloud-native microservices, or architecting distributed platforms at scale, ensuring your systems can withstand failures and recover gracefully is paramount.

This chapter covers:

- Core concepts of system reliability (MTBF, MTTR, SLAs)
- High availability, fault tolerance, and failover mechanisms
- Backup and recovery strategies
- Disaster recovery in practice
- Real-world patterns, trade-offs, and actionable tips

> *"Systems fail. Reliability is how gracefully they handle it."*

---

## 9.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Compute the **9s of availability** and translate "99.99% uptime" into hours of allowed downtime.
2. Pick **RTO and RPO targets** based on business needs and design backups accordingly.
3. Apply **retry-with-backoff, circuit breakers, bulkheads, and idempotency keys** correctly.
4. Distinguish **active-active vs active-passive** and when each is right.
5. Run a **chaos engineering** experiment and explain what it would prove.

---

## Table of Contents

- [9.2 Introduction to System Reliability](#92-introduction-to-system-reliability)
- [9.3 Core Concepts: Reliability, Availability & Durability](#93-core-concepts-reliability-availability--durability)
- [9.4 Key Metrics: MTBF, MTTR, SLAs](#94-key-metrics-mtbf-mttr-slas)
- [9.5 Reliability in Distributed & Cloud-Native Systems](#95-reliability-in-distributed--cloud-native-systems)
- [9.6 High Availability, Fault Tolerance & Failover](#96-high-availability-fault-tolerance--failover)
- [9.7 Graceful Degradation](#97-graceful-degradation)
- [9.8 High Availability Patterns](#98-high-availability-patterns)
- [9.9 Designing for Redundancy](#99-designing-for-redundancy)
- [9.10 Health Monitoring & Self-Healing Systems](#910-health-monitoring--self-healing-systems)
- [9.11 Backup & Recovery Strategies](#911-backup--recovery-strategies)
- [9.12 Disaster Recovery in Practice](#912-disaster-recovery-in-practice)
- [9.18 CI/CD and Safe Deployment](#918-cicd-and-safe-deployment)
- [9.19 Combined Tips & Tricks](#919-combined-tips--tricks)
- [9.20 Sample Interview Questions](#920-sample-interview-questions)
- [9.21 Summary & Key Takeaways](#921-summary--key-takeaways)
- [9.22 Further Reading](#922-further-reading)

---

## 9.2 Introduction to System Reliability

Modern users expect systems to be **always available, consistent, and trustworthy**. Any downtime can result in financial loss, reputational damage, and erosion of user trust. Reliability isn't just about preventing failures — it's about how quickly and gracefully a system can recover when something does go wrong.

---

## 9.3 Core Concepts: Reliability, Availability & Durability

### 9.3.1 What is System Reliability?

Reliability is a system's ability to **operate continuously without failure**. It encompasses:

- **Correctness:** The system performs its intended function without errors.
- **Consistency:** Predictable, repeatable behavior across requests and over time.
- **Fault Tolerance:** The ability to withstand failures without total disruption.
- **Availability / Uptime:** The percentage of time the system is working and accessible.

### 9.3.2 Availability vs. Durability

| Concept       | Description                                     | Example                              |
|---------------|-------------------------------------------------|--------------------------------------|
| **Availability** | System is accessible and responsive             | Can query a database anytime         |
| **Durability**   | Data is safe and not lost (even after failures) | Data remains after system crash      |

```mermaid
flowchart LR
    Q(["User query"]) --> Up{"System up?"}
    Up -- "yes: available" --> A(["Available"])
    Up --> D{"Data safe?<br/>(durability)"}
```


---

## 9.4 Key Metrics: MTBF, MTTR, SLAs

- **MTBF (Mean Time Between Failures):** Average time a system runs before encountering a failure. *Higher MTBF = more stable system.*
- **MTTR (Mean Time To Recovery):** Average time to recover from a failure. *Lower MTTR = faster recovery.*

```
High MTBF + Low MTTR = High Reliability
```

```mermaid
graph TD
    A[System Running] -->|MTBF| B[Failure Occurs]
    B -->|MTTR| C[System Recovered]
    C -->|MTBF| D[Next Failure]
```

### 9.4.1 SLAs (Service Level Agreements)

Contractual guarantees about system performance (e.g., 99.9% uptime, response time, error rate).

> 99.9% uptime = ~8.76 hours downtime/year.

Common metrics: availability, response time, error rate.

### 9.4.2 Code Example: MTBF/MTTR Calculation

```python
import statistics

failure_times = [100, 120, 95, 110]    # uptime between failures in hours
recovery_times = [2, 1.5, 3, 2.5]      # recovery durations in hours

mtbf = statistics.mean(failure_times)
mttr = statistics.mean(recovery_times)

print(f"MTBF: {mtbf} hrs, MTTR: {mttr} hrs")
```

---

## 9.5 Reliability in Distributed & Cloud-Native Systems

### 9.5.1 Impact of Reliability on System Design

Design decisions that affect reliability:

- **Redundancy:** Multiple instances, failover setups.
- **Health checks and monitoring.**
- **Retry mechanisms and circuit breakers.**
- **Distributed design patterns:** Replication, quorum.

### 9.5.2 Reliability in Distributed Systems

**Challenges:**

- Network partitions.
- Node failures.
- Eventual consistency.

**Solutions:**

- Use **CAP-aware design.**
- Ensure **fault isolation.**
- Implement **replication** & **consensus algorithms** (e.g., Paxos, Raft).

### 9.5.3 Reliability in Cloud-Native Systems

Cloud infrastructure is inherently unreliable.

**Design for:**

- **Transient failures.**
- **Auto-scaling and self-healing.**
- **Chaos engineering** to test resilience.

> *"Design for failure"* is the **cloud-native mindset.**

---

## 9.6 High Availability, Fault Tolerance & Failover

### 9.6.1 Redundancy

Redundancy prevents single points of failure. Types include:

- **Hardware:** Multiple servers/storage devices.
- **Network:** Multiple data centers, network connections, routers, paths.
- **Service:** Replicated microservices/databases.

```mermaid
graph LR
A[Client] --> LB1[Load Balancer]
LB1 --> S1[Server 1]
LB1 --> S2[Server 2]
LB1 --> S3[Server 3]
```

### 9.6.2 Redundancy Strategies

| Strategy           | Description                                          | Use Case                         |
|--------------------|------------------------------------------------------|----------------------------------|
| **N+1**            | One extra instance for failover                      | 3 servers for 2 needed           |
| **Active-Active**  | Multiple nodes handle requests together              | Load balancing across regions    |
| **Active-Passive** | One active node, standby nodes activated on failure  | Standby backup DB or service     |

#### 9.6.2.1 N+1 Redundancy

- One more instance than needed (e.g., 3 servers for a 2-server load).
- If any one fails, the system remains available.

```
Required = N
Provisioned = N+1
If one fails, N remain to serve traffic.
```

#### 9.6.2.2 Active-Active

- All nodes are active, sharing the workload.
- High availability and load distribution.
- Requires robust load balancing and state synchronization.

```mermaid
graph LR
Client1 --> LB[Load Balancer]
Client2 --> LB
LB --> S1[Active Node 1]
LB --> S2[Active Node 2]
LB --> S3[Active Node 3]
```

ASCII view:

```
Active-Active:
User --> [LB] --> Node A (active)
                    |--> Node B (active)
                    |--> Node C (active)
```

#### 9.6.2.3 Active-Passive

- Only one node is active; others are on standby.
- On failure, a passive node becomes active.
- Simpler, but less load-efficient and has failover latency.

```mermaid
graph LR
Client --> LB[Load Balancer]
LB --> A[Active Node]
LB -.-> P1[Passive Node 1]
LB -.-> P2[Passive Node 2]
A --failure--> P1
```

ASCII view:

```
Active-Passive:
User --> [LB] --> Node A (active)
                    |--> Node B (standby)
```

---

### 9.6.3 Single Points of Failure (SPOF)

A **single point of failure** is any one component whose failure takes the whole system down. It is the most common reason a system is less reliable than the sum of its parts.

**Why it matters:**

- **Reliability:** one failed part means lost business and unhappy users (for example, nobody can reach checkout).
- **Scalability:** a design full of single points struggles to grow, because every extra component is one more thing that can break the chain.

**Finding them:** walk the path of one request from the user to the data and ask of every box, *"if this dies right now, what happens?"* If the answer is "everything stops", you have found one.

```mermaid
flowchart LR
    U([User]) --> DNS["DNS"] --> LB["Load balancer"] --> A["App server"] --> DB[("Database")]
    A --> C[("Cache")]
    A --> Q[["Queue"]]
```

In this sketch every box is a single point of failure. Each fix below adds redundancy:

| Component | Typical single point | Remove it by |
|-----------|---------------------|--------------|
| App servers | one server | several instances behind a load balancer, spread across availability zones |
| Load balancer | one balancer | an active-passive pair with a shared virtual IP, or a managed, multi-zone load balancer |
| Database | one primary | replication with automatic failover, backups, and a standby in another zone |
| Cache and queue | one node | a replicated or clustered cache; a clustered broker with mirrored queues |
| DNS | one provider or name server | several name servers, ideally from more than one provider |
| Data center | one site or region | a second site or region (see Failing Over Between Data Centers) |

**Hidden single points** are easy to miss: a single expired TLS certificate, one shared configuration or secrets service, one deployment pipeline, one third-party API, one person who knows how a system works, or one cloud region.

**Trade-off:** every redundant part costs money and adds complexity (replication lag, failover logic, more to monitor). Spend redundancy where an outage costs more than the redundancy does, and rehearse the failover so you know it works.

## 9.7 Graceful Degradation

Graceful degradation is about keeping **core functionality alive** during partial failures, even if some features are unavailable.

- **Definition:** System still operates at a reduced capacity during failures.
- Example: During high traffic, disable non-essential features.
- Helps maintain **user experience** even when full service isn't possible.
- Critical for ensuring users still benefit from some **functionality during outages.**

**Example:** If a recommendation engine fails on an e-commerce site, the main shopping and checkout features remain operational.

```python
def handle_request(request):
    if not essential_feature_available():
        # Disable non-essential feature
        return minimal_viable_response(request)
    return full_feature_response(request)
```

```python
# Pseudocode for graceful degradation in a Flask app
@app.route('/recommendations')
def recommendations():
    try:
        return get_recommendations(user_id)
    except RecommendationServiceError:
        # Degrade gracefully: show popular items instead
        return get_popular_items()
```

A simpler form:

```python
def handle_request():
    try:
        return full_service()
    except ServiceOverloadError:
        return degraded_service()  # e.g., disable image uploads
```

---

## 9.8 High Availability Patterns

### 9.8.1 Load Balancing

Distribute traffic evenly across backend nodes. Essential for removing bottlenecks and handling node failures.

```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
}
server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### 9.8.2 Replication

Replicate data across nodes/data centers for availability and durability.

- **Synchronous replication:** Zero data loss, but higher latency.
- **Asynchronous replication:** Lower latency, but possible data loss on failure.

### 9.8.3 Failover

Automatically switches to a backup node if a primary fails.

```yaml
# Kubernetes deployment with readiness/liveness probes for failover
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 3
```

### 9.8.4 High Availability Diagram

```mermaid
flowchart LR
    User((User))
    LB[Load Balancer]
    S1[Server 1]
    S2[Server 2]
    S3["Server 3 (Standby)"]
    User --> LB
    LB --> S1
    LB --> S2
    S1 -.Failover.-> S3
    S2 -.Failover.-> S3
```

---

## 9.9 Designing for Redundancy

### 9.9.1 Redundant Components

Design with multiple instances of key components (servers, databases, etc.) to avoid single points of failure.

### 9.9.2 Geographical Redundancy

- Use **multiple data centers** or **cloud regions** for disaster recovery.
- Ensures high availability and resilience during regional outages.
- Distribute components across multiple regions to handle data center/region outages.

### 9.9.3 Failing Over Between Data Centers

A **data center** is a building (or campus) of servers with its own power, cooling and network. Cloud providers group them into **regions** and **availability zones**. Running in more than one data center protects you from a whole-site failure. The comparison of **active-active** and **active-passive** designs is in the section of that name later in this chapter; this part covers what makes either one work in practice.

**Routing users to a healthy site:** use **Geo-DNS** (see the DNS chapter) or a global load balancer to send each user to the nearest healthy site, and to drop a failed site from the answers. Keep DNS **TTLs** short enough for a failover to take effect quickly.

**Things that go wrong:**

- **Replication lag:** the standby is a few seconds behind, which sets your **RPO** (how much data you can lose).
- **Split brain:** both sites believe they are the primary and accept conflicting writes. Use a quorum or an external arbiter to decide the single winner.
- **Untested failover:** a switch you have never exercised often fails. Rehearse it regularly.
- **Capacity:** if one site fails, can the survivors carry the whole load? In active-active designs each site must be sized for that.

### 9.9.4 Automated Failover

- Ensure **failover happens automatically** without manual intervention.
- Enables seamless service continuity when a primary system fails.

**Example architecture:** A client application connects to a database driver, which handles connections to a primary database. The primary replicates data to secondary databases, ensuring redundancy and quick recovery during failure.

```mermaid
flowchart TD
    Client[Client Application]
    Driver[Database Driver]
    PrimaryDB[(Primary Database)]
    SecondaryDB1["(Secondary DB)"]
    SecondaryDB2["(Secondary DB)"]

    Client --> Driver
    Driver -->|Writes and Reads| PrimaryDB
    PrimaryDB -->|Replication| SecondaryDB1
    PrimaryDB -->|Replication| SecondaryDB2

    style PrimaryDB fill:#b6e7a7,stroke:#4CAF50,stroke-width:2px,color:black;
    style SecondaryDB1 fill:#d5f5e3,stroke:#4CAF50,stroke-width:1.5px,color:black;
    style SecondaryDB2 fill:#d5f5e3,stroke:#4CAF50,stroke-width:1.5px,color:black;
    style Driver fill:#ffe699,stroke:#e6ac00,stroke-width:1.5px,color:black;
    style Client fill:#d9e1f2,stroke:#0070c0,stroke-width:1.5px,color:black;
```

**Automation:** Use health checks; orchestration tools like Kubernetes, AWS Auto Scaling, Azure Availability Sets.

---

## 9.10 Health Monitoring & Self-Healing Systems

### 9.10.1 Health Monitoring

- Track server uptime, API responses, error rates, CPU/memory usage.
- Alert on anomalies before users notice.

### 9.10.2 Self-Healing

- Systems that **automatically recover** (restart, redeploy, reroute).
- E.g., Kubernetes restarts crashed pods automatically.

```yaml
# Kubernetes pod auto-restart example
restartPolicy: Always
```

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## 9.11 Backup & Recovery Strategies

### 9.11.1 What and Why

- **Backup:** Creating copies of data to protect against loss.
- **Recovery:** Restoring data after failure/corruption.
- Critical for: disaster recovery, ransomware protection, compliance, human error.

**Scenarios demanding backup & recovery:**

- Hardware or software failure.
- Human error (accidental deletion).
- Cyber attacks (ransomware).
- Natural disasters (fire, flood).
- Compliance & legal retention requirements.

> **Remember:** Backup and recovery **complement** redundancy and replication; they're not substitutes.

### 9.11.2 Backup Types

| Type             | Description                          | Pros                | Cons                  |
|------------------|--------------------------------------|---------------------|-----------------------|
| **Full**         | Copies all data                      | Simple restore      | High storage & time   |
| **Incremental**  | Changes since last backup            | Fast backup         | Slower restore        |
| **Differential** | Changes since last full backup       | Faster restore      | Larger than incremental |

```mermaid
flowchart LR
    M["Monday<br/><b>Full backup</b>"] --> T["Tuesday<br/><b>Incremental 1</b>"] --> W["Wednesday<br/><b>Incremental 2</b>"] --> Th["Thursday<br/><b>Differential 1</b>"] --> F["Friday<br/><b>Incremental 3</b>"]
    classDef full fill:#2563eb,stroke:#1d4ed8,color:#ffffff
    classDef inc fill:#10b981,stroke:#047857,color:#ffffff
    classDef diff fill:#f59e0b,stroke:#b45309,color:#111827
    class M full
    class T,W,F inc
    class Th diff
```

**Hybrid approach example:** Weekly full backups, daily incremental backups.

### 9.11.3 Recovery Models: Cold, Warm, Hot

| Model    | Resources Provisioned   | Downtime         | Cost     | Use Case                |
|----------|-------------------------|------------------|----------|-------------------------|
| **Cold** | None / backups offline  | Hours to days    | Low      | Non-critical apps       |
| **Warm** | Some / pre-provisioned  | Minutes to hours | Medium   | Business apps           |
| **Hot**  | Full (always ready)     | Seconds or less  | High     | Mission-critical systems|

```mermaid
graph TD
    A[Primary Data Center] -- Replication --> B[Warm Standby]
    A -- Full Sync --> C[Hot Standby]
    D[Offline Backups] -. Restore .-> A
```

### 9.11.4 Key Metrics: RTO & RPO

- **RTO (Recovery Time Objective):** How quickly can you recover? (e.g., 1 hour)
- **RPO (Recovery Point Objective):** How much data loss is acceptable? (e.g., 15 minutes)

> **Shorter RTO/RPO = higher cost and complexity.**

#### 9.11.4.1 Real-World Mapping

- **Banking system:** RTO = 5 minutes, RPO = near zero.
- **Internal tool:** RTO = 1 day, RPO = 12 hours.

```mermaid
gantt
    dateFormat  HH:mm
    axisFormat  %H:%M
    title Backup and Recovery Timeline
    section Normal operation
    Uptime                :done,    des1, 00:00, 4h
    section Failure and Recovery
    Failure Detected      :active,  des2, 04:00, 30m
    Recovery In Progress  :         des3, 04:30, 1h
```

### 9.11.5 Designing Your Backup & Recovery Strategy

**Key trade-offs:**

- **Cost vs. recovery speed:** Faster recovery usually means more redundancy and higher storage/infra spend.
- **Complexity:** More frequent backups = more management overhead.
- **Business criticality:** Mission-critical? Invest more.
- **Compliance:** Are there legal retention or encryption needs?
- **Infrastructure maturity:** Can your team automate and manage complex strategies?

**Sample hybrid strategy:**

- **Full backup:** Sunday 2 AM.
- **Incremental:** Daily at 2 AM.
- **Retention:** 30 days on disk, 1 year in cloud cold storage.

### 9.11.6 Best Practices: The 3-2-1 Rule

- **3** copies of your data (primary + 2 backups).
- **2** different storage media (e.g., disk, cloud).
- **1** backup offsite (remote/cloud).

**Other best practices:**

- **Automate everything:** Automate both backup creation and restore testing. Monitor backup jobs and alert on failures.
- **Encrypt data:** Use strong encryption at rest (AES-256) and in transit (TLS).

### 9.11.7 Sample Backup Automation Code

**Automated daily database backup with AWS S3 (Python):**

```python
import boto3
import subprocess
import datetime

def backup_postgres(db_name, s3_bucket, s3_prefix):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/tmp/{db_name}_backup_{timestamp}.sql.gz"
    # Dump and compress the database
    subprocess.run([
        "pg_dump", db_name,
        "--no-owner", "--no-acl"
    ], stdout=subprocess.PIPE)
    subprocess.run(["gzip", "-c"], stdin=subprocess.PIPE, stdout=open(filename, 'wb'))

    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(filename, s3_bucket, f"{s3_prefix}/{filename}")
    print(f"Backup uploaded to s3://{s3_bucket}/{s3_prefix}/{filename}")

# Usage
backup_postgres("mydb", "my-backup-bucket", "db-backups")
```

**Restore example:**

```sh
# Download from S3
aws s3 cp s3://my-backup-bucket/db-backups/mydb_backup_20230601_020000.sql.gz .
gunzip mydb_backup_20230601_020000.sql.gz
psql mydb < mydb_backup_20230601_020000.sql
```

**Linux cron backup:**

```bash
# Automated daily backup (cronjob)
0 2 * * * tar -czf /backups/app-$(date +\%F).tar.gz /data/app
```

---

## 9.12 Disaster Recovery in Practice

In today's digital world, downtime is expensive — not just in dollars, but also in lost trust and missed opportunities. Mission-critical systems in finance, healthcare, e-commerce, and beyond must be designed to recover gracefully from disasters — hardware failures, cyberattacks, or entire regional outages.

### 9.12.1 Why Disaster Recovery REALLY Matters

- **Downtime costs money & trust:** Even a few minutes of outage can mean lost revenue and broken user trust.
- **Beyond backups:** DR is not just about saving data; it's about keeping the *whole system* resilient and available.
- **Compliance:** For regulated industries (finance, healthcare), DR is a legal requirement, not just a best practice.

> DR builds on your backup strategy but focuses on *system-level* recovery — bringing apps, services, and infrastructure *all back online*.

### 9.12.2 DR for Mission-Critical Applications

**Example targets:**

| System Type     | Target RTO  | Target RPO    |
|-----------------|-------------|---------------|
| Bank Core       | < 5 minutes | < 1 minute    |
| E-commerce Cart | < 15 min    | < 5 minutes   |
| Social Media    | < 1 hour    | < 15 minutes  |

### 9.12.3 DR Architecture: Key Layers of Redundancy

- **Compute redundancy:** Multiple servers/VMs/containers.
- **Storage redundancy:** Replicated databases, distributed storage.
- **Network redundancy:** Multiple paths, routers, ISPs.
- **Geo-redundancy:** Multiple regions/data centers.

### 9.12.4 Backup vs. Failover: Why You Need Both

- **Backup:** Restores *data* after corruption, deletion, or ransomware.
- **Failover:** Keeps *services* running by switching to healthy infrastructure during a failure.

| Backup Only                              | Failover Only                                | Combined (Best)                              |
|------------------------------------------|----------------------------------------------|----------------------------------------------|
| Data recovery, but no service continuity | Service continuity, but not data loss        | Both service continuity and data integrity   |

**Diagram: DR Coverage**

```mermaid
flowchart TB
    D["Disaster event"] --> DL["Data loss"]
    D --> IO["Infrastructure outage"]
    DL --> B["Backup"]
    IO --> F["Failover"]
    B --> R(["Complete resilience"])
    F --> R
```


### 9.12.5 Recovery Automation and Testing

> *"If you haven't tested your DR plan, you don't really have one."*

**Automate key actions:**

- Failover switching (primary <-> secondary).
- Data validation after restore.
- Notifications and logging.

**Regularly run DR drills:** Simulate failures to test team readiness and system behavior.

**Sample pseudocode: Automated Failover**

```python
def disaster_recovery_monitor():
    while True:
        if not is_primary_healthy():
            promote_secondary()
            notify_team()
            log_event("Failover occurred at {}".format(datetime.now()))
        sleep(10)

def promote_secondary():
    # Switch DNS, reconfigure load balancer, etc.
    # Example for AWS Route53:
    subprocess.run([
        "aws", "route53", "change-resource-record-sets",
        "--hosted-zone-id", "<zone-id>",
        "--change-batch", "file://failover.json"
    ])
```

### 9.12.6 Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold):
        self.failure_threshold = failure_threshold
        self.failure_count = 0
        self.open = False

    def call(self, func, *args, **kwargs):
        if self.open:
            raise Exception("Circuit is open!")
        try:
            return func(*args, **kwargs)
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.open = True
            raise

    def reset(self):
        self.failure_count = 0
        self.open = False
```

### 9.12.7 Geo-Distributed Systems: DR Challenges

Geo-distribution increases resilience but also complexity:

- **Data consistency across regions:** Updates must be synchronized without conflict.
- **Latency:** Failover to distant regions can introduce delays.
- **Regulatory constraints:** Laws like GDPR may restrict where data can be stored.
- **Coordinated multi-region failover:** Avoiding split-brain and ensuring quorum is vital.

### 9.12.8 Geo-Redundancy & Quorum-Based Design

**Geo-Redundancy:**

Deploy services across multiple physical locations/regions.

```
+----------+       +----------+       +----------+
|  RegionA |<----->|  RegionB |<----->|  RegionC |
+----------+       +----------+       +----------+
      |                 |                  |
  [Users]           [Users]            [Users]
```

If one region fails, others continue serving requests.

**Quorum-Based Design:**

**Quorum:** Minimum number of nodes that must agree for an operation to be considered successful.

**Why:** Prevents "split-brain" scenarios and ensures consistency.

**Example: Write operation in a distributed DB**

- 5 nodes, quorum = 3.
- Operation succeeds if at least 3 nodes acknowledge the write.

```python
def write_with_quorum(data, nodes, quorum=3):
    acks = 0
    for node in nodes:
        if node.write(data):
            acks += 1
        if acks >= quorum:
            return True
    return False
```

```mermaid
graph TD
A[Primary Region] -.sync.-> B[Secondary Region]
A --> Quorum["Quorum (majority nodes)"]
```

### 9.12.9 Testing Your DR Plan: Example DR Drill

1. **Simulate failure:** Shut down a region or primary database.
2. **Observe automation:** Ensure failover scripts trigger; monitoring and alerting fire.
3. **Validate data:** Run integrity checks on restored data.
4. **Review logs:** Confirm timelines, actions, and gaps.

---

### 9.12.10 Replication Is Not a Backup

Replication keeps a **live copy**, which is exactly why it also copies your mistakes. Match each disaster to the right protection:

| Disaster | Replication helps? | Backups help? |
|----------|:-:|:-:|
| Disk or node failure | yes | yes |
| Zone outage | yes (multi-zone) | yes |
| Region outage | yes (cross-region) | yes, if stored cross-region |
| **Accidental `DELETE`, a bad migration, a bug corrupting data** | **no**: replicas copy the mistake instantly | **yes**, with point-in-time recovery |
| **Ransomware or a malicious admin** | no | yes, **only if** backups are immutable and in a separate account |
| Provider or account compromise | no | yes, with a copy in another account or provider |

Replication is for **availability**; backups are for **recovery**. You need both.

**The 3-2-1 rule, plus immutability:** keep **3** copies, on **2** different media or services, with **1** off-site, and make at least one copy **immutable** (object lock / write-once) in a separate account.

### 9.12.11 Disaster-Recovery Strategies: Cost vs. Recovery Time

| Strategy | The secondary region has | RTO | RPO | Cost |
|----------|--------------------------|-----|-----|------|
| **Backup and restore** | only backups | hours to a day | hours (minutes with point-in-time recovery) | $ |
| **Pilot light** | data replicated; a minimal core of infrastructure, off or tiny | tens of minutes | minutes | $$ |
| **Warm standby** | a scaled-down, fully working copy | minutes | seconds to minutes | $$$ |
| **Multi-site active-active** | full capacity serving live traffic | near zero (just reroute) | near zero (synchronous) or seconds | $$$$ |

**Test restores, not just backups.** Backups fail silently: expired credentials, missing tables, corrupt files, incompatible versions, a restore that takes 14 hours instead of the 1 you promised, a runbook nobody can follow. The only real measure of your RTO and RPO is a **timed restore**, rehearsed on a schedule.

## 9.13 The 9s of Availability — What "Five Nines" Actually Means

| Availability  | Allowed downtime per year | Per month     | Per day      |
|---------------|---------------------------|---------------|--------------|
| 99%           | 3.65 days                 | 7.2 hours     | 14.4 minutes |
| 99.9%         | 8.77 hours                | 43.8 minutes  | 1.44 minutes |
| 99.95%        | 4.38 hours                | 21.9 minutes  | 43.2 seconds |
| 99.99%        | 52.6 minutes              | 4.38 minutes  | 8.64 seconds |
| 99.999%       | 5.26 minutes              | 26.3 seconds  | 0.86 seconds |

> **Reality check:** "Five nines" (99.999%) means **less than 6 minutes of downtime per year.** That includes deploys, patches, and unforeseen incidents. Achieving it requires multi-region active-active, automated failover, no single points of failure anywhere, and rigorous testing. It's *expensive*.
>
> Most products live at 99.9% (three nines) and that's usually fine.

### 9.13.1 Compounding: System ≠ Component Availability

If your service depends on 3 things, each 99.9% available:

`0.999 × 0.999 × 0.999 ≈ 0.997` = 99.7% (about 26 hours of downtime/year).

**Lesson:** the more dependencies, the lower your composite availability. Either make each component *more* reliable, or design to **work in degraded mode** when a dependency is down.

---

### 9.13.2 Availability Math and Failure Domains

**Series and parallel.** Availability multiplies when parts depend on each other, and improves when parts back each other up.

| Setup | Formula | Example with 99.9% parts |
|-------|---------|--------------------------|
| **Series** (A needs B needs C) | `A × B × C` | 2 in series: 99.8% |
| **Parallel** (any one of n is enough) | `1 − (1 − A)ⁿ` | 2 in parallel: 99.9999% |
| 5 services in series | `0.999⁵` | about 99.5%, roughly 44 hours of downtime a year |

Parallel math assumes the failures are **independent**. That is the reason to spread replicas across different zones, not just different servers.

**Failure domains** are things that fail together: a process, a host, a rack, an availability zone, a region, a cloud provider, a deploy, a configuration push. Spread replicas across domains so one failure never takes out every copy. **Correlated failures** (the same bad deploy everywhere, the same shared dependency) are the real enemy, because they defeat the parallel math.

**Levers that raise reliability:** redundancy (N+1, N+2), health checks with automatic failover, timeouts, retries with backoff, circuit breakers, **load shedding** (deliberately rejecting excess work so the rest succeeds), graceful degradation, and gradual rollouts.

## 9.14 Retry Patterns Done Right

Retries are the #1 way to convert a single transient failure into a system-wide outage. Done wrong, they're an amplifier. Done right, they're a lifesaver.

### 9.14.1 The Five Rules of Retries

1. **Only retry idempotent operations.** Retrying a non-idempotent POST can double-charge a credit card.
2. **Exponential backoff** — `delay = base × 2^attempt`. Not constant delay.
3. **Add jitter** — `delay = random(0, base × 2^attempt)`. Without jitter, retries from many clients synchronize and stampede.
4. **Cap the retries.** Usually 3-5. Past that, give up and report failure.
5. **Respect `Retry-After` and `429`.** If the server tells you when to retry, listen.

### 9.14.2 Example

```python
import random, time

def with_retry(fn, max_attempts=4, base=0.1):
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            delay = random.uniform(0, base * (2 ** attempt))  # exponential + jitter
            time.sleep(delay)
```

---

## 9.15 Idempotency Keys

Even with retries done right, network failures can leave you unsure whether a request succeeded. The fix: **idempotency keys.**

Client generates a unique key (UUID) per logical operation. Server stores `(key → result)`. On retry, server returns the cached result instead of executing again.

```
POST /payments
Idempotency-Key: 6f7d3e4a-9b2c-4f1d-8e3a-1c2b3d4e5f60
{
  "amount": 100,
  "user_id": 42
}
```

Stripe, PayPal, and modern payment APIs all use this. **You should too** for any non-idempotent operation.

---

## 9.16 Active-Active vs Active-Passive

| Mode             | Behavior                                                                      | Pros                                  | Cons                                |
|------------------|-------------------------------------------------------------------------------|---------------------------------------|--------------------------------------|
| **Active-Active**| All regions serve traffic simultaneously; data replicated bidirectionally     | Zero failover time; uses all capacity | Conflict resolution required; complex |
| **Active-Passive**| One region serves; other(s) on standby, take over on failure                | Simpler; clean failover               | Standby capacity is paid for and idle |

*Routing, replication lag and split brain are covered under Failing Over Between Data Centers in the redundancy section.*

**Rule of thumb:** active-active is the right answer for read-heavy systems where eventual consistency is OK (social feeds, content delivery). Active-passive is simpler for transactional systems (banking, ticketing) where conflict resolution would be a nightmare.

---

## 9.17 Chaos Engineering — Failure as a Practice

You don't know if your reliability mechanisms work until you actually break things in production. **Chaos engineering** = deliberately injecting failures (kill pods, drop network packets, fail dependencies) to verify the system survives.

**Famous tools:**
- **Chaos Monkey** (Netflix) — kills random EC2 instances.
- **Gremlin** — broader fault injection: CPU, memory, network, dependencies.
- **LitmusChaos** (CNCF) — Kubernetes-native chaos experiments.

**Start small:**
1. Pick a non-critical service in staging.
2. Hypothesize what will happen ("if I kill this pod, traffic shifts to others, p99 stays under 200ms").
3. Inject the failure.
4. Measure. If you were wrong, fix the system *before* it happens for real.

> **Rule:** if you've never killed a database in staging, you don't know if your failover works. **Reliability is a measurable claim, not a feeling.**

---

## 9.18 CI/CD and Safe Deployment

> **Why this belongs in reliability:** most outages are caused by **changes**. A good delivery pipeline makes changes small, tested and reversible, which protects availability more than almost any other habit.

### 9.18.1 What the Terms Mean

| Term | Meaning |
|------|---------|
| **Continuous Integration (CI)** | every change is merged often and automatically built and tested |
| **Continuous Delivery (CD)** | every change that passes is **ready** to release; a human presses the button |
| **Continuous Deployment** | every change that passes is released **automatically**, with no button |

### 9.18.2 A Typical Pipeline

```mermaid
flowchart TB
    subgraph CI["Continuous integration: runs on every change"]
        direction LR
        C["Commit / pull request"] --> B["Build"] --> L["Lint and static checks"] --> T["Unit and integration tests"] --> P["Package container image"]
    end
    subgraph CD["Continuous delivery: release"]
        direction LR
        S["Deploy to staging"] --> A{"Approval gate"} --> D["Deploy to production"] --> M["Monitor, roll back if needed"]
    end
    CI --> CD
```

Each stage is a **gate**: if it fails, the change stops and nobody is paged at night. Fast stages (lint, unit tests) run first so feedback arrives in minutes.

### 9.18.3 Example: A CircleCI Configuration

```yaml
version: 2.1
jobs:
  test:
    docker:
      - image: cimg/node:20.11
    steps:
      - checkout
      - run: npm ci
      - run: npm run lint
      - run: npm test
  deploy:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - run: ./scripts/deploy.sh production
workflows:
  build-and-deploy:
    jobs:
      - test
      - hold:
          type: approval          # a human must approve before production
          requires: [test]
          filters: { branches: { only: main } }
      - deploy:
          requires: [hold]
          filters: { branches: { only: main } }
```

**Reading it:** *jobs* are units of work with their own environment and steps; the *workflow* wires jobs together, sets the order (`requires`) and adds a manual approval step. GitHub Actions, GitLab CI and Jenkins express the same ideas in their own syntax.

### 9.18.4 Deployment Strategies

| Strategy | How | Strength | Risk or cost |
|----------|-----|----------|--------------|
| **Rolling** | replace instances a few at a time | no extra capacity needed | old and new versions run together for a while |
| **Blue-green** | build a full new environment ("green"), switch traffic over at once from the old ("blue") | instant switch and instant rollback | double the infrastructure during release |
| **Canary** | send a small share of traffic (1 to 5 percent) to the new version, then increase | real-traffic test with limited blast radius | needs good monitoring and traffic splitting |
| **Feature flags** | ship code switched off, enable it later for chosen users | decouples deploy from release; instant off switch | flags pile up and must be cleaned |

### 9.18.5 Hot Fixes and Faster Pipelines

**Hot fix:** a small, urgent change that goes to production quickly to stop an ongoing problem, ahead of the normal release schedule. Typical flow:

1. **Detect:** monitoring and alerts show the failure (error rate or latency jumps). Teams usually route alerts to a chat channel and an on-call pager so someone sees them within minutes.
2. **Stabilise first:** roll back the last release or switch off a feature flag if that restores service; fixing forward is for when rollback is impossible.
3. **Diagnose:** use logs, metrics and traces to find the root cause, and, where safe, inspect the running application.
4. **Fix on a short branch,** run the *same* pipeline (a hot fix is not a reason to skip tests, only to keep the change tiny), and deploy through the normal path.
5. **Follow up:** merge the fix back to the main branch, write a short post-incident review, and replace the quick patch with a permanent solution.

**Keeping the pipeline fast:**

- **Cache dependencies** (for example `node_modules` or a package cache) between runs, keyed on the lock file, so builds do not download everything each time.
- **Pass build outputs between jobs** with the CI system's workspace or artifact feature instead of rebuilding in every job.
- **Run independent jobs in parallel** (lint, unit tests, security scan) and put the quickest checks first.
- **Protect the main branch:** require a passing pipeline and a reviewer's approval before a pull request can merge.

### 9.18.6 Making Releases Safe

- **Small, frequent changes** are easier to understand and to roll back than big ones.
- **Automate rollback** and rehearse it. Define the trigger up front (for example an error rate above a threshold).
- **Database changes** need care: use **expand then contract**. First add the new column or table (compatible with old code), deploy the code, migrate data, and only later remove the old structure. Never ship a change that requires old and new code to disagree.
- **Observe after release:** watch error rate, latency and business metrics for the new version (see Chapter 8) before widening a canary.
- **Same artifact everywhere:** build the container image once and promote that exact image from staging to production.
- **Protect secrets:** the pipeline needs credentials, so store them in a secrets manager and limit what each job can reach (see Chapter 10).

## 9.19 Combined Tips & Tricks

A consolidated master list drawn from all sections.

### 9.19.1 Design Philosophy

- **Design for failure:** Assume components/services will fail; plan accordingly. Use retries, circuit breakers, fallback logic.
- **Cloud-native mindset:** Leverage managed services' redundancy and auto-healing (AWS RDS Multi-AZ, GCP Cloud SQL HA).
- **Balance cost vs. risk:** Higher SLAs and lower RTO/RPO mean higher cost and complexity. Align with business needs.

### 9.19.2 Automation

- **Automate everything:** Backups, failover, health checks, restore tests.
- **Use circuit breakers and retries:** Prevent cascading failures due to repeated calls to failing services.

### 9.19.3 Testing

- **Test regularly:** Run DR drills, test backups, simulate failures (chaos engineering).
- **Test your DR plan:** *If you haven't tested it, you don't have it.*
- **Test across regions:** Don't assume multi-region just "works" — validate failover and data consistency.

### 9.19.4 Monitoring

- **Monitor key metrics:** Track MTBF, MTTR, availability, error rates, backup status.
- **Monitor and alert:** Don't just collect metrics — act on them.
- **Implement the 3-2-1 backup rule:** 3 copies, 2 different media, 1 offsite.

### 9.19.5 User Experience

- **Gracefully degrade:** Prioritize core features; design for partial service during failures.
- **Document SLAs and recovery objectives:** Explicitly define and communicate RTO/RPO.

### 9.19.6 Documentation

- **Document and review:** Keep disaster recovery and backup plans up to date and review them periodically.
- **Document your DR plan:** Ensure everyone knows the process and their role.

### 9.19.7 Backup-Specific

- **Test restores regularly:** A backup you've never restored is a backup you don't have.
- **Monitor success & failures:** Set up dashboards/alerts.
- **Cloud backups:** Use object storage with lifecycle policies for cost savings.
- **Immutable backups:** Protect against ransomware by making backups write-once, read-many (WORM).
- **Geo-redundancy:** For mission-critical data, store backups in different regions.
- **Automate cleanup:** Use scripts or cloud policies to prune old backups.

---

## 9.20 Sample Interview Questions

- How would you design a system for 99.99% availability?
- What's the difference between backup and failover?
- How do you optimize RTO and RPO in a distributed environment?
- How would you design DR for a high-traffic web app?
- What are RTO and RPO, and how do you optimize them?
- What are the challenges with geo-distributed DR systems?
- Explain quorum-based design in distributed recovery.
- How do you ensure high availability across multiple regions?
- Compare active-active and active-passive redundancy.
- What is graceful degradation? Provide an example.
- How do you detect and recover from failures automatically?

---

## 9.21 Summary & Key Takeaways

- **Reliability is foundational** — measured by metrics like MTBF, MTTR, and SLAs.
- **Design choices must anticipate and tolerate failure.**
- **Redundancy** (hardware, network, service) prevents single points of failure.
- Patterns like **N+1, active-active, and active-passive** support high availability.
- **Graceful degradation** keeps core user experience intact during partial failures.
- **Load balancing, replication, automated failover, and self-healing** are critical patterns in real-world HA systems.
- **Backup and disaster recovery** strategies require regular testing, automation, and a clear understanding of RTO/RPO trade-offs.
- **Geographical redundancy and quorum-based designs** support resilience in distributed and cloud-native environments.
- **DR is more than backups** — it's about *system continuity.*
- **Combine failover + backup** for true resilience.
- **DR is core architecture** for mission-critical systems, not an afterthought.

---

## 9.22 Further Reading

- [Google SRE Book: Reliability](https://sre.google/sre-book/reliability/)
- [Google SRE Book: Reliability and Recovery](https://sre.google/sre-book/)
- [AWS Well-Architected Framework: Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- [AWS Disaster Recovery Whitepaper](https://aws.amazon.com/whitepapers/disaster-recovery/)
- [AWS Backup Best Practices](https://docs.aws.amazon.com/backup/latest/devguide/best-practices.html)
- [PostgreSQL Backup & Restore Docs](https://www.postgresql.org/docs/current/backup.html)
- [Google Cloud: Disaster Recovery Planning Guide](https://cloud.google.com/architecture/disaster-recovery-cookbook)
- [Kubernetes Documentation: Self-Healing](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-lifetime)
- [CAP Theorem in Distributed Systems](https://en.wikipedia.org/wiki/CAP_theorem)

---

**Next Up:** [Chapter 10 — Security in System Design →](./10%20-%20Security%20in%20System%20Design%20%E2%80%93%20Principles%2C%20Practices%20%26%20Protocols.md) — protect your reliable systems from modern threats.
