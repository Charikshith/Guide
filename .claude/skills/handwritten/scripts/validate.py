#!/usr/bin/env python3
"""Validate a /handwritten notes page and render PNG previews.

Usage: python validate.py notes.html [--out DIR]
Checks: leftover {{placeholders}}, external hosts, handwriting font in use,
horizontal overflow at desktop + phone width, SVG labels clipped outside
their viewBox, text overlapping other text inside diagrams.
Writes <name>_desktop.png and <name>_mobile.png. Exit code 1 on any FAIL.
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
hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', html)) - {"fonts.googleapis.com", "fonts.gstatic.com"}
if hosts: fails.append(f"external resources not allowed: {sorted(hosts)}")
if len(html.encode()) > 2_000_000: warns.append("file > 2 MB")

JS = r"""() => {
 const r = {};
 r.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
 r.fontFamily = getComputedStyle(document.querySelector('.page')||document.body).fontFamily;
 r.handFont = ['Kalam','Patrick Hand','Caveat'].some(f => document.fonts.check(`20px "${f}"`));
 r.clipped = []; r.overlaps = [];
 document.querySelectorAll('figure svg').forEach((svg, i) => {
   const vb = svg.viewBox.baseVal; if (!vb || !vb.width) return;
   const boxes = [];
   svg.querySelectorAll('text').forEach(t => {
     const b = t.getBBox();
     if (b.x < vb.x - 2 || b.y < vb.y - 2 || b.x + b.width > vb.x + vb.width + 2 || b.y + b.height > vb.y + vb.height + 2)
       r.clipped.push(`fig${i+1}: "${t.textContent.trim().slice(0,30)}"`);
     boxes.push([t.textContent.trim().slice(0,20), b]);
   });
   for (let j=0;j<boxes.length;j++) for (let k=j+1;k<boxes.length;k++){
     const A=boxes[j][1], B=boxes[k][1];
     const ox=Math.min(A.x+A.width,B.x+B.width)-Math.max(A.x,B.x), oy=Math.min(A.y+A.height,B.y+B.height)-Math.max(A.y,B.y);
     if (ox>3 && oy>0.45*Math.min(A.height,B.height)) r.overlaps.push(`fig${i+1}: "${boxes[j][0]}" × "${boxes[k][0]}"`);
   }
 });
 r.height = document.documentElement.scrollHeight;
 return r;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w in (("desktop", 1000), ("mobile", 390)):
        pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=1.5)
        pg.goto(src.as_uri()); pg.wait_for_timeout(1200)
        pg.evaluate("document.fonts.ready")
        r = pg.evaluate(JS)
        if r["overflow"] > 1: fails.append(f"{name}: page scrolls sideways by {r['overflow']}px")
        if not r["handFont"]: warns.append(f"{name}: handwriting web font not loaded (offline?) — fallback in use")
        if name == "desktop":
            fails += [f"label clipped outside viewBox — {c}" for c in r["clipped"]]
            fails += [f"labels overlap — {o}" for o in r["overlaps"]]
        shot = out / f"{src.stem}_{name}.png"
        pg.screenshot(path=str(shot), full_page=True)
        print(f"rendered {shot}  ({w}px wide, {r['height']}px tall)")
    b.close()

for w_ in warns: print("WARN:", w_)
for f in fails: print("FAIL:", f)
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
