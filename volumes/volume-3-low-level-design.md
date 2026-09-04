# Volume 3 — Low-Level Design

> Goal: Design clean, correct, maintainable components. Requires Volume 2.
>
> **Chapters 1–14.** Each chapter is one pattern or principle plus a production-quality implementation. By the end you will have built **30+ components** (each chapter's mini project + exercises).

# Contents

1. OOP Fundamentals
2. SOLID Principles
3. Design Principles (Cohesion, Coupling, YAGNI, DRY, KISS)
4. UML & Diagramming
5. GoF Creational Patterns
6. GoF Structural Patterns
7. GoF Behavioral Patterns
8. Clean Architecture
9. Hexagonal Architecture (Ports & Adapters)
10. Domain-Driven Design (Tactical)
11. Repository Pattern & Data Mapping
12. Event Bus, CQRS & Event Sourcing
13. Concurrency Patterns & Thread Safety
14. Resilience Patterns (Idempotency, Retries, Backoff, Circuit Breakers)

---

## Chapter 1 — OOP Fundamentals

**Concept:** Encapsulation, inheritance, composition, polymorphism; objects as data + behavior with invariants.

**Prereqs:** Vol 1 Ch 14.

**Diagram:** A class diagram with fields/methods and an is-a vs has-a relationship.

**Example:** a `BankAccount` enforcing `balance >= 0` via methods, not public fields.

**Exercises:** (1) Refactor inheritance to composition. (2) Design a class where no invalid state is representable.

**Mini project:** A `BankAccount`/`Transaction` domain model with enforced invariants.

**Open source:** [`python/cpython`](https://github.com/python/cpython) classes; [`rust-lang/rust`](https://github.com/rust-lang/rust) (structs + traits as OOP).

**Interview:** "Composition vs inheritance?" / "What is encapsulation really for?"

**Checklist:** ☐ hide fields behind methods ☐ make invalid states unrepresentable ☐ prefer composition

---

## Chapter 2 — SOLID Principles

**Concept:** Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion — with violations and fixes.

**Prereqs:** Ch 1.

**Diagram:** A before/after of each principle on a small class set.

**Example:** splitting a god-class (SRP); adding a strategy instead of editing a switch (OCP).

**Exercises:** (1) Find and fix an LSP violation. (2) Apply DIP to decouple a high-level module from a low-level one.

**Mini project:** Refactor a small codebase until all five principles hold and explain each fix.

**Open source:** [`spring-projects/spring-framework`](https://github.com/spring-projects/spring-framework) (DIP/DI in practice).

**Interview:** "Explain each SOLID letter with an example." / "What's a real LSP violation?"

**Checklist:** ☐ one reason to change per class ☐ extend without modifying ☐ depend on abstractions

---

## Chapter 3 — Design Principles (Cohesion, Coupling, YAGNI, DRY, KISS)

**Concept:** Cohesion vs coupling; YAGNI/DRY/KISS as heuristics, and when they conflict.

**Prereqs:** Ch 2.

**Diagram:** A cohesion/coupling matrix with a high-cohesion, low-coupling target zone.

**Example:** removing a duplicated snippet (DRY) that actually increased coupling — and undoing it.

**Exercises:** (1) Measure coupling of two modules and reduce it. (2) Find a premature abstraction (YAGNI violation) and remove it.

**Mini project:** Refactor a tangled module into high-cohesion, low-coupling components.

**Open source:** [`rust-lang/rust`](https://github.com/rust-lang/rust) (module boundaries); [`golang/go`](https://github.com/golang/go) (packages).

**Interview:** "DRY vs coupling — when does DRY hurt?" / "What's cohesion?"

**Checklist:** ☐ keep related things together ☐ reduce cross-module fan-in/fan-out ☐ say no to speculative generality

---

## Chapter 4 — UML & Diagramming

**Concept:** Class, sequence, and component diagrams; reading and writing the diagrams that communicate design.

**Prereqs:** Ch 1.

**Diagram:** (this chapter *is* the diagram) — class + sequence + component examples.

**Example:** a sequence diagram of a request through controller → service → repo.

**Exercises:** (1) Draw a class diagram for a small domain. (2) Draw a sequence diagram for a login flow.

**Mini project:** Document a real component with class + sequence diagrams (Mermaid).

**Open source:** [`mermaid-js/mermaid`](https://github.com/mermaid-js/mermaid).

**Interview:** "Class vs sequence diagram — what does each show?" / "When is a diagram worth maintaining?"

**Checklist:** ☐ draw readable class diagrams ☐ show message flow in sequence diagrams ☐ keep diagrams at the right altitude

---

## Chapter 5 — GoF Creational Patterns

**Concept:** Factory Method, Abstract Factory, Builder, Singleton, Prototype — intent, structure, and when to reach for each.

**Prereqs:** Ch 1.

**Diagram:** A UML per pattern with participants labeled.

**Example:** a `Builder` for a config object with defaults; a `Factory` producing parsers by format.

**Exercises:** (1) Implement a builder for a complex object. (2) Replace a `new` scattered across callers with a factory.

**Mini project:** A config/request builder library used across multiple handlers.

**Open source:** [`spring-projects/spring-framework`](https://github.com/spring-projects/spring-framework) (factories); [`rust-lang/rust`](https://github.com/rust-lang/rust) builder crates.

**Interview:** "Builder vs Factory?" / "Why is Singleton controversial?"

**Checklist:** ☐ know each pattern's intent ☐ use a factory at a real seam ☐ avoid over-applying patterns

---

## Chapter 6 — GoF Structural Patterns

**Concept:** Adapter, Decorator, Facade, Proxy, Bridge, Composite, Flyweight.

**Prereqs:** Ch 5.

**Diagram:** UML for adapter (wraps interface) vs decorator (adds behavior) vs facade (simplifies).

**Example:** an adapter wrapping a third-party SDK; a decorator adding caching.

**Exercises:** (1) Adapter a mismatched interface without changing its callers. (2) Add a logging decorator to a service.

**Mini project:** A facade over a messy subsystem + a caching decorator.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `functools.wraps` (decorators); [`rust-lang/rust`](https://github.com/rust-lang/rust) adapter traits.

**Interview:** "Adapter vs Facade?" / "Decorator vs inheritance for adding behavior?"

**Checklist:** ☐ wrap, don't fork, third-party APIs ☐ add behavior without editing the target ☐ hide complexity behind a facade

---

## Chapter 7 — GoF Behavioral Patterns

**Concept:** Strategy, Observer, Command, State, Template Method, Chain of Responsibility, Mediator, Memento, Visitor.

**Prereqs:** Ch 6.

**Diagram:** UML for strategy (interchangeable algorithms) and observer (publish/subscribe).

**Example:** a `Strategy` for pricing rules; an `Observer` notifying on state change.

**Exercises:** (1) Implement strategy for a sorting option. (2) Build an observer that decouples producer and consumers.

**Mini project:** An event notification system (observer) with pluggable strategies.

**Open source:** [`ReactiveX/RxPY`](https://github.com/ReactiveX/RxPY); [`rust-lang/rust`](https://github.com/rust-lang/rust) (command/state in GUIs).

**Interview:** "Strategy vs State?" / "Observer vs pub/sub?"

**Checklist:** ☐ swap behavior via strategy ☐ decouple with observer ☐ know when each behavioral pattern earns its keep

---

## Chapter 8 — Clean Architecture

**Concept:** Entities → use cases → interface adapters → frameworks; the dependency rule pointing inward.

**Prereqs:** Ch 2.

**Diagram:** The concentric-circles diagram with dependencies pointing inward only.

**Example:** a use case that depends on a port (interface), with a DB adapter implementing it.

**Exercises:** (1) Invert a dependency so the domain no longer imports the framework. (2) Swap a SQL adapter for an in-memory one.

**Mini project:** A service with a pure domain layer and swappable DB/HTTP adapters.

**Open source:** [`ivanpaulovich/clean-architecture-manga`](https://github.com/ivanpaulovich/clean-architecture-manga).

**Interview:** "What is the dependency rule?" / "Why isolate the domain from frameworks?"

**Checklist:** ☐ domain has zero framework imports ☐ depend on ports, not adapters ☐ test the domain in isolation

---

## Chapter 9 — Hexagonal Architecture (Ports & Adapters)

**Concept:** Ports (the contract) and adapters (the implementations) around a core; driving vs driven sides.

**Prereqs:** Ch 8.

**Diagram:** A hexagon with driving adapters on the left, driven adapters on the right.

**Example:** a `PaymentGateway` port with a Stripe adapter and a fake test adapter.

**Exercises:** (1) Define a port and two adapters. (2) Test the core with a fake adapter, no network.

**Mini project:** A payments component with a real and fake gateway adapter.

**Open source:** [`thombergs/buckpal`](https://github.com/thombergs/buckpal) (Spring hexagonal example).

**Interview:** "Ports & adapters vs clean architecture?" / "How does hexagonal help testing?"

**Checklist:** ☐ define explicit ports ☐ implement adapters outside the core ☐ swap adapters without touching the core

---

## Chapter 10 — Domain-Driven Design (Tactical)

**Concept:** Entities, value objects, aggregates, repositories, domain events, ubiquitous language; bounded contexts (intro).

**Prereqs:** Ch 8.

**Diagram:** An aggregate with a root, entities, and value objects; a bounded-context map.

**Example:** an `Order` aggregate enforcing its own invariants; a `Money` value object.

**Exercises:** (1) Model a domain as aggregates with invariants. (2) Publish a domain event on a state change.

**Mini project:** An order-management domain with aggregates, value objects, and a repository.

**Open source:** [`AxonFramework/AxonFramework`](https://github.com/AxonFramework/AxonFramework); [`dotnet-architecture/eShopOnContainers`](https://github.com/dotnet-architecture/eShopOnContainers).

**Interview:** "Entity vs value object?" / "What's an aggregate root's job?"

**Checklist:** ☐ keep invariants inside the aggregate ☐ use value objects for domain types ☐ name things in domain language

---

## Chapter 11 — Repository Pattern & Data Mapping

**Concept:** A collection-like abstraction over persistence; mapping domain objects to storage; unit of work.

**Prereqs:** Ch 10.

**Diagram:** A repository interface between the domain and the data mapper/ORM.

**Example:** `repo.save(aggregate)` / `repo.find(id)` with an ORM adapter behind it.

**Exercises:** (1) Implement a repository over SQL and over in-memory. (2) Add a unit-of-work for a multi-write transaction.

**Mini project:** A repository + unit-of-work for a small aggregate, testable against SQL and in-memory.

**Open source:** [`sqlalchemy/sqlalchemy`](https://github.com/sqlalchemy/sqlalchemy) (data mapper).

**Interview:** "Repository vs DAO?" / "Why keep persistence out of the domain?"

**Checklist:** ☐ domain stays persistence-agnostic ☐ one repository per aggregate ☐ wrap multi-writes in a unit of work

---

## Chapter 12 — Event Bus, CQRS & Event Sourcing

**Concept:** In-process event bus; command/query separation; storing events as the source of truth and projecting state.

**Prereqs:** Ch 10, Ch 11.

**Diagram:** A CQRS flow (command → write model → events → projections → read model).

**Example:** an in-process event bus dispatching `OrderPlaced`; a projection rebuilding a read model.

**Exercises:** (1) Implement an in-process event bus. (2) Split a read/write model and build a projection.

**Mini project:** An event-sourced counter/aggregate with replay and a CQRS read model.

**Open source:** [`microsoft/orleans`](https://github.com/microsoft/orleans); [`EventStore/EventStore`](https://github.com/EventStore/EventStore).

**Interview:** "CQRS — when is it worth it?" / "How does event sourcing enable replay?"

**Checklist:** ☐ decouple via events ☐ separate read/write models when needed ☐ rebuild state by replaying events

---

## Chapter 13 — Concurrency Patterns & Thread Safety

**Concept:** Mutexes, channels, worker pools, actor model, lock-free patterns, and eliminating races.

**Prereqs:** Vol 1 Ch 13, Ch 38.

**Diagram:** A worker-pool (queue → N workers) and an actor mailbox diagram.

**Example:** a mutex-protected counter; a channel-based worker pool; an actor with a mailbox.

**Exercises:** (1) Implement a thread-safe worker pool. (2) Fix a data race with a channel instead of shared state.

**Mini project:** A concurrent task executor with a bounded worker pool and per-task results.

**Open source:** [`tokio-rs/tokio`](https://github.com/tokio-rs/tokio); [`python/cpython`](https://github.com/python/cpython) `concurrent.futures`.

**Interview:** "Shared state vs message passing?" / "How do you make a class thread-safe?"

**Checklist:** ☐ prefer channels over shared state ☐ bound concurrency ☐ document thread-safety contracts

---

## Chapter 14 — Resilience Patterns (Idempotency, Retries, Backoff, Circuit Breakers)

**Concept:** Making components survive failure — idempotency keys, retry with exponential backoff + jitter, and circuit breakers.

**Prereqs:** Ch 13.

**Diagram:** A circuit breaker state machine (closed → open → half-open).

**Example:** a retry with exponential backoff and jitter; a circuit breaker that trips after N failures.

**Exercises:** (1) Add idempotency to a payment endpoint. (2) Implement a circuit breaker with half-open probing.

**Mini project:** A resilient HTTP client with retries, backoff, and a circuit breaker.

**Open source:** [`resilience4j/resilience4j`](https://github.com/resilience4j/resilience4j); [`ihrwein/backoff`](https://github.com/ihrwein/backoff).

**Interview:** "Why jitter in backoff?" / "How does a circuit breaker recover?"

**Checklist:** ☐ idempotent writes ☐ back off with jitter ☐ fail fast with a breaker when downstream is down

---

**Exit criteria:** Implement **30+ production-quality components** (one or more per chapter across mini projects and exercises).
