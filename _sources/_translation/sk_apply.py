#!/usr/bin/env python3
"""Apply a Slovak mapping to a page whose English changed, then rebuild the SK edition.

    python3 sk_apply.py <slug> <mapping.py>

mapping.py defines SK = { live_segment_id: value } where value is either
  - a string: the full Slovak inner html for that segment, or
  - ('patch', needle, [(old, new), ...]): find the OLD Slovak segment containing `needle`
    (unique) and apply the replacements to it, or
  - ('number', None, None): the EN changed only by $700 -> $730; reuse the old SK with 700 -> 730.
Steps: snapshot old EN/SK maps, run resegment --write (live numbering), fill the SK file from the
mapping, report any live segment still carrying English, then run segments.py inject.
"""
import os, re, subprocess, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import ROOT, TDIR, find_segments, parse_segments_file

slug, mapping_path = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('m', mapping_path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SK = m.SK
en_old = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.txt'))
sk_old = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.sk.txt'))
old_en_to_sk = {en_old[i]: sk_old.get(i, en_old[i]) for i in en_old}

subprocess.run([sys.executable, os.path.join(TDIR, 'resegment.py'), slug, '--write'], check=True)
en_new = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.txt'))
sk_new = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.sk.txt'))

def find_old_sk(needle):
    hits = [v for v in sk_old.values() if needle in v]
    if len(hits) != 1:
        raise SystemExit(f'needle not unique ({len(hits)} hits): {needle[:60]!r}')
    return hits[0]

errors = []
for i, val in SK.items():
    if i not in en_new:
        errors.append(f'id {i} not in live segments'); continue
    if isinstance(val, str):
        sk_new[i] = val
    elif val[0] == 'patch':
        base = find_old_sk(val[1])
        for a, b in val[2]:
            if a not in base:
                errors.append(f'id {i}: patch anchor missing: {a[:60]!r}'); break
            base = base.replace(a, b)
        sk_new[i] = base
    elif val[0] == 'append':
        sk_new[i] = find_old_sk(val[1]) + val[2]
    elif val[0] == 'number':
        old_en = en_new[i].replace('$730', '$700')
        if old_en not in old_en_to_sk:
            errors.append(f'id {i}: number-only source not found'); continue
        sk_new[i] = re.sub(r'700(?=(\s|&nbsp;)*(mld|miliárd))', '730', old_en_to_sk[old_en])
    else:
        errors.append(f'id {i}: unknown mode')
if errors:
    print('\n'.join(errors)); sys.exit(1)

# write SK file back in live numbering
page = open(os.path.join(ROOT, slug, 'index.html'), encoding='utf-8').read()
live = find_segments(page)
out = [f'# segments of {slug}/index.html — Slovak (Fable 5); ids follow the EN extraction\n']
still_en = []
for j, (t, s, e, s2, e2) in enumerate(live):
    opening = page[s:e]
    hint = re.search(r'(class|id)="([^"]+)"', opening)
    hint = f' {hint.group(1)}={hint.group(2)}' if hint else ''
    body = sk_new.get(j, en_new[j])
    if body == en_new[j] and re.search(r'[A-Za-z]{4,}', re.sub(r'<[^>]+>|&[a-z]+;', '', body)) and not re.fullmatch(r'[\s\d$~%.,+&;a-zA-Z-]*', re.sub(r'<[^>]+>', '', body)):
        still_en.append((j, re.sub(r'<[^>]+>', '', body)[:70]))
    out.append(f'#### {j} {t}{hint}\n{body}\n')
open(os.path.join(TDIR, f'{slug}.segments.sk.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print(f'SK file written; segments identical to EN (check these): {len(still_en)}')
for j, s in still_en[:40]:
    print(f'   #{j} {s!r}')
