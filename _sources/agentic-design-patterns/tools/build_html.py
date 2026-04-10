#!/usr/bin/env python3
"""Build an interactive single-page HTML booklet from chapter markdown sources."""

import os
import re
import glob
import markdown

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "booklet.html")

CSS = """
:root {
    --navy: #1e3a5f;
    --navy-light: #2a5280;
    --accent: #3b82f6;
    --bg: #ffffff;
    --bg-sidebar: #f8fafc;
    --text: #1e293b;
    --text-light: #64748b;
    --border: #e2e8f0;
    --code-bg: #f1f5f9;
    --sidebar-width: 300px;
    --progress-height: 3px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 17px;
    line-height: 1.75;
    color: var(--text);
    background: var(--bg);
}

/* Progress bar */
#progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: var(--progress-height);
    background: var(--accent);
    z-index: 1000;
    transition: width 0.1s;
}

/* Sidebar */
#sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 2rem 0;
    z-index: 100;
    transition: transform 0.3s;
}

#sidebar-header {
    padding: 0 1.5rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

#sidebar-header h2 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

#sidebar-header p {
    font-size: 0.78rem;
    color: var(--text-light);
    margin-top: 0.3rem;
    line-height: 1.4;
}

#sidebar nav ul {
    list-style: none;
    padding: 0;
}

#sidebar nav ul li a {
    display: block;
    padding: 0.55rem 1.5rem;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.85rem;
    color: var(--text-light);
    text-decoration: none;
    border-left: 3px solid transparent;
    transition: all 0.2s;
    line-height: 1.4;
}

#sidebar nav ul li a:hover {
    color: var(--navy);
    background: rgba(30, 58, 95, 0.04);
}

#sidebar nav ul li a.active {
    color: var(--navy);
    font-weight: 600;
    border-left-color: var(--accent);
    background: rgba(59, 130, 246, 0.06);
}

/* Hamburger menu */
#menu-toggle {
    display: none;
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 200;
    background: var(--navy);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 1.2rem;
    cursor: pointer;
}

/* Main content wrapper */
#content-wrapper {
    margin-left: var(--sidebar-width);
    display: flex;
    justify-content: center;
    padding: 0 2rem;
}

/* Main content */
#content {
    max-width: 780px;
    width: 100%;
    padding: 3rem 1rem 6rem;
}

/* Chapter sections */
.chapter {
    margin-bottom: 5rem;
    padding-top: 1rem;
}

.chapter:first-child {
    margin-bottom: 4rem;
    padding-bottom: 2rem;
    border-bottom: 2px solid var(--border);
}

.chapter-number {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* Typography */
h1 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--navy);
    line-height: 1.2;
    margin-bottom: 1.5rem;
}

h2 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--navy);
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    line-height: 1.3;
}

h3 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--navy-light);
    margin-top: 2rem;
    margin-bottom: 0.75rem;
}

p {
    margin-bottom: 1.1rem;
}

/* Lists */
ul, ol {
    margin-bottom: 1.1rem;
    padding-left: 1.8rem;
}

li {
    margin-bottom: 0.4rem;
}

/* Strong / emphasis */
strong { font-weight: 700; }
em { font-style: italic; }

/* Code */
code {
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.88em;
    background: var(--code-bg);
    padding: 0.15em 0.4em;
    border-radius: 4px;
}

pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem;
    overflow-x: auto;
    margin-bottom: 1.5rem;
    font-size: 0.88rem;
    line-height: 1.6;
}

pre code {
    background: none;
    padding: 0;
    border-radius: 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.92rem;
    line-height: 1.5;
}

thead {
    background: var(--navy);
    color: white;
}

th {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-weight: 600;
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

td {
    padding: 0.7rem 1rem;
    border-bottom: 1px solid var(--border);
}

tbody tr:nth-child(even) {
    background: var(--bg-sidebar);
}

tbody tr:hover {
    background: rgba(59, 130, 246, 0.04);
}

/* Blockquotes (used for callouts / key takeaways) */
blockquote {
    border-left: 4px solid var(--accent);
    background: rgba(59, 130, 246, 0.04);
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 0 8px 8px 0;
    font-style: normal;
}

blockquote p:last-child {
    margin-bottom: 0;
}

/* Key points box — screen-sharing friendly summary */
.key-points {
    background: var(--bg-sidebar);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0 2rem;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.92rem;
    line-height: 1.6;
}

.key-points .kp-title {
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--navy);
    margin-bottom: 0.6rem;
}

.key-points ul {
    margin: 0;
    padding-left: 1.4rem;
}

.key-points li {
    margin-bottom: 0.35rem;
    color: var(--text);
}

/* Stat cards — big numbers for screen sharing */
.stat-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.stat-card {
    flex: 1;
    min-width: 140px;
    background: var(--bg-sidebar);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}

.stat-card .stat-number {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--navy);
    line-height: 1.2;
}

.stat-card .stat-label {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.78rem;
    color: var(--text-light);
    margin-top: 0.3rem;
    line-height: 1.3;
}

/* Visual diagrams — simple box-and-arrow layouts */
.visual-diagram {
    background: var(--bg-sidebar);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.88rem;
}

.visual-diagram .diagram-title {
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--navy);
    margin-bottom: 1rem;
    text-align: center;
}

.diagram-stack {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}

.diagram-box {
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    text-align: center;
    width: 80%;
    max-width: 420px;
    font-size: 0.85rem;
    font-weight: 600;
    line-height: 1.3;
}

.diagram-box.layer-1 { background: var(--navy); color: white; }
.diagram-box.layer-2 { background: var(--navy-light); color: white; }
.diagram-box.layer-3 { background: var(--accent); color: white; }
.diagram-box.layer-4 { background: #64748b; color: white; }
.diagram-box.layer-5 { background: #94a3b8; color: white; }

.diagram-box small {
    display: block;
    font-weight: 400;
    font-size: 0.75rem;
    opacity: 0.85;
    margin-top: 0.15rem;
}

.diagram-arrow {
    font-size: 1rem;
    color: var(--text-light);
    line-height: 1;
}

/* Horizontal flow diagram */
.diagram-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.diagram-flow .diagram-box {
    width: auto;
    min-width: 100px;
    padding: 0.6rem 1rem;
}

.diagram-flow .diagram-arrow {
    font-size: 1.2rem;
}

/* Risk cards — color-coded */
.risk-cards {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.risk-card {
    flex: 1;
    min-width: 180px;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Helvetica Neue', Arial, sans-serif;
}

.risk-card.risk-low {
    background: #f0fdf4;
    border: 1px solid #86efac;
}

.risk-card.risk-medium {
    background: #fefce8;
    border: 1px solid #fde047;
}

.risk-card.risk-high {
    background: #fef2f2;
    border: 1px solid #fca5a5;
}

.risk-card .risk-label {
    font-weight: 700;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.4rem;
}

.risk-low .risk-label { color: #166534; }
.risk-medium .risk-label { color: #854d0e; }
.risk-high .risk-label { color: #991b1b; }

.risk-card .risk-desc {
    font-size: 0.82rem;
    color: var(--text);
    line-height: 1.4;
}

/* Swarm topology diagram */
.swarm-diagram {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
}

.swarm-row {
    display: flex;
    gap: 0.8rem;
    justify-content: center;
    flex-wrap: wrap;
}

.swarm-node {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    text-align: center;
    min-width: 100px;
}

.swarm-node.orchestrator { background: var(--navy); color: white; }
.swarm-node.worker { background: var(--accent); color: white; }
.swarm-node.cache { background: #e2e8f0; color: var(--text); border: 1px solid var(--border); }
.swarm-node.user { background: #f0fdf4; color: #166534; border: 1px solid #86efac; }

/* Responsive adjustments for visual elements */
@media (max-width: 600px) {
    .stat-row, .risk-cards { flex-direction: column; }
    .diagram-box { width: 95%; font-size: 0.8rem; }
    .stat-card .stat-number { font-size: 1.4rem; }
    .diagram-flow { flex-direction: column; }
    .diagram-flow .diagram-arrow { transform: rotate(90deg); }
}

/* Horizontal rules (chapter dividers) */
hr {
    border: none;
    border-top: 2px solid var(--border);
    margin: 4rem 0;
}

/* Responsive */
@media (max-width: 900px) {
    #sidebar {
        transform: translateX(-100%);
    }
    #sidebar.open {
        transform: translateX(0);
        box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    }
    #menu-toggle {
        display: block;
    }
    #content-wrapper {
        margin-left: 0;
        padding: 0 1rem;
    }
    #content {
        padding: 2rem 0.5rem 4rem;
    }
    h1 { font-size: 1.7rem; }
    h2 { font-size: 1.3rem; }
    table { font-size: 0.82rem; }
    th, td { padding: 0.5rem 0.6rem; }
}

@media (max-width: 600px) {
    #content { padding: 1.5rem 1rem 3rem; }
    body { font-size: 15.5px; }
}

/* Print */
@media print {
    #sidebar, #menu-toggle, #progress-bar { display: none !important; }
    #content-wrapper { margin-left: 0; padding: 0; }
    #content { max-width: 100%; }
    .chapter { page-break-before: always; }
    .chapter:first-child { page-break-before: auto; }
}
"""

JS = """
document.addEventListener('DOMContentLoaded', function() {
    // Progress bar
    const progressBar = document.getElementById('progress-bar');
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
    });

    // Sidebar navigation highlighting
    const chapters = document.querySelectorAll('.chapter');
    const navLinks = document.querySelectorAll('#sidebar nav a');

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { rootMargin: '-20% 0px -70% 0px' });

    chapters.forEach(function(ch) { observer.observe(ch); });

    // Smooth scrolling
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Close sidebar on mobile
                document.getElementById('sidebar').classList.remove('open');
            }
        });
    });

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });

    // Close sidebar on outside click (mobile)
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 900 &&
            !sidebar.contains(e.target) &&
            e.target !== menuToggle) {
            sidebar.classList.remove('open');
        }
    });

    // Mark first nav item as active
    if (navLinks.length > 0) navLinks[0].classList.add('active');
});
"""


def get_chapter_files():
    return sorted(glob.glob(os.path.join(CHAPTERS_DIR, "*.md")))


def extract_title(content):
    for line in content.strip().split("\n"):
        m = re.match(r"^#\s+(.+)", line)
        if m:
            return m.group(1).strip()
        m = re.match(r"^##\s+(.+)", line)
        if m:
            return m.group(1).strip()
    return None


def make_id(title):
    slug = re.sub(r"[^a-z0-9\s-]", "", title.lower())
    return re.sub(r"\s+", "-", slug).strip("-")


def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "smarty"],
        output_format="html5"
    )


def build():
    files = get_chapter_files()
    chapters = []

    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        title = extract_title(content) or os.path.basename(f).replace(".md", "").replace("_", " ")
        html_content = md_to_html(content)
        ch_id = make_id(title)
        chapters.append((title, ch_id, html_content))

    # Build sidebar nav
    nav_items = []
    for i, (title, ch_id, _) in enumerate(chapters):
        label = title
        if i > 0:
            label = f"{i}. {title}"
        nav_items.append(f'<li><a href="#{ch_id}">{label}</a></li>')

    nav_html = "\n".join(nav_items)

    # Build chapter sections
    sections = []
    for i, (title, ch_id, html_content) in enumerate(chapters):
        ch_num = ""
        if i > 0:
            ch_num = f'<div class="chapter-number">Chapter {i}</div>'
        sections.append(f'''
        <section class="chapter" id="{ch_id}">
            {ch_num}
            {html_content}
        </section>''')

    sections_html = "\n".join(sections)

    # Assemble full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Building Agentic AI — Design Patterns from Production</title>
    <style>{CSS}</style>
</head>
<body>
    <div id="progress-bar"></div>

    <button id="menu-toggle" aria-label="Toggle navigation">&#9776;</button>

    <aside id="sidebar">
        <div id="sidebar-header">
            <h2>Building Agentic AI</h2>
            <p>Design Patterns from Production</p>
        </div>
        <nav>
            <ul>
                {nav_html}
            </ul>
        </nav>
    </aside>

    <div id="content-wrapper">
        <main id="content">
            {sections_html}
        </main>
    </div>

    <script>{JS}</script>
</body>
</html>"""

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"Built: {OUTPUT_FILE}")
    print(f"  Chapters: {len(chapters)}")


if __name__ == "__main__":
    build()
