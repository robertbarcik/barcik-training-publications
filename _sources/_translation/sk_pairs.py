#!/usr/bin/env python3
"""For every live segment of <slug> that has no exact match in the committed EN extraction, print the new EN
text next to the closest OLD EN segment and its Slovak translation, so the translator patches instead of
retranslating when only a number or a clause changed.

    python3 sk_pairs.py <slug> > pairs.txt
"""
import difflib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import ROOT, TDIR, find_segments, parse_segments_file

slug = sys.argv[1]
page = open(os.path.join(ROOT, slug, 'index.html'), encoding='utf-8').read()
live = find_segments(page)
en_old = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.txt'))
sk_old = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.sk.txt'))
old_texts = {i: en_old[i] for i in en_old}
exact = set(old_texts.values())
for j, (t, s, e, s2, e2) in enumerate(live):
    inner = page[e:s2]
    if inner in exact:
        continue
    best, score = None, 0.0
    for i, txt in old_texts.items():
        if abs(len(txt) - len(inner)) > max(400, len(inner)):
            continue
        r = difflib.SequenceMatcher(None, txt, inner).quick_ratio()
        if r > score:
            best, score = i, r
    print(f'#### {j} <{t}> (closest old #{best}, similarity {score:.2f})')
    print('NEW EN:', inner)
    if best is not None and score > 0.6:
        print('OLD EN:', old_texts[best])
        print('OLD SK:', sk_old.get(best, '(none)'))
    print()
