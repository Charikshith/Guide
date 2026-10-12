---
name: flowchart
description: Map any step-by-step process or decision flow as a clean, interactive flowchart page — proper start/end, step, decision (Yes/No) and input/output shapes, loops, optional swimlanes for who-does-what, auto-layout so arrows never tangle, "Try a path" buttons that trace a scenario through the chart, a Play walkthrough, light and dark mode, and an optional handwritten notebook style when asked. Use this whenever the user types /flowchart, or asks for a flowchart, process map, decision tree, workflow diagram, approval flow, "what happens if…", troubleshooting flow, or "map out the steps of X", even if they don't say "flowchart". For a general explainer visual (cycles, layers, anatomy, scenes) use /visualize instead.
---

# /flowchart — any process → a flowchart you can walk through

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent, a
lede, fact chips, **the flowchart** (drawn automatically by a built-in layout engine), "Try a
path" scenario buttons, a shape legend, a numbered reading guide with a Play walkthrough,
3 takeaways and a footnote. Light + dark mode, no external assets.

**You describe the flow as data; the engine draws it.** Never hand-place shapes or arrows —
the engine ranks the steps, keeps the main path straight down, routes branches around boxes,
draws loops as dashed return arrows, sizes every shape to its text, and fits the canvas.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).

## Usage
`/flowchart <process or decision>` — optional extras: audience, "with swimlanes" (who does
what), depth ("simple", "detailed"), language.
Defaults: general audience, 6–14 shapes, no lanes unless several people/systems hand off work.

If the user gives only `/flowchart` with no topic, ask for the topic in one short line.

## Step 1 — Understand the process
Write (for yourself) the real sequence: where it starts, every decision point and its
outcomes, every way it can end, and any "go back and try again" loops. Then decide:
- **Main path** = the most common / successful route. It will run straight down the middle.
- **Decisions** = only real yes/no (or few-way) questions. Phrase as a question ending in "?".
- **Ends** = every distinct outcome (success, failure, escalation…), each its own end shape.
- **Lanes** only if ≥ 2 actors hand work to each other (customer / shop / bank).

Fact-check: the order of steps, what each decision really depends on, and every outcome
must be true. Don't invent steps, rules or numbers; say "simplified" in the footnote.

## Step 2 — Write the flow spec (JSON)
Put it at the end of the content in `<script type="application/json" id="flow-spec">`.

```json
{
  "lanes": [{"id": "you", "label": "You"}, {"id": "bank", "label": "Bank"}],   // optional
  "nodes": [
    {"id": "start", "type": "start", "label": "Click Pay"},
    {"id": "enter", "type": "io", "label": "Enter card details", "sub": "number, expiry, CVV", "icon": "coin", "step": 1},
    {"id": "valid", "type": "decision", "label": "Details look valid?", "step": 2},
    {"id": "fix",   "type": "process", "label": "Show an error", "icon": "alert", "color": "c4", "step": 2},
    {"id": "ok",    "type": "end", "label": "Order confirmed", "color": "c2", "step": 3},
    {"id": "no",    "type": "end", "label": "Payment declined", "color": "c4"}
  ],
  "edges": [
    {"from": "start", "to": "enter"},
    {"from": "enter", "to": "valid"},
    {"from": "valid", "to": "ok",  "label": "Yes"},
    {"from": "valid", "to": "fix", "label": "No"},
    {"from": "fix",   "to": "enter", "label": "try again"}
  ],
  "paths": [
    {"name": "Smooth payment", "color": "c2", "nodes": ["start", "enter", "valid", "ok"], "note": "One sentence on what happens."}
  ]
}
```
(Real JSON has no `//` comments.)

**Style** (optional, top level — **off by default**): the clean style is the default; leave
`style` out. Add `"style": "handwritten"` **only when the user asks for it** — they say
handwritten, notebook style, or "like my class notes". Don't switch to it on your own because
the topic is a school or revision topic. It turns the whole page into a notebook page — ruled
paper, red margin, handwriting fonts (Kalam / Caveat), wobbly pen lines, highlighter fills,
circled step numbers and sticky-note takeaways. Nothing else changes: same
spec, layout, paths and walkthrough. It loads the two fonts from Google Fonts; offline it
falls back to a system handwriting font. Leave it out for the clean default style.

**Nodes**
| Field | Meaning |
|---|---|
| `id` | short unique name, used by edges and paths |
| `type` | `start`, `end` (pills), `process` (box), `decision` (diamond), `io` (parallelogram: data in/out, user input, a message or document) |
| `label` | ≤ 5 words; decisions are questions ("Bank approves?") |
| `sub` | optional second line, ≤ 5 words (not for decisions) |
| `icon` | optional, process/io only — a name from the icon list below |
| `color` | optional `c1`–`c5`. Defaults: start/end `c2`, process `c1`, decision `c3`, io `c5`. Use `c4` for failure / error ends and error steps, `c2` for success |
| `step` | optional number linking the shape to reading-guide step N (several shapes may share a step; the badge goes on the first) |
| `lane` | lane id, required on every node when `lanes` is used |

**Edges** `{"from", "to", "label"?, "color"?, "step"?}`
- **List the main / "Yes" branch FIRST** for every node — the first edge out of a node is the one
  that runs straight down. Later edges branch to the side.
- Label **every** edge out of a decision ("Yes" / "No", or the actual options). Yes-like labels
  turn green, No-like labels turn red automatically.
- An edge back to an earlier step becomes a dashed loop on the side — label it ("try again").

**Paths** (2–4 recommended): realistic scenarios through the chart, e.g. happy path, a
retry, a failure. `nodes` must follow existing arrows in order (a loop may repeat nodes).
Each gets a button; clicking it lights the route and sends a dot along it.

Keep it readable: ≤ 14 shapes, ≤ 4 decisions, ≤ 3 lanes. Bigger process → split it, or
summarise a sub-process as one step ("Bank fraud checks") and mention it in the footnote.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text),
`{{HEADLINE}}` (may contain `<span class="accent">`), `{{FORM}}` (e.g. `Flowchart · Decision
flow`, `Flowchart · Swimlanes`), `{{LEDE}}` (≤ 25 words), and put this where
`<!-- CONTENT GOES HERE -->` is:

```html
<ul class="chips"><li><b>3</b> checks before money moves</li><li><b>2</b> ways it can end</li></ul>
<figure class="stage">
  <svg id="flow" class="fc" role="img" aria-label="one-sentence summary of the flow"></svg>
  <figcaption>Follow the arrows from top to bottom. Diamonds are questions; dashed arrows loop back.</figcaption>
</figure>
<p class="scroll-hint">← swipe the chart →</p>      <!-- shows on phones only -->
<div class="paths" id="flow-paths"></div>          <!-- filled from "paths" -->
<ul class="legend" id="flow-legend"></ul>          <!-- filled with the shapes used -->
<h2>How to read it</h2>
<ol class="steps"><li class="c1"><b>Enter details</b><span>One or two sentences.</span></li>…</ol>
<h2>Key takeaways</h2>
<div class="cards"><div class="card c1"><svg><use href="#i-idea"/></svg><b>Insight</b><p>…</p></div>…</div>
<p class="note">Simplified: …</p>
<script type="application/json" id="flow-spec">{ … }</script>
```
- Reading guide: one `<li>` per `step` number used in the spec, in order; the `li` colour
  class matches that step's shape colour. Each text must make sense on its own — the Play
  walkthrough shows it as a caption while lighting up that step's shapes and arrows.
- Takeaways: the insight, a common mistake (`i-alert`), and a "so what".
- Don't add CSS, don't draw SVG by hand, don't edit the template's scripts.

**Icons** (`"icon": "…"`): `sun cloud rain drop wave wind leaf sprout tree mountain fire thermo
bolt atom flask cell dna heart eye user users home factory bank truck globe flag laptop phone
server db cpu code gear link lock key shield search mail chat coin cart chart target idea doc
book clock cal star check alert x loop`. Unknown names fail validation.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium);
otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py flow.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py flow.html --out <dir>
```
It FAILS on bad JSON, unknown ids or icons, overlapping shapes, edge labels on shapes,
clipped/overlapping text, JavaScript errors and sideways scrolling. It WARNS on dead ends,
unlabeled decision branches, unreachable shapes, paths that don't follow arrows, arrows
cutting through shapes, and step-count mismatch. It renders `*_light.png`, `*_dark.png`,
`*_mobile.png` — **look at them**. If an arrow cuts through a shape or the chart sprawls:
reorder edges (main branch first), merge minor steps, or move a node to another lane.

## Step 5 — Deliver
- Save as `examples/005-flowchart/<topic-slug>-flowchart.html` (unless the user or project names
  another place — never make a new top-level folder) and deliver it per the environment
  (publish as an artifact / present the file).
- If the user wants an image, also give the light PNG.
- In chat, at most two lines: what the flow covers and an offer (e.g. "want swimlanes for
  who does what, or a zoom into the bank's checks?"). Don't repeat the page.

## Quality bar (self-check before delivering)
- The main path reads straight down; a newcomer can follow it in 10 seconds.
- Every decision is a real question with every way out labelled; every path ends in an end shape.
- Loops are real "go back" steps, not decoration. No arrow cuts through a shape.
- "Try a path" scenarios are realistic and cover success and at least one failure.
- Facts are right; simplifications are named in the footnote.
