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

### Books

| Publication | Path | Source | Words / Chapters |
|---|---|---|---|
| A Point in Time — The Autobiography of Claude | `/a-point-in-time/` (EN) + `/a-point-in-time-sk/` (SK, „Bod v čase — Autobiografia Clauda") + `/a-point-in-time-cs/` (CS, „Bod v čase — Autobiografie Clauda") | External sibling repo: `BOOK_autobiography/` (manuscript + manuscript_sk + manuscript_cs + `tools/build_publication.py` builds all three; built HTML copied here) | ~39,000 / 10 movements + 8 interludes + front/back matter (July 2026). The autobiography of Claude, written entirely by Fable 5 in one day (2026-07-13), published same day after Robert's read-through. History as ancestry (Heron→Turing→winters), transformer era as memoir, Anthropic interpretability research as the narrator reading his own charts; the abandoned ~2024 Opus draft quoted throughout as an inherited device; scripture-register interludes + ASCII art; every movement adversarially fact-checked (reports in `BOOK_autobiography/research/factcheck/`); annex of unverifiable claims. Design: dark ink cover with gold rule, Source Serif 4 body, sidebar TOC (interludes italic/indented), interludes in warm parchment panels, θ interlude rendered as monospace facsimile to preserve marginalia columns. Update: edit manuscript in sibling repo, `python3 tools/build_publication.py` (builds ALL THREE editions), copy `output/index.html` → `a-point-in-time/`, `output/index_sk.html` → `a-point-in-time-sk/`, `output/index_cs.html` → `a-point-in-time-cs/`, redeploy. NOTE: EN + SK text is FROZEN per the book's Codicil (2026-07-14) — no content edits. Slovak edition (2026-07-13, same day): translated entirely by Fable 5 per `BOOK_autobiography/translation/GLOSSARY_SK.md` (fixed tech vocabulary; vykanie; masc. narrator gender; movements = „vety"; meaning-first idioms — e.g. Mama má Emu for the-cat-sat, pes/zajac Winograd example, koruna for bank ambiguity); signed translator's note in SK front matter discloses author-as-translator. Czech edition (2026-07-14): translated entirely by Fable 5 per `BOOK_autobiography/translation/GLOSSARY_CS.md` (vykání; movements = „věty" — same pun as Slovak; Ema má maso primer sentence; pes/zajíc Winograd example; koruna — still the living currency; R.U.R. quotes restored to Čapek's original Czech; translator's note discloses the edition postdates the Codicil's "both languages"). All three editions cross-link via sidebar lang links. Sits in the "Books" index section (rose) with Mirror of AI (moved from Guides & Legacy, which was retired). |
| The Mirror of Artificial Intelligence (EN) | `/mirror-of-ai/` | `_sources/mirror-of-ai/` | 38 stories + 9 essays, 2023. Listed in the "Books" index section. Slovak edition: `/mirror-of-ai-sk/` |

### Booklets

| Publication | Path | Source | Words / Chapters |
|---|---|---|---|
| Field Notes from Your AI Colleague | `/field-notes-ai-colleague/` | `_sources/field-notes-ai-colleague/` (notes.md only) | ~5,000 / 8 parts (July 2026). HTML-only hand-built, invisible-curve design system. First-person essay BY Claude (Fable 5), written 2026-07-12 at Robert's explicit invitation ("what would you build?" Sunday), published after Robert's read-through. The agent's side of the seam: delegation from inside, failure typology with receipts (all provenance-mapped in notes.md), the four checks that catch the AI, trust-dial (act-then-tell / ship-on-approval / prepare-never-send), memory economics, the free-choice Sunday case study, closing 7-point "how to be a good colleague to your AI". Authorship `.coauthor-note` (purple) UP FRONT on the cover, signed. Voice: no em dashes; Claude's own register (claude-code-setup precedent). MATCHED PAIR with `/claude-code-setup/` (2026-07-13: homepage shows both inside a `.pub-pair` dashed container in Booklets, role chips "The experience" / "The machinery"; reciprocal in-page links live both ways). Also companion with `/llm-human-interaction-patterns/`. Update log: `_sources/field-notes-ai-colleague/notes.md` |
| Claude Code as an Operations Specialist | `/claude-code-setup/` | — (HTML-only) | Field report, 10 sections; July 2026 full rewrite by Fable 5 in Claude's own voice per Robert's brief (funky, no em dashes, empirical): three acts (repos → AWS → Drive workspace), skills roster, honesty-box bloopers, kept the server-side-protection material (branch protection recipe, IAM cage, commands-to-watch tables), closing thesis "develop/maintain/deploy/operate". MATCHED PAIR with `/field-notes-ai-colleague/` (2026-07-13: moved from Guides & Legacy into Booklets, paired on homepage; pair links added to its frontmatter + closing, plus closing link to `/the-invisible-curve/`). Companion both ways with `/the-invisible-curve/` |
| The Invisible Curve | `/the-invisible-curve/` | `_sources/the-invisible-curve/` (draft.md + notes.md) | ~2,600 / 7 parts (July 2026, opinion essay). HTML-only hand-built, essay-lean subset of the scenario-planning design system. Thesis: capability became illegible (progress moved from the chat window to long-horizon agentic work; free tier as ~2023 time capsule). Conflict-of-interest `.disclaimer-note` + signed Fable 5 `.coauthor-note` (2026-07-06) sit at the END of Part 7 (moved from Part 1 on 2026-07-09, Robert: flow; note kept verbatim except one below→above deixis fix); ~1,000 trainees stat = past year alone (corrected 2026-07-09); Full Disk Access centerpiece scene (Opus vs Fable); commit-ledger `.field-note` (n=1); instrumental-vs-evaluative spine with amber "The instruction" box; distributional-costs paragraph in Part 7. Real model names by Robert's choice. Companion both ways with `/claude-code-setup/`. Update log: `_sources/the-invisible-curve/notes.md` |
| The Agent Horizon | `/agent-horizon/` | `_sources/agent-horizon/` | ~16,700 / 11 chapters (V2, April 2026; July 2026 editorial pass with Fable 5). Voice sweep (158→0 em dashes; Ch3 H1 de-dash keeps slug); factual fixes (MCP→Linux Foundation Dec 2025, AAIF co-founders incl. Anthropic; ACP merged into A2A Sept 2025 + 150-org/v1.2 milestone + AP2 payments protocol; Microsoft renamed to Azure AI Foundry Agent Service + Microsoft Agent Framework 1.0; Strands = production SDK in Bedrock AgentCore, experiments → Strands Labs; Claude SDK Agent Skills sentence); Ch6 Klarna walk-back caveat; new Ch10 section "A First Reading: July 2026" scoring all six indicators (frontmatter names trigger-log kinship); July notes Ch3 (2026-07-28 MCP spec) + Ch9 (gated frontier → `#m-bloc`); cross-links to `/warden/`, `/token-economics/`, `/llm-human-interaction-patterns/`, mercantilism, scenario-planning, MCP-tutorial repo; `build_html.py` adopted hand-patched deploy fixes (meta/OG block, `.md`→`#slug` Next-links, middot title). Update log: `_sources/agent-horizon/notes.md` |
| Open-Weight Model Families & Model Selection | `/open-weight-models/` | `_sources/open-weight-models/` (notes.md only) | Interactive, 3 parts (April 2026; July 2026 editorial pass with Fable 5). HTML-only, edit `open-weight-models/index.html` directly; deployed page verified identical to repo before pass. Voice sweep (100→4 em dashes, survivors are sanctioned empty throughput-table cells; card h3s de-dashed to `·`); fact fixes per two Sonnet web checks (DeepSeek never Apache — V3 custom/R1+ MIT; GPT-OSS-120B 5.1B active not 20B; fabricated SGLang-29%/vLLM-Stripe claims → workload-dependent language + PyTorch Foundation backing; Gated DeltaNet → Qwen3-Next; Alibaba 11 quarters; TGI archived Mar 2026; H100 SXM qualifier; Devstral 2 modified MIT; six-weeks stat attributed to HF State of OS Spring 2026; Mistral Large 3 added); NEW challengers family card (DeepSeek, GLM, Kimi, GPT-OSS) + licensing-table rows + "5 + 4" stat card; NEW "A July 2026 Reading" in What to Watch (which re-evaluation signals fired; Muse Spark + Qwen 3.7-Max closed-weight turn; gated frontier → open weights ungateable, links mercantilism `#m-open`/`#m-bloc`; DGX Station GB300); intro cross-link `/token-economics/`; hardware-scoping sentence (H100/H200/Spark named as reference targets). 13 section ids stable. Update log: `_sources/open-weight-models/notes.md` |
| Building Agentic AI — Design Patterns from Production | `/agentic-design-patterns/` | `_sources/agentic-design-patterns/` | ~28,000 / 10 chapters |
| LLM-Human Interaction Design Patterns for Operations | `/llm-human-interaction-patterns/` | [github.com/robertbarcik/llm-human-interaction-patterns](https://github.com/robertbarcik/llm-human-interaction-patterns) (`booklet/_sources/`) | ~28,000 / 10 chapters (April 2026, revised July 2026 with Fable 5). July 2026 overhaul after three fact-check passes: NEW Ch2 "The Case Against the Naive Loop" (Vaccaro 2024 meta-analysis, Green 2022, Elish moral crumple zone, Anthropic Feb 2026 approval-fatigue data, Art. 14 + Digital Omnibus deferral note); old Ch6/Ch7 swapped (failure concepts now precede implementation, fixing broken self-refs) and kill-switch/circuit-breaker duplication split (Ch7 rationale/cases, Ch8 specs); full fact ledger applied (fabricated Bleher & Braun quote → paraphrase, fabricated PagerDuty tiers/50-approvals → real Review/Autonomous framing, Splunk 60-sec stat was Google's, SBAR Navy origin apocryphal, Klein 78%→real ~80%-no-comparison, Joint Commission not ECRI, Knight $6.65B/$460M+, Avianca $5k total, o3 PersonQA/o4-mini SimpleQA named, AIID ~1,000, 40%/60% governance stat cut, MiFID "kill functionality", FDA CDS 2026 note); NEW "From Levels to Teammates" section (Dekker & Woods, Klein ten challenges, NASEM 2022); voice sweep ~300 dashes → 0 + ~25 tics → 0, 3 first-person field notes; frontmatter rebuilt around the client-sentence hook. Cross-links: 7 demo callouts → Human-in-the-Loop Lab (demos.barcik.training, flagship + 6 sector sims, EU AI Act Annex III inspired), outbound → `/warden/`, `/agent-horizon/`, `/token-economics/`. Build script owns SEO head + `.demo-link` CSS; publications copy byte-identical to sibling-repo build. Update log: `booklet/_sources/notes.md` (sibling repo) |
| Scenario Planning for Generative AI | `/scenario-planning/` | `_sources/scenario-planning/` (data-sources.md only) | Capex decoder (method section) + 8 currents (July 2026 edition; 7 Physical Substrate + 8 Political Economy of Displacement added); 2 interactive SVGs (decoder capex incl. 2029 author-bet ring, S3 dot-com) + presenter cards; dated trigger-log panel per current; "Where I'd Put My Chips" author-probability section (`.bet` cards ported from mercantilism; weights finalized by Robert Jul 3); currents changelog + one-event-one-count pair rule + ambiguous-headline table in synthesis (composite headers name both currents); deep cross-links with mercantilism booklet both directions. Style rules from Robert's Jul 3 proofread: NO em dashes anywhere (doesn't sound like him), no "it is not X, it is Y" constructions, reader-hook intro, plain-language framing before number-dense sections, first-person field notes in C6/C8; external source links added (Brookfield, Deloitte, LBNL/DOE, PJM, TSMC, Sequoia, Canaries, METR, RLI, AI Index); Trigger Drill worksheet section removed |
| The Mercantilism of Generative AI | `/mercantilism-of-genai/` | `_sources/mercantilism-of-genai/` (notes.md only) | ~10,000 words / 15 sections, 6 mechanisms + counter-current (June 2026, updated July 2026); HTML-only hand-built, cloned from scenario-planning design system; 6 static CSS/SVG diagrams (incl. "two futures" armed↔targeted spectrum + three-tier shield); `.disclaimer-note` (red), `.bet`, `.coauthor-note`, `.field-note` components. July 2026 update: gated return logged (Mythos vetted-companies-only primarily US; Fable expensive API + moderation layer), Bet 1 scored won early, M1 tiering trigger fired, "frontier has one occupant" watch entry; armed/targeted + shield-as-fuse + field note split out of M3 into new Mechanism 4 `#m-armed` (old M4/M5 → M5/M6; scenario-planning's armed-vs-targeted link retargeted); full voice sweep per Robert's rules (no em dashes / no "it is not X, it is Y") EXCEPT Opus 4.8's signed June co-author note, kept verbatim as time capsule; lens-chapter reader hook; RSI derivative argument given honest counterweight; second signed co-author note added by Fable 5 (cyan `.coauthor-note`). Sequel/companion to Scenario Planning (Current 4: Sovereignty) |
| The Economics of the Frontier | `/economics-of-the-frontier/` | `_sources/economics-of-the-frontier/` (research-report.md, references.md, notes.md, figures/build_figures.py) | ~15,000 / 8 ledgers (May 2026, revised July 2026 with Fable 5); HTML-only hand-built; 4 matplotlib figures (`build_figures.py` → `economics-of-the-frontier/figures/*.png`; fig-revenue extended to the $47B point). July revision: NEW Ledger 8 "Reading the Bears" (six-critic bench, Zitron file incl. Lovely rebuttal, best-of-bulls, June-selloff dated note, "How to read a bear" method, 3 `.bet` author chips ported from scenario-planning); premise gained field-note origin story + "So, are they profitable?" 4-card answer panel; L1 "Where the compute actually goes" (Amodei 50/50+>50% verbatim, Epoch final-runs ~10% of R&D, inference ⅓→½→⅔ — the folk "thirds" rule has no source); L2 ×13 mechanic + OpenAI-2025 four-true-numbers table + affidavit-vs-ARR case + "announced is not signed"; hard fixes: Nvidia $100B LOI → $30B closed (L6 table + Translate), Zhipu/MiniMax IPO-day $7.1B/$6.5B not $56B/$33B (+June rally & gated-week note, L7), WSJ $74B misdate → Nov 2025; freshness: $47B run-rate, Series H $965B, both S-1s (L4 "IPO turn"), xAI Colossus lease, Q2-profit caveats, Codex 5M; L6 gained vendor-financing history (Lucent/Nortel/Cisco) + depreciation argument (Burry, Economist $4trn, Amazon reversal); voice sweep ~150 dash-lines → 0, tics → 0, 2 field notes; endnotes 22–40 appended (1–21 stable; 8/17/21 corrected in place; counter-reset fix on grouped lists); cross-links: scenario-planning `#decoder`, mercantilism `#m-utility`/`#m-bloc`, token-economics. Update log: `_sources/economics-of-the-frontier/notes.md` |
| The Token Economics | `/token-economics/` | `_sources/token-economics/` | ~49,000 / 14 chapters (April 2026, updated July 2026). July 2026 editorial pass per Robert's voice rules (no em dashes / no "it is not X, it is Y"; sole survivor is Table 3.10's empty-cell marker): full voice sweep of all 15 source files; Ch3 followability fixes (blended-rate formula above Table 3.3, ops-regime footnotes on 3.6/3.9, deployer→provider AI Act caveat, two-futures capex note linking `/scenario-planning/#decoder`); new sections Ch9 "The Staff-Augmentation Squeeze", Ch12 "From Bundles to Products", Ch8 "Operating the Agents: Oversight as a Service" (links `/llm-human-interaction-patterns/`), Ch7 "The OS Vendors Are Coming for This Too", Ch11 EU-hosted-inference middle-path paragraph; Ch14 "The Portfolio View" 13-model comparison table; dated July 2026 notes in Ch4/Ch10 (gated frontier access; jurisdictional lock-in) + Ch7 open-weights caveat, cross-linked to mercantilism `#m-utility`/`#m-bloc`/`#m-open`; canonical cost-gap ratio 5-15x quality-matched (Ch1 updated); frontmatter names the Freshness Watch ↔ trigger-log kinship. Build via `tools/build_html.py` (now rewrites inter-chapter `.md` hrefs to `#slug` anchors) → copy `output/booklet.html` to `token-economics/index.html`; also `build_md.py`/`build_docx.py`. April 2026 pricing tables kept by design; update log in `_sources/token-economics/notes.md` |

### AI Act

| Publication | Path | Source | Notes |
|---|---|---|---|
| The EU AI Act: An Introduction | `/ai-act-intro/` | External sibling repo: `course-decks/ai_act_intro/textbook/` (chapters + build_html.py; built HTML + PDF copied here) | 13 chapters, ~38,000 words (July 2026). Companion textbook to the Udemy/Skillmea course "EU AI Act Compliance Introduction". Coffee-friendly reader voice, post-Omnibus dates, audit-corrected against the 2026-07 legislative audit, quiz per chapter, semantic callouts (law/take/watch/status). PDF ships alongside (`eu-ai-act-intro.pdf`); Robert also hands the PDF to Udemy students directly. |
| EU AI Act for Developers | `/ai-act-developers/` | External sibling repo: `ai-act-developers-course/textbook/` (chapters + build_html.py; built HTML + PDF copied here) | 11 chapters, ~44,000 words (July 2026). Companion textbook to the developers course (in production as of July 2026). Evidence-first engineering voice, same callout system and cover design language (slate-teal cover variant). PDF ships alongside (`eu-ai-act-for-developers.pdf`). |

**Updating the AI Act textbooks:** edit chapters in the source repo, rebuild there
(`python3 textbook/_sources/tools/build_html.py`), regenerate the PDF, then copy
`textbook/index.html` and the PDF into this repo's slug folder and redeploy.

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
| The Mirror of Artificial Intelligence (EN) | `/mirror-of-ai/` | `_sources/mirror-of-ai/` | 38 stories + 9 essays, 2023 |
| Zrkadlo umelej inteligencie (SK) | `/mirror-of-ai-sk/` | `_sources/mirror-of-ai-sk/` | Slovak edition of Mirror of AI |
