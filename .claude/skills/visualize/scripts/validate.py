#!/usr/bin/env python3
"""Validate a /visualize page and render PNG previews.

Usage: python validate.py visual.html [--out DIR]
Checks: leftover {{placeholders}}, external resources, hard-coded colours in the
SVG, horizontal overflow at desktop + phone width, SVG labels clipped outside the
viewBox, labels overlapping other labels, badge count vs. reading-guide steps.
Writes <name>_light.png, <name>_dark.png and <name>_mobile.png. Exit 1 on any FAIL.
"""
import re, sys, pathlib, argparse
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252

ap = argparse.ArgumentParser(); ap.add_argument("html"); ap.add_argument("--out", default=None)
a = ap.parse_args()
src = pathlib.Path(a.html).resolve(); out = pathlib.Path(a.out or src.parent); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
fails, warns = [], []

if re.search(r"\{\{[A-Z_]+\}\}", html): fails.append("unreplaced {{PLACEHOLDER}} left in file")
hosts = set(re.findall(r'(?:src|href)\s*=\s*["\']https?://([^/"\']+)', html))
if hosts: fails.append(f"external resources not allowed (page must be self-contained): {sorted(hosts)}")
if re.search(r'<img\b', html, re.I): fails.append("raster <img> found - draw the visual in SVG")
body = html.split("<main", 1)[-1]
hard = re.findall(r'(?:fill|stroke)\s*=\s*"(#[0-9a-fA-F]{3,8}|rgb[^"]*|(?:red|blue|green|black|white|orange|purple))"', body)
if hard: warns.append(f"hard-coded colours in markup ({len(hard)}) - use .c1-.c5 classes so dark mode works")
ids = set(re.findall(r'\bid="([^"]+)"', html))
refs = set(re.findall(r'(?:href|xlink:href)="#([^"]+)"', html)) | set(re.findall(r'url\(#([^)]+)\)', body))
missing = sorted(refs - ids)
if missing: fails.append(f"references to missing ids (icon/marker/path names?): {missing}")
if not re.search(r'href="#i-', body): warns.append("no icons used - give main elements an icon chip (see SKILL.md)")
if not re.search(r'class="[^"]*\b(flow|particle)\b', body): warns.append("no motion - add .flow dashes or a .particle on the main path")
if not re.search(r'data-step="', body): warns.append("no data-step groups - step highlighting will do nothing")
if len(html.encode()) > 2_000_000: warns.append("file over 2 MB")

JS = r"""() => {
 const r = {};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 r.clipped = []; r.overlaps = [];
 document.querySelectorAll('figure > svg').forEach((svg, i) => {
   const vb = svg.viewBox.baseVal; if (!vb || !vb.width) return;
   const boxes = [];
   const inv = svg.getScreenCTM().inverse();
   const bbox = el => {           // text bbox in the svg's own user space (handles transforms)
     const b = el.getBBox(), m = inv.multiply(el.getScreenCTM());
     const pts = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]]
       .map(([x,y]) => new DOMPoint(x,y).matrixTransform(m));
     const xs = pts.map(p=>p.x), ys = pts.map(p=>p.y);
     return {x:Math.min(...xs), y:Math.min(...ys), width:Math.max(...xs)-Math.min(...xs), height:Math.max(...ys)-Math.min(...ys)};
   };
   svg.querySelectorAll('text').forEach(t => {
     const b = bbox(t);
     if (b.x < vb.x - 2 || b.y < vb.y - 2 || b.x + b.width > vb.x + vb.width + 2 || b.y + b.height > vb.y + vb.height + 2)
       r.clipped.push(`fig${i+1}: "${t.textContent.trim().slice(0,30)}"`);
     if (!t.closest('.badge')) boxes.push([t.textContent.trim().slice(0,24), b]);
   });
   for (let j=0;j<boxes.length;j++) for (let k=j+1;k<boxes.length;k++){
     const A=boxes[j][1], B=boxes[k][1];
     const ox=Math.min(A.x+A.width,B.x+B.width)-Math.max(A.x,B.x), oy=Math.min(A.y+A.height,B.y+B.height)-Math.max(A.y,B.y);
     if (ox>2 && oy>0.3*Math.min(A.height,B.height)) r.overlaps.push(`fig${i+1}: "${boxes[j][0]}" × "${boxes[k][0]}"`);
   }
 });
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
        pg.goto(src.as_uri()); pg.wait_for_timeout(600)
        r = pg.evaluate(JS)
        if r["overflow"] > 1: fails.append(f"{name}: page scrolls sideways by {r['overflow']}px")
        if name == "light":
            fails += [f"label clipped outside viewBox - {c}" for c in r["clipped"]]
            fails += [f"labels overlap - {o}" for o in r["overlaps"]]
            if r["badges"] and r["steps"] and r["badges"] != r["steps"]:
                warns.append(f"{r['badges']} numbered badges in the visual but {r['steps']} steps in the reading guide")
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {scheme}, {r['height']}px tall)")
    b.close()

for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
