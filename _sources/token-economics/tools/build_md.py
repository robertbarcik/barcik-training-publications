#!/usr/bin/env python3
"""Build a single concatenated Markdown file from chapter sources."""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "booklet.md")


def get_chapter_files():
    """Get sorted list of chapter markdown files."""
    files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "*.md")))
    return files


def extract_title(content):
    """Extract first H1 or H2 title from markdown content."""
    for line in content.strip().split("\n"):
        match = re.match(r"^#{1,2}\s+(.+)", line)
        if match:
            return match.group(1).strip()
    return None


def generate_toc(chapters):
    """Generate a table of contents with anchor links."""
    toc_lines = ["## Table of Contents\n"]
    for i, (title, _) in enumerate(chapters):
        anchor = re.sub(r"[^a-z0-9\s-]", "", title.lower())
        anchor = re.sub(r"\s+", "-", anchor).strip("-")
        toc_lines.append(f"{i}. [{title}](#{anchor})")
    return "\n".join(toc_lines)


def build():
    """Build the concatenated markdown file."""
    files = get_chapter_files()
    chapters = []

    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        title = extract_title(content) or os.path.basename(f)
        chapters.append((title, content))

    # Build output
    parts = []

    # Frontmatter (first file)
    if chapters:
        parts.append(chapters[0][1])

    # TOC (skip frontmatter in the listing)
    if len(chapters) > 1:
        parts.append("")
        parts.append(generate_toc(chapters[1:]))

    # Chapters
    for title, content in chapters[1:]:
        parts.append("\n\n---\n")
        parts.append(content)

    output = "\n".join(parts)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(output)

    print(f"Built: {OUTPUT_FILE}")
    print(f"  Chapters: {len(chapters)}")
    print(f"  Words: ~{len(output.split())}")


if __name__ == "__main__":
    build()
