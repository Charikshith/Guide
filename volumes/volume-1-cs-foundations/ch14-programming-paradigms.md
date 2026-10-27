# Chapter 14 — Programming Paradigms

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 13 — Concurrency: Threads, Processes, Async, Futures & Coroutines](ch13-concurrency-threads-processes-async-futures-and-coroutines.md) · Next → [Chapter 15 — Correctness Traps](ch15-correctness-traps.md)

---

## Concept

Imperative, declarative, object-oriented, functional, reactive, and event-driven styles — and recognizing them in real code.

**In one sentence:** a paradigm is a way of organizing a program — step-by-step instructions, descriptions of the result, objects sending messages, pure functions transforming data, or reactions to streams of events — and real codebases mix them.

### Mental model — getting a sandwich

* **Imperative:** "Take two slices. Spread butter. Add cheese. Close." (How.)
* **Declarative:** "One cheese sandwich, please." (What.)
* **Object-oriented:** ask the `Chef` object to `make(Sandwich)`; the chef hides how.
* **Functional:** `sandwich = close(add(cheese, spread(butter, bread)))` — no step changes an existing thing; each returns a new one.
* **Event-driven:** when the buzzer rings (event), pick up the sandwich (handler).
* **Reactive:** subscribe to a stream of orders and describe how every future order flows to the counter.

### The paradigms

| Paradigm | Core idea | You'll see | Languages / tools |
|----------|-----------|-----------|-------------------|
| Imperative | statements change state step by step | loops, assignments, mutation | C, Python, Go |
| Procedural | imperative, organized into procedures | functions over shared structs | C, Pascal |
| Declarative | describe the result, not the steps | queries, configs, markup | SQL, HTML, CSS, Terraform, regex |
| Object-oriented | bundle data + behavior; objects collaborate | classes, methods, interfaces, polymorphism | Java, C#, Python, Ruby |
| Functional | pure functions, immutable data, functions as values | `map`/`filter`/`reduce`, recursion, no mutation | Haskell, Elixir, Clojure, F#; functional style in JS/Python/Rust |
| Event-driven | control flow is driven by events | callbacks, handlers, listeners, message queues | JS in browsers, GUIs, Node.js |
| Reactive | compose asynchronous *streams* of values over time | observables, operators (`map`, `debounce`, `merge`) | RxJS, RxPY, Reactor, Kotlin Flow |

### Pure functions and immutability

The heart of functional style.

* A **pure function** returns the same output for the same input and has no side effects (no I/O, no mutation of outside state). Easy to test, cache, and parallelize.
* **Immutable data** can't be changed after creation. No one can modify it behind your back, so sharing it between threads is safe.
* Real programs need side effects. Functional style *pushes them to the edges*: a pure core, with a thin imperative shell doing I/O.

---

## Prereqs

* [Chapter 3 — Functions, Parameters, Return Values, Scope & Namespaces](ch03-functions-parameters-return-values-scope-and-namespaces.md)
* [Chapter 13 — Concurrency: Threads, Processes, Async, Futures & Coroutines](ch13-concurrency-threads-processes-async-futures-and-coroutines.md)

---

## Diagram

### A map of paradigms

```mermaid
flowchart LR
    P((Paradigms)) --> IMP[Imperative]
    P --> DEC[Declarative]
    P --> EVT[Event-driven]
    IMP --> PROC["Procedural<br/><code>for i in range(n): total += x[i]</code>"]
    IMP --> OO["Object-oriented<br/><code>cart.add(item); cart.checkout()</code>"]
    DEC --> FN["Functional<br/><code>sum(map(price, filter(in_stock, items)))</code>"]
    DEC --> Q["Query / config<br/><code>SELECT sum(price) FROM items WHERE in_stock</code>"]
    DEC --> RX["Reactive<br/><code>clicks.pipe(debounce(300), map(search))</code>"]
    EVT --> CB["Callbacks<br/><code>button.on('click', handler)</code>"]
```

### Same task, three styles: total price of in-stock items

```
 IMPERATIVE                  FUNCTIONAL                          DECLARATIVE (SQL)
 total = 0                   total = sum(                        SELECT SUM(price)
 for it in items:                i.price                         FROM items
     if it.in_stock:             for i in items                  WHERE in_stock;
         total += it.price       if i.in_stock)
   how, step by step           transform data, no mutation         what, not how
```

### Reactive stream: search-as-you-type

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 260" role="img" aria-label="Marble diagram: keystrokes are debounced into hello and world, mapped to searches; switchMap cancels the stale hello request" style="width:100%;max-width:760px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="20" y="45" font-size="12.5" text-anchor="start" fill="var(--text-muted)" font-weight="600">keystrokes</text><line x1="120" y1="40" x2="740" y2="40" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><circle cx="140" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="140" y="44" font-size="11" text-anchor="middle" fill="var(--text)">h</text><circle cx="164" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="164" y="44" font-size="11" text-anchor="middle" fill="var(--text)">e</text><circle cx="188" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="188" y="44" font-size="11" text-anchor="middle" fill="var(--text)">l</text><circle cx="212" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="212" y="44" font-size="11" text-anchor="middle" fill="var(--text)">l</text><circle cx="236" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="236" y="44" font-size="11" text-anchor="middle" fill="var(--text)">o</text><circle cx="430" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="430" y="44" font-size="11" text-anchor="middle" fill="var(--text)">w</text><circle cx="454" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="454" y="44" font-size="11" text-anchor="middle" fill="var(--text)">o</text><circle cx="478" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="478" y="44" font-size="11" text-anchor="middle" fill="var(--text)">r</text><circle cx="502" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="502" y="44" font-size="11" text-anchor="middle" fill="var(--text)">l</text><circle cx="526" cy="40" r="9" fill=".25" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="526" y="44" font-size="11" text-anchor="middle" fill="var(--text)">d</text><text x="20" y="105" font-size="12.5" text-anchor="start" fill="var(--text-muted)" font-weight="600">debounce(300)</text><line x1="120" y1="100" x2="740" y2="100" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><rect x="240" y="84" width="90" height="32" rx="8" fill="var(--primary)" fill-opacity=".14" stroke="var(--primary)" stroke-width="1.6"/><text x="285.0" y="104.2" font-size="12" text-anchor="middle" fill="var(--text)" font-weight="600">"hello"</text><rect x="540" y="84" width="90" height="32" rx="8" fill="var(--success)" fill-opacity=".14" stroke="var(--success)" stroke-width="1.6"/><text x="585.0" y="104.2" font-size="12" text-anchor="middle" fill="var(--text)" font-weight="600">"world"</text><text x="20" y="165" font-size="12.5" text-anchor="start" fill="var(--text-muted)" font-weight="600">map(search)</text><line x1="120" y1="160" x2="740" y2="160" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><rect x="270" y="144" width="110" height="32" rx="8" fill="var(--primary)" fill-opacity=".14" stroke="var(--primary)" stroke-width="1.6"/><text x="325.0" y="164.2" font-size="12" text-anchor="middle" fill="var(--text)" font-weight="600">[results…]</text><rect x="570" y="144" width="110" height="32" rx="8" fill="var(--success)" fill-opacity=".14" stroke="var(--success)" stroke-width="1.6"/><text x="625.0" y="164.2" font-size="12" text-anchor="middle" fill="var(--text)" font-weight="600">[results…]</text><line x1="285" y1="116" x2="285" y2="144" stroke="var(--text-muted)" stroke-width="1.6" stroke-dasharray="3 3" marker-end="url(#ar)"/><line x1="585" y1="116" x2="585" y2="144" stroke="var(--text-muted)" stroke-width="1.6" stroke-dasharray="3 3" marker-end="url(#ar)"/><text x="380" y="226" font-size="13" text-anchor="middle" fill="var(--danger)" font-weight="600">switchMap cancels the "hello" request if "world" arrives first</text></svg>
</div>

---

## Example

```python
from functools import reduce
from dataclasses import dataclass

@dataclass(frozen=True)                     # immutable object
class Item:
    name: str
    price: float
    in_stock: bool

items = [Item("pen", 2.0, True), Item("ink", 9.5, False), Item("pad", 4.0, True)]

# Imperative
total = 0.0
for it in items:
    if it.in_stock:
        total += it.price

# Functional: map / filter / reduce
total_fn = reduce(lambda acc, p: acc + p,
                  map(lambda i: i.price, filter(lambda i: i.in_stock, items)), 0.0)
assert total == total_fn == 6.0

# Object-oriented
class Cart:
    def __init__(self): self._items = []
    def add(self, item): self._items.append(item)
    def total(self): return sum(i.price for i in self._items if i.in_stock)

# Event-driven: register callbacks, fire events
handlers = {}
def on(event, fn): handlers.setdefault(event, []).append(fn)
def emit(event, payload):
    for fn in handlers.get(event, []): fn(payload)

on("order_placed", lambda o: print("email receipt for", o))
on("order_placed", lambda o: print("reserve stock for", o))
emit("order_placed", "order-42")
```

```python
# Reactive (RxPY): pip install reactivex
import reactivex as rx
from reactivex import operators as ops

rx.from_iterable([1, 2, 3, 4, 5, 6]).pipe(
    ops.filter(lambda x: x % 2 == 0),
    ops.map(lambda x: x * 10),
).subscribe(print)                          # 20 40 60
```

---

## Exercises

1. Rewrite an imperative loop as `map/filter/reduce`.

   ```python
   out = []
   for w in words:
       if len(w) > 3:
           out.append(w.upper())
   ```

   <details><summary>Solution</summary><code>out = list(map(str.upper, filter(lambda w: len(w) &gt; 3, words)))</code>, or more idiomatically <code>[w.upper() for w in words if len(w) &gt; 3]</code>.</details>

2. Model an event-driven system with callbacks.

   <details><summary>Solution</summary>See the <code>on</code>/<code>emit</code> example. Extend it: <code>off()</code> to unsubscribe, catch exceptions per handler so one failing listener doesn't break the rest, and async handlers.</details>

3. Is this function pure? `def add_tax(order): order.total *= 1.2; return order`

   <details><summary>Solution</summary>No. It mutates its input — a side effect visible to the caller. Pure version: <code>return replace(order, total=order.total * 1.2)</code>, which returns a new object.</details>

---

## Mini project

### A tiny reactive event bus with subscribe/publish and a functional pipeline

```mermaid
flowchart LR
    PUB["publish('orders', o)"] --> BUS["EventBus<br/>topic → subscribers"]
    BUS --> S1["subscriber: pipeline<br/>filter(big) → map(to_alert) → sink(print)"]
    BUS --> S2["subscriber: audit log"]
    S1 --> UN["unsubscribe() handle"]
```

### Steps

1. `EventBus.subscribe(topic, fn)` returns an unsubscribe function; `publish(topic, payload)` calls every subscriber.
2. A `Stream` class with chainable `map`, `filter`, `take(n)`, and `debounce(seconds)` that returns new streams (immutable pipeline objects).
3. Connect them: `bus.stream("orders").filter(lambda o: o.total > 100).map(to_alert).subscribe(print)`.
4. Isolate failures: one subscriber raising must not stop the others.
5. Write the pipeline operators as pure functions and test them without the bus.

**Done when:** you can build a 3-stage pipeline in one line, and every operator has a unit test with no mocks.

---

## Open source

* [`ReactiveX/RxPY`](https://github.com/ReactiveX/RxPY) — `reactivex/operators/` implements each operator as a function returning a function. It is functional composition in practice.
* [`python/cpython`](https://github.com/python/cpython) `itertools` — the docs' "Itertools Recipes" section is a masterclass in lazy functional pipelines.

---

## Interview

1. **"Declarative vs imperative?"**
   <details><summary>Answer</summary>Imperative code tells the computer <i>how</i>: explicit steps and state changes. Declarative code states <i>what</i> result you want and lets an engine decide how (SQL's query planner, React's DOM diffing, Terraform's plan). Declarative code is usually shorter and easier to optimize; imperative code gives precise control.</details>

2. **"What makes code 'functional'?"**
   <details><summary>Answer</summary>Functions are values (passed and returned), most functions are pure, data is immutable, and programs are built by composing transformations instead of mutating state. Side effects are isolated at the edges. You can write functional-style code in most languages.</details>

---

## Checklist

- [ ] write pure functions
- [ ] identify a paradigm in the wild
- [ ] explain immutability benefits

---

> [Contents](index.md) · ← [Chapter 13 — Concurrency: Threads, Processes, Async, Futures & Coroutines](ch13-concurrency-threads-processes-async-futures-and-coroutines.md) · Next → [Chapter 15 — Correctness Traps](ch15-correctness-traps.md)
