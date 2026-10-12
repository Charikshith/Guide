#!/usr/bin/env python3
"""Validate an /infographic page and render previews.

Usage: python validate.py infographic.html [--out DIR]
FAILS on: leftover {{placeholders}} or the CONTENT marker, external resources (Google Fonts are allowed only for
the handwritten style), unknown icon ids (markup and data-icon), no .ig container, chart data that does not parse
or does not draw, a missing Sources section when the page has statistics, a source reference that points nowhere,
a count-up number whose final value differs from the written value, JavaScript errors, sideways page scroll,
text sticking out of its panel, overlapping elements, and a print layout that is not light or still shows the theme button.
WARNS on: a statistic with no source reference or no year, a source with no year / no link, an unused source, no
footnote on estimates, too much prose (a paragraph over 40 words), more than 8 panels, no hero number, a pictogram whose
count does not match its "N in M" label, a chart without its hidden data table, more than 2 printed A4 pages,
hard-coded colours in the content.
Writes <name>_light.png, <name>_dark.png, <name>_mobile.png and <name>_print.pdf (print media, A4 portrait).
Exit 1 on any FAIL.
"""
import re, sys, json, pathlib, argparse
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252

MAX_PANELS = 8       # panels (not counting Sources) before the poster counts as too long
MAX_PAGES = 2        # printed A4 pages before the poster counts as too long
MAX_PARA_WORDS = 40  # words in one paragraph before it counts as prose
MAX_WORDS = 520      # words in all panels together (Sources excluded)

ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--out", default=None)
a = ap.parse_args()
src = pathlib.Path(a.html).resolve(); out = pathlib.Path(a.out or src.parent); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
fails, warns = [], []

# ---------- static checks ----------
if re.search(r"\{\{[A-Z_]+\}\}", html): fails.append("unreplaced {{PLACEHOLDER}} left in file")
if "CONTENT GOES HERE" in html: fails.append("the 'CONTENT GOES HERE' marker is still in the file")
hand = bool(re.search(r'<div[^>]*class="[^"]*\big\b[^"]*"[^>]*data-style="handwritten"|<div[^>]*data-style="handwritten"[^>]*class="[^"]*\big\b', html))
fonts = {"fonts.googleapis.com", "fonts.gstatic.com"}
# external resources: anything a browser would load (<a href> links are fine; the Sources list needs them)
hosts = set()
for tag in re.findall(r"<(?:link|script|img|iframe|source|video|audio|embed|object)\b[^>]*>", html, flags=re.I):
    hosts |= set(re.findall(r'(?:src|href|data)\s*=\s*["\']https?://([^/"\']+)', tag))
if re.search(r"url\(\s*['\"]?https?://", html): hosts.add("(css url())")
bad_hosts = hosts - fonts
if bad_hosts: fails.append(f"external resources not allowed (page must be self-contained): {sorted(bad_hosts)}")
if hosts & fonts and not hand: fails.append("Google Fonts link in a page that is not handwritten style (the clean style is fully offline)")
m = re.search(r"<main\b.*?</main>", html, re.S); body = m.group(0) if m else html
if 'class="ig"' not in body and not re.search(r'class="ig\b', body): fails.append('no <div class="ig"> container found')
known = set(re.findall(r'<symbol id="i-([^"]+)"', html))
used = set(re.findall(r'<use\s+href="#i-([^"]+)"', body)) | set(re.findall(r'data-icon="([^"]+)"', body))
if used - known: fails.append(f"unknown icon ids: {sorted(used - known)} (see SKILL.md list)")
if re.search(r"(?<![&\w\"'=-])#[0-9a-fA-F]{3,8}\b|rgba?\(", re.sub(r"<style.*?</style>|<script.*?</script>|href=\"[^\"]*\"", "", body, flags=re.S)):
    warns.append("hard-coded colours in the content - use the c1..c5 classes so both themes work")
if 'class="chips"' not in body: warns.append('no header chips (<ul class="chips">)')

# chart data must parse (the page script draws the charts from it)
CHART = re.compile(r"<div\b[^>]*class=\"[^\"]*\big-(bars|stack|donut)\b[^\"]*\"[^>]*>", re.S)
import html as _h
n_charts = 0
for mm in CHART.finditer(body):
    n_charts += 1
    am = re.search(r"data-values=(?:'([^']*)'|\"([^\"]*)\")", mm.group(0))
    kind = mm.group(1)
    if not am: fails.append(f"ig-{kind}: no data-values attribute"); continue
    raw = _h.unescape(am.group(1) if am.group(1) is not None else am.group(2))
    try:
        v = json.loads(raw)
        if not isinstance(v, list) or not v or any((not isinstance(r, list) or len(r) < 2 or not isinstance(r[0], str)
                                                    or isinstance(r[1], bool) or not isinstance(r[1], (int, float)) or r[1] < 0) for r in v):
            raise ValueError("must be a list of [label, number] pairs")
        if kind in ("stack", "donut"):
            tm = re.search(r'data-total="([\d.]+)"', mm.group(0)); tot = float(tm.group(1)) if tm else sum(r[1] for r in v)
            if sum(r[1] for r in v) > tot * 1.005: raise ValueError(f"parts add up to {sum(r[1] for r in v)}, more than the total {tot}")
    except Exception as e:
        fails.append(f"ig-{kind}: data-values is not usable ({e})")
for mm in re.finditer(r"<div\b[^>]*class=\"[^\"]*\big-ring\b[^\"]*\"[^>]*>", body):
    n_charts += 1
    t = mm.group(0); vm = re.search(r'data-value="([^"]*)"', t); tm = re.search(r'data-total="([^"]*)"', t)
    try:
        val = float(vm.group(1)); tot = float(tm.group(1)) if tm else 100.0
        if not (0 <= val <= tot): raise ValueError("value outside 0..total")
    except Exception as e:
        fails.append(f"ig-ring: data-value / data-total not usable ({e})")
for mm in re.finditer(r"<div\b[^>]*class=\"[^\"]*\big-picto\b[^\"]*\"[^>]*>", body):
    n_charts += 1
    t = mm.group(0)
    try:
        tot = int(re.search(r'data-total="([^"]*)"', t).group(1)); fil = int(re.search(r'data-filled="([^"]*)"', t).group(1))
        if not (1 <= tot <= 100 and 0 <= fil <= tot): raise ValueError("data-filled must be between 0 and data-total (1-100)")
        lm = re.search(r'data-label="([^"]*)"', t)
        if lm:
            nm = re.search(r"(\d+)\s*(?:in|of|out of)\s*(\d+)", _h.unescape(lm.group(1)))
            if nm and (int(nm.group(1)), int(nm.group(2))) != (fil, tot):
                warns.append(f"pictogram label says {nm.group(1)} in {nm.group(2)} but data-filled/data-total is {fil}/{tot}")
            elif nm is None and re.search(r"\d", _h.unescape(lm.group(1))) is None:
                pass
    except Exception as e:
        fails.append(f"ig-picto: {e if isinstance(e, ValueError) else 'data-total / data-filled missing or not whole numbers'}")

# count-up numbers: the written text IS the final value
NUM = re.compile(r"-?[\d,]*\.?\d+")
n_stats = 0
for mm in re.finditer(r"<(\w+)\b([^>]*class=\"[^\"]*\big-n\b[^\"]*\"[^>]*)>(.*?)</\1>", body, re.S):
    n_stats += 1
    attrs, text = mm.group(2), _h.unescape(re.sub(r"<[^>]+>", "", mm.group(3))).strip()
    cm = re.search(r'data-count="([^"]*)"', attrs)
    if not cm: fails.append(f"stat \"{text}\" has class ig-n but no data-count"); continue
    nm = NUM.search(text)
    if not nm: fails.append(f"stat \"{text}\" has no number in its written text"); continue
    try:
        written, cnt = float(nm.group(0).replace(",", "")), float(cm.group(1))
    except ValueError:
        fails.append(f"stat \"{text}\": data-count \"{cm.group(1)}\" is not a number"); continue
    if abs(written - cnt) > 1e-9: fails.append(f"count-up mismatch: written \"{text}\" but data-count={cm.group(1)} (the page would end on {cnt})")
    dm = re.search(r'data-dec="(\d+)"', attrs); dec = int(dm.group(1)) if dm else 0
    wd = len(nm.group(0).split(".")[1]) if "." in nm.group(0) else 0
    if wd != dec: fails.append(f"count-up format mismatch: \"{text}\" shows {wd} decimals but data-dec={dec}")
    pm = re.search(r'data-pre="([^"]*)"', attrs); sm = re.search(r'data-suf="([^"]*)"', attrs)
    exp = _h.unescape((pm.group(1) if pm else "") ) + nm.group(0) + _h.unescape(sm.group(1) if sm else "")
    if text.replace(" ", " ") != exp.replace(" ", " "):
        fails.append(f"count-up text mismatch: written \"{text}\" but the script would show \"{exp}\" (check data-pre / data-suf)")
n_stats += n_charts

# sources
sec = re.search(r'<section\b[^>]*class="[^"]*\bsources\b[^"]*"[^>]*>.*?</section>', body, re.S)
src_ids = {}
if n_stats:
    if not sec: fails.append("no Sources section (<section class=\"pn sources\">) but the page has statistics - every stat needs a source")
    else:
        items = re.findall(r'<li\b([^>]*)>(.*?)</li>', sec.group(0), re.S)
        if not items: fails.append("the Sources section has no list items (<ol class=\"src-list\"><li id=\"s1\">…)")
        for attrs, inner in items:
            im = re.search(r'id="([^"]+)"', attrs); txt = re.sub(r"<[^>]+>", "", inner)
            lab = txt.strip()[:50]
            if not im: warns.append(f"source \"{lab}\" has no id (stats cannot point to it)")
            else: src_ids[im.group(1)] = txt
            if not re.search(r"\b(19|20)\d\d\b", txt): warns.append(f"source \"{lab}\" has no year")
            if not re.search(r'<a\s[^>]*href="https?://', inner): warns.append(f"source \"{lab}\" has no link (https://…)")
        refs = set(re.findall(r'<sup class="src"[^>]*>\s*<a[^>]*href="#([^"]+)"', body))
        for r_ in sorted(refs - set(src_ids)): fails.append(f"a source reference points to #{r_} but no Sources item has that id")
        for u_ in sorted(set(src_ids) - refs): warns.append(f"source #{u_} is listed but no statistic points to it")
if 'class="note"' not in body: warns.append('no footnote (<p class="note">) saying what is estimated or simplified')
if 'class="ig-n' not in body and n_charts == 0: warns.append("no statistics at all (no ig-n numbers, no charts) - an infographic is built on numbers")

# ---------- in-page checks ----------
JS = r"""(mode) => {
 const r = {errors: window.__igErrors || ['page script did not run'], issues: [], warns: []};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 const vis = e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0; };
 const label = e => (e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : '') + ' "' + e.textContent.trim().replace(/\s+/g, ' ').slice(0, 28) + '"');
 const panels = [...document.querySelectorAll('.ig > .pn')].filter(vis);
 const body = panels.filter(p => !p.classList.contains('sources'));
 r.panels = body.length; r.height = document.documentElement.scrollHeight;
 if (!document.querySelector('.ig > .pn.hero')) r.warns.push('no hero panel (<section class="pn hero">) with the giant number');
 // sources / years on every stat
 const units = '.tile, .hero, .side, .fig, .dyk, blockquote';
 const hasRef = u => u && u.querySelector('sup.src a[href^="#"], .srcline');
 const seen = new Set();
 document.querySelectorAll('.ig-n, .ig-bars, .ig-stack, .ig-donut, .ig-ring, .ig-picto').forEach(e => {
   if (e.closest('.sources')) return;
   if (e.classList.contains('ig-n') && e.closest('.ig-donut, .ig-ring')) return;
   const u = e.closest(units) || e.closest('.strip li') || e.closest('.pn');
   if (seen.has(u)) return; seen.add(u);
   const name = label(u).slice(0, 60);
   if (!hasRef(u)) r.warns.push('statistic without a source reference: ' + name + ' (add <sup class="src"><a href="#s1">1</a></sup> or a Source line)');
   const yearScope = u.closest('.strip') ? u.closest('.pn') : u;
   if (!/(?<!\d)(19|20)\d\d(?!\d\d)/.test(yearScope.textContent)) r.warns.push('statistic with no year / "as of": ' + name);
 });
 // after the animation has settled the count-ups must be at their final value; charts must have drawn
 document.querySelectorAll('.ig-n[data-count]').forEach(n => {
   const m = n.textContent.match(/-?[\d,]*\.?\d+/); const got = m ? parseFloat(m[0].replace(/,/g, '')) : NaN;
   if (mode === 'screen' && Math.abs(got - parseFloat(n.dataset.count)) > 1e-9) r.issues.push('count-up ended on "' + n.textContent + '" not ' + n.dataset.count);
 });
 document.querySelectorAll('.ig-bars, .ig-stack, .ig-donut, .ig-ring').forEach(c => {
   if (c.querySelector('.ig-err')) return;
   if (!c.querySelector('table.vh')) r.warns.push('chart without its hidden data table: ' + label(c));
   if (!c.children.length) r.issues.push('chart did not draw: ' + label(c));
 });
 document.querySelectorAll('.ig-picto').forEach(c => { if (!c.querySelector('.pic-g svg') && !c.querySelector('.ig-err')) r.issues.push('pictogram did not draw'); });
 // prose
 let words = 0;
 body.forEach(p => { words += p.innerText.split(/\s+/).filter(Boolean).length; });
 r.words = words;
 document.querySelectorAll('.ig > .pn:not(.sources) p').forEach(p => {
   if (p.classList.contains('note')) return;
   const n = p.textContent.split(/\s+/).filter(Boolean).length;
   if (n > MAXPARA) r.warns.push('paragraph of ' + n + ' words (max ' + MAXPARA + ', an infographic is numbers + short labels): "' + p.textContent.trim().slice(0, 40) + '…"');
 });
 // layout
 const inter = (A, B, m) => Math.min(A.right, B.right) - Math.max(A.left, B.left) > m && Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top) > m;
 panels.forEach(s => {
   const title = ((s.querySelector('.ph') || s.querySelector('.hn') || {textContent: 'panel'}).textContent || '').trim().slice(0, 28);
   const sb = s.getBoundingClientRect();
   s.querySelectorAll('*').forEach(e => {
     if (e.closest('svg') || e.closest('.vh') || e.classList.contains('deco') || !vis(e)) return;
     const b = e.getBoundingClientRect();
     if (b.right > sb.right + 1.5 || b.left < sb.left - 1.5 || b.bottom > sb.bottom + 1.5) r.issues.push('"' + title + '": ' + label(e) + ' sticks out of its panel');
     const cs = getComputedStyle(e);
     if (cs.display !== 'inline' && e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1 && !/auto|scroll|hidden/.test(cs.overflowX))
       r.issues.push('"' + title + '": text spills out of ' + label(e));
     if (cs.overflow === 'hidden' && e.clientWidth > 0 && e.tagName !== 'I' && e.scrollWidth > e.clientWidth + 1 && !e.classList.contains('b-t'))
       r.issues.push('"' + title + '": text is clipped in ' + label(e));
   });
   const L = [...s.querySelectorAll('h2.ph, .hn, .hl, .hs, .tile, .tn, .tl, .tc, .b-row > *, .stk, .lg li, .dn-fig, .dn > .lg, .pic-g, .pic-l, .cmp > *, .side > *, .strip li, .strip li > *, .dyk, .dyk > *, .quote, .fg, .srcline, .src-list li, .note')].filter(vis);
   for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) {
     if (L[i].contains(L[j]) || L[j].contains(L[i])) continue;
     if (inter(L[i].getBoundingClientRect(), L[j].getBoundingClientRect(), 1.5)) r.issues.push('overlap: ' + label(L[i]) + ' x ' + label(L[j]));
   }
 });
 for (let i = 0; i < panels.length; i++) for (let j = i + 1; j < panels.length; j++)
   if (inter(panels[i].getBoundingClientRect(), panels[j].getBoundingClientRect(), 2)) r.issues.push('panels overlap: ' + label(panels[i]) + ' x ' + label(panels[j]));
 return r;
}""".replace("MAXPARA", str(MAX_PARA_WORDS))

PRINT_JS = r"""() => {
 const lum = c => { const m = c.match(/[\d.]+/g).map(Number); return (m[0] + m[1] + m[2]) / 3; };
 const d = e => e ? getComputedStyle(e).display : 'none';
 const pn = document.querySelector('.ig > .pn');
 return {bg: getComputedStyle(document.body).backgroundColor, ink: getComputedStyle(document.body).color,
   bgL: lum(getComputedStyle(document.body).backgroundColor), inkL: lum(getComputedStyle(document.body).color),
   pnBg: pn && !/rgba\(.*, 0\)|transparent/.test(getComputedStyle(pn).backgroundColor) ? lum(getComputedStyle(pn).backgroundColor) : 255, toggle: d(document.querySelector('.theme-toggle')),
   avoid: pn ? getComputedStyle(pn).breakInside : '', sections: document.querySelectorAll('.ig > .pn:not(.sources)').length};
}"""

SCROLL_JS = r"""async () => {
 const h = document.documentElement.scrollHeight;
 for (let y = 0; y <= h; y += 300) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
 window.scrollTo(0, 0);
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
        pg.evaluate("() => window.__igReady")   # handwriting fonts (if any) are loaded first
        if name == "light" and pg.evaluate("document.documentElement.classList.contains('hand')") \
                and not pg.evaluate("document.fonts.check('16px Kalam')"):
            warns.append("handwriting web font not loaded (offline?) - fallback font in use")
        pg.evaluate(SCROLL_JS); pg.wait_for_timeout(1700)     # scroll through so every panel animates, then let it settle
        r = pg.evaluate(JS, "screen")
        if js_errors: fails.append(f"{name}: JavaScript error: {js_errors[0]}")
        if r["overflow"] > 1: fails.append(f"{name}: page scrolls sideways by {r['overflow']}px")
        fails += [f"{name}: {e}" for e in r["errors"]]
        fails += [f"{name}: {i}" for i in r["issues"][:8]]
        if name == "light":
            warns += sorted(set(r["warns"]))
            if r["panels"] > MAX_PANELS: warns.append(f"{r['panels']} panels - too many for a poster (aim for 6-{MAX_PANELS}, not counting Sources)")
            if 0 < r["panels"] < 4: warns.append(f"only {r['panels']} panels - a poster usually has 5-{MAX_PANELS}")
            if r["words"] > MAX_WORDS: warns.append(f"{r['words']} words in the panels - too much text; keep numbers, icons and short labels")
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {scheme}, {r['height']}px tall, {r['panels']} panels)")
        if name == "dark":
            # print must be light paper even though the screen theme is dark
            pg.emulate_media(media="print"); pg.wait_for_timeout(250)
            pr = pg.evaluate(PRINT_JS); rp = pg.evaluate(JS, "print")
            if pr["bgL"] < 235: fails.append(f"print: page background is not light ({pr['bg']})")
            if pr["inkL"] > 110: fails.append(f"print: text colour is not dark ({pr['ink']})")
            if pr["pnBg"] < 225 and "hand" not in pg.evaluate("document.documentElement.className"): fails.append("print: panels are not light")
            if pr["toggle"] != "none": fails.append("print: the theme toggle is still visible")
            if pr["avoid"] != "avoid": fails.append("print: panels may split across pages (break-inside must be avoid)")
            fails += [f"print: {i}" for i in rp["issues"][:8] if not i.startswith("count-up")]
            pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
            data = pdf_path.read_bytes()
            pages = len(re.findall(rb"/Type\s*/Page(?![s\w])", data)) or None
            print(f"rendered {pdf_path}  (A4 portrait, print media, {pages} page(s))")
            if pages and pages > MAX_PAGES: warns.append(f"prints on {pages} A4 pages - aim for {MAX_PAGES} or fewer: cut a panel or shorten one")
        pg.close()
    b.close()

if req_hosts - fonts - {""}: fails.append(f"the page requested external hosts at runtime: {sorted(req_hosts - fonts)}")
for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})", f"| printed pages: {pages}")
sys.exit(1 if fails else 0)
