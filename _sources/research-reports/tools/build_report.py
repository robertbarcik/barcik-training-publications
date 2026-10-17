#!/usr/bin/env /usr/bin/python3
"""Build one research report page from markdown chapters.

    /usr/bin/python3 _sources/research-reports/tools/build_report.py <slug>

Reads  _sources/research-reports/<slug>/report.json      (title, blurb, output, ...)
       _sources/research-reports/<slug>/chapters/NN_*.md (first file = cover, digits = chapter,
                                                          letters = appendix, mixed = front matter)
       _sources/research-reports/<slug>/references.md    (numbered list -> "Related work")
Writes <output>/index.html next to <output>/figures/*.png (figures are built separately by
       _sources/research-reports/<slug>/figures/build_figures.py).

Derived from _sources/warden/tools/build_html.py (same sidebar / progress bar / callouts), plus:
  <!-- FIG: name | caption -->      numbered <figure class="figure"> with figures/name.png
  <!-- HERO: 98% | caption -->      one big number with a caption (first-screen summary)
  > **Summary** ...                 one-screen summary card (class at-a-glance, Riso-styled)
  > **Classroom notes** ...         teaching aside (class exercise, Riso-styled)
  > **Key takeaways** / **Discussion questions** / **Freshness Watch** as in Warden
  [N] in running text               links to #ref-N in the Related work list
The body stays plain HTML (no external CSS/JS); the Riso head block is injected afterwards by
training-ops/web/riso/riso_reader.py apply, and the AI transparency notice is emitted here.
"""

import glob
import html as htmlmod
import json
import os
import re
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES_ROOT = os.path.dirname(HERE)                               # _sources/research-reports
PUB_ROOT = os.path.dirname(os.path.dirname(SOURCES_ROOT))          # barcik-training-publications

# Same wording as every other barcik.training publication (training-ops/web/ai_transparency_label.py).
AI_TRANSPARENCY_NOTICE = r'''
<!-- AI transparency notice (Art 50 EU AI Act, voluntary) -->
<aside class="ai-transparency" id="ai-transparency" lang="en" aria-label="AI transparency"><svg class="ait-icon" viewBox="85 96 374 374" aria-hidden="true" focusable="false"><defs><mask id="ait-m-c"><rect width="566.93" height="566.93" fill="#000"/><circle cx="272.03" cy="283.47" r="182.75" fill="#fff"/><path fill="#000" d="M170.79,353.74c-1.08,0-2.05-.43-2.92-1.31-.88-.87-1.31-1.84-1.31-2.92,0-.67.07-1.27.2-1.81l47.34-129.32c.4-1.48,1.24-2.79,2.52-3.93,1.27-1.14,3.05-1.71,5.34-1.71h29.81c2.28,0,4.06.57,5.34,1.71,1.27,1.14,2.11,2.45,2.52,3.93l47.14,129.32c.27.54.4,1.14.4,1.81,0,1.08-.44,2.05-1.31,2.92s-1.91,1.31-3.12,1.31h-24.78c-2.01,0-3.52-.5-4.53-1.51-1.01-1.01-1.65-1.91-1.91-2.72l-7.86-20.55h-53.78l-7.65,20.55c-.27.81-.88,1.71-1.81,2.72-.94,1.01-2.55,1.51-4.83,1.51h-24.78ZM218.13,299.96h37.47l-18.93-53.18-18.53,53.18Z"/><path fill="#000" d="M328.11,353.74c-1.48,0-2.69-.47-3.63-1.41-.94-.94-1.41-2.15-1.41-3.63v-130.93c0-1.48.47-2.68,1.41-3.63s2.15-1.41,3.63-1.41h26.99c1.48,0,2.68.47,3.63,1.41.94.94,1.41,2.15,1.41,3.63v130.93c0,1.48-.47,2.69-1.41,3.63-.94.94-2.15,1.41-3.63,1.41h-26.99Z"/></mask></defs><rect width="566.93" height="566.93" fill="currentColor" opacity=".5" mask="url(#ait-m-c)"/></svg><div><span class="ait-label">AI transparency</span><p>This publication was written with generative AI (Anthropic&rsquo;s Claude) working alongside Robert Barcik. The text went through his review, and he holds editorial responsibility for what is published here (LearningDoe s.r.o.). Where the AI writes in its own voice, the piece says so. Disclosed in the spirit of Article&nbsp;50 of the EU AI Act.</p></div></aside>
<style>
.ai-transparency{display:flex;gap:.9rem;align-items:flex-start;margin:3.5rem 0 1.5rem;padding:1.1rem 0 0;border-top:1px solid;border-color:color-mix(in srgb,currentColor 22%,transparent);opacity:.78;font-size:.82rem;line-height:1.55;font-family:inherit;text-align:left}
.ai-transparency .ait-icon{flex:0 0 auto;width:2.1rem;height:2.1rem;margin-top:.1rem}
.ai-transparency .ait-label{display:block;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700;margin-bottom:.3rem}
.ai-transparency p{margin:0;max-width:62ch}
</style>
'''

CSS = """
:root {
    --navy: #1e3a5f; --navy-light: #2a5280; --accent: #3b82f6;
    --bg: #ffffff; --bg-sidebar: #f8fafc; --text: #1e293b; --text-light: #64748b;
    --border: #e2e8f0; --code-bg: #f1f5f9; --sidebar-width: 300px; --progress-height: 3px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Georgia', 'Times New Roman', serif; font-size: 18px; line-height: 1.7; color: var(--text); background: var(--bg); }
#progress-bar { position: fixed; top: 0; left: 0; width: 0%; height: var(--progress-height); background: var(--accent); z-index: 1000; transition: width 0.1s; }
#sidebar { position: fixed; top: 0; left: 0; width: var(--sidebar-width); height: 100vh; background: var(--bg-sidebar); border-right: 1px solid var(--border); overflow-y: auto; padding: 2rem 0; z-index: 100; transition: transform 0.3s; }
#sidebar-header { padding: 0 1.5rem 1.5rem; border-bottom: 1px solid var(--border); margin-bottom: 1rem; }
#sidebar-header .all-pubs-link { display: inline-block; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-light); text-decoration: none; margin-bottom: 0.6rem; }
#sidebar-header .all-pubs-link:hover { color: var(--accent); }
#sidebar-header h2 { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--navy); letter-spacing: 0.02em; text-transform: uppercase; }
#sidebar-header p { font-size: 0.78rem; color: var(--text-light); margin-top: 0.3rem; line-height: 1.4; }
#sidebar nav ul { list-style: none; padding: 0; }
#sidebar nav ul li a { display: block; padding: 0.55rem 1.5rem; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.85rem; color: var(--text-light); text-decoration: none; border-left: 3px solid transparent; transition: all 0.2s; line-height: 1.4; }
#sidebar nav ul li a:hover { color: var(--navy); background: rgba(30, 58, 95, 0.04); }
#sidebar nav ul li a.active { color: var(--navy); font-weight: 600; border-left-color: var(--accent); background: rgba(59, 130, 246, 0.06); }
#menu-toggle { display: none; position: fixed; top: 1rem; left: 1rem; z-index: 200; background: var(--navy); color: white; border: none; border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 1.2rem; cursor: pointer; }
#content-wrapper { margin-left: var(--sidebar-width); display: flex; justify-content: center; padding: 0 2rem; }
#content { max-width: 820px; width: 100%; padding: 3rem 1rem 6rem; }
.chapter { margin-bottom: 5rem; padding-top: 1rem; }
.chapter:first-child { margin-bottom: 4rem; padding-bottom: 2rem; border-bottom: 2px solid var(--border); }
.chapter-number { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.82rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; }
h1 { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 2.3rem; font-weight: 700; color: var(--navy); line-height: 1.2; margin-bottom: 1.5rem; }
h2 { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--navy); margin-top: 2.5rem; margin-bottom: 1rem; line-height: 1.3; }
h3 { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 1.2rem; font-weight: 600; color: var(--navy-light); margin-top: 2rem; margin-bottom: 0.75rem; }
p { margin-bottom: 1.1rem; }
ul, ol { margin-bottom: 1.1rem; padding-left: 1.8rem; }
li { margin-bottom: 0.4rem; }
code { font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 0.88em; background: var(--code-bg); padding: 0.15em 0.4em; border-radius: 4px; }
pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem; overflow-x: auto; margin-bottom: 1.5rem; font-size: 0.85rem; line-height: 1.6; }
pre code { background: none; padding: 0; border-radius: 0; }
table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.9rem; line-height: 1.5; }
thead { background: var(--navy); color: white; }
th { font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 600; padding: 0.7rem 0.9rem; text-align: left; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.03em; }
td { padding: 0.65rem 0.9rem; border-bottom: 1px solid var(--border); vertical-align: top; }
tbody tr:nth-child(even) { background: var(--bg-sidebar); }
.table-wrap { overflow-x: auto; margin: 1.5rem 0; }
.table-wrap table { margin: 0; }
blockquote { border-left: 4px solid var(--accent); background: rgba(59, 130, 246, 0.04); padding: 1rem 1.5rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0; font-style: normal; }
blockquote p:last-child { margin-bottom: 0; }
/* callouts (same class names as the other reports so the Riso family file styles them) */
.freshness-watch, .takeaways, .discussion, .exercise, .at-a-glance { padding: 1rem 1.5rem; margin: 2rem 0 1rem; border-radius: 0 8px 8px 0; font-size: 0.97rem; border-left: 4px solid var(--accent); background: rgba(59,130,246,0.05); }
.freshness-watch { border-left-color: #d97706; background: rgba(217,119,6,0.06); }
.takeaways { border-left-color: #059669; background: rgba(5,150,105,0.06); }
.discussion { border-left-color: #7c3aed; background: rgba(124,58,237,0.05); }
.exercise { border-left-color: #059669; background: rgba(5,150,105,0.05); }
.at-a-glance { border-left-color: var(--navy); background: rgba(30,58,95,0.05); font-size: 1.05rem; padding: 1.4rem 1.8rem; margin: 1.5rem 0 2rem; }
.at-a-glance ul { margin-bottom: 0; }
.at-a-glance li { margin-bottom: 0.6rem; }
:is(.freshness-watch, .takeaways, .discussion, .exercise, .at-a-glance) > p:first-child { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.6rem; color: var(--navy); }
:is(.freshness-watch, .takeaways, .discussion, .exercise, .at-a-glance) > :last-child { margin-bottom: 0; }
/* hero number */
.hero { display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; margin: 1.2rem 0 1.6rem; font-family: 'Helvetica Neue', Arial, sans-serif; }
.hero-num { font-size: 3.6rem; font-weight: 800; line-height: 1; color: var(--navy); letter-spacing: -0.02em; }
.hero-cap { font-size: 1.05rem; color: var(--text-light); max-width: 30ch; line-height: 1.35; }
/* figures */
.figure { margin: 2rem 0 2.4rem; }
.figure img { display: block; width: 100%; height: auto; border: 1px solid var(--border); border-radius: 6px; }
.figure figcaption { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.92rem; color: var(--text-light); margin-top: 0.7rem; line-height: 1.45; }
.figure figcaption strong { color: var(--navy); }
/* citations and references */
a.cite { text-decoration: none; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 0.8em; vertical-align: super; line-height: 0; color: var(--accent); }
ol.refs { padding-left: 1.6rem; font-size: 0.95rem; }
ol.refs li { margin-bottom: 0.7rem; }
ol.refs li:target { background: rgba(59,130,246,0.1); }
ol.refs a { word-break: break-all; }
.model-table td:first-child { font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 600; }
hr { border: none; border-top: 2px solid var(--border); margin: 4rem 0; }
@media (max-width: 900px) {
    #sidebar { transform: translateX(-100%); }
    #sidebar.open { transform: translateX(0); box-shadow: 4px 0 20px rgba(0,0,0,0.15); }
    #menu-toggle { display: block; }
    #content-wrapper { margin-left: 0; padding: 0 1rem; }
    #content { padding: 2rem 0.5rem 4rem; }
    h1 { font-size: 1.7rem; } h2 { font-size: 1.3rem; }
    table { font-size: 0.82rem; } th, td { padding: 0.5rem 0.6rem; }
    .hero-num { font-size: 2.6rem; }
}
@media (max-width: 600px) { #content { padding: 1.5rem 1rem 3rem; } body { font-size: 16px; } }
@media print { #sidebar, #menu-toggle, #progress-bar { display: none !important; } #content-wrapper { margin-left: 0; padding: 0; } #content { max-width: 100%; } .chapter { page-break-before: always; } .chapter:first-child { page-break-before: auto; } }
"""

JS = """
document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.getElementById('progress-bar');
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        progressBar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
    });
    const chapters = document.querySelectorAll('.chapter');
    const navLinks = document.querySelectorAll('#sidebar nav a');
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) link.classList.add('active');
                });
            }
        });
    }, { rootMargin: '-20% 0px -70% 0px' });
    chapters.forEach(function(ch) { observer.observe(ch); });
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); document.getElementById('sidebar').classList.remove('open'); }
        });
    });
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    menuToggle.addEventListener('click', function() { sidebar.classList.toggle('open'); });
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 900 && !sidebar.contains(e.target) && e.target !== menuToggle) sidebar.classList.remove('open');
    });
    if (navLinks.length > 0) navLinks[0].classList.add('active');
});
"""

CALLOUTS = [
    (r"Summary", "at-a-glance", "Summary"),
    (r"Classroom notes", "exercise", "Classroom notes"),
    (r"Key takeaways", "takeaways", "Key takeaways"),
    (r"Discussion questions?", "discussion", "Discussion questions"),
    (r"Freshness Watch", "freshness-watch", "Freshness Watch"),
]
FIG_RE = re.compile(r'<!--\s*FIG:\s*([A-Za-z0-9_\-]+)\s*\|\s*(.*?)\s*-->', re.DOTALL)
HERO_RE = re.compile(r'<!--\s*HERO:\s*(.*?)\s*\|\s*(.*?)\s*-->', re.DOTALL)
CITE_RE = re.compile(r'\[(\d{1,2})\]')


def extract_title(content):
    for line in content.strip().split("\n"):
        m = re.match(r"^#{1,2}\s+(.+)", line)
        if m:
            return m.group(1).strip()
    return None


def make_id(title):
    slug = re.sub(r"[^a-z0-9\s-]", "", title.lower())
    return re.sub(r"\s+", "-", slug).strip("-")


def transform_callouts(html):
    for label_re, cls, label in CALLOUTS:
        pat = re.compile(r'<blockquote>\s*<p><strong>' + label_re + r'</strong>(.*?)</blockquote>', re.DOTALL)
        html = pat.sub(lambda m, cls=cls, label=label: f'<aside class="{cls}"><p><strong>{label}</strong>{m.group(1)}</aside>', html)
    return html


def wrap_tables(html):
    return re.sub(r'(<table>.*?</table>)', r'<div class="table-wrap">\1</div>', html, flags=re.DOTALL)


def render_figures(html, state, fig_dir_rel="figures"):
    def _fig(m):
        state["fig"] += 1
        n = state["fig"]
        name, caption = m.group(1), m.group(2)
        cap_html = markdown.markdown(caption, extensions=["smarty"], output_format="html5")
        cap_html = re.sub(r'^<p>(.*)</p>$', r'\1', cap_html.strip(), flags=re.DOTALL)
        return (f'<figure class="figure" id="fig-{n}"><img src="{fig_dir_rel}/{name}.png" '
                f'alt="Figure {n}: {htmlmod.escape(re.sub(r"<[^>]+>", "", cap_html))}" loading="lazy">'
                f'<figcaption><strong>Figure {n}.</strong> {cap_html}</figcaption></figure>')
    html = FIG_RE.sub(_fig, html)
    html = HERO_RE.sub(lambda m: f'<div class="hero"><span class="hero-num">{m.group(1)}</span>'
                                 f'<span class="hero-cap">{m.group(2)}</span></div>', html)
    # markdown wraps a lone HTML comment in <p>...</p>; drop the empty paragraphs it leaves
    html = re.sub(r'<p>\s*(<figure .*?</figure>)\s*</p>', r'\1', html, flags=re.DOTALL)
    html = re.sub(r'<p>\s*(<div class="hero">.*?</div>)\s*</p>', r'\1', html, flags=re.DOTALL)
    return html


def link_citations(html, max_ref):
    """[N] -> <a class="cite" href="#ref-N">[N]</a>, outside <code>/<pre>/<a> and the refs list."""
    parts = re.split(r'(<pre>.*?</pre>|<code>.*?</code>|<a [^>]*>.*?</a>)', html, flags=re.DOTALL)
    out = []
    for p in parts:
        if p.startswith(("<pre>", "<code>", "<a ")):
            out.append(p)
        else:
            out.append(CITE_RE.sub(lambda m: (f'<a class="cite" href="#ref-{m.group(1)}">[{m.group(1)}]</a>'
                                              if int(m.group(1)) <= max_ref else m.group(0)), p))
    return "".join(out)


def md_to_html(text):
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "smarty"], output_format="html5")
    return wrap_tables(transform_callouts(html))


def build(slug):
    src = os.path.join(SOURCES_ROOT, slug)
    with open(os.path.join(src, "report.json"), encoding="utf-8") as fh:
        cfg = json.load(fh)
    out_dir = os.path.join(PUB_ROOT, cfg["output"])
    out_file = os.path.join(out_dir, "index.html")
    files = sorted(glob.glob(os.path.join(src, "chapters", "*.md")))
    if not files:
        sys.exit(f"no chapters in {src}/chapters")

    # references -> numbered list with ids
    refs_html, n_refs, refs_title = "", 0, "Related work"
    ref_path = os.path.join(src, "references.md")
    if os.path.exists(ref_path):
        with open(ref_path, encoding="utf-8") as fh:
            ref_md = fh.read().strip()
        refs_title = extract_title(ref_md) or refs_title
        body = re.sub(r"^#{1,2}\s+.+\n", "", ref_md, count=1)
        refs_html = markdown.markdown(body, extensions=["smarty"], output_format="html5")
        items = re.findall(r"<li>", refs_html)
        n_refs = len(items)
        counter = {"n": 0}
        def _li(m):
            counter["n"] += 1
            return f'<li id="ref-{counter["n"]}">'
        refs_html = re.sub(r"<li>", _li, refs_html)
        refs_html = re.sub(r"<ol>", '<ol class="refs">', refs_html, count=1)
        if n_refs == 0:
            print("WARNING: references.md has no list items")

    state = {"fig": 0}
    chapters = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            content = fh.read().strip()
        title = extract_title(content) or os.path.basename(f)[:-3].replace("_", " ")
        html = md_to_html(content)
        html = render_figures(html, state)
        html = link_citations(html, n_refs)
        chapters.append((title, make_id(title), html))

    kinds, chapter_n = [], 0
    for i, f in enumerate(files):
        prefix = os.path.basename(f).split("_", 1)[0]
        if i == 0:
            kinds.append(("cover", None))
        elif prefix.isdigit():
            chapter_n += 1
            kinds.append(("chapter", chapter_n))
        elif prefix.isalpha():
            kinds.append(("appendix", prefix))
        else:
            kinds.append(("frontmatter", None))
    if refs_html:
        chapters.append((refs_title, make_id(refs_title), f"<h1>{htmlmod.escape(refs_title)}</h1>{refs_html}"))
        kinds.append(("frontmatter", None))

    nav, sections = [], []
    for (kind, marker), (title, ch_id, html) in zip(kinds, chapters):
        if kind in ("cover", "frontmatter"):
            label, num = title, ""
        elif kind == "chapter":
            label, num = f"{marker}. {title}", f'<div class="chapter-number">Chapter {marker}</div>'
        else:
            label, num = f"Appendix {marker} — {title}", f'<div class="chapter-number">Appendix {marker}</div>'
        nav.append(f'<li><a href="#{ch_id}">{htmlmod.escape(label)}</a></li>')
        sections.append(f'\n        <section class="chapter" id="{ch_id}">\n            {num}\n            {html}\n        </section>')

    title = cfg["title"]
    desc = cfg.get("description", "")
    canonical = cfg.get("canonical", "")
    head_meta = f'''    <meta name="description" content="{htmlmod.escape(desc)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{htmlmod.escape(title)}">
    <meta property="og:description" content="{htmlmod.escape(desc)}">
    <meta property="og:url" content="{canonical}">''' if canonical else ""

    page = f"""<!DOCTYPE html>
<html lang="{cfg.get('lang', 'en')}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{htmlmod.escape(title)}</title>
{head_meta}
    <style>{CSS}</style>
</head>
<body>
    <div id="progress-bar"></div>
    <button id="menu-toggle" aria-label="Toggle navigation">&#9776;</button>

    <aside id="sidebar">
        <div id="sidebar-header">
            <a class="all-pubs-link" href="/">&larr; All Publications</a>
            <h2>{htmlmod.escape(cfg.get('short_title', title))}</h2>
            <p>{cfg.get('blurb', '')}</p>
        </div>
        <nav>
            <ul>
                {chr(10).join(nav)}
            </ul>
        </nav>
    </aside>

    <div id="content-wrapper">
        <main id="content">
            {''.join(sections)}
        {AI_TRANSPARENCY_NOTICE}
        </main>
    </div>

    <script>{JS}</script>
</body>
</html>"""

    os.makedirs(out_dir, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write(page)
    missing = [m.group(1) for m in FIG_RE.finditer("\n".join(open(f, encoding='utf-8').read() for f in files))
               if not os.path.exists(os.path.join(out_dir, "figures", m.group(1) + ".png"))]
    print(f"Built {out_file}: {len(files)} chapter files, {state['fig']} figures, {n_refs} references, "
          f"{os.path.getsize(out_file) // 1024} KB")
    if missing:
        print("WARNING: missing figure PNGs:", ", ".join(missing))
    unresolved = sorted(set(int(n) for n in CITE_RE.findall(" ".join(h for _, _, h in chapters[:-1 if refs_html else None])) if int(n) > n_refs))
    if unresolved:
        print("WARNING: citations beyond the reference list:", unresolved)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
