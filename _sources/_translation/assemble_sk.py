#!/usr/bin/env python3
"""Assemble a Slovak edition of an HTML-only publication.

Takes the English page (head, CSS, scripts) + a hand-translated Slovak <body> fragment
and writes <slug>-sk/index.html with lang/meta/canonical swapped, hreflang alternates,
a .lang-link style, the Slovak AI-transparency colophon (from training-ops) and the
original scripts. Idempotent; run from the publications repo root.

Usage:
  python3 _sources/_translation/assemble_sk.py <en-slug> \
      --title "Slovenský názov · barcik.training" \
      --description "…" --og-title "…" --og-description "…"
"""
import argparse, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LABEL_PY = os.path.join(os.path.dirname(ROOT), 'training-ops', 'web', 'ai_transparency_label.py')

LANG_LINK_CSS = ("#sidebar-header .lang-link{display:inline-block;margin-top:.6rem;font-size:.78rem;"
                 "font-weight:600;color:var(--accent);text-decoration:none}"
                 "#sidebar-header .lang-link:hover{text-decoration:underline}\n")


def load_colophon(kind='pub', lang='sk'):
    spec = importlib.util.spec_from_file_location('ait', LABEL_PY)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.colophon(f'{kind}_{lang}', lang, uid='c')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--title', required=True)
    ap.add_argument('--description', required=True)
    ap.add_argument('--og-title', required=True)
    ap.add_argument('--og-description', required=True)
    ap.add_argument('--body', help='SK body fragment (default _sources/_translation/<slug>-sk-body.html)')
    ap.add_argument('--out-slug', help='default <slug>-sk')
    a = ap.parse_args()

    en_path = os.path.join(ROOT, a.slug, 'index.html')
    body_path = a.body or os.path.join(ROOT, '_sources', '_translation', f'{a.slug}-sk-body.html')
    out_slug = a.out_slug or f'{a.slug}-sk'
    out_dir = os.path.join(ROOT, out_slug)
    en = open(en_path, encoding='utf-8').read()
    body = open(body_path, encoding='utf-8').read().strip()

    head, rest = en.split('<body>', 1)
    # scripts / trailing part after </main></div>
    tail = rest[rest.rfind('<script'):] if '<script' in rest else '</body>\n</html>\n'

    base = 'https://publications.barcik.training'
    head = head.replace('<html lang="en">', '<html lang="sk">')
    head = re.sub(r'<title>.*?</title>', f'<title>{a.title}</title>', head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content=".*?">',
                  f'<meta name="description" content="{a.description}">', head, count=1, flags=re.S)
    head = head.replace(f'<link rel="canonical" href="{base}/{a.slug}/">',
                        f'<link rel="canonical" href="{base}/{out_slug}/">\n'
                        f'<link rel="alternate" hreflang="en" href="{base}/{a.slug}/">\n'
                        f'<link rel="alternate" hreflang="sk" href="{base}/{out_slug}/">')
    head = re.sub(r'<meta property="og:title" content=".*?">',
                  f'<meta property="og:title" content="{a.og_title}">', head, count=1, flags=re.S)
    head = re.sub(r'<meta property="og:description" content=".*?">',
                  f'<meta property="og:description" content="{a.og_description}">', head, count=1, flags=re.S)
    head = head.replace(f'<meta property="og:url" content="{base}/{a.slug}/">',
                        f'<meta property="og:url" content="{base}/{out_slug}/">')
    if 'og:locale' not in head:
        head = head.replace('<meta name="twitter:card"', '<meta property="og:locale" content="sk_SK">\n<meta name="twitter:card"')
    if '.lang-link' not in head:
        head = head.replace('</style>\n</head>', LANG_LINK_CSS + '</style>\n</head>', 1)

    # colophon goes before the last </main>
    if 'id="ai-transparency"' not in body:
        i = body.rfind('</main>')
        body = body[:i] + load_colophon('pub', 'sk') + body[i:]

    os.makedirs(out_dir, exist_ok=True)
    out = head + '<body>\n\n' + body + '\n\n' + tail
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'wrote {out_slug}/index.html ({len(out):,} bytes)')


if __name__ == '__main__':
    main()
