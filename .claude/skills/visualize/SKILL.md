---
name: visualize
description: Turn any concept, process or system into one rich, self-contained visual explainer page — an illustrated SVG scene or diagram (flow, cycle, layers, anatomy, timeline, comparison, network, tree, cause→effect or scale) with icons, depth, gentle motion showing what moves, hover-to-highlight steps, a numbered reading guide and key takeaways, in light and dark mode. Use this whenever the user types /visualize, or asks to visualize, illustrate, diagram, map out, "draw", "show me how X works", or "explain X visually", even if they don't say "visualize". Not for charts of a dataset (use a charting/dataviz skill) or notebook-style notes (use /handwritten).
---

# /visualize — any concept → one rich, clear visual

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent,
a one-line lede, fact chips, **one main illustrated SVG**, a legend, a numbered reading
guide that lights up the matching part of the visual, 3 takeaways with icons, and a footnote.
Light + dark mode, no external assets.

It must look **designed, not plain**: icons on every main element, soft depth, a scene or
grouping background, and motion on the path where something actually moves. And it must stay
**true**: the visual shows the real mechanism — what moves where, what causes what, what sits
inside what.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).

## Usage
`/visualize <concept or process>` — optional extras: audience (kid, student, engineer, exec),
form ("as a cycle", "as layers"), depth ("simple", "detailed"), language.
Defaults: general audience, the best-fitting form, ~6–10 elements, English.

If the user gives only `/visualize` with no topic, ask for the topic in one short line.

## Step 1 — Understand, then pick ONE form and a visual style
First write (for yourself): *what is the one thing the reader should SEE that text can't show?*

| The concept is mainly… | Form | Layout |
|---|---|---|
| ordered steps, a pipeline, a request path | **Flow** | left→right (≤ 6 per row) or top→down; snake to a 2nd row if needed |
| something that repeats / feeds back | **Cycle** | nodes round a loop, arrows clockwise, centre = what drives it |
| levels that build on each other | **Layers** | stacked full-width bands, bottom = foundation; side arrows for flow between layers |
| parts of one object or body | **Anatomy** | one central simplified shape + leader lines to labels on both sides |
| change over time | **Timeline** | horizontal axis, dated ticks, alternating labels above/below |
| A vs B (vs C) | **Comparison** | aligned columns, same rows across, differences coloured |
| many actors and links | **Network / hub** | hub-and-spoke or clusters; edge labels say what flows |
| a whole broken into kinds | **Tree** | root top, ≤ 3 levels, ≤ 5 children per node |
| causes producing an effect | **Cause → effect** | causes grouped in zones on the left, arrows converge on the effect |
| sizes that differ hugely | **Scale** | bars/circles to scale (log scale stated if used) — only real numbers |

Then choose the **visual style**:
- **Scene** — the topic happens in the physical world (weather, body, machine, city, ecosystem,
  supply chain). Draw a simple illustrated setting (sky, ground, sea, body outline, building)
  with `.wash` shapes and `.mass` blobs, and put the labelled cards **where things happen**.
  Physical position must be right (rain falls on land, the heart sits left of centre, …).
- **System** — abstract topics (software, law, finance, ideas). Use cards with icon chips,
  `.zone` group regions, and clear lanes.

Combine at most two forms. If the user named a form, use it unless it would mislead — then
say why in the footnote.

## Step 2 — Plan the content (before any SVG)
- **Title** 2–6 words; **headline** = the title with the key word(s) in `<span class="accent">`.
  **Eyebrow** = `Visualize · <Form>`. **Lede** ≤ 25 words: the big idea.
- **Chips**: 2–4 short facts under the lede (counts, the driver, the one-liner). Real facts only.
- **6–12 elements** in the visual. More than 12 → group into zones or cut.
- **Every main element = a card** with an icon chip, a title (≤ 3 words) and a sub-line
  (≤ 5 words). Pick the icon that names the thing (see icon list).
- **Numbered badges** (3–7) on the cards in reading order. Each badge gets a matching
  `<li>` in the reading guide. Badge colour = the card's colour.
- **Edge labels** say what moves: "DNS query", "glucose", "wind carries clouds".
- **Colour = meaning**, max 4 families (`c1`–`c5`), explained by the legend. Same colour for
  the same kind of thing (e.g. amber = energy in, blue = water down).
- **Motion**: the 1–3 paths where something really travels get `.flow` dashes and/or a
  `.particle`. Static relationships stay static. Never animate decoration for its own sake
  (exception: a slow `.spin` sun / `.pulse` heart that IS the driver).
- **3 takeaways** with icons: the insight (`i-idea`/`i-loop`), a common mistake (`i-alert`),
  a "so what" (`i-target`/topic icon).
- **Footnote**: simplifications, "not to scale", what was left out.

Fact-check: names, numbers, order of steps, physical positions and the direction of every
arrow must be correct. Never invent statistics; approximate numbers get "≈" and a footnote.
If the topic is contested, show the main views side by side instead of picking one.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text, used in
the tab), `{{HEADLINE}}` (may contain `<span class="accent">`), `{{FORM}}`, `{{LEDE}}`, and put
content where `<!-- CONTENT GOES HERE -->` is. Don't rewrite the CSS or the `<defs>`.

Page skeleton (in this order):
```html
<ul class="chips"><li><b>4</b> stages</li><li>Powered by <b>the Sun</b></li></ul>
<figure class="stage">
  <svg viewBox="0 0 960 600" role="img" aria-label="one-sentence description">…</svg>
  <figcaption>What the reader is looking at. Point at a step below to highlight it.</figcaption>
</figure>
<p class="scroll-hint">← swipe the diagram →</p>
<ul class="legend"><li><span class="sw c3"></span>Energy in</li>…</ul>
<h2>How to read it</h2>
<ol class="steps"><li class="c3"><b>Evaporation</b><span>One or two sentences.</span></li>…</ol>
<h2>Key takeaways</h2>
<div class="cards"><div class="card c1"><svg><use href="#i-idea"/></svg><b>Insight</b><p>…</p></div>…</div>
<p class="note">Simplified: …</p>
```

### Walkthrough player (automatic)
The template's script builds a **play / pause, back / next, progress bar and caption** inside
the stage from `ol.steps` — no markup to add. Pressing play shows step 1, 2, 3 … in turn: it
highlights every `[data-step]` group for that step, dims the rest, and shows the step's
`<b>` title and `<span>` text as the caption (time per step scales with its word count).
So: put each step's text in `<li><b>Title</b><span>Text</span></li>`, keep each step's text
self-contained (it is read on its own), and wrap **everything** that belongs to a step in
its `data-step` group — otherwise the walkthrough highlights the wrong thing.

### The card (use for every main element)
```html
<g data-step="1">                                   <!-- everything for step 1 goes in here -->
  <g class="lift">                                  <!-- soft shadow -->
    <rect class="node c3" x="560" y="404" width="250" height="68" rx="16"/>
    <circle class="chip c3" cx="594" cy="438" r="20"/>                 <!-- x+34, y+34 -->
    <use href="#i-sun" class="ico on" x="582" y="426" width="24" height="24"/>  <!-- chip −12 -->
    <text class="t" x="624" y="434">Evaporation</text>                 <!-- x+64, y+30 -->
    <text class="t sub" x="624" y="455">Sun heats water → vapour</text> <!-- x+64, y+51 -->
  </g>
</g>
<g class="badge c3" transform="translate(560,404)"><circle r="13"/><text text-anchor="middle" dy="4.5">1</text></g>
```
Card width = 64 + longest line × 9px (title) or × 7.5px (sub) + 20. Height 68 (two lines) or 52
(title only: text at y+32). A big hero card may use `t big`.

### SVG vocabulary (classes only — no hard-coded colours, so dark mode works)
| Need | Markup |
|---|---|
| Card / box | `<rect class="node c1" … rx="16"/>` (gradient fill + coloured border) |
| Strong box | `<rect class="node solid c1" …/>` + `<text class="t on">` |
| Soft shadow | wrap in `<g class="lift">` |
| Icon chip | `<circle class="chip c1" r="20"/>` + `<use href="#i-…" class="ico on" width="24" height="24"/>` |
| Bare icon | `<use href="#i-tree" class="ico c2" x y width="28" height="28"/>` |
| Group region | `<rect class="zone" … rx="18"/>` + a `.t.small` label in its top-left |
| Scene fill (sky, land, sea, body) | `<path class="wash c1" d="…"/>` (fades down) / `wash up c1` (fades up); draw its visible outline as a separate `edge` path |
| Solid blob (cloud, organ, object) | `<circle class="mass" …/>`, darker: `mass shade`; wrap in `.lift` |
| Arrow | `<path class="edge c1" d="M… C…" marker-end="url(#arr-c1)"/>` (grey: `edge` + `#arr`) |
| Moving arrow | add `flow` (marching dashes); `thick` for the main path; `dash` for optional/return |
| Travelling dot | `<circle class="particle c1" r="4.5"><animateMotion dur="3s" repeatCount="indefinite"><mpath href="#pathId"/></animateMotion></circle>` — give the path an `id`; stagger extra dots with a **negative** `begin="-1.5s"` (positive delays park the dot at 0,0) |
| Slow driver motion | `class="spin"` (rotating rays) / `class="pulse"` (beating) |
| Label | `<text class="t" …>`; `t sub`, `t small`, `t big`, `t c1`…, `t mono` |
| Label over a scene/line | add `halo` (outline in the background colour) |
| Leader line | `<path class="leader" d="M x1 y1 L x2 y2"/>` + `<circle class="dot" r="3"/>` at the part |
| Badge | `<g class="badge c1" transform="translate(x,y)"><circle r="13"/><text text-anchor="middle" dy="4.5">1</text></g>` |
| Step highlight | wrap each step's elements in `<g data-step="N">`; shared parts `data-step="2 3"` |

**Icons** (`#i-…`): nature/science `sun cloud rain drop wave wind leaf sprout tree mountain fire
thermo bolt atom flask cell dna heart eye` · people/places `user users home factory bank truck
globe flag` · tech `laptop phone server db cpu code gear link lock key shield search mail chat`
· business/ideas `coin cart chart target idea doc book clock cal star` · status `check alert x loop`.
Use only these names; the validator fails on a missing id.

### Geometry rules
- `viewBox` width **960**; height as needed (≈ 420–640). Keep 24px padding inside it.
- A scene background can fill the whole viewBox (`<rect class="wash c1" … rx="14" opacity=".7"/>`).
- ≥ 16px between labels; arrows start/end 4–6px off a card edge; never cross a label or card.
- Badges on the top-left corner of their card. Grid of 8. Equal gaps between siblings.
- Draw order: scene → zones → edges/particles → cards → badges (later = on top).
- Phones: the stage keeps a 640px minimum width and scrolls inside its card; the reading
  guide carries the same information as text.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium);
otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py visual.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py visual.html --out <dir>
```
It FAILS on placeholders, external resources, missing icon/marker/path ids, sideways
scrolling, and labels that are clipped or overlap. It WARNS on hard-coded colours, no icons,
no motion, no `data-step`, and badge-vs-step mismatch. It renders `*_light.png`, `*_dark.png`,
`*_mobile.png`. **Look at the light AND dark PNGs** and fix anything wrong — text spilling
out of a card, arrows crossing labels, a shape vanishing in dark mode, empty or lopsided areas.

## Step 5 — Deliver
- Save as `examples/001-visualize/<topic-slug>-visual.html` (unless the user or project names
  another place — never make a new top-level folder) and deliver it per the environment
  (publish as an artifact / present the file).
- If the user wants an image, also give the light PNG.
- In chat, at most two lines: what the visual shows and an offer for a follow-up form
  (e.g. "want it as a timeline, or a zoom into step 3?"). Don't repeat the page.

## Quality bar (self-check before delivering)
- 5-second test: a newcomer sees the main idea before reading any paragraph.
- Looks designed: icons on main elements, depth, a scene or zones, motion on the real flow.
- Every arrow points the true way and most say what moves; physical positions are right.
- Reading-guide numbers match the badges; hovering a step or pressing play lights up the
  right parts, step by step.
- ≤ 4 colours, each with one meaning; works in dark mode; no text outside its card.
- Nothing invented. Simplifications are named in the footnote.
