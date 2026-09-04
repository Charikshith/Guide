# Volume 1 — Computer Science Foundations

> Goal: Understand how computers work from the hardware up to applications.
>
> **Chapters 1–49.**

---

## Part 1 — Programming Fundamentals

### Chapter 1 — Variables, Data Types & Operators

**Concept:** Names that hold values; primitive (int, float, bool, char) vs complex (string, struct, object) types; arithmetic, comparison, logical, and bitwise operators; expressions vs statements.

**Prereqs:** none.

**Diagram:** A box-and-label diagram of a variable bound to a value in memory, plus a type table.

**Example:** `x = 5; y = x * 2; is_even = (y % 2 == 0)` — a variable, an expression, a boolean.

**Exercises:** (1) Predict the type of `3 / 2` in Python, Rust, and JS. (2) Write a one-liner using only bitwise ops to swap two ints.

**Mini project:** A calculator that reads an expression string, tokenizes it, and evaluates it (+, −, ×, ÷, parentheses).

**Open source:** [`rust-lang/rust`](https://github.com/rust-lang/rust) type system; [`python/cpython`](https://github.com/python/cpython) `operator` module.

**Interview:** "What's the difference between an expression and a statement?" / "Explain `x++` vs `++x`."

**Checklist:** ☐ name each primitive type's size/range ☐ know operator precedence ☐ distinguish value vs reference types

---

### Chapter 2 — Control Flow

**Concept:** `if`/`else`, `switch`/`match`, and loops (`for`, `while`, `do/while`, break, continue). Pattern matching in modern languages.

**Prereqs:** Ch 1.

**Diagram:** A flowchart of if/else branching and a loop with its exit condition.

**Example:** Rust `match` on an enum; a `for` loop summing an array.

**Exercises:** (1) Rewrite an if/else chain as a `match`. (2) Implement FizzBuzz using both a loop and recursion.

**Mini project:** A number-guessing game with input validation and a retry loop.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `match` statement (3.10+).

**Interview:** "When is `switch` faster than an if/else chain?" / "Explain fallthrough in C-style switch."

**Checklist:** ☐ convert if/else to match ☐ know loop exit vs continue ☐ avoid off-by-one errors

---

### Chapter 3 — Functions, Parameters, Return Values, Scope & Namespaces

**Concept:** Defining and calling functions; parameters vs arguments; pass-by-value vs pass-by-reference; return values (incl. multiple); lexical scope, closures over scope, and namespaces.

**Prereqs:** Ch 2.

**Diagram:** A call-stack diagram showing frames, parameters, locals, and return address.

**Example:** `def add(a, b): return a + b`; a closure capturing a counter variable.

**Exercises:** (1) Predict the output of a function with shadowed vs captured variables. (2) Write a function that returns another function.

**Mini project:** A memoizing `fib(n)` that demonstrates parameter passing and closure state.

**Open source:** [`rust-lang/rust`](https://github.com/rust-lang/rust) (explicit lifetimes and scoping).

**Interview:** "Pass-by-value vs pass-by-reference — what does Python do?" / "What is a closure?"

**Checklist:** ☐ trace a call stack ☐ explain lexical scope ☐ write a closure from scratch

---

### Chapter 4 — Built-in Data Structures

**Concept:** Arrays, lists, tuples, dictionaries/hashmaps, sets, queues, stacks — operations and time complexity for each.

**Prereqs:** Ch 1.

**Diagram:** A hashmap with buckets and chaining; a stack (LIFO) vs queue (FIFO) side by side.

**Example:** `d = {"a": 1}; d["a"] += 1` (hashmap); `stack.append(x)` / `stack.pop()`.

**Exercises:** (1) Implement a stack using only a list. (2) Explain when to use a tuple over a list.

**Mini project:** A task scheduler using a priority queue and a simple FIFO queue.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `collections` (`deque`, `defaultdict`).

**Interview:** "Array vs linked list — when is each better?" / "How does a hashmap achieve O(1) lookup?"

**Checklist:** ☐ know each structure's big-O ☐ pick the right structure for a task ☐ implement stack/queue by hand

---

### Chapter 5 — Modules, Packages, Imports & Dependency Management

**Concept:** Splitting code into modules, bundling into packages/libraries, importing, and pinning dependencies.

**Prereqs:** Ch 3.

**Diagram:** A directory tree showing modules → package → library and the dependency graph.

**Example:** `import numpy as np` (module); `pip install -e .` (package); `Cargo.toml` (deps).

**Exercises:** (1) Create a package with `__init__.py` and import a submodule. (2) Pin a dependency and explain `~=` vs `==` vs `^`.

**Mini project:** A small reusable library published locally with a lockfile.

**Open source:** [`python/cpython`](https://github.com/python/cpython) import system; [`rust-lang/cargo`](https://github.com/rust-lang/cargo).

**Interview:** "What's the difference between a module and a package?" / "What problem do lockfiles solve?"

**Checklist:** ☐ structure a package cleanly ☐ read a lockfile ☐ avoid circular imports

---

### Chapter 6 — Error Handling

**Concept:** Exceptions, panics, `Result`/`Option` types, error propagation (`?`), and custom error types. Fail loudly vs gracefully.

**Prereqs:** Ch 3.

**Diagram:** A try/catch flow vs Rust's `Result<T, E>` propagation chain.

**Example:** Rust `let x = parse()?;`; Python `try/except/else/finally`.

**Exercises:** (1) Write a parser that returns `Result` instead of panicking. (2) Create a custom exception with context.

**Mini project:** A config loader that surfaces precise, actionable errors with file/line context.

**Open source:** [`rust-lang/rust`](https://github.com/rust-lang/rust) `Result`/`Option`; [`serde-rs/serde`](https://github.com/serde-rs/serde) error types.

**Interview:** "Exceptions vs error values — trade-offs?" / "What does `finally` guarantee?"

**Checklist:** ☐ propagate errors without swallowing them ☐ distinguish recoverable vs fatal ☐ write a custom error type

---

### Chapter 7 — File I/O

**Concept:** Opening, reading, writing, appending; text vs binary mode; buffering; atomic writes; file descriptors.

**Prereqs:** Ch 3.

**Diagram:** A file-handle lifecycle diagram: open → read/write → flush → close.

**Example:** `with open("f.txt") as f: f.read()` (context-managed close).

**Exercises:** (1) Read a 1 GB file without loading it all into memory. (2) Write atomically via temp file + rename.

**Mini project:** A log-rotating file writer that splits files by size.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `io` module; [`BLAKE3-team/BLAKE3`](https://github.com/BLAKE3-team/BLAKE3) (streaming I/O patterns).

**Interview:** "Why use `with`/context managers for files?" / "Text vs binary mode — what changes?"

**Checklist:** ☐ always close/stream properly ☐ know buffered vs unbuffered ☐ write atomically

---

### Chapter 8 — Data Formats (Text): JSON, CSV, XML, YAML, TOML

**Concept:** Structured serialization formats — syntax, trade-offs, and when to use each.

**Prereqs:** Ch 7.

**Diagram:** Side-by-side snippets of the same record in JSON, YAML, TOML, XML, CSV.

**Example:** `json.dumps({"a": 1})`; a TOML config section.

**Exercises:** (1) Parse a CSV with quoted commas. (2) Round-trip a nested object through JSON and YAML.

**Mini project:** A config-file migrator that converts YAML ↔ JSON ↔ TOML.

**Open source:** [`yaml/pyyaml`](https://github.com/yaml/pyyaml); [`toml-lang/toml`](https://github.com/toml-lang/toml).

**Interview:** "YAML vs JSON vs TOML — when each?" / "Why is CSV parsing non-trivial?"

**Checklist:** ☐ pick the right format for config vs data ☐ handle escaping correctly ☐ avoid YAML footguns (e.g., `on` = true)

---

### Chapter 9 — Character Encoding & Binary Serialization

**Concept:** ASCII, Unicode, UTF-8 vs UTF-16 vs UTF-32; encoding/decoding; binary formats: Protobuf, MessagePack, Avro.

**Prereqs:** Ch 8.

**Diagram:** A byte-layout diagram of UTF-8 multibyte encoding and a Protobuf varint field.

**Example:** `"é".encode("utf-8")` → 2 bytes; a `.proto` message compiled to fast binary.

**Exercises:** (1) Manually encode a code point to UTF-8 bytes. (2) Compare JSON vs MessagePack sizes for a sample object.

**Mini project:** A tiny Protobuf-like varint encoder/decoder.

**Open source:** [`protocolbuffers/protobuf`](https://github.com/protocolbuffers/protobuf); [`simdutf/simdutf`](https://github.com/simdutf/simdutf).

**Interview:** "Why does UTF-8 dominate?" / "Schema-first (Protobuf) vs schema-less (JSON) — trade-offs?"

**Checklist:** ☐ explain UTF-8 multibyte ☐ know when binary beats text ☐ read a varint

---

### Chapter 10 — Generics, Traits, Interfaces & Abstract Classes

**Concept:** Writing code over types; bounded polymorphism (traits/interfaces) and shared contracts (abstract classes).

**Prereqs:** Ch 3.

**Diagram:** A `Box<T>` / `List<T>` diagram; a `Shape` interface implemented by `Circle`/`Square`.

**Example:** Rust `fn largest<T: PartialOrd>(xs: &[T]) -> &T`.

**Exercises:** (1) Write a generic `sort` that works on any `Comparable`. (2) Implement an interface with two different classes.

**Mini project:** A generic in-memory cache `Cache<K, V>` with a trait for eviction policy.

**Open source:** [`rust-lang/rust`](https://github.com/rust-lang/rust) std traits (`Iterator`, `Display`).

**Interview:** "Generics vs inheritance — when each?" / "What's monomorphization?"

**Checklist:** ☐ write a generic function ☐ implement a trait/interface ☐ know dynamic vs static dispatch

---

### Chapter 11 — Advanced Language Features

**Concept:** Reflection, metaprogramming, decorators, context managers, closures, lambdas, iterators, generators, regular expressions — the power tools of a language.

**Prereqs:** Ch 3, Ch 10.

**Diagram:** A decorator wrapping a function (in → out); a generator's yield/pause/resume cycle.

**Example:** `@lru_cache` on a function; `(x for x in xs if x > 0)`; `re.search(r"\d+", s)`.

**Exercises:** (1) Write a decorator that times a function. (2) Build a generator producing the Fibonacci sequence.

**Mini project:** A retry decorator + a streaming log-line regex parser.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `functools`, `re`, `contextlib`.

**Interview:** "What's a generator, and why is it memory-efficient?" / "When would you use reflection?"

**Checklist:** ☐ write a decorator/context manager ☐ lazily stream with a generator ☐ craft a non-trivial regex

---

### Chapter 12 — Memory: Stack, Heap, Ownership & Garbage Collection

**Concept:** Stack vs heap allocation; references; Rust ownership/borrowing/lifetimes; tracing GC vs reference counting.

**Prereqs:** Ch 3.

**Diagram:** A memory layout with stack frames and a heap with GC roots.

**Example:** Rust borrow-checker error when two mutable references alias; Python `sys.getrefcount`.

**Exercises:** (1) Explain why a returned reference to a stack local is invalid. (2) Write a Rust program and fix a borrow-checker error.

**Mini project:** A cycle-producing data structure in Python and how the GC collects it.

**Open source:** [`python/cpython`](https://github.com/python/cpython) GC; [`rust-lang/rust`](https://github.com/rust-lang/rust) borrow checker.

**Interview:** "Stack vs heap allocation?" / "How does Rust prevent use-after-free?"

**Checklist:** ☐ explain stack/heap ☐ read a borrow error ☐ know GC vs refcounting trade-offs

---

### Chapter 13 — Concurrency: Threads, Processes, Async, Futures & Coroutines

**Concept:** Threads vs processes; shared memory vs message passing; async/await, futures/promises, coroutines; the event loop.

**Prereqs:** Ch 12.

**Diagram:** A GIL/thread diagram vs a single-threaded async event loop with interleaved tasks.

**Example:** `asyncio.gather(*tasks)`; Rust `tokio::spawn(async { ... })`.

**Exercises:** (1) Parallelize I/O-bound work with async. (2) Show a race condition on a shared counter and fix it.

**Mini project:** A concurrent web scraper with a bounded worker pool and rate limiting.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `asyncio`; [`tokio-rs/tokio`](https://github.com/tokio-rs/tokio).

**Interview:** "Threads vs processes vs coroutines?" / "What is a future/promise?"

**Checklist:** ☐ choose thread vs async per workload ☐ detect a data race ☐ use a semaphore to bound concurrency

---

### Chapter 14 — Programming Paradigms

**Concept:** Imperative, declarative, object-oriented, functional, reactive, and event-driven styles — and recognizing them in real code.

**Prereqs:** Ch 3, Ch 13.

**Diagram:** A map of paradigms with example one-liners for each.

**Example:** `map/filter/reduce` (functional) vs `class` + methods (OO) vs a `Subject`/observer stream (reactive).

**Exercises:** (1) Rewrite an imperative loop as `map/filter/reduce`. (2) Model an event-driven system with callbacks.

**Mini project:** A tiny reactive event bus with subscribe/publish and a functional pipeline.

**Open source:** [`ReactiveX/RxPY`](https://github.com/ReactiveX/RxPY); [`python/cpython`](https://github.com/python/cpython) `itertools`.

**Interview:** "Declarative vs imperative?" / "What makes code 'functional'?"

**Checklist:** ☐ write pure functions ☐ identify a paradigm in the wild ☐ explain immutability benefits

---

### Chapter 15 — Correctness Traps

**Concept:** IEEE-754 floating point, integer overflow/signedness, and date/time/timezone bugs — the silent killers.

**Prereqs:** Ch 1.

**Diagram:** An IEEE-754 bit layout (sign/exponent/mantissa) and a two's-complement wrap-around.

**Example:** `0.1 + 0.2 != 0.3`; `i32::MAX + 1` wraps; UTC vs local time offsets.

**Exercises:** (1) Find a floating-point comparison bug and fix it with epsilon. (2) Compute a duration across a DST boundary correctly.

**Mini project:** A money class using integers (cents) and a DST-aware event scheduler.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `decimal`/`fractions`; [`chronotope/chrono`](https://github.com/chronotope/chrono).

**Interview:** "Why is `0.1 + 0.2 != 0.3`?" / "How do you store money?"

**Checklist:** ☐ never compare floats with `==` ☐ check overflow modes ☐ always store UTC + explicit tz

---

## Part 2 — Developer Environment

### Chapter 16 — Linux: Filesystem, Shell, Bash, Permissions, Users & Groups

**Concept:** The Unix filesystem tree, shell basics, Bash scripting, file permissions, users and groups.

**Prereqs:** none.

**Diagram:** A filesystem tree from `/` with permission bit annotations (`rwxr-xr-x`).

**Example:** `chmod 750 script.sh`; a Bash loop `for f in *.txt; do ...; done`.

**Exercises:** (1) Explain `chmod 750` in words. (2) Write a Bash script that finds and deletes files older than 30 days.

**Mini project:** A Bash backup script with permission handling and a cron entry.

**Open source:** [`torvalds/linux`](https://github.com/torvalds/linux) (permission model); [`bash`](https://www.gnu.org/software/bash/).

**Interview:** "What do 4/2/1 mean in permissions?" / "How do you make a script executable?"

**Checklist:** ☐ navigate the tree by heart ☐ set permissions correctly ☐ write a safe Bash script

---

### Chapter 17 — Linux: Processes, Signals, Services, systemd, SSH, Cron & Networking

**Concept:** Process lifecycle, signals (SIGTERM/SIGKILL/SIGINT), systemd units, remote access via SSH, and scheduled jobs via cron.

**Prereqs:** Ch 16.

**Diagram:** A process state machine (running/stopped/zombie) and a signal delivery diagram.

**Example:** `systemctl restart app`; `kill -TERM $PID`; a crontab entry `0 3 * * * /backup.sh`.

**Exercises:** (1) Trap SIGTERM in a script to clean up gracefully. (2) Write a systemd unit for a long-running service.

**Mini project:** A daemon with a systemd unit, a signal handler, and SSH remote logs.

**Open source:** [`systemd/systemd`](https://github.com/systemd/systemd); [`openssh/openssh-portable`](https://github.com/openssh/openssh-portable).

**Interview:** "SIGTERM vs SIGKILL?" / "What is a zombie process?"

**Checklist:** ☐ trap signals ☐ write a systemd unit ☐ schedule with cron safely

---

### Chapter 18 — Terminal Tools: grep, sed, awk, jq, curl, wget, find, xargs, tmux, rsync

**Concept:** The Unix toolbox — text search/transform, JSON, HTTP clients, file discovery, multiplexing, and sync.

**Prereqs:** Ch 16.

**Diagram:** A pipeline diagram: `grep` → `sed` → `awk` → `sort | uniq -c`.

**Example:** `cat logs.json | jq '.status' | sort | uniq -c`; `find . -name '*.py' | xargs grep TODO`.

**Exercises:** (1) Sum a CSV column with awk. (2) Extract all URLs from logs with grep + sed.

**Mini project:** A shell pipeline that parses access logs into a top-N report using jq/awk/sort.

**Open source:** [`jqlang/jq`](https://github.com/jqlang/jq); [`curl/curl`](https://github.com/curl/curl).

**Interview:** "How do you find the 10 largest files under a directory?" / "xargs — why is it needed?"

**Checklist:** ☐ compose pipelines fluently ☐ use jq for JSON ☐ batch safely with xargs

---

### Chapter 19 — Git: Branching, Merge, Rebase & Cherry-Pick

**Concept:** The commit DAG, branches, merge (3-way), rebase (replay), and cherry-pick (apply a commit elsewhere).

**Prereqs:** none.

**Diagram:** A commit graph showing a branch, a merge commit, and a rebase flattening history.

**Example:** `git rebase main`; `git cherry-pick abc123`; resolving a merge conflict.

**Exercises:** (1) Resolve a merge conflict by hand. (2) Rebase a feature branch and explain the resulting history.

**Mini project:** Reproduce a real PR flow (branch → commits → rebase → squash-merge) on a toy repo.

**Open source:** [`git/git`](https://github.com/git/git).

**Interview:** "Merge vs rebase — trade-offs?" / "What is a fast-forward merge?"

**Checklist:** ☐ read a commit graph ☐ resolve conflicts confidently ☐ choose merge vs rebase deliberately

---

### Chapter 20 — Git: Tags, Stash, Hooks & Internals

**Concept:** Tags (releases), stash (temporary WIP), hooks (automation), and Git's object model (blobs/trees/commits, content addressing).

**Prereqs:** Ch 19.

**Diagram:** Git's object database: commit → tree → blob, with SHA-1 hashes.

**Example:** `git tag v1.0.0`; `git stash push -m wip`; a pre-commit hook running a linter.

**Exercises:** (1) Inspect a commit object with `git cat-file`. (2) Write a pre-commit hook that blocks whitespace errors.

**Mini project:** A release script that tags, signs, and pushes — plus a pre-push hook running tests.

**Open source:** [`git/git`](https://github.com/git/git) internals; [`pre-commit/pre-commit`](https://github.com/pre-commit/pre-commit).

**Interview:** "What is Git's content model?" / "What's a lightweight vs annotated tag?"

**Checklist:** ☐ explain content addressing ☐ tag a release ☐ automate with hooks

---

### Chapter 21 — Build Systems & Package Management

**Concept:** Cargo, pip, uv, Poetry, npm, pnpm, Make, CMake, Taskfiles; packaging Python/Rust/Node projects; semantic versioning.

**Prereqs:** Ch 5.

**Diagram:** A dependency-resolution diagram (direct vs transitive deps) and a SemVer axis.

**Example:** `cargo build --release`; `uv pip install -e .`; `npm install` with a lockfile.

**Exercises:** (1) Add a dependency and pin it with a lockfile. (2) Explain how `^1.2.3` resolves.

**Mini project:** A multi-package repo built end-to-end by one Make/Taskfile command.

**Open source:** [`astral-sh/uv`](https://github.com/astral-sh/uv); [`rust-lang/cargo`](https://github.com/rust-lang/cargo).

**Interview:** "What is SemVer and when to bump major/minor/patch?" / "Lockfile vs manifest?"

**Checklist:** ☐ reproduce a build from a lockfile ☐ read SemVer ranges ☐ script common tasks

---

## Part 3 — Software Engineering Fundamentals

### Chapter 22 — Clean Code & Refactoring

**Concept:** Naming, small functions/classes, readability, and safe refactoring (red/green/refactor).

**Prereqs:** Ch 3.

**Diagram:** A before/after refactor of a long function into named steps.

**Example:** Renaming `d` → `elapsed_ms`; extracting a 40-line block into `parse_response()`.

**Exercises:** (1) Refactor a messy function without changing behavior (tests stay green). (2) Apply the "one level of abstraction per function" rule.

**Mini project:** Take a 200-line script and refactor it into small, tested functions.

**Open source:** [`psf/requests`](https://github.com/psf/requests) (clean Python); [`rust-lang/rust`](https://github.com/rust-lang/rust) std (naming conventions).

**Interview:** "What makes a function 'too long'?" / "How do you refactor safely?"

**Checklist:** ☐ write names that need no comment ☐ keep functions small ☐ refactor only under tests

---

### Chapter 23 — Documentation, ADRs & READMEs

**Concept:** Markdown, API docs, docstrings, Architecture Decision Records, and READMEs that actually help.

**Prereqs:** Ch 22.

**Diagram:** A template layout for an ADR (context/decision/consequences).

**Example:** A docstring with params/returns/raises; a one-page ADR recording "why PostgreSQL."

**Exercises:** (1) Write a docstring that a tool can render. (2) Write an ADR for a real past decision.

**Mini project:** Generate API docs from docstrings and write a project README + first ADR.

**Open source:** [`rust-lang/rust`](https://github.com/rust-lang/rust) rustdoc; [`mkdocs/mkdocs`](https://github.com/mkdocs/mkdocs).

**Interview:** "What belongs in a docstring vs a README?" / "Why record ADRs?"

**Checklist:** ☐ document why, not just what ☐ write renderable docstrings ☐ keep a decision log

---

### Chapter 24 — Logging

**Concept:** Log levels, structured logging, correlation IDs, and log hygiene (never leak secrets).

**Prereqs:** Ch 22.

**Diagram:** A request path with a correlation ID threaded through services into one log stream.

**Example:** `log.info("order_placed", order_id=123, user_id=7, trace_id=t)`.

**Exercises:** (1) Add a correlation ID to a request pipeline. (2) Pick the right level for a warning vs error.

**Mini project:** A structured logger that emits JSON and injects a trace ID into every line.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `logging`; [`Delgan/loguru`](https://github.com/Delgan/loguru).

**Interview:** "Structured vs free-text logging?" / "What level is a recoverable failure?"

**Checklist:** ☐ use levels consistently ☐ emit machine-parseable logs ☐ redact secrets

---

### Chapter 25 — Configuration & Secrets Management

**Concept:** Environment variables, dotenv, YAML/TOML/JSON config, and keeping secrets out of code.

**Prereqs:** Ch 8, Ch 24.

**Diagram:** A 12-factor config flow: env → config object → app; secrets via a vault.

**Example:** `os.getenv("DB_URL")`; a TOML config with `[server] port = 8080`.

**Exercises:** (1) Load config with layered precedence (defaults < file < env). (2) Move a hardcoded API key into a secret store.

**Mini project:** A config loader supporting file + env + CLI overrides, failing fast on missing keys.

**Open source:** [`theskumar/python-dotenv`](https://github.com/theskumar/python-dotenv); [`hashicorp/vault`](https://github.com/hashicorp/vault).

**Interview:** "Why never commit secrets?" / "Config file vs env var — when each?"

**Checklist:** ☐ precedence is explicit ☐ secrets never in git ☐ validate config at startup

---

### Chapter 26 — Testing: Unit, Integration, Mocking & Coverage

**Concept:** The testing pyramid; unit vs integration; mocks/stubs/fakes; coverage as a signal, not a goal.

**Prereqs:** Ch 22.

**Diagram:** The testing pyramid (many unit, fewer integration, fewest e2e).

**Example:** A unit test with a fake clock; an integration test against a test database.

**Exercises:** (1) Write a unit test with a mock. (2) Write an integration test that spins up a test DB.

**Mini project:** A test suite for a small service with unit + integration + a coverage report.

**Open source:** [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest); [`rust-lang/rust`](https://github.com/rust-lang/rust) `#[test]`.

**Interview:** "Mock vs stub vs fake?" / "Why is 100% coverage not the goal?"

**Checklist:** ☐ write tests that fail for the right reason ☐ mock only at seams ☐ read a coverage report

---

### Chapter 27 — Debugging & Profiling

**Concept:** Debuggers (breakpoints, stepping), stack traces, profiling CPU/memory, and the scientific debugging method.

**Prereqs:** Ch 26.

**Diagram:** A stack trace annotated with frames; a flame graph of hot functions.

**Example:** `pdb.set_trace()`; `py-spy top`; reading a panic backtrace.

**Exercises:** (1) Reproduce a bug, form a hypothesis, and confirm with a breakpoint. (2) Profile a slow function and find the hotspot.

**Mini project:** Add an intentional performance bug, profile it, fix it, and record a before/after flame graph.

**Open source:** [`benfred/py-spy`](https://github.com/benfred/py-spy); [`rr-debugger/rr`](https://github.com/rr-debugger/rr).

**Interview:** "How do you debug a crash you can't reproduce locally?" / "What is a flame graph?"

**Checklist:** ☐ read a stack trace ☐ bisect to a root cause ☐ profile before optimizing

---

### Chapter 28 — Static Analysis: Linters, Formatters & Type Checkers

**Concept:** Catching bugs before runtime — linters (style/bugs), formatters (consistency), type checkers (soundness).

**Prereqs:** Ch 22.

**Diagram:** A CI pipeline: formatter → linter → type checker → tests.

**Example:** `ruff check .`; `black .`; `mypy src/`.

**Exercises:** (1) Configure a linter and fix its findings. (2) Add type hints until `mypy` passes strict.

**Mini project:** Wire a pre-commit hook running format + lint + type-check on every commit.

**Open source:** [`astral-sh/ruff`](https://github.com/astral-sh/ruff); [`python/mypy`](https://github.com/python/mypy).

**Interview:** "Linter vs type checker?" / "What does strict typing buy you?"

**Checklist:** ☐ keep a linter green ☐ format automatically ☐ type-check critical paths

---

## Part 4 — Data Structures & Algorithms

> Requires Volume 0 (complexity).

### Chapter 29 — Basic Data Structures: Arrays, Linked Lists, Stack & Queue

**Concept:** Contiguous vs linked storage; LIFO stack, FIFO queue; operations and their Big-O.

**Prereqs:** Vol 0 Ch 6–7.

**Diagram:** An array (contiguous cells) vs a linked list (nodes + pointers); push/pop and enqueue/dequeue.

**Example:** `list.append/pop` (stack); `collections.deque` (queue).

**Exercises:** (1) Implement a linked list with insert/delete. (2) Implement a queue using two stacks.

**Mini project:** A ring buffer with O(1) enqueue/dequeue and wraparound.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `listobject.c` and `deque`.

**Interview:** "Array vs linked list cache behavior?" / "Queue with two stacks — complexity?"

**Checklist:** ☐ know each op's Big-O ☐ implement all four from scratch ☐ explain cache locality

---

### Chapter 30 — Trees, BST, Heap & Trie

**Concept:** Tree terminology; binary search trees; heaps (priority queues); tries (prefix search).

**Prereqs:** Ch 29.

**Diagram:** A balanced BST, a min-heap as an array, and a trie of words.

**Example:** `heapq.heappush`; a BST `search` in O(log n) if balanced.

**Exercises:** (1) Implement BST insert/search/delete. (2) Build a trie and autocomplete a prefix.

**Mini project:** A URL router or autocomplete engine backed by a trie.

**Open source:** [`python/cpython`](https://github.com/python/cpython) `heapq`.

**Interview:** "Heap vs BST?" / "Why is a BST O(n) when unbalanced?"

**Checklist:** ☐ traverse pre/in/post-order ☐ heapify in O(n) ☐ autocomplete with a trie

---

### Chapter 31 — Hash Tables & Graphs

**Concept:** Hash functions, collisions, resizing; graph representations (adjacency list/matrix), directed/weighted.

**Prereqs:** Ch 29.

**Diagram:** A hash table with chaining; an adjacency list vs matrix.

**Example:** `dict` with a custom `__hash__`; `G = {0: [(1, 5), (2, 3)]}`.

**Exercises:** (1) Implement a hash table with chaining and resize. (2) Convert an adjacency matrix to a list.

**Mini project:** A word-frequency counter with a custom hash table; a tiny graph library.

**Open source:** [`python/cpython`](https://github.com/python/cpython) dict; [`networkx/networkx`](https://github.com/networkx/networkx).

**Interview:** "How do you handle collisions?" / "Adjacency list vs matrix — memory trade-off?"

**Checklist:** ☐ implement hashing + probing/chaining ☐ model a graph two ways ☐ know amortized O(1)

---

### Chapter 32 — Advanced Structures: Segment Tree, Fenwick Tree & Union-Find

**Concept:** Range queries (segment/Fenwick) and dynamic connectivity (union-find with path compression + union by rank).

**Prereqs:** Ch 30–31.

**Diagram:** A segment tree over an array; a union-find forest with rank.

**Example:** Fenwick prefix sums in O(log n); `find`/`union` with path compression.

**Exercises:** (1) Build a Fenwick tree for prefix sums. (2) Implement union-find and detect a cycle in a graph.

**Mini project:** A range-minimum-query engine and a connected-components counter.

**Open source:** [`atcoder/ac-library`](https://github.com/atcoder/ac-library) (`dsu`, `segtree`).

**Interview:** "When do you need a Fenwick tree?" / "Why is union-find near-O(1) amortized?"

**Checklist:** ☐ implement range sum/update ☐ implement find/union with both optimizations ☐ know when each applies

---

### Chapter 33 — Sorting, Searching & Binary Search

**Concept:** Quicksort/mergesort/heapsort, stability, and binary search on sorted data and monotonic predicates.

**Prereqs:** Ch 29, Vol 0 Ch 6.

**Diagram:** A quicksort partition step and a binary search halving diagram.

**Example:** `sorted(xs)` (Timsort); `bisect_left(xs, x)`.

**Exercises:** (1) Implement mergesort and quicksort. (2) Use binary search on the *answer* (e.g., min speed).

**Mini project:** A sort visualizer plus a "first bad version" binary-search solver.

**Open source:** [`python/cpython`](https://github.com/python/cpython) Timsort.

**Interview:** "Stable vs unstable sort?" / "Binary search on a predicate — how?"

**Checklist:** ☐ implement two sorts ☐ know stability implications ☐ binary-search on answers

---

### Chapter 34 — Graph Algorithms: DFS, BFS, Topological Sort & Backtracking

**Concept:** Depth-first and breadth-first traversal, cycle detection, topological order, and systematic backtracking.

**Prereqs:** Ch 31.

**Diagram:** A DFS recursion tree and a BFS level-by-level expansion; a DAG with a topological order.

**Example:** BFS shortest path (unweighted); Kahn's algorithm for topo sort.

**Exercises:** (1) Detect a cycle with DFS. (2) Topologically sort a task dependency graph. (3) Solve N-queens with backtracking.

**Mini project:** A course-scheduler (topo sort) + a Sudoku solver (backtracking).

**Open source:** [`networkx/networkx`](https://github.com/networkx/networkx) (`topological_sort`, `bfs_edges`).

**Interview:** "BFS vs DFS — when each?" / "How do you topologically sort?"

**Checklist:** ☐ traverse both ways ☐ detect cycles ☐ prune backtracking search spaces

---

### Chapter 35 — Dynamic Programming, Greedy, Divide & Conquer, Sliding Window & Two Pointers

**Concept:** Overlapping subproblems + memoization (DP), local-optimal choices (greedy), split-and-combine (divide & conquer), and the sliding-window / two-pointer patterns.

**Prereqs:** Ch 33–34.

**Diagram:** A DP memo table (knapsack); a two-pointer window shrinking/expanding.

**Example:** Fibonacci with memo; a sliding-window max-subarray sum.

**Exercises:** (1) Solve 0/1 knapsack top-down and bottom-up. (2) Longest substring without repeating chars via sliding window.

**Mini project:** A coin-change solver and a longest-substring tool with visual step output.

**Open source:** [`TheAlgorithms/Python`](https://github.com/TheAlgorithms/Python).

**Interview:** "How do you recognize a DP problem?" / "When is greedy provably optimal?"

**Checklist:** ☐ write top-down + bottom-up DP ☐ prove a greedy choice ☐ apply two-pointer/sliding-window

---

## Part 5 — Computer Architecture

### Chapter 36 — Binary, CPU, Registers, Cache & Memory Hierarchy

**Concept:** Binary and number representation (two's complement, floats); CPU registers; cache levels and the memory hierarchy.

**Prereqs:** Vol 0 Ch 1.

**Diagram:** A memory-hierarchy pyramid (registers → L1/L2/L3 → RAM → disk) with latencies.

**Example:** Two's-complement encoding of −1; a cache hit vs miss walkthrough.

**Exercises:** (1) Convert an int to two's complement bytes. (2) Explain why a row-major loop is faster than column-major.

**Mini project:** A tiny instruction-set simulator with registers and a simulated cache.

**Open source:** [`riscv`](https://github.com/riscv) specs; [`rpjohnst/decs`](https://github.com/rpjohnst/decs) (educational CPU simulator).

**Interview:** "Why is L1 cache tiny but critical?" / "What is a cache line?"

**Checklist:** ☐ encode two's complement ☐ name each memory tier's latency class ☐ exploit cache locality

---

### Chapter 37 — Instruction Cycle, Pipelining, SIMD & Virtual Memory

**Concept:** Fetch-decode-execute; pipelining and hazards; SIMD (data parallelism); virtual memory and page tables.

**Prereqs:** Ch 36.

**Diagram:** A 5-stage pipeline diagram with a bubble (hazard); a virtual→physical address translation.

**Example:** A pipelined add with a data hazard stall; SIMD adding 8 ints at once.

**Exercises:** (1) Identify a pipeline hazard in a code snippet. (2) Explain how a TLB miss resolves.

**Mini project:** A 5-stage pipeline simulator that shows stalls/bubbles on a small program.

**Open source:** [`verilator/verilator`](https://github.com/verilator/verilator) (simulate real HDL).

**Interview:** "What is a pipeline hazard?" / "Why does virtual memory exist?"

**Checklist:** ☐ trace fetch-decode-execute ☐ name the three hazard types ☐ explain page faults

---

## Part 6 — Operating Systems

### Chapter 38 — OS: Processes, Threads, Scheduling, Synchronization & Deadlocks

**Concept:** Process/thread lifecycle, CPU scheduling algorithms, synchronization primitives (mutexes, semaphores, condvars), and deadlock (four conditions).

**Prereqs:** Ch 13, Ch 37.

**Diagram:** A ready/running/blocked state machine; a deadlock wait-for cycle.

**Example:** A mutex-protected counter; a dining-philosophers deadlock.

**Exercises:** (1) Detect the deadlock in a lock-ordering bug and fix it. (2) Compare round-robin vs CFS scheduling.

**Mini project:** A simulator of the dining philosophers with deadlock vs a lock-ordering fix.

**Open source:** [`torvalds/linux`](https://github.com/torvalds/linux) scheduler (`kernel/sched`).

**Interview:** "What are the four Coffman conditions?" / "Mutex vs semaphore?"

**Checklist:** ☐ lock in a consistent order ☐ avoid busy-waiting ☐ name the deadlock conditions

---

### Chapter 39 — OS: Memory Management, File Systems, System Calls & IPC

**Concept:** Address spaces and paging; file systems (inodes, journals); the syscall boundary; IPC (pipes, sockets, shared memory, signals).

**Prereqs:** Ch 38.

**Diagram:** A process address space layout (text/data/heap/stack) and an inode→blocks mapping.

**Example:** `strace` of a program showing `open`/`read`/`write` syscalls; a pipe between two processes.

**Exercises:** (1) Trace the syscalls of `cat file`. (2) Implement producer-consumer with a pipe.

**Mini project:** A mini shell that forks, pipes, and redirects I/O.

**Open source:** [`torvalds/linux`](https://github.com/torvalds/linux) (`fs/`, `ipc/`).

**Interview:** "User space vs kernel space?" / "What happens on `write()`?"

**Checklist:** ☐ draw an address space ☐ explain an inode ☐ build a pipeline with pipes

---

## Part 7 — Networking

### Chapter 40 — Networking Fundamentals: OSI, TCP/IP, IP, Ports, DNS & NAT

**Concept:** Layered models, IP addressing/subnets, ports, DNS resolution, and NAT.

**Prereqs:** none.

**Diagram:** The OSI 7 layers next to the TCP/IP 4 layers; a DNS resolution chain.

**Example:** `dig example.com`; `192.168.1.10:443`; a NAT table mapping private→public.

**Exercises:** (1) Explain what happens between typing a URL and page load (DNS → TCP → TLS → HTTP). (2) Subnet a /24 and pick valid hosts.

**Mini project:** A small DNS client that resolves A/AAAA records over UDP.

**Open source:** [`miekg/dns`](https://github.com/miekg/dns); [`curl/curl`](https://github.com/curl/curl).

**Interview:** "Walk me through DNS resolution." / "What does NAT solve (and not solve)?"

**Checklist:** ☐ name each layer's job ☐ resolve DNS by hand ☐ explain port exhaustion

---

### Chapter 41 — Transport & Security: TCP, UDP, QUIC, TLS & HTTPS

**Concept:** TCP (handshake, reliability, flow/congestion control), UDP, QUIC; TLS handshake and HTTPS.

**Prereqs:** Ch 40.

**Diagram:** TCP 3-way handshake and TLS 1.3 handshake side by side.

**Example:** `nc` a TCP server; a `tcpdump` of the handshake; a TLS cert chain.

**Exercises:** (1) Explain TCP's reliability mechanisms. (2) Walk through a TLS 1.3 handshake.

**Mini project:** A minimal TCP echo server and a TLS-terminating proxy.

**Open source:** [`quinn-rs/quinn`](https://github.com/quinn-rs/quinn) (QUIC); [`openssl/openssl`](https://github.com/openssl/openssl).

**Interview:** "TCP vs UDP — when each?" / "Why is QUIC faster than TCP+TLS?"

**Checklist:** ☐ draw the handshakes ☐ explain congestion control ☐ know TLS's guarantees

---

### Chapter 42 — HTTP, REST, GraphQL & JSON-RPC

**Concept:** HTTP methods/status codes/headers/cookies/caching/CORS; REST resources; GraphQL queries; JSON-RPC.

**Prereqs:** Ch 41.

**Diagram:** A request/response exchange with status-code flow; a REST vs GraphQL query shape.

**Example:** `GET /users/1` → `200 OK`; a GraphQL query selecting fields; a JSON-RPC `{ "method": "add" }`.

**Exercises:** (1) Design REST endpoints for a resource with nested relations. (2) Write a GraphQL schema with a resolver.

**Mini project:** A small REST API + a GraphQL endpoint exposing the same data.

**Open source:** [`graphql/graphql-js`](https://github.com/graphql/graphql-js); [`encode/django-rest-framework`](https://github.com/encode/django-rest-framework).

**Interview:** "REST vs GraphQL — trade-offs?" / "Which status code for a duplicate create?"

**Checklist:** ☐ use correct methods/status codes ☐ set caching headers ☐ explain CORS

---

### Chapter 43 — WebSockets, gRPC, MQTT & SSE

**Concept:** Real-time/streaming protocols — WebSockets (bidirectional), gRPC (binary, streaming RPC), MQTT (pub/sub for IoT), SSE (server→client push).

**Prereqs:** Ch 42.

**Diagram:** A comparison of connection models: request/response vs persistent vs publish/subscribe.

**Example:** a WebSocket echo; a gRPC `.proto` with streaming; an SSE `text/event-stream`.

**Exercises:** (1) Implement a WebSocket chat server. (2) Define a streaming gRPC service.

**Mini project:** A live-updates feed using SSE + a WebSocket chat room.

**Open source:** [`grpc/grpc`](https://github.com/grpc/grpc); [`eclipse-mosquitto/mosquitto`](https://github.com/eclipse-mosquitto/mosquitto).

**Interview:** "WebSocket vs SSE?" / "Why gRPC over HTTP/2?"

**Checklist:** ☐ choose the right realtime protocol ☐ stream server→client with SSE ☐ define a gRPC contract

---

### Chapter 44 — Delivery: Load Balancing, Reverse Proxies & CDN

**Concept:** L4 vs L7 load balancing, reverse proxies (nginx), and CDN/edge caching.

**Prereqs:** Ch 42.

**Diagram:** A client → CDN → LB → backend pool diagram with L4/L7 split.

**Example:** an nginx `upstream` config; a Cloudflare edge-cache rule.

**Exercises:** (1) Configure an L7 LB with health checks. (2) Explain a CDN cache hit vs origin fetch.

**Mini project:** A load balancer simulator that round-robins and removes unhealthy backends.

**Open source:** [`nginx/nginx`](https://github.com/nginx/nginx); [`envoyproxy/envoy`](https://github.com/envoyproxy/envoy).

**Interview:** "L4 vs L7 load balancing?" / "How does a CDN reduce latency?"

**Checklist:** ☐ set up health checks ☐ choose LB algorithm per workload ☐ cache at the edge

---

## Part 8 — Databases

### Chapter 45 — SQL & the Relational Model

**Concept:** The relational model; SQL (SELECT/JOIN/GROUP BY/subqueries); PostgreSQL vs MySQL.

**Prereqs:** none.

**Diagram:** An ER diagram of a few tables with FK relationships.

**Example:** `SELECT u.name, COUNT(o.id) FROM users u JOIN orders o ON ... GROUP BY u.name`.

**Exercises:** (1) Write a query with a self-join. (2) Explain a LEFT JOIN vs INNER JOIN result.

**Mini project:** A normalized schema + query set for an e-commerce store.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres).

**Interview:** "INNER vs LEFT JOIN?" / "How would you find duplicate rows?"

**Checklist:** ☐ write all join types ☐ group/aggregate correctly ☐ design a normalized schema

---

### Chapter 46 — Schema Design, Normalization & Indexing

**Concept:** Normal forms, denormalization trade-offs, B-tree indexes, composite indexes, and query planning (EXPLAIN).

**Prereqs:** Ch 45.

**Diagram:** A B-tree index over a column; a query plan tree from EXPLAIN.

**Example:** `CREATE INDEX ... ON orders(user_id, created_at)`; reading `EXPLAIN ANALYZE`.

**Exercises:** (1) Normalize a table to 3NF. (2) Design the optimal index for a given query and verify with EXPLAIN.

**Mini project:** Add indexes to a slow schema and measure the query-speed change.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres) planner.

**Interview:** "When to denormalize?" / "Why does a composite index order matter?"

**Checklist:** ☐ reach 3NF ☐ read EXPLAIN ☐ index for real query patterns

---

### Chapter 47 — ACID, Transactions & Isolation

**Concept:** Atomicity/Consistency/Isolation/Durability; transactions; isolation levels (read committed, repeatable read, serializable) and anomalies.

**Prereqs:** Ch 45.

**Diagram:** A transaction state diagram; a phantom-read example under two isolation levels.

**Example:** `BEGIN; ... COMMIT;` with `SET TRANSACTION ISOLATION LEVEL ...`.

**Exercises:** (1) Reproduce a lost update and fix it with a lock. (2) Explain what each isolation level prevents.

**Mini project:** A money-transfer service with transactions that pass a concurrency test.

**Open source:** [`postgres/postgres`](https://github.com/postgres/postgres) (MVCC).

**Interview:** "What anomalies does each isolation level allow?" / "How does MVCC work?"

**Checklist:** ☐ name the ACID properties ☐ pick an isolation level deliberately ☐ keep transactions short

---

### Chapter 48 — NoSQL: MongoDB, Cassandra & DynamoDB

**Concept:** Document, wide-column, and key-value/Dynamo-style stores; consistency models; when NoSQL beats SQL.

**Prereqs:** Ch 45.

**Diagram:** A document vs wide-column vs key-value data layout comparison.

**Example:** a MongoDB document; a Cassandra table with partition key; a DynamoDB `GetItem`.

**Exercises:** (1) Model a feed in Cassandra with the right partition key. (2) Explain DynamoDB's eventual consistency vs strong reads.

**Mini project:** A session store on DynamoDB and a product catalog on MongoDB.

**Open source:** [`mongodb/mongo`](https://github.com/mongodb/mongo); [`scylladb/scylladb`](https://github.com/scylladb/scylladb).

**Interview:** "When NoSQL over Postgres?" / "What is the CAP implication of DynamoDB?"

**Checklist:** ☐ choose a store per access pattern ☐ design a partition key ☐ know the consistency knob

---

### Chapter 49 — Redis, Elasticsearch, Neo4j & Vector Databases

**Concept:** Caching (Redis), full-text search (Elasticsearch), graphs (Neo4j), and vector similarity (Qdrant/Milvus).

**Prereqs:** Ch 45, Ch 48.

**Diagram:** A Redis data-structures cheat sheet; a graph of nodes/edges; a vector nearest-neighbor diagram.

**Example:** `SET k v EX 60`; an ES `match` query; a Cypher `MATCH (a)-[:FRIEND]->(b)`; a Qdrant HNSW search.

**Exercises:** (1) Cache an expensive query in Redis with TTL. (2) Write a Cypher query for friends-of-friends. (3) Run a vector similarity search.

**Mini project:** A hybrid search endpoint combining full-text + vector ranking.

**Open source:** [`redis/redis`](https://github.com/redis/redis); [`qdrant/qdrant`](https://github.com/qdrant/qdrant).

**Interview:** "Redis persistence vs pure cache?" / "When graph DB over SQL?"

**Checklist:** ☐ set sensible TTLs ☐ know inverted-index basics ☐ run a vector search

---

**Exit criteria:** Build one non-trivial CLI/service touching files, network, and a database.
