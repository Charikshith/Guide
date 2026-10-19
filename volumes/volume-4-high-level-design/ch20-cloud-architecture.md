# Chapter 20 — Cloud Architecture

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 19 — Authentication & Authorization in System Design](ch19-authentication-and-authorization-in-system-design.md) · Next → [Chapter 21 — Cost & Capacity Economics](ch21-cost-and-capacity-economics.md)

---

## Concept

Cloud building blocks (compute, storage, networking, managed services), serverless vs containers, and cost-aware design.

**In one sentence:** cloud architecture is choosing and connecting rented building blocks — compute, storage, networking, and managed services — so the system meets its reliability, performance, security, and cost goals with the least undifferentiated work for your team.

**Read the full explanation in the AI Library** (it is explained there once, so this chapter does not repeat it):

* [Chapter 6 — Cloud Architecture Choices](https://charikshith.github.io/AI_Library/notes/system-design/chapters/6%20-%20Scalability%20in%20System%20Design.html#617-cloud-architecture-choices)
* [Chapter 6 — Cloud Building Blocks: An AWS Service Map](https://charikshith.github.io/AI_Library/notes/system-design/chapters/6%20-%20Scalability%20in%20System%20Design.html#69-cloud-building-blocks-an-aws-service-map)

This chapter is the **practice layer**: the diagram, worked example, exercises, mini-project, design prompt, open-source reading, interview questions and checklist below.

---

## Prereqs

* [Chapter 2 — Capacity Planning](ch02-capacity-planning.md)
* [Chapter 3 — Scalability & Reliability Fundamentals](ch03-scalability-and-reliability-fundamentals.md)
* [Vol 1 Ch 44 — Delivery: Load Balancing, Reverse Proxies & CDN](../volume-1-cs-foundations/ch44-delivery-load-balancing-reverse-proxies-and-cdn.md)

---

## Diagram

**A reference architecture on a cloud provider with managed services**

```mermaid
flowchart TB
    U[users] --> DNS["Route 53 / Cloud DNS"] --> CDN["CloudFront / Cloud CDN + WAF"]
    CDN --> S3S[("static site bucket")]
    CDN --> APIGW["API gateway / ALB"]
    subgraph VPC["VPC (3 availability zones)"]
      subgraph Private["private subnets"]
        APP["API: containers<br/>(ECS Fargate / Cloud Run)<br/>autoscaling 2–40"]
        WK["workers (containers, spot)"]
        RDS[("managed Postgres<br/>Multi-AZ")]
        RED[("managed Redis")]
      end
      NAT["NAT gateway"]
      VPCE["VPC endpoints (S3, SQS, KMS)"]
    end
    APIGW --> APP
    APP --> RDS & RED
    APP --> Q[("SQS / Pub/Sub")] --> WK
    WK --> OBJ[("object storage")]
    APP & WK --> VPCE
    APP --> OBS["logs · metrics · traces"]
```

**Choosing compute**

```mermaid
flowchart TD
    Q1{"event glue, cron, webhooks,<br/>or very spiky low traffic?"} -- yes --> FN["functions"]
    Q1 -- no --> Q2{"a normal HTTP service or worker,<br/>small team, wants low ops?"}
    Q2 -- yes --> SC["serverless containers<br/>(Cloud Run / Fargate)"]
    Q2 -- no --> Q3{"many services, custom networking,<br/>GPUs, steady heavy load,<br/>a platform team?"}
    Q3 -- yes --> K8S["Kubernetes (managed)"]
    Q3 -- no --> VM["VMs with autoscaling groups"]
```

**Mapping a monolith to cloud services (lift → reshape)**

```
 on-prem monolith box                     cloud
 ┌────────────────────────┐
 │ nginx                  │  ──►  ALB / API gateway + CDN
 │ app (Django)           │  ──►  containers (Fargate / Cloud Run), 3 AZs
 │ cron jobs              │  ──►  EventBridge Scheduler / Cloud Scheduler → a job
 │ Celery + RabbitMQ      │  ──►  SQS / Pub/Sub + workers
 │ Postgres on the box    │  ──►  RDS / Cloud SQL (Multi-AZ, PITR)
 │ Redis                  │  ──►  ElastiCache / Memorystore
 │ /var/uploads           │  ──►  S3 / GCS (+ presigned URLs)
 │ logs in files          │  ──►  CloudWatch / Cloud Logging + OTel
 └────────────────────────┘
```

---

## Example

**API gateway → serverless/containers → managed DB/cache (Terraform excerpt, AWS)**

```hcl
resource "aws_ecs_service" "api" {
  name            = "api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  launch_type     = "FARGATE"
  desired_count   = 3
  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.api.id]
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
}

resource "aws_db_instance" "main" {
  engine                  = "postgres"
  engine_version          = "16"
  instance_class          = "db.r7g.large"
  multi_az                = true
  storage_encrypted       = true
  backup_retention_period = 14
  db_subnet_group_name    = aws_db_subnet_group.private.name
  publicly_accessible     = false
}

resource "aws_elasticache_replication_group" "cache" {
  replication_group_id       = "api-cache"
  description                = "api cache"
  node_type                  = "cache.r7g.large"
  num_cache_clusters         = 2
  automatic_failover_enabled = true
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
}
```

```python
# Serverless vs container cost model — plug in your own numbers
def lambda_cost(req_per_month, ms=100, mb=512):
    gb_s = req_per_month * (ms / 1000) * (mb / 1024)
    return gb_s * 0.0000166667 + req_per_month / 1e6 * 0.20

def container_cost(req_per_month, rps_per_task=200, task_month=50.0, min_tasks=2):
    avg_rps = req_per_month / (30 * 24 * 3600)
    tasks = max(min_tasks, -(-avg_rps // rps_per_task))    # ceiling division
    return tasks * task_month

for m in (1e6, 50e6, 500e6, 5e9):
    print(f"{m/1e6:>6.0f}M req/mo  lambda ${lambda_cost(m):>9,.0f}   containers ${container_cost(m):>6,.0f}")
#      1M req/mo  lambda $        1   containers $   100
#     50M req/mo  lambda $       52   containers $   100
#    500M req/mo  lambda $      517   containers $   100
#   5000M req/mo  lambda $    5,167   containers $   500
```

---

## Exercises

1. Map a monolith to cloud services.

   <details><summary>Solution</summary>See the mapping above. Order: (1) lift the app into containers behind a managed LB, move the DB to a managed service with Multi-AZ and PITR, and move files to object storage; (2) move cron and queues to managed schedulers and queues; (3) add a CDN and WAF; (4) put everything in IaC with observability; (5) only then consider splitting services where scaling or team boundaries demand it.</details>

2. Compare serverless vs container costs for a workload.

   <details><summary>Solution</summary>Model monthly requests, duration, memory, and the traffic shape. Run the cost model above with real prices: at 1–50M requests per month, functions are cheaper (and scale to zero); somewhere in the hundreds of millions of steady requests, containers win. Add hidden costs: API gateway fees per request, NAT and data transfer, cold-start impact on SLOs, and the engineering time for each option.</details>

3. Why put the database in private subnets with `publicly_accessible = false`?

   <details><summary>Solution</summary>It removes an entire attack surface: the database can't be reached from the internet at all, only from app security groups inside the VPC. Credential leaks or database zero-days then require a foothold inside the network first. Admins connect through SSM Session Manager, a bastion, or an identity-aware proxy.</details>

---

## Mini project

**A cost-estimate + architecture diagram for a service on a cloud provider.**

```mermaid
flowchart LR
    REQ["requirements:<br/>10k DAU, 50 rps avg / 400 peak,<br/>1 TB of files, 99.9% SLO"] --> ARCH["architecture diagram<br/>(Mermaid / draw.io)"]
    ARCH --> TF["Terraform skeleton"] --> IC["infracost breakdown"]
    ARCH --> CALC["cost sheet: compute, DB, cache,<br/>storage, transfer, observability"]
    IC & CALC --> ALT["2 alternatives:<br/>serverless-first vs containers"] --> ADR["ADR: the choice + trade-offs"]
```

**Steps**

1. Write requirements (traffic, data size, SLO, compliance).
2. Draw the architecture with managed services across 2–3 AZs.
3. A Terraform skeleton for the main resources; run `infracost breakdown`.
4. Build a cost sheet including easily forgotten items (NAT processing, egress, logs, backups).
5. Design an alternative (serverless-first) and cost it too.
6. Write an ADR choosing one, with the break-even point where you'd switch.

**Done when:** you have a diagram, a monthly estimate within ±30% for each option, and an ADR explaining the choice.

---

## Design

**Design a serverless image-processing pipeline.**

Requirements: users upload images (up to 25 MB); generate 4 sizes plus WebP; detect NSFW content; 1M uploads/day with peaks of 200/s; results available within 10 s p95; pay close to zero when idle.

```mermaid
flowchart LR
    C["client"] -->|"1. POST /uploads"| API["API Gateway + Lambda:<br/>auth, create a presigned PUT URL"]
    C -->|"2. PUT the file directly"| RAW[("S3 raw bucket")]
    RAW -->|"3. ObjectCreated event"| Q[("SQS queue<br/>(buffers the peaks)")]
    Q --> RES["Lambda: resize + WebP<br/>(concurrency limit 300)"]
    Q --> MOD["Lambda: moderation<br/>(managed vision API)"]
    RES --> OUT[("S3 variants bucket")]
    MOD --> DDB[("DynamoDB: image status")]
    RES --> DDB
    Q -. "3 failures" .-> DLQ[("DLQ + alarm")]
    OUT --> CDN["CloudFront"] --> V["viewers"]
    C -->|"4. poll / WebSocket for status"| DDB
```

**Decisions to justify**

* **Presigned uploads**: the file goes straight to S3; Lambda never handles 25 MB bodies (API Gateway payload limits make that impossible anyway).
* **SQS between S3 and the workers** absorbs peaks, gives retries and a DLQ, and lets you cap Lambda concurrency so downstream APIs aren't overwhelmed.
* **Idempotent processing** keyed by the object key and version: S3 events are at-least-once.
* **Capacity:** 200 uploads/s × ~2 s of processing ≈ 400 concurrent executions at peak (set reserved concurrency; request a limit increase if needed). Memory ~2 GB for image libraries (a faster CPU comes with more memory in Lambda).
* **Cost:** 1M/day × 2 s × 2 GB ≈ 4M GB-s/day ≈ $67/day of compute at list price, and near zero when idle. Compare with a container fleet sized for the peak.
* **Status in DynamoDB** (on-demand capacity) keyed by image ID; the client polls or subscribes.
* **Limits to watch:** Lambda's 15-minute timeout and `/tmp` size; very large images or video → Fargate tasks instead.

---

## Open source

* [`serverless/serverless`](https://github.com/serverless/serverless) — a framework for defining functions, events, and resources; compare with AWS SAM, SST, and Terraform modules.
* [`aws/aws-sdk`](https://github.com/aws/aws-sdk) — the SDK specs; the AWS, Google Cloud, and Azure "Well-Architected" / "Architecture Framework" docs are the reference checklists.

---

## Interview

1. **"Serverless vs containers — when each?"**
   <details><summary>Answer</summary>Serverless functions for event-driven glue, scheduled jobs, webhooks, and spiky or low-traffic APIs — you pay per use, scale to zero, and have almost no ops, but you accept cold starts, time limits, and per-request pricing that gets expensive at high steady volume. Containers for long-running or steady high-traffic services, custom runtimes, and portability — more control and a lower unit cost at scale, with more to operate (less with serverless containers like Cloud Run or Fargate). Decide with a cost model and the latency SLO.</details>

2. **"How do you control cloud cost?"**
   <details><summary>Answer</summary>Design for it (right service per workload, autoscaling, scale to zero where possible, keep traffic in-zone, a CDN for egress); make it visible (tags, per-team and per-service dashboards, unit cost per request or customer, budgets and anomaly alerts); optimize continuously (right-size, commitments for the steady baseline, spot for interruptible work, storage lifecycle, delete idle resources); and review cost in design reviews and PRs (Infracost). See <a href="ch21-cost-and-capacity-economics.md">Ch 20</a>.</details>

---

## Checklist

- [ ] use managed services where sensible
- [ ] design for cost
- [ ] avoid vendor lock-in where it matters

---

> [Contents](index.md) · ← [Chapter 19 — Authentication & Authorization in System Design](ch19-authentication-and-authorization-in-system-design.md) · Next → [Chapter 21 — Cost & Capacity Economics](ch21-cost-and-capacity-economics.md)
