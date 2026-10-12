---
name: diagram
description: Draw a technical or educational box-and-arrow diagram as a clean, interactive page — system and software architecture, network topology, data pipelines, how the parts of something connect, or a concept diagram such as "parts of a cell and how they interact" — with shapes per kind (service, database, queue, person, outside cloud, document), nested group boxes (VPC, Frontend, Nucleus), auto-layout so arrows never tangle, hover to see a part's connections, click a group to focus, "Try a flow" buttons that send a dot along a route, a Play walkthrough, light and dark mode, and an optional handwritten notebook style when asked. Use this whenever the user types /diagram, or asks for an architecture diagram, system diagram, network diagram, component diagram, pipeline diagram, "draw how X is structured / how the parts of X connect", even if they don't say "diagram". For steps and decisions use /flowchart; for an idea tree use /mindmap; for an illustrated explainer or scene use /visualize.
---

# /diagram — any structure → a box-and-arrow diagram you can explore

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent, a
lede, fact chips, **the diagram** (drawn automatically by a built-in layout engine), "Try a
flow" buttons, a shape legend, a numbered reading guide with a Play walkthrough, 3 takeaways
and a footnote. Light + dark mode, no external assets.

**You describe the structure as data; the engine draws it.** Never hand-place boxes or arrows —
the engine lays out each group as its own block, keeps members inside their group box, routes
arrows around every box, puts labels in clear space, sizes shapes to their text and fits the canvas.

**Which skill?** `/diagram` = what the parts are and how they connect (boxes + arrows, optionally
grouped). `/flowchart` = the order of steps and decisions. `/mindmap` = a tree of ideas with no
flow. `/visualize` = a rich illustrated explainer or scene.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).

## Usage
`/diagram <system or concept>` — optional extras: audience, direction ("top to bottom"), depth
("simple", "detailed"), language, "handwritten".
Defaults: general audience, 6–14 boxes, left-to-right, groups only where there are real zones.

If the user gives only `/diagram` with no topic, ask for the topic in one short line.

## Step 1 — Understand the structure
Write (for yourself) the real parts and how they connect: what talks to what, in which direction,
what carries what (a request, data, energy, a message). Then decide:
- **Boxes** = the real parts, ≤ 5 words each, one box per thing. Aim for 6–14; hard cap 18.
- **Groups** = real zones the parts belong to (Client / Edge / Backend / Data, VPC, Nucleus,
  Frontend). A group needs ≥ 1 box; groups may nest. Don't group for decoration.
- **Arrows** = real relationships, drawn in the direction the request, data or material moves.
  Label them with what flows ("API calls", "copied"). One arrow per relationship.
- **Direction**: `LR` (default) reads like a pipeline. Use `TB` for tall layered things (a
  request going down through tiers, a production line, a body or cell). Pick the one that gives
  a compact picture; wide diagrams shrink their text.

Fact-check: every part, link and direction must be true. Don't invent parts, products or
numbers; say "simplified" in the footnote and name what you left out.

## Step 2 — Write the spec (JSON)
Put it at the end of the content in `<script type="application/json" id="dg-spec">`.

```json
{
  "direction": "LR",
  "groups": [
    {"id": "edge", "label": "Edge", "color": "c1", "step": 2, "note": "optional sentence shown when the group is focused"},
    {"id": "inner", "label": "Inner zone", "parent": "edge"}
  ],
  "nodes": [
    {"id": "user", "kind": "user", "label": "Visitor", "sub": "browser or app", "step": 1},
    {"id": "lb", "kind": "service", "label": "Load balancer", "sub": "spreads requests", "icon": "link", "group": "edge", "step": 2},
    {"id": "db", "kind": "database", "label": "Database", "group": "edge", "step": 3}
  ],
  "edges": [
    {"from": "user", "to": "lb", "label": "requests"},
    {"from": "lb", "to": "db", "label": "queries", "style": "dashed"}
  ],
  "flows": [
    {"name": "Open a page", "color": "c2", "nodes": ["user", "lb", "db"], "note": "One sentence on what happens."}
  ]
}
```
(Real JSON has no `//` comments.)

**Style** (optional, top level — **off by default**): the clean style is the default; leave
`style` out. Add `"style": "handwritten"` **only when the user asks for it** — they say
handwritten, notebook style, or "like my class notes". Don't switch to it on your own because
the topic is a school or revision topic, and keep it out of default markup. It turns the page into a
notebook page — ruled paper, red margin, handwriting fonts (Kalam / Caveat), wobbly pen lines,
highlighter fills and sticky-note takeaways. Nothing else changes: same spec, layout, flows and
walkthrough. It loads the two fonts from Google Fonts; offline it falls back to a system handwriting font.

**Nodes**
| Field | Meaning |
|---|---|
| `id` | short unique name, used by edges, flows and groups |
| `label` | ≤ 5 words |
| `sub` | optional second line, ≤ 5 words |
| `kind` | `service` (default, rounded box), `database` (cylinder), `queue` (pipe), `user` (person), `external` (cloud: something outside your control), `document` (page with folded corner: a file, message or copy), `ellipse` (a concept or part, no icon) |
| `icon` | optional, `service`/`document`/`database`/`queue` only — a name from the icon list below |
| `color` | optional `c1`–`c5`. Defaults: service `c1`, database `c2`, queue `c3`, user `c4`, external `c5`, document `c3`, ellipse `c1`. Colour carries meaning — be consistent |
| `group` | optional group id the box lives in |
| `step` | optional number linking the box to reading-guide step N (several boxes may share a step; the badge goes on the first) |

**Groups** `{"id", "label", "parent"?, "color"?, "step"?, "note"?}` — `parent` nests a group in
another; `color` tints it; `note` is shown under the diagram when the group is clicked. Groups
are laid out as whole blocks, so they never overlap; a box listed in a group is always inside it.

**Edges** `{"from", "to", "label"?, "style"?, "both"?, "color"?, "step"?}`
- `from`/`to` are **node** ids (never group ids).
- `style`: `solid` (default), `dashed` (optional / indirect / asynchronous), `thick` (the main flow).
- `both: true` puts arrowheads on both ends.
- Label arrows with what flows (≤ 3 words). In a diagram with more than 8 arrows, label every one.

**Flows** (2–4 recommended; `paths` also works): realistic scenarios, each a list of `nodes` that
follow existing arrows in order (reverse only along `both` arrows). Each gets a "Try a flow" button
that lights the route and sends a dot along it. Use a normal case, a fast path and a failure or
slow path where they exist.

Keep it readable: ≤ 14 boxes ideally, ≤ 5 groups, ≤ 3 nesting levels, ≤ ~18 arrows.
Bigger system → split it, or summarise a sub-system as one box and mention it in the footnote.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text),
`{{HEADLINE}}` (may contain `<span class="accent">`), `{{FORM}}` (e.g. `Diagram · Architecture`,
`Diagram · Biology`), `{{LEDE}}` (≤ 25 words), and put this where `<!-- CONTENT GOES HERE -->` is:

```html
<ul class="chips"><li><b>9</b> parts</li><li><b>4</b> zones</li></ul>
<figure class="stage">
  <svg id="dg" class="dg" role="img" aria-label="one-sentence summary of the structure"></svg>
  <figcaption>Arrows show where a request goes next. Click a dashed zone to focus on it.</figcaption>
</figure>
<p class="scroll-hint">← swipe the diagram →</p>      <!-- shows on phones only -->
<div class="paths" id="dg-flows"></div>               <!-- filled from "flows" (+ a hover hint) -->
<ul class="legend" id="dg-legend"></ul>               <!-- filled with the shapes used -->
<h2>How to read it</h2>
<ol class="steps"><li class="c1"><b>Visitor asks</b><span>One or two sentences.</span></li>…</ol>
<h2>Key takeaways</h2>
<div class="cards"><div class="card c1"><svg><use href="#i-idea"/></svg><b>Insight</b><p>…</p></div>…</div>
<p class="note">Simplified: …</p>
<script type="application/json" id="dg-spec">{ … }</script>
```
- Reading guide: one `<li>` per `step` number used in the spec, in order; the `li` colour class
  matches that step's box colour. Each text must make sense on its own — the Play walkthrough
  shows it as a caption while lighting up that step's boxes and arrows.
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
.venv\Scripts\python <skill-dir>/scripts/validate.py diagram.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py diagram.html --out <dir>
```
It FAILS on bad JSON, unknown node / group / icon ids, overlapping boxes, a box outside its group,
groups overlapping other groups (unless nested), edge labels on boxes, clipped or overlapping text,
JavaScript errors and sideways scrolling. It WARNS on arrows cutting through boxes or group titles,
too many boxes (> 18), unlabeled arrows in a dense diagram, flows that don't follow arrows and
step-count mismatch. It renders `*_light.png`, `*_dark.png`, `*_mobile.png` — **look at them**.
If the picture is too wide or tangled: switch `direction`, merge minor boxes, split into two
diagrams, or move a box to another group.

## Step 5 — Deliver
- Save as `examples/004-diagram/<topic-slug>-diagram.html` (unless the user or project names
  another place — never make a new top-level folder) and deliver it per the environment
  (publish as an artifact / present the file).
- If the user wants an image, also give the light PNG.
- In chat, at most two lines: what the diagram covers and an offer (e.g. "want it top-to-bottom, or
  a zoom into the data layer?"). Don't repeat the page.

## Quality bar (self-check before delivering)
- You can read the diagram's story in 10 seconds: groups are real zones, arrows follow the flow.
- No arrow cuts through a box; every group clearly encloses its members; labels sit clear of boxes.
- Arrow labels say what moves; dashed means optional / indirect, thick means the main flow, and the legend says so.
- "Try a flow" scenarios are realistic and cover a normal case plus a fast or failure path where one exists.
- Facts are right; simplifications are named in the footnote. Handwritten style only if asked.
