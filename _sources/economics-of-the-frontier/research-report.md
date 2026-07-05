# The Economics of the Frontier — Research Report (canonical source)

> Snapshot: May 2026. This is the research dump that the booklet
> `economics-of-the-frontier/index.html` is built from. All figures are as of
> the dates noted. Treat run-rate figures as ~12× a single month, not GAAP.

> **July 2026 corrections (see `notes.md` for the full revision log):**
> three items below were wrong or misdated and are corrected in the deployed booklet:
> (1) Nvidia's "up to $100B" OpenAI investment was a non-binding LOI, never finalised;
> what closed (Mar 2026) was **$30B** inside the $122B round.
> (2) Zhipu/MiniMax HK IPO-day valuations were **~$7.1B / ~$6.5B** (Jan 8, 2026), not ~$56B/~$33B;
> those larger numbers only appeared after the June 2026 rally (Zhipu ~$63B peak, MiniMax ~$16B).
> (3) The WSJ $74B-loss/2028 reporting dates to **Nov 2025**, not May 2026.
> Also superseded: $30B run rate → $47B (late May); Series G $380B → Series H $65B at $965B + confidential S-1 (Jun 1).

## TL;DR

- Anthropic's per-model profitability framing is largely supported by the math, but the
  company-level "first profitable quarter" projected for Q2 2026 (~$10.9B revenue, $559M
  operating profit per WSJ) is a transient peak; scheduled compute ramps in H2 2026 will
  likely push it back into loss. OpenAI is on a fundamentally different trajectory —
  confidential financials reviewed by the WSJ show losses widening to ~$74–85B in 2028 and
  breakeven pushed to 2030, against Anthropic's projected free-cash-flow positive 2027.
- Inference economics have inflected. Anthropic's gross margin moved from −94% in 2024 to a
  projected 40% in 2025 and 77% by 2028; OpenAI's compute margin reached ~70% on frontier
  models, but the commoditized tier (Haiku, GPT-4o mini, open-weights replacements) carries
  margins below 20%, per SemiAnalysis. Anthropic now earns roughly $211 per monthly user vs.
  OpenAI's ~$25 per weekly user — an 8× monetization gap driven by enterprise concentration.
- The reported financials at both labs are heavily distorted by hyperscaler arrangements —
  Microsoft's restructured 27% / $135B equity stake and 20% revenue share capped at $38B;
  Amazon's $13B in cumulative Anthropic investment plus a $100B+ Anthropic commitment back to
  AWS over a decade; Google's up-to-$40B Anthropic commitment paired with a $200B 5-year
  Anthropic-to-Google-Cloud purchase; Oracle's reported $300B 5-year OpenAI compute deal.
  These are circular: investors' equity dollars largely flow back to themselves as revenue.

## Key findings (condensed)

1. Anthropic run-rate revenue: $1B (Jan 2025) → $9B (year-end 2025) → $14B (Feb 2026) →
   $19B (Mar) → $30B (Apr 2026), company-confirmed. OpenAI ~$24B annualized ($2B monthly,
   CFO Sarah Friar). OpenAI disputes Anthropic's figure (leaked Apr 13 memo from CRO Denise
   Dresser: Anthropic overstates by ~$8B by booking AWS/Google Cloud reseller revenue gross).
2. Dario Amodei's "each model is profitable, the company isn't" framing (Feb 2026 Dwarkesh
   Patel interview; Cheeky Pint with John Collison): a $100M 2023 model earns $200M; a $1B
   2024 model earns $2B; a $10B model trains for next year. Per-vintage each model returns
   ~2× training cost; conventional P&L shows accelerating losses.
3. Amodei's 50% compute-on-research heuristic: "spending 50% of your compute on research,
   roughly, plus a gross margin higher than 50% and correct demand prediction leads to
   profit." Stylized, not Anthropic's actual operating ratio.
4. Both labs capacity-constrained. Amodei at Code with Claude (May 6, 2026): planned for 10×
   growth, saw 80×. May 2026: Anthropic leased the entirety of xAI's Colossus 1 in Memphis
   (~220,000 GPUs, 300+ MW) at a reported $1.25B/month for inference for Claude Pro/Max.
5. Inference gross margins bifurcating: SemiAnalysis — frontier models >70%, trailing models
   with open-source competition <20%. Anthropic's inference gross margin moved ~38% → >70%
   inside a year.
6. Hyperscaler distortions structural. Microsoft restructured deal (Oct 2025): 27% / $135B
   equity, 20% revenue share capped at $38B through 2030. OpenAI contracted $250B Azure +
   reported $300B Oracle Stargate.
7. Mistral ~$400M ARR (Jan 2026), up from ~$16M end-2024. Sept 2025 €1.7B Series C led by
   ASML (largest shareholder ~11%) at €11.7B. Mar 2026 $830M debt facility for 13,800 Nvidia
   chips. ~75× smaller than Anthropic.
8. Chinese labs: DeepSeek V3 reported $5.58M marginal training cost (all-in $51M+); R1 RL
   post-training $294K. Dominant players (Qwen, GLM, Kimi, MiniMax, Ernie, Doubao) pursue
   user-traffic/ecosystem monetization, not pure API economics. Zhipu IPO'd in HK ~$56B;
   MiniMax ~$33B.
9. Forward projections (internal, investor-facing — optimistic): Anthropic $70B revenue /
   $17B cash flow 2028, 77% gross margin. OpenAI $200B revenue by 2030, $115B cumulative
   burn through 2029, $74B operating loss 2028. FutureSearch median OpenAI mid-2027 ARR
   $39B, 80% CI [$11B, $70B].
10. Bear case (Ed Zitron) right about the math, wrong about trajectory: Anthropic −94% gross
    margin 2024 was real; OpenAI Q3 2025 ~$12B loss (Microsoft FY26 Q1 10-Q equity-method
    line) is real accounting. But the 2025–26 inference margin inflection was also real.

## Detail dump

(Full detail — Anthropic, OpenAI, Mistral, Chinese labs, hyperscaler economics, compute
allocation, frontier vs commoditized tier, bear case, bull case — is preserved in the
original conversation that produced this report. Key numbers reproduced above. The booklet
uses these figures with `reported` / `projected` / `estimated` provenance tags and numbered
endnotes; see `references.md` for the source-URL list.)

### Anthropic
- Revenue run-rate: Jan 2024 $87M → Dec 2024 $1B → end-2025 $9B → Feb 2026 $14B → Mar $19B
  → Apr 2026 $30B (confirmed).
- ~80% enterprise revenue; 100,000+ business customers (AWS Bedrock, Apr 2026); customers
  >$1M/year doubled ~500 → >1,000 in eight weeks (Feb–Apr 2026).
- Claude Code: $1B run-rate in 6 months (Dec 3, 2025 press release); $2.5B by Feb 2026.
- Funding: Mar 2025 $61.5B (Series E); Sep 2025 $183B (Series F, $13B); Feb 2026 $380B
  post-money (Series G, $30B); May 2026 talks at >$900B pre-money. Bloomberg: Oct 2026 IPO.
- Gross margin: −94% on paying customers / −109% all-in (2024, The Information). 2025
  projection lowered 50% → 40% (inference costs ran 23% over budget). Internal: 77% by 2028.
- WSJ (May 20, 2026): Q2 2026 revenue $10.9B, $559M first operating profit; may not last
  through the year due to H2 2026 compute costs.

### OpenAI
- Revenue: 2023 ~$2B; 2024 ~$6B ($3.7B GAAP); 2025 $20B ARR exit / $13B GAAP; Apr 2026 $24B
  annualized ($2B/month). $122B raise at $852B valuation.
- 9M paying business users (Feb 2026); 900M+ weekly active ChatGPT users; 50M+ paying subs;
  API >15B tokens/min; Codex 2M+ weekly users.
- Losses: 2024 net loss ~$5B; 2025 ~$22B spend vs $13B sales (~$9B net loss). Microsoft FY26
  Q1 10-Q implies OpenAI Q3 2025 net loss ~$11.5–12B. WSJ: $74B operating loss 2028, $115B
  cumulative burn through 2029, breakeven 2029–2030.
- Altman (Aug 14, 2025): "We're profitable on inference. If we didn't pay for training, we'd
  be a very profitable company."
- Oct 28, 2025 recapitalization: Foundation 26% / ~$130B; Microsoft 27% / ~$135B; employees
  + investors 47%. Microsoft revenue share 20% capped $38B through 2030; IP license to 2032.

### Mistral
- Sacra: $400M ARR Jan 2026, $312M Dec 2025, $16M end-2024. 60% revenue from Europe.
- Sept 2025 €1.7B Series C, ASML largest shareholder ~11%, €11.7B post-money.
- Mar 2026 $830M debt facility (7 banks incl. Bpifrance) for 13,800 Nvidia chips, Paris DC.
- Strategy: La Plateforme, Le Chat, Forge (on-prem), Mistral Compute, Koyeb acquisition,
  vertical models (European bank cybersecurity).

### Chinese labs
- DeepSeek V3: 2,048 H800 GPUs ~2 months, $5.58M marginal; all-in ≥$51M GPU cluster. R1
  $294K RL post-training. Claimed 545% inference cost-profit ratio (theoretical).
- Moonshot K2 Thinking: ~$4.6M training; $0.60/$2.50 per MTok. Alibaba 36% stake.
- Zhipu IPO HK ~$56B; MiniMax ~$33B. Model: traffic/ecosystem monetization, not API margin.

### Hyperscaler economics
- Amazon–Anthropic: $4B (Sep 2023) + $4B (Nov 2024) + $5B (Nov 2025, up to $20B more on
  milestones) = ~$13–33B. Anthropic committed $100B+ over 10 years on AWS Trainium. Project
  Rainier ~500K Trainium2 → 1M+ by end-2025.
- Google–Anthropic: $3B prior; Apr 2026 up to $40B ($10B initial, $30B contingent).
  Anthropic committed $200B over 5 years to Google Cloud (~$40B/yr), 5GW capacity.
- Microsoft–OpenAI: $13.75B cumulative invested; post-restructuring 27% / $135B; OpenAI
  committed $250B incremental Azure.
- Oracle–OpenAI: reported $300B over 5 years from 2027; 4.5GW Stargate. Oracle RPO $455B →
  $523B. Moody's flagged leverage approaching 4× EBITDA.
- Nvidia: $100B "investment" in OpenAI structured as progressive disbursement contingent on
  OpenAI building $125B of data centers using $200B of Nvidia GPUs.

### Bull / bear
- Bear (Zitron): reported revenue doesn't align with cash disclosures; OpenAI burned $13.7B
  2023–H1 2025; Microsoft 10-Q $12B Q3 2025 loss is real; Stargate/Nvidia/Oracle deals
  circular; Anthropic −94% 2024 gross margin.
- Bear (Marcus): scaling hitting diminishing returns; per-vintage story collapses if
  capability gains go sub-linear.
- Bull (Cahn/Sequoia): the "$600B question" predicts value reallocation from infra to apps,
  not refutation. SemiAnalysis Dec 2025: "Agentic AI began to really work."
