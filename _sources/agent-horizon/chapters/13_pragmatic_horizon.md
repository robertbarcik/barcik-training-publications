# Chapter 13: A Pragmatic Horizon

---

## Why This Chapter Is Not a Roadmap

You came to this booklet looking for a map. A closing chapter that reads "do X in Q3, Y in Q4, Z by the end of 2027" would satisfy a specific kind of reader, and we have chosen deliberately not to write one.

The reason is simple. The landscape moves fast enough that anything this chapter wrote with calendar dates would be wrong by the time you read it in three months. A new framework launches. A vendor announces a foundation-backed open protocol. An EU enforcement action resets the compliance conversation. A model step-change invalidates half the architectural assumptions. Calendar-anchored advice ages badly. Principles age better.

So the closing chapter is a set of principles. Durable ones, each drawn directly from the patterns the booklet has laid out. They are intended to be useful in 2027 and 2028 as well as in 2026, regardless of which specific frameworks or models are dominant by then. If you read nothing else in this booklet, read the next eight items.

## Principle 1: Master the Layer Cake Before You Choose Anything

Most mistakes in agent architecture start upstream of the actual decision, in the confusion about what layer a given technology occupies. Is it a framework? A protocol? A model? A platform? If your team cannot answer this cleanly for every piece of technology you are considering, you will end up in category-error arguments — "should we use ADK or MCP?" — that waste engineering time and produce bad architectures.

The layer cake (orchestration / LLM / tool-and-agent access / actual systems) is the mental model that makes the rest of the decisions tractable. Invest in teaching it across your engineering team. Hold architecture reviews where every new technology proposal has to name its layer before it can be discussed on its merits. This is cheap, and it compounds for years.

## Principle 2: Treat MCP as Ambient Infrastructure

MCP is settled. It is governed by the Linux Foundation, supported by every major vendor, and heading into enterprise-readiness mode for its 2026 roadmap. The question is not "should we adopt MCP?" It is "how fast can we make MCP the default way our internal systems are reached by agents?"

Act accordingly. Build MCP servers in front of your critical internal systems. Train platform engineers in the craft of writing good MCP servers (tight tool surfaces, precise descriptions, structured errors, clean resource trees). Favour tools that ship MCP support. When an integration request lands on your desk, ask first whether an MCP server is the right shape of the answer — it usually is.

## Principle 3: Default to the Simplest Orchestration That Works

The industry's instinct is to reach for a framework immediately, often before a framework is justified. A plain LLM-in-a-loop with a clean tool surface solves more agent problems than people admit, and a vendor SDK solves most of the rest with less ceremony than an agnostic framework.

Start simple. Reach for a framework when you have a concrete reason — durability, state, multi-agent coordination, guardrails, observability — not because the framework is what "serious" agents use. Premature framework adoption is a common cause of slow projects and bloated architectures.

This principle inverts when your environment has hard requirements — compliance, multi-model routing, strict audit — that a simple approach cannot meet. In those environments, the framework is justified from the start. But "simple first" remains the disciplined default, and the burden of proof belongs to the framework, not to the simpler alternative.

## Principle 4: Own Your Observability

The framework and model you pick determines at most a third of your agent program's success. The observability, evaluation, and cost-governance practice you build determines the other two-thirds.

Own it early. Pick an observability tool (LangSmith, Langfuse, Phoenix, or a self-built equivalent) and use it from day one. Build an evaluation suite for every production agent. Attribute costs per interaction, per user, per feature. Capture quality signals and feed them back into evaluations. Do not wait until you are out of pilot — the observability choices you make in pilot constrain what you can do in production, and retrofitting them is expensive.

For European regulated deployments, this is compliance infrastructure, not engineering convenience. Build it that way from the start.

## Principle 5: Respect Lock-In as a Trade, Not a Taboo

Lock-in is not automatically bad. It is the price of velocity. An enterprise that picks a vendor SDK in 2026 and ships three customer-facing agents in 2027 has captured value that a more portable enterprise is still writing architecture documents about. In many cases, the velocity advantage is worth the migration cost.

What is important is that the trade is conscious. If you pick Claude Agent SDK, you are picking Claude. If you pick ADK, you are tilting toward Google Cloud. If you pick OpenAI Agents, you are accepting the hosted-features coupling. If you pick LangGraph, you are accepting the abstraction tax in exchange for portability. All of these are defensible. What is not defensible is pretending you did not choose — and then being surprised a year later when the implications of the choice become visible.

Make the trade consciously. Document it. Revisit it when a trigger arises.

## Principle 6: Invest in Agnostic Routing When Compliance Weight Is High

The routing pattern — an agnostic orchestration layer deciding per-interaction which model to use, where to execute, and which audit trail to write to — is the mature end-state of the regulated-enterprise architecture. It is also the most expensive architecture to build, because every layer has to be chosen and operated explicitly.

The pay-off is that the architecture survives regulatory weather. It survives vendor pricing shifts. It survives model-quality changes. It survives sovereignty mandates. For an enterprise where any of those risks is plausible, the extra upfront cost amortises quickly against the migrations it avoids.

For enterprises outside regulated industries, this architecture is over-engineered. For enterprises inside them — particularly in Europe — it is the defensible default. Know which you are.

## Principle 7: Think in Agent Cards, Even Before You Use A2A

A2A is real, but it is not yet universally adopted, and your immediate projects may not need it. That is fine. What matters is that you start writing down, for every agent you build, the structured description A2A calls an "agent card": what the agent does, what inputs it expects, what outputs it produces, what domains it covers, what it cannot do.

This discipline is useful even without A2A. It forces you to think about the boundaries of the agent rather than letting it accumulate responsibilities until it is everything. It makes handoffs easier to design. It makes the migration to A2A (or its eventual successor) cheap when the need arises. It is one of those cheap habits whose value is mostly revealed in hindsight.

## Principle 8: Build for Two to Three Years, Not Five

A final note on time horizons.

A five-year plan for your agent architecture is not useful. It will be wrong in specifics within six months. Write a two-to-three-year plan instead. That is long enough to make the investments that compound (observability, platform MCP servers, evaluation discipline, team capability) and short enough that you are not over-committing to specifics that will shift underneath you.

Within that window, optimise for reversibility at the edges and commitment at the core. The core — the observability platform, the orchestration layer, the routing logic, the audit architecture — should be something you intend to live with for the full two to three years, because migrating these is expensive and the value of stability is high. The edges — which specific models you route to, which specific MCP servers you build first, which specific agents you ship — should be things you expect to change, and the architecture should absorb those changes cheaply.

This is the same pattern that worked in cloud. The enterprises that did well were not the ones who picked the right cloud provider in 2012. They were the ones who built their commitments at the right layer — Kubernetes for portability, strong internal platforms for velocity, observability for control — and let the specifics above those layers change without pain. The agent transition rewards the same discipline, on a faster clock.

## The Horizon in One Paragraph

The agent stack in April 2026 is not settled, but its shape is. MCP is the protocol layer. A2A is the emerging peer protocol for agent-to-agent. The orchestration layer splits into vendor SDKs (fast, coupled) and agnostic frameworks (slower, portable), and the observability layer is becoming its own software category. The EU has reasons to prefer the mature architecture from the start; most other markets will live through a compressed version of the cloud lock-in cycle. The frameworks that matter today — ADK, the OpenAI Agents SDK, the Claude Agent SDK, AWS Strands, Azure AI Agent Service, LangGraph, CrewAI — will not all matter in 2028, but the layers they occupy will. Build with the layers in mind, own your observability, respect lock-in as a trade, keep things simple until you need them complex, and invest in the compounding infrastructure. The rest you can change as the horizon moves.

> **What to take from this chapter — and this booklet:** The agent stack has layers. Pick carefully at each layer, knowing what you are trading. Master the layer cake, treat MCP as ambient, default to simple orchestration, own your observability, respect lock-in consciously, invest in agnostic routing where compliance demands it, think in agent cards, and plan on a two-to-three-year horizon rather than a five-year one. The specifics will change. The discipline will not.

---

*End of booklet.*
