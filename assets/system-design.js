// ============================== THEME TOGGLE ==============================
(function () {
  const themeToggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  const saved = localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  html.setAttribute('data-theme', saved);
  if (themeToggle) {
    themeToggle.textContent = saved === 'dark' ? '☀️' : '🌙';
    themeToggle.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      themeToggle.textContent = next === 'dark' ? '☀️' : '🌙';
    });
  }
})();

// ============================== READING PROGRESS ==============================
(function () {
  const bar = document.getElementById('progressBar');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
  }, { passive: true });
})();

// ============================== TOC ACTIVE LINK ==============================
(function () {
  const tocLinks = document.querySelectorAll('#tocList a');
  if (!tocLinks.length) return;
  const linkFor = new Map();
  tocLinks.forEach(a => {
    const target = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
    if (target) linkFor.set(target, a);
  });
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const link = linkFor.get(entry.target);
      if (entry.isIntersecting && link) {
        tocLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
      }
    });
  }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });
  linkFor.forEach((_, s) => observer.observe(s));
})();

// ============================== MOBILE MENU ==============================
(function () {
  const menuBtn = document.getElementById('menuBtn');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  if (!menuBtn || !sidebar) return;
  menuBtn.addEventListener('click', () => {
    sidebar.classList.add('open');
    if (overlay) overlay.classList.add('show');
  });
  if (overlay) overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
  });
  document.querySelectorAll('#tocList a').forEach(a => {
    a.addEventListener('click', () => {
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('show');
    });
  });
})();

// ============================== COPY CODE BUTTONS ==============================
(function () {
  document.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.copy-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', async () => {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      try {
        await navigator.clipboard.writeText(code);
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1500);
      } catch (e) { btn.textContent = 'Failed'; }
    });
    pre.appendChild(btn);
  });
})();

// ============================== FLIP CARDS ==============================
(function () {
  document.querySelectorAll('.flip-card').forEach(card => {
    card.addEventListener('click', () => card.classList.toggle('flipped'));
  });
})();

// ============================== PRISM HIGHLIGHT ==============================
if (typeof Prism !== 'undefined') Prism.highlightAll();

// ============================== DIAGRAM VIEWER ==============================
// Wraps every Mermaid diagram and every plain-text (ASCII) diagram in a figure with a toolbar,
// keeps wide diagrams at a readable size (they scroll instead of shrinking), and opens a
// zoom / pan viewer on click. Mermaid flowcharts also highlight a node's connections on hover.
window.SDDiagrams = (function () {
  const MIN_SCALE = 0.75;          // never draw diagram text smaller than 75% of its natural size
  const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  function titleFor(el) {
    const fig = el.closest('figure');
    let h = fig ? fig.previousElementSibling : el.previousElementSibling;
    while (h && !/^H[1-6]$/.test(h.tagName)) h = h.previousElementSibling;
    return h ? h.textContent.trim().replace(/^[\d.]+\s+/, '') : 'Diagram';
  }
  function button(label, title, fn) {
    const b = document.createElement('button');
    b.className = 'sd-btn'; b.type = 'button'; b.textContent = label; b.title = title;
    b.addEventListener('click', e => { e.stopPropagation(); fn(b); });
    return b;
  }
  function flash(b, text) {
    const old = b.textContent; b.textContent = text; b.classList.add('ok');
    setTimeout(() => { b.textContent = old; b.classList.remove('ok'); }, 1400);
  }
  function figure(host, kind, extra) {
    if (host.parentElement && host.parentElement.classList.contains('sd-diagram')) return host.parentElement;
    const fig = document.createElement('figure');
    fig.className = 'sd-diagram ' + (kind === 'Text diagram' ? 'sd-text' : 'sd-mermaid');
    const bar = document.createElement('div'); bar.className = 'sd-bar';
    const k = document.createElement('span'); k.className = 'sd-kind'; k.textContent = kind;
    const hint = document.createElement('span'); hint.className = 'sd-hint'; hint.textContent = 'Click to zoom and pan';
    bar.append(k, hint);
    (extra || []).forEach(b => bar.appendChild(b));
    host.parentNode.insertBefore(fig, host);
    fig.append(bar, host);
    return fig;
  }

  // ---------- sizing: readable minimum, scroll instead of shrink ----------
  function fit(m) {
    const svg = m.querySelector('svg'); if (!svg) return;
    const vb = svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width;
    if (!vb) return;
    const cs = getComputedStyle(m);
    const fig = m.closest('.sd-diagram');
    if (fig) fig.style.marginRight = '';
    let avail = m.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    // too wide for the text column: on wide screens, grow into the empty space to its right first
    if (fig && vb * MIN_SCALE > avail && window.innerWidth > 1024) {
      const room = Math.max(0, window.innerWidth - fig.getBoundingClientRect().right - 24);
      const grow = Math.min(room, Math.ceil(vb * MIN_SCALE - avail));
      fig.style.marginRight = -grow + 'px'; avail += grow;
    }
    svg.removeAttribute('height');
    svg.style.maxWidth = 'none';
    if (vb * MIN_SCALE > avail) {                       // too wide: keep text readable, let it scroll
      svg.style.width = Math.round(vb * MIN_SCALE) + 'px';
      if (fig) fig.classList.add('sd-scrolls');
    } else {                                            // fits: fill the space but never upscale past natural size
      svg.style.width = Math.min(avail, vb) + 'px';
      if (fig) fig.classList.remove('sd-scrolls');
    }
  }

  // ---------- hover focus for flowcharts ----------
  function hoverFocus(m) {
    const svg = m.querySelector('svg'); if (!svg || svg.dataset.sdHover) return;
    svg.dataset.sdHover = '1';
    const fig = m.closest('.sd-diagram');
    const keyOf = n => (n.id || '').replace(/^flowchart-/, '').replace(/-\d+$/, '');
    const edges = [...svg.querySelectorAll('.flowchart-link')];
    if (!edges.length) return;
    const nodes = [...svg.querySelectorAll('g.node')];
    nodes.forEach(n => {
      const key = keyOf(n); if (!key) return;
      n.addEventListener('mouseenter', () => {
        const hitNodes = new Set([n]); const hitEdges = [];
        edges.forEach(e => {
          const body = (e.id || '').replace(/^L[-_]/, '').replace(/[-_]\d+$/, '');
          const other = nodes.find(o => { const ok = keyOf(o); return ok && ok !== key && (body === ok + '-' + key || body === key + '-' + ok); });
          if (other) { hitEdges.push(e); hitNodes.add(other); }
        });
        if (!hitEdges.length) return;
        fig.classList.add('sd-focus');
        svg.querySelectorAll('.sd-hl').forEach(x => x.classList.remove('sd-hl'));
        hitNodes.forEach(x => x.classList.add('sd-hl')); hitEdges.forEach(x => x.classList.add('sd-hl'));
      });
      n.addEventListener('mouseleave', () => {
        fig.classList.remove('sd-focus');
        svg.querySelectorAll('.sd-hl').forEach(x => x.classList.remove('sd-hl'));
      });
    });
  }

  // ---------- lightbox with zoom / pan ----------
  function lightbox(node, title, isSvg) {
    const ov = document.createElement('div'); ov.className = 'sd-lightbox';
    ov.innerHTML = '<div class="sd-lb-bar"><span class="sd-lb-title"></span>' +
      '<button class="sd-btn" data-a="out" title="Zoom out (-)">&minus;</button><span class="sd-lb-zoom">100%</span>' +
      '<button class="sd-btn" data-a="in" title="Zoom in (+)">+</button>' +
      '<button class="sd-btn" data-a="fit" title="Fit to screen (0)">Fit</button>' +
      '<button class="sd-btn" data-a="one" title="Actual size (1)">100%</button>' +
      '<button class="sd-btn" data-a="close" title="Close (Esc)">Close</button></div>' +
      '<div class="sd-lb-stage"><div class="sd-lb-content"></div></div>' +
      '<div class="sd-lb-help">Scroll to zoom &middot; drag to pan &middot; double-click to fit &middot; Esc to close</div>';
    ov.querySelector('.sd-lb-title').textContent = title;
    const stage = ov.querySelector('.sd-lb-stage'), box = ov.querySelector('.sd-lb-content'), zl = ov.querySelector('.sd-lb-zoom');
    let content;
    if (isSvg) {
      content = node.cloneNode(true);
      const vbw = node.viewBox.baseVal.width, vbh = node.viewBox.baseVal.height;
      content.removeAttribute('style'); content.setAttribute('width', vbw); content.setAttribute('height', vbh);
    } else { content = node.cloneNode(true); content.classList.remove('sd-body'); }
    box.appendChild(content);
    document.body.appendChild(ov); document.body.style.overflow = 'hidden';
    let k = 1, x = 0, y = 0;
    const size = () => ({ w: box.offsetWidth, h: box.offsetHeight });
    const apply = () => { box.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + k + ')'; zl.textContent = Math.round(k * 100) + '%'; };
    const fitAll = () => {
      const s = size(), W = stage.clientWidth, H = stage.clientHeight;
      k = Math.min((W - 40) / s.w, (H - 40) / s.h, 3); x = (W - s.w * k) / 2; y = (H - s.h * k) / 2; apply();
    };
    const actual = () => { const s = size(); k = 1; x = (stage.clientWidth - s.w) / 2; y = (stage.clientHeight - s.h) / 2; apply(); };
    const zoomAt = (f, cx, cy) => {
      const nk = Math.max(0.1, Math.min(8, k * f)); const r = nk / k;
      x = cx - (cx - x) * r; y = cy - (cy - y) * r; k = nk; apply();
    };
    const center = () => ({ cx: stage.clientWidth / 2, cy: stage.clientHeight / 2 });
    const close = () => { ov.remove(); document.body.style.overflow = ''; document.removeEventListener('keydown', key, true); };
    function key(e) {
      if (e.key === 'Escape') close();
      else if (e.key === '+' || e.key === '=') { const c = center(); zoomAt(1.25, c.cx, c.cy); }
      else if (e.key === '-') { const c = center(); zoomAt(0.8, c.cx, c.cy); }
      else if (e.key === '0') fitAll();
      else if (e.key === '1') actual();
      else return;
      e.preventDefault(); e.stopPropagation();
    }
    document.addEventListener('keydown', key, true);
    ov.querySelector('.sd-lb-bar').addEventListener('click', e => {
      const a = e.target.dataset && e.target.dataset.a; if (!a) return; const c = center();
      if (a === 'close') close(); else if (a === 'fit') fitAll(); else if (a === 'one') actual();
      else if (a === 'in') zoomAt(1.25, c.cx, c.cy); else if (a === 'out') zoomAt(0.8, c.cx, c.cy);
    });
    stage.addEventListener('wheel', e => {
      e.preventDefault(); const r = stage.getBoundingClientRect();
      zoomAt(e.deltaY < 0 ? 1.12 : 1 / 1.12, e.clientX - r.left, e.clientY - r.top);
    }, { passive: false });
    let drag = null;
    stage.addEventListener('pointerdown', e => { drag = { px: e.clientX, py: e.clientY, x: x, y: y }; stage.classList.add('drag'); stage.setPointerCapture(e.pointerId); });
    stage.addEventListener('pointermove', e => { if (!drag) return; x = drag.x + e.clientX - drag.px; y = drag.y + e.clientY - drag.py; apply(); });
    const end = () => { drag = null; stage.classList.remove('drag'); };
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    stage.addEventListener('dblclick', fitAll);
    requestAnimationFrame(fitAll);
  }

  // ---------- mermaid ----------
  function mermaid() {
    document.querySelectorAll('.main .mermaid').forEach(m => {
      if (!m.querySelector('svg')) return;
      const open = () => lightbox(m.querySelector('svg'), titleFor(m), true);
      if (!m.closest('.sd-diagram')) {
        const src = m.dataset.src || '';
        const extra = [
          button('Expand', 'Open in the zoom viewer', open),
          button('Copy source', 'Copy the Mermaid source', b => navigator.clipboard.writeText(src).then(() => flash(b, 'Copied'), () => flash(b, 'Failed'))),
          button('SVG', 'Download as an SVG file', () => {
            const svg = m.querySelector('svg').cloneNode(true); svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            const a = document.createElement('a');
            a.href = URL.createObjectURL(new Blob([svg.outerHTML], { type: 'image/svg+xml' }));
            a.download = (titleFor(m).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'diagram') + '.svg'; a.click();
          }),
        ];
        figure(m, 'Diagram', extra);
        m.addEventListener('click', e => { if (!e.target.closest('a')) open(); });
      }
      fit(m); hoverFocus(m);
    });
  }

  // ---------- plain-text (ASCII) diagrams ----------
  function looksLikeDiagram(t) {
    const lines = t.split('\n').filter(l => l.trim());
    if (lines.length < 3) return false;
    if (/[─│┌┐└┘├┤┬┴┼═║╔╗╚╝▼▲►◄]/.test(t)) return true;
    if (/\+-{2,}\+/.test(t) && /\|/.test(t)) return true;
    return lines.filter(l => /(-->|==>|<--|\s->\s|\s<-\s|[→←↑↓↔⇒])/.test(l)).length >= 2;
  }
  function decorate(text) {
    return esc(text)
      .replace(/(\[[^\]\n]{1,44}\])/g, '<span class="tx-node">$1</span>')
      .replace(/([─│┌┐└┘├┤┬┴┼═║╔╗╚╝]+|\+-{2,}\+?)/g, '<span class="tx-box">$1</span>')
      .replace(/(-{1,3}&gt;|={1,3}&gt;|&lt;-{1,3}|[→←↑↓▼▲►◄↔⇒])/g, '<span class="tx-arrow">$1</span>');
  }
  function text() {
    document.querySelectorAll('.main pre > code').forEach(code => {
      const pre = code.parentElement;
      if (pre.dataset.sdText || pre.closest('.sd-diagram')) return;
      if (/language-(?!text|ascii|plaintext|txt)/.test(code.className)) return;
      const t = code.textContent; if (!looksLikeDiagram(t)) return;
      pre.dataset.sdText = '1'; code.innerHTML = decorate(t); pre.classList.add('sd-body');
      const extra = [
        button('Expand', 'Open in the zoom viewer', () => lightbox(pre, titleFor(pre), false)),
        button('Copy', 'Copy the text', b => navigator.clipboard.writeText(t).then(() => flash(b, 'Copied'), () => flash(b, 'Failed'))),
      ];
      figure(pre, 'Text diagram', extra);
      pre.addEventListener('click', () => lightbox(pre, titleFor(pre), false));
    });
  }

  let timer;
  window.addEventListener('resize', () => { clearTimeout(timer); timer = setTimeout(() => document.querySelectorAll('.main .mermaid').forEach(fit), 150); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', text); else text();
  return { mermaid: mermaid, text: text, lightbox: lightbox, figure: figure, button: button, flash: flash, titleFor: titleFor };
})();
