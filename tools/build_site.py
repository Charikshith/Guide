"""Build a browsable HTML site from the Markdown volumes.

Usage:  python tools/build_site.py
Output: site/  (open site/index.html in a browser)

Stdlib only. Each page embeds its Markdown source; the browser renders it with
marked (Markdown) and mermaid (diagrams) loaded from a CDN.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "volumes"
OUT = ROOT / "site"

TEMPLATE = """<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Guide</title>
<link rel="stylesheet" href="{root}assets/style.css">
<script>document.documentElement.dataset.theme = localStorage.getItem("theme") || "light";</script>
</head>
<body>
<header class="topbar">
  <button id="menu" aria-label="Toggle navigation">☰</button>
  <a class="brand" href="{root}index.html">Guide</a>
  <input id="search" type="search" placeholder="Filter chapters…">
  <button id="theme" aria-label="Toggle theme">◐</button>
</header>
<div class="layout">
  <nav id="sidebar"></nav>
  <main><article id="content">Loading…</article></main>
</div>
<script type="text/markdown" id="source">{source}</script>
<script>window.GUIDE = {{ root: "{root}", page: "{page}", nav: {nav} }};</script>
<script src="https://cdn.jsdelivr.net/npm/marked@15/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script src="{root}assets/app.js"></script>
</body>
</html>
"""

CSS = """:root { --bg:#ffffff; --fg:#1f2328; --muted:#656d76; --line:#d0d7de; --side:#f6f8fa;
  --accent:#0969da; --code:#f6f8fa; --pill:#ddf4ff; }
[data-theme=dark] { --bg:#0d1117; --fg:#e6edf3; --muted:#8d96a0; --line:#30363d; --side:#010409;
  --accent:#4493f8; --code:#161b22; --pill:#12263f; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.65 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
a { color:var(--accent); text-decoration:none; } a:hover { text-decoration:underline; }
.topbar { position:sticky; top:0; z-index:10; display:flex; gap:12px; align-items:center;
  padding:10px 16px; background:var(--bg); border-bottom:1px solid var(--line); }
.topbar button { background:none; border:1px solid var(--line); color:var(--fg); border-radius:6px;
  padding:4px 10px; cursor:pointer; font-size:16px; }
.brand { font-weight:700; font-size:18px; color:var(--fg); }
#search { margin-left:auto; width:240px; padding:6px 10px; border-radius:6px;
  border:1px solid var(--line); background:var(--side); color:var(--fg); }
.layout { display:flex; }
#sidebar { width:300px; flex:none; height:calc(100vh - 53px); position:sticky; top:53px;
  overflow-y:auto; padding:12px 8px 40px; background:var(--side); border-right:1px solid var(--line);
  font-size:14px; }
#sidebar details { margin-bottom:4px; }
#sidebar summary { cursor:pointer; font-weight:600; padding:6px 8px; border-radius:6px; }
#sidebar summary:hover { background:var(--pill); }
#sidebar .part { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em;
  margin:10px 8px 2px 16px; }
#sidebar a { display:block; padding:3px 8px 3px 16px; border-radius:6px; color:var(--fg); }
#sidebar a.todo { color:var(--muted); font-style:italic; }
#sidebar a.active { background:var(--pill); color:var(--accent); font-weight:600; }
#sidebar a .done { color:#1a7f37; margin-right:4px; }
main { flex:1; min-width:0; padding:32px 48px 80px; }
article { max-width:900px; margin:0 auto; }
article h1 { font-size:2em; border-bottom:1px solid var(--line); padding-bottom:.3em; }
article h2 { margin-top:2em; padding-bottom:.25em; border-bottom:1px solid var(--line); }
article blockquote { margin:0; padding:.4em 1em; color:var(--muted); border-left:4px solid var(--line); }
article table { border-collapse:collapse; display:block; overflow-x:auto; margin:1em 0; }
article th, article td { border:1px solid var(--line); padding:6px 12px; }
article th { background:var(--side); }
article code { background:var(--code); padding:.15em .4em; border-radius:4px; font-size:.9em; }
article pre { background:var(--code); padding:14px 16px; border-radius:8px; overflow-x:auto;
  border:1px solid var(--line); line-height:1.45; }
article pre code { background:none; padding:0; }
article details { background:var(--side); border:1px solid var(--line); border-radius:8px;
  padding:6px 14px; margin:8px 0; }
article summary { cursor:pointer; font-weight:600; color:var(--accent); }
article .mermaid { background:#fff; border-radius:8px; padding:12px; margin:1em 0; text-align:center;
  border:1px solid var(--line); overflow-x:auto; }
article li input[type=checkbox] { transform:scale(1.2); margin-right:6px; }
.pager { display:flex; justify-content:space-between; gap:12px; margin-top:48px; }
.pager a { flex:1; border:1px solid var(--line); border-radius:8px; padding:10px 14px; }
.pager a.next { text-align:right; }
.pager small { display:block; color:var(--muted); }
.cards { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; }
.card { border:1px solid var(--line); border-radius:10px; padding:16px; color:var(--fg); }
.card:hover { border-color:var(--accent); text-decoration:none; }
.card b { display:block; font-size:17px; margin-bottom:4px; }
.card span { color:var(--muted); font-size:14px; }
.bar { height:6px; background:var(--line); border-radius:3px; margin-top:10px; overflow:hidden; }
.bar i { display:block; height:100%; background:#1a7f37; }
@media (max-width:900px) {
  #sidebar { position:fixed; left:0; z-index:9; transform:translateX(-100%); transition:transform .2s; }
  body.nav-open #sidebar { transform:none; }
  main { padding:20px; } #search { width:140px; }
}
"""

JS = r"""(function () {
  const G = window.GUIDE;
  const progressKey = "guide-progress";
  const progress = JSON.parse(localStorage.getItem(progressKey) || "{}");

  // ---- sidebar ----
  const side = document.getElementById("sidebar");
  let navHtml = "";
  for (const vol of G.nav) {
    const open = vol.chapters.some(c => c.page === G.page) || vol.index === G.page;
    navHtml += `<details ${open ? "open" : ""}><summary>${vol.title}</summary>`;
    navHtml += `<a href="${G.root}${vol.index}" class="${vol.index === G.page ? "active" : ""}">Contents</a>`;
    let part = null;
    for (const c of vol.chapters) {
      if (c.part && c.part !== part) { part = c.part; navHtml += `<div class="part">${part}</div>`; }
      const cls = [c.page === G.page ? "active" : "", c.exists ? "" : "todo"].join(" ");
      const done = progress[c.page] && progress[c.page].done ? '<span class="done">✓</span>' : "";
      navHtml += `<a class="${cls}" href="${G.root}${c.page}" data-title="${c.title.toLowerCase()}">${done}${c.n}. ${c.title}</a>`;
    }
    navHtml += "</details>";
  }
  side.innerHTML = navHtml;
  const activeLink = side.querySelector("a.active");
  if (activeLink) activeLink.scrollIntoView({ block: "center" });

  document.getElementById("menu").onclick = () => document.body.classList.toggle("nav-open");
  document.getElementById("search").oninput = e => {
    const q = e.target.value.toLowerCase().trim();
    side.querySelectorAll("details").forEach(d => { if (q) d.open = true; });
    side.querySelectorAll("a[data-title]").forEach(a => {
      a.style.display = !q || a.dataset.title.includes(q) ? "" : "none";
    });
  };
  document.getElementById("theme").onclick = () => {
    const t = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = t;
    localStorage.setItem("theme", t);
  };

  // ---- content ----
  const content = document.getElementById("content");
  const src = document.getElementById("source").textContent;
  if (!src.trim()) { renderHome(); return; }

  // Markdown links to .md files become links to the generated .html files.
  const renderer = new marked.Renderer();
  const baseLink = renderer.link.bind(renderer);
  renderer.link = function (token) {
    if (token.href && !/^[a-z]+:/i.test(token.href)) token.href = token.href.replace(/\.md(#|$)/, ".html$1");
    return baseLink(token);
  };
  renderer.code = function (token) {
    const esc = token.text.replace(/&/g, "&amp;").replace(/</g, "&lt;");
    if (token.lang === "mermaid") return `<pre class="mermaid">${esc}</pre>`;
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
    .replace(/(<p>)?@@FOLD(\d+)@@(<\/p>)?/g, (m, a, i) => folds[+i]);

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

  mermaid.initialize({ startOnLoad: false, theme: "default", securityLevel: "loose" });
  mermaid.run({ querySelector: ".mermaid" });

  function renderHome() {
    let h = "<h1>Mastery Guide</h1><p>From computer science foundations to AI systems engineering. Pick a volume to start.</p><div class='cards'>";
    for (const v of G.nav) {
      const total = v.chapters.length;
      const done = v.chapters.filter(c => progress[c.page] && progress[c.page].done).length;
      h += `<a class="card" href="${G.root}${v.index}"><b>${v.title}</b><span>${total} chapters · ${done} done</span>` +
           `<div class="bar"><i style="width:${total ? (100 * done / total) : 0}%"></i></div></a>`;
    }
    content.innerHTML = h + "</div>";
  }
})();
"""


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().replace("&", "and")).strip("-")
    return "-".join(slug.split("-")[:7])


def collect_nav():
    nav = []
    for index in sorted(SRC.glob("*/index.md")):
        vol_dir = index.parent.name
        text = index.read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
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
        nav.append(dict(title=title, index=f"volumes/{vol_dir}/index.html", chapters=chapters))
    return nav


def write_page(out_path, title, page, source, nav):
    depth = page.count("/")
    root = "../" * depth
    # "</script" inside the embedded source would end the tag early.
    safe = source.replace("</script", "<\\/script")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(TEMPLATE.format(title=html.escape(title), root=root, page=page,
                                        source=safe, nav=json.dumps(nav)), encoding="utf-8")


def main():
    nav = collect_nav()
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "app.js").write_text(JS, encoding="utf-8")

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
            if c["exists"]:
                source = (ROOT / c["md"]).read_text(encoding="utf-8")
            else:
                source = f"# Chapter {c['n']} — {c['title']}\n\n> Not written yet. See the [volume contents](index.md) for the chapter outline."
            write_page(OUT / c["page"], c["title"], c["page"], source, nav)
            count += 1

    written = sum(c["exists"] for v in nav for c in v["chapters"])
    total = sum(len(v["chapters"]) for v in nav)
    print(f"Built {count} pages into {OUT} ({written}/{total} chapters written)")


if __name__ == "__main__":
    main()
