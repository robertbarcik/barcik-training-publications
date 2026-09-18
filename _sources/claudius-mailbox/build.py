#!/usr/bin/env python3
"""Build /claudius-mailbox/index.html (EN) from body_en.html.

The page is the third sibling of claude-code-setup and field-notes-ai-colleague and shares
their design, so this script reuses the head (CSS) and the closing scripts of
claude-code-setup/index.html, swaps the metadata, inserts body_en.html and adds the
AI-transparency colophon from training-ops. Run from anywhere:

    python3 _sources/claudius-mailbox/build.py

The Slovak edition is then assembled the usual way (see build_all_sk.sh):
    python3 _sources/_translation/assemble_sk.py claudius-mailbox --title ... (etc.)
"""
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TEMPLATE = os.path.join(ROOT, "claude-code-setup", "index.html")
LABEL_PY = os.path.join(os.path.dirname(ROOT), "training-ops", "web", "ai_transparency_label.py")

SLUG = "claudius-mailbox"
TITLE = "An AI Assistant with Its Own Mailbox"
DESCRIPTION = ("An early prototype, explained simply: Robert Barcik's AI assistant got its own, "
               "openly labelled email address. How a letter reaches it, how an answer leaves, "
               "the five security rules, and why we do not hide an AI behind a human name.")
OG_DESCRIPTION = ("Robert Barcik's AI assistant got its own, openly labelled email address. "
                  "How it works, the security rules, and why we do not hide it.")


def sub_once(pattern, repl, text):
    out, n = re.subn(pattern, lambda m: repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"template changed: no match for {pattern}")
    return out


def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    head, rest = tpl.split("<body>", 1)
    tail = rest[rest.rfind("<script"):]

    head = head.replace("/claude-code-setup-sk/", f"/{SLUG}-sk/").replace("/claude-code-setup/", f"/{SLUG}/")
    head = sub_once(r"<title>.*?</title>", f"<title>{TITLE}</title>", head)
    head = sub_once(r'<meta name="description" content=".*?">',
                    f'<meta name="description" content="{DESCRIPTION}">', head)
    head = sub_once(r'<meta property="og:title" content=".*?">',
                    f'<meta property="og:title" content="{TITLE}">', head)
    head = sub_once(r'<meta property="og:description" content=".*?">',
                    f'<meta property="og:description" content="{OG_DESCRIPTION}">', head)
    if "claude-code-setup" in head:
        raise SystemExit("template slug still present in head")

    body = open(os.path.join(HERE, "body_en.html"), encoding="utf-8").read().strip()
    if "PLACEHOLDER" in body:
        raise SystemExit("body_en.html still contains a PLACEHOLDER")

    spec = importlib.util.spec_from_file_location("ait", LABEL_PY)
    ait = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ait)
    i = body.rfind("</main>")
    body = body[:i] + ait.colophon("pub_en", "en", uid="c") + body[i:]

    out_dir = os.path.join(ROOT, SLUG)
    os.makedirs(out_dir, exist_ok=True)
    out = head + "<body>\n" + body + "\n\n    " + tail
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {SLUG}/index.html ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
