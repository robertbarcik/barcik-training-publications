# The Token Economics — update log

Working notes for the booklet at `/token-economics/`. Sources: `chapters/*.md`, built by `tools/build_html.py` (→ `output/booklet.html`, copied to `token-economics/index.html`), plus `tools/build_md.py` and `tools/build_docx.py` for the other artifacts. Pricing tables remain the April 2026 snapshot by design; the Freshness Watch blocks own the aging story.

## 2026-07-04 — July 2026 editorial pass (with Claude / Fable 5)

Full editorial pass following Robert's review request; decisions: staff augmentation as a Chapter 9 section (not a new chapter), April pricing kept with dated July notes only where the world changed.

- **Voice sweep, all 15 chapter files**: ~630 em dashes rewritten (commas/colons/semicolons/parens; `·` in the 16 table captions), "it is not X, it is Y" tic removed throughout; approved "X, not Y" appositives kept. Sole surviving em dash: the empty-cell marker in Table 3.10.
- **Chapter 3 followability**: blended-rate formula added above Table 3.3 (0.75 × input + 0.25 × output, worked for Flash-Lite → $5.40); ops non-monotonicity footnotes on Tables 3.6/3.9 (validation → steady state → multi-tenant); EU AI Act deployer→provider caveat in "What These Numbers Do Not Capture"; two-futures capex note by Table 3.13 linking `/scenario-planning/#decoder`.
- **New sections**: Ch9 "The Staff-Augmentation Squeeze" (+ At-a-glance bullet); Ch12 "From Bundles to Products" (rule of three, provider-obligation warning); Ch8 "Operating the Agents: Oversight as a Service" (AgentOps desk, AI Act Article 14, links `/llm-human-interaction-patterns/`); Ch7 honest problem "The OS Vendors Are Coming for This Too"; Ch11 paragraph on EU-hosted third-party inference as the middle path.
- **Ch14 "The Portfolio View"**: 13-row comparison table of every business model in the booklet (margin, time to revenue, defensibility, what kills it) + cash-engine-plus-differentiator guidance, placed before the 18-month roadmap.
- **July 2026 dated notes** (blockquote `**July 2026 note...**` style): Ch4 "the sovereignty risk this chapter does not price" (gated frontier access → `/mercantilism-of-genai/#m-utility`); Ch10 jurisdictional lock-in layer (→ `#m-bloc`); Ch7 open-weights trajectory caveat (→ `#m-open`). Frontmatter date line now "April 2026 · log updated July 2026"; frontmatter also names the Freshness Watch ↔ trigger-log kinship with links to both companion booklets.
- **Consistency**: canonical cost-gap ratio is Ch4's (5-15x quality-matched, 10-30x all-in); Ch1's six "5-10x" sites updated to 5-15x with the quality-matched qualifier; Gemini naming aligned with Ch3's table ("Gemini Flash"; Ch4's $0.10 figure corrected to Flash-Lite); frontmatter ToC entry 3 now matches Chapter 3's actual title.
- **Build script** (`build_html.py`): inter-chapter `href="NN_*.md"` links now rewritten to in-page `#slug` anchors (they were broken in the deployed single page); hardcoded `<title>`/og:title em dash → `&middot;`.
- Root `index.html` card and repo `CLAUDE.md` row updated. Word count ~49,000.

Anchor slugs all preserved (Chapter 3's title de-dash keeps the same slug because punctuation is stripped by `make_id`).

## 2026-08-16 — Slovak edition (Ekonomika tokenov) at `/token-economics-sk/`

All 15 source files translated by Fable 5 into `chapters_sk/` (meaning-first; prices and figures
kept in original currencies/dates; SK money format "5,40 $", "700 mld. $", ranges " – ").
`tools/build_html.py --lang sk` builds `output/booklet_sk.html` → `token-economics-sk/index.html`:
`T` dict for title/meta/sidebar, SK panel markers ("V skratke", "Strážca čerstvosti",
"Tabuľka N.M ·", "Číslo, ktoré si zapamätať", "Čo si z tejto kapitoly odniesť") recognised
alongside the EN ones, section ids derived from the **English** chapter titles so `#chapter-N-…`
anchors are shared by both editions, SK colophon via `training-ops/web/ai_transparency_label.py`.
Cross-links point to the SK Scenario Planning / Mercantilism / LLM-Human editions. Structural
check: identical tag/class/id/table counts to EN (only the translator's note differs). EN rebuilt
with hreflang + "Čítať po slovensky" sidebar link. Official-Regulation terms used where the text
touches the AI Act (poskytovateľ / nasadzujúci subjekt, posudzovanie zhody, orgány dohľadu nad trhom).
