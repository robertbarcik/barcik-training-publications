/* Riso reader: the display control on every publication page.
   Loaded in <head> (blocking, tiny) so the saved display is applied before first paint.
   Three displays: Paper (default), Calm, Night; two text sizes. The choice is remembered per
   browser and shared by all publications. Nothing here touches <main>. */
(function () {
  var KEY = 'rz-display', root = document.documentElement, st = { mode: 'paper', size: 'normal' };
  try { var saved = JSON.parse(localStorage.getItem(KEY) || '{}'); if (saved.mode) st.mode = saved.mode; if (saved.size) st.size = saved.size; } catch (e) {}
  function apply() {
    if (st.mode === 'paper') root.removeAttribute('data-mode'); else root.setAttribute('data-mode', st.mode);
    if (st.size === 'large') root.setAttribute('data-size', 'large'); else root.removeAttribute('data-size');
  }
  apply();

  var L = { en: { label: 'Display', paper: 'Paper', calm: 'Calm', night: 'Night', size: 'Text size', normal: 'Normal text', large: 'Larger text' },
            sk: { label: 'Zobrazenie', paper: 'Papier', calm: 'Pokojné', night: 'Nočné', size: 'Veľkosť textu', normal: 'Bežný text', large: 'Väčší text' },
            cs: { label: 'Zobrazení', paper: 'Papír', calm: 'Klidné', night: 'Noční', size: 'Velikost textu', normal: 'Běžný text', large: 'Větší text' } };

  function build() {
    var t = L[(root.lang || 'en').slice(0, 2)] || L.en;
    var el = document.createElement('div');
    el.className = 'rz-ctl';
    el.setAttribute('role', 'group');
    el.setAttribute('aria-label', t.label);
    var modes = ['paper', 'calm', 'night'].map(function (m) {
      return '<button type="button" data-mode="' + m + '"><i class="rz-sw" aria-hidden="true"></i>' + t[m] + '</button>';
    }).join('');
    el.innerHTML = '<button type="button" class="rz-ctl-toggle" aria-expanded="false" aria-label="' + t.label + '">Aa</button>' +
      '<div class="rz-ctl-panel"><span>' + modes + '</span>' +
      '<span role="group" aria-label="' + t.size + '"><button type="button" data-size="normal" aria-label="' + t.normal + '">A</button>' +
      '<button type="button" data-size="large" aria-label="' + t.large + '">A</button></span></div>';
    document.body.appendChild(el);
    function sync() {
      el.querySelectorAll('[data-mode]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.mode === st.mode)); });
      el.querySelectorAll('[data-size]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.size === st.size)); });
    }
    var toggle = el.querySelector('.rz-ctl-toggle');
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b === toggle) { toggle.setAttribute('aria-expanded', String(el.classList.toggle('open'))); return; }
      // keep the reader's place: the text reflows when the display or size changes
      var keep = anchor();
      if (b.dataset.mode) st.mode = b.dataset.mode;
      if (b.dataset.size) st.size = b.dataset.size;
      apply(); sync(); restore(keep);
      try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (err) {}
    });
    document.addEventListener('click', function (e) { if (!el.contains(e.target) && el.classList.contains('open')) { el.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && el.classList.contains('open')) { el.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); } });
    sync();
    // at the top of the page the three displays are spelled out; further down they fold into "Aa"
    var folded = false;
    function fold() {
      var f = window.scrollY > 140;
      if (f === folded) return;
      folded = f; root.classList.toggle('rz-scrolled', f);
      el.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false');
    }
    window.addEventListener('scroll', fold, { passive: true }); fold();
    // textbook pages have no way back to the shelf: add one to the sidebar header
    var head = document.getElementById('sidebar-header');
    if (head && !head.querySelector('.all-pubs-link')) {
      var a = document.createElement('a');
      a.className = 'all-pubs-link'; a.href = '/';
      a.textContent = { sk: '← Všetky publikácie', cs: '← Všechny publikace' }[(root.lang || 'en').slice(0, 2)] || '← All Publications';
      head.insertBefore(a, head.firstChild);
    }
  }
  // the first block element at the top of the viewport, and how far it is from the top
  function anchor() {
    var main = document.querySelector('main') || document.body, els = main.querySelectorAll('p, h1, h2, h3, li, pre, table, figure');
    for (var i = 0; i < els.length; i++) { var r = els[i].getBoundingClientRect(); if (r.bottom > 0) return { el: els[i], top: r.top }; }
    return null;
  }
  function restore(k) { if (k) window.scrollBy(0, k.el.getBoundingClientRect().top - k.top); }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
