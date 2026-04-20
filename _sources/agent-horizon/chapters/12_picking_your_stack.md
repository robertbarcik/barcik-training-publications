# Chapter 12: Picking Your Stack

---

## A Decision Framework, Not a Beauty Contest

By this point, the landscape is mapped. MCP is the ambient protocol at the tool-access layer. A2A is the emerging protocol for agent-to-agent communication. The orchestration layer splits into vendor frameworks (ADK, OpenAI Agents SDK, Claude Agent SDK, AWS Strands, Azure AI Agent Service) and agnostic frameworks (LangGraph, CrewAI). Observability is a first-class concern. The lock-in question has sharp, per-vendor answers. The EU has specific reasons to pursue a different architecture than the US median.

What this chapter does is compress the decision. Not into a ranking — rankings age badly and mislead early. Into five questions, where your honest answers determine the architecture that fits you. Work through them in order. Each question narrows the field.

## Question 1: Where Does Your Cloud Allegiance Already Lie?

This is the first question because it usually has the largest practical impact on the final decision.

**If you are all-in on Google Cloud.** ADK is the default candidate at the orchestration layer. The Vertex AI integration, BigQuery access, and Gemini multimodal alignment are genuinely valuable, and any other framework will feel like you are fighting the ecosystem.

**If you are all-in on AWS.** AWS Strands is the natural default. Bedrock gives you model flexibility within AWS, the Lambda/DynamoDB integrations are smooth, and running a non-AWS framework on AWS is feasible but creates a long tail of integration friction.

**If you are all-in on Azure or Microsoft 365.** Azure AI Agent Service wins by default for most enterprise agent use cases, because the Microsoft 365 integrations are the main reason the agent exists in the first place.

**If you are cloud-portable or multi-cloud by policy.** The agnostic frameworks (LangGraph, CrewAI) become the natural centre of gravity. The vendor SDKs are usable but fight the neutrality goal.

This is not a lock-in concession; it is an engineering reality. Building a framework against the grain of your cloud ecosystem costs months of unnecessary integration work.

## Question 2: How Hard Is Your Model-Swap Requirement?

This question ranges from "absolutely must be able to swap models" to "happy to commit to one vendor for years."

**Hard swap requirement.** You need to route different workloads to different models — by compliance, by cost, by language, by task type — or you have a board-level mandate against being locked to a single model vendor. Go agnostic. LangGraph is the defensible default. Claude Agent SDK is immediately disqualified; the OpenAI Agents SDK is marginal at best.

**Soft swap requirement.** You prefer portability but would not rebuild everything for it. The vendor SDKs are viable, especially ADK (where swap feasibility is medium) and the OpenAI SDK (where swap is doable if you do not rely on hosted features). Strands within Bedrock also works.

**No swap requirement.** You have evaluated the trade-offs and decided that one model or one vendor is the right bet for the next two to three years. All frameworks are on the table; pick based on the other questions.

This is the question most enterprises answer in hindsight rather than upfront. A better discipline is to force the answer explicitly — in a document, with stakeholders aligned — before choosing a framework.

## Question 3: How Much Regulatory or Audit Weight Is on This Deployment?

The lighter the compliance burden, the more framework options are in play. The heavier the burden, the more the stack is determined by the compliance architecture rather than the developer preference.

**Heavy regulatory burden.** Banking, insurance, healthcare, public sector, defence, or any use case classified as high-risk under the EU AI Act. Observability and audit are non-negotiable. The framework has to support structured traces, human-in-the-loop oversight, and long-term log retention. LangGraph + LangSmith (or Langfuse self-hosted) is the most commonly defensible architecture. Vendor SDKs can be made to work but require heavier compliance engineering.

**Medium regulatory burden.** GDPR-relevant data, some sector-specific rules, an executive-level interest in audit but not a mandate. The vendor SDKs remain viable with supplemental observability tooling. The agnostic frameworks are easier to defend but the vendor options do not disqualify themselves.

**Low regulatory burden.** Internal productivity tools, non-sensitive content generation, analytics assistants. Framework choice is governed by the other questions; audit infrastructure can be lightweight.

For European enterprises, this question bites harder than for US ones. If your answer is "heavy" here, you are likely choosing between agnostic frameworks rather than between vendor and agnostic.

## Question 4: How Much Do You Need Multi-Agent Coordination?

This question is about A2A-relevance and multi-agent structure, which different frameworks handle differently.

**Yes, multi-agent is core.** You have or will have multiple specialist agents cooperating. Teams of agents. Cross-boundary delegation. A2A is important. ADK leads here, with its native A2A support and hierarchical agent structure. CrewAI is a strong second for prototyping; LangGraph handles multi-agent well but requires more explicit engineering.

**Maybe later, not today.** Start with a single-agent architecture but pick a framework with a credible multi-agent and A2A roadmap. ADK, LangGraph, and CrewAI all qualify. The OpenAI Agents SDK's handoff model also covers this territory, though with different idioms.

**Single-agent, probably always.** Simplicity is a feature. Any of the frameworks works; the LLM-in-a-loop baseline may even be adequate. Do not pay for multi-agent primitives you will not use.

The most common mistake on this question is over-estimating the multi-agent need. Many enterprises think they need multi-agent architectures because the concept sounds impressive, and end up with an over-engineered three-agent system doing work a single well-prompted agent would handle. Be honest about the shape of your problem.

## Question 5: How Much In-House AI Engineering Talent Do You Have?

This question controls how much architectural ambition your organisation can actually absorb.

**Deep in-house capability.** You have engineers who can build custom observability, write internal MCP servers, operate LangGraph in production, and handle the abstraction tax of agnostic frameworks. The full range of options is open, and the agnostic frameworks become more attractive because you can pay their cost.

**Moderate in-house capability.** A small AI-engineering team, handling one or two production agents at a time. The vendor SDKs become attractive because they absorb more of the engineering burden. An agnostic framework is viable but will consume more of your team's capacity than you may realise.

**Limited in-house capability.** You have engineers, but none of them specialise in agent development. The vendor SDKs are the correct default. The hosted features, bundled observability, and opinionated defaults compensate for the in-house gap. An agnostic framework without a team to drive it is a failed project waiting to happen.

This is the question enterprises are most tempted to answer optimistically. Be unflinching. The framework you can operate successfully is better than the framework that looks best on a slide.

## A Sample Decision

To ground the framework in a concrete example, consider a mid-sized European bank running on a mix of Azure and private cloud, building an agent to help relationship managers prepare client meetings.

**Question 1 (cloud allegiance)**: Azure-primary. Initially points toward Azure AI Agent Service.

**Question 2 (model swap)**: Hard requirement — for compliance reasons, some workloads must run on a locally-hosted model, others can go to a frontier API. The vendor SDK disqualifies itself here.

**Question 3 (regulatory burden)**: Heavy — banking sector, personal data, EU AI Act high-risk classification likely for certain advisory workflows. Observability and audit are mandatory.

**Question 4 (multi-agent)**: Multi-agent likely — a coordination agent handing off to specialist advisors, at least at the conceptual level. A2A-credible framework needed.

**Question 5 (in-house talent)**: Moderate — a small AI team, but serious about building it out.

**The resulting stack.** LangGraph at the orchestration layer (agnostic, strong multi-agent support, mature observability story). LangSmith self-hosted (or Langfuse self-hosted) for observability, running on Azure infrastructure in the EU. MCP servers for internal systems (CRM, client data, compliance documentation). Model routing: a locally-hosted open-weight model for sensitive-data tasks, Claude or GPT via API (with appropriate DPAs) for hard reasoning tasks. A2A considered for future cross-team scenarios but not prioritised for v1.

This is not the only viable answer for this hypothetical bank. But it is a defensible one, and it emerges from the questions, not from vendor-slide preferences.

## When To Revisit the Decision

A framework decision is not a one-way door, but it is not a casual choice either. The conditions that should prompt you to revisit are specific.

**A regulatory shift.** A new enforcement action under the EU AI Act, or a national-level AI governance change, may tighten requirements enough that your current framework becomes insufficient.

**A scale threshold.** Going from three agents in production to thirty changes the operational calculus. Frameworks that were adequate at low scale may stop being adequate.

**A vendor event.** A pricing change, an acquisition, a support-model shift, or a capability drop from a vendor you depend on can invalidate the original trade-off.

**An architectural inflection.** Moving into multi-agent coordination, moving into regulated workloads, or moving into sovereign-infrastructure deployment can each change the framework calculus.

Outside these triggers, resist the urge to re-litigate the framework choice. Most enterprise agent projects fail for reasons that have nothing to do with framework choice. Spend the energy on the tool surface, the evaluation harness, and the operational maturity instead.

> **What to take from this chapter:** Five questions determine your stack: cloud allegiance, model-swap requirement, regulatory weight, multi-agent need, and in-house talent. Work through them honestly and the framework falls out. The most common errors are picking a framework before answering the questions, over-estimating the multi-agent need, and optimistic answers to the in-house-talent question. Revisit the decision only when a specific trigger arises — regulatory shift, scale threshold, vendor event, architectural inflection — not because a new framework launched with a good demo.

---

*Next: [Chapter 13 — A Pragmatic Horizon](13_pragmatic_horizon.md)*
