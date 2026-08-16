# Scenario Planning for Generative AI — Data Sources

July 2026 edition (8 currents + capex decoder + "Where I'd Put My Chips").
Revised July 3, 2026: Robert's proofread pass (no em dashes, no "it is not X, it is Y" constructions, reader-hook intro, humanized Current 8, composite headers name both currents), chips weights finalized by Robert (C1 20 / C2 5 / C3 7 / C4 20 / C5 16 / C6 20 / C7 7 / C8 5), Trigger Drill worksheet removed, external source links inserted for heavyweight claims (listed per current below).
Companion publication: The Mercantilism of Generative AI (`/mercantilism-of-genai/`, `_sources/mercantilism-of-genai/notes.md`).

## The Capex Decoder / Current 1: Continued Scaling
- Capex data: company earnings reports and guidance (Alphabet, Amazon, Meta, Microsoft; Oracle supplemental)
- Inference share of AI compute: Brookfield "Building the Backbone of AI" (Aug 2025) — ~75% of AI compute demand from inference by 2030 (https://www.brookfield.com/sites/default/files/documents/Brookfield_Building_the_Backbone_of_AI.pdf); Deloitte TMT Predictions 2026 — inference ≈ two-thirds of all AI compute in 2026 (https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html). NOTE: the previously used "~70% by 2030" figure has no verifiable primary source; text now cites Brookfield's ~75%.
- Model parameter estimates: leaked/estimated from technical reports, analyst estimates
- Infrastructure milestones: xAI Colossus, Project Rainier (Amazon-built for Anthropic, ~500K chips), Stargate Abilene (OpenAI/Oracle, ~450K GPUs), Meta Hyperion (Louisiana, 5 GW)
- Fable 5 / Mythos launch, pricing, recall and gated restoration: Anthropic announcements (June 9, 2026), federal directive coverage (June 12–13, 2026), Project Glasswing reporting
- GPT-6 ("Spud") pre-training completion at Abilene: press reports (March 24, 2026)

## Current 2: Efficiency Revolution
- GPT-4 training cost: Sam Altman confirmed >$100M (includes R&D)
- Llama 3.1 405B: 30.84M H100 GPU-hours (~$60M compute)
- DeepSeek V3: $5.576M (2.788M H800 GPU-hours) — DeepSeek technical report
- DeepSeek R1: $294K incremental RL training — Nature, September 2025
- API pricing: OpenAI API pricing history, OpenRouter market rates, Anthropic pricing (May–July 2026)
- Open vs closed gap: Stanford HAI 2025 AI Index Report (Elo gap: 8.04% → 1.7%, https://hai.stanford.edu/ai-index/2025-ai-index-report); 2026 AI Index shows the gap re-widening to ~3.3% by March 2026 after the frontier stepped (https://hai.stanford.edu/ai-index/2026-ai-index-report) — booklet now frames convergence as per-tier
- April 2026 open-weight wave: model cards / release posts (GLM-5.1, Qwen 3.6, Kimi K2.6, DeepSeek V4-Pro, Mistral Medium 3.5)
- Mistral quotes: MIT Technology Review (March 2026), McKinsey interview, TIME (May 2024)
- Epoch AI peer-reviewed analysis of training costs

## Current 3: Financial Correction
- Nasdaq historical data: FRED/Yahoo Finance
- Amazon financials: SEC filings (10-K annual reports 2000-2005)
- Pets.com: IPO prospectus, post-mortem analyses
- Sequoia "AI's $600B Question": David Cahn, June 20, 2024 (https://sequoiacap.com/article/ais-600b-question/)
- Barclays "12,000 ChatGPT-sized products": Barclays Research 2025
- OpenAI valuation/financials: press reports (March 2026 funding round, $852B post-money)
- Anthropic valuation: Series H ($965B post-money), confidential S-1 (June 1, 2026), run-rate revenue reports
- MIT NANDA / Omdia (Oct 2025) / Accenture / Deloitte 2026 enterprise surveys
- GPU depreciation: Michael Burry analysis, CoreWeave S-1
- Ed Zitron arc: "Where's Your Ed At", "Better Offline"; Kelsey Piper in The Argument
- Julien Garran: MacroStrategy Partnership, CNN interview (October 2025)

## Current 4: Sovereignty
- Anthropic v. DoD: court filings (designation Feb 27, 2026; injunction; appeal)
- June 12, 2026 recall and gated restoration (Glasswing / API-only Fable): Anthropic statement, CNBC/9to5Mac coverage — see mercantilism booklet notes for the full source list
- Meta Muse Spark launch (April 8, 2026), Yann LeCun departure (Nov 2025)
- Chinese open-weight model cards (DeepSeek V4-Pro, GLM-5.1, Qwen 3.6, Kimi K2.6)
- Mistral Medium 3.5 release; Mistral ARR/valuation press (Jan 2026)
- Deep-dive companion: The Mercantilism of Generative AI (mechanisms 1–5, bets 1–6)

## Current 5: From Lab to Production
- Medical AI gap: meta-analysis across 83 studies (92% lab vs 52.1% field)
- SWE-Lancer / SWE-bench Verified / HumanEval leaderboards
- RE-Bench long-horizon comparisons
- Deloitte 2026, Accenture (61% underutilized), MIT NANDA (95%, caveated)
- EU AI Act + Digital Omnibus provisional agreement (May 7, 2026): Annex III → Dec 2, 2027; Annex I → Aug 2, 2028; transparency → Dec 2, 2026
- Copyright: Bartz v. Anthropic ($1.5B settlement), NYT v. OpenAI MDL (Jan 2026 log-production order), 56+ suits tracker

## Current 6: Hours and Dollars
- METR Time Horizon: TH 1.0 (Mar 2025, ~7-month doubling; https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/, paper arXiv 2503.14499), TH 1.1 (Jan 2026, ~3-month doubling from 2024; spring 2026 frontier pilot)
- Remote Labor Index: CAIS + Scale AI (https://www.remotelabor.ai/; arXiv 2510.26787); July 1, 2026 update — Fable 5 16.1% (218/240 projects), Opus 4.8 8.3%, GPT-5.5 6.3%; prior leader Opus 4.6 + Cowork 4.17%; 2.5% at launch
- Robert's field note (author-note in Current 6, added Jul 3): personal spend $20/mo (GPT-4 era) → $200/mo (Opus) → $500+/mo (Fable); "hours" jump felt first-hand rebuilding this edition
- Agent-hour cost math: Anthropic API pricing (Opus 4.7 $5/$25, Sonnet 4.6 $3/$15, Fable 5 $10/$50 per MTok), Claude Code token telemetry (~1M tok/hr moderate load)
- Developer loaded-cost comparators: Index.dev / MarsDevs hourly-rate surveys 2026
- Antigravity 2.0, Gemini Spark, Devin Cloud, Composer 2.5: vendor announcements / demo writeups

## Current 7: The Physical Substrate (new, July 2026)
- TSMC: quarterly reports (advanced nodes ~74% of wafer revenue); ~90% most-advanced chip share (The Conversation, Apr 2026: https://theconversation.com/how-taiwan-came-to-dominate-the-global-chip-industry-276939; USITC "Silicon Island" briefing corroborates 92% of capacity)
- Advanced packaging & HBM: Silicon Analysts foundry allocation Q1 2026 (CoWoS booked, 52–78 wk lead times, ~1M wafers 2026, Nvidia ~60%; HBM3E sold out 2026; SK Hynix ~62% HBM); Tom's Hardware (TSMC price hikes)
- Grid queues: LBNL "Queued Up" 2025 edition (Dec 2025; ~2,290 GW = 1,400 GW generation + ~890 GW storage, end-2024 data; https://emp.lbl.gov/publications/queued-2025-edition-characteristics, OSTI mirror https://www.osti.gov/biblio/3008763)
- Data-center electricity: LBNL/DOE US Data Center Energy Usage Report (4.4% of US electricity 2023 → 6.7–12% by 2028; DOE announcement https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers); S&P Global 451 Research (61.8 GW 2025 → 134.4 GW 2030)
- PJM: 2026/27 BRA cleared at cap $329.17/MW-day (https://insidelines.pjm.com/pjm-auction-procures-134311-mw-of-generation-resources-supply-responds-to-price-signal/); Dec 2025 auction (2027/28) at cap $333.44 (~$530 uncapped), third consecutive cap-clearing (https://insidelines.pjm.com/pjm-auction-procures-134479-mw-of-generation-resources/); IEEFA (data centers = 63% of 2025/26 increase, $9.3B); PJM market monitor (40% of $16.4B, Dec 2025 auction)
- TMI/Crane Clean Energy Center: Constellation–Microsoft 20-yr 835 MW PPA (Sept 2024); restart tracking H2 2027 (World Nuclear News, Utility Dive)
- State legislation: MultiState (300+ bills, 30+ states, first six weeks 2026), Good Jobs First (12 moratorium states; Maine LD 307 passed → vetoed Apr 24, 2026, override failed Apr 29; NY one-year moratorium passed, unsigned as of early July)
- Federal chip rules: BIS final rule (issued Jan 13, effective Jan 15, 2026); presidential proclamation (Jan 14, effective Jan 15, 2026) — 25% tariff on advanced AI chips not destined for US supply chain (Mayer Brown client alert)

## Current 8: The Political Economy of Displacement (new, July 2026)
- "Canaries in the Coal Mine": Brynjolfsson, Chandar & Chen (Stanford Digital Economy Lab / ADP; https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/) — Aug 2025 draft reported −13% for 22–25 in most-exposed occupations; Nov 2025 revision reports −16% (booklet now uses 16%), older cohorts grew; Canaries Dashboard (Apr 2026): decline accelerating 2.8%→3.8%/yr
- Stanford HAI AI Index 2026: ~20% decline in 22–25 software-dev employment since 2024
- NY WARN AI-attribution checkbox (rule from Mar 2025): 0 of 162 filings (~28,300 jobs) at ~11 months (TechBuzz)
- Challenger, Gray & Christmas: 87,714 AI-attributed cuts Jan–May 2026 vs 54,836 all of 2025 (NOTE: 150K+ figure circulating is total tech layoffs, not AI-attributed)
- OpenAI economic blueprint (Apr 6, 2026): robot tax, Public Wealth Fund, subsidized 4-day week (TechCrunch)
- RAISE US fund (launched Jun 25, 2026): $500M+ toward $1B; Raimondo/Holcomb; anchored by Amazon, Anthropic, Microsoft, OpenAI Foundation (TechTimes, Forbes)
- Gallup/Bentley: 75% of Americans expect AI to reduce jobs over next decade — survey fielded May 2023, published Sept 2023 (https://news.gallup.com/opinion/gallup/510635/three-four-americans-believe-reduce-jobs.aspx); booklet now dates it 2023 (previous "Aug 2025" dating was wrong)
- Robert's practice observations (author-note in Current 8, added Jul 3): covid-overhiring explanation is comfortable but doesn't explain within-firm age/exposure divergence; displacement timeline compressed vs prior tech waves (hyperscaler supply push × enterprise demand for automating creative office work)
- Labor actions: SAG-AFTRA 2023; Culinary Union tech-severance ($2,000/yr, Nov 2023); ILA port-automation contract (Jan 2025); ProPublica strike (Apr 8, 2026), NYT union letter (Apr 7), AP ULP complaint (Apr 6), Politico arbitration win (Dec 2025) — Poynter
- Bloomberg Law: "Nations are angling for ways to tax AI — defining how is elusive"

## Where I'd Put My Chips
- Author's own probabilities (Robert Barcik, July 2026), drafted with Claude Fable 5
- Bets 3 & 4 adopt/echo the mercantilism booklet's Bets 2 & 5

## Retired framings (changelog)
- "Scenario 4: Plateau + Regulation" → rebuilt as Current 5: From Lab to Production (May 2026); plateau sources (MMLU curves, Sutskever quotes, data-exhaustion projections) kept here for the record
- "Agentic Acceleration" → rebuilt as Current 6: Hours and Dollars (May 2026)

## 2026-08-16 — Slovak edition (Plánovanie scenárov pre generatívnu AI) at `/scenario-planning-sk/`

Translated entirely by Fable 5, meaning-first, via `_sources/_translation/segments.py`
(`scenario-planning.segments.txt` / `.segments.sk.txt` for the 720+ leaf segments plus
`scenario-planning.extra.sk.tsv` for the 49 JS/SVG string literals: legend labels, capex/model
data labels, dot-com timeline events, phase labels, "NOW" → "TERAZ", info-hint strings; the TSV
matcher also resolves `\uXXXX` escapes). Section ids and the decoder/current anchors unchanged;
JS verified with `node -e new Function(...)`. Terminology fixed in `GLOSSARY_SK.md` (prúdy,
Dekodér capexu, Denník spúšťačov, Spúšťacie signály, "Kam by som vsadil svoje žetóny", tag set
Spustené/Zatiaľ nie/Protisignál/Nabité/Potvrdené/Posunuté/Zvrat/Aktualizácia).
