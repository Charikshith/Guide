# Volume 0 — Math & Mental Models

> Goal: The math the rest of the book silently assumes. Load-bearing for algorithms (Vol 1 Part 4) and all of AI (Vol 5).
>
> Hard prerequisite gate. Don't start Volume 1 Part 4 (algorithms) or any of Volume 5 (AI) without it.
>
> **Chapters 1–9.**

# Contents

1. Logic & Boolean Algebra
2. Sets, Relations & Functions
3. Combinatorics & Counting
4. Graph Theory Foundations
5. Proof by Induction
6. Asymptotic Notation (Big-O, Θ, Ω)
7. Time/Space Complexity & Amortized Analysis
8. Probability, Distributions & Bayes
9. Linear Algebra for AI

---

## Chapter 1 — Logic & Boolean Algebra

**Concept:** Propositional logic, truth tables, De Morgan's laws; how boolean algebra maps to `and`/`or`/`not` and bitwise operators.

**Prereqs:** none.

**Diagram:** Truth tables for AND/OR/NOT/XOR, plus a Venn diagram of De Morgan's `¬(A∧B) = ¬A∨¬B`.

**Example:** `assert (not (a and b)) == (not a or not b)` — De Morgan.

**Exercises:** (1) Build the truth table for `(A → B) ∧ ¬B` and show it forces `¬A` (modus tollens). (2) Simplify `¬(¬A ∨ (B ∧ ¬C))` to a form using only AND and NOT.

**Mini project:** A boolean-expression simplifier that reduces small expressions via De Morgan and distributivity.

**Open source:** [`sympy/sympy`](https://github.com/sympy/sympy) — the `sympy.logic` module.

**Interview:** "Why does `x & (x - 1) == 0` test for a power of two?" / "Prove De Morgan's laws with a truth table."

**Checklist:** ☐ derive every gate from NAND alone ☐ negate a compound condition correctly ☐ know short-circuit evaluation order ☐ convert `if/else` chains into boolean expressions

---

## Chapter 2 — Sets, Relations & Functions

**Concept:** Sets, subsets, unions/intersections/differences, Cartesian products; relations (reflexive/symmetric/transitive); functions (injective/surjective/bijective).

**Prereqs:** Ch 1.

**Diagram:** Two overlapping sets + an arrow diagram of a function mapping domain → codomain.

**Example:** `set("mississippi")` → `{'m','i','s','p'}`; a bijection maps each key to one value.

**Exercises:** (1) Prove `|A ∪ B| = |A| + |B| − |A ∩ B|`. (2) Which relation properties does "divides" have on integers?

**Mini project:** A set-operations calculator with a visualization of two overlapping sets.

**Open source:** [`python/cpython`](https://github.com/python/cpython) — Python's built-in `set`/`frozenset`.

**Interview:** "What's the difference between a function and a relation?" / "Give an example of a relation that's symmetric but not transitive."

**Checklist:** ☐ state the inclusion-exclusion principle ☐ classify a relation's properties ☐ explain why hash sets give O(1) membership

---

## Chapter 3 — Combinatorics & Counting

**Concept:** Permutations, combinations, the multiplication/addition rules, binomial coefficients, pigeonhole principle.

**Prereqs:** Ch 1.

**Diagram:** A decision tree showing n·(n−1)·… choices for permutations.

**Example:** `math.comb(10, 3) == 120` — choosing 3 from 10 without order.

**Exercises:** (1) How many distinct words can be made from the letters of "BANANA"? (2) Prove that among 13 people, two share a birth month (pigeonhole).

**Mini project:** A password-strength estimator that computes the size of the search space.

**Open source:** [`scipy/scipy`](https://github.com/scipy/scipy) — `scipy.special.comb`.

**Interview:** "How many unique orderings of a deck of 52 cards?" / "Explain the pigeonhole principle with an example."

**Checklist:** ☐ know when order matters ☐ compute permutations with duplicates ☐ apply the pigeonhole principle

---

## Chapter 4 — Graph Theory Foundations

**Concept:** Vertices, edges, directed vs undirected, degree, paths/cycles, connectivity, trees (n−1 edges, acyclic).

**Prereqs:** Ch 2.

**Diagram:** A small graph with labels for degree, a path, a cycle, and a spanning tree.

**Example:** `G = {0:{1,2}, 1:{0,2}, 2:{0,1}}` — an undirected triangle.

**Exercises:** (1) Prove a tree with n vertices has n−1 edges. (2) Show the handshaking lemma: sum of degrees = 2·|E|.

**Mini project:** A graph class with degree, path-existence, and cycle-detection helpers.

**Open source:** [`networkx/networkx`](https://github.com/networkx/networkx).

**Interview:** "What's the difference between a path and a walk?" / "When is a graph a tree?"

**Checklist:** ☐ state the handshaking lemma ☐ detect a cycle ☐ explain connectivity vs biconnectivity

---

## Chapter 5 — Proof by Induction

**Concept:** Base case + inductive step; strong induction; using induction to prove loop invariants and recursion correctness.

**Prereqs:** Ch 1.

**Diagram:** A domino-chain drawing: first domino falls, and each topples the next.

**Example:** Prove `1+2+…+n = n(n+1)/2`: base n=1, then assume for k and add k+1.

**Exercises:** (1) Prove `2^n > n` for all n ≥ 1. (2) Prove a binary tree of height h has at most `2^h − 1` nodes.

**Mini project:** A recursive factorial/power function with a written inductive proof of correctness.

**Open source:** [`leanprover/lean4`](https://github.com/leanprover/lean4) — theorem prover, induction is the core tool.

**Interview:** "Prove by induction that the sum of the first n odd numbers is n²." / "What's strong induction vs weak?"

**Checklist:** ☐ identify base case ☐ write the inductive step ☐ use induction to justify a loop invariant

---

## Chapter 6 — Asymptotic Notation (Big-O, Θ, Ω)

**Concept:** Big-O (upper bound), Ω (lower bound), Θ (tight); growth classes (1, log n, n, n log n, n², 2ⁿ); worst vs average vs best case.

**Prereqs:** Ch 3.

**Diagram:** A graph of growth curves crossing at some n₀, with f(n) shaded under c·g(n).

**Example:** A loop over n items doing O(1) work each is O(n); a nested loop is O(n²).

**Exercises:** (1) Classify `3n² + 100n + 7` as Θ(n²) with witnesses c and n₀. (2) Order `log n, n log n, 2ⁿ, n², √n` by growth.

**Mini project:** A tiny benchmark script that plots measured runtime vs n and fits the Big-O curve.

**Open source:** [`sympy/sympy`](https://github.com/sympy/sympy) — `sympy.series.Order`.

**Interview:** "What's the difference between O(n) and Ω(n)?" / "Is O(log n) always faster than O(n)?"

**Checklist:** ☐ give formal c/n₀ witnesses ☐ rank common growth classes ☐ distinguish worst/average case

---

## Chapter 7 — Time/Space Complexity & Amortized Analysis

**Concept:** Counting operations; space complexity incl. recursion stack; amortized cost via aggregate/accounting (dynamic-array doubling).

**Prereqs:** Ch 6.

**Diagram:** A dynamic array's doubling steps drawn as a staircase of copies totaling O(n).

**Example:** Python list `append` is amortized O(1) — occasional O(n) reallocations average out.

**Exercises:** (1) Show that n pushes on a doubling vector cost O(n) total. (2) Compute the space complexity of a recursive DFS (stack depth).

**Mini project:** Implement a doubling dynamic array and instrument the number of element copies across n appends.

**Open source:** [`python/cpython`](https://github.com/python/cpython) — `list` growth strategy in `listobject.c`.

**Interview:** "Why is hash table insertion 'amortized' O(1)?" / "Explain amortized analysis with a bank-account argument."

**Checklist:** ☐ do aggregate amortized math ☐ count auxiliary space ☐ explain why amortized ≠ average-case

---

## Chapter 8 — Probability, Distributions & Bayes

**Concept:** Sample spaces, independence, expectation, variance, common distributions (uniform, binomial, normal), Bayes' theorem.

**Prereqs:** Ch 3.

**Diagram:** A Bayes two-branch tree: P(A|B) computed from P(B|A), P(A), P(B).

**Example:** `P(disease|positive) = P(positive|disease)·P(disease) / P(positive)` — the classic false-positive trap.

**Exercises:** (1) Compute expectation of a fair six-sided die. (2) A test is 99% accurate, disease prevalence 1% — what's P(disease|positive)?

**Mini project:** A Monte Carlo simulation of a false-positive diagnosis and a die-roll expectation.

**Open source:** [`numpy/numpy`](https://github.com/numpy/numpy) — `numpy.random`.

**Interview:** "Explain Bayes' theorem in plain words." / "What's the difference between expectation and variance?"

**Checklist:** ☐ compute expectation/variance ☐ apply Bayes to a real example ☐ recognize independence vs conditional dependence

---

## Chapter 9 — Linear Algebra for AI

**Concept:** Vectors, vector spaces, matrices & operations, dot product as similarity, eigenvalues/eigenvectors (intuition), gradients & derivatives as the engine of backprop.

**Prereqs:** Ch 2, Ch 8.

**Diagram:** Two vectors with the angle showing dot-product similarity; a matrix as a linear transformation of space.

**Example:** `cosine = (a @ b) / (norm(a) * norm(b))` — similarity used everywhere in embeddings.

**Exercises:** (1) Compute a dot product by hand and interpret the sign. (2) Compute the gradient of `f(x)=x²` and `f(x,y)=x²+y²` at a point.

**Mini project:** A 2D embedding visualizer that computes cosine similarity and nearest neighbors for a small vector set.

**Open source:** [`numpy/numpy`](https://github.com/numpy/numpy) and [`pytorch/pytorch`](https://github.com/pytorch/pytorch) (`torch.autograd`).

**Interview:** "Why does the dot product measure similarity?" / "What does an eigenvector represent?"

**Checklist:** ☐ multiply matrices correctly ☐ explain dot-product similarity ☐ state what a gradient tells you ☐ intuit eigenvalues as scaling directions

---

**Exit criteria:** Solve a set of Big-O, probability, and linear-algebra problems from scratch.
