#!/usr/bin/env python3
"""
build_html.py — Convert extracted EPUB of "The Mirror of Artificial Intelligence"
into a single-page interactive HTML file.

Reads from:  /tmp/epub-extract/OEBPS/
Writes to:   <repo>/_sources/mirror-of-ai/output/mirror.html

Usage:
    python build_html.py
"""

import base64
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
EPUB_ROOT = Path("/tmp/epub-extract/OEBPS")
TEXT_DIR = EPUB_ROOT / "Text"
IMAGES_DIR = EPUB_ROOT / "Images"
TOC_NCX = EPUB_ROOT / "toc.ncx"
CONTENT_OPF = EPUB_ROOT / "content.opf"

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "mirror.html"

# ---------------------------------------------------------------------------
# Spine order (from content.opf) — the canonical reading order
# ---------------------------------------------------------------------------

def get_spine_order() -> list[str]:
    """Return list of xhtml filenames in spine order from content.opf."""
    tree = ET.parse(CONTENT_OPF)
    root = tree.getroot()
    ns = {"opf": "http://www.idpf.org/2007/opf"}

    # Build idref -> href map from manifest
    id_to_href = {}
    for item in root.findall(".//opf:manifest/opf:item", ns):
        id_to_href[item.get("id")] = item.get("href")

    spine_files = []
    for itemref in root.findall(".//opf:spine/opf:itemref", ns):
        idref = itemref.get("idref")
        href = id_to_href.get(idref, "")
        if href.startswith("Text/"):
            spine_files.append(href.replace("Text/", ""))
        else:
            spine_files.append(href)
    return spine_files


# ---------------------------------------------------------------------------
# TOC parsing
# ---------------------------------------------------------------------------

def parse_toc() -> list[dict]:
    """Parse toc.ncx and return ordered list of {title, src_file} dicts."""
    tree = ET.parse(TOC_NCX)
    root = tree.getroot()
    ns = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}

    chapters = []
    for nav in root.findall(".//ncx:navMap/ncx:navPoint", ns):
        label_el = nav.find("ncx:navLabel/ncx:text", ns)
        content_el = nav.find("ncx:content", ns)
        if label_el is not None and content_el is not None:
            title = label_el.text.strip()
            src = content_el.get("src", "")
            # Strip Text/ prefix and fragment
            src_file = src.replace("Text/", "").split("#")[0]
            chapters.append({"title": title, "src_file": src_file})
    return chapters


# ---------------------------------------------------------------------------
# Image encoding
# ---------------------------------------------------------------------------

_image_cache: dict[str, str] = {}


def image_to_data_uri(image_name: str) -> str:
    """Convert an image file to a base64 data URI, with caching."""
    if image_name in _image_cache:
        return _image_cache[image_name]

    image_path = IMAGES_DIR / image_name
    if not image_path.exists():
        return ""

    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")

    uri = f"data:image/jpeg;base64,{data}"
    _image_cache[image_name] = uri
    return uri


# ---------------------------------------------------------------------------
# XHTML body extraction
# ---------------------------------------------------------------------------

def extract_body_html(xhtml_path: Path) -> str:
    """Read an XHTML file and return the inner HTML of the <body> tag."""
    with open(xhtml_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract body content
    body_match = re.search(r"<body[^>]*>(.*?)</body>", content, re.DOTALL)
    if not body_match:
        return ""

    body_html = body_match.group(1).strip()

    # Convert image references to data URIs
    def replace_image(m):
        img_name = m.group(1)
        data_uri = image_to_data_uri(img_name)
        if data_uri:
            return f'src="{data_uri}"'
        return m.group(0)

    body_html = re.sub(r'src="\.\./Images/([^"]+)"', replace_image, body_html)

    # Convert internal cross-reference links to footnote anchors within the page
    # e.g. href="../Text/Section0001_0089.xhtml#footnote-012" -> href="#footnote-012"
    body_html = re.sub(
        r'href="\.\./Text/[^"]*#([^"]+)"',
        r'href="#\1"',
        body_html,
    )

    return body_html


# ---------------------------------------------------------------------------
# Assign XHTML files to chapters
# ---------------------------------------------------------------------------

def build_chapter_content(chapters: list[dict], spine: list[str]) -> list[dict]:
    """
    For each TOC chapter, collect its primary XHTML file plus any
    'in-between' files (separator/image pages) that appear in the spine
    before the next TOC entry. Returns enriched chapter dicts with 'html' key.
    """
    # Build a set of TOC source files for quick lookup
    toc_files = {ch["src_file"] for ch in chapters}

    # Build map: toc_file -> list of spine files that belong to it
    # (the toc file itself + any files between it and the next toc entry)
    toc_file_to_group: dict[str, list[str]] = {}
    current_toc_file = None

    for spine_file in spine:
        if spine_file in toc_files:
            current_toc_file = spine_file
            toc_file_to_group.setdefault(current_toc_file, [])
            toc_file_to_group[current_toc_file].append(spine_file)
        elif current_toc_file is not None:
            toc_file_to_group[current_toc_file].append(spine_file)

    # Build HTML for each chapter
    enriched = []
    for ch in chapters:
        files = toc_file_to_group.get(ch["src_file"], [ch["src_file"]])
        html_parts = []
        for f in files:
            fpath = TEXT_DIR / f
            if fpath.exists():
                html_parts.append(extract_body_html(fpath))
        ch["html"] = "\n".join(html_parts)
        enriched.append(ch)

    return enriched


# ---------------------------------------------------------------------------
# Slug generation
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    """Create a URL-friendly slug from a chapter title."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "chapter"


# ---------------------------------------------------------------------------
# Determine chapter type for sidebar styling
# ---------------------------------------------------------------------------

def chapter_type(title: str) -> str:
    """Classify a chapter as 'story', 'essay', or 'other' for styling."""
    stripped = title.strip()
    if re.match(r"^\d+\.", stripped):
        return "story"
    if re.match(r"^[A-I]\.", stripped):
        return "essay"
    return "other"


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

def build_html(chapters: list[dict], cover_data_uri: str) -> str:
    """Assemble the final single-page HTML."""

    # Skip cover.xhtml and title.xhtml from content (we use cover image directly)
    skip_files = {"cover.xhtml", "title.xhtml"}
    visible_chapters = [ch for ch in chapters if ch["src_file"] not in skip_files]

    # Build sidebar nav and content sections
    nav_items = []
    content_sections = []

    for i, ch in enumerate(visible_chapters):
        slug = slugify(ch["title"]) or f"ch-{i}"
        ctype = chapter_type(ch["title"])
        css_class = f"nav-item nav-{ctype}"

        # Shorter nav labels for sidebar
        nav_title = ch["title"]

        nav_items.append(
            f'        <a href="#{slug}" class="{css_class}" data-index="{i}">'
            f'{nav_title}</a>'
        )

        content_sections.append(
            f'    <section id="{slug}" class="chapter chapter-{ctype}" '
            f'data-index="{i}">\n'
            f'      {ch["html"]}\n'
            f"    </section>"
        )

    nav_html = "\n".join(nav_items)
    content_html = "\n\n".join(content_sections)
    total_chapters = len(visible_chapters)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Mirror of Artificial Intelligence &mdash; R&oacute;bert Barc&iacute;k</title>
<style>
/* ===================================================================
   The Mirror of AI — Single-page book reader
   Warm, bookish palette for a collection of stories and essays
   =================================================================== */

:root {{
  --color-bg:            #faf7f2;
  --color-bg-warm:       #f5f0e8;
  --color-text:          #2c2416;
  --color-text-light:    #6b5d4f;
  --color-heading:       #3d2b1f;
  --color-accent:        #b8860b;
  --color-accent-light:  #d4a84b;
  --color-accent-faint:  #f0e6d0;
  --color-sidebar-bg:    #2c2116;
  --color-sidebar-text:  #d4cfc7;
  --color-sidebar-hover: #3d2b1f;
  --color-sidebar-active:#b8860b;
  --color-divider:       #d5cec3;
  --color-essay-accent:  #8b6914;
  --sidebar-width:       300px;
  --progress-height:     3px;
}}

*, *::before, *::after {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

html {{
  scroll-behavior: smooth;
  scroll-padding-top: 80px;
  font-size: 18px;
}}

body {{
  font-family: Georgia, "Times New Roman", "Noto Serif", serif;
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}}

/* ----- Progress bar ----- */
.progress-bar {{
  position: fixed;
  top: 0;
  left: 0;
  width: 0%;
  height: var(--progress-height);
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-light));
  z-index: 1000;
  transition: width 0.15s ease-out;
}}

/* ----- Sidebar ----- */
.sidebar {{
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--color-sidebar-bg);
  overflow-y: auto;
  z-index: 900;
  padding: 0;
  transition: transform 0.3s ease;
  scrollbar-width: thin;
  scrollbar-color: rgba(184,134,11,0.3) transparent;
}}

.sidebar::-webkit-scrollbar {{
  width: 5px;
}}
.sidebar::-webkit-scrollbar-thumb {{
  background: rgba(184,134,11,0.3);
  border-radius: 3px;
}}

.sidebar-header {{
  padding: 1.5rem 1.25rem 1rem;
  border-bottom: 1px solid rgba(184,134,11,0.2);
}}

.sidebar-header h2 {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin: 0;
  line-height: 1.3;
}}

.sidebar-header .author {{
  font-size: 0.7rem;
  color: var(--color-sidebar-text);
  opacity: 0.6;
  margin-top: 0.3rem;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  letter-spacing: 0.04em;
}}

.sidebar-nav {{
  padding: 0.75rem 0 2rem;
}}

.nav-item {{
  display: block;
  padding: 0.45rem 1.25rem;
  font-size: 0.78rem;
  line-height: 1.45;
  color: var(--color-sidebar-text);
  text-decoration: none;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}}

.nav-item:hover {{
  background: rgba(255,255,255,0.05);
  color: #fff;
}}

.nav-item.active {{
  color: var(--color-sidebar-active);
  border-left-color: var(--color-sidebar-active);
  background: rgba(184,134,11,0.08);
  font-weight: 600;
}}

.nav-essay {{
  color: rgba(212,207,199,0.7);
  font-style: italic;
}}

.nav-other {{
  color: rgba(212,207,199,0.5);
  font-size: 0.72rem;
}}

/* ----- Hamburger (mobile) ----- */
.hamburger {{
  display: none;
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 950;
  width: 44px;
  height: 44px;
  background: var(--color-sidebar-bg);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}

.hamburger span {{
  display: block;
  width: 22px;
  height: 2px;
  background: var(--color-accent);
  border-radius: 2px;
  transition: all 0.3s ease;
}}

.hamburger.active span:nth-child(1) {{
  transform: rotate(45deg) translate(5px, 5px);
}}
.hamburger.active span:nth-child(2) {{
  opacity: 0;
}}
.hamburger.active span:nth-child(3) {{
  transform: rotate(-45deg) translate(5px, -5px);
}}

.overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 850;
}}

/* ----- Content wrapper (centers the reading column) ----- */
.content-wrapper {{
  margin-left: var(--sidebar-width);
  display: flex;
  justify-content: center;
  padding: 0 2rem;
}}

/* ----- Main content area ----- */
.main-content {{
  max-width: 750px;
  width: 100%;
  padding: 2rem 1rem 4rem;
}}

/* ----- Cover ----- */
.cover-section {{
  text-align: center;
  padding: 2rem 0 3rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-divider);
}}

.cover-section img {{
  max-width: 380px;
  width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 8px 32px rgba(44,36,22,0.25), 0 2px 8px rgba(44,36,22,0.15);
}}

.cover-section h1 {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-top: 1.5rem;
  letter-spacing: -0.02em;
  line-height: 1.2;
}}

.cover-section .cover-author {{
  font-size: 1rem;
  color: var(--color-text-light);
  margin-top: 0.5rem;
  font-style: italic;
}}

/* ----- Chapter sections ----- */
.chapter {{
  padding: 2.5rem 0 2rem;
  border-bottom: 1px solid var(--color-divider);
}}

.chapter:last-child {{
  border-bottom: none;
}}

/* Chapter heading (kap) */
.chapter h1.kap,
.chapter h1[class*="kap"] {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-heading);
  text-align: center;
  margin: 0 0 1.8rem;
  line-height: 1.25;
  letter-spacing: -0.01em;
}}

/* Essay chapters get a subtle background */
.chapter-essay {{
  background: var(--color-bg-warm);
  margin-left: -2.5rem;
  margin-right: -2.5rem;
  padding-left: 2.5rem;
  padding-right: 2.5rem;
  border-radius: 0;
}}

.chapter-essay h1.kap,
.chapter-essay h1[class*="kap"] {{
  color: var(--color-essay-accent);
}}

/* ---- Typography ---- */
p.nrmltxt,
.chapter p.nrmltxt {{
  text-align: justify;
  text-indent: 1.5em;
  margin-bottom: 0.3rem;
  hyphens: auto;
  -webkit-hyphens: auto;
}}

/* First paragraph after heading — no indent */
h1 + p.nrmltxt,
h1.kap + p.nrmltxt {{
  text-indent: 0;
}}

.chapter p.nrmltxt:first-of-type {{
  text-indent: 0;
}}

span.kurziva,
span[class*="kurziva"] {{
  font-style: italic;
}}

span.bold,
span[class*="bold"] {{
  font-weight: 700;
}}

span.bold-kurziva {{
  font-weight: 700;
  font-style: italic;
}}

p.text-skraja,
.chapter p.text-skraja {{
  font-size: 0.82rem;
  color: var(--color-text-light);
  line-height: 1.6;
  margin-bottom: 0.15rem;
  text-indent: 0;
}}

p.Podnadpis,
.chapter p.Podnadpis {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-text-light);
  text-align: center;
  margin: 2rem 0 1rem;
  text-indent: 0;
}}

p.volny-riadok,
.chapter p.volny-riadok {{
  height: 0.8rem;
  margin: 0;
  text-indent: 0;
}}

p.text-na-stred,
.chapter p.text-na-stred {{
  text-align: center;
  text-indent: 0;
  margin: 1rem 0;
}}

span.super,
span.CharOverride-2 {{
  font-size: 0.7em;
  vertical-align: super;
  line-height: 0;
}}

/* Lists */
.chapter ol, .chapter ul {{
  margin: 0.8rem 0 0.8rem 2rem;
  padding: 0;
}}

.chapter li {{
  margin-bottom: 0.3rem;
  line-height: 1.6;
  padding-left: 0.3rem;
}}

.chapter li[class*="ParaOverride"] {{
  margin-bottom: 0.3rem;
}}

/* Images */
.chapter img,
.chapter p.logo img {{
  display: block;
  max-width: 100%;
  height: auto;
  margin: 1.5rem auto;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(44,36,22,0.12);
}}

.chapter p.logo {{
  text-align: center;
  text-indent: 0 !important;
}}

/* Title page styling */
.chapter h2 {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1rem;
  font-weight: 400;
  color: var(--color-text-light);
  text-align: center;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}}

.chapter h1.sigil_not_in_toc {{
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-heading);
  text-align: center;
  line-height: 1.2;
  margin-bottom: 1rem;
}}

/* Links */
.chapter a {{
  color: var(--color-accent);
  text-decoration: none;
  border-bottom: 1px solid rgba(184,134,11,0.3);
  transition: border-color 0.2s;
}}

.chapter a:hover {{
  border-bottom-color: var(--color-accent);
}}

/* Footnotes */
._idFootnotes {{
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-divider);
}}

._idFootnote {{
  margin-bottom: 0.75rem;
}}

._idFootnote p {{
  font-size: 0.82rem;
  color: var(--color-text-light);
  line-height: 1.6;
  text-indent: 0;
}}

._idFootnoteAnchor {{
  font-weight: 700;
  color: var(--color-accent);
  margin-right: 0.3em;
}}

/* Superscript footnote links */
a._idFootnoteLink {{
  font-size: 0.7em;
  vertical-align: super;
  line-height: 0;
  border-bottom: none;
}}

/* Padding class from title page */
p.padding-top {{
  height: 1.5rem;
  text-indent: 0;
}}

/* ===================================================================
   Responsive
   =================================================================== */

@media (max-width: 960px) {{
  .sidebar {{
    transform: translateX(-100%);
  }}
  .sidebar.open {{
    transform: translateX(0);
  }}
  .hamburger {{
    display: flex;
  }}
  .overlay.active {{
    display: block;
  }}
  .content-wrapper {{
    margin-left: 0;
    padding: 0 1rem;
  }}
  .main-content {{
    padding: 3.5rem 0.5rem 3rem;
  }}
  .chapter-essay {{
    margin-left: -1.5rem;
    margin-right: -1.5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }}
  html {{
    font-size: 17px;
  }}
}}

@media (max-width: 600px) {{
  .main-content {{
    padding: 3.5rem 0.5rem 2rem;
  }}
  .chapter-essay {{
    margin-left: -1rem;
    margin-right: -1rem;
    padding-left: 1rem;
    padding-right: 1rem;
  }}
  html {{
    font-size: 16px;
  }}
  .cover-section img {{
    max-width: 280px;
  }}
  .cover-section h1 {{
    font-size: 1.5rem;
  }}
  .chapter h1.kap,
  .chapter h1[class*="kap"] {{
    font-size: 1.4rem;
  }}
}}

/* Print */
@media print {{
  .sidebar, .hamburger, .progress-bar, .overlay {{
    display: none !important;
  }}
  .content-wrapper {{
    margin-left: 0;
    padding: 0;
  }}
  .main-content {{
    max-width: 100%;
  }}
}}
</style>
</head>
<body>

<!-- Progress bar -->
<div class="progress-bar" id="progressBar"></div>

<!-- Hamburger -->
<button class="hamburger" id="hamburger" aria-label="Toggle navigation">
  <span></span><span></span><span></span>
</button>

<!-- Overlay -->
<div class="overlay" id="overlay"></div>

<!-- Sidebar -->
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <h2>The Mirror of<br>Artificial Intelligence</h2>
    <div class="author">R&oacute;bert Barc&iacute;k</div>
  </div>
  <div class="sidebar-nav" id="sidebarNav">
{nav_html}
  </div>
</nav>

<!-- Main content -->
<div class="content-wrapper">
<main class="main-content" id="mainContent">

  <!-- Cover -->
  <div class="cover-section">
    <img src="{cover_data_uri}" alt="The Mirror of Artificial Intelligence — Book Cover">
    <h1>The Mirror of Artificial Intelligence</h1>
    <div class="cover-author">R&oacute;bert Barc&iacute;k &amp; ChatGPT</div>
  </div>

{content_html}

</main>
</div>

<script>
(function() {{
  // ---- Elements ----
  const sidebar    = document.getElementById("sidebar");
  const hamburger  = document.getElementById("hamburger");
  const overlay    = document.getElementById("overlay");
  const progressBar= document.getElementById("progressBar");
  const navLinks   = document.querySelectorAll(".nav-item");
  const sections   = document.querySelectorAll(".chapter");

  // ---- Hamburger toggle ----
  function toggleSidebar() {{
    sidebar.classList.toggle("open");
    hamburger.classList.toggle("active");
    overlay.classList.toggle("active");
  }}

  hamburger.addEventListener("click", toggleSidebar);
  overlay.addEventListener("click", toggleSidebar);

  // Close sidebar on nav click (mobile)
  navLinks.forEach(link => {{
    link.addEventListener("click", () => {{
      if (window.innerWidth <= 960) {{
        sidebar.classList.remove("open");
        hamburger.classList.remove("active");
        overlay.classList.remove("active");
      }}
    }});
  }});

  // ---- Progress bar ----
  function updateProgress() {{
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = progress + "%";
  }}

  // ---- Active nav tracking ----
  function updateActiveNav() {{
    let currentIndex = 0;
    const scrollPos = window.scrollY + 120;

    sections.forEach((section, i) => {{
      if (section.offsetTop <= scrollPos) {{
        currentIndex = i;
      }}
    }});

    navLinks.forEach(link => link.classList.remove("active"));
    if (navLinks[currentIndex]) {{
      navLinks[currentIndex].classList.add("active");
      // Scroll the active nav item into view in sidebar
      navLinks[currentIndex].scrollIntoView({{
        block: "nearest",
        behavior: "smooth"
      }});
    }}
  }}

  // ---- Scroll handler (throttled) ----
  let ticking = false;
  window.addEventListener("scroll", () => {{
    if (!ticking) {{
      requestAnimationFrame(() => {{
        updateProgress();
        updateActiveNav();
        ticking = false;
      }});
      ticking = true;
    }}
  }});

  // Initial state
  updateProgress();
  updateActiveNav();
}})();
</script>

</body>
</html>'''


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Parsing TOC...")
    chapters = parse_toc()
    print(f"  Found {len(chapters)} TOC entries")

    print("Reading spine order...")
    spine = get_spine_order()
    print(f"  Spine has {len(spine)} files")

    print("Building chapter content (extracting XHTML, encoding images)...")
    chapters = build_chapter_content(chapters, spine)

    print("Encoding cover image...")
    cover_uri = image_to_data_uri("bookcover.jpg")

    print("Assembling HTML...")
    html = build_html(chapters, cover_uri)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\nDone! Written to: {OUTPUT_FILE}")
    print(f"  File size: {size_mb:.1f} MB")
    print(f"  Chapters: {len(chapters)}")
    print(f"  Images embedded: {len(_image_cache)}")


if __name__ == "__main__":
    main()
