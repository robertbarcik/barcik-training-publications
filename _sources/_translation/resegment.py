#!/usr/bin/env python3
"""Re-align a Slovak segments file after the English page changed.

    python3 resegment.py <slug>            # dry run: report which live segments are new/changed
    python3 resegment.py <slug> --write    # rewrite <slug>.segments.txt + <slug>.segments.sk.txt
                                           # in the live numbering, carrying SK over by content match

Segments whose EN inner html is unchanged keep their translation. New or edited segments are
written into the SK file with their ENGLISH text (so `inject` leaves them readable) and listed
with a `TODO-SK` marker in the report, ready to be translated by hand (Fable, never a sub-model).
Run `segments.py inject <slug>` afterwards.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import ROOT, TDIR, find_segments, parse_segments_file


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    slug = sys.argv[1]; write = '--write' in sys.argv
    page = open(os.path.join(ROOT, slug, 'index.html'), encoding='utf-8').read()
    live = find_segments(page)
    en_old = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.txt'))
    sk_old = parse_segments_file(os.path.join(TDIR, f'{slug}.segments.sk.txt'))
    order = sorted(en_old); ptr = 0
    new_en, new_sk, todo = [], [], []
    for j, (t, s, e, s2, e2) in enumerate(live):
        inner = page[e:s2]
        opening = page[s:e]
        hint = re.search(r'(class|id)="([^"]+)"', opening)
        hint = f' {hint.group(1)}={hint.group(2)}' if hint else ''
        hit = None
        for k in range(ptr, len(order)):
            if en_old[order[k]] == inner:
                hit = k; break
        if hit is None:
            for k in range(max(0, ptr - 5), ptr):
                if en_old[order[k]] == inner:
                    hit = k; break
        if hit is not None:
            sk = sk_old.get(order[hit], inner); ptr = hit + 1
        else:
            sk = inner; todo.append((j, t, re.sub(r'<[^>]+>', '', inner)[:90]))
        new_en.append(f'#### {j} {t}{hint}\n{inner}\n')
        new_sk.append(f'#### {j} {t}{hint}\n{sk}\n')
    print(f'{slug}: {len(live)} live segments, {len(todo)} need translation (TODO-SK):')
    for j, t, snippet in todo:
        print(f'  TODO-SK #{j} <{t}> {snippet!r}')
    if write:
        open(os.path.join(TDIR, f'{slug}.segments.txt'), 'w', encoding='utf-8').write(
            f'# segments of {slug}/index.html — translate inner html in place; keep tags/attrs verbatim\n\n' + '\n'.join(new_en))
        open(os.path.join(TDIR, f'{slug}.segments.sk.txt'), 'w', encoding='utf-8').write(
            f'# segments of {slug}/index.html — Slovak (Fable 5); ids follow the EN extraction\n\n' + '\n'.join(new_sk))
        print('  written: segments.txt + segments.sk.txt (untranslated ids carry English text)')


if __name__ == '__main__':
    main()
