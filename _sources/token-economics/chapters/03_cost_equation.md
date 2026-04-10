# Chapter 3: The Cost Equation — Self-Hosting vs API at Every Scale

This is the chapter where we stop talking in abstractions and start talking in euros. If you take away one thing from this booklet, it should be the numbers on these pages. They will either confirm your strategic direction or force you to change it.

We will walk through the full cost of self-hosting large language models at different scales, compare those costs against current API pricing, and — critically — show you that the right comparison depends on which clients you serve. For cloud-comfortable clients, the API comparison is what matters. For on-premises-required clients, the comparison that matters is entirely different: your managed service versus the client doing it themselves. Both economics are covered in this chapter.

---

## Self-Hosting a 120B Parameter Model (100 Users)

Let us start with the scenario many IT services providers instinctively imagine: hosting a large, frontier-class open-weight model for a mid-size enterprise client. Something like Llama 3.1 405B quantized to fit, or a full-precision 120B parameter model such as Mistral Large or a fine-tuned derivative.

### Compute Requirements

A 120B parameter model at FP16 requires roughly 240 GB of GPU VRAM just for the weights. Add KV-cache for concurrent users, activation memory, and operational headroom, and you need 3 to 4 nodes of 8xH100 (80 GB each) to serve 100 concurrent users with acceptable latency.

### The Monthly Bill

| Cost Component | Monthly Estimate |
|---|---|
| GPU cloud rental (3-4 nodes, 8xH100 each) | $30,000 - $50,000 |
| Networking and storage | $1,500 - $3,000 |
| Monitoring and observability | $1,000 - $2,000 |
| DevOps / ML engineering staff (fractional) | $8,000 - $15,000 |
| On-call and incident management | $3,000 - $5,000 |
| Application hosting (API gateway, auth, logging) | $2,000 - $4,000 |
| Security and compliance overhead | $2,000 - $4,000 |
| **Total monthly cost** | **$47,500 - $83,000** |

### Per-User Reality

| Metric | Value |
|---|---|
| Raw compute per user | $300 - $500/month |
| Compute + operations per user | $475 - $830/month |
| Realistic all-in per user | **$600 - $1,000/month** |

The "realistic all-in" figure includes a margin buffer, amortized setup costs, and the inevitable underutilization during off-peak hours. GPU clusters do not scale to zero.

> **Key takeaway:** At $600-1,000 per user per month, a self-hosted 120B model is essentially unsellable. Enterprise AI seats from OpenAI, Anthropic, and Google run $20-30 per user per month for standard tiers and $200 per seat for the most premium enterprise packages. You cannot compete on price. You would need to sell on a value proposition so compelling that customers pay 3-5x the market rate. For most IT services providers, this is not a viable business.

---

## Self-Hosting a 20B Parameter Model at Different Scales

The more realistic play for an IT services provider is a smaller, more efficient model — 20B parameters or fewer. Models like Mistral Small, Llama 3.1 8B/70B (quantized), or domain-specific fine-tunes in the 7-20B range. These models can deliver strong performance on focused enterprise tasks while running on significantly less hardware.

### 10 Users — Dedicated Per-Customer Deployment

This is the "private AI appliance" scenario. One customer, one deployment, full data isolation.

**Cloud option:**

| Component | Monthly Cost |
|---|---|
| 1x A6000 or L40S (INT8 quantized) | $2,000 - $3,000 |
| Ops overhead (monitoring, support, patching) | $500 - $1,000 |
| **Total** | **$2,500 - $4,000** |
| **Per user** | **$250 - $400** |

**Hardware appliance option:**

| Component | Cost |
|---|---|
| Upfront hardware (server + GPU) | $10,000 - $15,000 (one-time) |
| Monthly software license + remote support | $1,000 - $2,000 |
| **Amortized per user (over 36 months)** | **$100 - $200/month** |

The appliance model is interesting because it shifts the cost structure. The upfront capital expense is significant, but the ongoing per-user cost drops considerably. This works best for regulated industries where data must stay on-premises — healthcare, legal, financial services.

### 100 Users — Shared Departmental Deployment

| Component | Monthly Cost |
|---|---|
| 2x H100 (handling concurrency and throughput) | $5,000 - $8,000 |
| Ops overhead (scaled) | $5,000 - $8,000 |
| **Total** | **$10,000 - $16,000** |
| **Per user** | **$100 - $160** |

At this scale, the operations overhead is roughly equal to compute. You need proper monitoring, a deployment pipeline, someone on call, and a process for model updates and security patches. The GPU may run itself, but the system around it does not.

### 500 Users — Business Unit or Mid-Size Enterprise

| Component | Monthly Cost |
|---|---|
| 2-3x H100 (with load balancing) | $7,500 - $12,000 |
| Ops overhead (dedicated team fraction) | $3,500 - $6,000 |
| **Total** | **$11,000 - $18,000** |
| **Per user** | **$22 - $36** |

This is where self-hosting starts to become competitive. Utilization improves dramatically with more users — 500 users generate enough traffic to keep GPU clusters reasonably busy throughout the business day. The per-user ops cost drops because you are spreading the same monitoring, support, and tooling across more seats.

### 1,000 Users — Large Enterprise or Multi-Tenant Platform

| Component | Monthly Cost |
|---|---|
| 3-4x H100 (high-throughput serving) | $11,000 - $18,000 |
| Ops overhead (dedicated team) | $7,000 - $9,000 |
| **Total** | **$18,000 - $27,000** |
| **Per user** | **$18 - $27** |

At 1,000 users, the economics tilt decisively. You are now in the range where self-hosting a smaller model can undercut API pricing for mid-tier models — and you retain full data sovereignty. This is the sweet spot for providers who can aggregate demand across multiple clients.

---

## API Pricing Landscape (April 2026)

Before comparing self-hosting to APIs, let us establish what the commercial API market actually charges today. Prices are listed per million tokens for input and output respectively.

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

Second, **there is a 50-100x spread** between the cheapest and most expensive models. A Gemini Flash-Lite call costs roughly 1/50th of a Claude Opus 4.6 call. For most routine enterprise tasks — summarization, classification, extraction, simple Q&A — the cheaper models are more than adequate.

Third, **output tokens are 3-5x more expensive than input tokens** across most providers. This matters for your cost modeling: a chatbot that produces long, detailed responses will cost significantly more than one that gives concise answers.

---

## GPU Rental Prices (April 2026)

For those planning self-hosted deployments, here are current cloud GPU rental rates. Prices vary significantly by provider, commitment level, and availability.

| GPU | Hourly Rate Range | Monthly Estimate (730 hrs) |
|---|---|---|
| NVIDIA H100 (80 GB) | $1.49 - $6.98 | $1,088 - $5,095 |
| NVIDIA H200 (141 GB) | $2.29 - $10.60 | $1,672 - $7,738 |
| NVIDIA A100 (80 GB) | $0.78 - $2.50 | $569 - $1,825 |
| NVIDIA A6000 (48 GB) | $0.50 - $1.20 | $365 - $876 |
| NVIDIA L40S (48 GB) | $0.60 - $1.80 | $438 - $1,314 |

The lower end of these ranges reflects spot pricing or long-term reservations with smaller GPU cloud providers (Lambda, RunPod, Vast.ai). The higher end reflects on-demand pricing from the major hyperscalers (AWS, Azure, GCP). For production workloads requiring reliability and SLAs, budget toward the mid-to-upper range.

> **Key takeaway:** GPU rental prices have declined roughly 30-40% year-over-year as supply expanded, but they remain substantial. A single H100 at mid-range pricing ($2,500-$3,500/month) costs more per month than many traditional server configurations. This is GPU-as-a-premium-commodity, not GPU-as-a-utility.

---

## API Cost Analysis: 100 Users Scenario

Now let us make the comparison concrete. Take our 100-user scenario and run the numbers through API pricing.

### Assumptions

- 100 users, each generating approximately 1 million tokens per day (a mix of input and output)
- That is 100 million tokens per day, or roughly **3 billion tokens per month**
- Blended rate assumes a typical 3:1 input-to-output token ratio

### API Cost at Different Price Points

| Model Tier | Blended Rate (per M tokens) | Monthly Cost (3B tokens) | Per User |
|---|---|---|---|
| Gemini Flash-Lite | ~$0.18 | $540 | $5.40 |
| GPT-4o-mini | ~$0.30 | $900 | $9.00 |
| Llama 70B (hosted) | ~$0.75 | $2,250 | $22.50 |
| Claude Haiku 4.5 | ~$2.00 | $6,000 | $60.00 |
| Mistral Medium | ~$1.50 | $4,500 | $45.00 |
| GPT-4o | ~$4.40 | $13,200 | $132.00 |
| Claude Sonnet 4.6 | ~$6.00 | $18,000 | $180.00 |

### Self-Hosting Cost for the Same 100 Users

From our earlier analysis of a self-hosted 20B model:

| Component | Monthly Cost |
|---|---|
| Compute (2x H100) | $5,000 - $8,000 |
| Operations overhead | $5,000 - $8,000 |
| **Total** | **$10,000 - $16,000** |
| **Per user** | **$100 - $160** |

### The Comparison

| Deployment | Monthly Cost | Per User |
|---|---|---|
| API: GPT-4o-mini | $900 | $9 |
| API: Claude Haiku 4.5 | $6,000 | $60 |
| API: Mistral Medium | $4,500 | $45 |
| **Self-hosted 20B model** | **$10,000 - $16,000** | **$100 - $160** |
| API: GPT-4o | $13,200 | $132 |
| API: Claude Sonnet 4.6 | $18,000 | $180 |

The pattern is clear. **Self-hosting is more expensive than small and mid-tier API models, and only approaches cost parity with frontier API models.** At 100 users, you are paying $13,000-$16,000 per month for a 20B parameter model that is objectively less capable than Claude Sonnet or GPT-4o — which cost about the same via API.

> **Key takeaway:** The traditional hosting logic is inverted. In traditional IT, self-hosting at moderate scale (100+ users) was almost always cheaper than buying a managed service. With AI, the hyperscaler API providers benefit from massive GPU fleets, custom silicon, and unbeatable economies of scale. Self-hosting only wins on cost at 500+ users with a smaller model — and even then, only if you are comparing against mid-tier API pricing. If your client is happy with GPT-4o-mini or Gemini Flash-Lite, no self-hosted deployment can compete on price. The case for self-hosting must rest on something other than cost.

---

## The Complete Scale Comparison

Here is the summary view that every IT services provider should have pinned to their wall. We compare self-hosting a 20B model against API costs across four deployment scales.

### Self-Hosted 20B Model vs API — Monthly Total Cost

| Scale | Self-Hosted (Total) | API: Budget Tier | API: Mid Tier | API: Frontier |
|---|---|---|---|---|
| 10 users | $2,500 - $4,000 | $54 | $600 | $1,800 |
| 100 users | $10,000 - $16,000 | $540 | $6,000 | $18,000 |
| 500 users | $11,000 - $18,000 | $2,700 | $30,000 | $90,000 |
| 1,000 users | $18,000 - $27,000 | $5,400 | $60,000 | $180,000 |

*Budget tier: Gemini Flash-Lite / GPT-4o-mini class (~$0.18-$0.30/M blended). Mid tier: Claude Haiku / Mistral Medium class (~$2.00/M blended). Frontier: Claude Sonnet / GPT-4o class (~$6.00/M blended). Assumes 1M tokens/user/day.*

### Self-Hosted 20B Model vs API — Per-User Monthly Cost

| Scale | Self-Hosted | API: Budget | API: Mid | API: Frontier |
|---|---|---|---|---|
| 10 users | $250 - $400 | $5.40 | $60 | $180 |
| 100 users | $100 - $160 | $5.40 | $60 | $180 |
| 500 users | $22 - $36 | $5.40 | $60 | $180 |
| 1,000 users | $18 - $27 | $5.40 | $60 | $180 |

API pricing is perfectly linear — the per-user cost does not change with scale. Self-hosting costs drop dramatically as you add users. The crossover points are:

- **Self-hosting beats mid-tier APIs** at roughly 400-500 users
- **Self-hosting beats frontier APIs** at roughly 100-200 users
- **Self-hosting never beats budget-tier APIs** at any realistic scale

### The Crossover Chart

If you plotted per-user cost against number of users, you would see two very different curves. The API line is flat — $5.40 per user whether you have 10 or 10,000. The self-hosting curve is a steep hyperbola, starting at $250-$400 for 10 users and asymptotically approaching $15-$20 for very large deployments.

The lines cross at different points depending on which API tier you are comparing against:

| Comparison | Crossover Point |
|---|---|
| Self-hosted vs Budget API (Flash-Lite, 4o-mini) | **Never** (self-hosting is always more expensive) |
| Self-hosted vs Mid-tier API (Haiku, Mistral Medium) | **~400-500 users** |
| Self-hosted vs Frontier API (Sonnet, GPT-4o) | **~100-200 users** |
| Self-hosted vs Premium API (Opus, GPT-4.1 + heavy usage) | **~50-80 users** |

---

## The On-Premises Economics: A Different Comparison

Everything above compares your self-hosting costs against API prices. That is the right comparison for clients who can use cloud APIs. But for a significant segment of the EU enterprise market — banking, healthcare, defense, legal, public sector, and any organization whose compliance or legal teams have ruled out external AI APIs — the API price is irrelevant. It is not an option they can choose.

For these clients, the comparison that matters is entirely different:

- **Your managed AI service** vs. **the client building and running it themselves**
- **Your managed AI service** vs. **the client having no AI at all**

This is traditional IT services economics, and the numbers look much more favorable.

### What It Costs a Client to Do It Themselves

Consider a mid-sized European bank that wants to run a 20B model on-premises for 100 internal users. If they build and manage the infrastructure themselves, they need:

| Cost Component | Annual Cost |
|---|---|
| GPU hardware (2x H100, amortized over 3 years) | $17,000 - $23,000 |
| Server infrastructure, networking, cooling | $8,000 - $12,000 |
| ML engineer (1 FTE, EU market) | $80,000 - $130,000 |
| DevOps/infrastructure engineer (0.5 FTE) | $30,000 - $50,000 |
| Software licensing, monitoring, security tools | $10,000 - $20,000 |
| Training and upskilling | $5,000 - $10,000 |
| **Total annual cost (client DIY)** | **$150,000 - $245,000** |
| **Monthly equivalent** | **$12,500 - $20,400** |
| **Per user per month** | **$125 - $204** |

The dominant cost is not hardware — it is people. An ML engineer who can deploy, optimize, and maintain LLM inference infrastructure commands a significant salary in the EU market, and the client needs at least one full-time. Many will need more, especially during the initial setup phase.

### What You Can Charge as a Managed Service

As an IT services provider, you have advantages the individual client does not:

- **Shared expertise.** Your ML engineer serves multiple clients, not one. The cost is spread across your customer base.
- **Reusable tooling.** Your deployment pipelines, monitoring dashboards, and update processes are built once and used for every client.
- **Operational maturity.** You have been managing infrastructure for decades. The client's newly-hired ML engineer is figuring it out for the first time.
- **Vendor relationships.** You negotiate GPU procurement and cloud pricing at volume.

These advantages let you deliver the same service at a lower cost than the client can achieve alone — the exact same economics that made traditional IT managed services profitable.

| Deployment Scale | Your Cost | You Charge | Client DIY Cost | Your Margin |
|---|---|---|---|---|
| 10 users (dedicated) | $2,500 - $4,000/mo | $5,000 - $8,000/mo | $7,000 - $12,000/mo | 40-55% |
| 100 users (shared infra) | $10,000 - $16,000/mo | $18,000 - $28,000/mo | $12,500 - $20,400/mo | 40-50% |
| 500 users (platform) | $11,000 - $18,000/mo | $22,000 - $35,000/mo | $20,000 - $35,000/mo | 45-55% |

At 10 users, the economics are especially compelling. A small client cannot justify a full-time ML engineer for 10 users, but they still need someone to manage the infrastructure. Your shared-expertise model gives them enterprise-grade AI ops at a fraction of the cost of doing it themselves.

At 100 users, you price competitively with the client's DIY cost while capturing a healthy margin. The client gets operational reliability, SLAs, and the ability to focus their internal team on using AI rather than running it.

At 500+ users, the client starts to have enough scale to justify their own team — but even then, your platform approach (serving multiple clients on shared infrastructure, with isolated data) can remain cost-competitive.

> **Key takeaway:** For on-prem-required clients, your competition is not OpenAI or Google. It is the client's internal IT team. And you beat internal IT teams the same way you always have: through operational specialization, shared costs across multiple clients, and mature tooling. The margin structure looks like traditional managed services — 40-55% — not the razor-thin margins of trying to compete with hyperscaler API pricing.

### The Market Size Question

How large is the on-prem segment? No published data answers this precisely for GenAI specifically, but several indicators suggest it is substantial in the EU market:

- **Banking and financial services**: ECB and national regulators increasingly scrutinize cloud concentration risk. Many EU banks maintain strict policies requiring sensitive data processing on-premises or in private cloud.
- **Healthcare**: Patient data under GDPR has stringent processing requirements. Many EU healthcare systems have explicit policies against external AI APIs for clinical data.
- **Public sector**: Government organizations across EU member states frequently require on-premises or sovereign cloud deployment for sensitive workloads.
- **Legal**: Attorney-client privilege and professional confidentiality obligations create strong incentives for on-prem AI.
- **Defense and critical infrastructure**: By definition, these sectors require controlled environments.

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

## What These Numbers Do Not Capture

The tables above cover the direct, measurable costs. But several factors shift the equation in ways that are harder to quantify:

**Factors favoring APIs:**
- Zero setup time — you can be live in hours, not weeks
- Automatic model upgrades — when GPT-4.1 improves, you get it free
- Elastic scaling — pay nothing during weekends and holidays
- No GPU procurement risk — you never own depreciating hardware

**Factors favoring self-hosting:**
- Data sovereignty — tokens never leave your infrastructure
- Regulatory compliance — some EU regulations and client contracts require on-premises processing
- Customization — fine-tuning, custom system prompts with no rate limits, specialized tooling
- Predictable costs — no surprise bills from a prompt injection attack or runaway agent loop
- Independence — no vendor can deprecate your model or change your terms overnight

For EU IT services providers, the data sovereignty and compliance arguments are often the strongest justification for self-hosting. The cost math alone rarely supports it. But combine cost with a genuine compliance requirement, and the self-hosting premium starts to look like a reasonable price for regulatory peace of mind.

> **Key takeaway:** Do not build your business case on cost savings from self-hosting. Build it on the value of data sovereignty, regulatory compliance, and customization. Then use these numbers to price your offering realistically — knowing exactly what premium you are asking customers to pay, and why that premium is worth it.

---

## Practical Implications for Your Pricing Strategy

These numbers lead to three immediate conclusions for how you should think about pricing:

**1. Do not try to undercut API providers on price.** You will lose. OpenAI, Google, and Anthropic are spending billions on custom silicon and infrastructure. Your cost per token will always be higher than theirs for equivalent model quality.

**2. For on-prem clients, price against the client's DIY cost — not against API pricing.** A managed AI infrastructure service at $180/user/month is expensive compared to a $5.40/user/month API call, but it is a bargain compared to the $125-$204/user/month it would cost the client to build and staff it themselves. Frame your pricing against the right benchmark.

**3. Price on value, not on cost-plus.** If your service provides data sovereignty, compliance assurance, or specialized fine-tuning, price those outcomes directly. A $180/user/month service that keeps patient data on-premises is a different product from a $5.40/user/month API call that sends data to US servers.

**4. Consider hybrid architectures.** Route sensitive queries through your self-hosted infrastructure and non-sensitive queries through cheap APIs. This keeps your GPU utilization high on the work that actually requires privacy, while keeping costs down on everything else. We will explore this model in detail in Chapter 5.

The numbers tell two stories. For cloud-comfortable clients, the strategy is not about running models cheaper than the hyperscalers — it is about delivering expertise, integration, and compliance on top of their APIs. For on-prem-required clients, you are still in the infrastructure business, and the economics work in your favour — as long as you price against the right comparison.
