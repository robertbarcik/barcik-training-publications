#!/usr/bin/env python3
"""Segment-based translation helper for HTML-only publications.

extract:  python3 segments.py extract <slug>            -> _sources/_translation/<slug>.segments.txt
inject:   python3 segments.py inject  <slug> [--out-slug <slug>-sk] [--title ..] [--description ..]
                                                        -> <slug>-sk/index.html

The segments file lists every leaf text block of <slug>/index.html (p, li, h1-h6, td, th, figcaption,
button, summary, label, svg <text>, and div/span that hold only inline content) as

    #### <n> <tag> [<path hint>]
    <inner html>

Translate the inner html in place (keep inline tags/attributes verbatim); untouched entries are
copied through. `inject` rewrites only those inner-html spans, then applies the same head/lang/
colophon treatment as assemble_sk.py (lang, title, meta, canonical, hreflang, og, lang link CSS,
Slovak AI-transparency colophon before the last </main>) — plus optional sidebar lang link when a
#sidebar-header <p> exists.
"""
import argparse, importlib.util, os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TDIR = os.path.join(ROOT, '_sources', '_translation')
LABEL_PY = os.path.join(os.path.dirname(ROOT), 'training-ops', 'web', 'ai_transparency_label.py')

LEAF_TAGS = ['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'th', 'figcaption', 'button', 'summary',
             'label', 'caption', 'dt', 'dd', 'text', 'div', 'span', 'a', 'em', 'strong', 'small', 'blockquote', 'title', 'option', 'legend']
BLOCK_TAGS = ['p', 'div', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
              'blockquote', 'section', 'article', 'aside', 'nav', 'header', 'footer', 'main', 'pre', 'svg', 'figure',
              'figcaption', 'details', 'summary', 'button', 'text', 'dl', 'dt', 'dd', 'form', 'select', 'label', 'style', 'script']
SKIP_INSIDE = ['script', 'style', 'pre', 'code']
BLOCK_RE = re.compile(r'<(' + '|'.join(BLOCK_TAGS) + r')(\s|>|/)', re.I)


def spans_of(text, tags):
    """Return list of (start,end) for elements of given tags, non-nested-aware via a simple stack."""
    out = []
    tag_re = re.compile(r'<(/?)(' + '|'.join(tags) + r')(\s[^>]*)?>', re.I | re.S)
    stack = []
    for m in tag_re.finditer(text):
        closing, tag = m.group(1) == '/', m.group(2).lower()
        selfclose = m.group(0).endswith('/>')
        if selfclose:
            continue
        if not closing:
            stack.append((tag, m.start(), m.end()))
        else:
            # pop to matching tag
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == tag:
                    t, s, e = stack.pop(i)
                    out.append((t, s, e, m.start(), m.end()))
                    del stack[i:]
                    break
    return out


def find_segments(text):
    """Leaf segments: elements in LEAF_TAGS whose inner html has no block-level tag, not inside skip areas,
    with at least one letter; nested leaf candidates collapse to the outermost."""
    skip = [(s, e2) for (t, s, e, s2, e2) in spans_of(text, SKIP_INSIDE)]
    # comments
    for m in re.finditer(r'<!--.*?-->', text, re.S):
        skip.append((m.start(), m.end()))
    def in_skip(a, b):
        return any(a >= s and b <= e for s, e in skip)
    cands = []
    for (t, s, e, s2, e2) in spans_of(text, LEAF_TAGS):
        inner = text[e:s2]
        if not inner.strip() or not re.search(r'[A-Za-z]', re.sub(r'<[^>]+>|&[a-z]+;', '', inner)):
            continue
        if BLOCK_RE.search(inner):
            continue
        if in_skip(s, e2):
            continue
        if 'class="lang-link"' in text[s:e]:
            continue  # sidebar language switch: handled by inject, never a translation segment
        cands.append((t, s, e, s2, e2))
    # collapse nested: keep outermost
    cands.sort(key=lambda c: (c[1], -c[4]))
    kept = []
    for c in cands:
        if kept and c[1] >= kept[-1][1] and c[4] <= kept[-1][4]:
            continue
        kept.append(c)
    return kept  # (tag, open_start, inner_start, inner_end, close_end)


def extract(slug):
    path = os.path.join(ROOT, slug, 'index.html')
    text = open(path, encoding='utf-8').read()
    segs = find_segments(text)
    out = [f'# segments of {slug}/index.html — translate inner html in place; keep tags/attrs verbatim\n']
    for i, (t, s, e, s2, e2) in enumerate(segs):
        opening = text[s:e]
        hint = re.search(r'(class|id)="([^"]+)"', opening)
        hint = f' {hint.group(1)}={hint.group(2)}' if hint else ''
        out.append(f'#### {i} {t}{hint}\n{text[e:s2]}\n')
    dst = os.path.join(TDIR, f'{slug}.segments.txt')
    open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    words = sum(len(re.sub(r'<[^>]+>', ' ', text[e:s2]).split()) for (t, s, e, s2, e2) in segs)
    print(f'{len(segs)} segments, ~{words} words -> {dst}')


def parse_segments_file(path):
    txt = open(path, encoding='utf-8').read()
    parts = re.split(r'^#### (\d+) \S+.*$', txt, flags=re.M)
    # parts: [preamble, id, body, id, body...]
    d = {}
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        if body.startswith('\n'): body = body[1:]
        if body.endswith('\n\n'): body = body[:-2]
        elif body.endswith('\n'): body = body[:-1]
        d[int(parts[i])] = body
    return d


def load_colophon():
    spec = importlib.util.spec_from_file_location('ait', LABEL_PY)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.colophon('pub_sk', 'sk', uid='c')


LANG_LINK_CSS = ("#sidebar-header .lang-link{display:inline-block;margin-top:.6rem;font-size:.78rem;"
                 "font-weight:600;color:var(--accent);text-decoration:none}"
                 "#sidebar-header .lang-link:hover{text-decoration:underline}\n")


def inject(slug, out_slug, title, description, og_title, og_description, sk_file=None):
    path = os.path.join(ROOT, slug, 'index.html')
    text = open(path, encoding='utf-8').read()
    segs = find_segments(text)
    sk = parse_segments_file(sk_file or os.path.join(TDIR, f'{slug}.segments.sk.txt'))
    # Align live segments with the SK file through the committed EN extraction (<slug>.segments.txt):
    # ids are matched by EN inner html (moving pointer, so duplicates keep their order), which keeps
    # injection correct after the EN page gains or loses a leaf. Falls back to positional ids.
    en_path = os.path.join(TDIR, f'{slug}.segments.txt')
    en = parse_segments_file(en_path) if os.path.exists(en_path) else {}
    idmap, drift = {}, []
    if en:
        order = sorted(en)
        ptr = 0
        for j, (t, s, e, s2, e2) in enumerate(segs):
            inner = text[e:s2]
            hit = None
            for k in range(ptr, len(order)):
                if en[order[k]] == inner:
                    hit = k; break
            if hit is None:  # look behind a little (reordered) before giving up
                for k in range(max(0, ptr - 5), ptr):
                    if en[order[k]] == inner:
                        hit = k; break
            if hit is None:
                drift.append((j, t, inner[:60])); continue
            idmap[j] = order[hit]; ptr = hit + 1
        if drift:
            print(f'  {len(drift)} live segment(s) not in {os.path.basename(en_path)} (left in English):')
            for j, t, snippet in drift[:20]:
                print(f'    live #{j} <{t}> {snippet!r}')
    else:
        idmap = {j: j for j in range(len(segs))}
    changed = 0
    for j in range(len(segs) - 1, -1, -1):
        i = idmap.get(j)
        if i is not None and i in sk:
            t, s, e, s2, e2 = segs[j]
            if sk[i] != text[e:s2]:
                text = text[:e] + sk[i] + text[s2:]
                changed += 1
    base = 'https://publications.barcik.training'
    text = text.replace('<html lang="en">', '<html lang="sk">', 1)
    if title:
        text = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', text, count=1, flags=re.S)
    if description:
        text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', text, count=1, flags=re.S)
    if og_title:
        text = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{og_title}">', text, count=1, flags=re.S)
    if og_description:
        text = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{og_description}">', text, count=1, flags=re.S)
    if 'hreflang=' in text:
        text = text.replace(f'<link rel="canonical" href="{base}/{slug}/">', f'<link rel="canonical" href="{base}/{out_slug}/">', 1)
    else:
        text = text.replace(f'<link rel="canonical" href="{base}/{slug}/">',
                            f'<link rel="canonical" href="{base}/{out_slug}/">\n<link rel="alternate" hreflang="en" href="{base}/{slug}/">\n<link rel="alternate" hreflang="sk" href="{base}/{out_slug}/">', 1)
    text = text.replace(f'<meta property="og:url" content="{base}/{slug}/">', f'<meta property="og:url" content="{base}/{out_slug}/">', 1)
    if 'og:locale' not in text:
        text = text.replace('<meta name="twitter:card"', '<meta property="og:locale" content="sk_SK">\n<meta name="twitter:card"', 1)
    # sidebar lang link: the EN page may already carry its own "Čítať po slovensky" link -> flip it
    en_link = re.search(r'<a class="lang-link" href="/[^"]+">.*?</a>', text, flags=re.S)
    if en_link:
        text = text[:en_link.start()] + f'<a class="lang-link" href="/{slug}/">Read in English &rarr;</a>' + text[en_link.end():]
    elif 'class="lang-link"' not in text:
        m = re.search(r'(<div id="sidebar-header">.*?<p>.*?</p>)', text, flags=re.S)
        if m:
            ind = re.search(r'\n(\s*)<p>', m.group(1))
            ind = ind.group(1) if ind else '    '
            text = text[:m.end()] + f'\n{ind}<a class="lang-link" href="/{slug}/">Read in English &rarr;</a>' + text[m.end():]
            if '.lang-link' not in text:
                text = text.replace('</style>\n</head>', LANG_LINK_CSS + '</style>\n</head>', 1)
    # colophon: replace the EN one if present, else insert before last </main>
    if 'lang="en" aria-label="AI transparency"' in text:
        text = re.sub(r'\n?<!-- AI transparency notice \(Art 50 EU AI Act, voluntary\) -->\n<aside class="ai-transparency".*?</aside>\n<style>.*?</style>\n',
                      lambda m: load_colophon(), text, count=1, flags=re.S)
    elif 'id="ai-transparency"' not in text:
        i = text.rfind('</main>')
        text = text[:i] + load_colophon() + text[i:]
    # extra literal replacements (JS strings, legend labels ...): <slug>.extra.sk.tsv, "old<TAB>new" per line
    extra = os.path.join(TDIR, f'{slug}.extra.sk.tsv')
    n_extra = 0
    if os.path.exists(extra):
        for line in open(extra, encoding='utf-8'):
            if not line.strip() or line.startswith('#'): continue
            old, new = line.rstrip('\n').split('\t', 1)
            if old not in text:
                # JS source keeps non-ASCII as \uXXXX escapes; try both cases
                cands = [''.join(c if ord(c) < 128 else ('\\u%04X' % ord(c) if ord(c) < 0x10000 else ''.join('\\u%04X' % x for x in (0xD800 + ((ord(c)-0x10000) >> 10), 0xDC00 + ((ord(c)-0x10000) & 0x3FF)))) for c in old)]
                cands.append(cands[0].replace('\\u00B7', '\\u00b7'))
                cands.append(re.sub(r'\\u([0-9A-F]{4})', lambda m: '\\u' + m.group(1).lower(), cands[0]))
                found = next((c for c in cands if c in text), None)
                if not found:
                    print('  extra: NOT FOUND ->', old[:70]); continue
                old = found
            text = text.replace(old, new); n_extra += 1
        print(f'  extra literals applied: {n_extra}')
    os.makedirs(os.path.join(ROOT, out_slug), exist_ok=True)
    open(os.path.join(ROOT, out_slug, 'index.html'), 'w', encoding='utf-8').write(text)
    missing = [i for i in range(len(segs)) if i not in sk]
    print(f'{out_slug}/index.html written; {changed}/{len(segs)} segments replaced; missing ids: {missing[:20]}{"..." if len(missing) > 20 else ""}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['extract', 'inject'])
    ap.add_argument('slug')
    ap.add_argument('--out-slug'); ap.add_argument('--title'); ap.add_argument('--description')
    ap.add_argument('--og-title'); ap.add_argument('--og-description'); ap.add_argument('--sk-file')
    a = ap.parse_args()
    if a.cmd == 'extract':
        extract(a.slug)
    else:
        inject(a.slug, a.out_slug or f'{a.slug}-sk', a.title, a.description, a.og_title, a.og_description, a.sk_file)
