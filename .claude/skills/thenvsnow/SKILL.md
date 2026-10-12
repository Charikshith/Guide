---
name: thenvsnow
description: Compare the past against the present as an interactive then-vs-now page built on real, sourced numbers — two big THEN and NOW year panels, an illustrated scene for each with a draggable before/after slider, data-driven metric rows (then value, % or × change coloured by better/worse, now value, bar pair), "what changed / what stayed the same" lists, an optional milestone strip, a "biggest change" callout, a "why it changed" box and a required Sources section that ties every figure to a named, dated, linked source. A % / × toggle, a Play walkthrough, light and dark mode, a print layout that fits 1–2 pages, and an optional handwritten notebook style when asked. Use this whenever the user types /thenvsnow, or asks for "then vs now", "past vs present", "before and after", "X in 1950 vs today", "how has X changed since …", "compare 1984 with today", or a two-moment comparison with numbers, even if they don't say "then vs now". For many dated events in a row use /timeline; for a poster of statistics use /infographic; for an illustrated explainer use /visualize.
---

# /thenvsnow — the past against the present, in real numbers

The output is ONE self-contained HTML page: an eyebrow, a headline with the two years, a lede, chips, **two
year panels** (THEN muted and sepia, NOW vivid), a **before/after slider** over two illustrated scenes, a
**table of metric rows** (each computed from data), reading guide, "what changed / what stayed the same", an
optional **milestone strip**, **The biggest change** + **Why it changed**, a **Sources** section and a footnote.
Light + dark mode, no external assets (Google Fonts only in the optional handwritten style).

**It is not a /timeline.** A timeline puts many dated events on one axis. /thenvsnow compares two moments
(or two moments plus 3–5 milestones between them) on the *same measures*. If the user wants "the history of X",
use /timeline.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).
**Printing is always light** (white paper, dark ink), whatever theme is on screen: the template does this for
you, hides the controls and the slider handle, and shows the two scenes side by side.

## No invented numbers (the rule of this skill)
A then-vs-now page lives on numbers, so every number must be real:
- **Use only figures you have sourced.** Look them up (web search / fetch) or take them from the user's own data.
  Prefer primary or well-documented sources: manufacturer specs, national statistics, UN / World Bank / OECD /
  Our World in Data, central banks, official archives. If you have no web access, use only well-established facts
  and mark them approximate (`data-approx`, "≈") and say so in the footnote. **If you cannot verify a figure, leave it out.**
- **Always state the two years** (`data-then-year`, `data-now-year`; the page shows them in the panels, the tags and the column
  heads). "Now" is the latest year the source covers, not today's date, unless it really is.
- **Show units** for every figure (`data-unit`, `data-pre` for "$"). Say whether money is nominal or adjusted
  (if adjusted, name the index and the base year, and add a second row for it).
- **Never type a % change or a × factor by hand.** The page computes them from `data-then` and `data-now`. In prose use
  `<span class="tn-fill" data-of="id" data-show="pct|abs|x|then|now"></span>`. If you do write one as a claim,
  put it in `data-pct` / `data-x`; the validator recomputes it and FAILS on a mismatch.
- **Compare the same thing.** Same measure, same definition, same unit family, same region. Say in the footnote
  where it is not like-for-like.
- **Sources section is required.** One `<li id="src-N">` per source with **name, year, link** and what it
  supports. Every metric carries `data-src="N"` (or `"1,3"`) so the page shows a small superscript link to it.

## Usage
`/thenvsnow <topic>` — optional extras: the two years ("1984 vs now", "1951 vs 2021"), region, audience, data the
user supplies, `handwritten`, language. Defaults: general audience, the clearest two moments, 5–7 measures.
If the user gives only `/thenvsnow` with no topic, ask for the topic in one short line.

## Step 1 — Choose the two moments and the measures
- **Two years** that a reader can feel the gap between, with data for both. If "now" is a product or a place, name
  it and its year ("MacBook Air M4, 2025"). If a newer one exists but its figures are not documented, say in the footnote
  which you used.
- **5–7 measures** (the validator warns above 10). Each one a number with a unit that exists for both years, and
  one that *means* something to a newcomer. Mix scales: one that falls, one that grows enormously, one that stays human-sized.
- For each, decide `better`: `higher`, `lower` or `neutral`. This sets the colour (green = better, rose = worse,
  grey = neutral). It is about meaning, not direction: a lower price is *better*; population growth is *neutral*.
- Ratios over 200× (or under 1/200) use log-scale bars automatically and say "log scale".

## Step 2 — Research and record every figure
For each figure write down: value, unit, year, source name, URL. Then fill the Sources section. Note arithmetic
(a pixel count is width × height; an inflation adjustment names the index and both years). % changes are computed
**from the figures shown**, so round the data to what the page displays (46.4, not 46.3944) and say so in the footnote.

## Step 3 — Build the page from the template
Copy `assets/template.html`. Replace `{{TITLE}}`, `{{HEADLINE}}` (`Computers: <span class="accent">1984 vs 2025</span>`),
`{{FORM}}` (`Then vs now · Technology`), `{{LEDE}}` (≤ 25 words), and put the following where
`<!-- CONTENT GOES HERE -->` is. Don't add CSS, don't edit the template's scripts.

```html
<ul class="chips"><li><b>1984</b> vs <b>2025</b></li><li><b>7</b> measures</li><li>Every figure has a <b>source</b></li><li>Prints on <b>2 pages</b></li></ul>
<div class="tn" id="tn" data-then-year="1984" data-now-year="2025">
  <section class="tn-hero">
    <div class="tn-panels">
      <div class="tn-panel then"><span class="tag">Then</span><span class="tn-y">1984</span><h3>Apple Macintosh 128K</h3><p>One or two lines.</p></div>
      <div class="tn-panel now"><span class="tag">Now</span><span class="tn-y">2025</span><h3>MacBook Air 13-inch (M4)</h3><p>One or two lines.</p></div>
    </div>
    <div class="tn-slider" id="tn-slider">
      <svg class="tn-layer then" viewBox="0 0 640 360" role="img" aria-label="describe the THEN scene">…</svg>
      <svg class="tn-layer now"  viewBox="0 0 640 360" role="img" aria-label="describe the NOW scene">…</svg>
    </div>
    <p class="tn-hint">Drag the handle left and right (or press ← → when it is focused) to wipe between 1984 and 2025.</p>
  </section>

  <h2>The numbers</h2>
  <div class="tn-bar" role="group" aria-label="Controls">
    <span class="tn-seg-l">Show change as</span>
    <div class="tn-seg" role="group" aria-label="Show change as"><button type="button" id="tn-m-pct" aria-pressed="true">%</button><button type="button" id="tn-m-x" aria-pressed="false">&times;</button></div>
    <span class="tn-play-grp"><button class="tn-btn nav" type="button" id="tn-prev" aria-label="Previous measure">&#9664;</button><button class="tn-btn" type="button" id="tn-play" aria-pressed="false">Play walkthrough</button><button class="tn-btn nav" type="button" id="tn-next" aria-label="Next measure">&#9654;</button></span>
  </div>
  <div class="tn-metrics" id="tn-metrics">
    <div class="tn-metric" data-id="price" data-label="Price when new" data-then="2495" data-now="999" data-unit="USD" data-pre="$" data-better="lower" data-src="2,5" data-icon="coin" data-step="1" data-note="small line under the label"></div>
    … 5–7 metrics …
  </div>
  <p class="tn-cap" id="tn-cap" aria-live="polite"></p>
  <h2 class="tn-steps-h">How to read it</h2>
  <ol class="steps"><li class="c3"><b>Price when new</b><span>One sentence (read aloud by Play).</span></li> … one per data-step …</ol>

  <h2>What changed — and what did not</h2>
  <div class="tn-cols">
    <section class="tn-col changed"><h3><svg aria-hidden="true"><use href="#i-loop"/></svg>What changed</h3><ul><li><svg aria-hidden="true"><use href="#i-cpu"/></svg><span><b>Memory</b> grew …</span></li>…</ul></section>
    <section class="tn-col same"><h3><svg aria-hidden="true"><use href="#i-check"/></svg>What stayed the same</h3><ul>…</ul></section>
  </div>

  <h2>On the way from 1984 to 2025</h2>               <!-- optional: 3–5 milestones, in date order, evenly spaced -->
  <ol class="tn-miles"><li data-year="2008" data-src="7"><b>MacBook Air</b><span class="d">one line</span></li>…</ol>

  <h2>The big picture</h2>
  <div class="tn-two">
    <div class="tn-big"><span class="lbl">The biggest change</span><span class="hl">From 400 KB to 256 GB: <span class="tn-fill" data-of="disk" data-show="x"></span> more</span><p>…</p></div>
    <div class="tn-why"><span class="lbl">Why it changed</span><ul><li><b>Smaller parts.</b> …</li>…</ul></div>
  </div>

  <h2>Sources</h2>
  <ol class="tn-src">
    <li id="src-1"><b>Apple Support — Macintosh 128K: Technical Specifications</b> <span class="yr">(2024)</span> — <a href="https://…" rel="noopener">support.apple.com/…</a><span class="for">what it supports</span></li>
    …
  </ol>
</div>
<p class="note">Simplified: … Not like-for-like: … Left out: … % changes are computed from the figures shown.</p>
```
The engine adds the handle, the THEN/NOW year tags, the column heads, each row's values, change pill, bars, source
numbers and screen-reader text, and the start/end years of the milestone strip. Use the page's own words only
in the places above.

### Metric attributes (`.tn-metric`)
| Attribute | Meaning |
|---|---|
| `data-label` | name of the measure (required) |
| `data-then`, `data-now` | plain numbers (digits, optional `.` and `,`); required. THEN must not be 0 |
| `data-unit` | unit shown under both values ("years", "USD", "per 1,000 births", "% of people") |
| `data-then-unit` / `data-now-unit` | different units on the two sides **and convertible** (see below); `data-then-disp` / `data-now-disp` = what to *show* (`KiB` → show "KB") |
| `data-pre` | prefix, e.g. `$` |
| `data-approx` | `then`, `now` or `both`: shows "≈" |
| `data-better` | `higher`, `lower` or `neutral` (colour by meaning) |
| `data-src` | source number(s): `"2"` or `"2,5"` |
| `data-icon` | an icon id (list below) |
| `data-id` | name for `.tn-fill` prose |
| `data-note` | small line under the label |
| `data-step` | walkthrough step number (matches the n-th `ol.steps` item) |
| `data-bars` | `linear` or `log` (default: log when the ratio is over 200× or under 1/200) |
| `data-dec` | force decimals (default: as many as you typed, per side) |
| `data-pct` / `data-x` | optional: a % change / × factor you claim; the validator checks it |

**Convertible units** (so 128 KB can be compared with 16 GB): bytes `B KB MB GB TB` (1000-based) and `KiB MiB GiB TiB`
(1024-based); mass `g kg lb oz`; frequency `Hz kHz MHz GHz`; length `mm cm m km in ft mi`; time `s min h`. Two
different units must be in the same family, or the page fails. Percent change is always computed on the converted values.

### Scene vocabulary (inside the two `<svg class="tn-layer">`, `viewBox="0 0 640 360"`)
Draw both scenes in the **same place** (same desk, same horizon, same centre) so the slider reads as "the same
spot, later". Make the then-scene simpler/older, the now-scene fuller. No text except a short caption at the bottom
corners (THEN caption left, NOW caption right; the page already puts the years on top). Classes only, no hard-coded colours:

| Need | Class |
|---|---|
| fills | `k0` zone · `k1` surface-ish · `k2` darker · `ks` surface · `kd` ink · `km` muted · `kc1`–`kc5` accents · `kf1`–`kf5` soft tints |
| outline on a filled shape | add `ko` (`class="k1 ko"`) |
| line | `kl` (muted) · `kl d` dark · `kl t` thin · `kl c1`…`c5` coloured |
| text | `kt` · `kt s` small · `kt m` mono |
| icons | `<use href="#i-…" x y width height class="ico c1"/>` |

The THEN layer is automatically sepia-toned; the NOW layer is not. Leave the scene's own background to a full-size
`<rect>` with a `kf*` class. Keep important content out of the far corners (the year tags sit there).

### Handwritten style (optional — OFF by default)
Add `data-style="handwritten"` to `<div class="tn" …>` **only when the user asks** (handwritten, notebook style).
It gives ruled paper, a margin, Kalam/Caveat fonts and highlighter fills; the theme button is hidden (always paper) and
printing is white. It loads two fonts from Google Fonts (offline it falls back to a system handwriting font). Keep it
out of default markup.

**Icons** (`#i-…` in headings, lists and `data-icon`): `sun cloud rain drop wave wind leaf sprout tree mountain fire thermo
bolt atom flask cell dna heart eye user users home factory bank truck globe flag laptop phone server db cpu code gear link
lock key shield search mail chat coin cart chart target idea doc book clock cal star check alert x loop`. Unknown names
fail validation.

### What the page does by itself
- **Slider:** drag anywhere on the scene, or focus the handle and use ← → (±5; Shift ±1), PageUp/PageDown (±20), Home/End.
  Phones: vertical scroll still works; drag horizontally on the scene.
- **% / ×:** changes every row's change pill (huge values are shortened: `+13.1M%`).
- **Play walkthrough:** steps through the rows with `ol.steps` text as the caption, dims the other rows, scrolls the
  active row into view; ◀ ▶ step by hand; hovering a row or a step highlights the pair.
- **Print:** light palette, A4 portrait, both scenes side by side, controls hidden, source URLs printed after the links.
- **Phones:** panels and columns stack; each row becomes a card; the milestone strip turns vertical.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium); otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py page.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py page.html --out <dir>
```
It FAILS on leftover placeholders, external resources (Google Fonts only for the handwritten style; `<a href>` links are
fine), unknown icon ids, JavaScript errors, sideways scroll, text sticking out of or overlapping inside its box, metric data
that is not a number or cannot be converted, a written `data-pct` / `data-x` that does not match the data, a `.tn-fill` with no
matching `data-id`, **figures without a Sources section**, a `data-src` pointing at a missing source, THEN year not before
NOW year, a slider that does not move with the keys or the mouse, a broken % / × toggle, and a print layout that is not light,
still shows the controls, or does not show both scenes side by side. It WARNS on figures without `data-src`, sources without a
year or link, missing or mismatched years, no metrics, no changed/same lists, no biggest-change or why box, milestones outside the
two years or not 3–5, more than 2 printed A4 pages, `ol.steps` that do not match `data-step`, and hard-coded colours.
It renders `*_light.png`, `*_dark.png`, `*_mobile.png` and `*_print.pdf` — **look at the PNGs** and fix anything cramped,
clipped, lopsided or unreadable in either theme. Use the page count it prints in the "Prints on N pages" chip.

## Step 5 — Deliver
- Save as `examples/010-thenvsnow/<topic-slug>-thenvsnow.html` (unless the user or project names another place — never
  make a new top-level folder) and deliver it per the environment.
- If the user wants a PDF, tell them to print the page (Ctrl/Cmd+P → Save as PDF) or give the validator's `_print.pdf`.
- In chat, at most three lines: what is compared (the two years), the headline number, that every figure is listed under
  Sources, and an offer ("want other years, or one more measure?"). Say plainly which figures are approximate.

## Quality bar (self-check before delivering)
- Every figure is real, with a source (name, year, link) and the right year on each side; nothing invented; anything
  unverified was left out; approximations are marked "≈" and explained.
- % and × are computed by the page; any % you wrote matches; units are shown; money says nominal or adjusted.
- Colour follows *better / worse*, not up / down; neutral things are grey.
- Both scenes sit in the same place, the slider works with mouse, touch and keyboard.
- 5–7 measures, a changed list, a stayed-the-same list, one biggest change, one "why" box, a Sources section, a footnote.
- Works in dark mode and on a phone; prints on 1–2 light pages with both scenes side by side.
