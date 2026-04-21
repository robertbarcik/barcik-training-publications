# Chapter 3: The Cost Equation — API, Rental, and On-Prem Economics at Every Scale

This is the chapter where we stop talking in abstractions and start talking in euros. If you take away one thing from this booklet, it should be the numbers on these pages. They will either confirm your strategic direction or force you to change it.

Before we run the numbers, we need to be precise about what we are comparing. There are three distinct ways to run a production AI workload, and the economics of each are genuinely different. The previous edition of this chapter muddled two of them under a single "self-hosting" label; this one separates them. We will then walk through the full cost of each mode at four scales (10, 100, 500, and 1,000 users), compare them against each other and against commercial APIs, and — critically — show that for on-premises-required clients the comparison that matters is different again: your managed service versus the client doing it themselves.

---

## The Three Deployment Modes

Every AI workload runs in one of three modes. Pricing, capital structure, and operational burden differ substantially across them.

| Mode | One-line definition | Who owns the GPU | Who runs the model stack |
|---|---|---|---|
| **API consumption** | Pay per token to a commercial provider | The hyperscaler | The hyperscaler |
| **Rented dedicated inference** | Reserve GPU-hours from a cloud provider and run your own model on them | The cloud provider (AWS, GCP, Azure, Lambda, RunPod, CoreWeave) | You |
| **Owned on-prem inference** | Buy the hardware; install in your rack or a colo | You | You |

**API consumption** is the lowest-friction option — OpenAI, Anthropic, Google, and Mistral take your prompt and bill you per million tokens. You write zero infrastructure code.

**Rented dedicated inference** is what most teams mean when they casually say "self-hosting." You spin up an instance with attached H100s, deploy vLLM or TGI, load an open-weight model, and serve it. The physical GPU is someone else's capital; you are paying monthly (or hourly) for exclusive access.

**Owned on-prem inference** is the traditional IT model — purchase order, depreciation schedule, rack space, power contract, spare units in the storeroom. Nothing leaves your perimeter. Capital expenditure up front, lower operating cost per month after that.

A fourth mode — **local/edge inference**, where the model runs on an employee laptop — is the subject of Chapter 7 and has economics of its own. This chapter is about the three above.

When you read a table in this chapter, look at the label. Every cost table below is tagged with one of those three modes. That is the distinction the previous edition was missing.

---

## How We Are Modelling Usage

Every number that follows depends on a usage assumption. Every crossover point, every "this beats that" statement, every conclusion moves if the assumption changes. So let us make it explicit.

The baseline throughout this chapter is **one million tokens per user per day**, split in a 3:1 input-to-output ratio. That is a heavy-usage assumption appropriate for a knowledge worker who has integrated AI into their daily workflow — a developer using a coding assistant across the full day, an analyst running retrieval against large document sets, a consultant with a long-running agentic workflow summarising meetings and drafting outputs.

To orient yourself: 1M tokens is roughly 750 pages of English text per day per user, input and output combined. That sounds large until you count tool-using agents that re-read their own context on every turn, retrieval systems that stuff 30-40K tokens of context into every call, and the reality that output tokens are the tip of the iceberg in an agentic workload.

**Calibrate this to your clients.** If your population is lighter — casual chat, occasional summarisation, 100-300K tokens per user per day — all the API-side numbers in this chapter drop proportionally while the rental and owned numbers stay almost unchanged (fixed GPU cost does not shrink with lower utilisation). The practical effect: at 300K tokens/day, every crossover point between self-hosted and API moves roughly three times further to the right. Self-hosting for 300 users at light usage economically resembles self-hosting for 100 users at heavy usage.

Sample your own clients before committing to any of these tables. The 1M/day baseline is a defensible upper bound for knowledge-worker teams that have actually adopted AI; it is an overestimate for populations still in the pilot phase.

---

## API Pricing Landscape (April 2026)

Since every mode eventually gets compared against API pricing, we establish that first. Prices are per million tokens — input and output respectively.

### Frontier and Mid-Tier Model Pricing

| Provider | Model | Input (per M tokens) | Output (per M tokens) |
|---|---|---|---|
| **OpenAI** | GPT-4.1 | $2.00 | $8.00 |
| | GPT-4o | $2.50 | $10.00 |
| | GPT-4o-mini | $0.15 | $0.60 |
| **Anthropic** | Claude Haiku 4.5 | $1.00 | $5.00 |
| | Claude Sonnet 4.6 | $3.00 | $15.00 |
| | Claude Opus 4.6 | $5.00 | $25.00 |
| **Google** | Gemini Flash-Lite | $0.10 | $0.40 |
| | Gemini Flash | $0.30 | $2.50 |
| | Gemini Pro | $1.25 | $10.00 |
| **Mistral** | Small | $0.20 | $0.60 |
| | Medium | $1.00 | $3.00 |
| | Large | $2.00 | $6.00 |
| **Llama (hosted)** | 8B | $0.05 | $0.08 |
| | Maverick | $0.15 | $0.60 |
| | 70B | $0.70 | $0.90 |

Several patterns jump out of this table.

First, **the price floor keeps dropping**. Google's Flash-Lite at $0.10/$0.40 and Llama 8B at $0.05/$0.08 are nearly free for most business use cases. A year ago, these price points did not exist for models of comparable capability.

Second, **there is a 50-100x spread** between the cheapest and most expensive models. A Gemini Flash-Lite call costs roughly 1/50th of a Claude Opus 4.6 call. For most routine enterprise tasks — summarisation, classification, extraction, simple Q&A — the cheaper models are more than adequate.

Third, **output tokens are 3-5x more expensive than input tokens** across most providers. This matters for your cost modelling: a chatbot that produces long, detailed responses will cost significantly more than one that gives concise answers.

### API Cost at 100 Users — Worked Example

With our 1M-tokens-per-user-per-day baseline, 100 users generate roughly 3 billion tokens per month. At a 3:1 input-to-output ratio, here is the monthly cost across model tiers:

| Model Tier | Blended Rate (per M tokens) | Monthly Cost (3B tokens) | Per User |
|---|---|---|---|
| Gemini Flash-Lite | ~$0.18 | $540 | $5.40 |
| GPT-4o-mini | ~$0.30 | $900 | $9.00 |
| Llama 70B (hosted) | ~$0.75 | $2,250 | $22.50 |
| Mistral Medium | ~$1.50 | $4,500 | $45.00 |
| Claude Haiku 4.5 | ~$2.00 | $6,000 | $60.00 |
| GPT-4o | ~$4.40 | $13,200 | $132.00 |
| Claude Sonnet 4.6 | ~$6.00 | $18,000 | $180.00 |

Budget-tier usage at $5.40 per user per month is the benchmark every self-hosted deployment will struggle to beat on cost alone. Hold that number — we return to it repeatedly.

---

## GPU Rental Prices (April 2026)

These are the rates that drive the Rental mode math below. Prices vary significantly by provider, commitment level, and availability.

| GPU | Hourly Rate Range | Monthly Estimate (730 hrs) |
|---|---|---|
| NVIDIA H100 (80 GB) | $1.49 - $6.98 | $1,088 - $5,095 |
| NVIDIA H200 (141 GB) | $2.29 - $10.60 | $1,672 - $7,738 |
| NVIDIA A100 (80 GB) | $0.78 - $2.50 | $569 - $1,825 |
| NVIDIA A6000 (48 GB) | $0.50 - $1.20 | $365 - $876 |
| NVIDIA L40S (48 GB) | $0.60 - $1.80 | $438 - $1,314 |

The lower end of these ranges reflects spot pricing or long-term reservations with smaller GPU cloud providers (Lambda, RunPod, Vast.ai, CoreWeave). The higher end reflects on-demand pricing from the major hyperscalers (AWS, Azure, GCP). For production workloads requiring reliability and SLAs, budget toward the mid-to-upper range.

> **Key takeaway:** GPU rental prices have declined roughly 30-40% year-over-year as supply expanded, but they remain substantial. A single H100 at mid-range pricing ($2,500-$3,500/month) costs more per month than many traditional server configurations. This is GPU-as-a-premium-commodity, not GPU-as-a-utility.

---

## Mode B — Rented Dedicated Inference

This is the mode many teams think of first when they imagine "running a model ourselves." You reserve GPU capacity from a cloud provider, deploy an open-weight model, and serve it yourself. The economics are direct: monthly GPU rental plus operations overhead.

### Briefly: Why the 120B Frontier-Class Play Does Not Work

A full-precision 120B parameter model (Llama 3.1 405B quantised, Mistral Large, or similar) requires 3-4 nodes of 8xH100 to serve 100 concurrent users, with GPU rental alone running $30,000-$50,000 per month and a realistic all-in cost of $600-$1,000 per user per month once ops, observability, networking, and staff are included. Enterprise AI seats from the hyperscalers list at $20-$30 per user per month for standard tiers and up to $200 at the premium end. The math does not work — you would need a value proposition so compelling that customers pay 3-5x the going rate. For the overwhelming majority of IT services providers, frontier-class self-hosting in rental mode is not a business. We are not dwelling on it because it is a dead end; read on for the mode that does work.

### Rental: 20B Model at Four Scales

The realistic play is a smaller, more efficient model — 20B parameters or fewer. Models like Mistral Small, Llama 3.1 8B/70B (quantised), or domain-specific fine-tunes in the 7-20B range deliver strong performance on focused enterprise tasks while running on far less hardware.

#### Rental: 10 Users — Dedicated Per-Customer Deployment

The "private AI appliance" scenario in rental form. One customer, one deployment, full data isolation.

| Component | Monthly Cost |
|---|---|
| 1x A6000 or L40S (INT8 quantised) | $2,000 - $3,000 |
| Ops overhead (monitoring, support, patching) | $500 - $1,000 |
| **Total** | **$2,500 - $4,000** |
| **Per user** | **$250 - $400** |

#### Rental: 100 Users — Shared Departmental Deployment

| Component | Monthly Cost |
|---|---|
| 2x H100 (handling concurrency and throughput) | $5,000 - $8,000 |
| Ops overhead | $5,000 - $8,000 |
| **Total** | **$10,000 - $16,000** |
| **Per user** | **$100 - $160** |

At 100 users, operations overhead is roughly equal to compute. You need proper monitoring, a deployment pipeline, someone on call, and a process for model updates and security patches. The GPU may run itself, but the system around it does not. A note on the ops line: 100 users typically represents a newly-launched deployment in validation. Per-user ops is higher here than at 500 users because you are still hand-holding. At 500+ users the same ops capability is spread over more seats.

#### Rental: 500 Users — Business Unit or Mid-Size Enterprise

| Component | Monthly Cost |
|---|---|
| 2-3x H100 (with load balancing) | $7,500 - $12,000 |
| Ops overhead (share of dedicated team) | $3,500 - $6,000 |
| **Total** | **$11,000 - $18,000** |
| **Per user** | **$22 - $36** |

This is where self-hosting starts to become competitive. Utilisation improves dramatically with more users — 500 users generate enough traffic to keep GPU clusters reasonably busy throughout the business day. The per-user ops cost drops because you are spreading the same monitoring, support, and tooling across more seats.

#### Rental: 1,000 Users — Large Enterprise or Multi-Tenant Platform

| Component | Monthly Cost |
|---|---|
| 3-4x H100 (high-throughput serving) | $11,000 - $18,000 |
| Ops overhead (dedicated team) | $7,000 - $9,000 |
| **Total** | **$18,000 - $27,000** |
| **Per user** | **$18 - $27** |

At 1,000 users, the economics tilt decisively. You are now in the range where rental of a smaller model can undercut API pricing for mid-tier models — and you retain full data sovereignty. This is the sweet spot for providers who can aggregate demand across multiple clients.

### The Utilisation Headwind

Every number above assumes your rented GPUs run 24/7. They do — you pay for 730 hours per month whether your users are active or asleep. A dedicated 2x H100 cluster serving 100 users is likely at 30-40% average utilisation during business hours and near zero at night and on weekends. You are paying for 100% of capacity and using 30-40% of it.

Hyperscaler APIs flatten this curve across millions of geographically distributed users and run their fleets at 80-90%+ utilisation. The structural cost advantage this creates is one of the reasons API pricing can sit below what looks like a sensible floor — Chapter 4 explores the mechanics in detail.

---

## Mode C — Owned On-Prem Inference

This is the mode that receives shortest treatment in most write-ups and needs the most attention here, because for EU regulated-industry clients it is often the only viable architecture.

In owned mode, you (or your client) buy the GPU. Capital expenditure up front, then electricity, cooling, networking, colo or data-centre space, and staff. Amortised over a three-year accounting life, the compute line looks very different from rental.

### The Capex Reality: What the Hardware Actually Costs

From Chapter 2's hardware table, 2026 pricing:

| GPU | Purchase Price | VRAM | Typical Use |
|---|---|---|---|
| NVIDIA H100 80 GB (SXM) | $25,000 - $40,000 | 80 GB HBM3 | Production inference, 20B-70B models |
| NVIDIA H200 141 GB | $30,000 - $45,000 | 141 GB HBM3e | Larger models, higher throughput |
| NVIDIA A100 80 GB | $15,000 - $17,000 | 80 GB HBM2e | Previous gen, good price/performance |
| NVIDIA L40S | $7,000 - $10,000 | 48 GB GDDR6X | Inference-optimised, smaller models |

A server chassis, NVLink/NVSwitch interconnect, networking, PSU, and rack integration adds roughly 20-30% to the GPU cost per node. A 2xH100 inference node turnkey lands around $75,000-$95,000. Colo (if you are not racking in your own DC) runs $500-$1,500 per month for a single-node footprint including power and cooling.

### Owned: 20B Model at Four Scales

The same model sizing as the rental section, but pricing the hardware as owned capital on a 36-month amortisation. Ops costs are the same as rental — those are people and tooling, not hardware.

#### Owned: 10 Users — The Hardware Appliance

| Component | Cost |
|---|---|
| Upfront hardware (server + L40S + rack kit) | $10,000 - $15,000 (one-time) |
| Monthly amortisation (36 months) | $280 - $420 |
| Colo / power / cooling (if hosted) | $300 - $600 |
| Software license + remote support | $500 - $1,000 |
| **Monthly equivalent** | **$1,100 - $2,000** |
| **Per user** | **$110 - $200** |

The appliance model shifts the cost structure dramatically. The upfront capital expense is significant, but once amortised the ongoing per-user cost drops below rental. This works best for regulated industries where data must stay on-premises — healthcare, legal, financial services.

#### Owned: 100 Users — Shared Departmental Deployment

| Component | Monthly Cost |
|---|---|
| 2x H100 purchased (amortised 36 mo) | $1,700 - $2,400 |
| Server, networking, rack, spares buffer | $400 - $600 |
| Colo / power / cooling | $800 - $1,500 |
| Ops overhead | $5,000 - $8,000 |
| **Total** | **$7,900 - $12,500** |
| **Per user** | **$79 - $125** |

Compare this to rental at the same scale ($10,000-$16,000). The delta is not huge — roughly 20-30% — because ops dominates. But it matters, and the compute line itself is 3x cheaper owned than rented.

#### Owned: 500 Users — Business Unit Deployment

| Component | Monthly Cost |
|---|---|
| 3x H100 purchased (amortised 36 mo) | $2,500 - $3,600 |
| Server, networking, rack, spares buffer | $600 - $900 |
| Colo / power / cooling | $1,200 - $2,200 |
| Ops overhead (share of dedicated team) | $3,500 - $6,000 |
| **Total** | **$7,800 - $12,700** |
| **Per user** | **$16 - $25** |

At 500 users, owned is materially cheaper than rental and starts to undercut mid-tier API pricing ($60/user at Haiku / Mistral Medium rates). This is where the owned-hardware case becomes commercially compelling.

#### Owned: 1,000 Users — Large Enterprise or Multi-Tenant Platform

| Component | Monthly Cost |
|---|---|
| 4x H100 purchased (amortised 36 mo) | $3,300 - $4,800 |
| Server, networking, rack, spares buffer | $800 - $1,200 |
| Colo / power / cooling | $1,800 - $3,200 |
| Ops overhead (dedicated team) | $7,000 - $9,000 |
| **Total** | **$12,900 - $18,200** |
| **Per user** | **$13 - $18** |

At 1,000 users, owned hardware serving a 20B model lands around $13-18 per user per month — competitive with hosted Llama 70B API pricing and comfortably below anything mid-tier or frontier.

> **Key takeaway:** Owned on-prem is systematically cheaper than rental on the compute line (roughly 3x for long-lived deployments) because renting for 36 months costs as much as buying three of the same GPUs. The savings narrow once ops overhead is included — ops is the same either way — but the owned mode is the right choice whenever you have confidence the workload will persist for the amortisation window.

---

## Rent vs. Own: The Gap the Old Chapter Hid

Directly comparing the 100-user scenario across modes makes the gap visible:

| Line item | Rental | Owned (36 mo amortised) | Ratio |
|---|---|---|---|
| Compute | $5,000 - $8,000/mo | $1,700 - $2,400/mo | ~3x |
| Infrastructure (networking, colo, power) | bundled | $1,200 - $2,100/mo | — |
| Ops overhead | $5,000 - $8,000/mo | $5,000 - $8,000/mo | 1x |
| **Total** | **$10,000 - $16,000** | **$7,900 - $12,500** | **~1.3x** |

Three questions determine which mode fits a given client:

1. **How long will this workload run?** Amortised purchase is cheaper only if you use the hardware for at least 24-30 months. For pilots, proofs of concept, or workloads with uncertain longevity, rental is correct even at premium prices.
2. **Who owns the capital risk?** Owned hardware is a depreciating asset. If GPU prices drop 30% next year (they did this year), your $60,000 cluster is worth $42,000 on the used market. Rental has no residual-value risk.
3. **Does the client require physical control of the hardware?** Banks, defence contractors, classified environments, and some hospital systems have policies that rule out shared cloud infrastructure entirely — even "dedicated" rental. These clients are owned-mode by default.

For everything else, the decision is an economic one: pay 30% more each month for the flexibility to turn it off, or commit capital and capture the 3x compute saving.

---

## Hardware Lifetime and Refresh Economics

Every owned-hardware calculation in this chapter uses a 36-month amortisation. That is the standard accounting convention. It is also, in practice, an incomplete picture. If you are advising a client on an owned-hardware AI deployment, you owe them a more honest view of the hardware lifetime question.

**Nvidia's published service life** for its data-centre GPUs is three to five years. Both numbers are correct depending on what you mean. Three years is the point at which the GPU has depreciated to zero on a typical corporate books and is eligible for refresh. Five years is the point at which the hardware itself typically starts showing failures under continuous load — fan wear, thermal paste degradation, HBM memory errors climbing above acceptable thresholds.

**Inference is gentler than training.** Most of the public failure data on large GPU fleets comes from training workloads, where GPUs run at sustained 95%+ utilisation for weeks at a time and failure rates of several percent per 10,000-GPU fleet per month have been publicly documented. Inference loads are bursty and thermally less punishing. Real-world failure rates for a well-cooled inference fleet are lower, but they are not zero — budget a small spare-unit reserve (one extra GPU per 8-10 production units) and an RMA process that does not require taking the service offline.

**Accounting life, physical life, and useful life are three different numbers.**

- Accounting life (36 months) governs depreciation on the client's balance sheet.
- Physical life (often 5+ years) governs when the hardware actually fails.
- Useful life — the one that matters for strategy — is typically governed by technology obsolescence, not by hardware failure. The H100 is being displaced by the H200 which is being displaced by Blackwell. In 36 months, today's H100s will still work. They will also be competing against hardware that is 2-3x faster at the same power envelope, running models that are more efficient on newer architectures. Your client will probably refresh before the hardware fails.

**What this means for TCO modelling:**

1. **Budget a replacement cycle.** Do not promise a client "36 months and the hardware is free." Promise 36 months to full amortisation, with a refresh decision at month 30 based on what newer silicon is capable of by then.
2. **Reserve spare units.** One extra GPU per rack is cheap insurance against the RMA timeline on replacements, which can stretch to weeks for in-demand SKUs.
3. **Consider the used-hardware market.** H100s from decommissioned training fleets have been entering the secondary market in increasing volumes since mid-2025, typically at 40-60% of MSRP. For clients who need capacity but not leading-edge performance, this can cut capex in half.
4. **Plan for progressive quantisation.** The same GPU hardware will run better-quantised versions of the same models over time as quantisation research advances. A 20B model that needs 40GB of VRAM at INT8 today may run at comparable quality on 20GB at INT4 in 18 months. Your owned cluster grows in effective capacity without any hardware change.

The consumer-hardware analog matters for Chapter 7, where the same refresh-and-depreciation dynamics apply to corporate laptops running local models — but the economics are still favourable because the client already owns the laptops.

---

## The Unified Comparison

The table every IT services provider should have on their wall: the same 20B model workload across all three modes, at all four scales, compared against the three API tiers.

### Monthly Total Cost — Three Modes, Four Scales

| Scale | API Budget | API Mid | API Frontier | Rental 20B | Owned 20B |
|---|---|---|---|---|---|
| 10 users | $54 | $600 | $1,800 | $2,500 - $4,000 | $1,100 - $2,000 |
| 100 users | $540 | $6,000 | $18,000 | $10,000 - $16,000 | $7,900 - $12,500 |
| 500 users | $2,700 | $30,000 | $90,000 | $11,000 - $18,000 | $7,800 - $12,700 |
| 1,000 users | $5,400 | $60,000 | $180,000 | $18,000 - $27,000 | $12,900 - $18,200 |

*Budget tier: Gemini Flash-Lite / GPT-4o-mini class (~$0.18-$0.30/M blended). Mid tier: Claude Haiku / Mistral Medium class (~$2.00/M blended). Frontier: Claude Sonnet / GPT-4o class (~$6.00/M blended). Assumes 1M tokens/user/day.*

### Per-User Monthly Cost — Three Modes, Four Scales

| Scale | API Budget | API Mid | API Frontier | Rental 20B | Owned 20B |
|---|---|---|---|---|---|
| 10 users | $5.40 | $60 | $180 | $250 - $400 | $110 - $200 |
| 100 users | $5.40 | $60 | $180 | $100 - $160 | $79 - $125 |
| 500 users | $5.40 | $60 | $180 | $22 - $36 | $16 - $25 |
| 1,000 users | $5.40 | $60 | $180 | $18 - $27 | $13 - $18 |

API pricing is perfectly linear — the per-user cost does not change with scale. Self-hosted costs (both rental and owned) drop dramatically as you add users. The crossover points depend on which API tier you are comparing against and which self-hosted mode.

### Crossover Points

| Comparison | Crossover Point |
|---|---|
| Rental 20B vs Budget API (Flash-Lite, 4o-mini) | **Never** (rental is always more expensive) |
| Owned 20B vs Budget API | **Never** (ops overhead floor exceeds budget API) |
| Rental 20B vs Mid-tier API (Haiku, Mistral Medium) | **~400-500 users** |
| Owned 20B vs Mid-tier API | **~250-350 users** |
| Rental 20B vs Frontier API (Sonnet, GPT-4o) | **~100-200 users** |
| Owned 20B vs Frontier API | **~50-100 users** |
| Rental 20B vs Premium API (Opus, GPT-4.1 + heavy usage) | **~50-80 users** |
| Owned 20B vs Premium API | **~30-50 users** |

Owning hardware shifts every crossover earlier by a factor of roughly 1.5-2x compared to renting. For a client committed to the workload, this is the difference between self-hosting being viable at 150 users rather than 300.

---

## What These Numbers Do Not Capture

Before drawing strategic conclusions from the table above, the caveats.

**Factors favouring APIs:**

- Zero setup time — you can be live in hours, not weeks
- Automatic model upgrades — when a frontier model improves, you get it free
- Elastic scaling — pay nothing during weekends and holidays
- No GPU procurement risk — you never own depreciating hardware
- No failure exposure — the hyperscaler replaces GPUs transparently

**Factors favouring rental:**

- Full stack control without capital commitment
- Data sovereignty to the extent the provider's data-processing agreement allows it
- Ability to run open-weight or fine-tuned models the hyperscalers do not offer
- Predictable monthly cost, no surprise bills from a prompt injection or runaway agent
- Independence from model deprecation or API terms changes

**Factors favouring owned on-prem:**

- True data sovereignty — tokens never leave your perimeter
- Compliance with the strictest EU regulatory requirements for regulated industries
- Full hardware control, including air-gapped deployments
- Lower long-run compute cost (3x on the compute line)
- Unlimited usage against a fixed cost — no per-token pressure on adoption
- Predictable refresh cycle you control

For EU IT services providers, the data sovereignty and compliance arguments are often the strongest justification for owned on-prem. The cost math alone rarely supports rental over API for cloud-comfortable clients, but combine cost with a genuine compliance requirement and owned on-prem starts to look like the right answer for a meaningful share of the market.

> **Key takeaway:** Do not build your business case on cost savings from self-hosting against APIs. For cloud-comfortable clients, you will lose that argument. Build the case on data sovereignty, regulatory compliance, and customisation — and use these numbers to know exactly what premium you are asking the client to pay, and why that premium is worth it.

---

## The On-Premises Economics: A Different Comparison Entirely

Everything above compares the three modes against each other and against API pricing. That is the right framing for clients who have a choice. For a significant segment of the EU enterprise market — banking, healthcare, defence, legal, public sector, and any organisation whose compliance or legal team has ruled out external AI APIs — API pricing is irrelevant. It is not an option they can select.

For these clients, the comparison that matters is different:

- **Your managed owned on-prem service** vs. **the client building and running it themselves**
- **Your managed owned on-prem service** vs. **the client having no AI at all**

This is traditional IT managed-services economics, and the numbers look much more favourable.

### What It Costs a Client to Do It Themselves

Consider a mid-sized European bank that wants to run a 20B model on-premises for 100 internal users. If the bank builds and manages the infrastructure itself, it needs:

| Cost Component | Annual Cost |
|---|---|
| GPU hardware (2x H100, amortised over 3 years) | $17,000 - $23,000 |
| Server infrastructure, networking, cooling | $8,000 - $12,000 |
| ML engineer (1 FTE, EU market) | $80,000 - $130,000 |
| DevOps/infrastructure engineer (0.5 FTE) | $30,000 - $50,000 |
| Software licensing, monitoring, security tools | $10,000 - $20,000 |
| Training and upskilling | $5,000 - $10,000 |
| **Total annual cost (client DIY)** | **$150,000 - $245,000** |
| **Monthly equivalent** | **$12,500 - $20,400** |
| **Per user per month** | **$125 - $204** |

The dominant cost is not hardware — it is people. An ML engineer who can deploy, optimise, and maintain LLM inference infrastructure commands a significant salary in the EU market, and the client needs at least one full-time. Many will need more, especially during the initial setup phase.

Notice the gap with the $79-125 per-user number from the owned-hardware table above. The same hardware, the same model, the same scale — but $79-125 when you (the IT services provider) run it, and $125-204 when the client runs it alone. That gap is your margin opportunity, and it is structural.

### What You Can Charge as a Managed Service

As an IT services provider, you have advantages the individual client does not:

- **Shared expertise.** Your ML engineer serves multiple clients, not one. The cost is spread across your customer base.
- **Reusable tooling.** Your deployment pipelines, monitoring dashboards, and update processes are built once and used for every client.
- **Operational maturity.** You have been managing infrastructure for decades. The client's newly-hired ML engineer is figuring it out for the first time.
- **Vendor relationships.** You negotiate GPU procurement and cloud pricing at volume.

These advantages let you deliver the same service at a lower cost than the client can achieve alone — the same economics that made traditional IT managed services profitable.

| Deployment Scale | Your Cost | You Charge | Client DIY Cost | Your Margin |
|---|---|---|---|---|
| 10 users (dedicated) | $2,500 - $4,000/mo | $5,000 - $8,000/mo | $7,000 - $12,000/mo | 40-55% |
| 100 users (shared infra) | $10,000 - $16,000/mo | $18,000 - $28,000/mo | $12,500 - $20,400/mo | 40-50% |
| 500 users (platform) | $11,000 - $18,000/mo | $22,000 - $35,000/mo | $20,000 - $35,000/mo | 45-55% |

*The "Your Cost" column uses rental-mode pricing from Mode B. If you run owned hardware, your costs drop further (see the Mode C tables) and margins improve accordingly.*

At 10 users, the economics are especially compelling. A small client cannot justify a full-time ML engineer for 10 users, but they still need someone to manage the infrastructure. Your shared-expertise model gives them enterprise-grade AI ops at a fraction of the cost of doing it themselves.

At 100 users, you price competitively with the client's DIY cost while capturing a healthy margin. The client gets operational reliability, SLAs, and the ability to focus their internal team on using AI rather than running it.

At 500+ users, the client starts to have enough scale to justify their own team — but even then, your platform approach (serving multiple clients on shared infrastructure, with isolated data) can remain cost-competitive.

> **Key takeaway:** For on-prem-required clients, your competition is not OpenAI or Google. It is the client's internal IT team. And you beat internal IT teams the same way you always have: through operational specialisation, shared costs across multiple clients, and mature tooling. The margin structure looks like traditional managed services — 40-55% — not the razor-thin margins of trying to compete with hyperscaler API pricing.

### The Market Size Question

How large is the on-prem segment? No published data answers this precisely for GenAI specifically, but several indicators suggest it is substantial in the EU market:

- **Banking and financial services:** ECB and national regulators increasingly scrutinise cloud concentration risk. Many EU banks maintain strict policies requiring sensitive data processing on-premises or in private cloud.
- **Healthcare:** Patient data under GDPR has stringent processing requirements. Many EU healthcare systems have explicit policies against external AI APIs for clinical data.
- **Public sector:** Government organisations across EU member states frequently require on-premises or sovereign cloud deployment for sensitive workloads.
- **Legal:** Attorney-client privilege and professional confidentiality obligations create strong incentives for on-prem AI.
- **Defence and critical infrastructure:** By definition, these sectors require controlled environments.

For a typical EU IT services provider whose client base skews toward regulated industries, the on-prem segment could represent 30-60% of potential AI service revenue. This is not a niche — it may be the core market.

### The Combined Picture

The reality for most EU IT services providers is that they will serve both segments simultaneously:

| Client Segment | Your Role | Revenue Model | Margin |
|---|---|---|---|
| On-prem required | Managed AI infrastructure provider | Monthly retainer + per-user fees | 40-55% |
| Cloud-comfortable | AI solutions integrator | Project fees + API passthrough + support | 25-40% |
| Both | Compliance and evaluation overlay | Assessment fees + monitoring retainer | 50-65% |

The healthiest business combines all three: infrastructure margins from on-prem clients, integration and advisory revenue from cloud-comfortable clients, and compliance services layered across both. Do not make the mistake of focusing exclusively on one segment when the other may be equally or more lucrative.

---

## Practical Implications for Your Pricing Strategy

These numbers lead to four immediate conclusions for how you should think about pricing:

**1. Do not try to undercut API providers on price.** You will lose. OpenAI, Google, and Anthropic are spending billions on custom silicon and infrastructure. Your cost per token will always be higher than theirs for equivalent model quality.

**2. For on-prem clients, price against the client's DIY cost — not against API pricing.** A managed AI infrastructure service at $180 per user per month is expensive compared to a $5.40 per user per month API call, but it is a bargain compared to the $125-$204 per user per month it would cost the client to build and staff it themselves. Frame your pricing against the right benchmark.

**3. Price on value, not on cost-plus.** If your service provides data sovereignty, compliance assurance, or specialised fine-tuning, price those outcomes directly. A $180/user/month service that keeps patient data on-premises is a different product from a $5.40/user/month API call that sends data to US servers.

**4. Consider hybrid architectures.** Route sensitive queries through your owned infrastructure and non-sensitive queries through cheap APIs. This keeps your GPU utilisation high on the work that actually requires privacy, while keeping costs down on everything else. We explore this model in detail in Chapter 5, and Chapter 7 extends the logic further to local-on-device inference — which, for workloads that fit, produces compute costs of literally zero.

The numbers tell two stories. For cloud-comfortable clients, the strategy is not about running models cheaper than the hyperscalers — it is about delivering expertise, integration, and compliance on top of their APIs. For on-prem-required clients, you are still in the infrastructure business, and the economics work in your favour — as long as you price against the right comparison and commit to the amortisation window that makes owned hardware viable.

---

> **Freshness Watch** · *verified April 2026 · estimated half-life: ~4 months*
>
> This chapter contains the booklet's most time-sensitive numbers. Claims most likely to shift within 3-6 months:
>
> - The **API pricing table** — every provider listed changes prices at least once per quarter, and the overall trend is downward. Re-verify Gemini Flash-Lite, GPT-4o-mini, Claude Haiku, and Llama 70B quotes before quoting to a client.
> - **GPU rental rates** — hyperscaler and neocloud spot markets move monthly. H100 pricing specifically has been tracking down 2-4% per month.
> - **Named model versions** (GPT-4.1, Claude Sonnet 4.6, Gemini Flash-Lite, Llama 3.1 70B) — new releases typically ship every 2-4 months and may rename, reprice, or supersede these entries.
> - The **crossover points** flow directly from the pricing tables; they move whenever either side moves.
>
> What should hold up longer: the three-mode framing, the rent-vs-own gap (~3x on compute), the shape of the scale curve (owned beats rental which beats API at different user counts), and the on-prem market economics. If you are reading this more than six months after the date above, treat every specific dollar figure as directional, but the structural argument should still track.

---

*Chapter 4 examines why the API side of the comparison is not just cheaper today but structurally cheaper — and what that means for any strategy built on competing with the hyperscalers on price.*
