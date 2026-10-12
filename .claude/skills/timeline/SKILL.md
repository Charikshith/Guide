---
name: timeline
description: Show how anything changed over time as a clean, interactive timeline page — a true-to-scale (or evenly spaced) time axis, event cards alternating above and below with lines to their exact dates, optional coloured era bands, optional lanes (parallel tracks such as "Science" and "Politics"), events that last a while shown as bars, a Play walkthrough in date order, hover and click-to-focus, light and dark mode, and an optional handwritten notebook style when asked. Use this whenever the user types /timeline, or asks for a timeline, a chronology, "the history of X", "how X evolved / developed over time", "key events of X", "in order of date", a revision timeline or a project history, even if they don't say "timeline". For a step-by-step process use /flowchart; for a topic's connected ideas use /mindmap; for a general explainer visual use /visualize.
---

# /timeline — anything → its story in date order

The output is ONE self-contained HTML page: an eyebrow, a headline with a colour accent, a
lede, fact chips, **the timeline** (drawn automatically by a built-in layout engine), era focus
buttons, a small legend, a numbered reading guide with a Play walkthrough, 3 takeaways and a
footnote. Light + dark mode, no external assets.

**You describe the events as data; the engine draws them.** Never hand-place cards or lines —
the engine puts every event at its exact date, measures the text, stacks cards into extra rows so
they never overlap, draws a straight line from each card to its point, marks eras, and fits the
canvas. Dates are the whole point: **every date must be right.**

**Page theme:** pages open in the **Deep dark** theme. A ☀/☾ button (built into the template, top right)
switches to the light theme and remembers the choice; the device's own dark mode is ignored.
Don't remove the button or add your own theme CSS. Check both themes (the validator renders both).

## Usage
`/timeline <topic>` — optional extras: audience, depth ("simple", "detailed"), a date range,
`handwritten`, language. Defaults: general audience, 8–14 events, eras when the story has phases.

If the user gives only `/timeline` with no topic, ask for the topic in one short line.

## Step 1 — Understand the topic
Decide what the story is, then pick the events.
- **Events**: 8–14 turning points that someone would need to tell the story. Not every date —
  the ones that changed things. Keep a similar level of detail between events.
- **Eras** (optional, 3–5): the phases of the story ("Early networks", "Shared rules"). Use them when the
  story has clear chapters. Eras should follow each other without gaps or overlaps.
- **Lanes** (optional, 2–4): only when two or three tracks run in parallel and the user cares
  about comparing them ("science vs politics", "us vs a competitor"). Skip lanes otherwise.
- **Major** events (3–5 at most): the ones the whole story turns on. They get bigger cards.
- Order: list the events **oldest first**.

**Fact-check — dates are the #1 risk.** For every event:
- Use a date you are sure of. If you are not sure of the day, give only the month or the year.
  Never invent a precise date to look neat.
- Use `"c. "` for approximate dates (`"c. 3000 BCE"`). BCE years are written `"44 BCE"` or `"-44"`.
  There is no year 0 (1 BCE is followed by 1 CE).
- Say what a date means: "first public message", "signed", "announced", "went on sale" are
  different dates for the same thing. Pick one and make the label match.
- For events that lasted a while (a battle, a war, a reign), give `date` and `to`.
- Don't mix calendars or time zones silently; if an event has two common dates, pick one and
  name the choice in the footnote.
- Say "simplified" in the footnote and name what you left out and any date you are less sure of.

## Step 2 — Write the timeline spec (JSON)
Put it at the end of the content in `<script type="application/json" id="tl-spec">`.

```json
{
  "eras": [
    {"from": "1969", "to": "1983-01-01", "label": "Early networks"},
    {"from": "1983-01-01", "to": "1991", "label": "Shared rules", "color": "c2"}
  ],
  "events": [
    {"date": "1969-10-29", "label": "First ARPANET message", "sub": "UCLA to Stanford", "icon": "link", "major": true},
    {"date": "1971", "label": "Email on ARPANET", "icon": "mail"},
    {"date": "1983-01-01", "label": "ARPANET switches to TCP/IP", "icon": "globe", "major": true},
    {"date": "1989-03", "label": "The web is proposed", "icon": "idea"}
  ]
}
```
(Real JSON has no comments. This example is cut short — a real timeline has 8–14 events.)

| Field | Meaning |
|---|---|
| `events[].date` | `"1969"`, `"1969-07"`, `"1969-07-20"`, `"c. 3000 BCE"`, `"44 BCE"`, `"-500"` |
| `events[].to` | optional end date, for something that lasted a while (drawn as a bar on the axis) |
| `events[].label` | ≤ 6 words, a noun phrase (what happened) |
| `events[].sub` | optional one short line of detail (≤ 10 words) |
| `events[].icon` | optional icon name (see list). Give every event an icon, or none |
| `events[].major` | `true` for the 3–5 key events |
| `events[].era` | optional era `label` or `id`; by default the era that contains the date |
| `events[].lane` | the lane `id` — required on every event when `lanes` exist |
| `events[].step` | optional number for the reading guide (see below) |
| `events[].color` | optional `c1`–`c5` (default: its lane's colour, else its era's colour) |
| `events[].when` | optional text shown instead of the computed date text |
| `eras[]` | `{"from", "to", "label", "color"?, "id"?}` — coloured band; default colours cycle blue, green, amber, rose, violet |
| `lanes[]` | `{"id", "label", "color"?}` — parallel tracks, top to bottom |
| `scale` | `"auto"` (default), `"linear"` (true spacing) or `"even"` (equal spacing, marked with a break symbol where time jumps) |

**Scale:** leave it out. `auto` uses true spacing, and switches to equal spacing when the dates are
so uneven that cards would pile up (it then shows a break mark where time jumps). Say
`"scale": "linear"` only when true spacing is the point (e.g. "show how recent it all is").

**Steps (reading guide + Play):** by default each *era* is one step (every event of the era lights
up together), and with no eras each *event* is one step, in date order. The reading guide has
**one `<li>` per step, in the same order**. To group events differently, give `step` numbers
(1, 2, 3 … no gaps, in date order; an event with no `step` joins the previous event's step).

**Style** (optional, top level — **off by default**): the clean style is the default; leave
`style` out. Add `"style": "handwritten"` **only when the user asks for it** — they say
handwritten, notebook style, or "like my class notes". Don't switch to it on your own because
the topic is a school or revision topic. It turns the page into a notebook page — ruled paper,
red margin, handwriting fonts (Kalam / Caveat), wobbly pen lines, highlighter fills, circled
step numbers and sticky-note takeaways. Nothing else changes: same spec, layout and
walkthrough. It loads the two fonts from Google Fonts; offline it falls back to a system
handwriting font.

Keep it readable: 8–14 events (the validator warns above 20), at most 5 eras, at most 4 lanes.
A bigger story → split it into two timelines, or merge detail into one event and say so in the footnote.

## Step 3 — Build the page from the template
Copy `assets/template.html` (in this skill's folder). Replace `{{TITLE}}` (plain text),
`{{HEADLINE}}` (may contain `<span class="accent">`), `{{FORM}}` (e.g. `Timeline · History`),
`{{LEDE}}` (≤ 25 words), and put this where `<!-- CONTENT GOES HERE -->` is:

```html
<ul class="chips"><li><b>13</b> turning points</li><li>…</li></ul>
<figure class="stage">
  <svg id="tl" class="tl" role="group" aria-label="one-sentence summary of the timeline"></svg>
  <figcaption>Each card is joined to its exact date on the line. Hover a card to light up its point, or click an era to focus on it.</figcaption>
</figure>
<p class="scroll-hint">← swipe the timeline →</p>   <!-- shows on phones only -->
<div class="tl-tools" id="tl-tools"></div>          <!-- era focus buttons, filled automatically -->
<ul class="legend" id="tl-legend"></ul>             <!-- filled automatically -->
<h2>How to read it</h2>
<ol class="steps"><li class="c1"><b>Era or event name</b><span>One or two sentences.</span></li>…</ol>
<h2>Key takeaways</h2>
<div class="cards"><div class="card c1"><svg><use href="#i-idea"/></svg><b>Insight</b><p>…</p></div>…</div>
<p class="note">Simplified: …</p>
<script type="application/json" id="tl-spec">{ … }</script>
```
- Reading guide: **one `<li>` per step**, in date order. The `li` colour class (`c1`–`c5`) must match the
  colour of that step's first event — normally its era's colour (the validator warns if not).
  Each text must make sense on its own — the Play walkthrough shows it as a caption while lighting
  up those events. Include the years in the text ("1969–1982. …").
- Takeaways: the main insight (the pattern across time), a common mix-up (`i-alert`), and a "so what".
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
.venv\Scripts\python <skill-dir>/scripts/validate.py timeline.html --out <dir>
# macOS / Linux
.venv/bin/python <skill-dir>/scripts/validate.py timeline.html --out <dir>
```
It FAILS on bad JSON, dates it cannot read, unknown icons, lanes, eras or colours, an end date
before the start date, cards overlapping, lines cutting through cards, labels overlapping or on a
card, text spilling out of a card, clipped text, JavaScript errors and sideways scrolling. It
WARNS on events out of date order in the spec, too many or too few events, too many `major`
events, overlapping eras, events outside every era, step-count or step-colour mismatch with the
reading guide, crowded dates and too-long labels. It renders `*_light.png`, `*_dark.png`,
`*_mobile.png` — **look at them**. If cards crowd together: drop a minor event, shorten labels
or sub-text, or set `"scale": "even"`.

## Step 5 — Deliver
- Save as `examples/011-timeline/<topic-slug>-timeline.html` (unless the user or project names
  another place — never make a new top-level folder) and deliver it per the environment
  (publish as an artifact / present the file).
- If the user wants an image, also give the light PNG.
- In chat, at most two lines: what the timeline covers and an offer (e.g. "want just one era
  zoomed in, or lanes to compare two tracks?"). Don't repeat the page.

## Quality bar (self-check before delivering)
- **Every date is correct** and means what the label says; approximate dates have `c.`; BCE is marked.
- 8–14 events, listed oldest first; 3–5 `major` events at most; labels are short noun phrases.
- Eras (if used) follow each other and cover every event; lanes only when parallel tracks matter.
- The reading guide has one step per era (or per event), in date order, colours matching.
- The footnote says what was simplified or left out, and any date you are less sure of.
