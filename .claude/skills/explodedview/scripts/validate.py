#!/usr/bin/env python3
"""Validate an /explodedview page and render PNG previews.

Usage: python validate.py page.html [--out DIR]
FAILS on: leftover {{placeholders}}, external resources (Google Fonts only in the handwritten style), raster <img>,
missing icon/marker ids, JavaScript errors, sideways page scroll, labels or parts outside the viewBox, labels /
balloons overlapping each other (checked in the EXPLODED state), parts whose boxes overlap each other when exploded,
parts that do not come back to their assembled place at 0%, a balloon number without a parts-list row (or the other
way round), duplicate part numbers, a print layout that is not light, not exploded, or still shows the controls.
WARNS on: missing assembly order (data-order), reading-guide steps that do not match the orders, more than 14 parts,
parts that never move, a label sitting on another part, hard-coded colours, no icons, no parts list.
Writes <name>_light.png, _dark.png, _mobile.png (page as it opens: exploded), _assembled.png, _exploded.png
and _print.pdf. Exit 1 on any FAIL.
"""
import re, sys, pathlib, argparse
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252

ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--out", default=None)
a = ap.parse_args()
src = pathlib.Path(a.html).resolve(); out = pathlib.Path(a.out or src.parent); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
fails, warns = [], []

hand = bool(re.search(r'data-style\s*=\s*"[^"]*hand', html))
if re.search(r"\{\{[A-Z_]+\}\}", html): fails.append("unreplaced {{PLACEHOLDER}} left in file")
hosts = set(re.findall(r'(?:src|href)\s*=\s*["\']https?://([^/"\']+)', html))
if hand: hosts -= {"fonts.googleapis.com", "fonts.gstatic.com"}        # handwritten-style fonts only
if hosts: fails.append(f"external resources not allowed (page must be self-contained): {sorted(hosts)}")
if re.search(r'<img\b', html, re.I): fails.append("raster <img> found - draw the parts in SVG")
body = html.split("<main", 1)[-1]
hard = re.findall(r'(?:fill|stroke)\s*=\s*"(#[0-9a-fA-F]{3,8}|rgb[^"]*|(?:red|blue|green|black|white|orange|purple))"', body)
if hard: warns.append(f"hard-coded colours in markup ({len(hard)}) - use .c0-.c5 classes so dark mode works")
ids = set(re.findall(r'\bid="([^"]+)"', html))
refs = set(re.findall(r'(?:href|xlink:href)="#([^"]+)"', html)) | set(re.findall(r'url\(#([^)]+)\)', body))
missing = sorted(refs - ids)
if missing: fails.append(f"references to missing ids (icon/marker names?): {missing}")
if not re.search(r'href="#i-', body): warns.append("no icons used - the takeaway cards need icons (see SKILL.md)")
if not re.search(r'class="[^"]*\bev-part\b', body): fails.append('no <g class="ev-part"> parts found')
if "ev-list" not in body: warns.append("no parts list (table.ev-list) - balloons need a list to point at")
if len(html.encode()) > 2_000_000: warns.append("file over 2 MB")

JS = r"""() => {
 const r = {};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 r.errors = window.__evErrors || [];
 const svg = document.querySelector('.stage > svg');
 r.hasBar = !!document.querySelector('.ev-bar input[type=range]');
 if (!svg) { r.nosvg = true; return r; }
 const vb = svg.viewBox.baseVal, inv = svg.getScreenCTM().inverse();
 const bbox = el => {
   const b = el.getBBox(), m = inv.multiply(el.getScreenCTM());
   const ps = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y]) => new DOMPoint(x,y).matrixTransform(m));
   const xs = ps.map(p=>p.x), ys = ps.map(p=>p.y);
   return {x:Math.min(...xs), y:Math.min(...ys), w:Math.max(...xs)-Math.min(...xs), h:Math.max(...ys)-Math.min(...ys)};
 };
 const parts = [...svg.querySelectorAll('.ev-part')];
 const uni = (a, b) => { if (!b) return a; const x0 = Math.min(a.x, b.x), y0 = Math.min(a.y, b.y), x1 = Math.max(a.x + a.w, b.x + b.w), y1 = Math.max(a.y + a.h, b.y + b.h); return {x: x0, y: y0, w: x1 - x0, h: y1 - y0}; };
 const lateOf = n => svg.querySelector('.ev-latepart[data-n="' + n + '"]');
 r.parts = parts.map(p => ({n: p.dataset.n || '', order: p.dataset.order || '', name: p.getAttribute('aria-label') || '', b: uni(bbox(p), lateOf(p.dataset.n) && bbox(lateOf(p.dataset.n))),
   moves: p.dataset.dx != null || p.dataset.dy != null || p.dataset.gap != null}));
 r.base = (window.__ev ? window.__ev.parts : []).map(p => p.bb);
 r.balloons = [...svg.querySelectorAll('.ev-b')].map(b => b.dataset.n);
 r.rows = [...document.querySelectorAll('.ev-list tbody tr')].map(tr => tr.dataset.n || '');
 r.steps = document.querySelectorAll('ol.steps > li').length;
 r.orders = [...new Set(parts.map(p => p.dataset.order).filter(Boolean))].length;
 r.pos = window.__ev ? window.__ev.pos() : [];
 /* labels: every text except the number inside a balloon, plus the balloon discs */
 const lab = [];
 svg.querySelectorAll('text').forEach(t => { if (!t.classList.contains('bn') && !t.classList.contains('ev-face')) lab.push(['"' + t.textContent.trim().slice(0, 24) + '"', bbox(t), t]); });
 svg.querySelectorAll('.ev-b .bc').forEach(c => lab.push(['balloon ' + c.parentNode.dataset.n, bbox(c), c]));
 r.clipped = []; r.overlaps = []; r.onPart = [];
 lab.forEach(([nm, b, el]) => {
   if (b.x < vb.x - 2 || b.y < vb.y - 2 || b.x + b.w > vb.x + vb.width + 2 || b.y + b.h > vb.y + vb.height + 2) r.clipped.push(nm);
 });
 for (let j = 0; j < lab.length; j++) for (let k = j + 1; k < lab.length; k++) {
   const A = lab[j][1], B = lab[k][1];
   const ox = Math.min(A.x+A.w, B.x+B.w) - Math.max(A.x, B.x), oy = Math.min(A.y+A.h, B.y+B.h) - Math.max(A.y, B.y);
   if (ox > 2 && oy > 2) r.overlaps.push(lab[j][0] + ' x ' + lab[k][0]);
 }
 lab.forEach(([nm, b, el]) => {
   const own = (el.closest('.ev-b') || {dataset: {}}).dataset.n;
   r.parts.forEach(p => {
     if (p.n === own) return;
     const ox = Math.min(b.x+b.w, p.b.x+p.b.w) - Math.max(b.x, p.b.x), oy = Math.min(b.y+b.h, p.b.y+p.b.h) - Math.max(b.y, p.b.y);
     if (ox > 6 && oy > 6) r.onPart.push(nm + ' over part ' + p.n);
   });
 });
 r.partsOut = r.parts.filter(p => p.b.x < vb.x - 2 || p.b.y < vb.y - 2 || p.b.x + p.b.w > vb.x + vb.width + 2 || p.b.y + p.b.h > vb.y + vb.height + 2).map(p => p.n);
 r.partOverlaps = [];
 const T = 2;
 for (let j = 0; j < r.parts.length; j++) for (let k = j + 1; k < r.parts.length; k++) {
   const A = r.parts[j].b, B = r.parts[k].b;
   const ox = Math.min(A.x+A.w, B.x+B.w) - Math.max(A.x, B.x), oy = Math.min(A.y+A.h, B.y+B.h) - Math.max(A.y, B.y);
   if (ox > T && oy > T) r.partOverlaps.push(`${r.parts[j].n} (${r.parts[j].name.replace(/^\d+:\s*/, '')}) x ${r.parts[k].n} (${r.parts[k].name.replace(/^\d+:\s*/, '')})`);
 }
 r.height = document.documentElement.scrollHeight;
 return r;
}"""
SET = "v => { const g = document.querySelector('.ev-bar input[type=range]'); g.value = v; g.dispatchEvent(new Event('input', {bubbles: true})); }"


def near(p, q, tol=0.6):
    return all(abs(p[k] - q[k]) <= tol for k in ("x", "y", "w", "h"))


def lum(s):
    return sum(int(v) for v in re.findall(r'\d+', s)[:3]) / 3


with sync_playwright() as pw:
    b = pw.chromium.launch()
    for name, w, scheme in (("light", 1100, "light"), ("dark", 1100, "dark"), ("mobile", 390, "light")):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1.5, color_scheme=scheme)
        errs = []
        pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)))
        pg.on("console", lambda m, errs=errs: errs.append(m.text) if m.type == "error" and "ERR_" not in m.text else None)
        # pages open in Deep dark and ignore the OS setting; the sun/moon toggle stores the choice here
        pg.add_init_script(f"try {{ localStorage.setItem('vs-theme', '{scheme}'); }} catch (e) {{}}")
        pg.goto(src.as_uri()); pg.evaluate("() => window.__evReady"); pg.wait_for_timeout(500)
        r = pg.evaluate(JS)
        if errs: fails.append(f"{name}: JavaScript errors: {errs[:3]}")
        if r.get("nosvg"): fails.append("no .stage > svg found"); break
        for e in r["errors"]: fails.append(f"{name}: engine error: {e}")
        if not r["hasBar"]: fails.append(f"{name}: the Assemble/Explode controls were not built (engine did not run?)")
        if r["overflow"] > 1: fails.append(f"{name}: page scrolls sideways by {r['overflow']}px")
        if name == "light":
            # ---- as opened: should be exploded ----
            if r["pos"] and min(r["pos"]) < 0.99: warns.append('the page does not open fully exploded (data-start="assembled"?)')
            # ---- data checks ----
            ns = [x["n"] for x in r["parts"]]
            if len(set(ns)) != len(ns): fails.append(f"duplicate part numbers (data-n): {sorted({n for n in ns if ns.count(n) > 1})}")
            for x in r["parts"]:
                if not x["n"]: fails.append("a .ev-part has no data-n")
            bal, rows = set(r["balloons"]), set(r["rows"])
            for n in sorted(bal - rows, key=lambda s: (len(s), s)): fails.append(f'balloon {n} has no parts-list row (tr[data-n="{n}"])')
            for n in sorted(rows - bal, key=lambda s: (len(s), s)): fails.append(f"parts-list row {n} has no part / balloon in the drawing")
            if len(r["parts"]) > 14: warns.append(f"{len(r['parts'])} parts - more than ~14 is hard to read; group small parts (screws) into one")
            noorder = [x["n"] for x in r["parts"] if not x["order"]]
            if noorder: warns.append(f"no data-order on part(s) {noorder} - the assembly order is guessed from the markup order")
            ords = sorted({int(x["order"]) for x in r["parts"] if x["order"].isdigit()})
            if ords and ords != list(range(1, len(ords) + 1)): warns.append(f"data-order values {ords} are not 1..N without gaps")
            if r["steps"] and r["orders"] and r["steps"] != r["orders"]:
                warns.append(f"{r['orders']} assembly orders but {r['steps']} steps in the reading guide")
            if not r["steps"]: warns.append("no ol.steps reading guide - 'Play assembly' needs it")
            if sum(1 for x in r["parts"] if x["moves"]) < len(r["parts"]) - 1:
                warns.append("some parts have no data-dx/data-dy/data-gap - they will not move (only the base part may stay)")
            if r["partsOut"]: fails.append(f"parts outside the viewBox (exploded): {r['partsOut']}")
            fails += [f"label or balloon clipped outside the viewBox (exploded) - {c}" for c in r["clipped"]]
            fails += [f"labels/balloons overlap (exploded) - {o}" for o in r["overlaps"]]
            fails += [f"parts overlap each other when exploded - {o}" for o in r["partOverlaps"]]
            warns += [f"{o} (exploded)" for o in r["onPart"]]
            exploded_boxes = [x["b"] for x in r["parts"]]
            # ---- slider: 0 -> assembled, 100 -> exploded, 0 again ----
            pg.evaluate(SET, 0); pg.wait_for_timeout(150); a1 = pg.evaluate(JS)
            shot = out / f"{src.stem}_assembled.png"; pg.screenshot(path=str(shot), full_page=True)
            print(f"rendered {shot}  (assembled)")
            fill = pg.evaluate("() => { const s = document.querySelector('.stage > svg').getBoundingClientRect(); const rs = [...document.querySelectorAll('.ev-part')].map(p => p.getBoundingClientRect()); return (Math.max(...rs.map(r => r.right)) - Math.min(...rs.map(r => r.left))) / s.width; }")
            if fill < 0.5: warns.append(f"the assembled object fills only {fill:.0%} of the stage width - raise data-zoom (default 2.6) or check data-fit")
            if a1["partsOut"]: fails.append(f"parts outside the viewBox (assembled): {a1['partsOut']}")
            for x, base in zip(a1["parts"], a1["base"]):
                if not near(x["b"], base):
                    fails.append(f"part {x['n']} does not sit at its assembled place at 0% (off by {x['b']['x']-base['x']:.1f},{x['b']['y']-base['y']:.1f})")
            pg.evaluate(SET, 100); pg.wait_for_timeout(150); e1 = pg.evaluate(JS)
            shot = out / f"{src.stem}_exploded.png"; pg.screenshot(path=str(shot), full_page=True)
            print(f"rendered {shot}  (exploded)")
            for x, y in zip(e1["parts"], exploded_boxes):
                if not near(x["b"], y): fails.append(f"part {x['n']} does not return to the same exploded place at 100%")
            pg.evaluate(SET, 0); pg.wait_for_timeout(150); a2 = pg.evaluate(JS)
            for x, y in zip(a2["parts"], a1["parts"]):
                if not near(x["b"], y["b"]): fails.append(f"part {x['n']} does not come back to its assembled place after exploding")
            # ---- print: light, exploded, list included, controls hidden ----
            pg.wait_for_timeout(50)                                        # still assembled here: print must explode it
            pg.emulate_media(media="print"); pg.wait_for_timeout(300)
            pr = pg.evaluate(JS)
            if pr["pos"] and min(pr["pos"]) < 0.99: fails.append("print layout is not the EXPLODED state")
            bg = pg.evaluate("() => getComputedStyle(document.body).backgroundColor"); ink = pg.evaluate("() => getComputedStyle(document.querySelector('h1')).color")
            if lum(bg) < 200 or lum(ink) > 120: fails.append(f"print layout is not light (background {bg}, headline {ink})")
            if pg.evaluate("() => { const b = document.querySelector('.ev-bar'); return !!b && getComputedStyle(b).display !== 'none'; }"):
                fails.append("print layout still shows the Assemble/Explode controls")
            if pg.evaluate("() => { const t = document.querySelector('.ev-list'); return !t || getComputedStyle(t).display === 'none'; }"):
                fails.append("print layout has no parts list")
            pdf = out / f"{src.stem}_print.pdf"
            try:
                pg.pdf(path=str(pdf), format="A4", print_background=True); print(f"rendered {pdf}  (print)")
            except Exception as ex:
                warns.append(f"could not write the print PDF: {ex}")
            pg.emulate_media(media="screen")
            pg.evaluate(SET, 100); pg.wait_for_timeout(200)
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {scheme}, {r['height']}px tall)")
        pg.close()
    b.close()

for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
