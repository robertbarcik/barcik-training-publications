# Chapter 5: The Orchestration Layer

---

## Where the Brain Lives

With the two protocols covered, the stack has its bottom floors in place. The LLM can reason. MCP can reach tools and data. A2A can reach other agents. But something still has to decide *what the agent actually does*. Which tool to call first. What to do if the tool fails. When to stop. When to ask the user for confirmation. When to hand off to a sub-agent. How to persist state across a conversation.

This is the orchestration layer. It is where the brain lives. And it is the layer where most of the interesting framework arguments play out — because unlike the protocol layer (settled around MCP) and the model layer (a handful of dominant vendors), the orchestration layer is still genuinely contested.

Before we survey the frameworks in Chapters 6 and 7, it is worth pausing on a more fundamental question: do you need a framework at all?

## The LLM-in-a-Loop Baseline

The simplest possible agent architecture has no framework in it. It is a while-loop, a language model with function-calling support, and a list of tools. The loop looks roughly like this, in pseudocode rather than real syntax:

1. Send the user's request, plus the tool catalogue, plus any prior conversation, to the model.
2. The model responds either with a final answer (stop) or with a tool call request (continue).
3. If it is a tool call, execute the tool, append the result to the conversation, go to step 1.

That is it. No framework. No graph. No handoffs. No role definitions. Just a loop. And for a surprisingly large class of enterprise use cases, this architecture is adequate. It handles most chatbot-style use cases, most "assistant over a specific tool surface" use cases, most short-running tasks with fewer than a dozen tools.

This matters because the industry's instinct is to reach for a framework immediately, often before the use case requires one. A framework has non-trivial costs: learning curve, abstraction tax, a layer of indirection between you and the model, production archaeology when something goes wrong. If you do not need those costs yet, do not pay them.

> **The first honest question in any agent project:** Have I actually tried an LLM-in-a-loop with good prompts and a clean tool surface? If not, I do not yet know whether I need a framework.

In the cloud analogy, an LLM-in-a-loop is the equivalent of running a plain EC2 instance with your own scripts. It is not sophisticated. It is not impressive in a design review. It is often exactly the right tool for the job, and it is underused because it is unfashionable.

## When the Baseline Breaks

The LLM-in-a-loop architecture starts to hurt in a predictable set of scenarios. When you hit these, that is when a framework earns its keep.

**Non-trivial control flow.** Some tasks have structure that does not fit a single linear loop. You need the model to plan, then execute each step in parallel, then synthesise the results. Or you need a retry policy with backoff for one specific tool. Or you need a branch where the model decides between two very different sub-workflows and the framework needs to route accordingly. Expressing these cleanly in a loop gets ugly fast. Frameworks exist precisely to give you the vocabulary for expressing them cleanly — as graphs, as pipelines, as sequences, depending on the framework's philosophy.

**State and memory across turns.** A loop with a long conversation can keep throwing everything into the prompt until the context window overflows. A framework can maintain explicit state, summarise older history, checkpoint progress, and resume from a saved state. For any agent that lives longer than a single session — a support agent, a research assistant, a long-running automation — state management is not optional, and building it from scratch in your loop is not where you want to spend your engineering time.

**Multi-agent coordination.** Once you have more than one agent, the LLM-in-a-loop baseline becomes genuinely wrong. Frameworks offer structured patterns for supervisor/worker hierarchies, specialist teams, and A2A-mediated delegation. Building these without a framework is possible but rarely a good use of effort.

**Guardrails and callbacks.** Production agents need hooks. "Before any tool call, check the user's permissions." "After the model responds, run a bias/PII filter." "If the agent spends more than five dollars, stop and ask for confirmation." Frameworks give you named lifecycle points where these hooks plug in cleanly. A loop forces you to sprinkle the same checks throughout the code, which rots quickly.

**Durability.** A process that takes thirty seconds is fine in a loop. A process that takes eight hours is not — if the server restarts, you lose everything. Frameworks like LangGraph offer durable execution: state is checkpointed, long-running agents can pause and resume, crashes are recoverable. This is a serious engineering concern for any agent that does real work at scale.

**Observability and evaluation.** Production agents need traces, token-cost attribution, quality metrics, and the ability to replay a past run to debug it. Frameworks either provide this directly or integrate with observability tools (LangSmith, Langfuse, Phoenix) that do. Rolling your own is a sizeable project.

When you hit several of these at once, a framework stops being a nice-to-have and becomes necessary infrastructure. When you hit none of them, a framework is mostly dead weight.

## The Two Families of Frameworks

If you have decided you need a framework, you now face the core decision of this booklet: which one?

As of 2026, the framework landscape has clarified into two broad families, with different assumptions about where you sit in the stack.

**The vendor frameworks.** Google ADK, OpenAI Agents SDK, Claude Agent SDK, AWS Strands, Azure AI Agent Service. Each is built by an infrastructure vendor or a foundation model vendor, and each is optimised for its creator's ecosystem. Their pitch is developer velocity: if you are willing to use the vendor's model (or cloud) as your default, the framework removes most of the friction from building agents. They play the same role in the agent stack that AWS Elastic Beanstalk or Google App Engine played in the cloud stack — opinionated, fast, and vendor-aligned.

**The agnostic frameworks.** LangGraph, CrewAI, and a small number of quieter contenders. These are model-agnostic and cloud-agnostic. Their pitch is portability and control: you can swap models, swap vendors, and keep your agent architecture intact. They play the role that Kubernetes and Docker Compose played in the cloud stack — more control, more work, more future-proofing.

Neither family is "better." They solve different problems. The vendor frameworks are optimised for teams that want to ship quickly and have already made peace with a vendor commitment. The agnostic frameworks are optimised for teams that want long-term portability and are willing to pay the abstraction tax for it.

The next two chapters cover each family in detail: Chapter 6 surveys the vendor frameworks; Chapter 7 covers the agnostic ones and engages directly with the "models got too good" counter-argument that has been gaining currency.

## The Orchestration Layer Is Not Everything

One more mental-model correction before we move on.

It is easy — especially for developers coming from a traditional software background — to think of the orchestration layer as "the agent." It is not. The orchestration layer is the manager. The actual intelligence is in the LLM layer below it. The actual capability is in the tools and data exposed via MCP below that. And the actual value is produced by the systems at the bottom.

A good framework is valuable the way a good project manager is valuable: it makes a team of smart specialists work well together. A bad framework is valuable the way a bad project manager is valuable: not at all. And no framework, however polished, can fix the problem of the specialists themselves being weak. If your model is mediocre or your tool surface is poorly designed, no orchestration layer will rescue the agent.

The corollary is important. When agent projects fail, the instinct is often to switch frameworks. This is almost always wrong. The failure is usually in the tool surface, the prompt design, the evaluation harness, or the model choice — not in the orchestrator. Changing frameworks is expensive and rarely fixes the real problem. Diagnose first.

> **What to take from this chapter:** The orchestration layer is where the agent's control flow lives. Before reaching for a framework, try an LLM-in-a-loop — for many use cases, it is enough. Reach for a framework when you hit non-trivial control flow, serious state/memory needs, multi-agent coordination, guardrail and callback requirements, durability needs, or production observability demands. The framework landscape splits into two families — vendor and agnostic — and the choice between them is the central decision of your agent stack. The next two chapters unpack each family in turn.

---

*Next: [Chapter 6 — The Vendor Frameworks](06_vendor_frameworks.md)*
