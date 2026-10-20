# Mastering Scalability in System Design

Scalability is the backbone of robust modern systems — enabling web applications, APIs, and microservices to gracefully handle growth in users, data, and workload.

In this chapter, we'll explore the **core principles, strategies, common pitfalls, and best practices** for designing scalable systems — drawing from theory and real-world cloud solutions. You'll learn vertical/horizontal/diagonal scaling, load balancing, autoscaling, and cost optimization.

---

## 6.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Choose between vertical, horizontal, and diagonal scaling for a given growth pattern.
2. Apply **Amdahl's Law** and recognize the limits of parallelism.
3. Design **stateless services** that scale horizontally without coordination.
4. Use **circuit breakers, bulkheads, and rate limiting** to prevent cascading failures.
5. Estimate capacity for a service from QPS, latency, and resource limits.

---

## Table of Contents

- [6.2 What is Scalability?](#62-what-is-scalability)
- [6.3 Why Systems Need to Scale](#63-why-systems-need-to-scale)
- [6.4 Types of Scalability](#64-types-of-scalability)
- [6.5 Common Challenges in Scaling](#65-common-challenges-in-scaling)
- [6.6 Scaling Strategies — A Deep Dive](#66-scaling-strategies--a-deep-dive)
- [6.7 Load Balancing — The Backbone of Scalability](#67-load-balancing--the-backbone-of-scalability)
- [6.8 Autoscaling in Cloud Environments](#68-autoscaling-in-cloud-environments)
- [6.9 Cloud Building Blocks: An AWS Service Map](#69-cloud-building-blocks-an-aws-service-map)
- [6.10 Monitoring & Proactive Scaling](#610-monitoring--proactive-scaling)
- [6.11 Cost Optimization Strategies](#611-cost-optimization-strategies)
- [6.17 Combined Tips & Tricks](#617-combined-tips--tricks)
- [6.18 Sample Interview Questions](#618-sample-interview-questions)
- [6.19 Key Takeaways](#619-key-takeaways)
- [6.20 Further Reading](#620-further-reading)

---

## 6.2 What is Scalability?

> **Scalability** is the capability of a system to handle an increasing load — or its potential to accommodate growth — without sacrificing performance, reliability, or availability.

A scalable system won't break, slow down, or become unreliable as more users come online or data volumes grow. Whether it's 1,000 users or 1 million, a well-designed system maintains its SLAs and keeps the user experience smooth.

**Key properties:**

- Maintains throughput and latency under growing traffic.
- Avoids downtime or service degradation.
- Grows efficiently without massive re-engineering.

---

## 6.3 Why Systems Need to Scale

- **User base growth:** Viral success or global expansion increases the number of users dramatically.
- **Data volume explosion:** IoT, analytics, and sensors can generate data that grows exponentially.
- **Peak events:** Black Friday, ticket sales, news spikes, or viral trends cause sudden traffic surges.
- **Service Level Agreements (SLAs):** Meet strict performance (e.g., <200ms response) and uptime targets (e.g., 99.99%).
- **Avoid downtime:** Unscalable systems crash or slow down under pressure, causing user churn.
- **Expanding to new regions or markets.**

---

## 6.4 Types of Scalability

There are three main ways to scale a system.

### 6.4.1 Vertical Scaling ("Scaling Up")

Add more resources (CPU, RAM, Disk) to a single server.

```mermaid
flowchart TD
    A[User Requests] --> B[Load Balancer]
    B --> C["Powerful Server (CPU↑, RAM↑)"]
```

A simpler view:

```mermaid
graph TD
    A[User Requests] --> B[Single Server]
    B --> C[Database]
```

**Pros:**

- Simple to implement.
- Fast upgrades.
- No need for distributed coordination.

**Cons:**

- Physical hardware caps.
- Single point of failure (SPOF).
- Costly at scale.

**Example: Upgrading an AWS EC2 instance:**

```bash
aws ec2 modify-instance-attribute --instance-id i-1234567890abcdef0 --instance-type "{\"Value\": \"t3.2xlarge\"}"
```

### 6.4.2 Horizontal Scaling ("Scaling Out")

Add more servers/nodes, distributing traffic and workload.

```mermaid
flowchart TD
    A[User Requests] --> B[Load Balancer]
    B --> C1[Server 1]
    B --> C2[Server 2]
    B --> C3[Server 3]
```

A more detailed version showing the shared database:

```mermaid
graph TD
    A[User Requests] --> LB[Load Balancer]
    LB --> S1[Server 1]
    LB --> S2[Server 2]
    LB --> S3[Server 3]
    S1 & S2 & S3 --> D[(Shared Database)]
```

**Pros:**

- High resilience and availability.
- Can scale indefinitely.
- Parallelism, redundancy.

**Cons:**

- Requires stateless design or careful coordination.
- Needs load balancers.
- Complex setup (data consistency, replication).

**Example: Kubernetes Horizontal Pod Autoscaler (HPA) YAML:** *(Kubernetes runs your containers across many machines; the HPA adds or removes copies of a container as load changes.)*

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 6.4.3 Diagonal Scaling (Hybrid)

Begin with vertical scaling for simplicity; transition to horizontal as needed. Common in cloud-native apps.

```mermaid
flowchart LR
    A[Start: Small Server] --Upgrade--> B[Bigger Server]
    B --Add More Servers--> C{Clustered Servers}
```

A two-phase view:

```mermaid
graph TD
    subgraph Phase1 [Phase 1: Vertical]
        A1[User Requests] --> S1v[Single Powerful Server]
    end
    subgraph Phase2 [Phase 2: Horizontal]
        A2[User Requests] --> LBd[Load Balancer]
        LBd --> S2v[Upgraded Server 1]
        LBd --> S3v[Upgraded Server 2]
    end
```

*Start vertical, then scale horizontally as needed.*

A single-graph view of all 3 types:

```mermaid
graph TB
    A[Start] --> B["Vertical Scaling (Upgrade existing server)"]
    A --> C["Horizontal Scaling (Add more servers)"]
    A --> D["Diagonal Scaling (Upgrade, then add servers)"]
```

**Real-world examples:**

- **AWS Lambda:** Starts small (vertical), but can auto-scale (horizontal) based on demand.
- **Twitter:** From monolith (vertical) to microservices (horizontal) as user base grew.

### 6.4.4 Scaling Types — Comparison

A summary of all three types side-by-side:

| Scaling Type      | Approach                                  | Pros                | Cons                           |
|-------------------|-------------------------------------------|---------------------|--------------------------------|
| Vertical Scaling  | Upgrade single machine (CPU/RAM/Disk)     | Simple, fast        | Physical limits, SPOF*         |
| Horizontal Scaling| Add more machines/nodes                   | Resilient, scalable | Complex architecture           |
| Diagonal Scaling  | Start vertical, then add horizontal nodes | Flexible, cost-wise | Hybrid (must manage both)      |

> *SPOF: Single Point of Failure.

A version focused on pros/cons:

| Type              | Description                              | Pros                        | Cons                       |
|-------------------|------------------------------------------|-----------------------------|----------------------------|
| **Vertical**      | Add resources (CPU/RAM) to a single node | Simple, fast upgrades       | Physical limits, SPOF      |
| **Horizontal**    | Add more nodes/servers                   | High resilience, big scale  | Complex, needs LB/replica  |
| **Diagonal**      | Start vertical, then go horizontal       | Flexible, cost-efficient    | Coordination complexity    |

### 6.4.5 Trade-Offs: Cost, Complexity, and Performance

|   Strategy   | Cost (Initial) | Cost (Growth) | Complexity | Performance       |
|--------------|----------------|---------------|------------|-------------------|
| Vertical     | Low            | High          | Low        | High (initial)    |
| Horizontal   | Medium         | Linear        | High       | High (scalable)   |
| Diagonal     | Balanced       | Balanced      | Medium     | Balanced          |

**Summary:**

- **Vertical scaling** is easy and cheap to start, but gets expensive and risky at scale.
- **Horizontal scaling** is robust and future-proof, but requires orchestration, monitoring, and stateless patterns.
- **Diagonal scaling** gives early simplicity and long-term scalability, favored by modern cloud-native architectures.

---

## 6.5 Common Challenges in Scaling

| Challenge   | Description                                              | Example                        |
|-------------|----------------------------------------------------------|--------------------------------|
| Latency     | Delay in response due to distributed components          | Microservices, DB hops         |
| Bottlenecks | Slowest service limits overall throughput                | Locked DB, single-threaded job |
| Downtime    | More servers = more potential failure points             | Outages during deployments     |
| Cost        | More resources = higher bills (especially in cloud)      | Over-provisioned instances     |

---

## 6.6 Scaling Strategies — A Deep Dive

### 6.6.1 When to Use Which Strategy?

| Approach    | When to Use                            | Real-World Example            |
|-------------|----------------------------------------|-------------------------------|
| Vertical    | MVPs, startups, low initial traffic    | Early-stage SaaS, blogs       |
| Horizontal  | High-scale apps, resilience needed     | Twitter, Facebook             |
| Diagonal    | Cloud-native with uncertain workloads  | AWS Lambda, GCP Cloud Run     |

**Real-world choices:**

- **Twitter:** Monolith → microservices (horizontal) as user base grew.
- **AWS Lambda:** Diagonal + autoscaling.
- **Startups:** Vertical first, then horizontal as needed.

### 6.6.2 Example: Setting up AWS Auto Scaling Group (Horizontal)

```bash
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --launch-configuration-name my-launch-config \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-12345678,subnet-23456789"
```

### 6.6.3 Practical Tips for Scaling Strategy Choice

- **Start simple:** Early-stage startups or MVPs should favor vertical scaling to keep things simple and cost-effective.
- **Know when to switch:** Monitor system metrics. When you approach hardware limits or need high availability, start planning horizontal or diagonal scaling.
- **Embrace statelessness:** For horizontal scaling, design services to be stateless. Use shared databases or distributed caches for state.
- **Use managed services:** Cloud providers offer powerful auto-scaling and load balancing solutions (AWS ELB, Azure Load Balancer).
- **Don't over-engineer:** Avoid building distributed systems too early. Scale complexity with actual demand.
- **Implement load balancers:** Distribute traffic, prevent overload, increase reliability.
- **Monitor proactively:** Use CloudWatch, Prometheus, or Grafana to anticipate scaling needs before issues arise.

---

## 6.7 Load Balancing — The Backbone of Scalability

Scalability is at the heart of robust system design. As user bases and data volumes grow, ensuring your application remains fast, available, and cost-effective becomes critical. One of the key enablers is **load balancing** — the art and science of distributing incoming traffic across a pool of servers.

### 6.7.1 Why Load Balancing is Essential

Imagine a high-traffic e-commerce website during Black Friday. Without load balancing, a single server could get overwhelmed, causing slowdowns or outages. With a load balancer, incoming requests are automatically spread across multiple backend servers for maximum uptime and minimum latency.

**Key benefits:**

- **High Availability:** Keeps your app running even during server failures or traffic spikes.
- **Traffic Distribution:** Prevents overload by spreading requests evenly.
- **Improved Performance:** Routes requests to the least-busy or fastest server.
- **Graceful Failure Handling:** Detects and bypasses failed servers.
- **Scalability:** Makes it easy to add or remove servers as demand changes.
- **Reduces latency for users.**

> **Real-World Example:** During a flash sale, Amazon's load balancers distribute millions of requests per second across a massive fleet of servers, ensuring shoppers never see a 503 error.

### 6.7.2 Types of Load Balancers

Load balancers can be categorized by the **network layer** they operate on and by their **deployment model**.

#### 6.7.2.1 By Network Layer

| Type                | Layer               | Examples                                |
|---------------------|---------------------|-----------------------------------------|
| Layer 4 (Transport) | TCP/UDP             | AWS NLB, HAProxy (TCP), F5              |
| Layer 7 (App)       | HTTP/HTTPS/gRPC     | AWS ALB, NGINX, Envoy, Google L7 LB     |

**Layer 4 (Transport Layer):**

- Operates at TCP/UDP level.
- Routes based on IP address and port.
- **Pros:** Blazing fast, efficient, low overhead.
- **Cons:** No content-based routing.

**Layer 7 (Application Layer):**

- Operates at HTTP/HTTPS.
- Routes based on HTTP headers, cookies, URLs, etc.
- **Pros:** Intelligent content-aware routing.
- **Cons:** Slightly more processing overhead.

#### 6.7.2.2 Diagram: Layer 4 vs Layer 7

```mermaid
flowchart LR
    Internet[Internet] --> LB4["Layer 4 LB"]
    Internet --> LB7["Layer 7 LB"]
    LB4 --> S1[Server 1]
    LB4 --> S2[Server 2]
    LB7 --> S3["Server 3 - Product Pages"]
    LB7 --> S4["Server 4 - Checkout"]

    N1["Note: Routes based on IP and port only"]
    N2["Note: Inspects HTTP path, headers, cookies"]

    LB4 -.-> N1
    LB7 -.-> N2

    classDef note fill:#fff3cd,stroke:#ffcc00,color:#000,stroke-dasharray: 3 3;
    class N1,N2 note;
```

#### 6.7.2.3 By Deployment Model

| Type                 | Examples                                          |
|----------------------|---------------------------------------------------|
| **Hardware**         | F5 BIG-IP, Citrix NetScaler                       |
| **Software**         | NGINX, HAProxy, Envoy                             |
| **Cloud-based**      | AWS ELB, Azure Load Balancer, GCP Load Balancer   |

**Hardware Load Balancers:**

- Specialized devices, used in large data centers.
- Often with SSL termination and DDoS protection.

**Software Load Balancers:**

- Apps running on commodity servers.
- Flexible, cost-effective, popular in microservices and Kubernetes.

**Cloud-based Load Balancers:**

- Managed services provided by cloud vendors.
- Handles scaling, failover, security out-of-the-box.

### 6.7.3 Load Balancing Algorithms

- **Round Robin:** Sequential distribution.
- **Least Connections:** Server with fewest active connections.
- **IP Hash:** Consistent routing based on client IP (supports sticky sessions).
- **Weighted:** Some servers get more requests based on capacity.
- **Least Response Time:** Fastest responding server.
- **Adaptive Load Balancing:** Continuously analyzes CPU, memory, and health metrics.

### 6.7.4 Code: Load Balancing Algorithms in Python

**Simple round-robin (pseudocode):**

```python
# Pseudocode: Simple Round Robin Load Balancer
servers = [srv1, srv2, srv3]
next_server = 0

def get_server():
    global next_server
    srv = servers[next_server]
    next_server = (next_server + 1) % len(servers)
    return srv
```

**Round-robin with function-level state:**

```python
servers = ['A', 'B', 'C']
idx = 0

def get_next_server():
    global idx
    server = servers[idx]
    idx = (idx + 1) % len(servers)
    return server
```

**Round-robin as a class:**

```python
class RoundRobinLB:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0

    def get_server(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

# Usage
lb = RoundRobinLB(['server1', 'server2', 'server3'])
for _ in range(6):
    print(lb.get_server())
```

Output:

```
server1
server2
server3
server1
server2
server3
```

**Least connections:**

```python
connections = {'A': 3, 'B': 1, 'C': 2}

def get_least_connections():
    return min(connections, key=connections.get)
```

**IP hashing:**

```python
import hashlib

def ip_hash(ip, servers):
    idx = int(hashlib.md5(ip.encode()).hexdigest(), 16) % len(servers)
    return servers[idx]
```

**Weighted round robin:**

```python
servers = [('A', 3), ('B', 1)]  # (server, weight)
weighted_list = [s for s, w in servers for _ in range(w)]
idx = 0

def get_weighted_server():
    global idx
    server = weighted_list[idx]
    idx = (idx + 1) % len(weighted_list)
    return server
```

### 6.7.5 Load Balancer in Action

```mermaid
sequenceDiagram
    participant User as User
    participant LB as Load Balancer
    participant S1 as Server 1
    participant S2 as Server 2
    participant S3 as Server 3

    User->>LB: HTTP Request 1
    LB->>S1: Forwards to Server 1

    User->>LB: HTTP Request 2
    LB->>S2: Forwards to Server 2

    User->>LB: HTTP Request 3
    LB->>S3: Forwards to Server 3

    Note right of LB: Monitors server health, reroutes if one fails
```

A simpler view:

```mermaid
graph LR
    Client1 --> LB[Load Balancer]
    Client2 --> LB
    LB --> S1[Server 1]
    LB --> S2[Server 2]
    LB --> S3[Server 3]
```

**Handling failures gracefully:** If Server 2 crashes, the load balancer detects this via health checks and reroutes all new traffic to Server 1 and Server 3 only, preserving high availability.

### 6.7.6 Sample NGINX Load Balancer Config

```nginx
http {
    upstream backend {
        server backend1.example.com weight=3;
        server backend2.example.com weight=2;
        server backend3.example.com weight=1;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend;
        }
    }
}
```

### 6.7.7 Choosing a Load-Balancing Algorithm for the Workload

| Workload | Algorithm | Why |
|----------|-----------|-----|
| Short, uniform requests; identical servers | round robin or weighted round robin | simple and even |
| Long or variable requests (uploads, reports, streaming) | **least connections** or least outstanding requests | adapts to the real load |
| Latency-sensitive services, large fleets | **power of two choices (P2C)**: pick two backends at random and send the request to the one with lower load or latency | near-optimal results with no global state |
| **Cache or state affinity** (sharded caches, per-user state, WebSocket rooms) | **consistent hashing** (hash ring, Maglev, rendezvous) | the same key reaches the same backend, with minimal remapping when backends change |
| Hot keys under consistent hashing | consistent hashing **with bounded loads** | caps any one backend at, say, 1.25× the average |
| Canary releases and A/B tests | weighted routing by percentage or header | controlled exposure |

**Why consistent hashing?** With `hash(key) % N`, adding one server remaps almost every key, which empties every cache at once. On a hash ring, adding one server to N moves only about 1/(N+1) of the keys.

### 6.7.8 Health Checks in Depth

| Type | How it works | What it catches |
|------|--------------|-----------------|
| **Active** | the balancer probes a `/readyz` endpoint every few seconds, with rise and fall thresholds | dead or not-yet-ready nodes |
| **Passive** (outlier detection) | eject backends that return 5xx errors or time out on real traffic | "gray failures" that active checks miss |
| **Shallow vs. deep** | deep checks also test dependencies such as the database | deep checks can **cascade**: one database blip ejects every node at once, so keep readiness about the node itself |

**Connection draining.** When a backend is removed or deployed, stop sending it new requests but let in-flight ones finish before shutting it down, so users do not see errors during rollouts.

### 6.7.9 From Nothing to a Running Server: SSH, a Runtime and a Process Manager

Before you can put anything behind a load balancer, you need one working server. This walk-through shows the manual steps on any cloud provider (the first-server experience on DigitalOcean, AWS, Google Cloud and others is nearly identical). A server like this is called a **virtual private server (VPS)**; DigitalOcean calls it a *droplet*, AWS an *EC2 instance*.

**1. Create the server.** Choose a **region** near your users, an operating system (Ubuntu is the common default), and a size. Choose **SSH key** login rather than a password.

**2. Why SSH keys beat passwords.** A password can be guessed or stolen; an SSH key is a long random **key pair**. The public half sits on the server, the private half stays on your machine and is never sent. Only someone holding the private key can log in.

```bash
ssh-keygen -t ed25519 -C "me@laptop"      # creates a private and a public key
# paste the public key (~/.ssh/id_ed25519.pub) into the provider's console
ssh root@203.0.113.10                      # log in to the new server (or use the provider's web console)
```

You are now in a remote computer with only a terminal and no graphical interface.

**3. Install what the app needs.** A fresh server has no language runtime or Git:

```bash
sudo apt update && sudo apt install -y git
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash   # Node version manager
source ~/.bashrc && nvm install 22
git clone https://github.com/you/user-management.git && cd user-management
npm install && node server.js              # works, but stops when you close the terminal
```

**4. Keep it running with a process manager.** Running `node server.js` by hand dies when the terminal closes or the app crashes. A **process manager** restarts crashed apps and starts them at boot. **PM2** is the common one for Node; **systemd** does the same job for any program.

```bash
npm install -g pm2
pm2 start server.js --name users          # runs in the background, restarts on a crash
pm2 save                                   # remember the process list
pm2 startup                                # prints a command; run it so PM2 itself starts at boot
pm2 logs users                             # read the app's output
```

**5. Make it safe to expose.** The app listens on a high port such as 3000, which visitors should not see.

- Put **NGINX** (a reverse proxy, see Chapter 2) on ports 80 and 443 and forward to `localhost:3000`, so users just use the domain name.
- Turn on the **firewall** and open only what is needed: `ufw allow OpenSSH`, `ufw allow 80,443/tcp`, then `ufw enable`.
- Keep the operating system patched and disable password login for SSH.

**6. Clone it.** Once one server works, take a **snapshot** (a saved copy of the whole disk) and launch a second server from it. This is the fastest way to get an identical machine for the load-balancer lab below, and it is why scalable systems treat servers as **disposable and reproducible** (see the containers primer in Chapter 4).

### 6.7.10 Hands-On Lab: Put a Load Balancer in Front of Two Servers

Seeing a load balancer work makes the theory stick. This lab needs only Docker and runs on your own machine.

**Goal:** run two identical servers behind NGINX, watch requests alternate, then stop one server and watch traffic keep flowing.

**1. Create a network and two servers** (each replies with its own name):

```bash
docker network create labnet
docker run -d --name app1 --network labnet hashicorp/http-echo -text="hello from app1"
docker run -d --name app2 --network labnet hashicorp/http-echo -text="hello from app2"
```

**2. Write the load balancer config** as `nginx.conf` in the current folder:

```nginx
upstream backend {
    server app1:5678;
    server app2:5678;
}
server {
    listen 80;
    location / { proxy_pass http://backend; }
}
```

**3. Start NGINX and send traffic:**

```bash
docker run -d --name lb --network labnet -p 8080:80 \
  -v "$PWD/nginx.conf:/etc/nginx/conf.d/default.conf:ro" nginx:alpine

for i in 1 2 3 4 5 6; do curl -s localhost:8080; done
```

You should see `hello from app1` and `hello from app2` taking turns: that is **round robin**.

**4. Try the strategies** from this chapter by editing `nginx.conf` and reloading (`docker exec lb nginx -s reload`):

- `least_conn;` as the first line inside `upstream` for **least connections**
- `ip_hash;` for **IP hashing** (one client now sticks to one server)
- `server app1:5678 weight=3;` for **weighted** balancing (app1 gets about three times the traffic)

**5. Test failure handling:**

```bash
docker stop app1
for i in 1 2 3 4; do curl -s localhost:8080; done   # every answer comes from app2
docker start app1                                    # it rejoins automatically
```

**6. Clean up:** `docker rm -f lb app1 app2 && docker network rm labnet`.

**The same idea in a cloud console** (any provider): create a server and install your app; take a **snapshot** and launch a **clone** from it; create a **load balancer** in the same network and region; add both servers as targets; define a **forwarding rule** (for example port 80 to port 80) and a **health check**; then open the load balancer's address, refresh repeatedly and check its metrics. This is the same flow you just did locally.

### 6.7.11 Choosing the Right Load Balancer

- **Layer 4:** Choose for raw speed and lower-level TCP/UDP traffic.
- **Layer 7:** Choose for intelligent routing (APIs, microservices).
- **Software:** Great for flexible, cost-effective deployments.
- **Hardware:** Enterprise-grade performance, in data centers.
- **Cloud:** Seamless scaling, built-in security, minimal management.

**Other considerations:**

- **SSL Termination:** Offload CPU-heavy encryption from backend servers.
- **DDoS Protection:** Many cloud/hardware LBs provide built-in attack mitigation.
- **Session Persistence:** Use IP hashing or sticky sessions if needed.

### 6.7.12 Load Balancing — Tips & Best Practices

- **Always set up health checks** for your backend servers.
- **Prefer stateless backend design** for easier load balancing.
- **Monitor metrics** like connection counts, response times, error rates.
- **For microservices**, consider using a service mesh (Istio, Linkerd) for advanced L7 routing.
- **Enable SSL termination** at the load balancer to reduce backend CPU load.
- **Use autoscaling** in conjunction with load balancing for elastic capacity.
- **Choose the right strategy** based on traffic patterns and backend capabilities.
- **Combine load balancing with autoscaling** for true elasticity in the cloud.
- **Monitor, test, and iterate** — don't "set and forget" your load balancer.

---

## 6.8 Autoscaling in Cloud Environments

In modern cloud architecture, **autoscaling** is a core technique for building highly available, cost-effective, and resilient systems.

### 6.8.1 What is Autoscaling?

**Autoscaling** is the **automatic adjustment of compute resources** (servers, containers, or functions) in response to real-time demand.

- **Objective:** Maintain performance and availability while optimizing costs.
- **Common use cases:** Microservices, web applications, event-driven systems, batch processing.

> *"Autoscaling plays a critical role in keeping system performance available and cost-efficient, especially where demand can vary drastically and unpredictably."*

### 6.8.2 How Autoscaling Works

Autoscaling decisions are **triggered by metrics** such as:

- **CPU usage**
- **Memory consumption**
- **Request rate**
- **Queue length**
- **Custom business KPIs**

### 6.8.3 Autoscaling Types

| Type               | Description                                                      | Example                |
|--------------------|------------------------------------------------------------------|------------------------|
| **Horizontal**     | Add/remove instances (scale out/in)                              | Add EC2 VMs/Pods       |
| **Vertical**       | Resize a single instance (scale up/down)                         | Add CPU/RAM to server  |
| **Diagonal**       | Start vertical, then add horizontal as needed (hybrid approach)  | Cloud-native workloads |

**Diagram: Scaling Types**

```mermaid
graph TD
    A[Vertical Scaling] -->|Add CPU/RAM| B[Single Server]
    A2[Horizontal Scaling] -->|Add Servers| C[Multiple Servers]
    A3[Diagonal Scaling] -->|Start vertical, then add servers| D[Hybrid]
```

### 6.8.4 Scaling Policies

- **Reactive Scaling:** Triggers when specific metrics cross thresholds (e.g., CPU > 80%).
- **Predictive Scaling:** Uses historical trends and ML to forecast and scale *before* demand spikes.
- **Scheduled Scaling:** Scales resources at set times based on known traffic patterns (e.g., daily peaks, Black Friday).

### 6.8.5 Autoscaling Across Major Cloud Providers

All major clouds offer first-class autoscaling features.

| Provider | Autoscaling Services                                                                      |
|----------|-------------------------------------------------------------------------------------------|
| AWS      | EC2 Auto Scaling Groups, Lambda, ECS, EKS                                                 |
| Azure    | VM Scale Sets, App Service Plans, AKS                                                     |
| GCP      | Managed Instance Groups (MIGs), Cloud Run, GKE, Functions                                 |

A more detailed view:

| Cloud  | Compute Autoscaling                | Container Autoscaling             | Monitoring / Metrics     |
|--------|------------------------------------|-----------------------------------|--------------------------|
| **AWS**   | EC2 Auto Scaling Groups, Lambda | ECS, EKS (Kubernetes) Autoscaling | CloudWatch               |
| **Azure** | VM Scale Sets, App Service Plans| AKS (Kubernetes) Autoscaling      | Azure Monitor            |
| **GCP**   | Managed Instance Groups, Functions | Cloud Run, GKE Autoscaling     | Stackdriver/Operations   |

### 6.8.6 Example: AWS EC2 Auto Scaling Group (CloudFormation YAML)

```yaml
Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: '2'
      MaxSize: '10'
      DesiredCapacity: '2'
      LaunchConfigurationName: !Ref MyLaunchConfig
      TargetGroupARNs:
        - !Ref MyTargetGroup
      MetricsCollection:
        - Granularity: "1Minute"
```

A version with tags:

```yaml
Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 4
      LaunchConfigurationName: !Ref MyLaunchConfig
      TargetGroupARNs:
        - !Ref MyTargetGroup
      MetricsCollection:
        - Granularity: "1Minute"
      Tags:
        - Key: Name
          Value: MyASGInstance
          PropagateAtLaunch: true
```

### 6.8.7 Example: Azure VM Scale Set (CLI)

```bash
az vmss create \
  --resource-group myResourceGroup \
  --name myScaleSet \
  --image UbuntuLTS \
  --upgrade-policy-mode automatic \
  --custom-data cloud-init.txt \
  --admin-username azureuser

az vmss autoscale create \
  --resource-group myResourceGroup \
  --name myAutoscaleSetting \
  --vmss-name myScaleSet \
  --min-count 2 --max-count 10 --count 2
```

### 6.8.8 Example: GCP Managed Instance Group (gcloud)

```bash
gcloud compute instance-groups managed create my-group \
  --base-instance-name my-instance \
  --template my-instance-template \
  --size 2 \
  --zone us-central1-a

gcloud compute instance-groups managed set-autoscaling my-group \
  --max-num-replicas 10 \
  --min-num-replicas 2 \
  --target-cpu-utilization 0.75 \
  --cool-down-period 90
```

---

## 6.9 Cloud Building Blocks: An AWS Service Map

> **Why this is here:** case studies and interviews name cloud services constantly. This map groups the common Amazon Web Services by the job they do, so each name has a place in your head. Other clouds have equivalents (Google Cloud, Azure); the **jobs** are the same.

| Job | Services | Plain meaning |
|-----|----------|---------------|
| **DNS and edge** | **Route 53**, **CloudFront** | DNS with health checks and routing; a CDN that caches content near users |
| **Edge security** | **WAF**, **Shield** | filter malicious requests; absorb DDoS floods |
| **API front door and sign-in** | **API Gateway**, **Cognito** | one entry point with throttling and auth; managed user sign-up, login and tokens (OpenID Connect) |
| **Load balancing** | **Elastic Load Balancing** (ALB for HTTP, NLB for raw TCP/UDP) | spread traffic across servers |
| **Compute** | **EC2**, **ECS / EKS**, **Fargate**, **Lambda** | virtual servers; container orchestration (Docker / Kubernetes); containers without managing servers; functions that run on demand |
| **Queues and events** | **SQS**, **SNS**, **EventBridge**, **Kinesis**, **Step Functions** | message queue; publish/subscribe fan-out; event routing; streaming log; workflow orchestration |
| **Relational databases** | **RDS**, **Aurora** | managed MySQL/PostgreSQL and others; a cloud-built MySQL/PostgreSQL-compatible engine with faster failover and replicas |
| **NoSQL and search** | **DynamoDB**, **OpenSearch** | key-value/document store at massive scale; search and log analytics |
| **Caching** | **ElastiCache**, **MemoryDB** | managed Redis/Memcached cache; a durable Redis-compatible in-memory database |
| **Storage** | **S3**, **EBS**, **EFS** | object storage; block storage for one server; shared network file system |
| **Config and secrets** | **AppConfig**, **Secrets Manager**, **Parameter Store**, **KMS** | feature flags and runtime config; store passwords and keys; encryption keys |
| **Identity and access** | **IAM** | who and what may call which AWS API |
| **Observability** | **CloudWatch**, **X-Ray** | metrics, logs and alarms; distributed tracing |

### 6.9.1 A Typical Web Request Path

```mermaid
flowchart TB
    U([User]) --> R53["Route 53 (DNS)"] --> CF["CloudFront CDN"] --> WAF["WAF"] --> GW["API Gateway or ALB"]
    GW --> COG["Cognito checks the token"]
    GW --> SVC["Service on ECS, EKS or Lambda"]
    SVC --> CACHE[("ElastiCache")]
    SVC --> DB[("Aurora / RDS")]
    SVC --> CW["CloudWatch logs and metrics"]
    SVC --> Q[["SQS queue"]] --> W["Worker service"] --> S3[("S3")]
```

### 6.9.2 Choosing Between Look-Alikes

| Question | Guidance |
|----------|----------|
| EC2 vs containers vs Lambda | EC2 for full control; containers for steady services that scale; Lambda for spiky or event-driven work with short runtimes |
| SQS vs SNS vs EventBridge vs Kinesis | SQS: one consumer group pulls work; SNS: push to many subscribers; EventBridge: route events by rules between services and SaaS; Kinesis: ordered, replayable stream |
| ElastiCache vs MemoryDB | ElastiCache when losing the cache is acceptable (it is a copy of data); MemoryDB when it must be the durable primary store |
| RDS vs Aurora vs DynamoDB | RDS for standard relational needs; Aurora for higher scale and faster failover; DynamoDB for key-based access at huge scale with no joins |
| Secrets Manager vs Parameter Store vs AppConfig | secrets with rotation; simple config values; feature flags and gradual config rollout |

> **Interview habit:** name the *job* first ("a managed queue"), then the product ("SQS"), and say what you would trade away by picking it.

## 6.10 Monitoring & Proactive Scaling

Effective autoscaling depends on robust monitoring.

- **Key Metrics:** CPU, memory, network, queue depth, custom KPIs.
- **Tools:** AWS CloudWatch, Prometheus, Azure Monitor, GCP Operations, Grafana.
- **Proactive Scaling:** Use ML/trends to *forecast* demand, not just react.
- **Scheduled Scaling:** Predefine scaling windows for known peak times (Black Friday, daily traffic patterns).

---

## 6.11 Cost Optimization Strategies

Cloud costs can spiral if autoscaling is not managed carefully. Best practices:

| Strategy                       | Description                                                          |
|--------------------------------|----------------------------------------------------------------------|
| **Avoid Over-provisioning**    | Scale just enough for demand; avoid idle resources.                  |
| **Use Spot/Preemptible VMs**   | For batch/non-critical workloads; up to 80% cheaper.                 |
| **Set Resource Limits/Quotas** | Prevent runaway scaling, especially in dev/test environments.        |
| **Rightsize Regularly**        | Analyze actual usage and adjust resource size accordingly.           |
| **Auto-pausing/Scale-to-zero** | Use features that pause/stop idle services (e.g., Cloud Run, Lambda) |

---

## 6.12 The Fundamental Laws

### 6.12.1 Amdahl's Law — Why Adding Servers Doesn't Linearly Scale

If 95% of a workload is parallelizable and 5% is serial, the **maximum speedup is 20×** — no matter how many machines you throw at it.

```
Speedup ≤  1 / ((1 - P) + P/N)
where P = parallel fraction, N = number of processors
```

| Parallel %  | Max speedup (∞ machines) |
|-------------|-------------------------|
| 50%         | 2×                       |
| 90%         | 10×                      |
| 95%         | 20×                      |
| 99%         | 100×                     |

**Lesson:** the serial part of your system is the bottleneck. Profile to find it; eliminate it before adding more machines.

### 6.12.2 Universal Scalability Law (Gunther)

In practice, scaling is often *worse* than Amdahl predicts because of **coordination overhead** — locks, consensus, distributed transactions. There's a point past which adding more nodes makes the system *slower*. This is why "just add another microservice" doesn't always help.

---

## 6.13 Stateless Service Design

The single most important enabler of horizontal scaling. A **stateless** service holds no per-request memory between requests; any instance can serve any request.

### 6.13.1 Where to Put the State Instead

| State                   | Where it goes               | Why                                  |
|-------------------------|------------------------------|--------------------------------------|
| User session            | Redis / Memcached            | Any instance can look it up by ID    |
| File uploads in progress| Object storage with session tokens | Resumable uploads work across servers |
| In-progress workflows   | Database or workflow engine (Temporal, Step Functions) | Survives restarts          |
| WebSocket state         | Pub/Sub layer (Redis Streams, Kafka) | Any WebSocket server can deliver to any user |

> **Rule:** if your service can't be killed and restarted at any moment without users noticing, you have hidden state. Find it.

---

## 6.14 Failure Containment Patterns

Scaling isn't only about handling load — it's about preventing one failure from cascading.

### 6.14.1 Circuit Breaker

If a downstream service is failing, **stop calling it for a while** so the failing service can recover and your service doesn't waste resources waiting on timeouts.

```
States:  CLOSED  →  OPEN  →  HALF-OPEN  →  CLOSED
         (normal)   (fail fast)  (try one)  (back to normal)
```

**Implementation:** count failures in a window; trip if >N% fail; after a cooldown, allow one trial request.

### 6.14.2 Bulkhead

Isolate resources so failure in one part of the system can't drown the rest. Just like the watertight compartments on a ship — if one floods, the rest stay dry.

**Example:** dedicate separate thread pools (or connection pools) per downstream service. If the slow payment service eats all 200 threads, your auth calls still have their own pool.

### 6.14.3 Rate Limiting

Cap how many requests any one client (IP, user, API key) can send in a window. Protects against abuse *and* against your own systems thundering when something goes wrong.

**Algorithms (in order of sophistication):**

| Algorithm        | Simplicity | Burst handling | Memory cost |
|------------------|-----------|-----------------|-------------|
| Fixed window     | simplest   | bad (allows 2× burst at window edges) | tiny |
| Sliding window log | precise  | great           | high (stores timestamps) |
| Sliding window counter | balanced | good       | low |
| Token bucket     | most flexible | great (allows bursts up to bucket size) | small |
| Leaky bucket     | smoothes traffic | enforces constant rate | small |

> **Default choice:** token bucket. Easy to reason about, allows reasonable bursts, well-supported in libraries.

### 6.14.4 Backpressure

When you can't keep up, **tell upstream to slow down** rather than silently dropping or queuing forever. Standard mechanisms: HTTP 429, gRPC `RESOURCE_EXHAUSTED`, blocking writes on a bounded queue.

---

## 6.15 Rate Limiting, Throttling and Backpressure

Token bucket, leaky bucket, sliding window; distributed limits; backpressure upstream.

**In one sentence:** rate limiting caps how fast any one caller can use a resource, throttling slows callers down instead of failing them, and backpressure is the downstream system telling upstream "slow down, I'm full" — together they keep one noisy client or one traffic spike from taking everyone down.

**Mental model — a nightclub door.** The token bucket is a bouncer with a stack of wristbands that refills at a steady rate: a group can rush in if wristbands are saved up (a burst), but once they're gone, people wait. The leaky bucket is a turnstile that lets exactly one person through every few seconds no matter how many are queued. Backpressure is the bar inside telling the door "we're at capacity — stop letting people in."

**Algorithms**

| Algorithm | How | Bursts | Memory per key | Accuracy |
|-----------|-----|--------|----------------|----------|
| Fixed window counter | count per clock minute; reset at :00 | up to 2× at window edges | 1 counter | edge spikes |
| Sliding window log | store every timestamp; count those in the last 60 s | exact | O(requests) | exact |
| Sliding window counter | weighted mix of current and previous window counts | smooth | 2 counters | ~approximate, very good |
| **Token bucket** | tokens refill at rate r up to capacity b; each request takes one | **allows bursts up to b** | 2 numbers (tokens, last time) | exact for its model |
| Leaky bucket (as a queue) | requests enter a queue drained at a fixed rate | smooths bursts into a steady flow | queue | exact |
| Concurrency limit | at most N requests in flight | — | 1 counter | protects slow backends |

**Where to limit**

| Layer | Example | Protects against |
|-------|---------|------------------|
| Edge / API gateway | 100 req/min per API key | abuse, scraping, credential stuffing |
| Per tenant / plan | free: 10 rps, pro: 100 rps | noisy neighbors (Ch 15) |
| Per endpoint | login: 5/min per account+IP | brute force |
| Service to service | client-side limits, retry budgets | cascading retries |
| Around a dependency | max 50 concurrent DB queries | overload of shared resources |

**Distributed rate limiting** — with 20 gateway nodes, a limit of 100/min must be shared.

| Approach | How | Trade-off |
|----------|-----|-----------|
| Central store (Redis) | atomic `INCR` + `EXPIRE`, or a Lua script for a token bucket | accurate; adds ~1 ms and a dependency (fail open or closed?) |
| Local limits = global ÷ N | each node enforces its share | no coordination; inaccurate when traffic is uneven |
| Local + periodic sync | nodes gossip or report counts every second | approximate, fast |
| Dedicated limit service | Envoy's global rate-limit service | central policy, a gRPC hop |

**Good 429s** — return `429 Too Many Requests` with `Retry-After`, plus headers like `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`. Clients must back off with jitter; retrying immediately makes it worse.

**Backpressure** — every buffer between producer and consumer must be **bounded**. When a queue fills: block the producer (TCP flow control, bounded channels), reject new work early (load shedding with 503), drop low-priority work, or scale consumers. An unbounded queue just converts overload into latency, then into out-of-memory crashes.

## 6.16 Capacity Planning — Back-of-the-Envelope

Given:
- p99 latency budget: **100 ms**
- Each request takes: **~20 ms** of CPU
- Each server: **8 cores**

**Throughput per server:** `(8 cores × 1000 ms/s) / 20 ms ≈ 400 req/s` (ignoring I/O wait)

**At 10K req/s peak load:** `10,000 / 400 = 25 servers`, plus **+50% headroom** for spikes and rolling deploys → **40 servers**.

> **Rule of thumb:** aim for **60-70% steady-state utilization.** Higher = no margin for spikes. Lower = wasted money.

---

### 6.16.1 Capacity Estimation Cheat Sheet

Turn product numbers ("10 million daily users") into engineering numbers with quick, explicit math. Size for the **peak**, not the average, and be right within about 2×.

| Quantity | Formula or rule of thumb |
|----------|--------------------------|
| Average QPS | `daily active users × requests per user per day ÷ 86,400` |
| Peak QPS | `average × peak factor` (2–10×; 5× is a common assumption) |
| Read : write ratio | often 10:1 to 100:1 for consumer apps |
| Servers | `peak QPS ÷ QPS per server`, then add headroom (aim for about 60–70% utilization) and N+2 spare capacity for failures |
| Storage | `items per day × bytes per item × retention days × replication factor` |
| Bandwidth | `QPS × response size` |

**Numbers worth memorizing**

| Item | Value |
|------|-------|
| Seconds per day | 86,400, roughly 10⁵ |
| 1 million requests per day | about 12 QPS |
| 1 billion requests per day | about 12,000 QPS |
| One typical web/API server | about 1,000 QPS (anywhere from 100 to 10,000+) |
| One PostgreSQL primary, simple queries | about 10,000–50,000 QPS |
| Round trip inside a data center | about 0.5 ms; across continents about 100–150 ms |
| Powers of two | 2¹⁰ ≈ 10³ (KB), 2²⁰ ≈ 10⁶ (MB), 2³⁰ ≈ 10⁹ (GB), 2⁴⁰ ≈ 10¹² (TB) |

**The tail dominates when requests fan out.** A page that calls 100 services, each with a 1% chance of being slow, is slow about 63% of the time (`1 − 0.99¹⁰⁰`). So track **p50** (typical), **p99** (what the unlucky users feel) and **p99.9** for high-volume services, not just the average.

**State your assumptions.** Every estimate is only as good as its inputs. Write them down so others can challenge the right number.

## 6.17 Combined Tips & Tricks

A consolidated master list drawn from all sections.

### 6.17.1 General Scaling

- **Start simple:** Use vertical scaling for MVPs; switch to horizontal as needs grow. Don't over-engineer.
- **Design stateless services:** Easier to distribute and scale horizontally. Use shared databases or distributed caches for state.
- **Choose the right scaling strategy:** Horizontal for resilience, vertical for simplicity, diagonal for flexibility.
- **Know when to switch:** Monitor system metrics; switch when approaching hardware limits or needing high availability.
- **Document scaling decisions:** Record why/when you chose vertical, horizontal, or diagonal scaling to aid future maintenance.

### 6.17.2 Automation & Monitoring

- **Automate monitoring:** Track key metrics and set up alerts.
- **Monitor everything:** Use dashboards and alerts (CloudWatch, Prometheus, Grafana).
- **Monitor both technical and business KPIs:** e.g., queue depth, orders per minute.
- **Plan for failure:** Implement health checks and graceful failover in load balancers.
- **Test under load:** Use chaos engineering and load testing to surface bottlenecks early.

### 6.17.3 Load Balancers

- **Implement load balancers:** Distribute traffic, prevent overload, increase reliability.
- **Choose the right load balancing strategy:** Match to traffic patterns.
- **Always set up health checks** for backend servers.
- **For microservices**, consider using a service mesh (Istio, Linkerd) for advanced L7 routing.
- **Enable SSL termination** at the load balancer to reduce backend CPU load.

### 6.17.4 Autoscaling

- **Set conservative thresholds at first, then tune.** Avoid thrashing (rapid scaling in/out).
- **Test autoscaling in staging with simulated traffic spikes.**
- **Combine reactive and predictive scaling for best results.**
- **Document your scaling policies** and update them as usage patterns evolve.
- **For serverless, check for concurrency limits and cold start implications.**
- **Always review cloud provider pricing calculators** to forecast cost under peak loads.
- **Limit autoscaling:** Set quotas to avoid runaway costs.

### 6.17.5 Cost Optimization

- **Avoid over-provisioning.** Use auto-pausing and scale-to-zero features in serverless/cloud.
- **Use spot/preemptible instances** for batch workloads (up to 80% cheaper).
- **Rightsize regularly** based on actual usage.
- **Set resource limits/quotas** to prevent runaway costs in dev/test environments.

---

## 6.18 Sample Interview Questions

1. What does scalability mean in system design?
2. Compare vertical and horizontal scaling. When would you use each?
3. Explain diagonal scaling and why it's useful in cloud-native apps.
4. What are common bottlenecks, and how do you identify them?
5. How does a load balancer improve availability and performance?
6. What is autoscaling, and how is it implemented in AWS/Azure/GCP?
7. How do you optimize for cost while scaling in the cloud?
8. Describe a scenario where horizontal scaling wouldn't help.
9. How do you balance cost and complexity in scaling strategies?
10. What challenges arise in horizontal scaling and how would you solve them?
11. Explain the difference between Layer 4 and Layer 7 load balancers — with examples.
12. Compare Round Robin vs. Least Connections — pros/cons.
13. When would you use software, hardware, or cloud-based load balancers?
14. How do you handle failover and high availability?
15. How does predictive autoscaling work?
16. How would you set up autoscaling for a containerized app?
17. What challenges arise with autoscaling in real-time systems?
18. How can you ensure cost optimization when implementing autoscaling?

---

## 6.19 Key Takeaways

- **Scalability is essential** for growth, reliability, and performance in modern architectures.
- **Vertical, horizontal, and diagonal scaling** serve different needs — choose wisely based on workload and growth patterns.
- **Load balancers are key** to distributing traffic and ensuring uptime.
- **Autoscaling** enables agility and cost efficiency in the cloud.
- **Continuous monitoring and optimization** keep your system healthy as it grows.
- **Your scaling strategy should evolve** with your system's growth and requirements.
- **Align autoscaling with cost optimization goals** to avoid budget overruns.

---

## 6.20 Further Reading

**AWS:**

- [AWS Auto Scaling Documentation](https://docs.aws.amazon.com/autoscaling/)
- [AWS Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/)

**Azure:**

- [Azure Autoscale Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-overview)
- [Azure Load Balancer](https://azure.microsoft.com/en-us/services/load-balancer/)

**GCP:**

- [GCP Autoscaling Documentation](https://cloud.google.com/compute/docs/autoscaler/)
- [Google Cloud Load Balancing](https://cloud.google.com/load-balancing)
- [Cloud Cost Optimization Guide](https://cloud.google.com/solutions/cost-optimization)

**Tools:**

- [NGINX Load Balancing Docs](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [NGINX Load Balancing Guide](https://docs.nginx.com/nginx/admin-guide/load-balancer/)
- [HAProxy Documentation](https://www.haproxy.org/)

---

**Diagram rendering note:** To view the Mermaid diagrams, use a Markdown viewer with Mermaid support (e.g., VS Code with Mermaid plugin, GitHub, HackMD).

---

**Next Up:** [Chapter 7 — Storage: Database and Storage →](./7%20-%20Storage%20-%20Database%20and%20Storage.md) — how databases are structured, stored, and scaled in distributed systems.
