// Guide extras: progress tracking (kept in this browser), chapter list in the sidebar, checklists that remember their state.
(function () {
  var G = window.GUIDE;
  if (!G) return;
  var KEY = 'guide-progress';
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } }
  function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) { /* private mode: progress just will not persist */ } }
  var P = load();
  var isDone = function (page) { return !!(P[page] && P[page].done); };
  var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };

  // ---------- chapter list in the sidebar ----------
  function volumeNav() {
    var side = document.getElementById('sidebar');
    if (!side || !G.chapters) return;
    var box = document.createElement('div'); box.className = 'guide-vol';
    var html = '<h3>' + esc(G.volumeTitle) + '</h3>', part = null;
    G.chapters.forEach(function (c) {
      if (c.part && c.part !== part) { part = c.part; html += '<div class="vol-part">' + esc(c.part) + '</div>'; }
      var cls = (c.page === G.page ? 'current ' : '') + (isDone(c.page) ? 'done' : '');
      html += '<a class="' + cls + '" href="' + c.href + '"><span class="n">' + c.n + '</span><span>' + esc(c.title) + '</span><span class="tick">✓</span></a>';
    });
    box.innerHTML = html;
    side.appendChild(box);
    var cur = box.querySelector('a.current');
    if (cur && cur.scrollIntoView) setTimeout(function () { /* keep the contents list in view without moving the page */ cur.scrollIntoView({ block: 'nearest' }); }, 0);
  }

  // ---------- checklists + "mark complete" ----------
  function chapterTools() {
    var main = document.getElementById('main');
    if (!main) return;
    var state = P[G.page] || { boxes: [], done: false };
    var boxes = main.querySelectorAll('li input[type="checkbox"]');
    boxes.forEach(function (b, i) {
      b.disabled = false;
      b.checked = !!state.boxes[i];
      b.addEventListener('change', function () {
        state.boxes[i] = b.checked; P[G.page] = state; save(P);
      });
    });
    var nav = main.querySelector(':scope > .chapter-nav');
    var row = document.createElement('div'); row.className = 'complete-row';
    row.innerHTML = '<p>Finished this chapter? Mark it complete to track your progress (saved in this browser).</p>';
    var btn = document.createElement('button'); btn.className = 'complete-btn'; btn.type = 'button';
    var paint = function () { btn.textContent = state.done ? '✓ Completed' : 'Mark chapter complete'; btn.classList.toggle('is-done', state.done); };
    btn.addEventListener('click', function () {
      state.done = !state.done; P[G.page] = state; save(P); paint();
      var link = document.querySelector('.guide-vol a.current'); if (link) link.classList.toggle('done', state.done);
    });
    paint(); row.appendChild(btn);
    main.insertBefore(row, nav);
  }

  // ---------- badges and counters on the contents pages ----------
  function badges() {
    document.querySelectorAll('.chapter-card[data-page]').forEach(function (a) {
      if (isDone(a.getAttribute('data-page'))) a.classList.add('done');
      if (!a.querySelector('.done-badge')) { var s = document.createElement('span'); s.className = 'done-badge'; s.textContent = '✓ Done'; a.appendChild(s); }
    });
    document.querySelectorAll('[data-vol]').forEach(function (el) {
      var prefix = el.getAttribute('data-vol'), total = +el.getAttribute('data-total') || 0, n = 0;
      Object.keys(P).forEach(function (k) { if (k.indexOf(prefix) === 0 && P[k].done) n++; });
      var out = el.querySelector('.vol-progress');
      if (!out) { out = document.createElement('span'); out.className = 'vol-progress'; el.appendChild(out); }
      out.innerHTML = n + ' of ' + total + ' chapters done<span class="bar"><i style="width:' + (total ? Math.round(100 * n / total) : 0) + '%"></i></span>';
    });
  }

  // Wrap what is inside each collapsible box so it can be padded (bare text cannot be styled directly).
  function wrapDetails() {
    document.querySelectorAll('.main details').forEach(function (d) {
      if (d.querySelector(':scope > .d-body')) return;
      var body = document.createElement('div'); body.className = 'd-body';
      var sum = d.querySelector(':scope > summary');
      var nodes = Array.prototype.slice.call(d.childNodes).filter(function (n) { return n !== sum; });
      nodes.forEach(function (n) { body.appendChild(n); });
      d.appendChild(body);
    });
  }

  function run() { if (G.kind === 'chapter') { wrapDetails(); volumeNav(); chapterTools(); } badges(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
