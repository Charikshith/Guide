#!/usr/bin/env python3
"""Validate a /thenvsnow page and render previews.

Usage: python validate.py page.html [--out DIR]
FAILS on: leftover {{placeholders}} or the CONTENT marker, external resources (links with <a href> are fine; Google Fonts
are allowed only for the handwritten style), unknown icon ids, no .tn container, JavaScript errors, sideways page scroll,
text sticking out of its box or overlapping, unparseable / unconvertible metric data (data-then / data-now), a written
% (data-pct) or x (data-x) that does not match the then/now values, a .tn-fill that points nowhere, figures but no
Sources section, a data-src that points to a missing source, THEN >= NOW years, a broken slider (the handle must exist, be
focusable and move with the arrow keys and with a drag), a broken % / x toggle, and a print layout that is not light, still shows
the controls, or does not show both scenes side by side.
WARNS on: more than 10 metrics, figures (metrics) without a data-src, sources without a year or a link, missing years, a panel year that differs
from the page years, no metrics, no "what changed / stayed" lists, no biggest-change or why box, milestones that are not
between the two years, more than 2 printed A4 pages, ol.steps that do not match the data-step numbers, hard-coded colours.
Writes <name>_light.png, <name>_dark.png, <name>_mobile.png and <name>_print.pdf (print media, A4 portrait).
Exit 1 on any FAIL.
"""
import re, sys, pathlib, argparse
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252

MAX_PAGES = 2        # printed pages (A4) before the page counts as too long

ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--out", default=None)
a = ap.parse_args()
src = pathlib.Path(a.html).resolve(); out = pathlib.Path(a.out or src.parent); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
fails, warns = [], []

# ---------- static checks ----------
if re.search(r"\{\{[A-Z_]+\}\}", html): fails.append("unreplaced {{PLACEHOLDER}} left in file")
if "CONTENT GOES HERE" in html: fails.append("the 'CONTENT GOES HERE' marker is still in the file")
hand = bool(re.search(r'<div[^>]*class="[^"]*\btn\b[^"]*"[^>]*data-style="handwritten"|<div[^>]*data-style="handwritten"[^>]*class="[^"]*\btn\b', html))
fonts = {"fonts.googleapis.com", "fonts.gstatic.com"}
# resources the page loads: src= on anything, href= on anything except plain <a> links (those are only references)
hosts = set(re.findall(r'<(?!a\b)[a-zA-Z][^>]*?\s(?:src|href)\s*=\s*["\']https?://([^/"\']+)', html)) | set(re.findall(r'\ssrc\s*=\s*["\']https?://([^/"\']+)', html))
bad_hosts = hosts - fonts
if bad_hosts: fails.append(f"external resources not allowed (page must be self-contained): {sorted(bad_hosts)}")
if hosts & fonts and not hand: fails.append("Google Fonts link in a page that is not handwritten style (the clean style is fully offline)")
m = re.search(r"<main\b.*?</main>", html, re.S); body = m.group(0) if m else html
if 'class="tn"' not in body and not re.search(r'class="tn[ "]', body): fails.append('no <div class="tn"> container found')
known = set(re.findall(r'<symbol id="i-([^"]+)"', html))
used = set(re.findall(r'<use\s+href="#i-([^"]+)"', body)) | set(re.findall(r'data-icon="([^"]+)"', body))
if used - known: fails.append(f"unknown icon ids: {sorted(used - known)} (see SKILL.md list)")
if 'class="chips"' not in body: warns.append('no header chips (<ul class="chips">)')
if 'class="note"' not in body: warns.append('no footnote (<p class="note">) with what was simplified / left out')

mt = re.search(r'class="tn"[^>]*', body)
tag = mt.group(0) if mt else ""
ty = re.search(r'data-then-year="([^"]*)"', tag); ny = re.search(r'data-now-year="([^"]*)"', tag)
ty = ty.group(1) if ty else None; ny = ny.group(1) if ny else None
yr_ok = lambda s: bool(s and re.fullmatch(r"-?\d{1,4}", s.strip()))
if not yr_ok(ty) or not yr_ok(ny): warns.append('the two years are missing: put data-then-year="1984" data-now-year="2025" on <div class="tn">')
elif int(ty) >= int(ny): fails.append(f"THEN year ({ty}) must be earlier than NOW year ({ny})")
for side, y in (("then", ty), ("now", ny)):
    mm = re.search(rf'class="tn-panel {side}"[^>]*>.*?class="tn-y">([^<]*)<', body, re.S)
    if y and mm and mm.group(1).strip() != y: warns.append(f"the {side.upper()} panel shows year '{mm.group(1).strip()}' but the page year is {y}")
    if not mm: warns.append(f"no .tn-panel.{side} (hero panel with the year)")

metrics = re.findall(r'<div[^>]*class="tn-metric"[^>]*>', body)
if not metrics: warns.append("no .tn-metric rows (the numbers are the point of a then-vs-now page)")
if len(metrics) > 10: warns.append(f"{len(metrics)} metrics - too many to take in; aim for 5-7")
src_ids = set(re.findall(r'<li[^>]*\bid="src-([^"]+)"', body))
src_block = re.search(r'<ol[^>]*class="tn-src"[^>]*>(.*?)</ol>', body, re.S)
src_items = re.findall(r"<li\b[^>]*>(.*?)</li>", src_block.group(1), re.S) if src_block else []
if metrics and not src_items: fails.append('figures are shown but there is no Sources section (<ol class="tn-src"> with one <li id="src-N"> per source)')
for i, li in enumerate(src_items, 1):
    txt = re.sub(r"<[^>]+>", " ", li)
    if not re.search(r"\b(1[0-9]|20)\d\d\b", txt): warns.append(f"source {i} has no year")
    if not re.search(r'<a\s[^>]*href="https?://', li): warns.append(f"source {i} has no link (<a href=\"https://...\">)")
for mtag in metrics:
    lab = (re.search(r'data-label="([^"]*)"', mtag) or [None, "(no label)"])[1]
    s = re.search(r'data-src="([^"]*)"', mtag)
    if not s or not s.group(1).strip(): warns.append(f'figure "{lab}" has no data-src (which source is it from?)')
    else:
        for n in re.split(r"[,\s]+", s.group(1).strip()):
            if src_items and n and n not in src_ids: fails.append(f'figure "{lab}" cites source {n} but no <li id="src-{n}"> exists')
for mm in re.finditer(r'<li[^>]*\bdata-src="([^"]*)"', body):
    for n in re.split(r"[,\s]+", mm.group(1).strip()):
        if src_items and n and n not in src_ids: fails.append(f"a milestone cites source {n} but no <li id=\"src-{n}\"> exists")
if metrics and not re.search(r'class="tn-col changed"', body): warns.append('no "What changed" list (<section class="tn-col changed">)')
if metrics and not re.search(r'class="tn-col same"', body): warns.append('no "What stayed the same" list (<section class="tn-col same">)')
if metrics and 'class="tn-big"' not in body: warns.append('no "The biggest change" box (<div class="tn-big">)')
if metrics and 'class="tn-why"' not in body: warns.append('no "Why it changed" box (<div class="tn-why">)')
if 'class="tn-slider"' not in body: warns.append('no before/after slider (<div class="tn-slider"> with two <svg class="tn-layer then|now">)')
elif not (re.search(r'<svg[^>]*class="tn-layer then"', body) and re.search(r'<svg[^>]*class="tn-layer now"', body)): fails.append('the slider needs <svg class="tn-layer then"> and <svg class="tn-layer now">')
# steps vs data-step
steps_n = len(re.findall(r"<li\b", (re.search(r'<ol[^>]*class="steps"[^>]*>(.*?)</ol>', body, re.S) or [None, ""])[1]))
ds = {int(x) for v in re.findall(r'data-step="([^"]*)"', body) for x in v.split() if x.isdigit()}
if metrics and not steps_n: warns.append('no reading guide (<ol class="steps">) - the Play walkthrough has nothing to say')
elif ds and ds != set(range(1, steps_n + 1)): warns.append(f"ol.steps has {steps_n} items but data-step numbers are {sorted(ds)}")
elif steps_n and not ds: warns.append("ol.steps has items but no element has data-step - Play would highlight nothing")
# milestones
miles = [int(y) for y in re.findall(r'<li[^>]*\bdata-year="(-?\d+)"', body)]
if miles:
    if len(miles) < 3 or len(miles) > 5: warns.append(f"{len(miles)} milestones - aim for 3-5")
    if miles != sorted(miles): warns.append("milestones are not in date order")
    if yr_ok(ty) and yr_ok(ny) and any(not (int(ty) <= y <= int(ny)) for y in miles): warns.append("a milestone year lies outside the two years")
if re.search(r"(?<![&\w\"'=-])#[0-9a-fA-F]{3,8}\b|rgba?\(", re.sub(r"<style.*?</style>|<script.*?</script>", "", body, flags=re.S)):
    warns.append("hard-coded colours in the content - use the c1..c5 / k* classes so both themes work")

# ---------- in-page checks ----------
JS = r"""(mode) => {
 const r = {errors: window.__tnErrors || ['page script did not run'], issues: [], warns: []};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 const vis = e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0; };
 const label = e => (e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : '') + ' "' + e.textContent.trim().replace(/\s+/g, ' ').slice(0, 28) + '"');
 const inter = (A, B, m) => Math.min(A.right, B.right) - Math.max(A.left, B.left) > m && Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top) > m;
 const tn = document.querySelector('.tn');
 r.model = (window.__tnModel || []).map(m => ({label: m.label, ok: m.ok, pct: m.pct, ratio: m.ratio, claim: m.el.dataset.pct, claimX: m.el.dataset.x, text: m.ct ? m.ct.textContent : ''}));
 // boxes: nothing may stick out of its box, nothing inside may overlap
 const BOXES = '.tn-panel, .tn-metric, .tn-col, .tn-big, .tn-why, .tn-miles > li, .tn-bar, .tn-head';
 [...document.querySelectorAll(BOXES)].filter(vis).forEach(s => {
   const sb = s.getBoundingClientRect(), t = label(s);
   s.querySelectorAll('*').forEach(e => {
     if (e.closest('svg') || e.classList.contains('sr-only') || e.closest('.sr-only') || !vis(e)) return;
     const b = e.getBoundingClientRect();
     if (b.right > sb.right + 1.5 || b.left < sb.left - 1.5) r.issues.push(`${t}: ${label(e)} sticks out of its box`);
     const cs = getComputedStyle(e);
     if (cs.display !== 'inline' && e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1 && !/auto|scroll|hidden/.test(cs.overflowX)) r.issues.push(`${t}: text spills out of ${label(e)}`);
   });
   const L = [...s.querySelectorAll(':scope > *, .tn-lab > *, .tn-chg > *, .tn-val > *, .tn-bars > *, .tn-col li, .tn-panel > *')].filter(x => vis(x) && !x.classList.contains('sr-only'));
   for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) {
     if (L[i].contains(L[j]) || L[j].contains(L[i])) continue;
     if (inter(L[i].getBoundingClientRect(), L[j].getBoundingClientRect(), 1.5)) r.issues.push(`overlap in ${t}: ${label(L[i])} x ${label(L[j])}`);
   }
 });
 // metric rows must not overlap each other
 const rows = [...document.querySelectorAll('.tn-metric')].filter(vis);
 for (let i = 0; i < rows.length; i++) for (let j = i + 1; j < rows.length; j++) if (inter(rows[i].getBoundingClientRect(), rows[j].getBoundingClientRect(), 2)) r.issues.push(`metric rows overlap: ${label(rows[i])} x ${label(rows[j])}`);
 const SIDE = [...document.querySelectorAll('.tn-panel, .tn-col, .tn-big, .tn-why')].filter(vis);
 for (let i = 0; i < SIDE.length; i++) for (let j = i + 1; j < SIDE.length; j++) if (inter(SIDE[i].getBoundingClientRect(), SIDE[j].getBoundingClientRect(), 2)) r.issues.push(`boxes overlap: ${label(SIDE[i])} x ${label(SIDE[j])}`);
 // the scene text must stay inside its layer
 document.querySelectorAll('.tn-layer').forEach(sv => { if (!vis(sv)) return; const sb = sv.getBoundingClientRect();
   sv.querySelectorAll('text').forEach(t => { const b = t.getBoundingClientRect(); if (b.width && (b.left < sb.left - 1 || b.right > sb.right + 1 || b.top < sb.top - 1 || b.bottom > sb.bottom + 1)) r.issues.push(`scene text "${t.textContent.slice(0, 24)}" is outside its scene`); }); });
 r.height = document.documentElement.scrollHeight;
 r.sl = !!document.querySelector('.tn-slider .tn-handle');
 return r;
}"""

PRINT_JS = r"""() => {
 const lum = c => { const m = c.match(/[\d.]+/g).map(Number); return (m[0] + m[1] + m[2]) / 3; };
 const d = e => e ? getComputedStyle(e).display : 'none';
 const rect = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return {l: b.left, r: b.right, t: b.top, b: b.bottom, w: b.width, h: b.height}; };
 return {bgL: lum(getComputedStyle(document.body).backgroundColor), inkL: lum(getComputedStyle(document.body).color),
   toggle: d(document.querySelector('.theme-toggle')), bar: d(document.querySelector('.tn-bar')), handle: d(document.querySelector('.tn-handle')),
   then: rect('.tn-layer.then'), now: rect('.tn-layer.now'), panelBg: lum(getComputedStyle(document.querySelector('.tn-metrics') || document.body).backgroundColor)};
}"""

INTERACT_JS = r"""async () => {
 const res = {};
 const tn = document.querySelector('.tn'); const sl = tn.querySelector('.tn-slider'), h = tn.querySelector('.tn-handle');
 if (sl && h) {
   res.focusable = h.tabIndex >= 0 && h.getAttribute('role') === 'slider';
   const v0 = +h.getAttribute('aria-valuenow'); h.focus();
   h.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));
   const v1 = +h.getAttribute('aria-valuenow');
   h.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowLeft', bubbles: true})); h.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowLeft', bubbles: true}));
   const v2 = +h.getAttribute('aria-valuenow');
   h.dispatchEvent(new KeyboardEvent('keydown', {key: 'End', bubbles: true})); res.end = +h.getAttribute('aria-valuenow');
   h.dispatchEvent(new KeyboardEvent('keydown', {key: 'Home', bubbles: true})); res.home = +h.getAttribute('aria-valuenow');
   h.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));
   res.keys = [v0, v1, v2]; res.pos = getComputedStyle(sl).getPropertyValue('--pos').trim();
 }
 const rows = [...tn.querySelectorAll('.tn-metric .tn-ct')]; const bX = document.getElementById('tn-m-x'), bP = document.getElementById('tn-m-pct');
 if (rows.length && bX && bP) { const p = rows[0].textContent; bX.click(); const x = rows[0].textContent; bP.click(); res.toggle = [p, x, rows[0].textContent]; }
 else res.toggle = null;
 return res;
}"""

DARK_PATTERN = "try { localStorage.setItem('vs-theme', '%s'); } catch (e) {}"
req_hosts = set()
pdf_path = out / f"{src.stem}_print.pdf"
pages = None


def decs(s):
    mm = re.search(r"\.(\d+)", s or "")
    return len(mm.group(1)) if mm else 0


with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, scheme in (("light", 1100, "light"), ("dark", 1100, "dark"), ("mobile", 390, "light")):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1.5, color_scheme=scheme)
        # pages open in Deep dark and ignore the OS setting; the sun/moon toggle stores the choice here
        pg.add_init_script(DARK_PATTERN % scheme)
        js_errors = []
        pg.on("pageerror", lambda e: js_errors.append(str(e)))
        pg.on("request", lambda rq: req_hosts.add(rq.url.split("/")[2]) if rq.url.startswith("http") else None)
        pg.goto(src.as_uri()); pg.wait_for_timeout(300)
        pg.evaluate("() => window.__tnReady")   # handwriting fonts (if any) are loaded first
        pg.wait_for_timeout(1000)               # bars finish growing
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
            # claimed % / x must match the computed change
            for m_ in r["model"]:
                if not m_["ok"]: continue
                for key, comp, lab in (("claim", m_["pct"], "% change"), ("claimX", m_["ratio"], "x change")):
                    c = m_[key]
                    if c in (None, ""): continue
                    try: cv = float(str(c).replace(",", "").replace("−", "-").replace("+", "").replace("%", "").replace("x", "").replace("×", ""))
                    except ValueError: fails.append(f'figure "{m_["label"]}": cannot read the written {lab} "{c}"'); continue
                    tol = 0.5 * 10 ** (-decs(str(c))) + 1e-9
                    if abs(cv - comp) > tol: fails.append(f'figure "{m_["label"]}": written {lab} {c} does not match the data ({comp:.4g}) - fix the number or the data')
            ix = pg.evaluate(INTERACT_JS)
            if "keys" in ix:
                v0, v1, v2 = ix["keys"]
                if not ix.get("focusable"): fails.append("slider handle is not a focusable role=slider")
                if not (v1 > v0 and v2 < v1): fails.append(f"slider does not move with the arrow keys ({ix['keys']})")
                if ix["end"] != 100 or ix["home"] != 0: fails.append("slider End/Home keys do not reach 100 / 0")
            elif metrics or 'class="tn-slider"' in body: fails.append("the slider handle was not created (is there a .tn-slider with two layers?)")
            if ix.get("toggle"):
                t0, t1, t2 = ix["toggle"]
                if t0 == t1 or t0 != t2: fails.append(f"% / x toggle does not change the change text ({ix['toggle']})")
            elif metrics: warns.append("no % / x toggle (#tn-m-pct and #tn-m-x buttons)")
            # slider drag with the mouse
            if r["sl"]:
                sb = pg.locator(".tn-slider").bounding_box()
                if sb:
                    pg.mouse.move(sb["x"] + sb["width"] * .5, sb["y"] + sb["height"] * .5); pg.mouse.down()
                    pg.mouse.move(sb["x"] + sb["width"] * .8, sb["y"] + sb["height"] * .5, steps=4); pg.mouse.up()
                    v = int(pg.get_attribute(".tn-handle", "aria-valuenow"))
                    if not 70 <= v <= 90: fails.append(f"dragging the slider did not move the divider (aria-valuenow={v}, expected about 80)")
                    pg.evaluate("document.querySelector('.tn-handle').dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}))")
                    pg.evaluate("document.querySelector('.tn-handle').dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))")
            pg.evaluate("document.querySelector('.tn-slider') && document.querySelector('.tn-slider').style.setProperty('--pos','50%')")
            pg.evaluate("(() => { const h = document.querySelector('.tn-handle'); if (h) { h.setAttribute('aria-valuenow','50'); } })()")
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {scheme}, {r['height']}px tall)")
        if name == "dark":
            # print must be light paper even though the screen theme is dark
            pg.emulate_media(media="print"); pg.wait_for_timeout(300)
            pr = pg.evaluate(PRINT_JS); rp = pg.evaluate(JS, "print")
            if pr["bgL"] < 235: fails.append("print: page background is not light")
            if pr["inkL"] > 110: fails.append("print: text colour is not dark")
            if pr["panelBg"] < 225: fails.append("print: the number table is not light")
            if pr["toggle"] != "none" or pr["bar"] != "none": fails.append("print: the theme toggle / controls are still visible")
            if pr["handle"] != "none": fails.append("print: the slider handle is still visible")
            if pr["then"] and pr["now"]:
                if not (pr["then"]["r"] <= pr["now"]["l"] + 2 and abs(pr["then"]["t"] - pr["now"]["t"]) < 4 and pr["then"]["w"] > 100 and pr["now"]["w"] > 100):
                    fails.append("print: the two scenes are not side by side and fully visible")
            fails += [f"print: {i}" for i in rp["issues"][:8]]
            pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
            data = pdf_path.read_bytes()
            pages = len(re.findall(rb"/Type\s*/Page(?![s\w])", data)) or None
            print(f"rendered {pdf_path}  (A4, print media, {pages} page(s))")
            if pages and pages > MAX_PAGES: warns.append(f"prints on {pages} A4 pages - too long (aim for 1-2): cut rows or sections")
        pg.close()
    b.close()

if req_hosts - fonts - {""}: fails.append(f"the page requested external hosts at runtime: {sorted(req_hosts - fonts)}")
for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})", f"| printed pages: {pages}")
sys.exit(1 if fails else 0)
