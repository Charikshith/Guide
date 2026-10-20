# Chapter 2 — Sets, Relations & Functions

> **Volume 0 — Math & Mental Models** · [Contents](index.md) · ← [Chapter 1 — Logic & Boolean Algebra](ch01-logic-and-boolean-algebra.md) · Next → [Chapter 3 — Combinatorics & Counting](ch03-combinatorics-and-counting.md)

---

## Concept

Sets, subsets, unions/intersections/differences, Cartesian products; relations (reflexive/symmetric/transitive); functions (injective/surjective/bijective).

**In one sentence:** a set is a bag of unique things, a relation is a list of pairs saying "these two are connected", and a function is a relation where every input gets exactly one output.

**Mental model — guest lists.** Two parties each have a guest list (sets). People on *both* lists are the intersection. Everyone invited *anywhere* is the union. "Who knows whom" is a relation. "Which seat each guest gets" is a function — every guest gets one seat.

**Set operations**

| Operation | Symbol | Python | Meaning |
|-----------|--------|--------|---------|
| Union | `A ∪ B` | `a \| b` | in A or B |
| Intersection | `A ∩ B` | `a & b` | in both |
| Difference | `A − B` | `a - b` | in A, not in B |
| Symmetric difference | `A △ B` | `a ^ b` | in exactly one |
| Subset | `A ⊆ B` | `a <= b` | every element of A is in B |
| Cartesian product | `A × B` | `itertools.product(a, b)` | all ordered pairs `(x, y)` |
| Cardinality | `\|A\|` | `len(a)` | how many elements |

**Relation properties** (a relation `R` on a set `S` is a set of pairs from `S × S`)

| Property | Rule | Example that has it |
|----------|------|---------------------|
| Reflexive | every `x R x` | `≤`, "same birthday as" |
| Symmetric | `x R y ⇒ y R x` | "is sibling of", "=" |
| Antisymmetric | `x R y ∧ y R x ⇒ x = y` | `≤`, "divides" (on positives) |
| Transitive | `x R y ∧ y R z ⇒ x R z` | `<`, "is ancestor of" |

* **Equivalence relation** = reflexive + symmetric + transitive. It splits a set into groups (equivalence classes). Example: "same remainder mod 3".
* **Partial order** = reflexive + antisymmetric + transitive. Example: `⊆` on sets, task dependencies.

**Function types** — `f: A → B`

| Type | Rule | Picture |
|------|------|---------|
| Injective (one-to-one) | different inputs → different outputs | no two arrows land on the same target |
| Surjective (onto) | every target is hit | no target left empty |
| Bijective | both | perfect pairing; has an inverse |

---

## Prereqs

* [Chapter 1 — Logic & Boolean Algebra](ch01-logic-and-boolean-algebra.md)

---

## Diagram

**Two overlapping sets**

```venn
title: Two overlapping sets
sets: A | B
name A: A = {1, 2, 3, 4}
name B: B = {3, 4, 5}
label A: 1
2
label A&B: 3
4
label B: 5
note: A − B = {1, 2} · A ∩ B = {3, 4} · B − A = {5} · A ∪ B = {1, 2, 3, 4, 5}
```

**Arrow diagrams of functions**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 270" role="img" aria-label="Three mappings from A to B: injective but not surjective, surjective but not injective, and bijective" style="width:100%;max-width:780px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="110" y="24" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">Injective, not surjective</text><text x="50" y="52" font-size="13" text-anchor="middle" fill="var(--text-muted)" font-weight="600">A</text><text x="180" y="52" font-size="13" text-anchor="middle" fill="var(--text-muted)" font-weight="600">B</text><circle cx="50" cy="80" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="50" y="85" font-size="13" text-anchor="middle" fill="var(--text)">1</text><circle cx="50" cy="120" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="50" y="125" font-size="13" text-anchor="middle" fill="var(--text)">2</text><circle cx="50" cy="160" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="50" y="165" font-size="13" text-anchor="middle" fill="var(--text)">3</text><circle cx="180" cy="80" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="180" y="85" font-size="13" text-anchor="middle" fill="var(--text)">a</text><circle cx="180" cy="120" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="180" y="125" font-size="13" text-anchor="middle" fill="var(--text)">b</text><circle cx="180" cy="160" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="180" y="165" font-size="13" text-anchor="middle" fill="var(--text)">c</text><circle cx="180" cy="200" r="16" fill=".2" fill-opacity="0.2" stroke="var(--danger)" stroke-width="1.6"/><text x="180" y="205" font-size="13" text-anchor="middle" fill="var(--text)">d</text><line x1="67" y1="80" x2="162" y2="80" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="67" y1="120" x2="162" y2="120" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="67" y1="160" x2="162" y2="160" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><text x="110" y="248" font-size="12" text-anchor="middle" fill="var(--text-muted)">d is never hit</text><text x="370" y="24" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">Surjective, not injective</text><text x="310" y="52" font-size="13" text-anchor="middle" fill="var(--text-muted)" font-weight="600">A</text><text x="440" y="52" font-size="13" text-anchor="middle" fill="var(--text-muted)" font-weight="600">B</text><circle cx="310" cy="80" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="310" y="85" font-size="13" text-anchor="middle" fill="var(--text)">1</text><circle cx="310" cy="120" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="310" y="125" font-size="13" text-anchor="middle" fill="var(--text)">2</text><circle cx="310" cy="160" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="310" y="165" font-size="13" text-anchor="middle" fill="var(--text)">3</text><circle cx="440" cy="80" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="440" y="85" font-size="13" text-anchor="middle" fill="var(--text)">a</text><circle cx="440" cy="120" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="440" y="125" font-size="13" text-anchor="middle" fill="var(--text)">b</text><line x1="327" y1="80" x2="422" y2="80" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="327" y1="120" x2="422" y2="80" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="327" y1="160" x2="422" y2="120" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><text x="370" y="168" font-size="12" text-anchor="middle" fill="var(--text-muted)">a is shared by 1 and 2</text><text x="630" y="24" font-size="14" text-anchor="middle" fill="var(--text)" font-weight="700">Bijective</text><text x="570" y="52" font-size="13" text-anchor="middle" fill="var(--text-muted)" font-weight="600">A</text><text x="700" y="52" font-size="13" text-anchor="middle" fill="var(--text-muted)" font-weight="600">B</text><circle cx="570" cy="80" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="570" y="85" font-size="13" text-anchor="middle" fill="var(--text)">1</text><circle cx="570" cy="120" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="570" y="125" font-size="13" text-anchor="middle" fill="var(--text)">2</text><circle cx="570" cy="160" r="16" fill=".2" fill-opacity="0.2" stroke="var(--primary)" stroke-width="1.6"/><text x="570" y="165" font-size="13" text-anchor="middle" fill="var(--text)">3</text><circle cx="700" cy="80" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="700" y="85" font-size="13" text-anchor="middle" fill="var(--text)">a</text><circle cx="700" cy="120" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="700" y="125" font-size="13" text-anchor="middle" fill="var(--text)">b</text><circle cx="700" cy="160" r="16" fill=".2" fill-opacity="0.2" stroke="var(--success)" stroke-width="1.6"/><text x="700" y="165" font-size="13" text-anchor="middle" fill="var(--text)">c</text><line x1="587" y1="80" x2="682" y2="80" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="587" y1="120" x2="682" y2="120" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="587" y1="160" x2="682" y2="160" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><text x="630" y="208" font-size="12" text-anchor="middle" fill="var(--text-muted)">every element used exactly once</text></svg>
</div>

**Is it a function? A decision flow**

```mermaid
flowchart TD
    R[Relation from A to B] --> Q1{Every input in A<br/>has an output?}
    Q1 -- no --> N[Not a function]
    Q1 -- yes --> Q2{Any input with<br/>two outputs?}
    Q2 -- yes --> N
    Q2 -- no --> F[Function]
    F --> I{Outputs all distinct?}
    I -- yes --> INJ[Injective]
    F --> S{Every B element hit?}
    S -- yes --> SUR[Surjective]
    INJ & SUR --> BIJ[Both → Bijective]
```

---

## Example

```python
print(set("mississippi"))            # {'m', 'i', 's', 'p'} — duplicates vanish

a, b = {1, 2, 3, 4}, {3, 4, 5}
print(a | b, a & b, a - b, a ^ b)    # {1,2,3,4,5} {3,4} {1,2} {1,2,5}

# Inclusion–exclusion, checked
assert len(a | b) == len(a) + len(b) - len(a & b)

# A bijection: each key maps to one value, each value comes from one key
code = {"red": 1, "green": 2, "blue": 3}
inverse = {v: k for k, v in code.items()}
assert len(inverse) == len(code)     # no collisions → injective, so invertible
```

**Checking relation properties by brute force**

```python
S = range(1, 7)
divides = {(x, y) for x in S for y in S if y % x == 0}

reflexive  = all((x, x) in divides for x in S)
symmetric  = all((y, x) in divides for (x, y) in divides)
transitive = all((x, z) in divides
                 for (x, y) in divides for (y2, z) in divides if y == y2)
print(reflexive, symmetric, transitive)   # True False True → a partial order
```

**Why sets give O(1) membership** — a `set` is a hash table. `x in s` hashes `x`, jumps to one bucket, and checks only what is there, instead of scanning every element like a `list` does.

```
 x in list:  [7, 3, 9, 1, 4, ...]  → check 1, 2, 3, ... n items    O(n)
 x in set:   hash(4) % 8 = 5  → bucket[5] → found                   O(1) average
```

---

## Exercises

1. Prove `|A ∪ B| = |A| + |B| − |A ∩ B|`.

   <details><summary>Solution</summary>

   Split `A ∪ B` into three disjoint parts: `A − B`, `A ∩ B`, `B − A`. Then `|A| = |A − B| + |A ∩ B|` and `|B| = |B − A| + |A ∩ B|`. Adding gives `|A| + |B| = |A ∪ B| + |A ∩ B|`, because the overlap is counted twice. Rearrange.
   </details>

2. Which relation properties does "divides" have on integers?

   <details><summary>Solution</summary>

   On positive integers: reflexive (`x | x`), antisymmetric (`x | y` and `y | x` ⇒ `x = y`), transitive. Not symmetric (`2 | 4` but `4 ∤ 2`). So it is a partial order. On all integers antisymmetry fails, since `2 | −2` and `−2 | 2`.
   </details>

3. Is `f(x) = x²` from integers to integers injective? Surjective? What if the domain is non-negative integers?

   <details><summary>Solution</summary>On all integers: not injective (`f(2) = f(−2)`), not surjective (3 is never hit). On non-negative integers: injective, still not surjective.</details>

---

## Mini project

**A set-operations calculator with a visualization of two overlapping sets.**

```mermaid
flowchart LR
    IN["input: A = 1,2,3,4 / B = 3,4,5"] --> P[Parse into sets] --> OPS["compute ∪ ∩ − △ ⊆"] --> V[Draw Venn regions]
    OPS --> T[Print table]
```

**Steps**

1. Read two comma-separated lists from the user.
2. Compute union, intersection, both differences, symmetric difference, and subset checks.
3. Draw a text Venn diagram that places each element in its region (only A, both, only B).
4. Bonus: use `matplotlib_venn` to draw real circles.

**Done when:** for any two inputs, the counts in each Venn region add up to `|A ∪ B|`.

---

## Open source

* [`python/cpython`](https://github.com/python/cpython) — Python's built-in `set`/`frozenset`. Read `Objects/setobject.c`: look at `set_add_entry` for hashing and probing, and `set_intersection` for how it loops over the *smaller* set.

---

## Interview

1. **"What's the difference between a function and a relation?"**
   <details><summary>Answer</summary>A relation is any set of pairs. A function is a relation where every input appears exactly once as the first element of a pair. So every function is a relation, but not every relation is a function.</details>

2. **"Give an example of a relation that's symmetric but not transitive."**
   <details><summary>Answer</summary>"Is a friend of": Alice–Bob and Bob–Carol are friends, but Alice and Carol may not be. Another: "differs by exactly 1" on integers, since 1~2 and 2~3 but not 1~3.</details>

---

## Checklist

- [ ] state the inclusion-exclusion principle
- [ ] classify a relation's properties
- [ ] explain why hash sets give O(1) membership

---

> [Contents](index.md) · ← [Chapter 1 — Logic & Boolean Algebra](ch01-logic-and-boolean-algebra.md) · Next → [Chapter 3 — Combinatorics & Counting](ch03-combinatorics-and-counting.md)
