// Hand-built SVG figures (<div class="fig"><svg>…</svg></div>): give them the same frame as the Mermaid diagrams —
// click to zoom and pan, an Expand button and an SVG download.
(function () {
  'use strict';
  var hosts = [];
  document.querySelectorAll('.main .fig').forEach(function (h) { if (h.querySelector('svg')) hosts.push(h); });
  if (!hosts.length) return;

  // the downloaded file has no page CSS, so write the theme colours into it
  function resolved(svg) {
    var cs = getComputedStyle(document.documentElement), copy = svg.cloneNode(true);
    var sub = function (v) { return v.replace(/var\((--[\w-]+)\)/g, function (_, n) { return cs.getPropertyValue(n).trim() || '#888'; }); };
    [copy].concat([].slice.call(copy.querySelectorAll('*'))).forEach(function (el) {
      ['fill', 'stroke', 'style'].forEach(function (a) { if (el.hasAttribute(a)) el.setAttribute(a, sub(el.getAttribute(a))); });
    });
    copy.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    var bg = cs.getPropertyValue('--bg').trim() || '#ffffff';
    copy.insertAdjacentHTML('afterbegin', '<rect width="100%" height="100%" fill="' + bg + '"/>');
    return copy;
  }

  function go() {
    var D = window.SDDiagrams;
    if (!D || !D.figure) return;
    hosts.forEach(function (h) {
      var svg = h.querySelector('svg');
      var open = function () { D.lightbox(svg, D.titleFor(h), true); };
      var extra = [
        D.button('Expand', 'Open in the zoom viewer', open),
        D.button('SVG', 'Download as an SVG file', function () {
          var a = document.createElement('a');
          a.href = URL.createObjectURL(new Blob([resolved(svg).outerHTML], { type: 'image/svg+xml' }));
          a.download = (D.titleFor(h).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'diagram') + '.svg';
          a.click();
        })
      ];
      D.figure(h, 'Diagram', extra);
      h.style.cursor = 'zoom-in';
      h.addEventListener('click', function (e) { if (!e.target.closest('a,button')) open(); });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
