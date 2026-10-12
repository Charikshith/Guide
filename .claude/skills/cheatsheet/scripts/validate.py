#!/usr/bin/env python3
"""Validate a /cheatsheet page and render previews.

Usage: python validate.py sheet.html [--out DIR]
FAILS on: leftover {{placeholders}} or the CONTENT marker, external resources (Google Fonts are allowed
only for the handwritten style), unknown icon ids, no .sheet container, JavaScript errors, sideways
page scroll, text sticking out of its section, overlapping elements or sections, a broken search box,
and a print layout that is not light (white paper, dark ink) or still shows the controls.
Code blocks may scroll sideways INSIDE themselves on screen (that is not a failure; it is a WARN
because a cheat sheet should not need it). In print, code wraps.
WARNS on: more than 2 printed pages (A4), too many sections or rows, a section with too many rows,
no search box, no chips, no gotcha callout, no tip or mnemonic, no starred rows, no footnote,
a <pre> outside a .code block (no copy button), hard-coded colours in the content.
Writes <name>_light.png, <name>_dark.png, <name>_mobile.png and <name>_print.pdf (print media, A4; the sheet asks for landscape).
Exit 1 on any FAIL.
"""
import re, sys, pathlib, argparse
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252

MAX_ROWS = 14        # rows / snippets / callouts in one section before it counts as too long
MAX_PAGES = 2        # printed pages (A4) before the sheet counts as too long

ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--out", default=None)
a = ap.parse_args()
src = pathlib.Path(a.html).resolve(); out = pathlib.Path(a.out or src.parent); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
fails, warns = [], []

# ---------- static checks ----------
if re.search(r"\{\{[A-Z_]+\}\}", html): fails.append("unreplaced {{PLACEHOLDER}} left in file")
if "CONTENT GOES HERE" in html: fails.append("the 'CONTENT GOES HERE' marker is still in the file")
hand = bool(re.search(r'<div[^>]*class="[^"]*\bsheet\b[^"]*"[^>]*data-style="handwritten"|<div[^>]*data-style="handwritten"[^>]*class="[^"]*\bsheet\b', html))
fonts = {"fonts.googleapis.com", "fonts.gstatic.com"}
hosts = set(re.findall(r'(?:src|href)\s*=\s*["\']https?://([^/"\']+)', html))
bad_hosts = hosts - fonts
if bad_hosts: fails.append(f"external resources not allowed (page must be self-contained): {sorted(bad_hosts)}")
if hosts & fonts and not hand: fails.append("Google Fonts link in a page that is not handwritten style (the clean style is fully offline)")
m = re.search(r"<main\b.*?</main>", html, re.S); body = m.group(0) if m else html
if 'class="sheet' not in body: fails.append('no <div class="sheet"> container found')
known = set(re.findall(r'<symbol id="i-([^"]+)"', html))
used = set(re.findall(r'<use\s+href="#i-([^"]+)"', body))
if used - known: fails.append(f"unknown icon ids: {sorted(used - known)} (see SKILL.md list)")
if 'id="cs-q"' not in body: warns.append("no search box (<input id=\"cs-q\">) - add the toolbar from SKILL.md")
if 'class="chips"' not in body: warns.append("no header chips (<ul class=\"chips\">)")
if "callout warn" not in body: warns.append("no gotcha / common-mistake callout (class \"callout warn\")")
if "callout tip" not in body and 'class="mnemo"' not in body: warns.append("no tip callout or mnemonic box")
if not re.search(r'class="[^"]*\bstar\b', body): warns.append("no starred rows (class \"star\") - mark the most used ones")
if 'class="note"' not in body: warns.append("no footnote (<p class=\"note\">) with scope / what was left out")
if re.search(r"<pre\b", re.sub(r'<div class="code".*?</div>', "", body, flags=re.S)): warns.append("<pre> outside a .code block (it gets no copy button)")
if re.search(r"(?<![&\w\"'=-])#[0-9a-fA-F]{3,8}\b|rgba?\(", re.sub(r"<style.*?</style>|<script.*?</script>", "", body, flags=re.S)):
    warns.append("hard-coded colours in the content - use the c1..c5 classes so both themes work")

# ---------- in-page checks ----------
JS = r"""(mode) => {
 const r = {errors: window.__csErrors || ['page script did not run'], issues: [], warns: []};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 const vis = e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0; };
 const label = e => (e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : '') + ' "' + e.textContent.trim().replace(/\s+/g, ' ').slice(0, 28) + '"');
 const sheet = document.querySelector('.sheet');
 const secs = [...document.querySelectorAll('.sheet > .sec')].filter(vis);
 r.secs = secs.length;
 const UNIT = '.r, tbody tr, .code, .formula, .callout, .eg, .mnemo, ul.list > li';
 r.maxRows = 0; r.rowsTotal = 0;
 secs.forEach(s => {
   const title = (s.querySelector('.sh') || {textContent: '(no heading)'}).textContent.trim().slice(0, 30);
   if (!s.querySelector('.sh')) r.warns.push('a section has no <h2 class="sh"> heading');
   const n = [...s.querySelectorAll(UNIT)].filter(u => !u.parentElement.closest(UNIT)).length;
   r.rowsTotal += n;
   if (n > r.maxRows) r.maxRows = n;
   if (mode === 'screen' && n > MAXROWS) r.warns.push(`section "${title}" has ${n} rows (more than ${MAXROWS}): split it or cut rows`);
   if (n === 0) r.warns.push(`section "${title}" has no rows / snippets to search`);
   const sb = s.getBoundingClientRect();
   s.querySelectorAll('*').forEach(e => {
     if (e.closest('pre') || e.closest('svg') || !vis(e)) return;
     const b = e.getBoundingClientRect();
     if (b.right > sb.right + 1.5 || b.left < sb.left - 1.5) r.issues.push(`"${title}": ${label(e)} sticks out of its section`);
     const cs = getComputedStyle(e);
     if (cs.display !== 'inline' && e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1 && !/auto|scroll|hidden/.test(cs.overflowX))
       r.issues.push(`"${title}": text spills out of ${label(e)}`);
   });
   s.querySelectorAll('pre').forEach(p => { if (vis(p) && p.scrollWidth > p.clientWidth + 1 && mode === 'screen') r.warns.push(`"${title}": a code line is wider than its block (it scrolls sideways) - shorten it`); });
   if (!s.querySelector('.sh')) return;
 });
 // sections must not overlap each other
 const inter = (A, B, m) => Math.min(A.right, B.right) - Math.max(A.left, B.left) > m && Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top) > m;
 for (let i = 0; i < secs.length; i++) for (let j = i + 1; j < secs.length; j++)
   if (inter(secs[i].getBoundingClientRect(), secs[j].getBoundingClientRect(), 2)) r.issues.push(`sections overlap: ${label(secs[i])} x ${label(secs[j])}`);
 // blocks inside a section must not overlap
 secs.forEach(s => {
   const L = [...s.querySelectorAll('.sh, .sb > *, dl.kv > .r, .r > dt, .r > dd, tbody tr, tr > td, .formula, .formula > *, .callout > *, .code > *')].filter(vis);
   for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) {
     if (L[i].contains(L[j]) || L[j].contains(L[i])) continue;
     if (inter(L[i].getBoundingClientRect(), L[j].getBoundingClientRect(), 1.5)) r.issues.push(`overlap: ${label(L[i])} x ${label(L[j])}`);
   }
 });
 r.cols = sheet ? getComputedStyle(sheet).columnCount : '';
 r.height = document.documentElement.scrollHeight;
 return r;
}""".replace("MAXROWS", str(MAX_ROWS))

PRINT_JS = r"""() => {
 const lum = c => { const m = c.match(/[\d.]+/g).map(Number); return (m[0] + m[1] + m[2]) / 3; };
 const d = e => e ? getComputedStyle(e).display : 'none';
 const sec = document.querySelector('.sheet > .sec');
 return {bg: getComputedStyle(document.body).backgroundColor, ink: getComputedStyle(document.body).color,
   bgL: lum(getComputedStyle(document.body).backgroundColor), inkL: lum(getComputedStyle(document.body).color),
   secBg: sec ? lum(getComputedStyle(sec).backgroundColor) : 255,
   toggle: d(document.querySelector('.theme-toggle')), bar: d(document.querySelector('.cs-bar')),
   cols: getComputedStyle(document.querySelector('.sheet')).columnCount,
   avoid: sec ? getComputedStyle(sec).breakInside : ''};
}"""

SEARCH_JS = r"""() => {
 const q = document.getElementById('cs-q'); if (!q) return {skip: true};
 const secs = () => [...document.querySelectorAll('.sheet > .sec')];
 const shown = () => secs().filter(s => !s.hidden).length;
 const total = secs().length;
 const cells = [...document.querySelectorAll('.sheet .r dt, .sheet .r dd, .sheet tbody td')];
 const word = (cells.map(c => (c.textContent.match(/[A-Za-z]{4,}/) || [''])[0].slice(0, 6)).find(Boolean)) || (cells.map(c => (c.textContent.match(/[A-Za-z]{3,}/) || [''])[0]).find(Boolean)) || '';
 const res = {total};
 const set = v => { q.value = v; q.dispatchEvent(new Event('input', {bubbles: true})); };
 set('zzqxjv'); res.noneShown = shown(); const e = document.querySelector('.cs-empty'); res.emptyVisible = !!e && !e.hidden;
 set(word); res.wordShown = shown(); res.marks = document.querySelectorAll('mark.hit').length;
 set(''); res.restored = shown(); res.marksAfter = document.querySelectorAll('mark.hit').length;
 res.word = word;
 return res;
}"""

DARK_PATTERN = "try { localStorage.setItem('vs-theme', '%s'); } catch (e) {}"
req_hosts = set()
pdf_path = out / f"{src.stem}_print.pdf"
pages = None

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, scheme in (("light", 1100, "light"), ("dark", 1100, "dark"), ("mobile", 390, "light")):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1.5, color_scheme=scheme)
        # pages open in Deep dark and ignore the OS setting; the ☀/☾ toggle stores the choice here
        pg.add_init_script(DARK_PATTERN % scheme)
        js_errors = []
        pg.on("pageerror", lambda e: js_errors.append(str(e)))
        pg.on("request", lambda rq: req_hosts.add(rq.url.split("/")[2]) if rq.url.startswith("http") else None)
        pg.goto(src.as_uri()); pg.wait_for_timeout(300)
        pg.evaluate("() => window.__csReady")   # handwriting fonts (if any) are loaded first
        pg.wait_for_timeout(300)
        if name == "light" and pg.evaluate("document.documentElement.classList.contains('hand')") \
                and not pg.evaluate("document.fonts.check('16px Kalam')"):
            warns.append("handwriting web font not loaded (offline?) - fallback font in use")
        r = pg.evaluate(JS, "screen")
        if js_errors: fails.append(f"{name}: JavaScript error: {js_errors[0]}")
        if r["overflow"] > 1: fails.append(f"{name}: page scrolls sideways by {r['overflow']}px")
        fails += [f"{name}: {e}" for e in r["errors"]]
        fails += [f"{name}: {i}" for i in r["issues"][:8]]
        if name == "light":
            warns += sorted(set(r["warns"]))
            if r["secs"] and r["secs"] < 4: warns.append(f"only {r['secs']} sections - a cheat sheet usually has 6-10")
            if r["secs"] > 12: warns.append(f"{r['secs']} sections - too many for a cheat sheet (aim for 6-10)")
            if r["rowsTotal"] > 130: warns.append(f"{r['rowsTotal']} rows in total - too long for a cheat sheet; cut the least used")
            s = pg.evaluate(SEARCH_JS)
            if not s.get("skip"):
                if s["noneShown"] != 0 or not s["emptyVisible"]: fails.append("search: a query with no match must hide every section and show the 'no results' message")
                if s["wordShown"] == 0 or (s["marks"] == 0): fails.append(f"search: typing '{s['word']}' found nothing / highlighted nothing")
                if s["restored"] != s["total"] or s["marksAfter"]: fails.append("search: clearing the box must bring every section back and remove highlights")
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {scheme}, {r['height']}px tall, {r['cols']} column(s))")
        if name == "dark":
            # print must be light paper even though the screen theme is dark
            pg.emulate_media(media="print"); pg.wait_for_timeout(200)
            pr = pg.evaluate(PRINT_JS); rp = pg.evaluate(JS, "print")
            if pr["bgL"] < 235: fails.append(f"print: page background is not light ({pr['bg']})")
            if pr["inkL"] > 110: fails.append(f"print: text colour is not dark ({pr['ink']})")
            if pr["secBg"] < 225 and "hand" not in pg.evaluate("document.documentElement.className"): fails.append("print: section cards are not light")
            if pr["toggle"] != "none" or pr["bar"] != "none": fails.append("print: the theme toggle / toolbar are still visible")
            if pr["avoid"] != "avoid": fails.append("print: sections may split across columns/pages (break-inside must be avoid)")
            if str(pr["cols"]) in ("auto", "1"): warns.append("print: single column - a printed cheat sheet should use several columns")
            fails += [f"print: {i}" for i in rp["issues"][:8]]
            pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
            data = pdf_path.read_bytes()
            pages = len(re.findall(rb"/Type\s*/Page(?![s\w])", data)) or None
            print(f"rendered {pdf_path}  (A4, print media, {pages} page(s))")
            if pages and pages > MAX_PAGES: warns.append(f"prints on {pages} A4 pages - too long for a cheat sheet (aim for 1-2): cut rows or sections")
        pg.close()
    b.close()

if req_hosts - fonts - {""}: fails.append(f"the page requested external hosts at runtime: {sorted(req_hosts - fonts)}")
for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})", f"| printed pages: {pages}")
sys.exit(1 if fails else 0)
