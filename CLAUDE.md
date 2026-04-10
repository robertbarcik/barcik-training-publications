# barcik-training-publications

Publications site for barcik.training — long-form guides, booklets, and research.

**Live URL:** https://publications.barcik.training/

## Site structure

```
/                           → index.html (publication listing)
/token-economics/           → index.html (The Token Economics booklet)
/[future-publication]/      → index.html (future publications)
```

**Source files** live in `_sources/{publication-name}/`:
- `chapters/` — Markdown chapter files (canonical source)
- `data/` — Structured data (pricing, etc.)
- `tools/` — Build scripts (build_html.py, build_docx.py, build_md.py)
- `output/` — DOCX and Markdown outputs (not deployed to S3)

## Build a publication

Each publication has its own build scripts in `_sources/{name}/tools/`.

**Token Economics example:**
```bash
cd /Users/robertbarcik/git-repos/barcik-training-publications
python3 _sources/token-economics/tools/build_html.py
cp _sources/token-economics/output/booklet.html token-economics/index.html
```

The build scripts read from `_sources/{name}/chapters/*.md` and write to `_sources/{name}/output/`.
After building, copy the HTML output to the site directory for deployment.

## Deploy to S3 + CloudFront

**AWS Profile:** `barcik-demos`
**Region:** `eu-central-1`
**S3 Bucket:** `barcik-training-publications`
**CloudFront Distribution ID:** `E1LQ9VRFA5AT7D`

### Step 1: Sync to S3

```bash
aws s3 sync . s3://barcik-training-publications/ \
  --exclude ".git/*" \
  --exclude ".github/*" \
  --exclude ".claude/*" \
  --exclude ".gitignore" \
  --exclude ".DS_Store" \
  --exclude "CLAUDE.md" \
  --exclude "_sources/*" \
  --profile barcik-demos \
  --region eu-central-1
```

### Step 2: Invalidate CloudFront cache

```bash
aws cloudfront create-invalidation \
  --distribution-id E1LQ9VRFA5AT7D \
  --paths "/*" \
  --profile barcik-demos
```

## Dependencies

For building publications:
```bash
pip3 install python-docx markdown
```

## Current publications

| Publication | Path | Source | Words | Status |
|---|---|---|---|---|
| The Token Economics | `/token-economics/` | `_sources/token-economics/` | ~40,000 | Published |
