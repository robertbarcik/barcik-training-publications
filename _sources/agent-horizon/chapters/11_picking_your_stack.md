# Chapter 11: Picking Your Stack

---

The landscape is mapped. MCP is the ambient protocol at the access layer. A2A is the emerging protocol for agent-to-agent. The orchestration layer splits into vendor SDKs and agnostic frameworks. Observability is a first-class concern. Lock-in has sharp per-vendor answers. The EU has specific reasons to pursue a different architecture. The forecast has six falsifiable indicators.

What this chapter does is compress the decision. Not into a ranking; rankings age badly. Into five questions where your honest answers determine the architecture that fits you, plus a decision tree that renders the answers visually, plus a worked case study of a regulated European bank, plus a short epilogue.

## The Five Questions

Work through them in order. Each narrows the field.

**1. Where does your cloud allegiance already lie?** All-in on Google Cloud → ADK is the default candidate. All-in on AWS → Strands. All-in on Azure or Microsoft 365 → Azure AI Foundry Agent Service. Cloud-portable or multi-cloud by policy → the agnostic frameworks (LangGraph, CrewAI) become the natural centre. Building against the grain of your cloud ecosystem costs months of unnecessary integration work.

**2. How hard is your model-swap requirement?** Hard (must route by compliance / cost / language, or board-level anti-lock-in) → agnostic. LangGraph is the defensible default. Claude Agent SDK is immediately disqualified; OpenAI Agents SDK is marginal. Soft (prefer portability, wouldn't rebuild everything) → vendor SDKs are viable, especially ADK and OpenAI Agents. None → all frameworks on the table; pick based on the other questions.

**3. How much regulatory or audit weight is on this deployment?** Heavy (banking, insurance, healthcare, public sector, defence, high-risk under AI Act) → observability and audit are non-negotiable. LangGraph + LangSmith (or Langfuse self-hosted) is the most commonly defensible architecture. Medium (GDPR, some sector rules) → vendor SDKs remain viable with supplemental observability. Light (internal productivity, non-sensitive) → governed by other questions.

**4. How much do you need multi-agent coordination?** Yes, core → ADK leads, with native A2A and hierarchical structure. CrewAI is a strong second for prototyping; LangGraph handles multi-agent but requires more explicit engineering. Maybe later → pick a framework with a credible multi-agent + A2A roadmap. Single-agent, probably always → LLM-in-a-loop baseline may even suffice. The most common mistake here is over-estimating the need; many enterprises ship three-agent systems where one well-prompted agent would handle the work.

**5. How much in-house AI engineering talent do you have?** Deep → full range open; agnostic frameworks more attractive because you can pay their cost. Moderate → vendor SDKs absorb more engineering burden; agnostic viable but consumes more capacity than you expect. Limited → vendor SDKs are the correct default. An agnostic framework without a team to drive it is a failed project waiting to happen. Be unflinching here: enterprises are most tempted to answer optimistically.

## The Decision Tree

<div style="margin: 2rem 0; padding: 1rem; border: 1px solid #e2e8f0; border-radius: 8px; background: #f8fafc; overflow-x: auto;">
<svg viewBox="0 0 780 520" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 780px; height: auto; font-family: 'Helvetica Neue', Arial, sans-serif;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
    <style>
      .q-node { fill: #1e3a5f; }
      .q-text { fill: white; font-size: 12px; font-weight: 700; }
      .q-sub { fill: rgba(255,255,255,0.85); font-size: 10px; }
      .leaf { stroke-width: 2; }
      .leaf-booklets { fill: #eff6ff; stroke: #3b82f6; }
      .leaf-reports { fill: #f5f3ff; stroke: #8b5cf6; }
      .leaf-guides { fill: #fffbeb; stroke: #d97706; }
      .leaf-text { font-size: 11px; font-weight: 700; fill: #1e293b; }
      .leaf-sub { font-size: 9.5px; fill: #475569; }
      .edge { stroke: #94a3b8; stroke-width: 1.5; fill: none; }
      .edge-label { font-size: 10px; fill: #475569; font-weight: 600; }
    </style>
  </defs>

  <!-- Title -->
  <text x="390" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1e3a5f">The Agent Stack · Decision Tree</text>

  <!-- Root: Q3 Regulatory weight -->
  <rect class="q-node" x="320" y="40" width="140" height="44" rx="6"/>
  <text class="q-text" x="390" y="58" text-anchor="middle">Q3: Regulatory weight?</text>
  <text class="q-sub" x="390" y="72" text-anchor="middle">AI Act high-risk? Audit mandates?</text>

  <!-- Branch Heavy -->
  <path class="edge" d="M 380 84 L 200 120" marker-end="url(#arrow)"/>
  <text class="edge-label" x="270" y="98">Heavy</text>

  <!-- Branch Light/Medium -->
  <path class="edge" d="M 400 84 L 580 120" marker-end="url(#arrow)"/>
  <text class="edge-label" x="490" y="98">Light / Medium</text>

  <!-- Q2 Model swap (on heavy path) -->
  <rect class="q-node" x="130" y="125" width="140" height="44" rx="6"/>
  <text class="q-text" x="200" y="143" text-anchor="middle">Q2: Model swap?</text>
  <text class="q-sub" x="200" y="157" text-anchor="middle">Routing / anti-lock-in mandate?</text>

  <!-- Q1 Cloud (on light/med path) -->
  <rect class="q-node" x="510" y="125" width="140" height="44" rx="6"/>
  <text class="q-text" x="580" y="143" text-anchor="middle">Q1: Cloud allegiance?</text>
  <text class="q-sub" x="580" y="157" text-anchor="middle">GCP / AWS / Azure / neutral?</text>

  <!-- Leaves on heavy path -->
  <path class="edge" d="M 170 169 L 90 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="115" y="190">Hard</text>
  <path class="edge" d="M 230 169 L 310 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="280" y="190">Soft / None</text>

  <!-- Leaf: LangGraph + Langfuse self-hosted (Heavy + Hard) -->
  <rect class="leaf leaf-booklets" x="10" y="215" width="175" height="90" rx="6"/>
  <text class="leaf-text" x="97" y="235" text-anchor="middle">LangGraph + self-hosted</text>
  <text class="leaf-text" x="97" y="250" text-anchor="middle">Langfuse / LangSmith</text>
  <text class="leaf-sub" x="97" y="270" text-anchor="middle">Multi-model routing,</text>
  <text class="leaf-sub" x="97" y="283" text-anchor="middle">audit-grade traces, EU-region</text>
  <text class="leaf-sub" x="97" y="296" text-anchor="middle">observability infrastructure</text>

  <!-- Leaf: Azure AI Foundry Agent Service with heavy compliance (Heavy + Soft/None) -->
  <rect class="leaf leaf-reports" x="230" y="215" width="175" height="90" rx="6"/>
  <text class="leaf-text" x="317" y="235" text-anchor="middle">Foundry Agent Service</text>
  <text class="leaf-text" x="317" y="250" text-anchor="middle">or ADK on Vertex EU</text>
  <text class="leaf-sub" x="317" y="270" text-anchor="middle">Vendor compliance posture,</text>
  <text class="leaf-sub" x="317" y="283" text-anchor="middle">sovereign region + DPA,</text>
  <text class="leaf-sub" x="317" y="296" text-anchor="middle">supplement with Langfuse</text>

  <!-- Leaves on light/medium path (Q1) -->
  <path class="edge" d="M 550 169 L 460 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="490" y="190">GCP / AWS / Azure</text>
  <path class="edge" d="M 610 169 L 700 210" marker-end="url(#arrow)"/>
  <text class="edge-label" x="670" y="190">Neutral</text>

  <!-- Leaf: Vendor SDK fit to cloud (Light + Major cloud) -->
  <rect class="leaf leaf-guides" x="380" y="215" width="175" height="90" rx="6"/>
  <text class="leaf-text" x="467" y="235" text-anchor="middle">Vendor SDK matching</text>
  <text class="leaf-text" x="467" y="250" text-anchor="middle">your cloud</text>
  <text class="leaf-sub" x="467" y="270" text-anchor="middle">ADK on GCP,</text>
  <text class="leaf-sub" x="467" y="283" text-anchor="middle">Strands on AWS,</text>
  <text class="leaf-sub" x="467" y="296" text-anchor="middle">Azure Agent on Azure</text>

  <!-- Q5 Talent (Neutral branch) -->
  <rect class="q-node" x="620" y="215" width="140" height="44" rx="6"/>
  <text class="q-text" x="690" y="233" text-anchor="middle">Q5: In-house talent?</text>
  <text class="q-sub" x="690" y="247" text-anchor="middle">AI-engineering depth</text>

  <!-- Talent leaves -->
  <path class="edge" d="M 650 259 L 570 310" marker-end="url(#arrow)"/>
  <text class="edge-label" x="590" y="286">Deep / Moderate</text>
  <path class="edge" d="M 720 259 L 720 310" marker-end="url(#arrow)"/>
  <text class="edge-label" x="730" y="290">Limited</text>

  <!-- Leaf: LangGraph or CrewAI (Neutral + Deep) -->
  <rect class="leaf leaf-booklets" x="480" y="315" width="175" height="80" rx="6"/>
  <text class="leaf-text" x="567" y="335" text-anchor="middle">LangGraph (production)</text>
  <text class="leaf-text" x="567" y="350" text-anchor="middle">or CrewAI (prototyping)</text>
  <text class="leaf-sub" x="567" y="370" text-anchor="middle">Bring your own</text>
  <text class="leaf-sub" x="567" y="383" text-anchor="middle">observability + auth</text>

  <!-- Leaf: OpenAI Agents or LLM-in-a-loop (Neutral + Limited) -->
  <rect class="leaf leaf-guides" x="670" y="315" width="100" height="80" rx="6"/>
  <text class="leaf-text" x="720" y="335" text-anchor="middle">OpenAI Agents SDK</text>
  <text class="leaf-text" x="720" y="350" text-anchor="middle">or LLM-in-a-loop</text>
  <text class="leaf-sub" x="720" y="370" text-anchor="middle">Absorb vendor</text>
  <text class="leaf-sub" x="720" y="383" text-anchor="middle">burden; ship fast</text>

  <!-- Note at bottom -->
  <text x="390" y="465" text-anchor="middle" font-size="11" fill="#475569" font-style="italic">Q4 (multi-agent) and Q5 (talent) narrow within each leaf; Q1 may override heavy-path choice if cloud commitment is absolute.</text>
  <text x="390" y="488" text-anchor="middle" font-size="10" fill="#64748b">Colour legend: blue = agnostic-leaning · violet = vendor-with-compliance-overlay · amber = vendor-default fast path</text>

</svg>
</div>

The tree is a scanning aid, not a substitute for thinking. The case study below shows how the questions actually resolve in practice, and where the tree's answer was wrong.

## A Worked Case: A Regulated European Bank

Let me walk through a composite; details are amalgamated from real engagements, specifics changed.

A mid-sized European retail bank. Roughly 4,000 employees across four EU countries. Retail products (mortgages, consumer credit, cards), a wealth-advisory arm, no investment-banking division. Tech stack: Azure-dominant, some on-prem mainframe for core banking (the usual European bank architecture). In-house dev capability: solid on Java/.NET, nascent on AI. Executive sponsorship from the COO, who has been told by the board that the bank "must ship something meaningful with AI in 2026" and is being careful about which meaningful thing.

The use case: an internal advisor assistant for relationship managers. Summarise a client's portfolio, flag anomalies, surface relevant product offers, prepare meeting notes, draft follow-up emails. Not customer-facing. Not making credit decisions. But touching personal data continuously and, for the meeting-prep portion, adjacent to regulated advisory workflows.

### Walking the Five Questions

**Q1 Cloud allegiance.** Azure-primary but with a sovereignty overlay: client data for regulated workflows has to execute in EU regions and the internal security team is openly hostile to any architecture that hard-binds to one US vendor. Initial instinct: Azure AI Foundry Agent Service. The tree disagrees (see below).

**Q2 Model swap.** Hard. Security policy explicitly requires that PII-bearing inference can be moved to a different model provider inside four weeks if a specific vendor becomes unavailable or non-compliant. This isn't theoretical: the team has been burned by an abrupt vendor policy change in the past on a different product.

**Q3 Regulatory weight.** Heavy. The advisory-adjacent workflows likely classify as high-risk under the AI Act (even though we're still waiting on case law around "advisory" scope). Six-month log retention is a floor; internal banking regulation pushes it to seven years for anything touching advisory content. Annual internal audit + quarterly external compliance review.

**Q4 Multi-agent.** Meaningfully yes. The final architecture wants three specialists: a retrieval agent (pulls client data and product catalog), an advisor agent (reasons about recommendations), a compliance agent (checks outputs against policy and flags anything that needs human review). Routing between them is structured, not ad-hoc.

**Q5 Talent.** Moderate-trending-toward-limited. The team has two engineers who have built LLM applications before. Neither has run LangGraph in production. Capacity to absorb learning curve is real but bounded by quarterly delivery pressure.

### What the Tree Said

Heavy regulation + hard swap → **LangGraph + self-hosted Langfuse, EU-region Azure, multi-model routing**. That's the blue leaf.

The architecture would be: LangGraph for orchestration; Langfuse self-hosted on Azure North Europe for observability/audit; MCP servers in front of the CRM, product catalog, and policy library; per-interaction model routing: Claude via Azure (Anthropic's Azure partnership, with a contractual EU-region guarantee) for reasoning-heavy tasks; locally-hosted Mistral for tasks touching personal data; A2A between the three specialist agents with agent cards registered in an internal registry.

That's the architecturally correct answer. It's also where the framework's answer and what the team actually did diverged.

### Where We Overrode the Framework

The bank shipped v1 on the **OpenAI Agents SDK** via Azure OpenAI, not LangGraph.

The reason was Q5. The two AI-capable engineers didn't have the bandwidth to simultaneously learn LangGraph, stand up a self-hosted Langfuse, configure multi-model routing, *and* deliver a pilot in the quarter the COO had committed to. The framework-correct answer was infeasible given the organisational reality. And shipping something good-enough in the committed window mattered more strategically than shipping the architecturally-perfect thing six months late.

What we did instead: OpenAI Agents SDK for orchestration, Azure OpenAI with EU-region Claude (which Microsoft offers via Anthropic through the Azure marketplace) as the default model, Azure Monitor + a thin internal tracing wrapper as the observability layer, vendor-native guardrails, MCP servers for the internal systems. We wrote down (explicitly, in the architecture decision record) that this was a temporary choice, that the migration target was LangGraph + Langfuse, and that certain features (A2A-mediated multi-agent delegation, durable execution for long-running compliance reviews) would be deferred until the migration.

We migrated to LangGraph in month 9. The migration took seven weeks including the observability cutover. It would have taken longer if we hadn't designed the v1 architecture knowing it was temporary: specifically, if we hadn't kept the prompts and tool surfaces as framework-agnostic as possible and invested early in MCP servers (which were the one piece that didn't need to change at all). The prompts and the MCP servers moved verbatim. The orchestration rewrote cleanly once the team had the bandwidth.

### What the Case Teaches

**The framework-correct answer is often not the timing-correct answer.** A v1 that ships on a compromised stack and gets migrated is frequently better than a v1 that's architecturally pristine and ships eight months late. The decision tree gives you the destination. It doesn't always give you the sequence.

**Preserving optionality costs less than people think, if you design for it.** The two things that made the migration tractable (MCP servers for internal systems, and prompts written to be framework-agnostic) cost the v1 team roughly 10% more engineering time than the fully-vendor-coupled alternative. That 10% saved 60% on the migration.

**Observability is the hardest thing to retrofit.** The weakest part of the v1 architecture was the thin internal tracing layer. When we needed to audit a specific advisory recommendation from month 4 for a compliance review in month 11, the traces existed but weren't searchable in the way a real observability platform would have offered. If I were doing it again, I'd spend the extra three weeks to stand up Langfuse even in v1, even on the vendor SDK. Everything else you can retrofit. Trace history you can't.

**The "must migrate by Q3" clock worked.** Writing the temporary nature into the ADR, with a named migration target and a named date, is what kept the team from drifting into "the vendor SDK is working fine, why migrate?" stasis. The ADR had teeth because three senior stakeholders had signed it. Without that, the v1 stack would probably still be running.

## Epilogue: What Survives

This booklet has been a set of mental models. The layer cake. The cloud parallel. The two protocols. The two framework families. The lock-in ranges. The EU leapfrog hypothesis. The forecast with its six indicators. The five-question framework. The case study above.

In eighteen months, which of these will still be useful?

The layer cake will. The question "what layer does this sit on?" is a durable habit that pays off every time a new piece of technology gets announced. MCP will still matter; more, not less. The observability layer will be larger and more mature. A2A will either be ambient or will have been replaced by something that solves the same problem under a different name; in either case, the concept survives.

The specific frameworks are harder. LangGraph will very likely still be the agnostic default. CrewAI's future is more uncertain. ADK will continue because Google's incentives don't change. The Claude Agent SDK will have either spread or narrowed dramatically depending on how much the broader market wants Claude-specific computer-use. The OpenAI Agents SDK is the hardest to forecast; it depends on decisions inside OpenAI that we can't see. Azure and AWS will persist because their parent companies need them to.

The specific numbers will all be wrong. The 97M MCP downloads will be some larger number. The 44k CrewAI stars will have moved. The exact vendor capabilities will have drifted. Every cost figure will need revision. This is fine. The numbers are there to anchor the mental model, not to be load-bearing on their own.

What I'd tell a colleague asking how to use this book in 2027: *start with the layer cake, believe the MCP default, own your observability, respect lock-in consciously, and when you come to pick a stack, run the five questions and then be honest about which answer you can actually execute this quarter.* The rest you can update as the horizon moves.

**The specifics will change. The discipline will not.**

---

*End of booklet.*
