/* Riso kit: search, shelf chips and the detail sheet for the publications shelf and the demos index.
   The page works without this file: every tile is a plain link. */
(function () {
  const band = document.getElementById('filters'), main = document.getElementById('shelves');
  if (!band || !main) return;
  const tiles = [...main.querySelectorAll('.tile')];
  const sections = [...main.querySelectorAll('[data-series]:not(.tile)')];
  const input = band.querySelector('input');
  const state = { q: '', series: 'all' };

  // what a tile can be found by: its caption, its cover, and the long description in its detail sheet
  const hay = new Map(tiles.map((t) => {
    const tpl = t.dataset.detail && document.getElementById(t.dataset.detail);
    return [t, (t.textContent + ' ' + (tpl ? tpl.content.textContent : '')).toLowerCase()];
  }));

  const empty = document.createElement('p');
  empty.className = 'empty'; empty.hidden = true;
  empty.innerHTML = 'Nothing matches that. Try a shorter search. <button type="button">Show everything</button>';
  main.after(empty);
  empty.style.maxWidth = '1240px'; empty.style.margin = '0 auto'; empty.style.padding = '3rem var(--gut)';

  function apply() {
    const words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    tiles.forEach((t) => {
      const ok = (state.series === 'all' || t.dataset.series === state.series) && words.every((w) => hay.get(t).includes(w));
      t.hidden = !ok; if (ok) shown++;
    });
    sections.forEach((s) => { s.hidden = !s.querySelector('.tile:not([hidden])'); });
    empty.hidden = shown > 0;
  }
  function setSeries(key) {
    state.series = key;
    band.querySelectorAll('.chip').forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.series === key)));
    apply();
  }
  input.addEventListener('input', () => { state.q = input.value.trim(); apply(); });
  band.addEventListener('click', (e) => {
    const c = e.target.closest('.chip'); if (!c) return;
    setSeries(c.dataset.series);
    // after choosing a shelf from far down the page, bring its top into view
    const top = main.getBoundingClientRect().top + scrollY - band.offsetHeight - 8;
    if (scrollY > top) scrollTo({ top });
  });
  empty.querySelector('button').addEventListener('click', () => { input.value = ''; state.q = ''; setSeries('all'); input.focus(); });

  /* ---------- detail sheet ---------- */
  if (!main.querySelector('.tile[data-detail]')) return;
  const dlg = document.createElement('dialog');
  dlg.className = 'detail';
  dlg.innerHTML = '<form method="dialog"><button class="d-close">Close</button></form><div class="d-body"><div class="d-cover static"></div><div class="d-text"></div></div>';
  document.body.appendChild(dlg);
  dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
  main.addEventListener('click', (e) => {
    const t = e.target.closest('.tile[data-detail]');
    if (!t || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    const tpl = document.getElementById(t.dataset.detail); if (!tpl) return;
    e.preventDefault();
    const book = document.createElement('span');
    book.className = 'book';
    book.appendChild(t.querySelector('.cover').cloneNode(true));
    dlg.querySelector('.d-cover').replaceChildren(book);
    dlg.querySelector('.d-text').replaceChildren(tpl.content.cloneNode(true));
    dlg.showModal();
    dlg.scrollTop = 0;
  });
})();

/* footer link "AI transparency": opens and closes the folded notice below it */
(() => {
  const link = document.querySelector('.ai-toggle');
  const box = document.getElementById('ai-transparency');
  if (!link || !box) return;
  const isOpen = () => getComputedStyle(box).display !== 'none';
  link.setAttribute('role', 'button');
  link.setAttribute('aria-expanded', String(isOpen()));
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const open = !isOpen();
    box.classList.toggle('open', open);
    box.classList.toggle('shut', !open);
    link.setAttribute('aria-expanded', String(open));
    if (open) box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  });
})();
