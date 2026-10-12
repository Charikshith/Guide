(function boot() {
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
