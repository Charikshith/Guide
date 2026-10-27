# Chapter 32 — Library Ch 10 — Security

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 31 — Library Ch 9 — Reliability & DR](ch31-library-09-reliability-dr.md) · Next → [Chapter 33 — Library Ch 11 — Distributed Systems Fundamentals](ch33-library-11-distributed-systems-fundamentals.md)

---

## Concept

CIA triad, STRIDE, OAuth 2.0 flows, JWT pitfalls, defense-in-depth, encryption, secrets management, Zero Trust.

**In one sentence:** Security is not just a feature — it's a core pillar of reliable, scalable, and trustworthy system architecture.

Security is not just a feature — it's a **core pillar** of reliable, scalable, and trustworthy system architecture. In this chapter, we'll explore security for distributed systems, drawing from fundamental principles, real-world attacks, best practices, and interview-ready explanations.

This chapter covers: the CIA triad, threat modeling, authentication & authorization, encryption & PKI, network & infrastructure security, zero-trust, cloud/container/serverless security, microservices security, OWASP Top 10, and security in the SDLC.

> *"Security is a non-functional requirement, but it's critical for user trust, data protection, and system reliability."*

---

### Learning Outcomes

After reading this chapter, you'll be able to:

1. Apply the **CIA triad** to evaluate a system's security posture.
2. Pick the right **OAuth 2.0 flow** for a given client type (web app, SPA, mobile, machine-to-machine).
3. Avoid the **top JWT pitfalls** (storing tokens in localStorage, not validating signatures, no expiry).
4. Apply **defense-in-depth** with WAF → API Gateway → app-level auth → DB-level access controls.
5. Design **secrets management** with rotation, least privilege, and audit logs.


---

### Why Security Matters

- **User trust:** Users won't share data with insecure platforms.
- **Data protection:** Prevent leaks, theft, and accidental exposure.
- **System reliability:** Systems under attack can't perform well.
- **Compliance:** Laws like **GDPR** and **HIPAA** strictly mandate how data should be handled.

**Real-world breaches** (Equifax, Facebook) show that neglecting security can lead to massive financial and reputational damage.


### Security in Distributed Systems

Distributed architectures = more components, more entry points, more vulnerabilities.

**Key considerations:**

- Data protection **in transit** and **at rest**.
- Robust **authentication / authorization.**
- **Secure APIs:** Input validation, rate limiting, exploit protection.
- **Node & network protection:** Segmentation, firewalls, monitoring.

(See `image-24.png` for layered-security diagram. Security must be enforced at every layer: API, service, data, infrastructure.)


### The CIA Triad

The backbone of security:

| Principle              | Goal                                          | Techniques                                       |
|------------------------|-----------------------------------------------|--------------------------------------------------|
| **(C) Confidentiality**| Prevent unauthorized data access              | Encryption (at rest/in transit), access control  |
| **(I) Integrity**      | Prevent data tampering                        | Hashing, digital signatures, checksums, versioning |
| **(A) Availability**   | Ensure system/data are accessible when needed | Redundancy, DDoS protection, failover            |

(See `image-25.png` for CIA triad diagram.)

```mermaid
graph TD
    A[Confidentiality]
    B[Integrity]
    C[Availability]
    D[System Security]
    A --> D
    B --> D
    C --> D
```

```mermaid
graph LR
  A[Confidentiality] --> B[System Security]
  C[Integrity] --> B
  D[Availability] --> B
```


### Threat Modeling & Attack Vectors

**Threat modeling** helps you think like an attacker.

#### Steps

- **Identify attack surface:** Exposed APIs, UIs, network endpoints.
- **Entry points:** Vulnerable integrations, user errors.
- **Assets to protect:** Sensitive data, financial transactions, IP.

#### STRIDE Model

(See `image-26.png` for STRIDE diagram.)

- **S**poofing
- **T**ampering
- **R**epudiation
- **I**nformation Disclosure
- **D**enial of Service
- **E**levation of Privilege

#### Common Attack Vectors

| Vector                 | Description                            | Defense                                  |
|------------------------|----------------------------------------|------------------------------------------|
| Insecure APIs          | Poor validation, lack of auth          | Input validation, auth, rate limiting    |
| Misconfigured Servers  | Defaults, missing patches              | Config management, regular audits        |
| Poor Authentication    | Weak passwords, no 2FA, session flaws  | Strong auth, MFA, secure token handling  |
| Open Ports/Services    | Unnecessary or exposed ports           | Firewalls, segmentation, port closure    |

```mermaid
flowchart LR
    I(["Internet"]) --> FW["Firewall"] --> W["Web service"]
    FW --> DB[("Database")]
    W --> IA["Internal APIs"]
```


Attackers probe every interface — APIs, open ports, misconfigured servers.


### Common Attacks

#### DDoS (Distributed Denial of Service)

- **Description:** Flooding system with traffic to disrupt service.
- **Target:** Availability.
- **Mitigation:** Rate limiting, traffic scrubbing (e.g., Cloudflare), autoscaling and failover.

#### Man-in-the-Middle (MITM)

- **Description:** Attacker intercepts communication.
- **Targets:** Confidentiality & Integrity.
- **Protection:** HTTPS (TLS), certificate pinning, VPNs.

#### Injection Attacks (e.g., SQL Injection)

- **Description:** Attacker sends malicious input to execute unwanted commands.
- **Impacts:** Data integrity, confidentiality.
- **Mitigation:** Input validation, parameterized queries, WAF (Web Application Firewall).

#### Spoofing Attacks

- **Description:** Impersonation of another user or system.
- **Types:** IP spoofing, email spoofing, DNS spoofing.
- **Defense:** Multi-factor authentication, token-based authentication, IP whitelisting.


### Security in the SDLC

**Embed security from the start (Shift Left):** Integrate security practices early in the development process to prevent vulnerabilities instead of fixing them later.

#### Phases

- **Requirements:** Threat modeling — identify and assess potential security threats before development begins.
- **Design:** Secure architecture — create system designs that minimize attack surfaces and enforce least privilege.
- **Development:** Secure coding — follow coding standards and best practices to avoid introducing vulnerabilities.
- **Testing:** Security tests, fuzzing — detect and fix vulnerabilities through automated and manual security testing.
- **Deployment:** Secrets management — protect credentials, keys, and sensitive configurations in production environments.
- **Maintenance:** Patch management — continuously update and patch systems to address newly discovered vulnerabilities.


### Authentication & Authorization

*This section is in [Chapter 19 — Authentication & Authorization in System Design](ch19-authentication-and-authorization-in-system-design.md), next to that chapter's practice material, so it is not repeated here.*

### Data Protection & Secure Communication

*This section is in [Chapter 18 — Security at the System Level](ch18-security-at-the-system-level.md), next to that chapter's practice material, so it is not repeated here.*

### Network & Infrastructure Security

#### Why Network Security Matters

- **External Threats:** DDoS, intrusion attempts, IP spoofing, etc.
- **Internal Risks:** Misconfiguration, lateral movement after a breach.
- **Cloud-Native Expansion:** More exposure, new attack surfaces.
- **Business Impact:** Reliability, uptime, user trust, and data protection.

(See `image-31.png` for network security overview.)

#### Firewalls

**Purpose:** Filter traffic based on IP, port, protocol.

**Types:**

- **Network-based:** Protects entry points (perimeter gateway).
- **Host-based:** Secures individual servers/devices.
- **Cloud firewalls:** Tailored for cloud resources (e.g., AWS Security Groups).

**Example: AWS Security Group (Terraform)**

```hcl
resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow HTTP and HTTPS"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

#### Reverse Proxies

**Purpose:** Route incoming requests, mask backend identities, add security layers (SSL termination, load balancing).

**Popular tools:** NGINX, AWS ALB, HAProxy.

**Basic NGINX reverse proxy:**

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend-service:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**With TLS:**

```nginx
server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://backend:8080;
    }
}
```

```mermaid
graph LR
    User --Request--> Proxy[Reverse Proxy]
    Proxy --Request--> Backend[Backend Server]
    Backend --Response--> Proxy
    Proxy --Response--> User
```

#### Firewall vs. Reverse Proxy

##### Firewall

A **security barrier** that filters incoming and outgoing network traffic based on defined security rules.

**Pros:** Blocks unauthorized traffic; enforces policies based on IP/port/protocol/packet state; prevents malware/DDoS/brute-force; supports network segmentation (e.g., DMZ).

**Cons:** Can't inspect application-level payloads deeply (unless NGFW); needs constant rule updates; doesn't provide caching/load balancing.

##### Reverse Proxy

Sits in front of web servers and acts as an **intermediary** for client requests.

**Pros:** Hides internal server identities; load balancing; SSL/TLS termination; caching; can integrate WAF and authentication features.

**Cons:** Adds complexity; can be a single point of failure if not redundant; slight latency; misconfiguration risk.

##### Comparison Table

| Feature             | **Firewall**                                    | **Reverse Proxy**                                    |
|---------------------|-------------------------------------------------|------------------------------------------------------|
| **Primary Purpose** | Block unauthorized network traffic              | Handle and manage web traffic to backend servers     |
| **OSI Layer**       | Network (Layer 3/4)                             | Application (Layer 7)                                |
| **Direction**       | Controls traffic *into and out of* the network  | Handles traffic *into* web servers                   |
| **Security Role**   | Network perimeter defense                       | Application-level protection and traffic management  |
| **Functions**       | Filtering, monitoring, blocking                 | Load balancing, SSL termination, caching, routing    |
| **Visibility**      | Sees IPs, ports, and protocols                  | Sees HTTP/HTTPS requests and responses               |
| **Example Tools**   | pfSense, Cisco ASA, Fortinet                    | NGINX, HAProxy, Apache HTTPD, Cloudflare             |

**Summary:** Firewalls protect the **network layer;** reverse proxies protect the **application layer.** They're complementary — often used together.

```mermaid
flowchart LR
    Internet["(Internet)"]
    Firewall["Firewall (Network Layer Protection)"]
    ReverseProxy["Reverse Proxy (App Layer Protection)"]
    WebServer1["(Web Server 1)"]
    WebServer2["(Web Server 2)"]
    Database["(Database)"]

    Internet -->|Incoming Requests| Firewall
    Firewall -->|Filtered Traffic| ReverseProxy
    ReverseProxy -->|Load Balancing / Caching| WebServer1
    ReverseProxy -->|Load Balancing / Caching| WebServer2
    WebServer1 -->|Queries| Database
    WebServer2 -->|Queries| Database

    style Firewall fill:#f9d5d3,stroke:#d9534f,stroke-width:2px,color:black;
    style ReverseProxy fill:#d0e6ff,stroke:#0275d8,stroke-width:2px,color:black;
    style WebServer1 fill:#dff0d8,stroke:#5cb85c,stroke-width:1.5px,color:black;
    style WebServer2 fill:#dff0d8,stroke:#5cb85c,stroke-width:1.5px,color:black;
    style Database fill:#fff3cd,stroke:#f0ad4e,stroke-width:1.5px,color:black;
```

#### API Traffic Control: Rate Limiting, Throttling, IP Filtering

##### Rate Limiting

Controls how many requests a client (IP, user, API key) can make within a specified time period.

**Example:** A user may make **100 requests per minute.** Exceeding returns **429 – Too Many Requests.**

**Pros:** Prevents DDoS / API abuse; ensures fair usage; manages server load; protects against brute-force login.

**Cons:** Can block legitimate bursts; adds latency at gateways; requires state management.

**Tools:** NGINX, Kong Gateway, Cloudflare, AWS API Gateway.

##### Throttling

**Softer version** of rate limiting: rather than rejecting excess requests, throttling **queues or delays** them.

**Example:** After 100 requests/min, additional requests are processed slower (e.g., 1 per second).

**Pros:** Prevents overload gracefully; better UX than hard blocking; useful for streaming/real-time systems.

**Cons:** Adds response latency; more complex; might not fully protect against massive spikes.

**Use cases:** Payment gateways, file uploads / video streaming, real-time APIs.

##### IP Filtering

Allows or blocks traffic based on the **source IP address.** First layer of defense at network or application level.

**Example:** Allow only requests from specific corporate IPs; block known malicious IPs.

**Pros:** Simple and effective for basic access control; reduces attack surface; works with firewalls/proxies/LBs.

**Cons:** Ineffective against spoofed IPs / botnets; static allowlists need updates; not suitable for mobile clients or dynamic-IP cloud environments.

**Implementation:** Firewall rules (AWS Security Groups, NACLs), reverse proxies, API Gateways.

##### Summary Table

| Technique         | Purpose                                 | Behavior               | Pros                           | Cons                        |
|-------------------|------------------------------------------|------------------------|--------------------------------|-----------------------------|
| **Rate Limiting** | Restrict total requests per time window | Blocks excess          | Prevents abuse, DDoS           | May block legitimate spikes |
| **Throttling**    | Slow down excess requests               | Queues or delays       | Smooth handling, user-friendly | Adds latency                |
| **IP Filtering**  | Allow/block based on IPs                | Drops or denies        | Simple, low-cost security      | Hard to manage dynamic IPs  |

```mermaid
flowchart TD
    Client["Client Application"]
    Gateway["API Gateway"]
    IPFilter["IP Filtering (Allow/Deny based on IP)"]
    RateLimit["Rate Limiter (Limit requests per time window)"]
    Throttle["Throttler (Delay excess requests)"]
    Backend["(Backend Service)"]
    Logs["(Monitoring & Logs)"]

    Client -->|Request| Gateway
    Gateway --> IPFilter
    IPFilter -->|Allowed| RateLimit
    IPFilter -.->|Blocked IPs| Logs
    RateLimit -->|Within limit| Throttle
    RateLimit -.->|429 Too Many Requests| Logs
    Throttle -->|Processed| Backend
    Backend -->|Response| Client
    Backend --> Logs
```


### Network Segmentation & Isolation

**Network segmentation** is the practice of dividing a network into smaller logical or physical subnetworks (segments) to limit lateral movement, enforce granular security policies, and improve performance. **Isolation** means enforcing strict controls (often via firewalls or access control) so that one segment cannot freely access another.

> **Lateral Movement:** The technique attackers use to move within a network after gaining initial access — typically moving from one compromised system to others, in search of sensitive data, credentials, or critical assets.

#### Why It Matters

- Reduces blast radius when a system is compromised.
- Enforces least-privilege access between services.
- Improves performance and traffic management.
- Helps meet compliance and audit requirements (PCI, HIPAA, etc.).

#### Common Segmentation Patterns

- **Perimeter (Internet) → DMZ → Application → Database.**
- **VLAN-based segmentation** (L2 segmentation inside LANs).
- **Subnet + ACLs** (IP subnets with routing / access control lists).
- **Zone-based firewalling** (separate security zones).
- **Microsegmentation** (host-level segmentation using software agents, service mesh, cloud security groups).
- **Zero Trust segmentation** (authenticate & authorize every connection).

#### Techniques / Tools

- **VLANs** (switch-level segmentation).
- **Subnets + routing** (logical segments).
- **Firewalls / NGFWs** (policy enforcement between segments).
- **Security groups / NACLs** (cloud-native segmentation).
- **VPNs and private links** (isolate management and inter-datacenter traffic).
- **Service mesh / sidecars** (mTLS, policies between microservices).
- **Host-based firewalls** (iptables, Windows Firewall).
- **Network access control (NAC)** and identity-aware proxies.

#### Pros

- Limits lateral movement and attack surface.
- Better compliance and auditability.
- Fine-grained policy control.
- Can improve network performance.

#### Cons / Trade-offs

- Increased management complexity.
- Misconfiguration risk.
- Potential operational overhead.
- Can add latency if traffic traverses multiple enforcement points.

#### Best Practices

- Start with a **clear segmentation plan:** Categorize assets by sensitivity & function.
- Apply **least privilege:** Default deny between segments; allow only required flows.
- **Defense-in-depth:** Combine perimeter, segment firewalls, host controls.
- **Centralize policy management** (IaC for network/firewall rules).
- **Document** allowed flows and maintain network maps.
- **Automate** audits and drift detection.
- **Use monitoring & IDS/IPS** per segment.
- Test via chaos / attack simulations and pentesting.

#### Implementation Checklist

- [ ] Inventory assets and classify by sensitivity (prod, dev, management, public).
- [ ] Define required flows (source → dest: ports/protocols).
- [ ] Design segments (DMZ, app, db, management, monitoring, CI/CD).
- [ ] Implement segmentation (VLANs/subnets, security groups, NGFW rules).
- [ ] Harden management plane (separate network + MFA for admin access).
- [ ] Deploy host-based protections & microsegmentation if required.
- [ ] Configure logging & monitoring per segment.
- [ ] Set up automated policy tests and regular audits.
- [ ] Plan for incident response (how to quarantine a segment).

#### Typical Segmented Layout

```mermaid
flowchart LR
  Internet["(Internet)"]
  PerimeterFW["Perimeter Firewall"]
  CDN["/CDN & LB/"]
  DMZ1["(Web App DMZ)"]
  AppFW["App Firewall"]
  AppSubnet["(App Subnet)"]
  DBFW["DB Firewall"]
  DBSubnet["(DB Subnet)"]
  Mgmt["(Management Network)"]
  Monitoring["(Monitoring & IDS)"]

  Internet --> CDN
  CDN --> PerimeterFW
  PerimeterFW --> DMZ1
  DMZ1 --> AppFW
  AppFW --> AppSubnet
  AppSubnet --> DBFW
  DBFW --> DBSubnet

  Mgmt -.-> PerimeterFW
  Mgmt --> AppFW
  Mgmt --> DBFW

  Monitoring -->|Flow logs, Alerts| AppFW
  Monitoring -->|Flow logs, Alerts| DBFW
```

#### When to Use Microsegmentation

- Highly dynamic, east-west traffic heavy environments (K8s, microservices).
- Environments with strict compliance or where host-level compromise risk is high.
- When you need policy tied to identity/service, not to network addresses.

#### Pitfalls to Avoid

- Over-segmentation causing operational headache.
- Relying on network segmentation alone (forget host-level controls).
- Not version-controlling network policies.
- Ignoring management plane isolation.


### Zero Trust Security Model

*This section is in [Chapter 18 — Security at the System Level](ch18-security-at-the-system-level.md), next to that chapter's practice material, so it is not repeated here.*

### Securing Cloud Environments

#### Shared Responsibility Model

Security in the cloud is a **shared responsibility** between the **cloud provider** and the **customer.**

| Responsibility     | Description                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------------|
| **Cloud Provider** | Secures physical infrastructure, hardware, network, and foundational services (AWS, Azure, GCP).     |
| **Customer**       | Secures data, identity, access, and configurations within the cloud environment.                     |

#### Key Cloud Security Practices

| Practice                          | Description                                                                                                                |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **IAM (Identity & Access Mgmt)**  | Enforce RBAC, least privilege, and MFA.                                                                                    |
| **Encryption**                    | Encrypt data at rest (EBS, S3, Cloud Storage) and data in transit (via TLS/HTTPS).                                         |
| **Audit Logging**                 | Enable detailed audit trails (AWS CloudTrail, Azure Monitor, GCP Audit Logs).                                              |
| **CSPM (Cloud Security Posture Management)** | Continuously scan cloud resources for misconfigurations, policy violations, and compliance gaps.                  |

#### AWS IAM Policy Example

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::mybucket/*"]
    }
  ]
}
```

> Grants read-only access to all objects in the S3 bucket `mybucket`.

#### Additional Cloud Security Best Practices

- **Network segmentation:** Use VPCs, subnets, and security groups to isolate workloads.
- **Zero Trust principles:** Verify each access request — don't assume trust inside your network.
- **Key management:** Use managed services like **AWS KMS**, **Azure Key Vault**, **GCP KMS** for secure key lifecycle.
- **Monitoring & alerting:** Use SIEM tools (AWS GuardDuty, Azure Sentinel) for threat detection.
- **Backup & recovery:** Automate snapshots, versioning, cross-region backups.
- **Compliance automation:** Use **CSPM** and **CIEM** to maintain governance.

| Aspect                      | Best Practice                            |
|-----------------------------|------------------------------------------|
| **Access Management**       | RBAC, least privilege, MFA               |
| **Data Protection**         | Encryption (in transit & at rest)        |
| **Visibility & Monitoring** | Logging, threat detection, alerts        |
| **Configuration Security**  | CSPM & automated policy enforcement      |
| **Resilience**              | Regular backups, versioning, DR planning |


### Serverless & Container Security

#### Serverless Security

Serverless functions (AWS Lambda, Azure Functions, GCP Cloud Functions) abstract away infrastructure, but **security of the code and configurations** remains your responsibility.

| Practice                          | Description                                                                                                  |
|-----------------------------------|--------------------------------------------------------------------------------------------------------------|
| **IAM Roles (Least Privilege)**   | Assign narrowly scoped IAM roles — each function should only access the resources it truly needs.            |
| **Timeouts & Execution Limits**   | Set strict runtime limits to prevent resource abuse or infinite loops.                                       |
| **API Gateway Security**          | Front serverless functions with API Gateways that enforce authentication, rate limiting, and IP filtering.   |
| **Input Validation**              | Sanitize and validate inputs to prevent injection attacks.                                                   |
| **Logging & Monitoring**          | Use services like AWS CloudWatch Logs or Azure Monitor for visibility and anomaly detection.                 |
| **Dependency Management**         | Regularly scan third-party libraries for vulnerabilities (AWS CodeGuru, Snyk).                               |

#### Container Security

Containers (Docker, Kubernetes workloads) share the host kernel, requiring **strong isolation and image hygiene.**

| Practice                          | Description                                                                                       |
|-----------------------------------|---------------------------------------------------------------------------------------------------|
| **Image Scanning**                | Scan container images using **Trivy**, **Clair**, **Anchore** to detect known CVEs.               |
| **Run as Non-Root**               | Prevent privilege escalation by running containers under non-root users.                          |
| **Limit Privileges**              | Use minimal capabilities (`--cap-drop=ALL`) and read-only file systems.                           |
| **Network Policies (Kubernetes)** | Use **NetworkPolicies** to restrict pod-to-pod communication and block lateral movement.          |
| **Image Signing**                 | Use **Notary** or **Cosign** to verify image authenticity before deployment.                      |
| **Runtime Protection**            | Employ tools like **Falco** or **AppArmor** to detect abnormal container activity.                |
| **Patch & Update**                | Regularly rebuild and update images with the latest OS and library patches.                       |

#### Summary Table

| Area           | Key Security Measures                                                   | Tools/Services                                                                        |
|----------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| **Serverless** | IAM least privilege, input validation, API Gateway protection           | AWS Lambda + CloudWatch, Azure Functions + Defender, GCP Functions + Security Scanner |
| **Containers** | Image scanning, non-root execution, network policies, runtime hardening | Trivy, Clair, Falco, AppArmor, Kubernetes NetworkPolicies                             |

#### Best Practices Across Both

- Adopt the **Principle of Least Privilege** everywhere.
- Automate security checks in **CI/CD pipelines.**
- Use **Infrastructure as Code (IaC)** scanning tools (Checkov, tfsec).
- Continuously monitor logs and metrics for anomalies.
- Rotate and securely store **secrets** using KMS or Vault.


### Security in Microservices

#### Service-to-Service Authentication

Each microservice must verify the identity of the other before sharing data.

- Use **JWT** for stateless authentication and authorization.
- Use **Mutual TLS (mTLS)** to authenticate both client and server using digital certificates.
- Rotate tokens and certificates regularly.
- Store secrets securely (AWS Secrets Manager, HashiCorp Vault).

*Example:* Service A → includes JWT in request → Service B verifies signature and claims.

#### API Gateway

Acts as a **central entry point** for all external traffic into your microservices.

- Enforces **authentication**, **authorization**, **input validation.**
- Implements **rate limiting**, **IP filtering**, **request logging.**
- Hides internal services from external exposure.
- Integrates with **IAM** or **OAuth 2.0** providers for user identity management.

*Example:* API Gateway verifies OAuth token before routing request to internal services.

#### Service Mesh

A **service mesh** (Istio, Linkerd, Consul) adds security, observability, and traffic management between microservices without changing application code.

- Provides **fine-grained traffic policies** and **mTLS encryption** for all inter-service communication.
- Implements **zero-trust** principles inside the cluster.
- Enables **access control**, **telemetry**, **automatic certificate rotation.**
- Offloads network security from developers — handled by **sidecar proxies** (Envoy).

*Example:* Service A ↔ Service B communication is automatically encrypted and authenticated by the service mesh.

#### Summary Table

| Layer                       | Security Focus                         | Techniques / Tools                   |
|-----------------------------|----------------------------------------|--------------------------------------|
| **Edge (External)**         | Secure user access                     | API Gateway, OAuth 2.0, WAF          |
| **Service-to-Service**      | Authenticate internal requests         | JWT, mTLS, Service Accounts          |
| **Intra-Service (Network)** | Encrypted and controlled communication | Service Mesh (Istio, Linkerd)        |
| **Secrets Management**      | Protect credentials and tokens         | HashiCorp Vault, AWS Secrets Manager |
| **Monitoring & Auditing**   | Detect abnormal behavior               | Prometheus, OpenTelemetry, SIEM      |

#### Secure Microservices Architecture

```mermaid
flowchart LR
    User[("User")]
    APIGW["API Gateway (Auth, Rate Limit, Validation)"]
    SvcA[("Service A")]
    SvcB[("Service B")]
    SvcC[("Service C")]
    Mesh["Service Mesh (mTLS, Policy, Observability)"]
    Vault["Secrets Manager"]
    Monitor["Monitoring & Logging"]

    User -->|Authenticated Request| APIGW
    APIGW -->|JWT / OAuth Token| SvcA
    SvcA -->|mTLS + Policy| SvcB
    SvcB -->|mTLS + Policy| SvcC
    SvcA -.-> Vault
    SvcB -.-> Vault
    SvcC -.-> Vault
    Mesh --> SvcA
    Mesh --> SvcB
    Mesh --> SvcC
    SvcA --> Monitor
    SvcB --> Monitor
    SvcC --> Monitor

    style APIGW fill:#d9ead3,stroke:#6aa84f,stroke-width:2px,color:black;
    style Mesh fill:#d0e6ff,stroke:#1155cc,stroke-width:2px,color:black;
    style Vault fill:#fff2cc,stroke:#e69138,stroke-width:2px,color:black;
    style Monitor fill:#f4cccc,stroke:#cc0000,stroke-width:2px,color:black;
```

**Key takeaways:**

- Apply **Zero Trust:** authenticate and encrypt *every* service call.
- Use **API Gateways** for edge protection, and **Service Meshes** for internal trust.
- Automate **certificate and token management.**
- Continuously **monitor, log, and analyze** inter-service communication.


### Common Vulnerabilities — OWASP Top 10

- **Injection:** SQL, NoSQL, OS command injection.
- **Broken Authentication:** Weak or no authentication.
- **Sensitive Data Exposure:** Unencrypted data.
- **Security Misconfiguration:** Default creds, open ports.
- **XSS, CSRF, SSRF:** Client-side and server-side threats.

**Mitigation:**

- Input validation.
- Secure authentication.
- Encrypt sensitive data.
- Harden configuration.
- Secure defaults.


### OAuth 2.0 Flows — Pick the Right One

Most security failures in modern apps come from picking the wrong OAuth flow or skipping steps. Here's the decision tree.

| Flow                              | Use for                                                | What you need to know                                              |
|-----------------------------------|---------------------------------------------------------|---------------------------------------------------------------------|
| **Authorization Code + PKCE**     | SPAs, mobile apps                                       | Modern best practice. PKCE prevents code interception.              |
| **Authorization Code** (no PKCE)  | Server-side web apps with a client secret              | Classic flow; needs a confidential client (secret server-side).     |
| **Client Credentials**            | Machine-to-machine (one service calls another)         | No user; just a service identity.                                   |
| **Device Code**                   | TVs, CLI tools, IoT devices                            | "Visit example.com/device and enter ABC-123"                        |
| **~~Implicit~~** (deprecated)     | ~~SPAs~~                                                | **Don't use.** Token in URL = browser history leakage. Use Auth Code + PKCE. |
| **~~Resource Owner Password~~** (deprecated) | ~~Trusted first-party login~~              | **Don't use.** App handles the password directly — defeats OAuth's purpose. |

> **In a system design interview:** "We'll use Authorization Code + PKCE for the SPA, Client Credentials for our microservices to talk to each other, and Device Code for the CLI tool."


### JWT Pitfalls — What Goes Wrong

JWT is everywhere, but it's also where the most security mistakes happen.

| Pitfall                                  | Why it's bad                                                                       | Fix                                                                            |
|------------------------------------------|------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Storing JWT in `localStorage`**         | Any XSS instantly steals the token (no `HttpOnly` protection)                      | Use `HttpOnly`, `Secure`, `SameSite=Lax` cookies instead                       |
| **Not validating the signature**          | Anyone can forge a JWT with admin claims                                          | Always verify with the public key/secret. Reject `alg: none`.                  |
| **Accepting `alg: none`**                 | Famous CVE — library lets you skip signature                                       | Pin the expected algorithm in your verifier                                    |
| **No expiry (`exp`)**                     | Stolen token works forever                                                        | Set short `exp` (15-60 min). Use refresh tokens for long-lived sessions.       |
| **No token revocation strategy**          | Can't invalidate before `exp` even if you know the token is compromised           | Keep a blocklist OR use short expiry + refresh                                |
| **Storing sensitive data in the payload** | JWT payload is base64-encoded, *not encrypted* — anyone with the token can read it| Don't put PII or secrets in the JWT. Use opaque tokens or encrypt the payload (JWE). |
| **Confusing JWT with sessions**           | JWTs can't be revoked easily; sessions can be deleted server-side                  | If you need instant revocation, use server-side sessions.                      |


### Defense in Depth — Layered Security

*This section is in [Chapter 18 — Security at the System Level](ch18-security-at-the-system-level.md), next to that chapter's practice material, so it is not repeated here.*

### Secrets Management — Don't Put Secrets in Code

*This section is in [Chapter 18 — Security at the System Level](ch18-security-at-the-system-level.md), next to that chapter's practice material, so it is not repeated here.*

### Common Security Headers — Defaults Every App Should Set

These belong on every HTTP response. Forgetting them is a finding in any security audit.

| Header                          | What it does                                                |
|---------------------------------|--------------------------------------------------------------|
| `Strict-Transport-Security`     | Force HTTPS for all future requests (HSTS)                  |
| `Content-Security-Policy`       | Whitelist allowed scripts/styles (strongest XSS defense)    |
| `X-Content-Type-Options: nosniff` | Stop browsers from guessing MIME types                    |
| `X-Frame-Options: DENY`         | Prevent clickjacking (or use CSP's `frame-ancestors`)       |
| `Referrer-Policy: strict-origin-when-cross-origin` | Limit referer leakage                  |
| `Permissions-Policy`            | Disable browser features (camera, mic) you don't need       |


### Combined Tips & Tricks

A consolidated master list from all sections.

#### General

- **Shift Left:** Start thinking about security early in your project. Embed security throughout the SDLC.
- **Automate security checks:** Use CI tools to catch issues early. Integrate security tests and vulnerability scans into CI/CD pipelines.
- **Principle of Least Privilege:** Give only the permissions needed.
- **Patch early, patch often:** Stay on top of OS, library, and container image updates.
- **Review regularly:** Security is an ongoing process, not a one-time setup.
- **Educate your team:** Security awareness is everyone's job.

#### Authentication & Authorization

- Always use **multi-factor authentication (MFA)** where possible.
- Store sensitive tokens/secrets in **vaults** (AWS Secrets Manager, HashiCorp Vault).
- Rotate keys and secrets regularly. Automate rotation.

#### Data Protection

- **Encrypt everywhere:** Both at rest and in transit — never skip one.
- Use **parameterized queries** to prevent SQL injection.
- Always **salt** and **hash** passwords — never store them in plaintext.
- **Hash, don't encrypt, passwords:** And always salt them.
- **Automate certificate renewal:** Use tools like Let's Encrypt with auto-renewal.

#### Network Security

- Regularly **scan for open ports** and **unused services.**
- Use **security groups** and **VPCs** in the cloud for isolation.
- **Harden your APIs:** Rate limiting, IP filtering, input validation, strong authentication.
- **Trust but verify:** Use mTLS, certificate pinning, threat modeling.

#### Monitoring & Logging

- Log **all security events** and review them regularly.
- Set up **alerting** for suspicious activities.
- **Enable logging and monitoring:** Know when and where breaches or anomalies happen.
- **Log everything (securely):** Centralize logs and protect them with encryption.

#### Operations

- **Embrace CSPM:** Use tools to continuously assess your cloud security posture.
- **Practice incident response:** Regularly test your recovery and incident response plans.
- **Red team exercises:** Regularly test your defenses.


### Sample Interview Questions

1. How would you design a secure authentication system for a distributed application?
2. Explain how the CIA triad applies to system design.
3. What are common security threats in a microservices architecture, and how would you mitigate them?
4. How would you protect your system from a DDoS attack?
5. What role does TLS/HTTPS play in system security?
6. How would you implement certificate management at scale?
7. How can you ensure secure data storage in a cloud-based system?
8. What is threat modeling and how would you incorporate it into your design process?
9. What is the difference between hashing and encryption?
10. Why is asymmetric encryption slower than symmetric?
11. How does PKI build trust online?
12. How would you secure data at rest and in motion?
13. How do you protect APIs from abuse and unauthorized access?
14. Explain the Zero Trust security model.
15. How would you implement microsegmentation?
16. What are the OWASP Top 10 vulnerabilities, and how do you mitigate them?


### Summary & Quick Reference

- **Security** is ongoing. It must be built into every phase and layer of your system.
- **CIA triad:** Confidentiality, Integrity, Availability.
- **Threat modeling** and awareness of **common attack vectors** are critical.
- Use **modern authentication & access control** (OAuth2, JWT, RBAC/ABAC).
- **Encrypt data everywhere** — at rest and in transit.
- **Harden your network** with firewalls, segmentation, zero trust, monitoring.
- **DR is more than backups** — it's about system continuity.

#### Quick Reference: Security by Layer

| Layer         | Key Controls                                |
|---------------|---------------------------------------------|
| App/API       | Input validation, auth, rate limiting       |
| Data          | Encryption, hashing, access controls        |
| Network       | Firewalls, segmentation, Zero Trust         |
| Cloud/Infra   | IAM, audit, secure defaults                 |

> *Building secure systems isn't a checkbox — it's the foundation of good architecture.*


### Further Reading

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT.io Introduction](https://jwt.io/introduction)
- [OAuth 2.0 and OpenID Connect](https://auth0.com/docs/get-started/authentication-and-authorization-protocols/oauth-2-0-and-openid-connect)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [Let's Encrypt](https://letsencrypt.org/)


**Next Up:** Chapter 11 — Distributed Systems Fundamentals → — a 4-step methodology for tackling any system design problem.


*(From AI Library chapter 10.)*

