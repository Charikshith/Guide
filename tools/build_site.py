"""Build a browsable HTML site from the Markdown volumes, in the handwritten notebook look.

Usage:  python tools/build_site.py
Output: site/  (open site/index.html in a browser)

Stdlib only. Each page embeds its Markdown source unchanged; the browser renders it with
marked (Markdown) from a CDN. The look comes from the handwritten skill
(.claude/skills/handwritten): ruled paper, pen fonts, margin line.

Diagrams: every ```mermaid block is replaced by the hand-drawn SVG figure from the chapter's
<chapter>.notes.html (matched by label overlap). If a chapter has no matching figure, the
browser falls back to mermaid (loaded lazily from a CDN) for that block.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "volumes"
OUT = ROOT / "site"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Kalam:wght@400;700&family=Patrick+Hand&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t;var n=localStorage.getItem("nav");if(n)document.documentElement.dataset.nav=n;}}catch(e){{}}</script>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <filter id="rough" filterUnits="userSpaceOnUse" x="-500" y="-500" width="3000" height="3000">
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3"/>
  </filter>
  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M1 1 L9 5 L1 9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
  </marker>
</defs></svg>
<div class="notebook" id="notebook">
  <button id="menu" class="pen tl" aria-label="Show or hide contents" title="Show / hide contents">☰</button>
  <button id="theme" class="pen tr" aria-label="Toggle theme" title="Light / dark desk">◐</button>
  <nav id="sidebar" aria-label="Contents"></nav>
  <main><article id="content" class="page">Loading…</article></main>
</div>
<textarea id="source" hidden>{source}</textarea>
<textarea id="figs" hidden>{figs}</textarea>
<script>window.GUIDE = {{ root: "{root}", page: "{page}", nav: {nav} }};</script>
<script src="https://cdn.jsdelivr.net/npm/marked@15/marked.min.js"></script>
<script src="{root}assets/app.js"></script>
</body>
</html>
"""

CSS = r"""/* Handwritten notebook look (from the handwritten skill). Every vertical size is a multiple of --line. */
:root{
  --line:32px; --paper:#fdfbf4; --rule:#c9dcef; --margin:#e8a0a0;
  --ink:#1f3a93; --ink2:#222; --red:#c0392b; --green:#1e8449;
  --hl-yellow:rgba(255,235,59,.55);
  --desk:#e9e4d8;
  --hand:'Kalam','Patrick Hand','Comic Sans MS','Segoe Print','Bradley Hand',cursive;
  --title:'Caveat','Kalam','Segoe Print','Bradley Hand',cursive;
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){ --desk:#2b2b2b; } }
:root[data-theme="dark"]{ --desk:#2b2b2b; }
*,*::before,*::after{box-sizing:border-box}
html{scroll-padding-top:64px}
body{margin:0;background:var(--desk);font-family:var(--hand);color:var(--ink)}
a{color:var(--ink);text-decoration:underline dotted}

/* ===== one notebook sheet: contents in the left column, chapter on the right, same ruled paper ===== */
.notebook{
  position:relative;display:flex;align-items:stretch;max-width:1180px;margin:24px auto;padding:var(--line) 28px calc(var(--line)*2) 62px;
  background:repeating-linear-gradient(var(--paper) 0,var(--paper) calc(var(--line) - 1px),var(--rule) calc(var(--line) - 1px),var(--rule) var(--line));
  background-color:var(--paper);
  box-shadow:0 2px 6px rgba(0,0,0,.15),0 12px 28px rgba(0,0,0,.12);
  font-size:20px;line-height:var(--line);color:var(--ink);
}
.notebook::before{content:"";position:absolute;left:22px;top:0;bottom:0;width:18px;pointer-events:none;
  background:radial-gradient(circle,var(--desk) 7px,transparent 8px) 0 40px/18px 220px repeat-y}
main{flex:1;min-width:0;border-left:2px solid var(--margin);padding-left:22px}
.page{font-size:20px;line-height:var(--line);color:var(--ink)}

/* small pen buttons live on the blank first ruled line, like the date in the skill */
.pen{position:absolute;top:0;height:var(--line);padding:0 10px;border:0;background:none;cursor:pointer;
  font-family:var(--title);font-size:24px;line-height:var(--line);color:var(--red)}
.pen:hover{background:var(--hl-yellow);border-radius:4px 8px 4px 8px}
.pen.tl{left:10px;z-index:2} .pen.tr{right:18px}

/* contents column: native sticky (smooth, no scroll script); rows are 32px, so at rest the text sits on the rules */
#sidebar{width:262px;flex:none;align-self:flex-start;position:sticky;top:var(--line);max-height:calc(100vh - 2*var(--line));
  overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;
  padding:0 10px 0 4px;scrollbar-width:none;font-size:17px;line-height:var(--line)}
#sidebar::-webkit-scrollbar{display:none}
#sidebar[hidden],html[data-nav="closed"] #sidebar{display:none}
#sidebar .vol{font-family:var(--title);font-weight:700;font-size:26px;color:var(--red);margin-top:var(--line)}
#sidebar .part{font-family:var(--title);font-size:20px;color:var(--ink2)}
#sidebar a{display:block;padding:0 6px;color:var(--ink);text-decoration:none;border-radius:4px 8px 4px 8px}
#sidebar a:hover{background:var(--hl-yellow)}
#sidebar a.home{font-family:var(--title);font-weight:700;font-size:24px;color:var(--ink2)}
#sidebar a.todo{opacity:.55;font-style:italic}
#sidebar a.active{background:var(--hl-yellow);font-weight:700;color:var(--ink2)}
#sidebar a .done{color:var(--green);margin-right:4px}
.filter{display:block;width:100%;height:var(--line);padding:0 6px;border:0;border-bottom:2px dashed var(--ink2);background:transparent;
  color:var(--ink);font-family:var(--hand);font-size:16px;outline:0}
.filter:focus{background:var(--hl-yellow)}
.filter::placeholder{color:#7b86b4}

/* ===== text (all margins are multiples of --line) ===== */
.page h1{font-family:var(--title);font-weight:700;color:var(--ink2);font-size:46px;line-height:calc(var(--line)*2);margin:0 0 var(--line);transform:rotate(-1deg)}
.page h1 .u{background:linear-gradient(transparent 62%,var(--hl-yellow) 62%,var(--hl-yellow) 92%,transparent 92%)}
.page h2{font-family:var(--title);font-weight:700;color:var(--red);font-size:32px;line-height:calc(var(--line)*1.5);margin:var(--line) 0 calc(var(--line)*.5)}
.page h2::before{content:"➤ ";font-size:22px}
.page h3{font-family:var(--title);font-weight:700;color:var(--ink2);font-size:26px;line-height:var(--line);margin:var(--line) 0 0}
.page h3::before{content:"✎ ";font-size:18px;color:var(--red)}
.page h4,.page h5{font-family:var(--title);font-size:22px;line-height:var(--line);margin:0;color:var(--ink2)}
.page p{margin:0 0 var(--line)}
.page ul,.page ol{margin:0 0 var(--line);padding-left:28px}
.page li>ul,.page li>ol{margin:0}
.page ul{list-style:none}
.page ul>li::before{content:"–";position:absolute;margin-left:-20px}
.page li.ti::before{content:none}
.page strong{color:var(--ink2)}
.page hr{border:0;border-top:3px dashed var(--margin);margin:var(--line) 0;height:0}
.page blockquote{margin:0 0 var(--line);padding:calc(var(--line)*.5 - 2px) 14px;border:2.5px solid var(--red);border-radius:4px 10px 6px 12px;background:rgba(255,255,255,.35)}
.page blockquote p:last-child{margin:0}

/* code stays verbatim; only the paper look changes */
.page code{font-family:Consolas,'Courier New',monospace;font-size:.82em;background:rgba(0,0,0,.06);padding:0 3px;border-radius:3px}
.page pre{font-family:Consolas,'Courier New',monospace;font-size:14px;line-height:var(--line);color:var(--ink);background:rgba(255,255,255,.45);
  border-left:4px solid var(--red);margin:0 0 var(--line);padding:0 12px;overflow-x:auto;white-space:pre}
.page pre code{background:none;padding:0;font-size:inherit}

/* tables */
.page table{border-collapse:collapse;display:block;overflow-x:auto;margin:0 0 var(--line)}
.page th,.page td{border:2px solid var(--ink2);padding:0 10px;text-align:left;vertical-align:top}
.page th{font-family:var(--title);font-size:24px;color:var(--ink2)}

/* interview answers etc. */
.page details{border:2.5px dashed var(--ink2);border-radius:4px 10px 6px 12px;padding:0 14px;margin:0 0 var(--line);background:rgba(255,255,255,.35)}
.page details[open]{padding-bottom:var(--line)}
.page summary{cursor:pointer;font-family:var(--title);font-weight:700;font-size:24px;color:var(--red)}
.page details>p:last-child,.page details>ul:last-child,.page details>ol:last-child{margin-bottom:0}

/* checklist */
.page li input[type=checkbox]{width:18px;height:18px;margin:0 8px 0 -20px;vertical-align:-3px;accent-color:var(--green)}

/* hand-drawn diagrams */
.page figure{margin:0 0 var(--line);text-align:center}
.page figure svg{width:100%;max-width:640px;height:auto;overflow:visible}
.page figcaption{font-family:var(--title);font-size:20px;color:var(--ink2)}
.page pre.mermaid{background:#fff;border-left:0;text-align:center;white-space:normal}
.sk{fill:none;stroke:var(--ink2);stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;filter:url(#rough)}
.sk.blue{stroke:var(--ink)} .sk.red{stroke:var(--red)} .sk.green{stroke:var(--green)}
.lbl{font-family:var(--hand);font-size:17px;fill:var(--ink)}
.lbl.b{font-weight:700;fill:var(--ink2)} .lbl.r{fill:var(--red)} .lbl.g{fill:var(--green)}

/* previous / next */
.pager{display:flex;justify-content:space-between;gap:12px;margin-top:var(--line);font-family:var(--title);font-size:22px;line-height:var(--line)}
.pager a{flex:1;color:var(--red);text-decoration:none}
.pager a.next{text-align:right}
.pager a:hover{text-decoration:underline wavy}
.pager small{display:block;color:var(--ink);font-size:18px}

/* home: one boxed section per volume */
.home-vol{border:2.5px solid var(--ink2);border-radius:4px 10px 6px 12px;padding:calc(var(--line)*.5 - 2.5px) 16px;margin:0 0 var(--line);
  background:rgba(255,255,255,.35)}
.home-vol h2{margin:0}
.home-vol h2 a{color:var(--red);text-decoration:none}
.home-vol h2 a:hover{text-decoration:underline wavy}
.home-vol .goal{margin:0}
.home-vol .meta{margin:0;color:var(--ink2)}
.home-vol .pg>.plabel{font-family:var(--title);font-size:22px;color:var(--ink2);margin-top:calc(var(--line)*.5);break-after:avoid}
.home-vol ol{margin:0;padding:0;list-style:none;columns:2;column-gap:28px}
.home-vol li{break-inside:avoid;padding-left:34px;text-indent:-34px}
.home-vol li::before{content:none!important}
.home-vol li a{text-decoration:none}
.home-vol li a:hover{background:var(--hl-yellow)}
.home-vol li .n{display:inline-block;width:30px;text-align:right;margin-right:4px;color:var(--red);text-indent:0}
.home-vol li.todo a{opacity:.55;font-style:italic}
.map-frame{display:block;width:100%;height:2300px;border:0;margin:0 0 var(--line)}
@media (max-width:900px){.map-frame{height:3400px}}
.bar{height:8px;border:2px solid var(--ink2);border-radius:6px;margin:0 0 var(--line);overflow:hidden}
.bar i{display:block;height:100%;background:var(--green)}
@media (max-width:700px){.home-vol ol{columns:1}}

@media (max-width:900px){
  /* phones/tablets: contents is a paper sheet that slides over the page */
  #sidebar{position:fixed;left:0;top:0;bottom:0;height:auto!important;z-index:9;width:min(300px,86vw);padding:var(--line) 12px var(--line) 16px;
    transform:translateX(-105%);transition:transform .2s;box-shadow:4px 0 14px rgba(0,0,0,.25);
    background:repeating-linear-gradient(var(--paper) 0,var(--paper) calc(var(--line) - 1px),var(--rule) calc(var(--line) - 1px),var(--rule) var(--line));
    background-color:var(--paper);border-right:2px solid var(--margin)}
  html[data-nav="closed"] #sidebar{display:block}
  body.nav-open #sidebar{transform:none}
}
@media (max-width:600px){
  .notebook{margin:0;padding-left:40px;padding-right:12px;font-size:18px}
  .notebook::before{left:10px;width:16px}
  main{padding-left:12px}
  .page{font-size:18px}
  .page figure{overflow-x:auto}.page figure svg{min-width:520px}
}
@media print{body{background:#fff}.pen,#sidebar,.pager{display:none!important}.notebook{box-shadow:none;margin:0}.notebook::before{display:none}}
"""

JS = r"""(function boot() {
  /* Some hosts (e.g. htmlpreview.github.io) run this file before the marked CDN script has loaded.
     Chapter pages need marked, so load it here and start over once it is ready. */
  if (typeof marked === "undefined" && document.getElementById("source").value.trim()) {
    const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/marked@15/marked.min.js";
    s.onload = boot;
    document.head.appendChild(s);
    return;
  }
  /* Online preview (htmlpreview.github.io): relative links would resolve against the previewer, not the repo.
     The real page URL is in the query string, so map every relative link and the map iframe through it. */
  const PV = location.hostname === "htmlpreview.github.io" && location.search.length > 1;
  function pvUrl(rel) {
    const real = decodeURIComponent(location.search.slice(1)).split("#")[0];
    const u = new URL(rel, real);
    return "https://htmlpreview.github.io/?" + u.origin + u.pathname + u.search + u.hash;
  }
  function pvFrames() {
    if (!PV) return;
    const f = content.querySelector("iframe.map-frame");
    if (f) f.src = pvUrl(G.root + "guide-map.html#embed");
  }
  if (PV) document.addEventListener("click", e => {
    const a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    const h = a.getAttribute("href");
    if (!h || /^(#|[a-z]+:)/i.test(h)) return;
    e.preventDefault();
    location.href = pvUrl(h);
  });
  const G = window.GUIDE;
  const progressKey = "guide-progress";
  const progress = JSON.parse(localStorage.getItem(progressKey) || "{}");

  // ---- contents column: Home + the selected volume only (hidden on Home / Roadmap) ----
  const root = document.documentElement;
  const nb = document.getElementById("notebook");
  const side = document.getElementById("sidebar");
  const cur = G.nav.find(v => G.page.startsWith(v.index.replace("index.html", "")));
  const setNav = v => { root.dataset.nav = v; try { localStorage.setItem("nav", v); } catch (e) {} };
  if (!cur) {
    side.hidden = true;
  } else {
    let h = `<a class="home" href="${G.root}index.html">⌂ Home</a>` +
            `<input class="filter" id="filter" type="search" placeholder="filter chapters…" aria-label="Filter chapters">` +
            `<div class="vol">${cur.title}</div>` +
            `<a href="${G.root}${cur.index}" class="${cur.index === G.page ? "active" : ""}">Contents</a>`;
    let part = null;
    for (const c of cur.chapters) {
      if (c.part && c.part !== part) { part = c.part; h += `<div class="part">${part}</div>`; }
      const cls = [c.page === G.page ? "active" : "", c.exists ? "" : "todo"].join(" ");
      const done = progress[c.page] && progress[c.page].done ? '<span class="done">✓</span>' : "";
      h += `<a class="${cls}" href="${G.root}${c.page}" data-title="${c.title.toLowerCase()}">${done}${c.n}. ${c.title}</a>`;
    }
    side.innerHTML = `<div id="sidein">${h}</div>`;
    document.getElementById("filter").oninput = e => {
      const q = e.target.value.toLowerCase().trim();
      side.querySelectorAll("a[data-title]").forEach(a => { a.style.display = !q || a.dataset.title.includes(q) ? "" : "none"; });
      place();
    };
  }

  // ☰ hides / shows the contents column (remembered on desktop; slides over the page on phones).
  document.getElementById("menu").onclick = () => {
    if (window.innerWidth <= 900) { document.body.classList.toggle("nav-open"); return; }
    setNav(root.dataset.nav === "closed" ? "open" : "closed");
    place();
  };
  document.getElementById("theme").onclick = () => {
    const dark = getComputedStyle(root).getPropertyValue("--desk").trim() === "#2b2b2b";
    const t = dark ? "light" : "dark";
    root.dataset.theme = t;
    try { localStorage.setItem("theme", t); } catch (e) {}
  };

  // The contents column is `position:sticky` in CSS, so nothing runs on scroll. place() only clears old inline styles.
  const LINE = 32;
  function place() { side.style.transform = ""; side.style.height = ""; }

  // ---- content ----
  const content = document.getElementById("content");
  const src = document.getElementById("source").value;
  if (!src.trim()) { renderHome(); place(); return; }

  const figs = JSON.parse(document.getElementById("figs").value || "[]");
  let mermaidSeen = 0, needMermaid = false;

  // Markdown links to .md files become links to the generated .html files.
  const renderer = new marked.Renderer();
  const baseLink = renderer.link.bind(renderer);
  renderer.link = function (token) {
    if (token.href && !/^[a-z]+:/i.test(token.href)) token.href = token.href.replace(/\.md(#|$)/, ".html$1");
    return baseLink(token);
  };
  renderer.code = function (token) {
    const esc = token.text.replace(/&/g, "&amp;").replace(/</g, "&lt;");
    if (token.lang === "mermaid") {
      const fig = figs[mermaidSeen++];
      if (fig) return fig;                         // hand-drawn SVG figure
      needMermaid = true;
      return `<pre class="mermaid">${esc}</pre>`;  // fallback
    }
    return `<pre><code class="language-${token.lang || ""}">${esc}</code></pre>`;
  };
  // Render each <details> body as its own markdown, since marked leaves raw HTML blocks unparsed.
  const folds = [];
  const prepared = src.replace(/<details><summary>([\s\S]*?)<\/summary>([\s\S]*?)<\/details>/g, (m, summary, body) => {
    const inner = marked.parse(body.replace(/^ {3}/gm, "").trim(), { renderer, gfm: true });
    folds.push(`<details><summary>${marked.parseInline(summary)}</summary>${inner}</details>`);
    return `@@FOLD${folds.length - 1}@@`;
  });
  content.innerHTML = marked.parse(prepared, { renderer, gfm: true })
    .replace(/(<p>)?@@FOLD(\d+)@@(<\/p>)?/g, (m, a, i) => folds[+i])
    .replace(/(href="[^"#:]*?)\.md(#[^"]*)?"/g, '$1.html$2"');   // raw <a href="x.md"> too

  content.querySelectorAll("h1").forEach(h => { h.innerHTML = `<span class="u">${h.innerHTML}</span>`; });
  content.querySelectorAll("li").forEach(li => { if (li.querySelector(":scope > input[type=checkbox]")) li.classList.add("ti"); });

  // Checklist boxes: clickable and remembered per page.
  const boxes = content.querySelectorAll('li input[type="checkbox"]');
  const state = progress[G.page] || { boxes: [] };
  boxes.forEach((b, i) => {
    b.disabled = false;
    b.checked = !!state.boxes[i];
    b.onchange = () => {
      state.boxes[i] = b.checked;
      state.done = boxes.length > 0 && [...boxes].every(x => x.checked);
      progress[G.page] = state;
      localStorage.setItem(progressKey, JSON.stringify(progress));
    };
  });

  // Replace the markdown nav lines with a pager.
  const flat = G.nav.flatMap(v => v.chapters);
  const i = flat.findIndex(c => c.page === G.page);
  if (i >= 0) {
    content.querySelectorAll("blockquote").forEach(q => { if (/Contents/.test(q.textContent) && q.querySelector("a")) q.remove(); });
    const prev = flat[i - 1], next = flat[i + 1];
    const link = (c, cls, label) => c ? `<a class="${cls}" href="${G.root}${c.page}"><small>${label}</small>${c.title}</a>` : "<span></span>";
    content.insertAdjacentHTML("beforeend", `<div class="pager">${link(prev, "prev", "← Previous")}${link(next, "next", "Next →")}</div>`);
  }

  place();
  const act = side.querySelector("a.active");
  if (act && !side.hidden) side.scrollTop = Math.max(0, Math.round((act.offsetTop - 4 * LINE) / LINE) * LINE);
  setTimeout(place, 400);

  if (needMermaid) {
    const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";
    s.onload = () => { mermaid.initialize({ startOnLoad: false, theme: "default", securityLevel: "loose" }); mermaid.run({ querySelector: ".mermaid" }); };
    document.head.appendChild(s);
  }

  function renderHome() {
    const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
    let h = "<h1>Mastery Guide</h1><p>From computer science foundations to AI systems engineering. " +
            `Pick a volume, or jump straight to a chapter. <a href="${G.root}roadmap.html">Roadmap &amp; prerequisites →</a></p>` +
            `<section class="home-vol"><h2>Start here — the big picture</h2>` +
            `<p class="goal">Six volumes in learning order, with the chapter groups in each. Click a branch to fold it, or press play for a walkthrough. ` +
            `<a href="${G.root}guide-map.html">Open the map on its own page →</a></p>` +
            `<iframe class="map-frame" title="Map of the guide" src="${G.root}guide-map.html#embed" loading="lazy"></iframe></section>` +
            `<input class="filter" id="homefilter" type="search" placeholder="filter chapters…" aria-label="Filter chapters"><p></p>`;
    for (const v of G.nav) {
      const total = v.chapters.length;
      const done = v.chapters.filter(c => progress[c.page] && progress[c.page].done).length;
      h += `<section class="home-vol"><h2><a href="${G.root}${v.index}">${esc(v.title)}</a></h2>`;
      if (v.goal) h += `<p class="goal">${esc(v.goal)}</p>`;
      h += `<p class="meta">${total} chapters · ${done} done</p><div class="bar"><i style="width:${total ? (100 * done / total) : 0}%"></i></div>`;
      let part = null, open = false;
      for (const c of v.chapters) {
        if (!open || c.part !== part) {
          if (open) h += "</ol></div>";
          part = c.part; open = true;
          h += `<div class="pg">${part ? `<div class="plabel">${esc(part)}</div>` : ""}<ol>`;
        }
        h += `<li class="${c.exists ? "" : "todo"}" data-title="${esc(c.title.toLowerCase())}"><span class="n">${c.n}.</span><a href="${G.root}${c.page}">${esc(c.title)}</a></li>`;
      }
      if (open) h += "</ol></div>";
      h += `<p></p></section>`;
    }
    content.innerHTML = h;
    content.querySelectorAll("h1").forEach(x => { x.innerHTML = `<span class="u">${x.innerHTML}</span>`; });
    document.getElementById("homefilter").oninput = e => {
      const q = e.target.value.toLowerCase().trim();
      content.querySelectorAll(".home-vol").forEach(sec => {
        let any = false;
        sec.querySelectorAll(".pg").forEach(pg => {
          let n = 0;
          pg.querySelectorAll("li").forEach(li => { const ok = !q || li.dataset.title.includes(q); li.style.display = ok ? "" : "none"; if (ok) n++; });
          pg.style.display = n ? "" : "none"; if (n) any = true;
        });
        sec.style.display = !q || any ? "" : "none";
      });
    };
    pvFrames();
  }
})();
"""

STOP = set("graph flowchart subgraph end direction participant actor note over sequencediagram statediagram classdiagram "
           "erdiagram title style classdef class click linkstyle and the for with from that this into".split())


def words(text):
    return {w for w in re.findall(r"[a-z][a-z0-9]{2,}", text.lower()) if w not in STOP}


def figures_for(md_path):
    """Hand-drawn SVG <figure> for each ```mermaid block of a chapter, in order (None if no match)."""
    notes = md_path.with_suffix(".notes.html")
    mer = re.findall(r"^```mermaid\n(.*?)^```", md_path.read_text(encoding="utf-8"), re.S | re.M)
    if not mer:
        return []
    figs = re.findall(r"<figure.*?</figure>", notes.read_text(encoding="utf-8"), re.S) if notes.exists() else []
    fw = [words(" ".join(re.findall(r"<text[^>]*>(.*?)</text>", f, re.S))) for f in figs]
    out, used = [], set()
    for k, m in enumerate(mer):
        mw = words(m)
        if len(figs) == len(mer):        # same count: take them in order
            j = k
        else:                            # otherwise best label overlap among unused figures
            scores = [(len(mw & fw[x]) / (len(mw) or 1), x) for x in range(len(figs)) if x not in used]
            j = max(scores)[1] if scores else None
        score = len(mw & fw[j]) / (len(mw) or 1) if j is not None else 0
        if j is None or score < 0.15:
            print(f"  warning: weak diagram match {md_path.name} block {k + 1} (score {score:.2f})")
        if j is None:
            out.append(None)
            continue
        used.add(j)
        out.append(figs[j])
    return out


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().replace("&", "and")).strip("-")
    return "-".join(slug.split("-")[:7])


def collect_nav():
    nav = []
    for index in sorted(SRC.glob("*/index.md")):
        vol_dir = index.parent.name
        text = index.read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
        goal = re.search(r"^> Goal: (.+)$", text, re.M)
        chapters, part = [], None
        for line in text.splitlines():
            m = re.match(r"^## Part \d+ — (.+)", line)
            if m:
                part = m.group(1).strip()
                continue
            m = re.match(r"^#{2,3} Chapter (\d+) — (.+)", line)
            if m:
                n, t = int(m.group(1)), m.group(2).strip()
                md = f"volumes/{vol_dir}/ch{n:02d}-{slugify(t)}.md"
                chapters.append(dict(n=n, title=t, part=part, md=md,
                                     page=md[:-3] + ".html", exists=(ROOT / md).exists()))
        nav.append(dict(title=title, goal=goal.group(1).strip() if goal else "",
                        index=f"volumes/{vol_dir}/index.html", chapters=chapters))
    return nav


def write_page(out_path, title, page, source, nav, figs=()):
    depth = page.count("/")
    root = "../" * depth
    # Data sits in <textarea> (not <script>) so previewers that re-run scripts do not choke on it.
    safe = html.escape(source, quote=False)
    safe_figs = html.escape(json.dumps(list(figs)), quote=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(TEMPLATE.format(title=html.escape(title), root=root, page=page,
                                        source=safe, figs=safe_figs, nav=json.dumps(nav)), encoding="utf-8")


def main():
    nav = collect_nav()
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "app.js").write_text(JS, encoding="utf-8")

    # The mind-map page (made with the mindmap skill, handwritten style). #embed makes it sit flat on our sheet.
    mm = (ROOT / "tools" / "guide-mindmap.html").read_text(encoding="utf-8")
    embed_css = ("<style>html.embed.hand body{background:transparent!important}"
                 "html.embed.hand .page{background:none;box-shadow:none;margin:0 auto;padding:0}"
                 "html.embed .eyebrow,html.embed h1,html.embed .lede,html.embed .theme-toggle{display:none}</style>"
                 "<script>if(location.hash==='#embed')document.documentElement.classList.add('embed')</script>")
    (OUT / "guide-map.html").write_text(mm.replace("</head>", embed_css + "</head>", 1), encoding="utf-8")

    write_page(OUT / "index.html", "Home", "index.html", "", nav)
    write_page(OUT / "roadmap.html", "Roadmap", "roadmap.html",
               (ROOT / "roadmap.md").read_text(encoding="utf-8"), nav)

    count = 2
    for vol in nav:
        md = vol["index"][:-5] + ".md"
        write_page(OUT / vol["index"], vol["title"], vol["index"],
                   (ROOT / md).read_text(encoding="utf-8"), nav)
        count += 1
        for c in vol["chapters"]:
            figs = ()
            if c["exists"]:
                source = (ROOT / c["md"]).read_text(encoding="utf-8")
                figs = figures_for(ROOT / c["md"])
            else:
                source = f"# Chapter {c['n']} — {c['title']}\n\n> Not written yet. See the [volume contents](index.md) for the chapter outline."
            write_page(OUT / c["page"], c["title"], c["page"], source, nav, figs)
            count += 1

    written = sum(c["exists"] for v in nav for c in v["chapters"])
    total = sum(len(v["chapters"]) for v in nav)
    print(f"Built {count} pages into {OUT} ({written}/{total} chapters written)")


if __name__ == "__main__":
    main()
