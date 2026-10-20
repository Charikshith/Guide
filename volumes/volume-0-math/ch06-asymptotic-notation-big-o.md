# Chapter 6 — Asymptotic Notation (Big-O, Θ, Ω)

> **Volume 0 — Math & Mental Models** · [Contents](index.md) · ← [Chapter 5 — Proof by Induction](ch05-proof-by-induction.md) · Next → [Chapter 7 — Time/Space Complexity & Amortized Analysis](ch07-time-space-complexity-and-amortized-analysis.md)

---

## Concept

Big-O (upper bound), Ω (lower bound), Θ (tight); growth classes (1, log n, n, n log n, n², 2ⁿ); worst vs average vs best case.

**In one sentence:** Big-O ignores constants and small inputs, and asks only *how fast the cost grows* as the input gets large.

**Mental model — travel time.** Walking, cycling, and driving differ by a constant factor. Walking to the next city versus walking around the world differs by the *distance*. Big-O is about distance (growth), not vehicle (constants).

**Formal definitions** (for positive functions, n ≥ n₀)

| Notation | Read as | Definition | Analogy |
|----------|---------|------------|---------|
| `f = O(g)` | "at most g" | ∃ c, n₀: `f(n) ≤ c·g(n)` for all n ≥ n₀ | `≤` |
| `f = Ω(g)` | "at least g" | ∃ c, n₀: `f(n) ≥ c·g(n)` for all n ≥ n₀ | `≥` |
| `f = Θ(g)` | "exactly g" | both O and Ω | `=` |
| `f = o(g)` | "strictly less" | `f/g → 0` | `<` |

The pair `(c, n₀)` is called a *witness*. To prove a bound, you produce one.

**Growth classes, slowest to fastest**

| Class | Name | Example | n = 10⁶ (ops) |
|-------|------|---------|--------------:|
| `O(1)` | constant | array index, hash lookup | 1 |
| `O(log n)` | logarithmic | binary search | 20 |
| `O(√n)` | root | trial-division prime check | 1,000 |
| `O(n)` | linear | one scan | 10⁶ |
| `O(n log n)` | linearithmic | merge sort | 2 × 10⁷ |
| `O(n²)` | quadratic | nested loops, bubble sort | 10¹² |
| `O(2ⁿ)` | exponential | all subsets | ∞ in practice |
| `O(n!)` | factorial | all orderings | ∞ in practice |

**Simplification rules**

* Drop constants: `5n → n`.
* Keep the dominant term: `n² + 100n + 7 → n²`.
* Log bases don't matter: `log₂ n = log₁₀ n / log₁₀ 2`, a constant factor.
* Sequential code adds: `O(f) + O(g) = O(max(f, g))`. Nested code multiplies: `O(f · g)`.

**Cases are not bounds.** "Worst case" / "average case" / "best case" pick *which input* you measure. O / Ω / Θ describe *how you bound* that measurement. Quicksort's *worst case* is `Θ(n²)`; its *average case* is `Θ(n log n)`.

---

## Prereqs

* [Chapter 3 — Combinatorics & Counting](ch03-combinatorics-and-counting.md)

---

## Diagram

**`f(n)` shaded under `c·g(n)` after `n₀`**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 330" role="img" aria-label="f(n) may be above c times g(n) before n0, but stays below it for every n after n0" style="width:100%;max-width:640px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><line x1="60" y1="270" x2="60" y2="20" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><line x1="60" y1="270" x2="600" y2="270" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#ar)"/><text x="45" y="28" font-size="13" text-anchor="end" fill="var(--text-muted)">cost</text><text x="600" y="292" font-size="13" text-anchor="end" fill="var(--text-muted)">n</text><line x1="60" y1="270" x2="580" y2="62" stroke="var(--primary)" stroke-width="2.4"/><text x="584" y="56" font-size="13" text-anchor="start" fill="var(--primary)" font-weight="700">c·g(n)</text><line x1="300" y1="40" x2="300" y2="270" stroke="var(--accent)" stroke-width="1.6" stroke-dasharray="5 4"/><text x="300" y="292" font-size="14" text-anchor="middle" fill="var(--accent)" font-weight="700">n₀</text><path d="M90,190 L125,155 L160,195 L200,150 L240,175 L270,130 L300,150 L345,205 L395,190 L440,205 L490,175 L540,185" stroke="var(--success)" stroke-width="1.4" fill="none" stroke-dasharray="3 3"/><circle cx="90" cy="190" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="125" cy="155" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="160" cy="195" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="200" cy="150" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="240" cy="175" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="270" cy="130" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="300" cy="150" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="345" cy="205" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="395" cy="190" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="440" cy="205" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="490" cy="175" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="540" cy="185" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><circle cx="430" cy="40" r="5" fill="var(--success)" fill-opacity="1" stroke="var(--success)" stroke-width="1.6"/><text x="442" y="45" font-size="13" text-anchor="start" fill="var(--text)">= f(n)</text><rect x="60" y="38" width="238" height="52" rx="6" fill="var(--danger)" fill-opacity=".10" stroke="var(--danger)" stroke-width="1.6"/><text x="70" y="58" font-size="12" text-anchor="start" fill="var(--text)">before n₀, f(n) may sit above c·g(n)</text><text x="70" y="76" font-size="12" text-anchor="start" fill="var(--text-muted)">Big-O does not care</text><text x="425" y="232" font-size="12" text-anchor="middle" fill="var(--success)" font-weight="600">after n₀, every point stays under the line</text></svg>
</div>

**Growth curves** (values at small n)

| n | log₂ n | n | n log₂ n | n² | 2ⁿ |
|--:|------:|--:|---------:|---:|---:|
| 1 | 0 | 1 | 0 | 1 | 2 |
| 8 | 3 | 8 | 24 | 64 | 256 |
| 16 | 4 | 16 | 64 | 256 | 65,536 |
| 32 | 5 | 32 | 160 | 1,024 | 4.3 × 10⁹ |
| 64 | 6 | 64 | 384 | 4,096 | 1.8 × 10¹⁹ |

```mermaid
xychart-beta
    title "Growth (n = 1..10)"
    x-axis [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y-axis "operations" 0 --> 110
    line [0, 1, 1.6, 2, 2.3, 2.6, 2.8, 3, 3.2, 3.3]
    line [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    line [0, 2, 4.8, 8, 11.6, 15.5, 19.7, 24, 28.5, 33.2]
    line [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

Lines from bottom to top: `log n`, `n`, `n log n`, `n²`.

---

## Example

```python
def contains(xs, target):          # O(n): one pass, O(1) work each
    for x in xs:
        if x == target:
            return True
    return False

def has_duplicate(xs):             # O(n²): every pair
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[i] == xs[j]:
                return True
    return False

def has_duplicate_fast(xs):        # O(n) expected: hash set
    seen = set()
    for x in xs:
        if x in seen:
            return True
        seen.add(x)
    return False

def binary_search(xs, target):     # O(log n): halves the range each step
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < len(xs) and xs[lo] == target
```

**Counting the nested loop exactly:** the inner body runs `(n−1) + (n−2) + … + 1 = n(n−1)/2` times, which is `Θ(n²)`.

---

## Exercises

1. Classify `3n² + 100n + 7` as Θ(n²) with witnesses c and n₀.

   <details><summary>Solution</summary>

   Upper: for n ≥ 1, `100n ≤ 100n²` and `7 ≤ 7n²`, so `f(n) ≤ 110n²`. Witness c = 110, n₀ = 1. Lower: `f(n) ≥ 3n²` for all n ≥ 1. Witness c = 3, n₀ = 1. Both hold, so Θ(n²).
   </details>

2. Order `log n, n log n, 2ⁿ, n², √n` by growth.

   <details><summary>Solution</summary><code>log n &lt; √n &lt; n log n &lt; n² &lt; 2ⁿ</code>.</details>

3. What is the complexity of this loop? `i = 1; while i < n: i *= 2`

   <details><summary>Solution</summary><code>Θ(log n)</code>: i takes values 1, 2, 4, …, so it reaches n after about log₂ n steps.</details>

---

## Mini project

**A tiny benchmark script that plots measured runtime vs n and fits the Big-O curve.**

```mermaid
flowchart LR
    F[Function under test] --> R["Run for n = 1k, 2k, 4k, …"] --> T[Record median time]
    T --> FIT["Fit to 1, log n, n, n log n, n²"] --> P["Plot + report best fit"]
```

**Steps**

1. Time a function with `timeit` for doubling n; keep the median of 5 runs.
2. For each candidate class g(n), fit `t ≈ c · g(n)` by least squares.
3. Report the class with the smallest error, and the *doubling ratio* `t(2n)/t(n)`: ≈1 → O(1), ≈2 → O(n), ≈4 → O(n²).
4. Plot with `matplotlib` on log-log axes; the slope is the exponent.

**Done when:** it correctly classifies `sorted`, `list.index`, `has_duplicate`, and `binary_search`.

---

## Open source

* [`sympy/sympy`](https://github.com/sympy/sympy) — `sympy.series.Order`. `O(3*x**2 + 100*x + 7, (x, oo))` simplifies to `O(x**2)`.

---

## Interview

1. **"What's the difference between O(n) and Ω(n)?"**
   <details><summary>Answer</summary>O(n) says the cost grows <i>no faster</i> than linearly (upper bound). Ω(n) says it grows <i>at least</i> linearly (lower bound). If both hold, it's Θ(n). Any algorithm that must read all input is Ω(n).</details>

2. **"Is O(log n) always faster than O(n)?"**
   <details><summary>Answer</summary>Only for large enough n. Big-O hides constants: 1000·log n is slower than n until n is about 14,000. Cache effects matter too — a linear scan over a small contiguous array can beat a tree search.</details>

---

## Checklist

- [ ] give formal c/n₀ witnesses
- [ ] rank common growth classes
- [ ] distinguish worst/average case

---

> [Contents](index.md) · ← [Chapter 5 — Proof by Induction](ch05-proof-by-induction.md) · Next → [Chapter 7 — Time/Space Complexity & Amortized Analysis](ch07-time-space-complexity-and-amortized-analysis.md)
