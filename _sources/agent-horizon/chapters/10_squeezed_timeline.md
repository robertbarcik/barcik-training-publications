# Chapter 10: Will the Timeline Actually Squeeze?

---

Everything so far has assumed the agent transition will move faster than the cloud transition did, and that European enterprises especially will have reason to jump ahead to the mature architecture rather than live through the lock-in phase. That assumption is baked into the advice this booklet gives. It is also genuinely contestable. This chapter owes the reader a forecast — not a both-sides essay, a clear call about which way the evidence points and what would have to happen for the call to be wrong.

## Two Scenarios

**The Leapfrog Scenario.** Enterprises, particularly in Europe, move quickly past vendor lock-in and settle on hybrid, agnostic, routing-heavy architectures by 2027-2028. MCP-style protocols dominate the access layer. LangGraph-style agnostic frameworks become the reference orchestration layer for regulated industries. Vendor SDKs persist as acceleration tools for less-regulated verticals but don't become the dominant enterprise default. Observability and audit tooling become a distinct enterprise software category analogous to APM. The cycle the cloud industry took twelve years completes in five.

**The Pilot-Purgatory Scenario.** Most enterprises get stuck in the same trap that's already catching 95% of AI pilots: the technology works, the pilots are interesting, scaling never happens. Models keep getting better, which paradoxically makes frameworks feel less necessary, which keeps architectures small and informal. Vendor SDKs win by default because they're the path of least resistance. Agnostic frameworks remain a specialty concern for a narrow slice of regulated enterprises. The lock-in cycle resembles the cloud cycle — a long messy intermediate phase taking most of a decade.

## The Call

The likeliest outcome is **bifurcated, tilted toward Leapfrog for regulated EU and Pilot Purgatory for everyone else**. Regulated European enterprises (banking, insurance, public sector, healthcare, defence) will Leapfrog because the AI Act is a direct forcing function and the architectures they need to meet compliance look like the mature end-state. Everyone else will spend time in Pilot Purgatory — not because the technology fails, but because organisational machinery (data quality, exec sponsorship, evaluation discipline) isn't ready. The vendor SDKs will do most of the quiet heavy lifting for the pilots that succeed. The agnostic frameworks plus observability will dominate the long-term architecture for the workloads that matter most.

In cloud-parallel terms: Leapfrog looks like the EU enterprise in 2012 that skipped AWS-mono and went straight to hybrid cloud with Kubernetes. Pilot Purgatory looks like the US mid-market enterprise in 2015 still running parallel systems in three clouds trying to figure out a coherent strategy. Both existed; both were rational responses to specific conditions.

## Why This Might Still Be Wrong — Named Leading Indicators

A forecast should be falsifiable. Here are six specific 2026-2027 indicators. If they trend as listed, Leapfrog-for-regulated-EU holds. If they don't, I'm wrong.

**1. MCP reaches 200M monthly SDK downloads by Q4 2026.** Currently ~97M. Continued doubling confirms the protocol layer is truly settled. Flattening below 150M by Q4 means protocol adoption is stalling and the thesis weakens.

**2. The EU AI Act produces at least one publicly announced high-risk enforcement action by Q2 2027.** Not a warning letter — an actual fine or order. Absent that, the forcing-function premise is weaker than I've claimed.

**3. LangSmith crosses 1,000 paying enterprise seats by Q3 2026.** Concrete, trackable (LangChain publishes milestone counts). If the observability category doesn't monetise, the "becomes its own software category like APM" prediction is off.

**4. Mistral, Aleph Alpha, or a similarly-positioned EU lab ships a model within 10% of the frontier (on a named benchmark — say, GPQA or SWE-Bench) by mid-2027.** If the gap widens instead, the routing pattern collapses for reasoning-heavy workloads and EU enterprises will be forced to choose between frontier access and sovereignty. Pilot-Purgatory odds rise materially.

**5. At least one of OpenAI, Google, or Anthropic ships a sovereign-cloud data-residency guarantee for EU customers — contractually binding, not just regional availability — by end of 2026.** If they do, vendor SDKs stay in play for European regulated workloads and the agnostic case weakens. If they don't, vendor SDKs are effectively disqualified from a chunk of the regulated EU market.

**6. A2A (or a direct successor) reaches 10k+ public agent cards in a discoverable registry by end of 2027.** That's the indicator that multi-agent interop is becoming ambient rather than theoretical. If A2A traffic stays internal to single enterprises, the "multi-agent architecture becomes mainstream" premise is deferred and the timing of Leapfrog slips.

**These aren't the usual indicators. Nobody else is tracking them as a coherent set.** If three of the six move as described, the forecast holds. If three or more don't, I'm wrong about the timing or the shape — probably both.

> **Our forecast in one sentence:** Regulated European enterprises will Leapfrog by roughly 2028; most other enterprises will live through a compressed but real version of the cloud-era Lock-In Cycle; vendor SDKs will win the short term and the agnostic frameworks plus their observability ecosystem will win the long term for workloads that matter most — unless three of the six named indicators above don't move as described, in which case I've mis-read the cycle.

---

*Next: [Chapter 11 — Picking Your Stack](11_picking_your_stack.md)*
