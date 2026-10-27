"""Build the Guide's HTML pages (home, roadmap, one contents page per volume, one page per chapter).

Usage:  python tools/build_pages.py     (safe to re-run; writes the .html files next to the Markdown)
Output: index.html, roadmap.html, volumes/<volume>/index.html and volumes/<volume>/chNN-*.html

The Markdown chapters are the source of truth. Each page embeds its Markdown and the browser renders
it with marked (text) and mermaid (diagrams) from local copies in assets/, and Prism (code) from a CDN.

The look comes from the AI Library's course theme: assets/system-design.css, assets/home.css and
assets/system-design.js are copies of that theme, and the constants and render script below are taken
from the AI Library's build script so the two sites feel the same. Guide-only behaviour (progress
tracking, the chapter list in the sidebar, checklists) lives in assets/guide.css and assets/guide.js.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900'
         '&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">')

PRISM_CSS = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">'

PRISM_JS = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>')

def stats_block(stats):
    return ('<div class="home-stats">' + "".join(
        f'<div><div class="home-stat-num">{h(st["num"])}</div>'
        f'<div class="home-stat-label">{h(st["label"])}</div></div>' for st in stats) + '</div>')

COURSE_FONTS = FONTS.replace("800;900", "800")

COURSE_CSS = (".main .mermaid{display:flex;justify-content:center;margin:24px 0;padding:20px;"
              "background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--radius);"
              "overflow-x:auto}.main .mermaid svg{max-width:100%;height:auto}")

MARKED_JS = "assets/marked.min.js"  # local copy of marked 12.0.2, so text renders without the internet

MERMAID_JS = "assets/mermaid.min.js"  # local copy of mermaid 10.9.1, so diagrams draw without the internet

PRISM_AUTOLOADER = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/'
                    'prism-autoloader.min.js"></script>')

COURSE_RENDER_JS = r"""
var m=document.getElementById("main"),nav=m.querySelector(":scope > .chapter-nav");
var tmp=document.createElement("div");tmp.innerHTML=marked.parse(MD,{gfm:true,breaks:false});
while(tmp.firstChild){m.insertBefore(tmp.firstChild,nav);}
var seen={};
m.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach(function(hd){
 if(hd.closest(".hero"))return;
 var id=hd.textContent.trim().toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu,"").replace(/\s/g,"-");
 if(seen[id]!==undefined){id=id+"-"+(++seen[id]);}else{seen[id]=0;}hd.id=id;});
m.querySelectorAll(":scope > h2").forEach(function(hd){
 if(!/^table of contents$/i.test(hd.textContent.trim()))return;
 var n=hd.nextElementSibling;
 while(n&&n.tagName!=="H2"&&n!==nav){var x=n.nextElementSibling;n.remove();n=x;}
 var p=hd.previousElementSibling;if(p&&p.tagName==="HR")p.remove();hd.remove();});
var s2=0,s3=0,pre=typeof CH!=="undefined"?CH+".":"";
m.querySelectorAll(":scope > h2, :scope > h3").forEach(function(hd){
 var num;if(hd.tagName==="H2"){s2++;s3=0;num=pre+s2;}else{if(!s2)return;s3++;num=pre+s2+"."+s3;}
 var f=hd.firstChild;if(f&&f.nodeType===3)f.nodeValue=f.nodeValue.replace(/^\s*\d+(\.\d+)*[.)]?\s+/,"");
 var k=document.createElement("span");k.className="sec-num";k.textContent=num+" ";hd.insertBefore(k,hd.firstChild);});
var toc=document.getElementById("tocList");
m.querySelectorAll(m.querySelector(":scope > h2")?":scope > h2, :scope > h3":":scope > h1").forEach(function(hd){
 var li=document.createElement("li"),a=document.createElement("a");if(hd.tagName==="H3")li.className="toc-sub";
 a.href="#"+hd.id;a.textContent=hd.textContent;li.appendChild(a);toc.appendChild(li);});
m.querySelectorAll("table").forEach(function(t){
 var w=document.createElement("div");w.className="table-wrapper";t.parentNode.insertBefore(w,t);w.appendChild(t);});
m.querySelectorAll(":scope > h2").forEach(function(hd){
 if(!/learning outcomes/i.test(hd.textContent))return;
 var n=hd.nextElementSibling;while(n&&n.tagName==="P")n=n.nextElementSibling;
 if(!n||n.tagName!=="OL")return;n.className="outcomes-list";
 Array.prototype.forEach.call(n.children,function(li,i){
  var s=document.createElement("span");s.innerHTML=li.innerHTML;li.innerHTML="";
  var k=document.createElement("span");k.className="outcome-num";k.textContent=i+1;
  li.appendChild(k);li.appendChild(s);});});
m.querySelectorAll("a[href]").forEach(function(a){var u=a.getAttribute("href");
 if(!/^[a-z][a-z0-9+.-]*:|^\/\//i.test(u))a.setAttribute("href",u.replace(/\.md(?=[?#]|$)/i,".html"));});
m.querySelectorAll('a[href^="http"]').forEach(function(a){a.target="_blank";a.rel="noopener";});
var dia=[];
m.querySelectorAll("pre > code.language-mermaid").forEach(function(c){
 var d=document.createElement("div");d.className="mermaid";d.dataset.src=c.textContent;d.textContent=c.textContent;
 c.parentNode.replaceWith(d);dia.push([d,c.textContent]);});
async function drawMermaid(){
 if(!dia.length||typeof mermaid==="undefined")return;
 var dark=document.documentElement.getAttribute("data-theme")==="dark";
 var tv=dark?{primaryColor:"#1e3a5f",primaryTextColor:"#e2e8f0",primaryBorderColor:"#60a5fa",lineColor:"#94a3b8",secondaryColor:"#3b2f12",secondaryTextColor:"#fde68a",secondaryBorderColor:"#fbbf24",tertiaryColor:"#1a2030",tertiaryTextColor:"#e2e8f0",noteBkgColor:"#3b2f12",noteTextColor:"#fde68a",noteBorderColor:"#fbbf24",actorBkg:"#1e3a5f",actorBorder:"#60a5fa",actorTextColor:"#e2e8f0",actorLineColor:"#475569",signalColor:"#cbd5e1",signalTextColor:"#e2e8f0",labelBoxBkgColor:"#1a2030",labelBoxBorderColor:"#475569",labelTextColor:"#e2e8f0",loopTextColor:"#e2e8f0",clusterBkg:"#131826",clusterBorder:"#334155",edgeLabelBackground:"#131826",titleColor:"#e2e8f0",fontSize:"15px"}:{primaryColor:"#dbeafe",primaryTextColor:"#0f172a",primaryBorderColor:"#2563eb",lineColor:"#64748b",secondaryColor:"#fef3c7",secondaryTextColor:"#78350f",secondaryBorderColor:"#f59e0b",tertiaryColor:"#f1f5f9",tertiaryTextColor:"#0f172a",noteBkgColor:"#fef3c7",noteTextColor:"#78350f",noteBorderColor:"#f59e0b",actorBkg:"#dbeafe",actorBorder:"#2563eb",actorTextColor:"#0f172a",actorLineColor:"#94a3b8",signalColor:"#475569",signalTextColor:"#0f172a",labelBoxBkgColor:"#f1f5f9",labelBoxBorderColor:"#cbd5e1",labelTextColor:"#0f172a",loopTextColor:"#0f172a",clusterBkg:"#f8fafc",clusterBorder:"#cbd5e1",edgeLabelBackground:"#ffffff",titleColor:"#0f172a",fontSize:"15px"};
 mermaid.initialize({startOnLoad:false,securityLevel:"strict",theme:"base",fontFamily:"Inter,system-ui,sans-serif",flowchart:{curve:"basis",htmlLabels:true,padding:12,nodeSpacing:40,rankSpacing:48},sequence:{mirrorActors:false,actorMargin:50,messageMargin:34},themeVariables:tv});
 var nodes=[];
 for(var i=0;i<dia.length;i++){var p=dia[i];
  if(!p[2]&&!(await mermaid.parse(p[1],{suppressErrors:true}))){
   // Invalid diagram source: show it as a code block instead of mermaid's error box.
   var pre=document.createElement("pre"),code=document.createElement("code");
   code.textContent=p[1];pre.appendChild(code);p[0].replaceWith(pre);dia.splice(i--,1);continue;}
  p[2]=true;p[0].removeAttribute("data-processed");p[0].textContent=p[1];nodes.push(p[0]);}
 var closed=[].slice.call(m.querySelectorAll('details:not([open])'));closed.forEach(function(d){d.open=true;});if(nodes.length){try{await mermaid.run({nodes:nodes,suppressErrors:true});}catch(e){}}
 // A wide left-to-right flowchart is re-drawn top-to-bottom when that is much narrower, so it fits without scrolling.
 for(var j=0;j<dia.length;j++){var q=dia[j],el=q[0];
  if(q[3]||!/^\s*(flowchart|graph)\s+LR/.test(q[1]))continue;
  var sv=el.querySelector("svg");if(!sv||!sv.viewBox)continue;
  var vw=sv.viewBox.baseVal.width,cw=el.clientWidth-40;
  if(vw<cw*1.3)continue;
  try{var alt=q[1].replace(/^(\s*(?:flowchart|graph)\s+)LR/,"$1TB");
   var out=await mermaid.render("sdflip"+j+"x"+Date.now(),alt);
   var tmp2=document.createElement("div");tmp2.innerHTML=out.svg;var nv=tmp2.querySelector("svg").viewBox.baseVal.width;
   if(nv<vw*0.75){el.innerHTML=out.svg;q[1]=alt;q[3]=true;}}catch(e){}}
 if(window.SDDiagrams)window.SDDiagrams.mermaid();closed.forEach(function(d){d.open=false;});}
window.addEventListener("load",function(){drawMermaid();
 new MutationObserver(drawMermaid).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});});
"""


# ----------------------------------------------------------------------------------------------
# Guide-specific page builders. Everything above this line is copied from the AI Library's
# build script so that both sites share one look; everything below is specific to this repo.
# ----------------------------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
VOLS = ROOT / "volumes"
ICONS = {0: "📐", 1: "💻", 2: "🛠️", 3: "🧩", 4: "🏗️", 5: "🤖"}
TAGLINE = "From computer science foundations to AI systems engineering, in six volumes and 135 single-concept chapters."


def h(s):
    return html.escape(str(s), quote=True)


def embed_md(text):
    return json.dumps(text, ensure_ascii=False).replace("</", "<\\/")


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def first_sentence(s, limit=190):
    s = strip_md(s)
    m = re.match(r"(.{35,%d}?[.!?])(?:\s|$)" % limit, s)
    if m:
        return m.group(1)
    return s if len(s) <= limit else s[:limit].rsplit(" ", 1)[0] + "…"


def concept_line(text):
    m = re.search(r"^## Concept\s*\n+(.*?)(?:\n\s*\n|\Z)", text, re.M | re.S)
    return strip_md(m.group(1)).rstrip(".") + "." if m else ""


def one_sentence(text):
    m = re.search(r"\*\*In one sentence:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    return first_sentence(m.group(1), 230) if m else concept_line(text)


def prep_md(text):
    """Drop what the page template already provides: the title (hero) and the old prev/next line."""
    text = text.lstrip("﻿")
    text = re.sub(r"\A#\s+[^\n]*\n+", "", text, count=1)
    text = re.sub(r"\A(?:>[^\n]*\n)+\s*(?:---\s*\n+)?", "", text, count=1)
    return text


def load_volumes():
    vols = []
    for vdir in sorted(p for p in VOLS.iterdir() if p.is_dir()):
        idx = (vdir / "index.md").read_text(encoding="utf-8")
        m = re.match(r"#\s+Volume\s+(\d+)\s+[—-]\s+(.+)", idx)
        num, name = int(m.group(1)), m.group(2).strip()
        goal_lines = []
        for ln in idx.splitlines()[1:]:
            if ln.startswith(">"):
                body = ln.lstrip("> ").strip()
                if not body:
                    break
                goal_lines.append(body)
            elif goal_lines:
                break
        goal = strip_md(" ".join(goal_lines))
        goal = re.sub(r"^Goal:\s*", "", goal)
        part_of, part = {}, None
        for ln in idx.splitlines():
            pm = re.match(r"^## Part \d+ — (.+)", ln)
            if pm:
                part = pm.group(1).strip()
                continue
            cm = re.match(r"^#{2,3} Chapter (\d+) — ", ln)
            if cm and part:
                part_of[int(cm.group(1))] = part
        chapters = []
        for f in sorted(vdir.glob("ch*.md")):
            n = int(re.match(r"ch(\d+)-", f.name).group(1))
            text = f.read_text(encoding="utf-8")
            t = re.search(r"^#\s+Chapter\s+\d+\s+[—-]\s+(.+)$", text, re.M)
            chapters.append(dict(n=n, title=t.group(1).strip() if t else f.stem, stem=f.stem, text=text,
                                 concept=cap(concept_line(text)), lead=cap(one_sentence(text)), part=part_of.get(n),
                                 page=f"volumes/{vdir.name}/{f.stem}.html"))
        vols.append(dict(num=num, name=name, dir=vdir.name, goal=goal, chapters=chapters,
                         title=f"Volume {num} — {name}", icon=ICONS.get(num, "📘")))
    return vols


def head(title, root, extra_css, description=""):
    return "".join([
        '<!DOCTYPE html><html lang="en" data-theme="light"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>{h(title)}</title>',
        f'<meta name="description" content="{h(description)}">' if description else "",
        COURSE_FONTS, PRISM_CSS,
        "".join(f'<link rel="stylesheet" href="{root}assets/{c}.css">' for c in extra_css),
    ])


def topbar(root, menu):
    return "".join([
        f'<header class="topbar"><a class="brand" href="{root}index.html"><span class="brand-icon">G</span>',
        '<span>Guide</span></a><div class="topbar-actions">',
        '<button class="icon-btn menu-btn" id="menuBtn" aria-label="Open menu">☰</button>' if menu else "",
        '<button class="icon-btn" id="themeToggle" aria-label="Toggle theme">🌙</button></div></header>',
    ])


def scripts(root, guide):
    return (f'<script src="{root}assets/system-design.js"></script>'
            f'<script>window.GUIDE={json.dumps(guide, ensure_ascii=False)};</script>'
            f'<script src="{root}assets/guide.js"></script></body></html>')


def card(c, vol, first):
    foot = "Start here →" if first else "Read chapter →"
    return "".join([
        f'<a class="chapter-card" href="{h(c["stem"])}.html" data-page="{h(c["page"])}">',
        f'<div class="chapter-card-head"><span class="chapter-num">CH {c["n"]:02d}</span>',
        f'<span class="chapter-icon">{vol["icon"]}</span></div>',
        f'<h3 class="chapter-title">{h(c["title"])}</h3>',
        f'<p class="chapter-desc">{h(first_sentence(c["concept"], 150))}</p>',
        f'<div class="chapter-card-foot">{foot}</div></a>',
    ])


def volume_index(vol, vols):
    chapters = vol["chapters"]
    groups, order = {}, []
    for c in chapters:
        key = c["part"] or "Chapters"
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(c)
    sections = []
    for key in order:
        items = groups[key]
        nums = [c["n"] for c in items]
        rng = f"Chapter {nums[0]}" if len(nums) == 1 else f"Chapters {min(nums)}–{max(nums)}"
        cards = "".join(card(c, vol, c is chapters[0]) for c in items)
        style = ' style="margin-top: 64px;"' if sections else ""
        sections.append(f'<section{style}><div class="home-section-header"><h2>{h(key)}</h2>'
                        f'<span class="count">{rng}</span></div><div class="chapter-list">{cards}</div></section>')
    stats = [{"num": str(len(chapters)), "label": "Chapters"},
             {"num": str(len(chapters)), "label": "Mini-projects"},
             {"num": str(len(order)) if vol["chapters"][0]["part"] else "9", "label": "Parts" if vol["chapters"][0]["part"] else "Sections per chapter"}]
    nxt = next((v for v in vols if v["num"] == vol["num"] + 1), None)
    ctas = (f'<a class="home-btn home-btn-primary" href="{h(chapters[0]["stem"])}.html">Start Chapter 1 →</a>'
            '<a class="home-btn home-btn-secondary" href="../../index.html">All volumes</a>')
    footer = ('<footer class="home-footer"><p>Guide · a mastery roadmap · '
              + (f'Next: <a href="../{h(nxt["dir"])}/index.html">{h(nxt["title"])}</a>' if nxt else "You have reached the last volume") + '</p></footer>')
    guide = {"kind": "volume", "page": f"volumes/{vol['dir']}/index.html"}
    return "".join([
        head(f"{vol['title']} · Guide", "../../", ["system-design", "home", "guide"], vol["goal"]),
        '</head><body>', topbar("../../", False),
        f'<section class="home-hero"><span class="home-eyebrow">Volume {vol["num"]}</span>',
        f'<h1>{h(vol["name"])}</h1><p class="home-tagline">{h(vol["goal"])}</p>',
        f'<div class="home-cta-row">{ctas}</div>', stats_block(stats), '</section>',
        f'<main class="home-container">{"".join(sections)}</main>', footer, scripts("../../", guide),
    ])


def nav_card(label, title, href, cls=""):
    return (f'<a class="chapter-nav-card{cls}" href="{h(quote(href, safe="/#."))}">'
            f'<div class="chapter-nav-label">{label}</div><div class="chapter-nav-title">{h(title)}</div></a>')


def chapter_page(vol, i, vols):
    c = vol["chapters"][i]
    chapters = vol["chapters"]
    root = "../../"
    prev_card = next_card = ""
    if i > 0:
        p = chapters[i - 1]
        prev_card = nav_card("← Previous", f'Chapter {p["n"]} — {p["title"]}', p["stem"] + ".html")
    else:
        prev_card = nav_card("← Volume", "Contents", "index.html")
    if i < len(chapters) - 1:
        n = chapters[i + 1]
        next_card = nav_card("Next chapter →", f'Chapter {n["n"]} — {n["title"]}', n["stem"] + ".html", " next")
    else:
        nv = next((v for v in vols if v["num"] == vol["num"] + 1), None)
        if nv:
            next_card = nav_card("Next volume →", nv["title"], f'../{nv["dir"]}/index.html', " next")
        else:
            next_card = nav_card("Finished →", "Back to all volumes", "../../index.html", " next")
    guide = {"kind": "chapter", "page": c["page"], "volumeTitle": f'Volume {vol["num"]} · Chapters',
             "chapters": [dict(n=x["n"], title=x["title"], href=x["stem"] + ".html", page=x["page"], part=x["part"]) for x in chapters]}
    label = f'Volume {vol["num"]} · {vol["name"]} · Chapter {c["n"]}'
    return "".join([
        head(f'Vol {vol["num"]} · Ch {c["n"]} — {c["title"]}', root, ["system-design", "guide"], c["lead"]),
        f'<style>{COURSE_CSS}</style></head><body>',
        '<div class="progress-bar" id="progressBar"></div>', topbar(root, True), '<div class="overlay" id="overlay"></div>',
        f'<div class="layout"><aside class="sidebar" id="sidebar"><h3>Chapter {c["n"]} — On This Page</h3>',
        '<ul class="toc-list" id="tocList"></ul></aside>',
        '<main class="main" id="main"><section class="hero">',
        f'<span class="chapter-label">{h(label)}</span><h1>{h(c["title"])}</h1>',
        f'<p class="hero-subtitle">{h(c["lead"])}</p></section>',
        f'<nav class="chapter-nav">{prev_card}{next_card}</nav></main></div>',
        f'<script src="{root}{MARKED_JS}"></script><script src="{root}{MERMAID_JS}"></script>',
        f'<script>const MD={embed_md(prep_md(c["text"]))},CH={c["n"]};{COURSE_RENDER_JS}</script>',
        f'<script src="{root}assets/venn.js"></script>',
        f'<script src="{root}assets/figs.js"></script>',
        PRISM_JS, PRISM_AUTOLOADER, scripts(root, guide),
    ])


def simple_page(title, label, md_text, root=""):
    """A plain reading page (used for the roadmap) in the same template as a chapter."""
    text = re.sub(r"\A#\s+[^\n]*\n+", "", md_text.lstrip("﻿"), count=1)
    nav = nav_card("← Home", "All volumes", root + "index.html")
    guide = {"kind": "page", "page": "roadmap.html"}
    return "".join([
        head(f"{title} · Guide", root, ["system-design", "guide"]),
        f'<style>{COURSE_CSS}</style></head><body>',
        '<div class="progress-bar" id="progressBar"></div>', topbar(root, True), '<div class="overlay" id="overlay"></div>',
        '<div class="layout"><aside class="sidebar" id="sidebar"><h3>On This Page</h3><ul class="toc-list" id="tocList"></ul></aside>',
        f'<main class="main" id="main"><section class="hero"><span class="chapter-label">{h(label)}</span><h1>{h(title)}</h1></section>',
        f'<nav class="chapter-nav">{nav}</nav></main></div>',
        f'<script src="{root}{MARKED_JS}"></script><script src="{root}{MERMAID_JS}"></script>',
        f'<script>const MD={embed_md(text)};{COURSE_RENDER_JS}</script>',
        f'<script src="{root}assets/venn.js"></script>',
        f'<script src="{root}assets/figs.js"></script>',
        PRISM_JS, PRISM_AUTOLOADER, scripts(root, guide),
    ])


def home_page(vols):
    total = sum(len(v["chapters"]) for v in vols)
    cards = []
    for v in vols:
        cards.append("".join([
            f'<a class="chapter-card" href="volumes/{h(v["dir"])}/index.html" data-vol="volumes/{h(v["dir"])}/" data-total="{len(v["chapters"])}">',
            f'<div class="chapter-card-head"><span class="chapter-num">VOL {v["num"]}</span><span class="chapter-icon">{v["icon"]}</span></div>',
            f'<h3 class="chapter-title">{h(v["name"])}</h3><p class="chapter-desc">{h(first_sentence(v["goal"], 150))}</p>',
            f'<div class="chapter-card-foot">{len(v["chapters"])} chapters →</div></a>',
        ]))
    learn = ["A one-sentence idea and a mental model", "A diagram and a worked example",
             "Exercises with solutions you can reveal", "A mini-project to build",
             "Open-source code worth reading", "Interview questions and a checklist"]
    intro = ('<div class="home-intro-card"><div><h3>Every chapter has the same shape</h3>'
             '<p>One concept per chapter, so you always know what you are learning and how to practise it.</p></div>'
             '<ul class="home-intro-list">' + "".join(f"<li>{h(x)}</li>" for x in learn) + "</ul></div>")
    stats = [{"num": "6", "label": "Volumes"}, {"num": str(total), "label": "Chapters"}, {"num": str(total), "label": "Mini-projects"}]
    ctas = ('<a class="home-btn home-btn-primary" href="volumes/' + h(vols[0]["dir"]) + '/index.html">Start with Volume 0 →</a>'
            '<a class="home-btn home-btn-secondary" href="roadmap.html">Roadmap and order</a>')
    footer = '<footer class="home-footer"><p>Guide · a mastery roadmap · progress is saved in this browser</p></footer>'
    guide = {"kind": "home", "page": "index.html"}
    return "".join([
        head("Guide — a mastery roadmap", "", ["system-design", "home", "guide"], TAGLINE), '</head><body>', topbar("", False),
        '<section class="home-hero"><span class="home-eyebrow">Mastery roadmap</span><h1>Guide</h1>',
        f'<p class="home-tagline">{h(TAGLINE)}</p><div class="home-cta-row">{ctas}</div>', stats_block(stats), '</section>',
        f'<main class="home-container">{intro}<section style="margin-top: 56px;"><div class="home-section-header"><h2>The six volumes</h2>'
        f'<span class="count">{total} chapters</span></div><div class="chapter-list">{"".join(cards)}</div></section></main>',
        footer, scripts("", guide),
    ])


def main():
    vols = load_volumes()
    (ROOT / "index.html").write_text(home_page(vols), encoding="utf-8")
    (ROOT / "roadmap.html").write_text(
        simple_page("Mastery Roadmap", "Guide · Roadmap", (ROOT / "roadmap.md").read_text(encoding="utf-8")), encoding="utf-8")
    n = 0
    for v in vols:
        out = VOLS / v["dir"]
        (out / "index.html").write_text(volume_index(v, vols), encoding="utf-8")
        for i, c in enumerate(v["chapters"]):
            (out / (c["stem"] + ".html")).write_text(chapter_page(v, i, vols), encoding="utf-8")
            n += 1
        print(f'  {v["title"]}: {len(v["chapters"])} chapters')
    print(f"Built home, roadmap, {len(vols)} volume contents pages and {n} chapter pages.")


if __name__ == "__main__":
    main()
