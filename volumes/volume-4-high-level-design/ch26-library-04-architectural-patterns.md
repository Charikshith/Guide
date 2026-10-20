# Chapter 26 — Library Ch 4 — Architectural Patterns

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 25 — Library Ch 3 — Protocols](ch25-library-03-protocols.md) · Next → [Chapter 27 — Library Ch 5 — Web Concepts](ch27-library-05-web-concepts.md)

---

## Concept

Monolith, modular monolith, microservices, event-driven, BFF, CQRS, Event Sourcing, Saga — and when NOT to use microservices.

**In one sentence:** Welcome to a deep dive into Architectural Patterns and Styles!

Welcome to a deep dive into **Architectural Patterns and Styles**! Understanding architecture is fundamental for building robust, scalable, and maintainable software systems. Whether you're designing your first application or optimizing an enterprise solution, understanding these patterns will help you build adaptable software.

In this chapter we'll explore the foundational architectural patterns — Monolithic, Layered (N-Tier), Client-Server, Microservices, and Event-Driven — see practical code and diagram examples, compare them, and finish with actionable tips and interview prep.

---

### Learning Outcomes

After reading this chapter, you'll be able to:

1. Pick monolith, layered, microservices, or event-driven for a given problem and justify the choice.
2. Recognize a **distributed monolith** anti-pattern and avoid it.
3. Identify when to *defer* moving to microservices (almost always when starting out).
4. Apply the **Strangler Fig** pattern when migrating a monolith.
5. Reach for **CQRS, Saga, and BFF** patterns in the right situations.


---

### What is Software Architecture?

At its core, **software architecture** defines the **high-level structure** of your system — describing how its components are organized and how they interact. It encompasses:

- **Module organization**
- **Component relationships**
- **Data flow**
- **Communication patterns**
- **Component dependencies**

> *"Software architecture is the high-level structure of a software system — much like a blueprint for a building."*

#### Why Does It Matter?

The architectural choices you make will directly impact:

- **Scalability:** Can the system handle more users/data?
- **Performance:** How fast does it respond under load?
- **Maintainability:** How easily can you update or fix it?
- **Resilience:** How well does the system tolerate failure?

> **Key Point:** Every architectural decision shapes your system's behavior in production.


### Key Design Considerations

Before selecting an architecture, consider these core aspects:

1. **Business Needs:** What is the system's core purpose and requirements?
2. **Scalability:** Expected load and growth.
3. **Performance:** Latency, throughput, and responsiveness.
4. **Maintainability:** Ease of updates, fixes, and evolution.
5. **Team Skillsets:** Familiarity with distributed systems, automation, etc.
6. **Time to Market:** Speed vs. long-term scalability.

> **Remember:** Choices like monolithic vs. microservices, database structure, and communication protocols directly affect system behavior in production.


### Building Block Primer: Message Queues in Plain Terms

*This section is in [Chapter 9 — Message Queues & Streaming (Kafka, SQS, Pub/Sub)](ch09-message-queues-and-streaming-kafka-sqs-pub.md), next to that chapter's practice material, so it is not repeated here.*

### Building Block Primer: Containers and Docker in Plain Terms

> **Why this is here:** microservices, autoscaling and most modern deployments assume you run software in **containers**. You will meet the words Docker and Kubernetes in this chapter and again in Chapters 6, 10 and the case studies. This primer explains what they are before they appear. Chapter 6 shows containers being scaled automatically; Chapter 10 covers container security.

#### The Problem: "It Works on My Machine"

A program needs more than its own code: the right language version, libraries, system tools and settings. If the laptop, the test server and the production server each differ slightly, the program works in one place and breaks in another.

A **container** solves this by packaging the program **together with everything it needs to run** into one sealed unit that behaves the same wherever it runs.

#### Container vs. Virtual Machine

Both give you an isolated environment, but at different costs.

| | **Virtual machine (VM)** | **Container** |
|--|--------------------------|---------------|
| What is isolated | a whole computer, including its own operating system | just the application and its libraries |
| Operating system | each VM carries a full guest OS | all containers **share the host's OS kernel** |
| Size | gigabytes | often tens to hundreds of megabytes |
| Start time | minutes | seconds or less |
| How many per machine | a few | dozens to hundreds |
| Isolation strength | stronger (separate OS) | lighter (shared kernel) |

```mermaid
flowchart TB
    subgraph VMs["Virtual machines"]
      direction TB
      H1[Hardware] --> HV[Hypervisor]
      HV --> G1["Guest OS + App A"]
      HV --> G2["Guest OS + App B"]
    end
    subgraph Containers["Containers"]
      direction TB
      H2[Hardware] --> OS[Host OS]
      OS --> RT[Container runtime]
      RT --> C1["App A + libraries"]
      RT --> C2["App B + libraries"]
    end
```

Because containers are small and start fast, they suit systems that add and remove copies of a service all day, which is exactly what scaling needs.

#### Key Words

| Term | Meaning |
|------|---------|
| **Image** | a read-only template: your code, its libraries and settings, frozen into a package. Built in **layers**, so unchanged layers are reused. |
| **Container** | a running instance of an image. You can start many containers from one image. |
| **Dockerfile** | a short recipe that tells Docker how to build an image |
| **Registry** | a store for images (Docker Hub, Amazon ECR) from which servers pull them |
| **Docker** | the most common tool for building and running containers |

A Dockerfile for a small web service:

```dockerfile
FROM python:3.12-slim          # start from a ready-made base image
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt   # install libraries (this layer is cached)
COPY . .                              # add your code
CMD ["python", "app.py"]              # what to run when the container starts
```

```bash
docker build -t shop-api:1.0 .        # build the image
docker run -p 8080:8080 shop-api:1.0  # start a container from it
```

#### Containers Are Disposable

A container is meant to be **thrown away and replaced**, not repaired. Anything written inside it vanishes when it is removed. This has direct design consequences:

- Keep services **stateless** where you can (Chapter 5, Chapter 6), so any copy can serve any request.
- Put data that must survive in an outside **volume** or, better, in a proper database or object store (Chapter 7), never only inside the container.
- Configuration and secrets come in from outside (environment variables, a secrets manager), not baked into the image.

#### Many Containers: Orchestration and Kubernetes

Running one container is easy. Running **hundreds**, across **many machines**, keeping them healthy, is not. An **orchestrator** automates this. The most widely used one is **Kubernetes**.

You describe the result you want ("run 5 copies of this image") and Kubernetes keeps it true:

| Kubernetes idea | Plain meaning |
|-----------------|---------------|
| **Pod** | the smallest unit it runs: one or a few tightly linked containers |
| **Deployment** | "keep N copies of this pod running, and roll out new versions gradually" |
| **Service** | a stable network address in front of changing pods (a built-in load balancer) |
| **Node** | one machine in the cluster |
| **Autoscaler (HPA)** | adds or removes pod copies as load changes (Chapter 6) |

What this buys you:

- **Self-healing:** a crashed container is restarted, and pods from a failed machine are rescheduled elsewhere.
- **Scaling:** change a number, or let the autoscaler do it.
- **Rolling updates:** replace old versions step by step with no downtime, and roll back if something breaks.

Cloud providers offer managed versions (Amazon EKS and ECS/Fargate, Google GKE, Azure AKS) so you do not run the control machinery yourself.

#### Why System Design Cares

| Design goal | How containers help |
|-------------|---------------------|
| **Consistency** | the same image runs in development, testing and production |
| **Microservices** | each service ships in its own image and scales on its own |
| **Fast scaling** | a new copy starts in seconds, so you can follow traffic closely |
| **Efficiency** | many containers share one machine, so fewer servers sit idle |
| **Reliability** | failed copies are replaced automatically |

**Trade-offs to remember:** an orchestrator is a complex system you must learn and operate; shared-kernel isolation is lighter than a VM, so security needs care (Chapter 10); and stateful systems such as databases need extra thought to run in containers.

*Goes deeper in:* Chapter 6 (autoscaling with Kubernetes), Chapter 9 (reliability and deployment), Chapter 10 (container security), and the planned Cloud Architecture chapter.


### Common Architectural Patterns

#### Monolithic Architecture

A **monolithic architecture** bundles all components of an application into a single, tightly-coupled unit where everything is deployed together.

##### Diagram

```mermaid
flowchart TB
    A[User] --> B[Monolith App]
    B --> C[Database]
```

A more detailed view:

```mermaid
graph LR
    UI[User Interface] --> Monolith[Monolithic Application]
    API[API Layer] --> Monolith
    BLL[Business Logic] --> Monolith
    DAL[Data Access Layer] --> Monolith
    Monolith --> DB[(Database)]
```

ASCII view:

```mermaid
flowchart TD
    subgraph app["Monolith App"]
        direction LR
        ui["UI"] --- logic["Logic"] --- db["DB"]
    end
```

```mermaid
flowchart TD
    ui["User Interface"] --> bl["Business Logic"] --> da["Data Access"] --> db[("Single Database")]
```

##### Example Code: Flask Monolith

```python
# Everything in one place (e.g., Flask app)
from flask import Flask, request

app = Flask(__name__)

@app.route('/user/<id>')
def get_user(id):
    # Business logic and data access mixed
    user = db.query_user(id)
    return render_template('user.html', user=user)
```

A simpler version showing multiple routes:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/users')
def users():
    return "List of users"

@app.route('/orders')
def orders():
    return "List of orders"

if __name__ == "__main__":
    app.run()
```

A version with mixed UI + logic + data layer in one place:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_home()

def render_home():
    # UI + business logic + data access all here
    return "Welcome!"

if __name__ == '__main__':
    app.run()
```

##### Pros & Cons

| Pros                                            | Cons                                                     |
|-------------------------------------------------|----------------------------------------------------------|
| Simple to develop and deploy                    | Hard to scale                                            |
| Easier management for small apps                | Difficult to maintain as codebase grows                  |
| No inter-service communication complexity       | High risk of system-wide failure due to a single bug     |
| Easy to test                                    | Updates require redeploying the whole app                |

##### Use Cases

- Small-scale applications
- Startups / MVPs
- Simple CRUD-based apps


### Layered (N-Tier) Architecture

*This section is in [Volume 3, Chapter 8 — Clean Architecture](../volume-3-low-level-design/ch08-clean-architecture.md), next to that chapter's practice material, so it is not repeated here.*

#### Client-Server Architecture

**Client-server** divides the system into clients (requesters) and servers (responders).

##### Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: Request
    Server->>Client: Response
```

```mermaid
graph LR
  Client1[Client] --> Server[Server]
  Client2[Client] --> Server
```

##### Examples

- Web browser (client) communicates with web server (server).
- Mobile app (client) calls backend API (server).
- Email client connects to mail server.

##### Pros & Cons

| Pros                   | Cons                                 |
|------------------------|--------------------------------------|
| Centralized control    | Server can become a bottleneck       |
| Easier management      | Limited offline capability           |

##### Use Cases

- Web applications
- Email systems
- Most traditional web/mobile setups


#### Microservices Architecture

**Microservices** is a software design pattern that structures an application as a collection of small, independent services. Each service is responsible for a specific business capability and can be deployed, updated, and scaled independently.

**Key characteristics:**

- **Independently deployable:** Services are autonomous and can be upgraded without redeploying the entire system.
- **Loosely coupled:** Services interact via well-defined APIs, minimizing dependencies.
- **Scalable & fault-tolerant:** Each microservice can be scaled horizontally and failures are isolated.

##### Diagram

```mermaid
flowchart LR
    subgraph Users
        A[User]
    end
    subgraph Services
        B[API Gateway] --> C1[Service 1]
        B --> C2[Service 2]
        B --> C3[Service 3]
    end
    C1 --> D[Database 1]
    C2 --> E[Database 2]
    C3 --> F[Database 3]
    A --> B
```

A version showing specific service names:

```mermaid
graph LR
    UI[UI] --> API_GW[API Gateway]
    API_GW --> S1[User Service]
    API_GW --> S2[Order Service]
    API_GW --> S3[Product Service]
    S1 --> DB1[(User DB)]
    S2 --> DB2[(Order DB)]
    S3 --> DB3[(Product DB)]
```

```mermaid
graph LR
  User --> API_Gateway
  API_Gateway --> ServiceA[Product Service]
  API_Gateway --> ServiceB[Order Service]
  API_Gateway --> ServiceC[Payment Service]
  ServiceA --> DB1[(DB)]
  ServiceB --> DB2[(DB)]
  ServiceC --> DB3[(DB)]
```

```mermaid
graph TD
  API[API Gateway]
  MS1[User Service]
  MS2[Order Service]
  MS3[Inventory Service]

  API --> MS1
  API --> MS2
  API --> MS3
```

ASCII view:

```mermaid
flowchart LR
    gw["API Gateway"] --- us["User Service"]
    gw --- os["Order Service"]
    gw --- ps["Payment Service"]
    us <--> os <--> ps
```

##### Example Code

**Node.js (Express) microservice:**

```js
// order-service.js
const express = require('express');
const app = express();

app.get('/orders', (req, res) => {
  res.json([{ id: 1, item: 'Apple' }]);
});

app.listen(3001, () => console.log('Order Service running'));
```

**Python Flask microservice (Users service):**

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users/<id>')
def get_user(id):
    # This service only knows about users
    return jsonify({'id': id, 'name': 'Alice'})

if __name__ == "__main__":
    app.run(port=5001)
```

**Python Flask microservice (Products service):**

```python
# product_service.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/products')
def get_products():
    return jsonify([{"id": 1, "name": "Book"}])

if __name__ == '__main__':
    app.run(port=5001)
```

**Node.js (Express) — Users service:**

```javascript
const express = require('express');
const app = express();

app.get('/users', (req, res) => {
  res.json([{ name: "Alice" }, { name: "Bob" }]);
});

app.listen(3001, () => console.log('User service running on port 3001'));
```

**Flask microservice with `app.run()` in main:**

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users')
def users():
    return jsonify([{"id": 1, "name": "Alice"}])

if __name__ == "__main__":
    app.run(port=5001)
```

##### Communication

- **Synchronous:** REST, gRPC
- **Asynchronous:** Message queues (a buffer where one service leaves messages that another picks up later; Kafka and RabbitMQ are popular products; see Chapter 8, Messaging & Queues)

##### Pros & Cons

| Pros                                        | Cons                                               |
|---------------------------------------------|----------------------------------------------------|
| Independent deployment / scaling            | Increased system complexity                        |
| Flexibility in technology stack (polyglot)  | Need for robust DevOps and monitoring              |
| Better fault isolation                      | Data consistency, distributed tracing challenges   |
| Easier modular updates                      | Network overhead, more API call latency            |

##### Use Cases

- Large-scale applications
- Cloud-native apps (Netflix, Amazon, Uber)
- E-commerce platforms


### Event-Driven Architecture

*This section is in [Chapter 12 — Event-Driven Systems](ch12-event-driven-systems.md), next to that chapter's practice material, so it is not repeated here.*

### Multi-Tier Architecture — A Deep Dive

*This section is in [Volume 3, Chapter 8 — Clean Architecture](../volume-3-low-level-design/ch08-clean-architecture.md), next to that chapter's practice material, so it is not repeated here.*

### Microservices Architecture — A Deep Dive

Modern applications must be scalable, resilient, and maintainable. As businesses grow and requirements change rapidly, traditional monolithic architectures often fail to keep up. Enter **Microservices Architecture** — adopted by giants like Netflix, Uber, and Amazon.

#### Monolith vs. Microservices Comparison

| Aspect          | Monolithic Architecture     | Microservices Architecture      |
|-----------------|------------------------------|----------------------------------|
| Deployment      | Single unit                  | Independent services             |
| Scalability     | Whole app scales together    | Each service scales separately   |
| Technology      | Unified stack                | Polyglot (mixed stacks)          |
| Fault Tolerance | Single point of failure      | Isolated failures                |
| Maintainability | Hard as app grows            | Easier, modular updates          |
| Data Storage    | Centralized                  | Decentralized, per-service DBs   |

ASCII view of monolith vs microservices:

```mermaid
flowchart LR
    subgraph Monolith
        M["UI | Logic | Data<br/>(one unit)"]
    end
    subgraph Microservices
        A["Auth"]
        O["Orders"]
        P["Payment"]
    end
```


```mermaid
flowchart TB
    OS["Order service"] --- ODB[("Order DB")]
    PS["Payment service"] --- PDB[("Payment DB")]
    US["User service"] --- UDB[("User DB")]
    OS <-- "API / events" --> PS
    PS <-- "API / events" --> US
```


#### Identifying and Structuring Microservices

**Principles to follow:**

- **Business capabilities:** Each service aligns with a business function (e.g., Payments, Orders, Users).
- **Single Responsibility Principle:** One microservice should do one thing well.
- **Data ownership:** Each microservice owns its own data; avoid shared databases.
- **Independent deployment:** Updating one service should not require redeploying others.
- **Right granularity:** Avoid too-large (monolith) or too-fine (excessive complexity) services.

**Domain-Driven Design (DDD)** is a useful approach:

```mermaid
flowchart TB
    O["Order service"] <--> P["Payment service"] <--> U["User service"]
    O --- ODB[("Order DB")]
    P --- PDB[("Payment DB")]
    U --- UDB[("User DB")]
```


ASCII domain model:

```mermaid
flowchart LR
    O["Order"] <--> P["Payment"] <--> I["Inventory"]
```


#### Example: Node.js Microservice Skeleton

```js
// orders-service/app.js (Express)
const express = require('express');
const app = express();
const port = 3001;

app.use(express.json());

app.get('/orders/:id', (req, res) => {
  // Fetch order from Order DB
  res.json({ orderId: req.params.id, status: 'processing' });
});

app.listen(port, () => {
  console.log(`Order service listening at http://localhost:${port}`);
});
```

#### Communication Between Microservices

Microservices must interact to fulfill business flows. Two main models:

##### Synchronous Communication

- **REST APIs**
  - Easy to implement and widely supported.
  - Uses HTTP/JSON — higher latency.
- **gRPC**
  - Uses Protocol Buffers (binary format) for faster, low-latency RPC.
  - Great for high-performance internal communication.

**Example: REST call from Payment Service to Order Service (Python):**

```python
import requests

order = requests.get('http://orders-service:3001/orders/123').json()
```

**Example: gRPC service definition:**

```protobuf
// order.proto
syntax = "proto3";
service OrderService {
  rpc CreateOrder (OrderRequest) returns (OrderResponse);
}
message OrderRequest { string item_id = 1; }
message OrderResponse { string status = 1; }
```

**Example: Flask service with create_order endpoint:**

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    # Process order...
    return jsonify({'status': 'created'}), 201
```

**Example: User Service calling Order Service (Python):**

```python
# User Service
@app.route('/users/<id>/orders')
def get_orders(id):
    # REST call to Order Service
    response = requests.get(f'http://orders/api/orders?user={id}')
    return response.json()
```

##### Asynchronous Communication

- **Event-driven messaging:** Services publish events (e.g., `OrderCreated`) to a message broker (Kafka, RabbitMQ).
- Other services subscribe and react to these events.
- **Benefits:** Loose coupling, improved scalability, non-blocking.

**Example: Publish an Event with RabbitMQ (Node.js):**

```js
const amqp = require('amqplib');

async function publish() {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();
  const queue = 'order_created';
  const msg = JSON.stringify({ orderId: 123 });

  await channel.assertQueue(queue, { durable: true });
  channel.sendToQueue(queue, Buffer.from(msg));
  console.log('Order event published');
}

publish();
```

**Example: Python Kafka producer:**

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('order-events', json.dumps({'order_id': 123, 'status': 'created'}).encode())
```

**Event flow diagram:**

```mermaid
flowchart LR
    O["Order service"] -- "order_created" --> K[["Kafka"]]
    K --> P["Payment service"]
    P --> I["Inventory service"]
```


#### Key Challenges in Microservices

| Challenge             | Description                                                                       | Solutions / Tools                                |
|-----------------------|-----------------------------------------------------------------------------------|--------------------------------------------------|
| Data Consistency      | Eventual consistency due to distributed databases                                 | Compensating transactions, idempotent operations (safe to repeat; see the note under the HTTP methods table in Chapter 3) |
| Distributed Tracing   | Hard to trace requests across multiple services                                   | OpenTelemetry, Jaeger, Zipkin                    |
| Network Overhead      | More API calls mean more latency and failure points                               | Optimize with gRPC, caching, API Gateway         |
| Security              | Each service needs auth, encrypted communication                                  | OAuth2, JWT, mTLS, API Gateway                   |
| Operational Complexity| Deployment, orchestration, and monitoring across many services                    | Kubernetes, robust DevOps                        |

#### Example: Distributed Tracing (OpenTelemetry — Node.js)

```js
// Pseudo-setup for distributed tracing
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const provider = new NodeTracerProvider();
provider.register();
```

#### Scaling Microservices

Microservices shine in scalability:

- **Horizontal Scaling:** Add more instances of a service to handle increased load.
- **Database Sharding & Read Replicas:** Split data to optimize for high traffic. *Sharding* spreads one large database across several machines; a *read replica* is an extra copy that serves read requests. Both are covered in Chapter 7.

**Auto-Scaling (Kubernetes example):** *(Kubernetes is software that runs and scales containers, which are packaged applications, across many machines; see the containers primer earlier in this chapter, and Chapter 6 for its autoscaler.)*

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
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

**Horizontal scaling diagram:**

```mermaid
flowchart TB
    C([Client]) --> LB["Load balancer"]
    LB --> S1["Order S1"]
    LB --> S2["Order S2"]
    LB --> S3["Order S3"]
```


#### Real-World Examples

- **Netflix:** Streams video via hundreds of microservices — separate services for streaming, recommendations, personalization, scaled independently.
- **Uber:** Ride-matching, payments, and navigation are different services.
- **Amazon:** Search, payments, recommendations are modular, allowing real-time updates and massive scale.

#### Microservices — Tips for Success

- **Start with clear service boundaries:** Use DDD to avoid accidental monoliths.
- **Automate everything:** CI/CD, testing, deployment, and monitoring.
- **Invest in observability:** Logging, metrics, tracing — don't leave debugging until production.
- **Use an API Gateway:** Centralize cross-cutting concerns (authentication, rate-limiting, routing).
- **Design for failure:** Assume outages; use retries, circuit breakers, bulkheads, and graceful degradation.
- **Document APIs:** Keep OpenAPI/Swagger specs updated.
- **Version your contracts:** Don't break clients when updating APIs.
- **Keep data isolated:** No shared databases; use events for cross-service sync.
- **Right-size your services:** Too fine-grained increases complexity; too coarse defeats the purpose.
- **Secure all endpoints** and encrypt inter-service traffic.

#### Microservices — Interview Questions

- What are microservices and how do they differ from monolithic architecture?
- How do microservices communicate?
- What are the biggest challenges in microservices?
- How do you ensure data consistency?
- What is the role of an API Gateway?
- How do you structure microservices for a new project?
- How would you debug errors in a distributed microservices system?
- When would you choose microservices over N-tier or monolithic?
- When would you use synchronous vs. asynchronous communication?
- How do you implement service discovery and load balancing?
- What tools would you use for monitoring and observability?


### Event-Driven Architecture — A Deep Dive

**Event-Driven Architecture (EDA)** is a system design paradigm where components communicate through events. Rather than making direct synchronous calls, services publish events (like `OrderPlaced` or `UserRegistered`) and other services consume these events to trigger their own logic.

**Three key characteristics:**

- **Asynchronous processing:** Components don't wait for responses and continue processing other work.
- **Loose coupling:** Components interact via events, not direct calls, so they evolve independently.
- **Scalability & flexibility:** Easily handle spikes in workload without tight dependencies.

#### Why Use Event-Driven Architecture?

- **Asynchronous processing:** Services continue working while events are handled in the background.
- **Loose coupling:** Components evolve independently, increasing system flexibility.
- **Scalability:** Handles spikes and high traffic with ease.
- **Real-time responsiveness:** Ideal for finance, IoT, and notification systems.
- **Complex workflows:** Multiple services respond to a single event, supporting sophisticated business processes.

#### Core Components

| Component         | Role                                                          | Example                                  |
|-------------------|---------------------------------------------------------------|------------------------------------------|
| **Event Producer**| Generates events based on actions or changes                  | User places an order                     |
| **Event Broker**  | Routes, stores, and delivers events                           | Kafka, RabbitMQ, AWS EventBridge         |
| **Event Consumer**| Listens for events and performs actions                       | Payment service, Email notifier          |
| **Event Storage** | (Optional) Persists events for replay, auditing, or recovery  | Kafka log, AWS Kinesis                   |

##### Event Flow Sequence Diagram

```mermaid
sequenceDiagram
    participant Producer
    participant Broker
    participant Consumer
    participant Storage

    Producer->>Broker: Publish Event
    Broker->>Storage: Store Event (optional)
    Broker->>Consumer: Deliver Event
    Consumer->>Storage: (Optional) Query/Replay Event
```

#### Synchronous vs. Asynchronous Communication

| Synchronous                                 | Asynchronous (Event-Driven)               |
|---------------------------------------------|-------------------------------------------|
| Blocking calls (wait for response)          | Non-blocking (fire-and-forget)            |
| Tight coupling between components           | Decoupled; services operate independently |
| Example: HTTP REST API                      | Example: Kafka, RabbitMQ, SQS             |
| Can lead to bottlenecks                     | Promotes scalability and resilience       |

**Example: Synchronous (traditional HTTP call)**

```python
def place_order(order):
    response = payment_service.process_payment(order)
    if response.success:
        inventory_service.update(order)
```

**Example: Asynchronous (event-driven)**

```python
def place_order(order):
    event_broker.publish('OrderPlaced', order)
    # Continue without waiting for payment/inventory

# Payment service (subscriber)
def on_order_placed(event):
    process_payment(event.data)
```

#### Messaging Patterns

##### Publish-Subscribe (Pub/Sub)

- Producers send events to a "topic."
- All subscribed consumers receive the event, usually once and in real-time.
- Subscribers receive events in real-time but must be online.
- **Example:** Notifications to all followers when a user posts.

##### Event Streaming

- Events are stored in an ordered log; consumers can replay and process at their own pace.
- Useful when replayability or ordered processing is needed.
- **Example:** Analytics, audit logs, IoT sensor data, website analytics tracking user activity over time.

##### Mermaid Diagram: Pub/Sub vs. Event Streaming

```mermaid
graph LR
  A[Event Producer] -- Publish Event --> B[Event Broker]
  B -- Event --> C[Subscriber 1]
  B -- Event --> D[Subscriber 2]

  subgraph PubSub [Pub/Sub Model]
    A
    B
    C
    D
  end

  subgraph EventStreamingModel [Event Streaming Model]
    E[Event Producer] -- Append Event --> F[Event Log]
    F -- Read Event --> G[Consumer 1]
    F -- Read Event --> H[Consumer 2]
  end
```

##### Code Example: Pub/Sub with Python & Redis

```python
# Producer
import redis
r = redis.Redis()
r.publish('orders', 'order_placed:12345')

# Consumer
import redis
r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe('orders')
for message in pubsub.listen():
    if message['type'] == 'message':
        print('Received:', message['data'])
```

#### Event-Driven Architecture in Action: E-Commerce Example

**Workflow:**

1. **Order Service:** User places an order → emits `OrderPlaced` event.
2. **Payment Service:** Listens for `OrderPlaced` → processes payment.
3. **Inventory Service:** Listens for `OrderPlaced` → updates stock.
4. **Notification Service:** Listens for `OrderPlaced` → sends email/SMS.

This enables independent scaling and failure isolation for each service.

#### Challenges in Event-Driven Systems

| Challenge               | Description                                                               | Solutions / Tools                                 |
|-------------------------|---------------------------------------------------------------------------|---------------------------------------------------|
| Eventual Consistency    | State updates are not always immediate across services                    | Idempotent processing, compensating transactions  |
| Ordering Guarantees     | Events may arrive out of sequence in distributed systems                  | Partitioning, sequence numbers, deduplication     |
| Fault Tolerance         | Handling failures without data loss                                       | Dead-letter queues, retries, event replay         |
| Debugging Complexity    | Harder to trace asynchronous flows                                        | Distributed tracing (OpenTelemetry, Jaeger)       |

#### Best Practices

1. **Idempotent event processing:** Ensure consumers can safely process the same event multiple times.

```python
# Pseudocode for idempotency
if not already_processed(event_id):
    process_event(event)
```

2. **Implement dead-letter queues (DLQ):** Capture failed events for later inspection and manual handling.
3. **Choose the right broker:** Kafka for high-throughput streaming, RabbitMQ for classic queuing, AWS EventBridge for serverless event routing.
4. **Event versioning:** Use schema registries (e.g., [Apache Avro](https://avro.apache.org/)) to evolve event formats without breaking consumers.

#### Common Use Cases

- **Logging & auditing:** Capture all system changes for compliance and debugging.
- **Real-time notifications:** Messaging apps, stock price updates, push notifications.
- **Microservices decoupling:** Independent scalability and resilience.
- **IoT systems:** High-frequency, real-time sensor data processing.
- **E-commerce order processing:** Orchestrate complex, multi-step order workflows.

#### Event-Driven — Tips & Tricks

- **Always make consumers idempotent:** Use unique event IDs or database constraints.
- **Monitor event flows:** Use distributed tracing tools (Jaeger, OpenTelemetry).
- **Plan for schema evolution:** Add new fields, never remove or change existing ones without versioning.
- **Use partitioning for ordering:** Partition events by relevant key (e.g., user ID) to maintain order where required.
- **Embrace infrastructure as code:** Use Terraform or AWS CloudFormation to automate broker setup and scaling.
- **Monitor event lag:** Track how far behind consumers are from the latest event.
- **Back pressure handling:** Protect slow consumers from being overwhelmed.
- **Compensating transactions:** Use when eventual consistency isn't enough — e.g., refund a payment if order fails.
- **Testing:** Simulate failure scenarios and duplicate events during testing.

#### Event-Driven — Interview Prep

- Explain the difference between Pub/Sub and Event Streaming.
- How do you ensure idempotency in event consumers?
- What are dead-letter queues and why are they important?
- Describe a real-world use case for event-driven architecture.
- How would you handle event versioning and schema evolution?


### Factors Influencing Architecture Selection

When choosing an architectural style, consider:

1. **Business Needs:** What is the system's core purpose?
2. **Scalability:** Expected load and growth.
3. **Performance:** Latency, throughput, and responsiveness.
4. **Maintainability:** Ease of updates, fixes, and evolution.
5. **Team Skillsets:** Familiarity with distributed systems, automation, etc.
6. **Time to Market:** Speed vs. long-term scalability.

| Architecture     | Best For                                       | Avoid When                          |
|------------------|------------------------------------------------|-------------------------------------|
| Monolithic       | Small, simple apps, MVPs, startups             | Large/complex, needs high scale     |
| Layered (N-Tier) | Enterprise apps, CRMs, banking systems         | Performance-critical hot paths      |
| Microservices    | Large-scale, cloud-native, independent scaling | Small/simple projects               |
| Event-Driven     | Real-time, IoT, async, scalable systems        | When strong consistency is needed   |

#### Example: When to Use Which?

- **Building a CRM for a small business?** Go for **Layered Architecture**.
- **Launching an MVP for a startup?** Start with **Monolithic**; split into microservices if it grows.
- **Creating a real-time notification system?** **Event-Driven** is a strong fit.
- **Developing a large e-commerce platform?** **Microservices** for independent scaling of catalog, orders, payments.


### Patterns Worth Knowing (Beyond the Big Four)

The four main patterns above (monolith, layered, microservices, event-driven) are *categories*. The patterns below are *specific techniques* that show up inside or across those categories.

#### Modular Monolith

A monolith **internally organized as if it were microservices** — clear module boundaries, no cross-module DB access, well-defined interfaces — but deployed as a single binary.

**Why it matters:** combines monolith's deployment simplicity with microservices' modularity. Often the *correct* starting point for a new system. You can split it into actual services later if growth demands it.

#### Strangler Fig — How to Migrate Monolith → Microservices

Named after the strangler fig tree that grows around an existing tree and eventually replaces it. Coined by Martin Fowler.

**The technique:**
1. Put a **facade** (API Gateway or reverse proxy) in front of the monolith.
2. Build the new microservice alongside the monolith.
3. Reroute the facade so specific endpoints go to the microservice instead of the monolith.
4. Once everything is moved, the monolith dies.

> **Why it works:** no "big bang" rewrite (which almost always fails). You ship incrementally, and at any point you can stop. The new code never has to be perfect because the monolith is always the fallback.

#### Backend for Frontend (BFF)

Each frontend (web, iOS, Android, smart TV) gets its **own dedicated backend service** that aggregates calls to underlying microservices, shaping responses for that frontend's needs.

**Why:** different clients have different data needs and constraints. The iOS app wants minimal data on cellular; the web wants more. Without a BFF, every microservice has to support every client variation — or the frontend makes 10 separate calls.

```mermaid
flowchart LR
    Clients([Clients]) --> BW["BFF for Web"]
    Clients --> BI["BFF for iOS"]
    Clients --> BT["BFF for TV"]
    BW --> MS["Microservices"]
    BI --> MS
    BT --> MS
```


### CQRS (Command Query Responsibility Segregation)

*This section is in [Volume 3, Chapter 12 — Event Bus, CQRS & Event Sourcing](../volume-3-low-level-design/ch12-event-bus-cqrs-and-event-sourcing.md), next to that chapter's practice material, so it is not repeated here.*

#### Event Sourcing

Instead of storing the *current state*, store the *sequence of events* that produced it. Current state is derived by replaying events.

**Why:** complete audit log built in, time-travel debugging, easy to derive new read models.

**Trade-off:** querying current state requires replay or maintained projections. Schema evolution is hard.

> Often paired with CQRS: events are the write model, projections are the read model.

### Saga Pattern (Distributed Transactions Without 2PC)

*This section is in [Volume 3, Chapter 12 — Event Bus, CQRS & Event Sourcing](../volume-3-low-level-design/ch12-event-bus-cqrs-and-event-sourcing.md), next to that chapter's practice material, so it is not repeated here.*

#### When NOT to Use Microservices

A microservices anti-checklist. Stay with a monolith if:

- You have fewer than ~10 engineers.
- Your domain isn't well understood yet (service boundaries will be wrong).
- You don't have CI/CD, observability, and on-call rotation already.
- Different parts of your system don't scale independently (no scaling problem to solve).
- Latency is critical and you can't afford network hops between services.

> **The truth:** every team that adopts microservices too early ends up with a *distributed monolith* — slower than a monolith, harder to debug, and more expensive to operate.


### Practical Trade-offs

| Pattern         | Pros                  | Cons                              | Use Cases                  |
|-----------------|-----------------------|-----------------------------------|----------------------------|
| Monolithic      | Simple, fast to start | Hard to scale, maintain           | Startups, simple apps      |
| Layered (N-Tier)| Separated concerns    | Overhead, possible coupling       | Enterprise, banking        |
| Microservices   | Scale, flexibility    | Complexity, consistency problems  | Large, cloud-native        |
| Event-Driven    | Async, decoupled      | Debugging, ordering, consistency  | IoT, real-time, logging    |


### Tips & Tricks

A merged master list of advice across all patterns.

#### General

- **Start simple, scale out.** Begin with monolithic or layered; refactor to microservices when growth demands.
- **Document boundaries.** In microservices, define clear API contracts and data ownership to avoid integration mess.
- **Document your architecture** with diagrams and clear descriptions.
- **Design for change.** Assume requirements will change; favor modular, loosely-coupled designs.
- **Choose the right pattern.** Not every problem needs microservices. Start with monolithic or multi-tier, and migrate when scaling demands it.

#### Automation & Observability

- **Automate everything.** Especially with microservices: CI/CD, monitoring, automated testing.
- **Monitor performance.** Use tools like Prometheus, Grafana, or Datadog to track bottlenecks and system health.
- **Centralized logging.** Essential for debugging in distributed/event-driven systems.
- **Prepare for debugging.** Implement distributed tracing (OpenTelemetry, Jaeger) early.
- **Automate testing.** Especially in event-driven and microservices systems, automated integration tests are vital.

#### Communication

- **Choose the right communication pattern.** Use **REST/gRPC** for synchronous, **Kafka/RabbitMQ** for async/event-driven.
- **Use API gateways** to manage requests in microservices architectures.
- **Document interfaces** — clearly specify contracts between services and layers.
- **Version your contracts** — don't break clients when updating APIs.

#### Reliability

- **Handle failures gracefully.** In event-driven designs, use **dead-letter queues** and **idempotent handlers**.
- **Embrace eventual consistency** in distributed/event-driven systems — design for eventual rather than immediate.
- **Use retries, circuit breakers, and graceful degradation** for distributed systems.
- **Consistency vs. Availability** — understand the CAP theorem (Chapter 7) and make informed trade-offs.

#### Security

- **Security first.** Isolate services, secure APIs, and encrypt inter-service communication.
- Authentication, authorization, and data protection — especially as services multiply.

#### Data

- **Data ownership in microservices.** Each microservice should own its database. Avoid sharing schemas.
- **Plan for schema changes.** Use event versioning or backward-compatible messages in EDA.

#### Evolution

- **Plan for evolution.** Choose an architecture that can evolve as your business needs change.


### Sample Interview Questions

- What are the differences between monolithic, layered, microservices, and event-driven architectures?
- How does a 2-Tier architecture differ from a 3-Tier architecture?
- How does scalability improve in a multi-tier system?
- When would you choose microservices over a monolith?
- What are the key challenges of microservices, and how do you mitigate them?
- How would you handle data consistency in distributed systems?
- What is the role of an API Gateway?
- When would you use synchronous vs. asynchronous communication?
- Explain the difference between Pub/Sub and Event Streaming.
- How do you ensure idempotency in event consumers?
- What are dead-letter queues and why are they important?
- How do you implement service discovery and load balancing?
- What tools would you use for monitoring and observability in a distributed system?


### Summary & Key Takeaways

- **Monolithic:** Simple, good for small apps or prototypes; struggles at scale.
- **Layered (N-Tier):** Clear separation, maintainable; can have performance overhead.
- **Client-Server:** Foundational for web/mobile; server can be a bottleneck.
- **Microservices:** Scalable, resilient, flexible; complex to manage.
- **Event-Driven:** Decoupled, real-time, scalable; introduces consistency and debugging challenges.

> *"Choose architecture based on business needs, technical requirements, and scalability goals — not just trends."*


### Further Reading

- [Martin Fowler — Microservices](https://martinfowler.com/articles/microservices.html)
- [Martin Fowler — Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
- [Martin Fowler — Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Microservices.io (Chris Richardson)](https://microservices.io/)
- [Event-Driven Architecture on AWS](https://aws.amazon.com/architecture/event-driven/)
- [AWS Multi-Tier Architecture Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/multi-tier-architectures.html)
- [Microsoft Patterns & Practices — Multi-tier Architecture](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)


**Next Up:** [Chapter 5 — Web Concepts in System Design →](./5%20-%20Web%20Concepts%20in%20System%20Design%20(System%20Design%20Fundamentals).md) — sessions, serialization, CORS, and the practical web-specific concerns that build on top of these architectural patterns.


*(From AI Library chapter 4.)*

