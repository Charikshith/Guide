---
name: handwritten
description: Turn any topic into a handwritten-style notebook page — ruled paper, pen-and-highlighter look, hand-drawn labelled diagrams, boxed key points and a sticky-note exam tip. Use this whenever the user types /handwritten, or asks for handwritten notes, notebook-style notes, study notes, revision notes, a study sheet, "notes like a topper's notebook", or class notes with diagrams on any subject, even if they don't say "handwritten".
---

# /handwritten — notebook-style study notes

The output is ONE self-contained HTML page that looks like a neat student's notebook page:
ruled lines, red margin, blue-pen body text, black-pen headings, highlighter, red-pen
corrections, a hand-drawn diagram, and a sticky note. It must be **accurate, compact and
exam-useful** — the handwriting look is the wrapper, the content is the point.

## Usage
`/handwritten <topic>` — optional extras the user may add: level (class 10, undergrad, interview prep),
length ("1 page", "detailed"), language, or "with diagrams". Defaults: one page, general
student level, English, at least one diagram.

If the user gives only `/handwritten` with no topic, ask for the topic in one short line.

## Step 1 — Plan the content (before any HTML)
Write notes the way a top student would, not the way a textbook would:
- **Title** (2–5 words) and today's date in the corner.
- **3–6 short sections** with `h2` headings. Fragments, not paragraphs: max ~12 words per line.
- Abbreviations and symbols are encouraged: →, ∴, ∵, ≈, ↑, ↓, w/, b/c, e.g., imp!
- **Definition box** (`.box`) for the single most important definition or formula.
- **1–2 diagrams** (see Step 3) — the diagram must teach something the text doesn't.
- **Sticky note** (`.sticky`) with a mnemonic, exam tip, or common mistake.
- Optional: a comparison table, a margin note (`.side`), a red-pen correction of a common
  misconception using `.strike` followed by the right answer.
- Highlight sparingly: ≤ 1 highlight per section; yellow = key term, pink = warning,
  green = result, blue = example.

Fact-check yourself: formulas, numbers, names and directions of arrows must be correct.
Never invent statistics. If the topic is contested or uncertain, say so in a short note.

## Step 2 — Build the page from the template
Copy `assets/template.html` (in this skill's folder) and fill it. Replace `{{TITLE}}`
and `{{DATE}}`, and put content where `<!-- CONTENT GOES HERE -->` is. Do not rewrite the CSS;
use its classes:

| Need | Markup |
|---|---|
| Section heading | `<h2>Light reaction</h2>` |
| Bullets | `<ul><li>…</li></ul>`; variants `li.star`, `li.arrow`, `li.check` |
| Numbered steps | `<ol><li>…</li></ol>` |
| Key term | `<span class="term">…</span>` |
| Highlighter | `<span class="hl">` / `hl pink` / `hl green` / `hl blue` |
| Red / green pen | `<span class="red">`, `<span class="green">` |
| Wavy underline / circled | `<span class="ul">`, `<span class="circ">` |
| Correction | `<span class="strike">wrong</span> <span class="red">right</span>` |
| Boxed definition | `<div class="box">…</div>` (`box red` for warnings) |
| Formula line | `<p class="formula">6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂</p>` |
| Sticky note | `<aside class="sticky"><b>Exam tip!</b><br>…</aside>` — place it right before the section it sits beside |
| Margin note | `<span class="side" style="top:XXXpx">imp!</span>` — top is a multiple of 32 |
| Two columns | `<div class="cols"><div>…</div><div>…</div></div>` |
| Blank ruled line | `<div class="gap"></div>` |
| Table | `<div class="wrap"><table>…</table></div>` |
| Code block | `<pre class="code">…</pre>` with token spans `kw` (keyword), `st` (string), `nu` (number), `bi` (built-in), `fn` (function call), `cm` (comment) |

Spacing rule: everything is sized in multiples of `--line` (32px) so writing sits on the
ruled lines. Don't add custom margins/padding/font-sizes that break this grid.

## Step 3 — Draw the diagram (hand-drawn SVG)
```html
<figure>
  <svg viewBox="0 0 600 300" role="img" aria-label="…">
    <rect class="sk" x="40" y="60" width="140" height="80" rx="14"/>
    <path class="sk blue" d="M180 100 C 240 90, 300 90, 360 100" style="color:var(--ink)" marker-end="url(#arr)"/>
    <text class="lbl b" x="110" y="105" text-anchor="middle">Chloroplast</text>
  </svg>
  <figcaption>Fig 1: what the diagram shows</figcaption>
</figure>
```
- Every stroke gets `class="sk"` (+ `blue`/`red`/`green`) — the template's sketch script redraws
  each `.sk` shape (path, line, polyline, polygon, rect, circle, ellipse) as a smooth, gently wobbly
  hand-drawn line when the page loads. Draw clean geometry; don't add your own filter or jitter.
  A path with several sub-paths (more than one `M`) is left as drawn — split it into separate
  paths if you want the wobble. Never use `fill` colours other than light washes
  (e.g. `fill:var(--hl-green)` with the `sk` stroke) — a pen sketch, not clip-art.
- Arrows: `marker-end="url(#arr)"` and set `style="color:…"` to the stroke colour.
- Prefer curved paths (`C`/`Q`) to dead-straight lines.
- Labels: `class="lbl"` (`b` bold, `r` red, `g` green), ≥ 15px gap between labels, and keep
  every label inside the viewBox (leave 20px padding at the edges).
- Diagram types that work well: process flow (boxes + arrows), labelled object (simple shapes
  + leader lines to labels), cycle (nodes on a circle), comparison (two columns), graph
  (axes + one curve, labelled).
- Keep the viewBox ≤ 660 wide and label font at the default 17px; on phones the template gives
  diagrams a 520px minimum width (they scroll inside their own box) so labels stay legible.
- Straight lines are fine — they get a slight wobble too; their end points stay exactly in place,
  so arrows still meet their targets.
- No raster images, no emoji as diagram parts, no external assets.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium);
otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py notes.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py notes.html --out <dir>
```
If Playwright is missing, set it up from the repo root:
`python -m venv .venv` → `<venv-python> -m pip install -r requirements.txt` →
`<venv-python> -m playwright install chromium`.
It checks for leftover placeholders, disallowed external resources, sideways scrolling at
desktop and phone width, diagram labels that are clipped or overlap, and renders
`*_desktop.png` / `*_mobile.png`. **View the PNGs** and fix anything that looks wrong
(overlaps, cramped diagram, text crossing lines, empty half-page) before delivering. A
"web font not loaded" WARN only means the sandbox is offline; it's fine.

## Step 5 — Deliver
- Save as `examples/002-handwritten/<topic-slug>-notes.html` (unless the user or project names
  another place — never make a new top-level folder), then deliver it (publish it as an
  artifact / present the file, per the environment).
- If the user wants an image or something printable, also give the desktop PNG, or a PDF via
  `page.pdf()` in Playwright.
- In chat, add at most two lines: what the page covers and an offer to do a page 2,
  a different level, or flashcards from the same notes. Don't repeat the notes in chat.

## Quality bar (self-check before delivering)
- Would a student revise from this the night before an exam? Every line earns its place.
- One clear visual hierarchy: title → section headings → bullets; nothing wall-of-text.
- Diagram is correct, labelled, and readable on a phone.
- Colours used with meaning, not decoration (≤ 4 highlights total on the page).
