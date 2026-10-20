# Chapter 4 — Built-in Data Structures

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 3 — Functions, Parameters, Return Values, Scope & Namespaces](ch03-functions-parameters-return-values-scope-and-namespaces.md) · Next → [Chapter 5 — Modules, Packages, Imports & Dependency Management](ch05-modules-packages-imports-and-dependency-management.md)

---

## Concept

Arrays, lists, tuples, dictionaries/hashmaps, sets, queues, stacks — operations and time complexity for each.

**In one sentence:** each data structure is a trade-off between how fast you can find, add, and remove things, and choosing the right one is often the whole optimization.

**Mental model — storage in a house.**

* **Array/list** — a row of numbered lockers. Jump to locker 57 at once; inserting in the middle means shifting everyone.
* **Tuple** — a sealed, labeled box. You can read it, not change it.
* **Dict/hashmap** — a coat check. Hand over a ticket (key), get your coat (value) at once.
* **Set** — a guest list. Only "is this person on it?" matters.
* **Stack** — a pile of plates. Last on, first off (LIFO).
* **Queue** — a line at a shop. First in, first out (FIFO).

**Big-O cheat sheet (Python, average case)**

| Structure | Index `x[i]` | Search `in` | Append / push | Insert at front | Delete by key | Ordered? |
|-----------|:-:|:-:|:-:|:-:|:-:|:-:|
| `list` (dynamic array) | O(1) | O(n) | O(1)* | O(n) | O(n) | yes |
| `tuple` | O(1) | O(n) | — immutable | — | — | yes |
| `dict` | — | O(1) key | O(1) | — | O(1) | insertion order (3.7+) |
| `set` | — | O(1) | O(1) | — | O(1) | no |
| `collections.deque` | O(n) middle | O(n) | O(1) both ends | O(1) | O(n) | yes |
| `heapq` on a list | — | O(n) | O(log n) | — | O(log n) min | heap order |

\* amortized — see [Vol 0 Ch 7](../volume-0-math/ch07-time-space-complexity-and-amortized-analysis.md).

**Which one should I use?**

| Need | Use |
|------|-----|
| ordered items, access by position | `list` |
| fixed record, dict key, return several values | `tuple` |
| look up by key | `dict` |
| uniqueness, fast membership | `set` |
| undo history, DFS, matching brackets | stack (`list`) |
| BFS, job line, buffering | queue (`deque`) |
| "always give me the smallest/most urgent" | priority queue (`heapq`) |
| count things | `collections.Counter` |

---

## Prereqs

* [Chapter 1 — Variables, Data Types & Operators](ch01-variables-data-types-and-operators.md)

---

## Diagram

**A hashmap with buckets and chaining**

| Key | hash(key) | hash % 8 | |
|---|---|---|---|
| `"apple"` | 9_817_223 | 7 | |
| `"grape"` | 4_441_017 | 1 | |
| `"melon"` | 2_003_191 | 7 | **collision** with "apple" |

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 290" role="img" aria-label="A hash table with eight buckets: grape in bucket 1, apple and melon chained in bucket 7" style="width:100%;max-width:700px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="60" y="24" font-size="13" text-anchor="start" fill="var(--text-muted)" font-weight="600">buckets</text><rect x="60" y="36" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="54" font-size="12.5" text-anchor="middle" fill="var(--text)">[0]</text><rect x="60" y="66" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="84" font-size="12.5" text-anchor="middle" fill="var(--text)">[1]</text><rect x="60" y="96" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="114" font-size="12.5" text-anchor="middle" fill="var(--text)">[2]</text><rect x="60" y="126" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="144" font-size="12.5" text-anchor="middle" fill="var(--text)">[3]</text><rect x="60" y="156" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="174" font-size="12.5" text-anchor="middle" fill="var(--text)">[4]</text><rect x="60" y="186" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="204" font-size="12.5" text-anchor="middle" fill="var(--text)">[5]</text><rect x="60" y="216" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="234" font-size="12.5" text-anchor="middle" fill="var(--text)">[6]</text><rect x="60" y="246" width="50" height="26" rx="3" fill="var(--border)" fill-opacity=".3" stroke="var(--border)" stroke-width="1.6"/><text x="85" y="264" font-size="12.5" text-anchor="middle" fill="var(--text)">[7]</text><text x="130" y="54" font-size="14" text-anchor="start" fill="var(--text-muted)">∅</text><text x="130" y="114" font-size="14" text-anchor="start" fill="var(--text-muted)">∅</text><text x="130" y="144" font-size="14" text-anchor="start" fill="var(--text-muted)">∅</text><text x="130" y="174" font-size="14" text-anchor="start" fill="var(--text-muted)">∅</text><text x="130" y="204" font-size="14" text-anchor="start" fill="var(--text-muted)">∅</text><text x="130" y="234" font-size="14" text-anchor="start" fill="var(--text-muted)">∅</text><line x1="110" y1="79" x2="140" y2="79" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><rect x="142" y="66" width="130" height="26" rx="4" fill="var(--success)" fill-opacity=".2" stroke="var(--success)" stroke-width="1.6"/><text x="207" y="84" font-size="12.5" text-anchor="middle" fill="var(--text)">("grape", 3)</text><line x1="110" y1="259" x2="140" y2="259" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><rect x="142" y="246" width="130" height="26" rx="4" fill="var(--primary)" fill-opacity=".2" stroke="var(--primary)" stroke-width="1.6"/><text x="207" y="264" font-size="12.5" text-anchor="middle" fill="var(--text)">("apple", 5)</text><line x1="272" y1="259" x2="300" y2="259" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><rect x="302" y="246" width="130" height="26" rx="4" fill="var(--danger)" fill-opacity=".2" stroke="var(--danger)" stroke-width="1.6"/><text x="367" y="264" font-size="12.5" text-anchor="middle" fill="var(--text)">("melon", 2)</text><text x="448" y="264" font-size="12.5" text-anchor="start" fill="var(--text-muted)">chain: compare keys one by one</text></svg>
</div>

When the table gets too full (load factor above ~⅔), it doubles and every key is re-placed. Python actually uses *open addressing* (probe the next slot) rather than chains, but the idea is the same.

**Stack (LIFO) vs queue (FIFO)**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 280" role="img" aria-label="A stack pushes and pops at the top; a queue enqueues at the back and dequeues from the front" style="width:100%;max-width:700px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="120" y="26" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">STACK</text><text x="120" y="46" font-size="12.5" text-anchor="middle" fill="var(--text-muted)">push 1, push 2, push 3</text><rect x="80" y="64" width="80" height="44" rx="4" fill="var(--primary)" fill-opacity=".18" stroke="var(--primary)" stroke-width="1.6"/><text x="120" y="92" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">3</text><rect x="80" y="108" width="80" height="44" rx="4" fill="var(--primary)" fill-opacity=".18" stroke="var(--primary)" stroke-width="1.6"/><text x="120" y="136" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">2</text><rect x="80" y="152" width="80" height="44" rx="4" fill="var(--primary)" fill-opacity=".18" stroke="var(--primary)" stroke-width="1.6"/><text x="120" y="180" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">1</text><line x1="170" y1="76" x2="170" y2="94" stroke="var(--accent)" stroke-width="1.6" marker-end="url(#ar)" marker-start="url(#ar)"/><text x="184" y="90" font-size="12.5" text-anchor="start" fill="var(--accent)" font-weight="600">push / pop</text><text x="184" y="108" font-size="12.5" text-anchor="start" fill="var(--text-muted)">pop → 3</text><text x="480" y="26" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">QUEUE</text><text x="480" y="46" font-size="12.5" text-anchor="middle" fill="var(--text-muted)">enqueue 1, 2, 3</text><rect x="400" y="96" width="60" height="44" rx="4" fill="var(--success)" fill-opacity=".18" stroke="var(--success)" stroke-width="1.6"/><text x="430" y="124" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">1</text><rect x="460" y="96" width="60" height="44" rx="4" fill="var(--success)" fill-opacity=".18" stroke="var(--success)" stroke-width="1.6"/><text x="490" y="124" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">2</text><rect x="520" y="96" width="60" height="44" rx="4" fill="var(--success)" fill-opacity=".18" stroke="var(--success)" stroke-width="1.6"/><text x="550" y="124" font-size="15" text-anchor="middle" fill="var(--text)" font-weight="700">3</text><line x1="340" y1="118" x2="396" y2="118" stroke="var(--accent)" stroke-width="1.6" marker-end="url(#ar)"/><text x="368" y="92" font-size="12.5" text-anchor="middle" fill="var(--accent)" font-weight="600">out</text><text x="368" y="156" font-size="12.5" text-anchor="middle" fill="var(--text-muted)">dequeue → 1</text><line x1="584" y1="118" x2="640" y2="118" stroke="var(--accent)" stroke-width="1.6" marker-start="url(#ar)"/><text x="612" y="92" font-size="12.5" text-anchor="middle" fill="var(--accent)" font-weight="600">in</text></svg>
</div>

**Why inserting at the front of a list is O(n)**

```
 insert(0, 'X') into [A, B, C, D]
   step 1: shift  [_, A, B, C, D]   ← every element moves right
   step 2: place  [X, A, B, C, D]
```

---

## Example

```python
from collections import deque, defaultdict, Counter
import heapq

d = {"a": 1}
d["a"] += 1                                  # hashmap update: O(1)
d.setdefault("b", 0)

stack = []
stack.append(1); stack.append(2)
print(stack.pop())                           # 2 — LIFO

q = deque()
q.append("job1"); q.append("job2")
print(q.popleft())                           # job1 — FIFO, O(1)
# list.pop(0) would also work, but it is O(n)

groups = defaultdict(list)
for word in ["apple", "avocado", "banana"]:
    groups[word[0]].append(word)
print(dict(groups))                          # {'a': ['apple', 'avocado'], 'b': ['banana']}

print(Counter("mississippi").most_common(2)) # [('i', 4), ('s', 4)]

tasks = []
heapq.heappush(tasks, (2, "write docs"))
heapq.heappush(tasks, (1, "fix prod bug"))
print(heapq.heappop(tasks))                  # (1, 'fix prod bug') — smallest first

point = (3, 4)                               # tuple: immutable, hashable
seen = {point}                               # can be a set member or dict key
```

---

## Exercises

1. Implement a stack using only a list.

   <details><summary>Solution</summary>

   ```python
   class Stack:
       def __init__(self): self._items = []
       def push(self, x): self._items.append(x)          # O(1) amortized
       def pop(self):
           if not self._items: raise IndexError("pop from empty stack")
           return self._items.pop()                      # O(1)
       def peek(self): return self._items[-1]
       def __len__(self): return len(self._items)
   ```
   Push and pop at the *end* of the list. The front would make them O(n).
   </details>

2. Explain when to use a tuple over a list.

   <details><summary>Solution</summary>Use a tuple for a fixed-size record whose fields mean different things (<code>(lat, lon)</code>), when you need a hashable value (dict key, set member), or to signal "this should not change". Use a list for a variable-length collection of similar items.</details>

3. Check whether a string of brackets like `"([]{})"` is balanced.

   <details><summary>Solution</summary>Push each opener on a stack. On a closer, pop and check it matches. The string is balanced if every pop matches and the stack is empty at the end. O(n).</details>

---

## Mini project

**A task scheduler using a priority queue and a simple FIFO queue.**

```mermaid
flowchart LR
    IN[New task] --> R{urgent?}
    R -- yes --> PQ["Priority queue (heapq)<br/>ordered by (priority, time)"]
    R -- no --> FQ["FIFO queue (deque)"]
    PQ --> W[Worker]
    FQ --> W
    W -->|"every 3rd pick comes from FIFO<br/>so normal tasks never starve"| W
```

**Steps**

1. `add(task, priority=None)`: urgent tasks go to a heap as `(priority, counter, task)`; the counter breaks ties in arrival order.
2. Normal tasks go to a `deque`.
3. `next()` usually takes from the heap, but every 3rd call takes from the FIFO queue to prevent starvation.
4. Add `peek`, `len`, and a simulation of 1,000 random tasks showing the wait-time distribution per queue.

**Done when:** urgent tasks always run first among urgent tasks, and no normal task waits forever.

---

## Open source

* [`python/cpython`](https://github.com/python/cpython) `collections` (`deque`, `defaultdict`) — `Modules/_collectionsmodule.c` shows `deque` as a doubly linked list of 64-item blocks, which is why both ends are O(1). `Objects/dictobject.c` has a long comment explaining Python's compact dict design.

---

## Interview

1. **"Array vs linked list — when is each better?"**
   <details><summary>Answer</summary>Arrays give O(1) indexing and are cache-friendly because elements are contiguous. Inserts in the middle are O(n). Linked lists give O(1) insert/delete at a known node but O(n) indexing and poor cache behavior. In practice, arrays win almost always; linked lists fit when you splice often and already hold node pointers (LRU caches, allocators).</details>

2. **"How does a hashmap achieve O(1) lookup?"**
   <details><summary>Answer</summary>It hashes the key to an integer and uses it (mod table size) as an array index, so it jumps straight to one slot. Collisions are handled by chaining or probing. Keeping the load factor bounded by resizing keeps the expected chain length constant. The worst case is O(n) if many keys collide.</details>

---

## Checklist

- [ ] know each structure's big-O
- [ ] pick the right structure for a task
- [ ] implement stack/queue by hand

---

> [Contents](index.md) · ← [Chapter 3 — Functions, Parameters, Return Values, Scope & Namespaces](ch03-functions-parameters-return-values-scope-and-namespaces.md) · Next → [Chapter 5 — Modules, Packages, Imports & Dependency Management](ch05-modules-packages-imports-and-dependency-management.md)
