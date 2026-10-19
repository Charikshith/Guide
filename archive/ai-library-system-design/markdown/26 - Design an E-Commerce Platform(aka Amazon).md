# Designing a Scalable E-Commerce Marketplace Platform (Amazon)

Designing a high-scale **multi-vendor e-commerce marketplace** — think Amazon or Flipkart — requires a deep understanding of system design principles, from functional and non-functional requirements to architecture, scaling, and operational challenges. In this case study, we'll walk through the end-to-end process of designing such a platform.

---

## 26.1 Learning Outcomes

After working through this case study, you'll be able to:

1. Design **multi-warehouse inventory** that prevents overselling across distribution centers.
2. Implement the **checkout Saga** — coordinating cart, inventory, payment, shipping without a distributed transaction.
3. Build **product search** with faceted filtering, ranking, and personalization.
4. Outline a **recommendation system** for "Customers also bought" and personalized homepage.
5. Handle **returns and refunds** as a first-class workflow.

---

## Table of Contents

- [26.2 What Are We Building?](#262-what-are-we-building)
- [26.3 Functional Requirements](#263-functional-requirements)
- [26.4 Non-Functional Requirements](#264-non-functional-requirements)
- [26.5 Core System Design Challenges](#265-core-system-design-challenges)
- [26.6 Assumptions & Constraints](#266-assumptions--constraints)
- [26.7 Scale Estimation & Bottlenecks](#267-scale-estimation--bottlenecks)
- [26.8 Service Decomposition & APIs](#268-service-decomposition--apis)
- [26.9 Service Communication Patterns](#269-service-communication-patterns)
- [26.10 Database & Storage Choices](#2610-database--storage-choices)
- [26.11 Caching & Queueing Strategies](#2611-caching--queueing-strategies)
- [26.12 Tech Stack & Infra Decisions](#2612-tech-stack--infra-decisions)
- [26.13 Architecture Diagrams](#2613-architecture-diagrams)
- [26.14 Sample Code & API Flows](#2614-sample-code--api-flows)
- [26.16 Tips & Tricks](#2616-tips--tricks)
- [26.17 Conclusion](#2617-conclusion)

---

## 26.2 What Are We Building?

A **multi-vendor e-commerce platform** for buyers and sellers. Core functionalities include:

- Browsing and searching products.
- Managing inventory and product listings.
- Shopping cart and secure checkout.
- Payment processing and fraud detection.

**Non-negotiable attributes:** Scalable, secure, consistent.

---

## 26.3 Functional Requirements

- **User registration & authentication** (Buyers/Sellers, with MFA).
- **Product catalog management** (CRUD for products).
- **Inventory consistency during checkout** (avoid overselling).
- **Shopping cart & order management** (persistent carts, order lifecycle).
- **Secure payment processing** (PCI-compliant integration).
- **Basic fraud detection & alerts** (rule-based checks, admin/user notifications).
- **Seller dashboard** (sales, product management, payouts).
- **Administrator tools** (moderation, platform health, disputes).

**Users & roles:**

- **Buyers:** Search, browse, cart, checkout, track orders.
- **Sellers:** List/manage products, handle orders, track earnings.
- **Administrators:** Content moderation, system health, dispute resolution.

---

## 26.4 Non-Functional Requirements

- **Performance:** <300ms latency for common queries.
- **Scalability:** Start with 10,000 concurrent users, elastic growth.
- **Availability:** 99.9% uptime, fault-tolerant services.
- **Security:** OAuth2/JWT, PCI-DSS for payments, encrypted storage.
- **Consistency:** Strong consistency for inventory updates.
- **Maintainability:** Modular microservices, easy onboarding.

---

## 26.5 Core System Design Challenges

- **Inventory accuracy:** Prevent overselling (real-time updates, distributed locks).
- **High availability:** Resilient to failures, auto-scaling, load balancing.
- **Secure payments:** Sensitive data handling, fraud detection.
- **System scalability:** Sharding, partitioning, stateless services.
- **Efficient search:** Fast, relevant search over millions of products (indexing, caching).

---

## 26.6 Assumptions & Constraints

### 26.6.1 Assumptions

- Users have stable internet (no offline mode).
- Payments via third-party gateway (Stripe/Razorpay).
- Sellers handle shipping/logistics.
- Initial catalog: ~500,000 products.
- Basic, rule-based fraud detection.

### 26.6.2 Constraints

- MVP launch in 3–4 months.
- Cloud services preferred (budget).
- Minimal DevOps/SRE support.
- Limited personalization (no ML recommendations).
- Regulatory compliance: PCI-DSS, GDPR.

---

## 26.7 Scale Estimation & Bottlenecks

### 26.7.1 Scale Numbers

| Metric                  | Initial Estimate                |
|-------------------------|---------------------------------|
| Registered Users        | 1,000,000                       |
| Daily Active Users (DAU)| 10,000                          |
| Peak Traffic            | 100 requests/sec (sales events) |
| Product Catalog Size    | 500,000 products                |
| Orders/Day              | 1,000                           |
| Active Sellers          | 5,000                           |

> While these numbers are for launch, design must anticipate growth — seamless scaling is non-negotiable.

### 26.7.2 Critical Bottlenecks

| Bottleneck             | Why It's Painful                                  | Solution                                       |
|------------------------|---------------------------------------------------|------------------------------------------------|
| Search Latency         | <300ms for 500K+ products                         | Elasticsearch, Redis caching                   |
| Inventory Consistency  | Simultaneous purchases can oversell               | DB transactions, locks, message queues         |
| Checkout Flows         | Reliable orders during peaks                      | Async event-driven, external payments          |
| Database Hotspots      | Heavy reads/writes on popular products            | Sharding, caching, read replicas               |
| Fraud Detection        | Suspicious transactions in real-time              | Rule-based engine, event-based scaling         |

### 26.7.3 Example: Fast Product Search

```python
def search_products(query):
    # Try cache first for popular queries
    results = redis.get(f"search:{query}")
    if results:
        return results
    # Fallback to Elasticsearch
    results = elasticsearch.search(index="products", q=query)
    redis.set(f"search:{query}", results, ex=60)
    return results
```

### 26.7.4 Example: Atomic Stock Reservation

```sql
BEGIN;
SELECT stock FROM inventory WHERE product_id=123 FOR UPDATE;
UPDATE inventory SET stock = stock - 1 WHERE product_id=123 AND stock > 0;
COMMIT;
```

### 26.7.5 Example: Rule-Based Fraud Detection

```python
def is_fraudulent(order):
    if order.amount > 1000 and order.user.orders_today > 3:
        return True
    if order.card in BLOCKLISTED_CARDS:
        return True
    return False
```

### 26.7.6 Checkout Flow Diagram

```mermaid
flowchart TB
    U(["User"]) -- "POST /checkout" --> O["Order service"]
    O --> E1[["Order placed event"]]
    E1 --> P["Payment service (async)"]
    P --> E2[["Payment success / failure event"]]
    E2 --> N["Notification service"]
```


### 26.7.7 Bottleneck Diagram

```mermaid
flowchart LR
    UR(["User request"]) --> GW["API gateway"] --> SL["Service layer"]
    SL --> CS["Catalog / search"] --> ESr[("Elasticsearch")]
    SL --> IV["Inventory"] --> PG[("Postgres + locks")]
    SL --> OR["Orders"] --> Q[["Queue"]]
```


---

## 26.8 Service Decomposition & APIs

### 26.8.1 Core Services

| Service                  | Responsibility                                                                |
|--------------------------|--------------------------------------------------------------------------------|
| **User Service**         | Registration, login, authentication (OAuth2/JWT), profile.                     |
| **Product Catalog**      | Product CRUD, category, price, image, search.                                  |
| **Inventory Service**    | Real-time stock level management, stock reservation during checkout.           |
| **Order Service**        | Shopping cart, checkout, order lifecycle, price calculation, discounts.        |
| **Payment Service**      | Secure payment processing, retries, basic fraud detection.                     |
| **Notification Service** | Email/SMS notification on events.                                              |
| **Admin Service**        | Seller/product moderation, platform health monitoring, admin controls.         |

### 26.8.2 Example API Endpoints

**User Service:**

```http
POST /api/v1/users/register
POST /api/v1/users/login
GET  /api/v1/users/profile
```

**Catalog Service:**

```http
GET  /api/v1/products
GET  /api/v1/products/{id}
POST /api/v1/products
```

**Inventory Service:**

```http
GET  /api/v1/inventory/{productId}
POST /api/v1/inventory/reserve
POST /api/v1/reserve-stock
```

**Order Service:**

```http
POST /api/v1/cart/add
POST /api/v1/checkout
GET  /api/v1/orders/{orderId}
```

**Payment Service:**

```http
POST /api/v1/payments/initiate
POST /api/v1/payments/verify
```

**APIs should be:** RESTful, stateless, versioned (`/api/v1/...`).

---

## 26.9 Service Communication Patterns

A hybrid model:

### 26.9.1 Synchronous (HTTP REST)

For real-time flows (e.g., validating inventory during checkout):

```mermaid
sequenceDiagram
  participant User
  participant OrderService as Order Service
  participant InventoryService as Inventory Service

  User->>OrderService: Add to Cart (POST /cart/add)
  OrderService->>InventoryService: Check Stock (GET /inventory/{productId})
  InventoryService-->>OrderService: Stock OK
  OrderService-->>User: Added to Cart
```

### 26.9.2 Asynchronous (Event-Driven)

For non-blocking flows (e.g., notifications, background updates):

```mermaid
sequenceDiagram
  participant OrderService as Order Service
  participant InventoryService as Inventory Service
  participant NotificationService as Notification Service
  participant MQ as Message Queue

  OrderService->>MQ: Publish "OrderPlaced" Event
  InventoryService->>MQ: Subscribe "OrderPlaced", update stock
  NotificationService->>MQ: Subscribe "OrderPlaced", send email/SMS
```

**Tech:** Kafka, RabbitMQ, AWS SQS.

---

## 26.10 Database & Storage Choices

| Data Type        | Primary Store                                    | Notes                                       |
|------------------|--------------------------------------------------|---------------------------------------------|
| User Data        | PostgreSQL                                       | Strong consistency                          |
| Product Catalog  | Elasticsearch + PostgreSQL                       | Search-optimized + backup                   |
| Inventory        | PostgreSQL                                       | Strict consistency on stock                 |
| Orders           | PostgreSQL                                       | Transactional                               |
| Payments         | PostgreSQL                                       | Encrypted fields                            |
| Logs/Events      | Object Storage                                   | E.g., AWS S3                                |

**In-memory stores:** Redis for caching, session management, fast stock reads.

### 26.10.1 Example: Create Orders Table

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  product_id INT REFERENCES products(id),
  quantity INT NOT NULL,
  status VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 26.10.2 Example: Elasticsearch Product Mapping

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name":        { "type": "text" },
      "description": { "type": "text" },
      "category":    { "type": "keyword" },
      "price":       { "type": "float" }
    }
  }
}
```

---

## 26.11 Caching & Queueing Strategies

### 26.11.1 Caching (Redis)

- Hot product data (popular products, categories).
- User session tokens.
- Stock levels (read-heavy optimization).

```python
import redis, json

r = redis.Redis(host='localhost', port=6379, db=0)

# Cache product details
r.setex(f"product:{product_id}", 3600, json.dumps(product_data))  # Expires in 1 hour

# Get cached product
cached = r.get(f"product:{product_id}")
if cached:
    product = json.loads(cached)
else:
    # Fetch from DB and cache
    pass
```

A simpler example:

```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
product_id = 1234
product_data = {"name": "T-shirt", "stock": 52}
r.set(f"product:{product_id}", str(product_data), ex=300)  # expires in 5 mins
```

### 26.11.2 Queues (Kafka/SQS/RabbitMQ)

- Order placement events → inventory update.
- Payment success events → order confirmation, notification.
- Asynchronous email/SMS notification.

```python
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.send('order-events', b'{"order_id":123, "status":"PLACED"}')
producer.close()
```

**Sample event (Order Placed):**

```json
{
  "eventType": "OrderPlaced",
  "orderId": "12345",
  "userId": "u789",
  "timestamp": "2024-06-11T10:11:12Z"
}
```

**Summary:**

- **Caching = speed up reads.**
- **Queues = decouple heavy async tasks.**

---

## 26.12 Tech Stack & Infra Decisions

| Layer        | Tech Choice                                      | Rationale                                          |
|--------------|--------------------------------------------------|----------------------------------------------------|
| Database     | PostgreSQL                                       | Transactional, ACID, relational                    |
| Search       | Elasticsearch                                    | Fast full-text search                              |
| Caching      | Redis                                            | In-memory, fast reads                              |
| Message Queue| Kafka (preferred), AWS SQS, RabbitMQ             | Decouple async flows                               |
| Cloud        | AWS/GCP/Azure managed services                   | Reduce ops overhead                                |
| Auth         | OAuth2/OpenID Connect, JWT                       | Stateless, secure                                  |
| Payments     | Stripe/Razorpay                                  | PCI compliance, secure                             |
| Comms        | REST APIs, event-driven for async                | Hybrid pattern                                     |

### 26.12.1 JWT Token Example

```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjM0fQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 26.12.2 Stripe Payment Intent

```python
import stripe
stripe.api_key = "sk_test_..."
intent = stripe.PaymentIntent.create(
  amount=5000,
  currency='usd',
  payment_method_types=['card'],
)
```

---

## 26.13 Architecture Diagrams

### 26.13.1 High-Level Mermaid Architecture

```mermaid
graph TD
  subgraph APILayer [API Layer]
    A1[User API]
    A2[Catalog API]
    A3[Order API]
    A4[Payment API]
    A5[Admin API]
  end
  subgraph Services
    S1(User Service)
    S2(Catalog Service)
    S3(Inventory Service)
    S4(Order Service)
    S5(Payment Service)
    S6(Notification Service)
    S7(Admin Service)
  end
  subgraph DataStore [Data Store]
    D1[(PostgreSQL)]
    D2[(Elasticsearch)]
    D3[(Redis Cache)]
    D4[("Object Storage: S3")]
  end
  subgraph Infra
    Q1[Kafka/SQS]
    EXT[Stripe/Razorpay]
  end

  A1 --> S1
  A2 --> S2
  A3 --> S4
  A4 --> S5
  A5 --> S7

  S1 --> D1
  S2 --> D2
  S2 --> D1
  S3 --> D1
  S4 --> D1
  S5 --> D1
  S5 --> EXT
  S6 --> Q1
  S7 --> D1

  S3 --> D3
  S2 --> D3

  S4 -.->|Async Events| Q1
  Q1 -.-> S3
  Q1 -.-> S6
  Q1 -.-> S4

  S6 --> D4
```

### 26.13.2 Detailed Architecture (with DBs per service)

```mermaid
graph TD
    Client["User (Web/App)"]
    APIGateway[API Gateway]
    UserService[User Service]
    ProductService[Product Catalog Service]
    InventoryService[Inventory Service]
    OrderService[Order Service]
    PaymentService[Payment Service]
    NotificationService[Notification Service]
    AdminService[Admin Service]
    RedisCache[Redis Cache]
    MessageQueue["Message Queue (Kafka/SQS)"]
    PaymentGateway["Payment Gateway (Stripe, Razorpay)"]
    UserDB[("User DB - PostgreSQL")]
    ProductDB[("Product DB - PostgreSQL")]
    SearchDB[("Search DB - Elasticsearch")]
    InventoryDB[("Inventory DB - PostgreSQL")]
    OrderDB[("Order DB - PostgreSQL")]
    PaymentDB[("Payment DB - PostgreSQL")]

    Client-->|REST API|APIGateway
    APIGateway-->|Sends to|UserService
    APIGateway-->|Sends to|ProductService
    APIGateway-->|Sends to|OrderService
    APIGateway-->|Sends to|PaymentService
    APIGateway-->|Sends to|AdminService

    UserService-->|CRUD|UserDB
    UserService-->|Cache|RedisCache
    ProductService-->|CRUD|ProductDB
    ProductService-->|Search|SearchDB
    ProductService-->|Cache|RedisCache
    InventoryService-->|CRUD|InventoryDB
    InventoryService-->|Cache|RedisCache
    OrderService-->|CRUD|OrderDB
    OrderService-->|Cache|RedisCache
    PaymentService-->|CRUD|PaymentDB
    PaymentService-->|Cache|RedisCache
    PaymentService-->|Process|PaymentGateway

    OrderService-->|OrderPlacedEvent|MessageQueue
    PaymentService-->|PaymentSuccessEvent|MessageQueue
    MessageQueue-->|Consume|InventoryService
    MessageQueue-->|Consume|NotificationService
    NotificationService-->|Send|EmailSMS[Email/SMS Provider]
```

### 26.13.3 Service Communication Diagram

```mermaid
graph TD
  UserService([User Service])
  CatalogService([Product Catalog Service])
  InventoryService([Inventory Service])
  OrderService([Order Service])
  PaymentService([Payment Service])
  NotificationService([Notification Service])
  AdminService([Admin Service])

  UserService -- Registers/Login --> CatalogService
  CatalogService -- Product Info --> InventoryService
  InventoryService -- Stock Check --> OrderService
  OrderService -- Create Order --> PaymentService
  PaymentService -- Payment Status --> OrderService
  OrderService -- Order Events --> NotificationService
  AdminService -- Moderation --> CatalogService
```

---

## 26.14 Sample Code & API Flows

### 26.14.1 Reserve Stock (Inventory Service)

```python
# Flask-like pseudocode
@app.route('/api/v1/reserve-stock', methods=['POST'])
def reserve_stock():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    with db.transaction():
        current = db.get_stock(product_id)
        if current < quantity:
            return {"error": "Insufficient stock"}, 409
        db.update_stock(product_id, current - quantity)
    # Emit event to Kafka for order processing
    kafka.produce('order_stock_reserved', {'product_id': product_id, 'quantity': quantity})
    return {"status": "reserved"}
```

### 26.14.2 Order Placement (Order Service)

```python
@app.route('/api/v1/checkout', methods=['POST'])
def checkout():
    order_data = request.get_json()
    # Validate cart, reserve stock via Inventory Service
    reserve_resp = requests.post('http://inventory/api/v1/reserve-stock', json=order_data['cart'])
    if reserve_resp.status_code != 200:
        return {"error": "Stock unavailable"}, 409
    # Proceed with payment
    payment_resp = requests.post('http://payment/api/v1/payments/initiate', json=order_data['payment'])
    if payment_resp.status_code != 200:
        return {"error": "Payment failed"}, 402
    # Save order, emit async events
    db.save_order(order_data)
    kafka.produce('order_placed', order_data)
    return {"status": "order placed"}
```

### 26.14.3 User Registration (Node.js)

```js
app.post('/api/v1/users/register', async (req, res) => {
  const { email, password } = req.body;
  const hash = await bcrypt.hash(password, 12);
  await db.users.insert({ email, password_hash: hash });
  res.status(201).json({ success: true });
});
```

### 26.14.4 Product Search Handler (Node.js)

```js
app.get('/api/v1/products', async (req, res) => {
  const { search, category } = req.query;
  const cacheKey = `products:${search}:${category}`;
  let products = await redis.get(cacheKey);
  if (!products) {
    products = await elasticsearch.search({ query: { match: { name: search } } });
    await redis.set(cacheKey, JSON.stringify(products), 'EX', 60 * 5);
  }
  res.json(JSON.parse(products));
});
```

### 26.14.5 Kafka Event Publishing & Consumption (Node.js)

```js
// Publish event
await kafka.produce('order-placed', { orderId, productId, quantity });

// Inventory Service consumes event
kafka.consume('order-placed', async (msg) => {
  await db.inventory.update({ productId: msg.productId }, { $inc: { stock: -msg.quantity } });
});
```

### 26.14.6 Checkout Flow Steps

1. API Gateway routes request to Order Service.
2. Order Service checks stock via Inventory Service.
3. If available, creates order and triggers Payment Service.
4. Payment Service processes via external gateway (Stripe/Razorpay).
5. On payment success, events are published to Message Queue for:
   - Inventory update (reserve stock).
   - Notification dispatch (email/SMS).

---

## 26.15 Beyond MVP — What a Senior Designer Adds

### 26.15.1 The Checkout Saga (Distributed Transaction Without 2PC)

Checkout touches multiple services: cart, inventory, payment, shipping. You can't wrap them in a DB transaction. Use a **Saga** (see Chapter 4):

```mermaid
flowchart TB
    S1["1. Reserve inventory: success"] --> S2["2. Charge payment: success"] --> S3["3. Create order: success"] --> S4["4. Notify shipping: success"] --> S5["5. Send confirmation: success<br/>(commit)"]
    S2 -. "if step 2 fails" .-> X["compensate(1): release inventory, then abort"]
    style X fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
```


Implement with a **Saga orchestrator** service (or a workflow engine like Temporal / AWS Step Functions). Each step must be **idempotent** so retries don't double-charge.

### 26.15.2 Multi-Warehouse Inventory

Real Amazon ships from hundreds of warehouses. A product isn't "in stock" globally — it's in stock *in specific warehouses*. Checkout needs to:

1. Find warehouses with the item.
2. Pick the closest/cheapest to the user.
3. Reserve from that specific warehouse.

If the chosen warehouse runs out between checkout and shipment, **route to another warehouse** automatically.

**Data model:** `inventory(item_id, warehouse_id, count)` instead of `inventory(item_id, count)`.

### 26.15.3 Search & Faceted Filtering

E-commerce search is largely about filtering. Users search "laptop" then filter by brand, price, RAM, screen size, rating, etc. Each filter must update results instantly.

**Implementation:** Elasticsearch with **aggregations** — same query returns matching docs *and* facet counts (e.g., "MacBook: 142, Dell: 87, HP: 65"). Pre-compute popular facets in Redis to speed up first paint.

### 26.15.4 Recommendation Engine

Two main types:

- **Item-to-item:** "Customers who bought X also bought Y." Collaborative filtering. Computed offline; cached per item.
- **User-to-item:** "Recommended for you." Combines user history, embeddings, and demographic signals. Updated nightly or real-time depending on freshness needs.

For freshness-sensitive items (news, fashion trends), use real-time updates from a stream processor (Flink, Spark Streaming).

### 26.15.5 Reviews & Ratings

Heavily skewed: most ratings are 5-star. Show average + count, but also:

- **Most helpful review** (community-upvoted).
- **Critical review** highlighted alongside positive.
- **Verified purchase** badge to reduce fake reviews.
- **Anti-spam:** detect review velocity, IP clusters, language similarity to known fake review patterns.

### 26.15.6 Returns & Refunds Workflow

Often more complex than the order itself:

1. User requests return → eligibility check (within window, condition).
2. Generate return label → email to user.
3. User ships item back → tracking starts.
4. Warehouse receives → quality check.
5. Refund to original payment method (or store credit).
6. Update inventory (resellable items go back, damaged ones go to liquidation).

This is a multi-day Saga with manual steps. Underinvested by most early-stage e-commerce platforms.

### 26.15.7 Personalization & Homepage

The Amazon homepage is different for every user. Each card (deals, recently viewed, recommendations, restock) is rendered from a different service. **Use a BFF** (Chapter 4) that composes the page from microservice calls in parallel; each card has its own SLA so a slow service doesn't block the page.

### 26.15.8 Internationalization

Multi-currency, multi-language, multi-warehouse-region. Often modeled as **separate logical stores** sharing some infrastructure (catalog, sellers) but with region-specific pricing, tax, shipping rules.

### 26.15.9 Fraud Detection

Real-time evaluation at checkout: device fingerprint, velocity (5 orders to different addresses in 10 minutes?), card BIN reputation, address risk. ML model scores each order; high-risk orders go to manual review or step-up verification (3D Secure).

---

## 26.16 Tips & Tricks

### 26.16.1 Consistency

- **Strong consistency for inventory:** Use DB transactions with row-level locking or atomic operations to prevent overselling. For high-scale, consider distributed locks (Redis Redlock) or event-sourcing.
- **Use eventual consistency** for non-critical flows (notifications).
- **Design idempotent endpoints** for order and payment flows to handle retries gracefully.

### 26.16.2 Search

- **Search scaling:** Use Elasticsearch or Redisearch for fast, full-text product search. Periodically sync with primary DB to avoid stale indexes.
- **Regularly re-index** product data.

### 26.16.3 Caching

- **Cache hot products, categories, and stock levels.** Use short TTLs for inventory to reduce staleness.
- **Monitor cache hit rates** — if Redis hit rate drops, you may be caching the wrong data.

### 26.16.4 Async Processing

- **Async processing:** Offload non-critical user flows (emails, notifications, analytics) to message queues.
- **Decouple with message queues:** Use queues for non-blocking, asynchronous operations.

### 26.16.5 API Design

- **Always version your APIs** (`/v1/...`) for backward compatibility.
- **Separate read/write models** (CQRS) for heavy modules like catalog and orders if scaling further.
- **Modular services:** Decompose by business capability (catalog, inventory, orders), not by technical layer.

### 26.16.6 Security

- **Payment security:** Never store raw card data. Integrate with PCI-compliant providers; always encrypt sensitive fields at rest.
- **Use HTTPS everywhere.**
- **Store credentials/secrets** out of code.
- **PCI-DSS & GDPR compliance:** Offload payment handling; encrypt user/payment data.
- **Rate limiting and abuse detection** at the API gateway.

### 26.16.7 Operations

- **Monitoring & alerts:** Instrument services for latency, error rates, inventory anomalies, payment failures.
- **Graceful degradation:** If a service (e.g., recommendations) is down, the system should still allow core flows.
- **Automated tests:** Especially for inventory, checkout, payments — simulate race conditions and failures.
- **Use managed services:** Cloud-managed DBs, queues, storage to cut operational overhead.

### 26.16.8 Disaster Recovery

- **Plan for DR:** Regularly backup relational DBs and object storage.
- **Horizontal scalability:** Design all stateless services to scale out.

---

## 26.17 Conclusion

By breaking the e-commerce platform into modular, independently scalable services with clear API contracts, robust caching, and resilient async flows, you set the foundation for a system that can grow with your user base and business demands. The architecture above ensures **performance**, **consistency**, and **security** — all while keeping the system maintainable and developer-friendly.

With this modular, event-driven architecture, you can build a **robust, scalable, and fault-tolerant e-commerce marketplace.**

---

## 26.18 Further Reading

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [AWS Architecture Center: Microservices](https://aws.amazon.com/architecture/microservices/)
- [Elasticsearch Official Docs](https://www.elastic.co/guide/)
- [PostgreSQL Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [AWS SQS Queues](https://aws.amazon.com/sqs/)
- [Redis Caching Patterns](https://redis.io/docs/)

---

**Next Up:** [Chapter 27 — Design a Taxi Hailing App (Uber) →](./27%20-%20Design%20a%20Taxi%20Hailing%20App%20(aka%20Uber).md)
