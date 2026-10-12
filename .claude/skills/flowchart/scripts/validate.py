#!/usr/bin/env python3
"""Validate a /flowchart page and render PNG previews.

Usage: python validate.py flow.html [--out DIR]
FAILS on: leftover {{placeholders}}, external resources, flow-spec errors (bad JSON,
unknown ids, duplicate ids), overlapping shapes, edge labels on top of shapes,
labels clipped or overlapping, sideways page scroll.
WARNS on: engine warnings (dead ends, unlabeled decision branches, unreachable steps,
bad "Try a path" routes), arrows that cut through a shape, step-count mismatch.
Writes <name>_light.png, <name>_dark.png and <name>_mobile.png. Exit 1 on any FAIL.
"""
import re, sys, json, pathlib, argparse
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252

ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--out", default=None)
a = ap.parse_args()
src = pathlib.Path(a.html).resolve(); out = pathlib.Path(a.out or src.parent); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
fails, warns = [], []

if re.search(r"\{\{[A-Z_]+\}\}", html): fails.append("unreplaced {{PLACEHOLDER}} left in file")
hosts = set(re.findall(r'(?:src|href)\s*=\s*["\']https?://([^/"\']+)', html)) - {"fonts.googleapis.com", "fonts.gstatic.com"}  # handwritten-style fonts
if hosts: fails.append(f"external resources not allowed (page must be self-contained): {sorted(hosts)}")
m = re.search(r'<script type="application/json" id="flow-spec">(.*?)</script>', html, re.S)
if not m: fails.append('no <script type="application/json" id="flow-spec"> found')
else:
    try: json.loads(m.group(1))
    except Exception as e: fails.append(f"flow-spec is not valid JSON: {e}")
icons = set(re.findall(r'"icon"\s*:\s*"([^"]+)"', m.group(1) if m else ""))
known = set(re.findall(r'<symbol id="i-([^"]+)"', html))
if icons - known: fails.append(f"unknown icon names in flow-spec: {sorted(icons - known)} (see SKILL.md list)")

JS = r"""() => {
 const r = {errors: window.__flowErrors || ['engine did not run'], warns: window.__flowWarnings || [], issues: [], crossings: []};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 const L = window.__flowLayout;
 if (L) {
   const N = L.nodes, hit = (a, b, m = 0) => a.x < b.x + b.w - m && b.x < a.x + a.w - m && a.y < b.y + b.h - m && b.y < a.y + a.h - m;
   for (let i = 0; i < N.length; i++) for (let j = i + 1; j < N.length; j++) if (hit(N[i], N[j], 2)) r.issues.push(`shapes overlap: "${N[i].id}" × "${N[j].id}"`);
   L.labels.forEach(l => N.forEach(n => { if (hit({x:l.x,y:l.y,w:l.w,h:l.h}, n, 1)) r.issues.push(`edge label "${l.text}" sits on shape "${n.id}"`); }));
   L.edges.forEach(e => {
     for (let k = 0; k < e.pts.length - 1; k++) {
       const [x1, y1] = e.pts[k], [x2, y2] = e.pts[k + 1];
       const seg = {x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || .5, h: Math.abs(y2 - y1) || .5};
       N.forEach(n => { if (n.id !== e.from && n.id !== e.to && hit(seg, n, 3)) r.crossings.push(`arrow ${e.from}→${e.to} cuts through "${n.id}"`); });
     }
   });
 }
 r.clipped = []; r.overlaps = [];
 const svg = document.querySelector('figure > svg');
 if (svg && svg.viewBox.baseVal && svg.viewBox.baseVal.width) {
   const vb = svg.viewBox.baseVal, inv = svg.getScreenCTM().inverse();
   const bbox = el => { const b = el.getBBox(), m = inv.multiply(el.getScreenCTM());
     const p = [[b.x,b.y],[b.x+b.width,b.y+b.height]].map(([x,y]) => new DOMPoint(x,y).matrixTransform(m));
     return {x:Math.min(p[0].x,p[1].x), y:Math.min(p[0].y,p[1].y), width:Math.abs(p[1].x-p[0].x), height:Math.abs(p[1].y-p[0].y)}; };
   const boxes = [];
   svg.querySelectorAll('text').forEach(t => {
     if (!t.textContent.trim()) return;
     const b = bbox(t);
     if (b.x < vb.x - 2 || b.y < vb.y - 2 || b.x + b.width > vb.x + vb.width + 2 || b.y + b.height > vb.y + vb.height + 2) r.clipped.push(t.textContent.trim().slice(0, 30));
     if (!t.closest('.badge')) boxes.push([t.textContent.trim().slice(0, 24), b]);
   });
   for (let j = 0; j < boxes.length; j++) for (let k = j + 1; k < boxes.length; k++) {
     const A = boxes[j][1], B = boxes[k][1];
     const ox = Math.min(A.x + A.width, B.x + B.width) - Math.max(A.x, B.x), oy = Math.min(A.y + A.height, B.y + B.height) - Math.max(A.y, B.y);
     if (ox > 2 && oy > 0.3 * Math.min(A.height, B.height)) r.overlaps.push(`"${boxes[j][0]}" × "${boxes[k][0]}"`);
   }
 }
 r.badges = document.querySelectorAll('figure .badge').length;
 r.steps = document.querySelectorAll('ol.steps > li').length;
 r.height = document.documentElement.scrollHeight;
 return r;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, scheme in (("light", 1100, "light"), ("dark", 1100, "dark"), ("mobile", 390, "light")):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1.5, color_scheme=scheme)
        # pages open in Deep dark and ignore the OS setting; the ☀/☾ toggle stores the choice here
        pg.add_init_script(f"try {{ localStorage.setItem('vs-theme', '{scheme}'); }} catch (e) {{}}")
        js_errors = []
        pg.on("pageerror", lambda e: js_errors.append(str(e)))
        pg.goto(src.as_uri()); pg.wait_for_timeout(300)
        pg.evaluate("() => window.__flowReady")   # the engine draws after the fonts are ready
        pg.wait_for_timeout(300)
        if name == "light" and pg.evaluate("document.documentElement.classList.contains('hand')") \
                and not pg.evaluate("document.fonts.check('16px Kalam')"):
            warns.append("handwriting web font not loaded (offline?) - fallback font in use")
        r = pg.evaluate(JS)
        if js_errors: fails.append(f"{name}: JavaScript error: {js_errors[0]}")
        if r["overflow"] > 1: fails.append(f"{name}: page scrolls sideways by {r['overflow']}px")
        if name == "light":
            fails += [f"flow-spec: {e}" for e in r["errors"]]
            warns += [f"flow-spec: {w_}" for w_ in r["warns"]]
            fails += r["issues"]
            warns += sorted(set(r["crossings"]))
            fails += [f"label clipped outside viewBox - {c}" for c in r["clipped"]]
            fails += [f"labels overlap - {o}" for o in r["overlaps"]]
            if r["steps"] and r["badges"] != r["steps"]:
                warns.append(f"{r['badges']} numbered steps in the chart but {r['steps']} in the reading guide")
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {scheme}, {r['height']}px tall)")
    b.close()

for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
