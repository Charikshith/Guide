// Venn diagrams: turns ```venn code blocks into real, theme-aware SVG (two or three overlapping circles).
//
//   sets: A | B | C              2 or 3 set ids
//   name A: Consistency          optional longer label for a set
//   title: Optional heading
//   shade: A&B, outside          regions to fill ("outside" = in none of the sets; A&B = in A and B only)
//   label A&B: text              text inside a region (\n starts a new line)
//   note: Caption under the diagram
//   universe: off                hide the surrounding box
//   ---                          a line of three dashes starts another diagram (shown side by side)
//
// Region keys are set ids joined with & (in the order given in "sets"); a single id means "only that set".
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var uid = 0;
  var COLORS = ['var(--primary)', 'var(--accent)', 'var(--success)'];
  var GEOM = {
    2: { w: 320, h: 200, r: 70, c: [[115, 100], [205, 100]], names: [[78, 22], [242, 22]], out: [20, 186],
         pos: { 1: [78, 100], 2: [242, 100], 3: [160, 100] }, max: 380 },
    3: { w: 360, h: 330, r: 82, c: [[140, 125], [220, 125], [180, 195]], names: [[84, 24], [276, 24], [180, 316]], out: [20, 24],
         pos: { 1: [100, 100], 2: [260, 100], 4: [180, 255], 3: [180, 88], 5: [135, 185], 6: [225, 185], 7: [180, 150] }, max: 430 }
  };

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function parse(src) {
    var d = { sets: [], names: {}, shade: [], labels: {}, title: '', note: '', universe: true, src: src };
    src.split('\n').forEach(function (raw) {
      var line = raw.trim();
      if (!line || line.charAt(0) === '#') return;
      var m = line.match(/^([a-z]+)(?:\s+(\S+))?\s*:\s*(.*)$/i);
      if (!m) return;
      var key = m[1].toLowerCase(), arg = m[2], val = m[3].trim();
      if (key === 'sets') d.sets = val.split('|').map(function (s) { return s.trim(); }).filter(Boolean);
      else if (key === 'name') d.names[arg] = val;
      else if (key === 'title') d.title = val;
      else if (key === 'note') d.note = val;
      else if (key === 'universe') d.universe = !/^(off|no|false)$/i.test(val);
      else if (key === 'shade') d.shade = val.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
      else if (key === 'label') d.labels[arg] = val.replace(/\\n/g, '\n');
    });
    return d;
  }

  // "A&B" -> bit mask (bit i set = inside set i); "outside" -> 0; unknown -> -1
  function maskOf(d, key) {
    if (/^outside$/i.test(key)) return 0;
    var mask = 0, ok = true;
    key.split('&').forEach(function (p) {
      var i = d.sets.indexOf(p.trim());
      if (i < 0) ok = false; else mask |= (1 << i);
    });
    return ok ? mask : -1;
  }

  function popcount(n) { var c = 0; while (n) { c += n & 1; n >>= 1; } return c; }

  function build(d) {
    var n = d.sets.length, g = GEOM[n];
    if (!g) return null;
    var id = 'v' + (++uid) + '_', W = g.w, H = g.h, defs = '', i;
    for (i = 0; i < n; i++) defs += '<clipPath id="' + id + 'c' + i + '"><circle cx="' + g.c[i][0] + '" cy="' + g.c[i][1] + '" r="' + g.r + '"/></clipPath>';

    function region(mask, attrs) {
      var ins = [], outs = [], k;
      for (k = 0; k < n; k++) (mask >> k & 1 ? ins : outs).push(k);
      var inner = '<rect x="6" y="6" width="' + (W - 12) + '" height="' + (H - 12) + '" ' + attrs + '/>';
      ins.forEach(function (s) { inner = '<g clip-path="url(#' + id + 'c' + s + ')">' + inner + '</g>'; });
      if (outs.length) {
        var mid = id + 'm' + mask;
        defs += '<mask id="' + mid + '" maskUnits="userSpaceOnUse" x="0" y="0" width="' + W + '" height="' + H + '"><rect width="' + W + '" height="' + H + '" fill="#fff"/>' +
          outs.map(function (s) { return '<circle cx="' + g.c[s][0] + '" cy="' + g.c[s][1] + '" r="' + g.r + '" fill="#000"/>'; }).join('') + '</mask>';
        inner = '<g mask="url(#' + mid + ')">' + inner + '</g>';
      }
      return inner;
    }

    var s = '';
    if (d.universe) s += '<rect class="v-universe" x="6" y="6" width="' + (W - 12) + '" height="' + (H - 12) + '" rx="12"/>';
    for (i = 0; i < n; i++) s += '<circle cx="' + g.c[i][0] + '" cy="' + g.c[i][1] + '" r="' + g.r + '" fill="' + COLORS[i] + '" fill-opacity=".10"/>';
    d.shade.forEach(function (k) {
      var m = maskOf(d, k);
      if (m < 0 || (m === 0 && !d.universe)) return;
      s += '<g class="v-shade">' + region(m, 'fill="var(--primary)" fill-opacity=".34"') + '</g>';
    });
    // hover areas: fewer sets first, so the more specific region sits on top and catches the pointer
    var masks = [];
    for (var mk = (d.universe ? 0 : 1); mk < (1 << n); mk++) masks.push(mk);
    masks.sort(function (a, b) { return popcount(a) - popcount(b); });
    masks.forEach(function (m) {
      var key = m === 0 ? 'outside' : d.sets.filter(function (_, j) { return m >> j & 1; }).join('&');
      var lab = d.labels[key];
      s += '<g class="v-hit">' + region(m, 'fill="var(--primary)" fill-opacity="0"') + (lab ? '<title>' + esc(lab.replace(/\n/g, ' ')) + '</title>' : '') + '</g>';
    });
    for (i = 0; i < n; i++) s += '<circle cx="' + g.c[i][0] + '" cy="' + g.c[i][1] + '" r="' + g.r + '" fill="none" stroke="' + COLORS[i] + '" stroke-width="2.4" pointer-events="none"/>';
    for (i = 0; i < n; i++) {
      var nm = d.names[d.sets[i]] || d.sets[i];
      s += '<text class="v-set" x="' + g.names[i][0] + '" y="' + g.names[i][1] + '" text-anchor="middle" fill="' + COLORS[i] + '">' + esc(nm) + '</text>';
    }
    Object.keys(d.labels).forEach(function (k) {
      var m = maskOf(d, k), p = m === 0 ? g.out : g.pos[m];
      if (m < 0 || !p) return;
      var lines = d.labels[k].split('\n'), y0 = p[1] - (lines.length - 1) * 8;
      s += '<text class="v-label' + (m === 0 ? ' v-out' : '') + '" x="' + p[0] + '" text-anchor="' + (m === 0 ? 'start' : 'middle') + '">' +
        lines.map(function (ln, j) { return '<tspan x="' + p[0] + '" y="' + (y0 + j * 16) + '" dominant-baseline="middle">' + esc(ln) + '</tspan>'; }).join('') + '</text>';
    });
    var svg = '<svg xmlns="' + NS + '" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(d.title || 'Venn diagram') + '" style="width:100%;max-width:' + g.max + 'px"><defs>' + defs + '</defs>' + s + '</svg>';
    return svg;
  }

  function item(d) {
    var el = document.createElement('div'); el.className = 'venn-item';
    var svg = build(d);
    if (!svg) { el.textContent = 'Venn diagram needs 2 or 3 sets.'; return el; }
    el.innerHTML = (d.title ? '<div class="venn-title">' + esc(d.title) + '</div>' : '') + svg + (d.note ? '<div class="venn-cap">' + esc(d.note) + '</div>' : '');
    return el;
  }

  function render(host) {
    var D = window.SDDiagrams;
    var src = host.getAttribute('data-src') || '';
    var parts = src.split(/\n-{3,}[ \t]*\n/).filter(function (p) { return p.trim(); });
    var row = document.createElement('div'); row.className = 'venn-row';
    var items = parts.map(function (p) { var d = parse(p); var it = item(d); it._d = d; row.appendChild(it); return it; });
    host.appendChild(row);
    host.className = 'venn-host';
    if (!D || !D.figure) return;
    var extra = [];
    if (items.length === 1) extra.push(D.button('Expand', 'Open in the zoom viewer', function () { D.lightbox(row.querySelector('svg'), (items[0]._d.title || D.titleFor(host)), true); }));
    extra.push(D.button('Copy source', 'Copy the venn source', function (b) { navigator.clipboard.writeText(src).then(function () { D.flash(b, 'Copied'); }, function () { D.flash(b, 'Failed'); }); }));
    D.figure(host, 'Venn diagram', extra).classList.add('sd-venn');
    row.querySelectorAll('svg').forEach(function (sv, k) {
      sv.style.cursor = 'zoom-in';
      sv.addEventListener('click', function () { D.lightbox(sv, items[k]._d.title || D.titleFor(host), true); });
    });
  }

  // Phase 1 (immediately): take the code blocks away from the syntax highlighter.
  var hosts = [];
  document.querySelectorAll('pre > code.language-venn').forEach(function (c) {
    var h = document.createElement('div'); h.className = 'venn-host'; h.setAttribute('data-src', c.textContent);
    c.parentNode.replaceWith(h); hosts.push(h);
  });
  // Phase 2 (once every script has run, so the diagram viewer helpers exist): draw.
  function go() { hosts.forEach(render); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
  window.SDVenn = { parse: parse, build: build };
})();
