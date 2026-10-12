---
name: explodedview
description: Break any object into its parts and show how they fit — the classic exploded assembly drawing, with the parts pulled apart along an axis (isometric or front view), dashed assembly lines, numbered balloons with leader lines, a numbered parts list (name, quantity, material or role), and an interactive Assemble / Explode slider with a "Play assembly" button that flies the parts in one by one in the right order, synced with a reading guide and walkthrough. Light and dark mode, phone-friendly, prints light in the exploded state with the parts list, and an optional handwritten notebook style when asked. Use this whenever the user types /explodedview, or asks for an exploded view, exploded diagram, "break X into its parts", "show how X is put together / assembled", "what is inside X", a teardown, an assembly drawing or a parts breakdown of a physical object (pen, torch, phone, PC, engine, lamp, bicycle part), even if they don't say "exploded". For a process use /flowchart; for an idea map use /mindmap; for a general explainer visual use /visualize.
---

# /explodedview — an object → its parts pulled apart, and how they fit

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent, a one-line lede,
chips, **one SVG with the parts drawn as an exploded assembly**, an **Assemble ↔ Explode** control bar
(slider 0–100 %, *Assemble*, *Explode*, *Play assembly*), a legend, a **parts list**, the assembly steps
(reading guide with a Play walkthrough), 3 takeaways and a footnote. Light + dark mode, no external assets
(Google Fonts only in the optional handwritten style).

It must stay **true**: the parts, their names, the order they go together and what sits inside what must be
correct. When assembled the parts must read as ONE object; when exploded they must be cleanly separated.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).
**Printing is always light** (white paper, dark ink) and shows the **exploded** drawing plus the parts list;
the template does this for you and hides the controls and the toggle.

## Usage
`/explodedview <object>` — optional extras: view ("isometric", "side view"), level ("simple", "detailed"),
audience, `handwritten`, language.
Defaults: the common version of the object, 6–10 parts, isometric for blocky things (boxes, boards, layers), side
view for long round things (pens, torches), English.

If the user gives only `/explodedview` with no object, ask for the object in one short line.

## Step 1 — Understand the object
- **Which version?** "A click pen", "a Maglite-style torch with 2 AA cells", "a smartphone". Say it in a chip and the
  footnote; real products differ.
- **One explode axis per object.** Parts are pulled apart along ONE straight line, the way they are assembled: straight up
  (stacks and layers: phone, PC case, lamp) or along the length (pen, torch, bolt). ALL parts sit on that centre line, in
  assembly order, with a dash-dot centre line through them. Only small side parts (a clip, a button, a screw) may step a
  short distance off the axis, with a short dashed guide to the part they fit on (`data-mate`). Parts that slide *inside*
  another part (a refill, a spring) are pulled out along the axis past the end of the body, never parked above or below it.
- **Real proportions.** Look up or recall the real size (a click pen is ≈ 140 mm long and 10 mm wide, its refill ≈ 105 mm, its
  spring ≈ 15 mm; a phone is ≈ 147 x 71 x 8 mm) and draw in one scale (px per mm). State the reference size in a chip and the
  footnote. Thin layers may be thickened for legibility: say so. Never draw a tiny cone and a giant refill.
- **Parts are drawn as real parts, not flat boxes**: cylinders get shading, end caps and threads; springs a helix; flat
  electronics a board outline with chips, connectors and a label; glass a screen; frames their buttons and ports. Think
  product-manual illustration (IKEA, iFixit, a parts catalogue).
- **List 6–10 parts** (hard cap ~14; group screws and washers into one row with a quantity). Put them in
  **assembly order** (what you would do first … last). Check each name and the order against how the thing is
  really built. If you are not sure of a detail, leave it out or say so in the footnote.
- **Colour = kind of thing**, max 4 families (`c0` grey, `c1`–`c5`): e.g. metal `c0`, plastic body `c1`,
  electronics `c2`, power `c3`. Explain them in a legend.

## Step 2 — Plan the page
- **Title** 2–5 words ("Inside a ballpoint pen"); headline = the title with a key word in `<span class="accent">`;
  eyebrow `Exploded view · <Everyday object|Technology|…>`; lede ≤ 25 words.
- **Chips** (3–4): number of parts, number of steps, the version, "Drag the slider to explode".
- **Numbers = assembly order** (`data-n` = `data-order` = 1…N), so the balloons, the list and the steps agree.
- **Parts list:** number, name (≤ 3 words), quantity, material or role (one short sentence).
- **Reading guide:** one step per assembly order (`ol.steps`, `<li class="cN"><b>Part</b><span>one or two sentences</span></li>`),
  each self-contained. Steps = distinct `data-order` values.
- **3 takeaways** with icons: how it works (`i-idea`), a common mistake or safety point (`i-alert`), a "so what" (`i-target`).
- **Footnote:** what was simplified or left out; "not to scale".

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text), `{{HEADLINE}}`, `{{FORM}}`,
`{{LEDE}}` and put the content where `<!-- CONTENT GOES HERE -->` is. Don't rewrite the CSS, the scripts or the `<defs>`.

Page skeleton (in this order):
```html
<ul class="chips"><li><b>8</b> parts</li><li>Type: <b>click pen</b></li></ul>
<figure class="stage">
  <svg viewBox="0 0 960 560" role="img" aria-label="one-sentence description" data-names="1">
    <g class="ev-part c1" data-n="4" data-order="4" data-dx="-60" data-dy="0" data-balloon="b"> …drawing… </g>
    … one ev-part per part …
  </svg>
  <figcaption>What the reader is looking at.</figcaption>
</figure>
<p class="scroll-hint">← swipe the drawing →</p>
<ul class="legend"><li><span class="sw c1"></span>Plastic body</li><li><span class="sw c0"></span>Metal</li>…</ul>
<h2>Parts list</h2>
<table class="ev-list"><caption class="sr">Parts list</caption>
  <thead><tr><th scope="col">#</th><th scope="col">Part</th><th scope="col">Qty</th><th scope="col">Material / role</th></tr></thead>
  <tbody><tr data-n="4"><td class="n"><span>4</span></td><td class="nm">Lower barrel</td><td class="q">1</td><td class="ro">Plastic. The grip.</td></tr>…</tbody></table>
<h2>How it goes together</h2>
<ol class="steps"><li class="c0"><b>Nose cone</b><span>Hold it point down …</span></li>…</ol>
<h2>Key takeaways</h2>
<div class="cards"><div class="card c1"><svg><use href="#i-idea"/></svg><b>Insight</b><p>…</p></div>…</div>
<p class="note">Simplified: …</p>
```
**The page builds the controls, the dashed assembly lines, the balloons, the walkthrough player and the hover
links by itself — do not draw them.** The colour classes of the legend swatches are `sw c0`…`sw c5`.

### The part: `<g class="ev-part cN" …>`
| Attribute | Meaning |
|---|---|
| `data-n` | part number — must have a row `tr[data-n]` in the parts list (the validator fails otherwise) |
| `data-order` | assembly order 1…N (parts with the same order arrive together). Defaults to markup order (the validator warns) |
| `data-dx`, `data-dy` | how far the part moves (SVG units) when fully exploded. Or `data-gap="120"` = distance along the svg's `data-axis="x,y"` (default `0,-1` = up) |
| `data-balloon` | side of the balloon: `r` (default) `l` `t` `b`; `data-bgap` distance (default 36); or `data-bx`/`data-by` explicit offset from the anchor |
| `data-anchor="x,y"` | where the leader line touches the part (assembled position); default = middle of the bbox side |
| `data-center="x,y"` | where the dashed assembly line starts (default: bbox centre) |
| class `c0`–`c5` | the part's colour (inherited by the helpers below, and copied to the balloon and list row) |

The base part (the one everything is built on) may have no offset. **Draw each part at its ASSEMBLED position.**
DOM order = drawing order (later parts are drawn on top): draw hidden inner parts first so the body covers them when assembled.
Balloons show the number, plus the part's name next to it when the svg has `data-names="1"` (recommended).

Extra page-level attributes on the `<svg>`: `data-names="1"` (show names next to the balloons), `data-centerline="x1,y1,x2,y2"`
(dash-dot centre line, fades in as the parts separate), `data-ghost="cx,cy,scale"` + `data-ghost-label="Assembled pen, 140 mm"`
(a faint copy of the assembled object, centred at cx,cy, as a size reference while exploded), `data-zoom="2.6"` (the most the view
may zoom in; default 2.6), `data-fit="off"` (turn the auto-zoom off). More part attributes: `data-line="none"` (no own assembly
line: use it when a centre line is drawn), `data-mate="N"` (a short dashed guide from this part to part N), `data-late-before="N"`
(see `late` below).

**Auto-fit zoom:** the page zooms the view to what is on screen: assembled = the object fills the stage, exploded = everything
(parts, balloons, ghost) fits. The `viewBox` you write only sets the aspect ratio and the drawing coordinates, so draw big and
don't worry about empty margins.

### Drawing helpers
Put helpers inside a part: `<g class="ev-prim [cN]" data-type="..." data-...="..."></g>`. The script turns them into shaded
shapes. A class `c0`–`c5` (or `ev-dark`, `ev-metal`) on the helper changes its colour. Draw every part from several helpers
(body + details), the way a real part is made.

**Side views** (pen, torch, bolt; the long axis is horizontal; units = px):
| `data-type` | Attributes | Draws |
|---|---|---|
| `tube` | `x y` (top-left) `w h`, `dir="h"` or `"v"`, `cap` (end-ellipse half width), `ends="lr"` (`l` rounded left end, `r` visible right end face), `wall` (rim thickness: a dark open end) | cylinder with shading, highlight line and end caps |
| `cone` | `x y` (left centre) `len r1 r2`, `wall` | tapered cylinder (nose cone, tip) with a face ellipse |
| `thread` | `x y w h pitch`, `cap`, `ends` | threaded cylinder (screw-in neck) |
| `coil` | `x y w h turns wire` | spring with front and back wire and a highlight |
| `teeth` | `x y w h n` | saw teeth pointing left (ratchets, cams, crowns) |
| `slab` | `x y w h rx depth` | rounded card with a visible edge |

**Isometric** (phone, board, case; units = any, e.g. mm; x runs down-right, y down-left, z up). Set the projection on the svg:
`data-angle="26"` (30 = true isometric, smaller = flatter), `data-k="0.95"` (px per unit), `data-ox`, `data-oy` (screen position of the origin).
| `data-type` | Attributes | Draws |
|---|---|---|
| `rbox` | `x y z w d h r` (corner radius), `pocket` (inset) `pocket-depth` `pocket-r` (dark recess with floor), `panel` (inset) `panel-r` `fill` (`screen` `wall` `lt` `dk` `glass`), `shadow="1"`, `late="1"` | rounded box with walls shaded by direction (light from the top-left), a rim, soft shadow |
| `poly` | `pts="x,y x,y …"` `z h r shadow` | extruded outline (L-shaped boards, brackets) with rounded corners |
| `box` | `x y z w d h`, `pocket`, `panel` | sharp box |
| `irect` | `x y z w d r fill` | flat rounded rectangle on a plane: screen, label, pad, cut-out (`fill`: `screen` `hole` `label` `lt` `dk` `wall` `app` `ring` `glass`) |
| `icirc` | `cx cy z r fill` | flat circle on a plane (hole, coil, LED) |
| `lens` | `cx cy z r h` | camera lens barrel with rings and a glint |
| `cyl` / `screw` | `cx cy z r h hole` / `cx cy z r len` | vertical cylinder, disc or ring / screw with a slot |
| `itext` | `x y z size text`, `dir="x"` or `"up"` (phone UI), `on="dark"` | text lying on a face (labels, clock) |
| `sface` | `face="y"` or `"x"` `pos u0 u1 z0 z1 r fill` | rounded rectangle on a side face: buttons, USB port, speaker holes |

`late="1"` on an `rbox` (a frame) draws its walls and rim ABOVE the parts that sit inside it (battery, board), so they are
hidden by the walls as in the real object; give the frame part `data-late-before="N"` (the number of the first part that
should cover it, e.g. the display). Mark side details (`sface`) with the class `ev-late` too.

Plain SVG classes (no hard-coded colours; all follow the part's `cN` class and the theme): `pf` (flat face; `pf lt`, `pf dk`),
`iso-t` / `iso-l` / `iso-r`, `ev-fine` (thin detail line), `ev-wire`, `ev-hole`, `ev-screen`, `ev-label`, `ev-ring`.
Add `data-gloss="h"` (or `v`) to any path to get cylinder-like shading.

### Layout rules (the validator checks these in the EXPLODED state)
- `viewBox` width **960**; height as needed. Labels and parts must stay inside the zoomed view (the zoom takes care of it).
- **Parts must not overlap each other when exploded** — the check uses each part's bounding box (2 px tolerance). Diagonal
  isometric shapes have big boxes: space layers by their full box height (compute it from the geometry, leave 14–16 px).
- Balloons: choose sides so balloons and names never overlap (axis parts: all `b` or alternate `l`/`r`); give the balloon an
  explicit `data-anchor="x,y"` on a point that is really on the part (e.g. its right-most corner).
- A name label is ≤ 3 words. The page opens **exploded**; the assembled view must look like the real object.
- Light comes from the top-left: top faces lightest, left walls lighter than right walls. Don't outline parts in a loud colour.
- Phones: the stage keeps a 640 px minimum width and scrolls inside its card.

### What the page does by itself
- **Slider 0–100 %** (keyboard: arrows), **Assemble**, **Explode**, **Play assembly** (flies the parts in one by one in
  `data-order`, each step lighting up its reading-guide card; ends assembled).
- Dashed **assembly lines** grow as parts separate; **balloons** with leader lines follow the parts and fade in.
- **Hover or focus** a part, a balloon or a parts-list row: all three light up. Parts and rows are keyboard-focusable.
- The **walkthrough player** (from `ol.steps`) assembles the object step by step; clicking a step card shows the object
  assembled up to that step (later parts wait exploded and faded).
- **Reduced motion:** no animation, the slider still works. **Print:** light, exploded, parts list included.

### Handwritten style (optional — OFF by default)
Leave `data-style` out. Add `data-style="handwritten"` on the figure (`<figure class="stage" data-style="handwritten">`)
**only when the user asks** (handwritten, notebook style, "like my class notes"). Never choose it yourself and keep it
out of default example markup. It gives ruled paper, handwriting fonts (Kalam / Caveat) and sticky notes; the page then
has no theme button (always paper). The fonts load from Google Fonts; offline a system handwriting font is used.

**Icons** (`#i-…` in takeaway cards): `sun cloud rain drop wave wind leaf sprout tree mountain fire thermo bolt atom
flask cell dna heart eye user users home factory bank truck globe flag laptop phone server db cpu code gear link lock
key shield search mail chat coin cart chart target idea doc book clock cal star check alert x loop`. Unknown names fail validation.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium); otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py page.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py page.html --out <dir>
```
It FAILS on placeholders, external resources, unknown icon/marker ids, JavaScript errors, sideways scrolling, labels or
parts outside the viewBox, labels or balloons overlapping (exploded), **parts overlapping each other when exploded**,
**parts that do not return to their assembled place at 0 %**, **a balloon without a parts-list row (or the reverse)**,
duplicate numbers, and a print layout that is not light, not exploded or still shows the controls. It WARNS on a missing
`data-order`, steps that do not match the orders, more than 14 parts, parts that never move, a label sitting on another
part, hard-coded colours, no icons. It renders `*_light.png`, `*_dark.png`, `*_mobile.png`, `*_assembled.png`,
`*_exploded.png` and `*_print.pdf`. **Look at all the PNGs**: the assembled one must read as one object, the exploded
one must be cleanly separated, balloons and names must not collide, and both themes must be readable.

## Step 5 — Deliver
- Save as `examples/009-explodedview/<object-slug>-explodedview.html` (unless the user or project names another place —
  never make a new top-level folder) and deliver it per the environment (publish as an artifact / present the file).
- If the user wants an image, give the `_exploded.png` (and `_assembled.png`).
- In chat, at most two lines: what the drawing shows and an offer ("want it as a flowchart of the assembly, or one part zoomed?").

## Quality bar (self-check before delivering)
- **Part names, the part count and the assembly order are correct** for the stated version of the object.
- Assembled = one believable object (hidden inner parts are covered, walls hide what is inside); exploded = every part visible, separated along the one axis.
- Numbers match everywhere: balloon, list row, reading-guide step, `data-order`.
- ≤ 4 colour families, each explained; works in dark mode and on a phone; no label outside the drawing or on top of another.
- **Would this pass as a product-manual illustration?** One centre line, real proportions with a stated reference size, shaded
  parts with believable detail (threads, chips, buttons, ports), a faint assembled reference, and a view that zooms to fit.
- Nothing invented: sizes and detail are simplified and the footnote says so.
