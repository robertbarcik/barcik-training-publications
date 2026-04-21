# Chapter 8: The Lock-In Question

---

The framework vendors say you can swap models. The agnostic frameworks say you can't — or, rather, that you can in theory but not in practice without broken features and degraded behaviour. Who is right?

This chapter takes the question seriously, one vendor at a time. For each major vendor SDK: if you build on it today with the default model, and tomorrow you decide to swap the model, how much of your agent still works? And what breaks first?

The answer is more variable than the abstract lock-in debate suggests. Some vendor SDKs are almost genuinely model-agnostic. Some market themselves as agnostic but have deep hidden couplings. One is explicitly trained into model behaviour and shouldn't even be called agnostic. The nuances matter because they determine the real engineering cost of a migration, not the theoretical one.

**The lock-in honesty test:** if I swap the underlying model in this framework, which of the framework's headline capabilities still work? The honest answer ranges from "most" to "almost none."

## Google ADK — Medium Lock-In (Ecosystem, Not Model)

Nominally model-agnostic, and it is in the basic case. But three headline capabilities degrade on a swap.

*Multimodal* — deeply integrated into ADK through Gemini's API. Swap to a text-only model and you lose a class of use cases entirely. Swap to a multimodal model from another vendor and you pay for custom integration work to reach parity.

*Agent-card generation* — ADK auto-generates A2A cards based on Gemini's function-calling behaviour. Other models produce less predictable function-call outputs, which makes the auto-generated cards less reliable. You can fix it, but it becomes manual rather than automatic.

*Vertex integrations* — ADK's most frictionless integrations are with Vertex AI for deployment, BigQuery for data, Google Cloud for compute. These don't go away on a model swap, but they become less natural if you're also moving off Google Cloud.

The orchestration structure (hierarchical agent tree, Sequential/Parallel/Loop primitives, visual debugger) continues to function on other models — just with more manual work at the edges.

**Verdict**: medium lock-in. The framework itself is moderately portable; the ecosystem around it isn't.

## OpenAI Agents SDK — High Lock-In (Hosted Features)

Partially agnostic. The SDK can be pointed at non-OpenAI models through routing proxies like LiteLLM. Mechanism exists. What breaks on a swap:

*Hosted tools* — web search, file search, code interpreter are OpenAI-hosted. Disappear the moment you swap providers.

*Sandbox execution* — the managed sandbox for code execution runs on OpenAI infrastructure. Swap providers and you either lose the sandbox or rebuild it yourself at non-trivial cost.

*Handoff reliability* — the handoff mechanism relies on OpenAI's structured-output and function-calling reliability. Other models handle structured output, but not always with the same reliability profile. Subtle changes can make previously-working handoffs flaky.

*Voice and Realtime API* — OpenAI-specific. Voice use cases are effectively OpenAI-only.

Basic agent and handoff primitives continue to function on other models. Simple text-only agents with custom tools run on non-OpenAI models with modest friction.

**Verdict**: high lock-in, but more about *hosted features* than *model behaviour*. If you're not using the hosted tools, sandbox, or voice, the SDK is more portable than its reputation. If you are — and most compelling OpenAI-SDK use cases *are* — the migration cost is substantial.

## Claude Agent SDK — Very High Lock-In (Model Behaviour)

Not agnostic, and Anthropic doesn't pretend otherwise. The SDK is named for Claude, built around Claude's training, presumes Claude underneath.

*Computer-use fidelity* — Claude has been specifically trained on computer-use tasks (reading screens, running commands, navigating file systems). Other models haven't had equivalent training. Running Claude Agent SDK workflows through a non-Claude model produces unpredictable output — hallucinated screen coordinates, misunderstood Bash semantics, failed file manipulation.

*Built-in tools* — the eight tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch) are designed around prompt patterns Claude responds to well. They work with other models but precision and safety degrade noticeably.

*Long-running session behaviour* — Claude's context compaction is trained into the model. Other models handle long contexts differently, sometimes worse.

*Hooks and subagents* — these structural primitives work with any model, but the benefit depends on model reliability at following hook contracts, which is Claude-specific training.

**Verdict**: the deepest lock-in of any framework in this chapter — and honestly, that's by design. Not a generic agent framework that happens to come from Anthropic. A framework specifically built to exploit Claude's training. Pick it and you're picking Claude. That's a reasonable bet if you've already made that decision; it's a bad bet if you need portability.

## AWS Strands — Cloud Lock-In, Model Flexibility

Inverted. Uses Bedrock for model access, which means native support for Claude, Llama, Mistral, and other Bedrock-hosted models.

*Swapping within Bedrock is relatively painless* — one of Strands's strongest design features. Want to run the same agent on Claude today and Llama tomorrow? Strands supports it more gracefully than any foundation-vendor SDK.

*Swapping off Bedrock breaks the framework.* The cost is at the cloud layer, not the model layer. Strands assumes Bedrock for models, Lambda for tools, DynamoDB for state. Leave AWS and you're rewriting the deployment from scratch.

**Verdict**: inverted lock-in from the foundation-vendor frameworks. Flexible on model (within Bedrock), locked to cloud (AWS). For AWS-native enterprises, often the best fit in the vendor-framework category. For cloud-portable enterprises, the worst.

## Azure AI Agent Service — Microsoft Ecosystem Lock-In

Partially model-agnostic. Leans on OpenAI models through the Microsoft partnership, but non-OpenAI options exist.

*Microsoft 365 integrations* — SharePoint, Teams, Outlook, the whole M365 surface. Main reason you chose the service. Don't depend on a specific model but are useless outside the Microsoft ecosystem.

*Compliance and identity* — Microsoft's enterprise compliance infrastructure is a feature of the service. Don't lose it on a model swap, lose it entirely leaving Azure.

*Managed runtime* — runs on Azure. The managed service doesn't port.

**Verdict**: ecosystem lock-in, not model lock-in. Valuable to the extent you're committed to the Microsoft enterprise ecosystem. If you are, a feature. If you're trying to stay neutral, a trap.

## Summary

| Framework | Nominal | Actual Depth | What Breaks First on Model Swap |
|---|---|---|---|
| Google ADK | Yes | Medium (ecosystem) | Multimodal, auto-A2A cards, Vertex integrations |
| OpenAI Agents SDK | Partial | High (hosted features) | Hosted tools, sandbox, voice, handoff reliability |
| Claude Agent SDK | No | Very High (model behaviour) | Computer-use, built-in tools, long-session behaviour |
| AWS Strands | Yes within Bedrock | Cloud lock-in | Leaves AWS and nothing survives |
| Azure AI Agent Service | Partial | Microsoft ecosystem | M365 integrations, Azure runtime |
| LangGraph | Yes | Low | Minimal — this is the design goal |
| CrewAI | Yes | Low | Minimal — this is the design goal |

## Lock-In Is Not Always a Problem

Before declaring all vendor frameworks disqualified, a symmetric point. Lock-in isn't automatically bad. It's a trade.

Enterprises that locked into AWS in 2010 had a more expensive migration in 2018 than enterprises that used Kubernetes from day one. They also shipped faster in 2010, 2011, 2012, 2013, 2014 — and captured business value during those years that the more portable enterprises were still writing architecture documents about. In many cases, the velocity advantage compounded faster than the lock-in cost accumulated.

Same logic today. An enterprise that picks OpenAI Agents SDK in 2026 and ships three customer-facing agents by Q2 2027 has captured value an enterprise still arguing about LangGraph vs CrewAI hasn't. If the eventual migration off OpenAI is expensive — and it might be — that's a future cost to weigh against a present benefit.

**The lock-in question, honestly asked, is not "will there be a cost?" The answer is yes. The question is "how does the cost of this future migration compare to the value I capture in the meantime?"** For many enterprises the math is favourable. For others — particularly regulated, where the future migration may be involuntary and urgent — the math is unfavourable, and they should invest in portability from day one.

## When Lock-In Becomes Structural

Four conditions tip the math toward portability being worth the cost.

**Regulatory risk of forced migration.** A new regulation could plausibly force you off a specific vendor. You need the portability *before* the regulation, not after.

**Pricing power of the vendor.** Your workload becomes dependent on a single vendor, and they can raise prices unilaterally. You've handed over your margin. Portability is leverage.

**Strategic importance of the workload.** A stake-the-company deployment has higher migration risk than departmental automation. Further up the business-critical spectrum, the more portability insurance is worth.

**Data sovereignty.** Your regulatory environment may require sovereign infrastructure. Vendor frameworks that assume their own infrastructure underneath become liabilities.

Outside these conditions, vendor lock-in is a real but manageable cost. Inside them, the cost is strategic, not operational — and strategic costs are the ones that put CEOs in uncomfortable board meetings.

> **What to take from this chapter:** "Model-agnostic" in vendor-framework marketing usually means "you can technically swap the model" — not "the framework's headline capabilities survive the swap." Lock-in ranges from low (LangGraph, CrewAI) to medium (ADK) to high (OpenAI Agents SDK) to very high (Claude Agent SDK). AWS and Azure invert the pattern: model-flexible, cloud-locked. For most enterprises, vendor lock-in is a price worth paying for velocity, until it isn't — and the conditions under which it isn't are regulatory risk, vendor pricing power, workload criticality, and data sovereignty. Know which of those apply to you before committing.

---

*Next: [Chapter 9 — The EU Angle](09_eu_angle.md)*
