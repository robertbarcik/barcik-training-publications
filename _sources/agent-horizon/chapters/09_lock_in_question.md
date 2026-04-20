# Chapter 9: The Lock-In Question

---

## A Specific, Awkward Question

The framework vendors say you can swap models. The agnostic frameworks say you cannot — or, rather, that you can in theory but not in practice without paying for it with broken features and degraded behaviour. Who is right?

This chapter takes that question seriously, one vendor at a time. For each of the major vendor SDKs, we ask: if I build on this framework today with the default model, and tomorrow I decide to swap the model, how much of my agent still works? And what breaks first?

The answer turns out to be more interesting — and more variable — than the abstract lock-in debate suggests. Some vendor SDKs are almost genuinely model-agnostic. Some are marketing themselves as agnostic but have deep hidden couplings. One is explicitly trained into the model behaviour and should not even be called agnostic. The nuances matter, because they determine the real engineering cost of a migration, not the theoretical one.

> **The lock-in honesty test:** If I swap the underlying model in this framework, which of the framework's headline capabilities still work? The honest answer ranges from "most of them" to "almost none" depending on which framework you picked.

## Google ADK — Medium Lock-In (Ecosystem, Not Model)

**Nominally model-agnostic?** Yes. ADK supports non-Gemini models through its integration layer.

**What breaks when you swap?**

*Multimodal.* Gemini's multimodal capabilities (image, audio, video) are deeply integrated into ADK. Swap to a text-only model and you lose a class of use cases entirely. Swap to a multimodal model from another vendor and you pay for custom integration work to reach parity.

*Agent-card generation.* ADK auto-generates A2A agent cards based on Gemini's function-calling behaviour. Other models produce less predictable function-call outputs, which makes the auto-generated cards less reliable. You can fix it, but it becomes manual rather than automatic.

*Vertex integrations.* ADK's most frictionless integrations are with Vertex AI for deployment, BigQuery for data, and Google Cloud for compute. These do not go away when you swap models, but they become less natural if you are also moving off Google Cloud.

**What survives a model swap?** Most of the orchestration structure. The hierarchical agent tree, the Sequential/Parallel/Loop primitives, the visual debugger, the agent-to-agent scaffolding — all continue to function, just with more manual work at the edges.

**Honest verdict.** ADK's lock-in is medium. The framework itself is moderately portable; the ecosystem around it is not. If you run ADK on Google Cloud with Gemini, you get the full experience. If you run ADK on AWS with Claude, you get a diminished experience that may not be worth the remaining value.

## OpenAI Agents SDK — High Lock-In (Hosted Features)

**Nominally model-agnostic?** Partially. The SDK can be pointed at non-OpenAI models through routing proxies like LiteLLM. The mechanism exists.

**What breaks when you swap?**

*Hosted tools.* The SDK's web search, file search, and code interpreter are OpenAI-hosted capabilities. They disappear the moment you swap providers.

*Sandbox execution.* The managed sandbox for code execution runs on OpenAI infrastructure. Swap providers and you either lose the sandbox entirely or rebuild it yourself (at non-trivial engineering cost).

*Handoff reliability.* The SDK's handoff mechanism relies on OpenAI's structured output and function-calling reliability. Other models handle structured output, but not always with the same reliability profile — subtle changes in model behaviour can make previously-working handoffs flaky.

*Voice and Realtime API.* The Realtime API is OpenAI-specific. Voice use cases are effectively OpenAI-only in this SDK.

**What survives a model swap?** The basic agent and handoff primitives continue to function. Simple, text-only agents with custom tools can run on non-OpenAI models through the SDK with modest friction.

**Honest verdict.** OpenAI Agents SDK is high lock-in, but the lock-in is more about *hosted features* than about model behaviour. If you are not using the hosted tools, the sandbox, or voice, the SDK is more portable than its reputation. If you are — and most compelling OpenAI-SDK use cases *are* — the migration cost is substantial.

## Claude Agent SDK — Very High Lock-In (Model Behaviour)

**Nominally model-agnostic?** No, and Anthropic does not pretend otherwise. The SDK is named for Claude, built around Claude's training, and presumes Claude underneath.

**What breaks when you swap?**

*Computer-use fidelity.* Claude has been specifically trained on computer-use tasks (reading screens, running commands, navigating file systems). Other models have not had equivalent training. Running Claude Agent SDK workflows through a non-Claude model produces unpredictable output — the model may hallucinate screen coordinates, misunderstand Bash semantics, or fail at the file-manipulation tasks Claude handles cleanly.

*The built-in tools.* The eight built-in tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch) are designed around the prompt patterns Claude responds to well. They work with other models but the precision and safety degrade noticeably.

*Long-running session behaviour.* Claude's context compaction behaviour — how the model reasons about what is relevant to keep as a long session extends — is trained into the model. Other models handle long contexts differently, sometimes worse.

*Hooks and subagents.* These structural primitives work fine with any model, but the benefit of the structure is partially dependent on the model's reliability at following the hook contracts, which again is Claude-specific training.

**What survives a model swap?** Not much, if you want the framework's headline capabilities. Basic tool-calling agents can run through the SDK on other models, but that is a small fraction of what Claude Agent SDK is designed to do.

**Honest verdict.** Claude Agent SDK is the deepest lock-in of any framework in this chapter — and honestly, that is by design. It is not a generic agent framework that happens to come from Anthropic. It is a framework specifically built to exploit Claude's training. If you pick it, you are picking Claude. That is a reasonable bet if you have already made that decision; it is a bad bet if you need portability.

## AWS Strands — Cloud Lock-In, Model Flexibility

**Nominally model-agnostic?** Yes, within the Bedrock universe. Strands uses Bedrock for model access, which means native support for Claude, Llama, Mistral, and other Bedrock-hosted models.

**What breaks when you swap?**

*Swapping models within Bedrock is relatively painless.* This is one of Strands's strongest design features. If you want to run the same agent on Claude today and Llama tomorrow, Strands supports that more gracefully than any of the foundation-vendor SDKs.

*Swapping off Bedrock breaks the framework.* The cost is at the cloud layer, not the model layer. Strands assumes Bedrock for model access, Lambda for tool execution, DynamoDB for state. Leave AWS and you are rewriting the deployment from scratch.

**What survives?** Within AWS, everything. Outside AWS, almost nothing.

**Honest verdict.** Strands has inverted the lock-in of the foundation-vendor frameworks. Instead of being locked to a model and flexible on cloud, it is flexible on model (within Bedrock) and locked to cloud (AWS). For AWS-native enterprises, this is often the best fit in the vendor-framework category. For cloud-portable enterprises, it is the worst.

## Azure AI Agent Service — Microsoft Ecosystem Lock-In

**Nominally model-agnostic?** Partially. The service leans on OpenAI models through Microsoft's partnership, but non-OpenAI options exist.

**What breaks when you swap?**

*Microsoft 365 integrations.* The deep integrations with SharePoint, Teams, Outlook, and the Microsoft 365 surface are the main reason you chose Azure AI Agent Service. They do not depend on a specific model, but they are useless outside the Microsoft ecosystem.

*Compliance and identity.* Microsoft's enterprise compliance infrastructure is a feature of the service. You do not lose it by swapping models, but you lose it entirely if you leave Azure.

*Managed runtime.* Azure AI Agent Service runs on Azure. The managed service does not port to AWS or GCP.

**What survives?** The agent logic itself can be rewritten on another platform, but the entire reason to use Azure AI Agent Service — the Microsoft ecosystem depth — does not travel.

**Honest verdict.** Azure AI Agent Service is ecosystem lock-in, not model lock-in. The service is valuable to the extent that you are committed to the Microsoft enterprise ecosystem. If you are, the lock-in is a feature. If you are trying to stay neutral, it is a trap.

## A Summary Matrix

| Framework | Nominal Agnosticism | Actual Lock-In Depth | What Breaks First on Model Swap |
|---|---|---|---|
| Google ADK | Yes | Medium (ecosystem) | Multimodal, auto-A2A cards, Vertex integrations |
| OpenAI Agents SDK | Partial | High (hosted features) | Hosted tools, sandbox, voice, handoff reliability |
| Claude Agent SDK | No | Very High (model behaviour) | Computer-use, built-in tools, long-session behaviour |
| AWS Strands | Yes (within Bedrock) | Cloud lock-in, model-flexible | Leaves AWS and nothing survives |
| Azure AI Agent Service | Partial | Microsoft ecosystem lock-in | Microsoft 365 integrations, Azure runtime |
| LangGraph | Yes | Low | Minimal — this is the design goal |
| CrewAI | Yes | Low | Minimal — this is the design goal |

## Why Lock-In Is Not Always a Problem

Before declaring all vendor frameworks disqualified, it is worth making a symmetric point. Lock-in is not automatically bad. It is a trade, like any other.

Enterprises that locked into AWS in 2010 had a more expensive migration story in 2018 than enterprises that used Kubernetes from day one. They also shipped faster in 2010, 2011, 2012, 2013, and 2014 — and captured business value during those years that the more portable enterprises were still writing architecture documents about. In many cases, the velocity advantage compounded faster than the lock-in cost accumulated.

The same logic applies today. An enterprise that picks the OpenAI Agents SDK in 2026 and ships three customer-facing agents by Q2 2027 has captured value that an enterprise still arguing about LangGraph vs CrewAI has not. If the eventual migration off OpenAI is expensive — and it might be — that is a future cost to weigh against a present benefit.

The lock-in question, honestly asked, is not "will there be a cost?" The answer is yes. The question is "how does the cost of this future migration compare to the value I capture in the meantime?" For many enterprises, the math is favourable. For others — particularly those in regulated industries where the future migration may be involuntary and urgent — the math is unfavourable, and they should invest in portability from day one.

## When Lock-In Becomes a Structural Problem

A few conditions tip the math toward portability being worth the cost.

**Regulatory risk of forced migration.** If a new regulation (EU AI Act, national-level AI governance, sector-specific rules) could plausibly force you off a specific vendor, you need the portability before the regulation, not after.

**Pricing power of the vendor.** If your agent workload becomes dependent on a single vendor and that vendor can raise prices unilaterally, you have handed over your margin. Portability is leverage in that negotiation.

**Strategic importance of the workload.** A stake-the-company agent deployment has higher migration risk than a departmental automation. The further up the business-critical spectrum, the more the portability insurance is worth.

**Data sovereignty and sovereign AI.** If your regulatory environment may require you to run workloads on sovereign infrastructure, the vendor frameworks that assume their own infrastructure underneath become liabilities.

Outside these conditions, the lock-in penalty of a vendor framework is a real but manageable cost. Inside them, the cost is strategic, not operational — and strategic costs are the ones that put CEOs in uncomfortable board meetings.

> **What to take from this chapter:** "Model-agnostic" in vendor-framework marketing usually means "you can technically swap the model" — not "the framework's headline capabilities survive the swap." The lock-in ranges from low (LangGraph, CrewAI) to medium (ADK) to high (OpenAI Agents SDK) to very high (Claude Agent SDK). AWS and Azure have their own pattern: model-flexible, cloud-locked. For most enterprises, the vendor lock-in is a price worth paying for velocity, until it isn't — and the conditions under which it isn't are regulatory risk, vendor pricing power, workload criticality, and data sovereignty. Know which of those apply to you before committing.

---

*Next: [Chapter 10 — The EU Angle](10_eu_angle.md)*
