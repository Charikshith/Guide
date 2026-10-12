---
name: infographic
description: Build a structured, poster-style infographic page from real numbers — a giant hero stat, rows of count-up stat tiles with icons, icon pictograms ("7 in 10"), bar charts, stacked bars, donut and ring charts, A-vs-B comparisons, a short step strip, "Did you know?" and quote boxes, and a required Sources section that ties every statistic to a named, dated, linked source. Scannable in 10 seconds, mostly numbers + icons + short labels, light and dark mode, prints on 1–2 pages, with an optional handwritten notebook style when asked. Use this whenever the user types /infographic, or asks for an infographic, "key stats", "by the numbers", a stats poster, a data story, a one-page fact sheet with numbers, or "show this data visually with icons", even if they don't say "infographic". For a dense reference page use /cheatsheet; for how something changed over time use /timeline; for an explainer scene use /visualize; for notebook-style notes use /handwritten.
---

# /infographic — real numbers → a one-page, poster-like visual story

The output is ONE self-contained HTML page: an eyebrow, a headline, a one-line lede, small chips, then a vertical column
(max ~880px) of **5–8 stacked panels** — a **hero** with one giant number, stat tiles, pictograms, charts, a
comparison, a step strip, a "Did you know?" box — then a required **Sources** panel with a footnote on what is
estimated. Light + dark mode, no external assets (Google Fonts only in the optional handwritten style).
Charts are drawn by the page's script from **data attributes**: you write the data, not SVG geometry.

It is a **poster, not an article**: numbers, icons and short labels. No paragraph over 40 words.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).
**Printing is always light** (white paper, dark ink), whatever theme is on screen: the template does this
for you, portrait A4, panels never split, and it hides the theme button.

## THE rule: no invented numbers
An infographic is only as good as its figures. Wrong or made-up statistics are worse than no infographic.
- **Use only real, sourced figures.** If you have a web search / fetch tool, look each number up and read it on
  the source page. Do not copy a number from a blog if you can reach the original (WHO, UN, NASA, USGS, national
  statistics offices, the report itself). If a figure only appears in a secondary source, say so in the Sources list.
- **No tools?** Use only well-established facts you are sure of, round them, mark them "approximate" (≈) and say in the
  footnote that they were not looked up.
- **If the user gives data, use it exactly** as given (same numbers, units, years). Do not "fix" or round it. Credit
  them ("Data: provided by the user") in Sources.
- **If you cannot verify a figure, leave it out.** Never fill a panel with a plausible-looking number.
- **Every stat has a year** ("2024", "as of 2023", "1993 estimate") written next to it.
- **Round honestly.** Use ≈ when you round; never add decimals the source does not have. Keep the source's unit.
  Shares that add to 99% or 101% because of rounding: say so in the footnote, do not "fix" them.
- **Derived numbers** (a ratio, a sum, "6 of 8") are allowed only if you worked them out from sourced numbers;
  say how in the footnote ("176 days = 4,222.6 hours ÷ 24").
- **Tie each stat to a source** with a small superscript `<sup class="src"><a href="#s1">1</a></sup>` or a
  "Source: …" line, and list every source in the **Sources** panel: name, year, link (https). The validator
  FAILS a page with stats and no Sources section, and WARNS on any stat without a source reference or a year.
- **Say what is estimated or simplified** in the footnote (`<p class="note">`).

## Usage
`/infographic <topic>` — optional extras: audience ("for kids", "for a board meeting"), region or year range,
the user's own data (pasted numbers), size ("short"), `handwritten`, language.
Defaults: a general reader, 5–8 panels, prints on ≤ 2 pages.

If the user gives only `/infographic` with no topic or data, ask for it in one short line.

## Step 1 — Understand the story and the data
- **One takeaway.** What should the reader remember in 10 seconds? That is the hero number. Write it as one sentence.
- **Where do the numbers come from?** User data, or you research it. Collect 8–15 real figures with their source and
  year before designing anything. Read the original page; note the exact wording and unit.
- **Pick the strongest figures** and the comparison that gives them meaning (before/after, A vs B, share of a whole,
  rank). A number without a comparison is trivia: "2.1 billion" works because it is "1 in 4".
- **What to leave out:** figures you cannot verify, figures from different years that are compared as if equal, anything
  that needs a paragraph to explain.

## Step 2 — Plan the panels (story + data)
- **5–8 panels** (the validator warns above 8, not counting Sources). Order: hook (hero) → the big picture
  (share / proportion) → the breakdown (bars, stack) → the human scale (pictogram, tiles) → the contrast
  (comparison) → what to remember ("Did you know?") → Sources.
- **Use at least four different component types**, so the page has rhythm. Do not stack four bar charts.
- **Colour = meaning.** One accent per category (`c1`–`c5`), the same colour for the same thing everywhere on the page
  (all "water" things blue, all "problem" things rose). Add a legend wherever colour is the only link between a label
  and a mark. `muted` is for "everything else".
- **Pairs:** two adjacent panels with class `half` sit side by side on wide screens (always use them in pairs).
- **Chips (3–4):** number of panels, the years the data covers, number of sources, "Prints on N pages" (use the
  number the validator reports).
- **Fit:** it must print on ≤ 2 A4 pages. If the validator says 3, cut a panel or shorten one.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text), `{{HEADLINE}}` (may contain
`<span class="accent">`), `{{FORM}}` (e.g. `Infographic · Water`), `{{LEDE}}` (≤ 25 words), and put the following where
`<!-- CONTENT GOES HERE -->` is. Don't add CSS, don't edit the template's script.

```html
<ul class="chips"><li><b>7</b> panels</li><li>Data: <b>1993–2024</b></li><li><b>3</b> sources</li><li>Prints on <b>2 pages</b></li></ul>
<div class="ig" id="ig">
  <section class="pn hero c1"> … hero … </section>
  <section class="pn half c2"> <h2 class="ph"><svg aria-hidden="true"><use href="#i-drop"/></svg>Panel title<small>what / year</small></h2> … </section>
  <section class="pn half c3"> … </section>
  <section class="pn c1"> … </section>
  <section class="pn sources" id="sources"> … Sources … </section>
</div>
```
Every panel: `<section class="pn [half] c1..c5">` with an `<h2 class="ph">` (icon + title + optional `<small>`). Keep titles short.

### Components
| Need | Markup |
|---|---|
| **Hero** (first panel) | `<section class="pn hero c1"><svg class="deco" aria-hidden="true"><use href="#i-drop"/></svg><p class="hn"><b class="ig-n" data-count="2.1" data-dec="1">2.1</b><span class="u">billion people</span></p><p class="hl">still lack safely managed drinking water.</p><p class="hs">WHO / UNICEF JMP, 2024<sup class="src"><a href="#s1">1</a></sup></p></section>` |
| **Count-up number** (anywhere) | `<b class="ig-n" data-count="354" [data-dec="1"] [data-pre="≈"] [data-suf="%"]>354</b>` — the **written text is the final value** and must equal `data-count` plus prefix/suffix (decimals = `data-dec`; thousands commas are added by the script: write `4,515` for `4515`). It counts up from 0 when the panel scrolls into view; with reduced motion, no JS, print or the validator it just shows the written value. A mismatch FAILS validation. |
| **Stat tiles** (3–4) | `<div class="tiles"><div class="tile c1"><svg aria-hidden="true"><use href="#i-wave"/></svg><p class="tn"><b class="ig-n" data-count="106">106</b><span class="u">million</span></p><p class="tl">label (≤ 8 words)</p><p class="tc">context · 2024<sup class="src"><a href="#s1">1</a></sup></p></div>…</div>` |
| **Pictogram** ("7 in 10") | `<div class="ig-picto" data-total="10" data-filled="7" data-icon="drop" data-color="c1" data-label="≈7 in 10" data-note="short explanation"></div>` — 1–100 icons, `data-size="small|medium|big"` (auto by count). The label's "N in M" must match filled/total (WARN if not). `data-icon` is any icon id below without `i-`. |
| **Bars** (≤ 14) | `<div class="ig-bars" data-values='[["Asia",2.9],["Europe",0.7,"c2"]]' data-unit=" bn" data-title="…"></div>` — optional `data-pre="$"`, `data-dec`, `data-max`, `data-color` (default `c1`); a third item per row sets that bar's colour (`c1`–`c5`, `muted`). Values are printed as text next to each bar. |
| **Stacked bar** (parts of a whole, ≤ 8) | `<div class="ig-stack" data-values='[["Ice",68.7,"c1"],["Ground",30.1,"c2"]]' data-unit="%" [data-total="100"]></div>` — parts must not exceed the total; a legend with values is added. |
| **Donut** (several shares, ≤ 6) | `<div class="ig-donut" data-values='[["Farming",71,"c2"],["Industry",15,"c3"]]' data-unit="%" data-center="71%" data-center-label="farming"></div>` |
| **Ring** (one share) | `<div class="ig-ring" data-value="96.5" data-total="100" data-unit="%" data-label="is in the oceans" data-color="c1"></div>` |
| **Comparison** (A vs B) | `<div class="cmp"><div class="side c4"><svg aria-hidden="true"><use href="#i-drop"/></svg><span class="cn"><b class="ig-n" data-count="2.1" data-dec="1" data-suf=" bn">2.1 bn</b></span><span class="cl">label</span><span class="cc">source line, 2024<sup class="src"><a href="#s1">1</a></sup></span></div><span class="vs" aria-hidden="true">vs</span><div class="side c5">…</div></div>` |
| **Step strip** (3–5) | `<ol class="strip"><li class="c1"><svg aria-hidden="true"><use href="#i-globe"/></svg><b class="ig-n" data-count="2.5" data-dec="1" data-pre="≈" data-suf="%">≈2.5%</b><span>short label<sup class="src"><a href="#s2">2</a></sup></span></li>…</ol>` — arrows are added. Works for a funnel, a sequence or a short mini-timeline. |
| **Did you know?** | `<aside class="dyk c3"><svg aria-hidden="true"><use href="#i-idea"/></svg><div><b>Did you know?</b><p>One short sentence with a year.<sup class="src"><a href="#s2">2</a></sup></p></div></aside>` |
| **Quote / callout** | `<blockquote class="quote c1">“Short quote.”<cite>Name, source, year<sup class="src"><a href="#s3">3</a></sup></cite></blockquote>` (only real, exactly quoted words) |
| **Figure + source line** | wrap a chart: `<figure class="fig"><div class="ig-bars" …></div><figcaption class="fg">One-line note, year. Source: Name<sup class="src"><a href="#s3">3</a></sup></figcaption></figure>` |
| **Legend** (when colour carries meaning) | `<ul class="lg"><li class="c3"><span class="sw2"></span>Rocky planets</li>…</ul>` |
| **Spacing** | `class="mt"` on a block inside a panel adds space above it |
| **Sources** (required) | see below |

**Sources panel** (always last; required whenever there is a stat):
```html
<section class="pn sources" id="sources">
  <h2 class="ph"><svg aria-hidden="true"><use href="#i-book"/></svg>Sources</h2>
  <ol class="src-list">
    <li id="s1"><b>Publisher, report title</b>, 2025 — used for 2.1 bn and 3.4 bn. <a href="https://example.org/report">example.org/report</a></li>
    <li id="s2">…</li>
  </ol>
  <p class="note">Estimates and simplifications: … what is rounded (≈), what is derived, what is a model estimate, what was left out.</p>
</section>
```
Each source: **name, year, a working https link** (shown as text, so it prints). Say which numbers it supports. If you
could only reach a secondary report of the original, say "as reported by …". The superscripts must match the ids.

- **Short text only.** Tile label ≤ 8 words, panel title ≤ 6 words, no paragraph over 40 words (WARN).
- **Accessibility:** charts get a visually hidden data table and an `aria-label` automatically (`data-title`
  becomes its name). Values are always printed as text, never only as bar length. Don't use colour alone: legends and
  value labels carry the meaning.
- **Colours:** only the classes `c1`–`c5` (and `muted`). No hard-coded colours.

### Handwritten style (optional — OFF by default)
The clean style is the default; leave `data-style` out. Add `data-style="handwritten"` on the poster div
(`<div class="ig" id="ig" data-style="handwritten">`) **only when the user asks for it** — they say handwritten,
notebook style, or "like my class notes". Never choose it on your own because the topic is a school or revision
topic, and keep it out of the default example markup. It gives ruled paper, a red margin, handwriting fonts (Kalam /
Caveat), highlighter fills and a sticky-note "Did you know?". Nothing else changes (same data, same sources). It loads
the two fonts from Google Fonts; offline it falls back to a system handwriting font. These pages have no theme button
(always paper), and they print on white without the ruled lines.

**Icons** (`#i-…` in panel headings, tiles, comparison sides, strips, `data-icon`): `sun cloud rain drop wave wind
leaf sprout tree mountain fire thermo bolt atom flask cell dna heart eye user users home factory bank truck globe flag
laptop phone server db cpu code gear link lock key shield search mail chat coin cart chart target idea doc book clock
cal star check alert x loop`. Unknown names fail validation.

### What the page does by itself
- Draws bars, stacked bars, donuts, rings and pictograms from the data attributes; each gets a hidden table.
  Bad JSON or an unknown icon shows a visible error box and fails validation.
- Counts the `ig-n` numbers up, grows bars and rings, and pops in pictogram icons when a panel scrolls into view
  (not with reduced motion, not in print).
- **Print:** light palette, portrait A4, panels never split, theme button hidden. **Phones:** one column.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium); otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py page.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py page.html --out <dir>
```
It FAILS on leftover placeholders, external resources (Google Fonts only for the handwritten style), unknown icon
ids, chart data that does not parse or draw, a missing Sources section when the page has statistics, a source
reference that points nowhere, a count-up whose final value differs from the written value, JavaScript errors,
sideways page scroll, text sticking out of its panel or clipped, overlapping elements, and a print layout that is not
light or still shows the theme button. It WARNS on a stat with no source reference or no year, a source with no year or
link or that nothing points to, no footnote, paragraphs over 40 words, too many words, more than 8 panels, no hero,
a pictogram whose "N in M" label does not match its icons, more than 2 printed A4 pages, and hard-coded colours.
It renders `*_light.png`, `*_dark.png`, `*_mobile.png` and `*_print.pdf` (print media, A4 portrait) — **look at the
PNGs**, and open the PDF if you can. Fix anything cramped, clipped, lopsided or unreadable in either theme.
**Then re-check the numbers yourself** against your sources: the validator cannot tell if a figure is true.

## Step 5 — Deliver
- Save as `examples/003-infographic/<topic-slug>-infographic.html` (unless the user or project names another
  place — never make a new top-level folder) and deliver it per the environment (publish as an artifact / present
  the file).
- If the user wants a PDF, tell them to use the browser's **Print → Save as PDF** (or give the validator's `_print.pdf`).
- In chat, at most three lines: what the poster says (the hero stat), where the numbers come from, and an offer
  (e.g. "want it handwritten, or a different angle?"). Name anything you left out because you could not verify it.
  Don't repeat the page.

## Quality bar (self-check before delivering)
- **Every number is real, sourced, dated and correctly rounded**; estimates and derived values are marked; user data is used exactly.
- **Sources panel** lists each source with name, year and link; every stat points to one.
- Scannable in 10 seconds: one hero number, big numbers, icons, short labels; no paragraph over 40 words.
- 5–8 panels with at least four component types; colour means one thing; legends where needed.
- Charts show their values as text; the page is readable in dark, light, on a phone, and in print.
- Prints on 1–2 pages, light, panels not split; handwritten style only if the user asked.
