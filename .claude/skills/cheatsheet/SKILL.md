---
name: cheatsheet
description: Make a dense, scannable, printable quick-reference page (a cheat sheet / revision guide) — colour-grouped section cards in a masonry-style grid with key→value rows, compact tables, copyable code snippets, formulas, "gotcha" and tip callouts, a mnemonic box and starred "most used" rows, plus live search that filters and highlights, a "Most used" filter, a comfortable/compact toggle, a Print / Save PDF button, light and dark mode, a print layout that fits 1–2 pages, and an optional handwritten notebook style when asked. Use this whenever the user types /cheatsheet, or asks for a cheat sheet, quick reference, quick-reference card, revision sheet, formula sheet, "one-pager", "commands I need", syntax summary or last-minute revision guide, even if they don't say "cheat sheet". For a long explanation use /visualize; for notebook-style study notes with diagrams use /handwritten; for a topic's connected ideas use /mindmap.
---

# /cheatsheet — any topic → a one-page quick reference

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent, a one-line
scope (lede), small chips, a toolbar (**search**, **Most used**, **Compact**, **Print / Save PDF**),
then **6–10 section cards** in a multi-column grid, and a footnote saying what was simplified or
left out. Light + dark mode, no external assets (Google Fonts only in the optional handwritten style).

It is a **reference, not an article**: short rows, no paragraphs, nothing the reader must read in order.
Every row must be something a person would look up. Cut everything else.

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).
**Printing is always light** (white paper, dark ink), whatever theme is on screen: the template does this
for you, and hides the toolbar and the toggle.

## Usage
`/cheatsheet <topic>` — optional extras: audience or level ("beginner", "Class 10", "interview"), version
("Python 3.12"), size ("1 page", "detailed"), `handwritten`, language.
Defaults: general learner, the everyday core of the topic, 6–10 sections, fits 2 printed pages.

If the user gives only `/cheatsheet` with no topic, ask for the topic in one short line.

## Step 1 — Understand what a reader will look up
- **Who and when?** A learner revising, a developer mid-task, a student the night before an exam. Pick
  the level and say it in a chip. Write for someone who knows the basics but forgets the exact form.
- **What matters most?** The 20% used 80% of the time. Mark those rows with a star (`star`).
- **What to leave out:** rare options, history, long explanations, advanced corners. Name what you left out
  in the footnote. A cheat sheet that tries to cover everything is a manual.
- **Version or scope:** if commands or syntax differ by version, pick one ("Git 2.23+", "Python 3.12") and say so
  in the chip and the footnote; mark newer items with a `tag` (for example `2.23+`).

**Accuracy is the whole value.** Every command, flag, formula, syntax and number must be correct and
current. Do not guess a flag or a value to fill space. If you are not sure of a detail, leave the row out or
mark it in the footnote. For maths, check each formula and table value (substitute a test value in your head).
For commands, check the exact spelling, the flag and what it does. Say what is version-specific.

## Step 2 — Plan the content
- **6–10 sections**, each a cluster the reader would think of together ("Branches", "Undo", "Standard angles").
  Order: the order of use (set up → everyday → advanced → undo/troubleshoot).
- **Colour = topic group** (`c1`–`c5`): give related sections the same colour (all remote commands `c5`, all
  "undo" sections `c4`). Max five groups.
- **Rows per section: ≤ 12** (the validator warns above 14). Rows are short: a command or term on the left
  (≤ 4 words if possible), a few words on the right. Long left sides get `wide` (see below).
- **Per sheet**: at least one code snippet or formula block, at least one `callout warn` (a gotcha or common
  mistake, real and specific), at least one tip or mnemonic, 5–15 starred rows, a footnote.
- **Chips (3–4):** level or audience, version or scope, number of sections, "Prints on N pages" (use the number the
  validator reports; do not claim "1 page" unless it is true).
- **Fit:** the print layout is landscape, 4 columns, and must fit 1–2 pages. Columns fill left to right and a
  section never splits, so a very tall section can leave a gap: if the validator says 3 pages, move a short section
  in front of a long one, shorten a section or cut rows.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text), `{{HEADLINE}}` (may
contain `<span class="accent">`), `{{FORM}}` (e.g. `Cheat sheet · Git`), `{{LEDE}}` (≤ 25 words: the scope), and put
the following where `<!-- CONTENT GOES HERE -->` is. Don't add CSS, don't edit the template's scripts.

```html
<ul class="chips"><li><b>9</b> sections</li><li>Git <b>2.x</b></li><li>Level: <b>beginner</b></li><li>Prints on <b>2 pages</b></li></ul>

<div class="cs-bar" role="search">
  <label class="cs-search"><svg aria-hidden="true"><use href="#i-search"/></svg><input id="cs-q" type="search" placeholder="Search commands and words" aria-label="Search this cheat sheet" autocomplete="off" spellcheck="false"><kbd>/</kbd></label>
  <button class="cs-btn" id="cs-star" type="button" aria-pressed="false" title="Show only the starred rows">&#9733; Most used</button>
  <button class="cs-btn" id="cs-density" type="button" aria-pressed="false" title="Tighter spacing">Compact</button>
  <button class="cs-btn" id="cs-print" type="button">Print / Save PDF</button>
  <span class="cs-count" id="cs-count" aria-live="polite"></span>
</div>

<div class="sheet" id="sheet">
  <section class="sec c1">
    <h2 class="sh"><svg aria-hidden="true"><use href="#i-gear"/></svg>Section title<small>optional note</small></h2>
    <div class="sb">
      … components …
    </div>
  </section>
  … 6–10 sections …
</div>
<p class="note">Scope: … Left out: … A star marks the most used rows.</p>
```

### Components (put these inside `<div class="sb">`)
| Need | Markup |
|---|---|
| Key → value rows | `<dl class="kv"><div class="r"><dt><code>git init</code></dt><dd>what it does</dd></div>…</dl>` |
| Most-used row | `<div class="r star">…` (gets a star and a tinted background) |
| Long key (full-width key, value below) | `<div class="r wide">…` — use when the key is longer than about 22 characters |
| Wider key column | `<dl class="kv" style="--kcol:55%">` (default 42%) |
| Version tag | `<span class="tag">2.23+</span>` inside a `dt` or `dd` |
| Table | `<table class="tbl"><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table>` — add `center` for number grids, `grid` for lines, `math` for formula cells; `<tr class="star">` for a starred row |
| Code snippet | `<div class="code" data-lang="bash"><pre><code>line 1\nline 2 <span class="cm"># comment</span></code></pre></div>` — the script adds the label and a **Copy** button. Escape `<` as `&lt;`. No `$` prompts. Keep lines short: wide lines scroll sideways inside the block (a validator WARN). |
| Formula | `<div class="formula star" data-kw="search words"><span class="fl">Name</span><span class="eq">sin<sup>2</sup><i>θ</i> + cos<sup>2</sup><i>θ</i> = 1</span></div>` — several `.eq` lines allowed; `<small>` for a note |
| Fraction / root | `<span class="frac"><i>numerator</i><i>denominator</i></span>`, `<span class="rt">x + 1</span>` (use `<span class="nb">…</span>` to stop a line breaking) |
| Gotcha / common mistake | `<p class="callout warn"><svg aria-hidden="true"><use href="#i-alert"/></svg><span><b>Gotcha.</b> text</span></p>` |
| Tip | `<p class="callout tip"><svg aria-hidden="true"><use href="#i-idea"/></svg><span><b>Tip.</b> text</span></p>` |
| Mnemonic | `<div class="mnemo"><span class="lbl">Mnemonic</span><b>SOH · CAH · TOA</b><span>what it stands for</span></div>` |
| Mini example | `<div class="eg"><span class="lbl">Example</span>a worked one-liner</div>` |
| Small heading / small note / list | `<h3>Group</h3>` · `<p class="fine">…</p>` · `<ul class="list"><li>…</li></ul>` |

- **Search** matches the text of every row, table row, snippet, formula and callout, plus the section title. For
  formulas, symbols and superscripts do not search well (`sin²` is `sin` + `2`), so add `data-kw="pythagorean
  identity sin squared"` with the words people would type (also useful for old/new names, such as `checkout switch`).
- **Don't** put long prose paragraphs, images or nested sections in a card.
- **Colours:** only the classes `c1`–`c5` on sections. No hard-coded colours.

### Handwritten style (optional — OFF by default)
The clean style is the default; leave `data-style` out. Add `data-style="handwritten"` on the sheet div
(`<div class="sheet" id="sheet" data-style="handwritten">`) **only when the user asks for it** — they say
handwritten, notebook style, or "like my class notes". Never choose it on your own because the topic is a school
or revision topic, and keep it out of the default example markup. It gives ruled paper, a red margin, handwriting
fonts (Kalam / Caveat), highlighter fills and a sticky-note mnemonic. Nothing else changes. It loads the two
fonts from Google Fonts; offline it falls back to a system handwriting font. These pages have no theme button
(always paper), and they print on white without the ruled lines.

**Icons** (`#i-…` in section headings and callouts): `sun cloud rain drop wave wind leaf sprout tree mountain
fire thermo bolt atom flask cell dna heart eye user users home factory bank truck globe flag laptop phone server
db cpu code gear link lock key shield search mail chat coin cart chart target idea doc book clock cal star check
alert x loop`. Unknown names fail validation.

### What the page does by itself
- **Search box** (`/` focuses it, `Esc` clears it): hides rows that do not match and sections with no match, highlights
  matches, says "N of M entries match", shows a "nothing matches" message with a Clear button.
- **★ Most used**: shows only the starred rows. **Compact**: tighter spacing (remembered). **Print / Save PDF**:
  opens the print dialog.
- **Copy** buttons on snippets (keyboard accessible; the button says "Copied ✓").
- **Print:** light palette, landscape, 4 columns, sections never split, toolbar and theme button hidden, code wraps.
  Highlight and background colours are kept (the page asks the browser to print them).
- **Phones:** one column.

## Step 4 — Validate (when you have a code/computer tool)
Run it with the project's `.venv` Python if one exists (it has Playwright + Chromium); otherwise plain `python`:
```bash
# Windows
.venv\Scripts\python <skill-dir>/scripts/validate.py sheet.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py sheet.html --out <dir>
```
It FAILS on leftover placeholders, external resources (Google Fonts only for the handwritten style), unknown
icon ids, JavaScript errors, sideways page scroll, text sticking out of its section, overlapping elements or
sections, a broken search box, and a print layout that is not light or still shows the controls. Code blocks may scroll
sideways inside themselves on screen (a WARN, not a FAIL; in print they wrap). It WARNS on more than 2 printed
A4 pages, too many sections or rows, no search box, no chips, no gotcha callout, no tip or mnemonic, no starred
rows, no footnote, a bare `<pre>` (no copy button) and hard-coded colours. It renders `*_light.png`,
`*_dark.png`, `*_mobile.png` and `*_print.pdf` (print media, A4 landscape) — **look at the PNGs**, and open the
PDF if you can. Fix anything cramped, clipped, lopsided or unreadable in either theme.

## Step 5 — Deliver
- Save as `examples/059-cheatsheet/<topic-slug>-cheatsheet.html` (unless the user or project names another
  place — never make a new top-level folder) and deliver it per the environment (publish as an artifact / present
  the file).
- If the user wants a PDF, tell them to use the page's **Print / Save PDF** button (or give the validator's `_print.pdf`).
- In chat, at most two lines: what the sheet covers (and its version or level) and an offer (e.g. "want a
  1-page version, or a section added?"). Don't repeat the page.

## Quality bar (self-check before delivering)
- **Every command, flag, formula, syntax and number is correct** for the stated version; version-specific items are tagged.
- It is a reference: 6–10 sections, short rows, ≤ 12 rows each, no paragraphs; the most used rows are starred.
- Has at least one snippet or formula, one specific gotcha, one tip or mnemonic.
- Related sections share a colour; section order follows how the topic is used.
- Prints on 1–2 pages, light, columns not split; works in dark mode and on a phone.
- The footnote says the scope, the version, and what was left out.
