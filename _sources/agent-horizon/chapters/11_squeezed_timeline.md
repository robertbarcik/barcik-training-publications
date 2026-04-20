# Chapter 11: Will the Timeline Actually Squeeze?

---

## The Forecast This Chapter Has To Make

Everything so far has assumed that the agent transition will move faster than the cloud transition did, and that European enterprises especially will have reason to jump ahead to the mature architecture rather than living through the lock-in phase. That assumption is baked into the advice this booklet gives. It is also genuinely contestable. This chapter owes the reader a forecast — not a both-sides essay, not a confident prediction, but a clear argument about which way the evidence actually points and what would have to happen for the forecast to be wrong.

The two competing scenarios are sharp enough to name.

**The Leapfrog Scenario.** Enterprises, particularly in Europe, move quickly past vendor-lock-in and settle on hybrid, agnostic, routing-heavy architectures by 2027–2028. MCP-style protocols dominate the access layer. LangGraph-style agnostic frameworks become the reference orchestration layer for regulated industries. The vendor SDKs persist as acceleration tools for less-regulated verticals but do not become the dominant enterprise default. Observability and audit tooling become a distinct enterprise software category analogous to APM. The cycle the cloud industry went through in twelve years completes in five.

**The Pilot-Purgatory Scenario.** Most enterprises get stuck in the same trap that is already catching 95% of AI pilots: the technology works, the pilots are interesting, but the scaling never happens. Models keep getting better, which paradoxically makes frameworks feel less necessary, which keeps architectures small and informal. Vendor SDKs win by default because they are the path of least resistance. Agnostic frameworks remain a specialty concern for a narrow slice of regulated enterprises. The lock-in cycle looks a lot like the cloud cycle — a long, messy intermediate phase that takes most of a decade to resolve.

Both scenarios are coherent. Both have evidence supporting them. Our forecast is that something between them is the most likely outcome, tilted toward the Leapfrog side for regulated enterprises and toward the Pilot-Purgatory side for the rest. Here is how we get there.

## The Case for Leapfrog

The strongest arguments for Leapfrog are structural.

**The tooling has already matured faster than anyone expected.** MCP went from proposal to de-facto standard in under two years. The Linux Foundation donation happened within a year of serious enterprise adoption. The observability ecosystem (LangSmith, Langfuse, Phoenix) matured faster than the equivalent APM ecosystem did for microservices. Tooling maturity is a leading indicator of architectural settlement, and the tooling is settling fast.

**The regulatory environment is forcing the mature architecture.** As Chapter 10 argued, the EU AI Act's compliance requirements push architectures toward observability, audit, and sovereignty-respecting execution — features that happen to align with the agnostic + routing pattern that represents the mature end-state of the cycle. When regulation pre-specifies the destination, the intermediate phases compress.

**The lessons from cloud are fresh.** Enterprise architects who lived through the 2014–2020 multi-cloud reckoning are now in senior roles. They have institutional memory of what vendor lock-in cost them. They are less likely to make the same bet twice, and the vendors are finding those buyers harder to convince.

**AI coding assistants cut the cost of custom infrastructure.** One of the historical reasons to use a framework was the time cost of writing custom glue code. That cost has dropped by an order of magnitude. Building a lightweight, custom, agnostic orchestration layer tailored to one enterprise's needs is now a weeks-long project for a small team, not a multi-quarter effort. This lowers the cost of being agnostic.

**The models are shipping with agent-friendly primitives.** Every major frontier model ships with structured output, reliable function calling, tool-use training, and long-context support. This is the model layer doing the framework's historical job for it — and once that work is in the model, the agnostic framework on top becomes thinner and more viable.

Taken together, these arguments suggest that the intermediate phase of the transition is genuinely compressible. The things that slowed cloud adoption — immature tooling, lock-in surprises, a shortage of sophisticated buyers, a cost-inflated alternative to vendor services — are weaker in 2026 than they were in 2012.

## The Case for Pilot Purgatory

The strongest arguments against Leapfrog are operational.

**Most enterprises cannot execute the mature architecture today.** Running a well-observed, auditable, multi-model routed agent system requires engineering talent most enterprises do not have. It requires observability discipline that most enterprises do not practice. It requires an evaluation and cost-attribution culture that most enterprises have not built. Regulation does not create engineering capacity. Requirements without capacity produce half-finished projects, not leapfrogs.

**The 95% pilot failure rate is real.** Industry analyst data consistently shows that the overwhelming majority of enterprise AI pilots do not scale to production. Most of them die for reasons that have nothing to do with framework choice: messy data, absent executive sponsorship, unclear ROI, underestimated integration complexity. A framework decision cannot rescue a project that fails for organisational reasons, and no amount of Leapfrog-ready architecture saves a pilot that never ships.

**Models getting better paradoxically slows framework adoption.** When a single well-prompted GPT-4o or Claude call can do what required a twelve-node LangGraph graph eighteen months ago, the business case for the framework weakens. Engineers reach for the simpler solution, which is usually the vendor SDK or a plain LLM-in-a-loop. This is a headwind for framework adoption in general, not just agnostic frameworks — but it bites agnostic frameworks hardest, because their value proposition is most tied to mitigating model weakness.

**Vendors are closing compliance gaps.** OpenAI's European regions, Anthropic's European infrastructure investments, Microsoft's sovereign cloud offerings, Google's GCP compliance certifications — the vendors are working hard to make the "I can use a vendor SDK and still meet European compliance" story credible. If they succeed, the regulatory forcing function for agnostic architectures weakens.

**Inertia is a powerful force in enterprise IT.** Enterprises that successfully deploy agents on OpenAI in 2026 will not rip them out in 2027 just because a better architecture exists. The migration cost is real, the benefit is deferred, and quarterly pressure discourages the refactor. Installed base is sticky even when the original choice was suboptimal.

These arguments are not strawmen. They describe the lived experience of many enterprise programmes, and they are consistent with what the analyst community has been saying. A responsible reader should take them seriously.

## The Probable Outcome

Weighing both sides, the likeliest actual trajectory is bifurcated.

**Regulated enterprises in Europe** — banking, insurance, public sector, healthcare, heavy industry in regulated verticals — are likely to take the Leapfrog path. The regulatory pressure is a direct forcing function; the architectures they need to meet compliance look like the mature end-state; and they have the discipline (slow, but real) to absorb the engineering cost of getting there. For these enterprises, the trajectory from 2026 to 2029 probably looks a lot like the Leapfrog scenario.

**Everyone else** is more likely to spend time in Pilot Purgatory. Not because the technology fails, but because the organisational machinery is not ready. Pilots will keep shipping. Some will scale; most will not. The vendor SDKs will do most of the quiet heavy lifting for the pilots that succeed. The agnostic frameworks will remain a specialist concern for regulated workloads and for a handful of enterprises with unusually strong engineering cultures. This is not Pilot Purgatory forever — it is Pilot Purgatory until the industry develops the management and operational discipline that deploying agents at scale actually requires. That might be 2028, 2029, or later.

In terms of the cloud parallel: the Leapfrog scenario is the EU enterprise in 2012 that skipped AWS-mono and went straight to hybrid cloud with Kubernetes. The Pilot-Purgatory scenario is the US mid-market enterprise in 2015 that was still running parallel systems in three clouds and trying to figure out a coherent strategy. Both existed; both were rational responses to the conditions those specific organisations faced.

> **Our forecast in one sentence:** Regulated European enterprises will Leapfrog by roughly 2028; most other enterprises will live through a compressed but real version of the cloud-era Lock-In Cycle; the vendor SDKs will win the short term, and the agnostic frameworks (with their observability ecosystems) will win the long term for the workloads that matter most.

## Leading Indicators to Watch

A forecast should be falsifiable. Here are the signals that, over the next eighteen months, will tell you whether the forecast is holding.

**Signal 1: How aggressively MCP adoption continues.** If MCP's growth flattens, the protocol layer's settlement is less complete than it currently appears, which would weaken the Leapfrog case. If growth continues at or above current rates, the protocol layer is genuinely settling into the HTTP-like role we have described.

**Signal 2: Whether AI Act enforcement actually bites.** Real, public enforcement actions against non-compliant deployments in 2026–2027 will push the regulated-enterprise segment hard toward Leapfrog. Weak enforcement will slow the transition.

**Signal 3: Vendor SDK market share in regulated industries.** If Google ADK, OpenAI Agents, and similar vendor SDKs show significant adoption in European regulated verticals, the Leapfrog hypothesis is weakening. If regulated enterprises in Europe keep drifting toward LangGraph and self-hosted observability, the Leapfrog hypothesis is strengthening.

**Signal 4: The compliance gap between vendors and sovereign alternatives.** If OpenAI, Anthropic, and Google successfully close the sovereignty gap — with regional availability, contractual data-residency guarantees, and credible audit artefacts — the Leapfrog case weakens meaningfully.

**Signal 5: Open-weight model competitiveness.** If Llama, Mistral, and other open-weight contenders stay within striking distance of frontier proprietary models, the routing pattern stays viable. If they fall meaningfully behind, the routing pattern collapses and enterprises are forced to choose between frontier access (US vendors) and sovereignty (worse models).

**Signal 6: Observability market maturation.** If the LangSmith/Langfuse/Phoenix category consolidates, raises real revenue, and builds enterprise features at pace, the mature architecture is arriving. If the category stays fragmented and under-resourced, it is not.

None of these signals is decisive on its own. Together, they will tell you by late 2027 whether the Leapfrog has happened, is happening, or has been deferred for another cycle.

> **What to take from this chapter:** Neither the Leapfrog scenario nor the Pilot-Purgatory scenario is a confident single forecast. The likeliest outcome is bifurcated: regulated European enterprises will Leapfrog; most other enterprises will move through a compressed Lock-In Cycle. Vendor SDKs will dominate the short-term installed base; agnostic frameworks plus observability will dominate the long-term architecture for strategic workloads. Six leading indicators — MCP growth, AI Act enforcement, vendor SDK regulated-market share, compliance-gap closure, open-weight competitiveness, observability market maturation — will tell you by late 2027 whether the forecast is holding.

---

*Next: [Chapter 12 — Picking Your Stack](12_picking_your_stack.md)*
