# Chapter 4: The Orchestration Layer

---

With both protocols covered, the stack's bottom floors are in place. The LLM can reason. MCP can reach tools and data. A2A can reach other agents. But something still has to decide *what the agent actually does*: which tool to call first, what to do if it fails, when to stop, when to ask the user, when to hand off.

This is the orchestration layer. It's where the brain lives. And it's the layer where most of the interesting framework arguments happen, because unlike the protocol layer (settled around MCP) and the model layer (a handful of dominant vendors), the orchestration layer is still genuinely contested.

Before we survey frameworks in the next two chapters, a more fundamental question: do you need a framework at all?

## The LLM-in-a-Loop Baseline

The simplest possible agent architecture has no framework. It's a while-loop, a language model with function-calling support, and a list of tools:

1. Send the user's request, the tool catalogue, and any prior conversation to the model.
2. Model either returns a final answer (stop) or a tool call (continue).
3. If tool call, execute it, append the result to the conversation, go to 1.

That's it. No framework. No graph. No handoffs. For a surprisingly large class of enterprise use cases, this is adequate. It handles most chatbot-style assistants, most "agent over a specific tool surface" cases, most short-running tasks with fewer than a dozen tools.

This matters because the industry's instinct is to reach for a framework immediately, often before the use case requires one. A framework has real costs: learning curve, abstraction tax, a layer of indirection between you and the model, production archaeology when something goes wrong. If you don't need those costs yet, don't pay them.

**The first honest question in any agent project is whether you've actually tried an LLM-in-a-loop with good prompts and a clean tool surface. If not, you don't yet know whether you need a framework.**

In the cloud analogy, an LLM-in-a-loop is a plain EC2 instance with your own scripts. Not sophisticated, not impressive in a design review, often exactly the right tool for the job, and underused because it's unfashionable.

## When the Baseline Breaks

The baseline starts to hurt in a predictable set of scenarios. When you hit these, a framework earns its keep.

**Non-trivial control flow.** The model needs to plan, execute steps in parallel, then synthesise. Or a retry policy with backoff for one specific tool. Or a branch where the model decides between two sub-workflows. Expressing these cleanly in a loop gets ugly fast.

**State and memory across turns.** A loop with a long conversation keeps stuffing everything into the prompt until the context window overflows. A framework can maintain explicit state, summarise older history, checkpoint progress, and resume from a saved state. For any agent that lives longer than a single session, state management isn't optional.

**Multi-agent coordination.** Once you have more than one agent, the baseline becomes wrong. Frameworks offer structured patterns for supervisor/worker hierarchies, specialist teams, A2A-mediated delegation. Building these without a framework is possible but rarely a good use of effort.

**Guardrails and callbacks.** Production agents need hooks. "Before any tool call, check permissions." "After the model responds, run a bias/PII filter." "If the agent spends more than five euros, stop and ask." Frameworks give you named lifecycle points. A loop forces you to sprinkle the same checks throughout the code, which rots quickly.

**Durability.** A thirty-second process is fine in a loop. An eight-hour process isn't; if the server restarts, you lose everything. LangGraph offers durable execution: state checkpointed, long-running agents pause and resume, crashes recoverable. Serious engineering concern for agents that do real work at scale.

**Observability and evaluation.** Production agents need traces, token-cost attribution, quality metrics, replayability. Frameworks either provide this or integrate with tools (LangSmith, Langfuse, Phoenix) that do. Rolling your own is a sizeable project, and one covered in its own chapter (Chapter 7).

Hit several of these at once and a framework stops being nice-to-have and becomes necessary infrastructure. Hit none and it's mostly dead weight.

## The Two Families

If you need a framework, the core decision of this booklet arrives: which one?

As of 2026, the landscape has clarified into two broad families.

**The vendor frameworks.** Google ADK, OpenAI Agents SDK, Claude Agent SDK, AWS Strands, Azure AI Foundry Agent Service. Each built by an infrastructure or foundation-model vendor, each optimised for its creator's ecosystem. Pitch: developer velocity. Play the role AWS Elastic Beanstalk and Google App Engine played: opinionated, fast, and vendor-aligned.

**The agnostic frameworks.** LangGraph, CrewAI, and a small number of quieter contenders. Model-agnostic and cloud-agnostic. Pitch: portability and control. Play the role Kubernetes and Docker Compose played: more control, more work, more future-proofing.

Neither family is "better." They solve different problems. Vendor frameworks are for teams that want to ship quickly and have made peace with a vendor commitment. Agnostic frameworks are for teams that want long-term portability and will pay the abstraction tax for it.

The next two chapters cover each family in turn: Chapter 5 surveys the vendors; Chapter 6 covers the agnostic ones and engages with the "models got too good" counter-argument that's been gaining currency.

## One More Mental-Model Correction

It's easy (especially for developers coming from traditional software) to think of the orchestration layer as "the agent." It isn't. The orchestration layer is the manager. The actual intelligence is in the LLM layer below it. The actual capability is in the tools and data exposed via MCP. The actual value is produced by the systems at the bottom. A good framework is valuable the way a good project manager is valuable: it makes a team of smart specialists work well together. And no framework, however polished, rescues weak specialists.

The corollary: when agent projects fail, the instinct is often to switch frameworks. This is almost always wrong. The failure is usually in the tool surface, the prompt design, the evaluation harness, or the model choice, not the orchestrator. Diagnose first. **If your first instinct when an agent misbehaves is to reach for a different framework, you're probably treating the wrong disease.**

---

*Next: [Chapter 5: The Vendor Frameworks](05_vendor_frameworks.md)*
