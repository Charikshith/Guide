---
name: mindmap
description: Explore any topic and its connected ideas as a clean, interactive mind map page — a central idea, 5–7 colour-coded main branches that curve out to sub-ideas and details, optional dashed links between ideas on different branches, click-to-fold branches, hover to follow a path, a Play walkthrough that goes branch by branch, light and dark mode, and an optional handwritten notebook style when asked. Use this whenever the user types /mindmap, or asks for a mind map, concept map, brainstorm map, "map out the ideas around X", "break X into its parts", a topic overview, or revision / study notes as a mind map, even if they don't say "mind map". For a step-by-step process use /flowchart; for a general explainer visual use /visualize.
---

# /mindmap — any topic → a map of its connected ideas

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent, a
lede, fact chips, **the mind map** (drawn automatically by a built-in layout engine), fold /
unfold buttons, a small legend, a numbered reading guide with a Play walkthrough (one step per
main branch), 3 takeaways and a footnote. Light + dark mode, no external assets.

**You describe the ideas as data; the engine draws them.** Never hand-place labels or curves —
the engine splits the main branches left and right by size, gives every level its own column so
text never overlaps, centres each idea on its children, draws tapered curved branches in each
branch's colour, routes dashed links around the text, and fits the canvas.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).

## Usage
`/mindmap <topic>` — optional extras: audience, depth ("simple", "detailed"), `handwritten`,
language. Defaults: general audience, 5–6 main branches, 25–40 ideas in total.

If the user gives only `/mindmap` with no topic, ask for the topic in one short line.

## Step 1 — Understand the topic
Write (for yourself) the real structure: what the centre is, then the 5–7 biggest parts of it.
- **Main branches** = the biggest, different-in-kind parts (causes / effects / solutions; parts of
  a system; stages; people / places / ideas). Not a list of leftovers — each is a real category.
- **Sub-ideas** (level 2): 2–4 per branch. **Details** (level 3): 0–3 under a sub-idea, only when
  they add something. Keep branches roughly the same size.
- **Links** (0–3): real relationships between ideas on *different* branches ("causes",
  "secures", "makes"). Link ideas on neighbouring branches — links across the whole map are long.
- Order the branches the way you would read them: the map goes clockwise from the top right.

Fact-check: every label, note and link must be true. Don't invent numbers, dates or names. Say
"simplified" in the footnote and name what you left out.

## Step 2 — Write the mind-map spec (JSON)
Put it at the end of the content in `<script type="application/json" id="mm-spec">`.

```json
{
  "center": {"label": "Photosynthesis", "sub": "plants make food from light", "icon": "leaf"},
  "branches": [
    {"label": "Raw materials", "icon": "drop", "color": "c2", "children": [
      {"label": "Carbon dioxide", "note": "enters through stomata"},
      {"id": "water", "label": "Water", "note": "taken up by roots", "children": [
        {"label": "Moves up the xylem"}
      ]}
    ]},
    {"label": "Two stages", "icon": "loop", "children": [
      {"id": "lr", "label": "Light reactions"},
      {"id": "cc", "label": "Calvin cycle"}
    ]}
  ],
  "links": [{"from": "lr", "to": "cc", "label": "ATP + NADPH"}]
}
```
(Real JSON has no comments. The example is cut short — a real map has 5–7 branches.)

| Field | Meaning |
|---|---|
| `center.label` | the topic, ≤ 5 words |
| `center.sub` | optional second line, ≤ 6 words |
| `center.icon` | optional icon name (see list) |
| `branches[]` | main branches, in reading order (clockwise from top right) |
| `branches[].label` | ≤ 4 words |
| `branches[].icon` | give **every** main branch an icon (or none of them) |
| `branches[].color` | optional `c1`–`c5`; default cycles blue, green, amber, rose, violet, green |
| `branches[].step` | optional number for the reading guide (default: position, 1, 2, 3 …) |
| `children[]` | sub-ideas; each has `label` (≤ 6 words), optional `note` (≤ 6 words, level 2–3), optional `id`, optional `children` (details, ≤ 6 words each) |
| `id` | only needed on ideas used in `links`; short and unique. Any idea can have one |
| `links[]` | `{"from": id, "to": id, "label"?, "color"?}` — dashed arrow between two ideas |

**Style** (optional, top level — **off by default**): the clean style is the default; leave
`style` out. Add `"style": "handwritten"` **only when the user asks for it** — they say
handwritten, notebook style, or "like my class notes". Don't switch to it on your own because
the topic is a school or revision topic. It turns the page into a notebook page — ruled paper,
red margin, handwriting fonts (Kalam / Caveat), wobbly pen lines, highlighter fills, circled
step numbers and sticky-note takeaways. Nothing else changes: same spec, layout and
walkthrough. It loads the two fonts from Google Fonts; offline it falls back to a system
handwriting font.

Keep it readable: 5–7 main branches, 25–40 ideas, 3 levels. Bigger topic → split it into two
maps, or summarise a part as one idea and mention it in the footnote.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text),
`{{HEADLINE}}` (may contain `<span class="accent">`), `{{FORM}}` (e.g. `Mind map · Technology`),
`{{LEDE}}` (≤ 25 words), and put this where `<!-- CONTENT GOES HERE -->` is:

```html
<ul class="chips"><li><b>6</b> big ideas</li><li>…</li></ul>
<figure class="stage">
  <svg id="mm" class="mm" role="group" aria-label="one-sentence summary of the map"></svg>
  <figcaption>The big idea sits in the middle … Hover to follow a branch, click a main branch to fold it.</figcaption>
</figure>
<p class="scroll-hint">← swipe the map →</p>      <!-- shows on phones only -->
<div class="mm-tools" id="mm-tools"></div>          <!-- Fold all / Unfold all -->
<ul class="legend" id="mm-legend"></ul>             <!-- filled automatically -->
<h2>How to read it</h2>
<ol class="steps"><li class="c1"><b>Branch name</b><span>One or two sentences.</span></li>…</ol>
<h2>Key takeaways</h2>
<div class="cards"><div class="card c1"><svg><use href="#i-idea"/></svg><b>Insight</b><p>…</p></div>…</div>
<p class="note">Simplified: …</p>
<script type="application/json" id="mm-spec">{ … }</script>
```
- Reading guide: **one `<li>` per main branch**, in the same order; the `li` colour class matches
  that branch's colour. Each text must make sense on its own — the Play walkthrough shows it as a
  caption while lighting up that branch.
- Takeaways: the insight, a common mix-up (`i-alert`), and a "so what".
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
.venv\Scripts\python <skill-dir>/scripts/validate.py map.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py map.html --out <dir>
```
It FAILS on bad JSON, unknown ids, icons or colours, overlapping labels or shapes, link labels on
text, text spilling out of a pill, clipped text, JavaScript errors and sideways scrolling. It
WARNS on too many or too few ideas, too many main branches, unbalanced branches, branches with no
sub-ideas, ideas nested deeper than 3 levels, too-long labels, links that cross text, and
step-count mismatch. It renders `*_light.png`, `*_dark.png`, `*_mobile.png` — **look at them**.
If the map is lopsided or a link crosses text: reorder the branches, rebalance the sub-ideas,
shorten labels, or link ideas on neighbouring branches.

## Step 5 — Deliver
- Save as `examples/006-mindmap/<topic-slug>-mindmap.html` (unless the user or project names
  another place — never make a new top-level folder) and deliver it per the environment
  (publish as an artifact / present the file).
- If the user wants an image, also give the light PNG.
- In chat, at most two lines: what the map covers and an offer (e.g. "want one branch zoomed
  into its own map, or a simpler version?"). Don't repeat the page.

## Quality bar (self-check before delivering)
- The centre is one clear topic; the main branches are different kinds of thing and similar in size.
- Labels are short noun phrases, not sentences; notes add a fact, not a repeat of the label.
- Each branch has 2–4 sub-ideas; nothing deeper than 3 levels; links are few and meaningful.
- Facts are right; simplifications are named in the footnote.
- The reading guide has one step per main branch, in map order.
