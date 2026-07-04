# Open-Weight Model Families & Model Selection — update log

Working notes for the booklet at `/open-weight-models/`. This publication is HTML-only (no markdown sources, no build script): edit `open-weight-models/index.html` directly. The deployed page and the repo file were verified byte-identical before the July 2026 pass, so there is no hand-patch drift to fold in.

Build/verify facts:
- Anchors: 13 `<section class="chapter" id="…">` slugs (cover, intro, families-overview, family-profiles, beyond-llms, hardware-reality, what-fits, quantization, inference-frameworks, throughput, decision-framework, exercise, watch-signals). Sidebar nav + IntersectionObserver depend on them; keep them stable.
- Sanctioned em dashes: exactly 4 `<td>&mdash;</td>` empty cells in the throughput table. Everything else must be 0.
- Interactive bits: toggle panels (scenario reveals) via `togglePanel()`; print CSS forces panels open.

## 2026-07-04 — July 2026 editorial pass (with Claude / Fable 5)

Kept brief per the booklet's own "brief and fresh" brief. Two independent Sonnet web fact-checks grounded the corrections.

- **Voice sweep**: 100 em dashes → 4 (the sanctioned empty table cells); family-card h3 titles and step/risk labels de-dashed to `·`; "It is not X. It is Y." constructions rewritten (intro comparison-tables paragraph, Phi card).
- **Factual corrections**: DeepSeek was never Apache 2.0 (V3 custom license, R1 onward MIT); GPT-OSS-120B is 117B total / 5.1B active (was "20B active", which is the sibling model's name); SGLang "29% faster than vLLM" and "vLLM powers Stripe/Meta/Mistral" replaced (no traceable primary sources) with workload-dependent language + PyTorch Foundation backing; Gated DeltaNet attributed to Qwen3-Next (Sept 2025), not Qwen 3.5; Alibaba AI growth 11 consecutive quarters (May 2026 earnings), not 8; TGI archived March 2026, not just maintenance mode; H100 3.35 TB/s qualified as SXM (PCIe ≈2 TB/s); Phi speech-leaderboard claim date-stamped; Devstral 2 is modified MIT with the revenue gate; "six weeks mean engagement" attributed to HuggingFace's State of Open Source Spring 2026 report; Mistral Large 3 (Dec 2025, 675B/41B, Apache 2.0) added to the Mistral card.
- **New: challengers family card** (Part 1, after Phi): DeepSeek (V4 preview Apr 2026, MIT), GLM/Zhipu (GLM-5.2 Jun 2026, #1 open-weight), Kimi/Moonshot (K2.6/K2.7, modified MIT), GPT-OSS (117B/5.1B active, Apache 2.0, single-80GB-GPU). Landscape chapter stat card now "5 + 4 core families + challenger tier"; licensing table gained DeepSeek, GPT-OSS, GLM·Kimi rows.
- **New: "A July 2026 Reading"** (What to Watch): which of the booklet's own re-evaluation signals fired April→July (new-family signal ×3; licensing signal ×2 toward closed — Muse Spark proprietary, Qwen 3.7-Max closed; the unnamed signal: gated frontier access makes open weights the ungateable tier; DGX Station GB300 + RTX 5090 hardware notes; TGI archiving). Cover date line and footer now carry "first freshness reading July 2026". Same instrument as the trigger logs / indicator readings in the other booklets.
- **Cross-links added**: intro → `/token-economics/` (whether to self-host at all); Llama card + July reading → `/mercantilism-of-genai/#m-open`; July reading → `/mercantilism-of-genai/#m-bloc`.
- **Scoping sentence** added to The Hardware Reality naming the three-target choice (H100/H200/Spark) and pointing other hardware owners at the formulas.

Verified: 13 section ids unchanged, all `#` hrefs resolve, cross-booklet fragments exist, tag balance clean.
