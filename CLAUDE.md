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

## Source conventions

Publications in this repo follow one of three source-location patterns:

1. **Full markdown sources** — chapter `.md` files under `_sources/<slug>/chapters/` with a `build_html.py` that produces the deployed HTML. Use this pattern for new long-form booklets.
2. **HTML-only** — some publications were built elsewhere (or imported) and only the final `<slug>/index.html` lives in this repo. Listed with a `—` in the Source column below.
3. **External sibling repo** — one publication (LLM-Human Interaction Patterns) ships with an interactive app, so its source + app live in their own GitHub repo. The deployed booklet HTML is copied into this repo under the publication's slug.

## Current publications

### Booklets

| Publication | Path | Source | Words / Chapters |
|---|---|---|---|
| The Agent Horizon | `/agent-horizon/` | `_sources/agent-horizon/` | ~16,000 / 11 chapters (V2) |
| Open-Weight Model Families & Model Selection | `/open-weight-models/` | — (HTML-only) | Interactive, 3 parts |
| Building Agentic AI — Design Patterns from Production | `/agentic-design-patterns/` | `_sources/agentic-design-patterns/` | ~28,000 / 10 chapters |
| LLM-Human Interaction Design Patterns for Operations | `/llm-human-interaction-patterns/` | [github.com/robertbarcik/llm-human-interaction-patterns](https://github.com/robertbarcik/llm-human-interaction-patterns) (`booklet/_sources/`) | ~30,000 / 10 chapters |
| Scenario Planning for Generative AI | `/scenario-planning/` | `_sources/scenario-planning/` (data-sources.md only) | Capex decoder (method section) + 8 currents (July 2026 edition; 7 Physical Substrate + 8 Political Economy of Displacement added); 2 interactive SVGs (decoder capex incl. 2029 author-bet ring, S3 dot-com) + presenter cards; dated trigger-log panel per current; "Where I'd Put My Chips" author-probability section (`.bet` cards ported from mercantilism; weights finalized by Robert Jul 3); currents changelog + one-event-one-count pair rule + ambiguous-headline table in synthesis (composite headers name both currents); deep cross-links with mercantilism booklet both directions. Style rules from Robert's Jul 3 proofread: NO em dashes anywhere (doesn't sound like him), no "it is not X, it is Y" constructions, reader-hook intro, plain-language framing before number-dense sections, first-person field notes in C6/C8; external source links added (Brookfield, Deloitte, LBNL/DOE, PJM, TSMC, Sequoia, Canaries, METR, RLI, AI Index); Trigger Drill worksheet section removed |
| The Mercantilism of Generative AI | `/mercantilism-of-genai/` | `_sources/mercantilism-of-genai/` (notes.md only) | ~10,000 words / 15 sections, 6 mechanisms + counter-current (June 2026, updated July 2026); HTML-only hand-built, cloned from scenario-planning design system; 6 static CSS/SVG diagrams (incl. "two futures" armed↔targeted spectrum + three-tier shield); `.disclaimer-note` (red), `.bet`, `.coauthor-note`, `.field-note` components. July 2026 update: gated return logged (Mythos vetted-companies-only primarily US; Fable expensive API + moderation layer), Bet 1 scored won early, M1 tiering trigger fired, "frontier has one occupant" watch entry; armed/targeted + shield-as-fuse + field note split out of M3 into new Mechanism 4 `#m-armed` (old M4/M5 → M5/M6; scenario-planning's armed-vs-targeted link retargeted); full voice sweep per Robert's rules (no em dashes / no "it is not X, it is Y") EXCEPT Opus 4.8's signed June co-author note, kept verbatim as time capsule; lens-chapter reader hook; RSI derivative argument given honest counterweight; second signed co-author note added by Fable 5 (cyan `.coauthor-note`). Sequel/companion to Scenario Planning (Current 4: Sovereignty) |
| The Economics of the Frontier | `/economics-of-the-frontier/` | `_sources/economics-of-the-frontier/` (research-report.md, references.md, figures/build_figures.py) | ~13,000 / 7 ledgers; HTML-only hand-built; 4 static figures rendered by matplotlib (`build_figures.py` → `economics-of-the-frontier/figures/*.png`) |
| The Token Economics | `/token-economics/` | `_sources/token-economics/` | ~49,000 / 14 chapters (April 2026, updated July 2026). July 2026 editorial pass per Robert's voice rules (no em dashes / no "it is not X, it is Y"; sole survivor is Table 3.10's empty-cell marker): full voice sweep of all 15 source files; Ch3 followability fixes (blended-rate formula above Table 3.3, ops-regime footnotes on 3.6/3.9, deployer→provider AI Act caveat, two-futures capex note linking `/scenario-planning/#decoder`); new sections Ch9 "The Staff-Augmentation Squeeze", Ch12 "From Bundles to Products", Ch8 "Operating the Agents: Oversight as a Service" (links `/llm-human-interaction-patterns/`), Ch7 "The OS Vendors Are Coming for This Too", Ch11 EU-hosted-inference middle-path paragraph; Ch14 "The Portfolio View" 13-model comparison table; dated July 2026 notes in Ch4/Ch10 (gated frontier access; jurisdictional lock-in) + Ch7 open-weights caveat, cross-linked to mercantilism `#m-utility`/`#m-bloc`/`#m-open`; canonical cost-gap ratio 5-15x quality-matched (Ch1 updated); frontmatter names the Freshness Watch ↔ trigger-log kinship. Build via `tools/build_html.py` (now rewrites inter-chapter `.md` hrefs to `#slug` anchors) → copy `output/booklet.html` to `token-economics/index.html`; also `build_md.py`/`build_docx.py`. April 2026 pricing tables kept by design; update log in `_sources/token-economics/notes.md` |

### Research Reports

| Publication | Path | Source | Notes |
|---|---|---|---|
| Warden — Testing LLM-as-Judge Defenses Against Public Jailbreaks | `/warden/` | `_sources/warden/` | ~19,500 / 9 chapters + 3 appendices. Analysis repo: [github.com/robertbarcik/warden](https://github.com/robertbarcik/warden) |
| GeoBias — 7B Model Evaluation Report | `/reports/geobias-7b/` | — (HTML-only) | Analysis repo: [github.com/robertbarcik/geobias](https://github.com/robertbarcik/geobias) |
| SelfJudge — Can Small LLMs Judge Their Own Outputs? | `/reports/selfjudge/` | — (HTML-only) | Analysis repo: [github.com/robertbarcik/selfjudge](https://github.com/robertbarcik/selfjudge) |
| Bloom — AI Behavioral Safety Evaluation | `/reports/bloom/` | — (HTML-only) | Analysis repo: [github.com/robertbarcik/bloom](https://github.com/robertbarcik/bloom) |

### Guides & Legacy

| Publication | Path | Source | Notes |
|---|---|---|---|
| Claude Code Setup — How It All Works | `/claude-code-setup/` | — (HTML-only) | Reference guide, 9 sections |
| The Mirror of Artificial Intelligence (EN) | `/mirror-of-ai/` | `_sources/mirror-of-ai/` | 38 stories + 9 essays, 2023 |
| Zrkadlo umelej inteligencie (SK) | `/mirror-of-ai-sk/` | `_sources/mirror-of-ai-sk/` | Slovak edition of Mirror of AI |
