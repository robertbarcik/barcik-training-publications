#!/usr/bin/env /usr/bin/python3
"""QA for the research-report pages before deploy.

    /usr/bin/python3 _sources/research-reports/tools/verify_pages.py [slug ...]

Checks each reports/<slug>/index.html for: the riso reader block, exactly one AI transparency
notice, no PLACEHOLDER text, every figure PNG present, every [N] citation resolving to a
reference id, every root-relative link resolving to a file in the repo, and reports the page size.
Exit code 1 if anything fails.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
slugs = sys.argv[1:] or ["selfjudge", "geobias", "bloom"]
ok = True
for slug in slugs:
    path = os.path.join(PUB, "reports", slug, "index.html")
    if not os.path.exists(path):
        print(f"[{slug}] MISSING {path}")
        ok = False
        continue
    html = open(path, encoding="utf-8").read()
    probs = []
    if "riso-reader:start" not in html:
        probs.append("no riso reader block (run riso_reader.py apply)")
    n_ait = html.count('id="ai-transparency"')
    if n_ait != 1:
        probs.append(f"{n_ait} AI transparency notices (want 1)")
    if "PLACEHOLDER" in html:
        probs.append("PLACEHOLDER text still present")
    for src in re.findall(r'<img src="(figures/[^"]+)"', html):
        if not os.path.exists(os.path.join(PUB, "reports", slug, src)):
            probs.append(f"missing figure {src}")
    ref_ids = set(re.findall(r'id="ref-(\d+)"', html))
    for n in re.findall(r'href="#ref-(\d+)"', html):
        if n not in ref_ids:
            probs.append(f"citation [{n}] has no reference")
    for href in re.findall(r'href="(/[^"#?]*)', html):
        target = os.path.join(PUB, href.lstrip("/"))
        if href.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            probs.append(f"dead local link {href}")
    body_only = re.sub(r"<script>.*?</script>|<style>.*?</style>|<pre>.*?</pre>|<code>.*?</code>", "", html, flags=re.DOTALL)
    for m in re.findall(r'\[(\d{1,2})\](?!</a>)', re.sub(r'<a class="cite"[^>]*>\[\d+\]</a>', "", body_only)):
        probs.append(f"unlinked citation marker [{m}]")
    size_kb = os.path.getsize(path) // 1024
    figs = len(re.findall(r'<figure class="figure"', html))
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    status = "OK " if not probs else "FAIL"
    print(f"[{slug}] {status} {size_kb} KB, {figs} figures, ~{words} words")
    for p in probs:
        print(f"    - {p}")
        ok = False
sys.exit(0 if ok else 1)
