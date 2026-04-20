# Chapter 7: The Agnostic Frameworks

---

## The Kubernetes of the Agent Era

There is a smaller — and noisier — corner of the agent-framework landscape where the defining feature is *not* being aligned with a model vendor. These are the agnostic frameworks: they assume from day one that you will want to swap models, cloud providers, and tool surfaces, and they optimise for that flexibility even at the cost of developer velocity.

Two frameworks dominate this corner: LangGraph and CrewAI. They both predate most of the vendor SDKs covered in the previous chapter, both have larger communities than any single vendor framework, and both are currently positioning themselves as the neutral middle layer — the Switzerland, as one discussion we drew on for this booklet put it — that large enterprises will eventually want between themselves and the foundation-model vendors.

The cloud analogy holds here again, and it holds tightly. If the vendor frameworks are PaaS, the agnostic frameworks are the container orchestration layer: LangGraph is Kubernetes, and CrewAI is Docker Compose.

## LangGraph as Kubernetes

**The pitch.** "Bulletproof production agents, model-agnostic by design."

**The design philosophy.** LangGraph treats agent workflows as state machines. You define nodes (steps in the workflow) and edges (transitions between them). State flows through the graph. The framework is explicit about persistence: at every step, the state is checkpointed, so if the server crashes or the agent pauses for human approval, the workflow resumes from exactly where it left off. LangGraph's insistence on this structural explicitness is what gives it its power — and also what generates the most complaints.

**What it is genuinely good at.**

*Durable execution.* This is LangGraph's defining capability. Long-running agents can pause for hours or days, wait for human input, survive server restarts, and resume without losing state. For enterprise use cases — regulatory approvals, multi-step workflows with human-in-the-loop steps, agents that run overnight — this is often the only tractable solution.

*Observability and audit.* LangGraph pairs naturally with LangSmith (covered in Chapter 8), which provides deep traces, evaluation harnesses, and audit-grade records of every model call, every tool invocation, and every state transition. For regulated enterprises, this paper trail can be the difference between a deployable agent and a blocked one.

*Model agnosticism.* LangGraph does not care whether the underlying model is Claude, GPT, Gemini, Mistral, or a local Llama. The framework's primitives are model-neutral. You can swap the model layer without rewriting the workflow — which is the entire point.

*Production scale.* LangGraph has the most mature production story of any agent framework. More than 400 production deployments are publicly documented, including high-scale cases like Klarna's customer support agent handling 85 million users with 80% reduction in resolution time. The framework has accumulated the boring reliability features (connection pooling, retry semantics, backoff, rate limiting) that matter more in production than in demos.

**The cost.** LangGraph has a real learning curve. Developers coming from a "just write the agent code" instinct find LangGraph's graph formalism verbose for simple cases. Critics call it "a very fancy if-else statement" — and for a three-step linear agent, they have a point. LangGraph's value shows up at scale, in production, under edge conditions, not in demos.

**Who should take LangGraph seriously.** Regulated enterprises, long-running or human-in-the-loop agents, multi-model routing architectures, organisations where vendor-lock-in is a real concern at the board level, and teams large enough to absorb the learning curve and benefit from the structure.

## CrewAI as Docker Compose

**The pitch.** "A team of specialist agents, spun up in an afternoon."

**The design philosophy.** CrewAI organises work the way a human team does. You create agents, give each one a role ("Senior Data Analyst"), a goal ("find trends in Q2 sales data"), and a backstory ("You have ten years of experience in retail analytics"). You assemble agents into a "crew" and give the crew a task. CrewAI orchestrates the team.

The mental model is disarmingly friendly. Business stakeholders can read a CrewAI agent definition and understand what is happening. This friendliness is both the framework's greatest strength and its greatest weakness.

**What it is genuinely good at.**

*Prototyping speed.* Nothing in the agnostic category — and very little in the vendor category — can get a multi-agent prototype running as fast as CrewAI. For workshops, proofs-of-concept, and "show me what this could look like" demos, CrewAI is often the fastest path.

*Role-based reasoning.* For tasks where the natural breakdown is "a team of specialists," the role-based abstraction is genuinely elegant. Research tasks, content creation pipelines, analysis workflows — anywhere the work decomposes naturally into specialist roles — CrewAI fits the shape.

*Protocol support.* CrewAI added native MCP and A2A support earlier than most frameworks, reflecting its multi-agent-first design. For teams building around open protocols, CrewAI is a natural fit.

*Community momentum.* 44,000+ GitHub stars, active Discord, a growing commercial ecosystem. The community size means a wealth of examples, recipes, and patterns you can borrow.

**The cost.** CrewAI's abstractions are optimised for prototyping, not for production. State management is thinner than LangGraph's. Checkpointing and durability are limited. For a long-running, mission-critical agent where reliability is paramount, CrewAI forces you to solve enterprise concerns outside the framework — at which point the framework's main value (quick prototyping) has been outgrown.

**Who should take CrewAI seriously.** Teams running rapid POCs and workshops, multi-agent workflows where the role-based decomposition fits naturally, and any project where time-to-demo matters more than time-to-five-nines.

## The Quieter Contenders

A handful of other frameworks occupy the agnostic category but have smaller footprints. A complete picture should acknowledge them without overselling their current adoption.

**Mastra** and **Agno** are newer frameworks competing on model agnosticism with different opinions about memory and agent lifecycle.

**Semantic Kernel** (from Microsoft, open-source) predates much of this space and still has followers, particularly in enterprises bridging to the Microsoft ecosystem without going all-in on Azure AI Agent Service.

**Pydantic AI** is a newer entrant from the Pydantic team with a focus on type-safe agent composition.

These frameworks matter in specific niches but do not currently compete with LangGraph or CrewAI at scale. A five-year outlook might change this; a twelve-month outlook does not.

## "But Models Got Too Good" — the Counter-Argument

Before anyone adopts an agnostic framework, they should understand the strongest argument against doing so. It goes like this.

Agnostic frameworks like LangGraph exist in part because early LLMs were weak. Context windows were small, so frameworks added summarisation and memory management. Reasoning was unreliable, so frameworks added structured control flow. Function calling was crude, so frameworks added tool-validation scaffolding. Hallucinations were frequent, so frameworks added retry and validation layers. A significant portion of what LangGraph does was developed to patch limitations of the underlying models.

By 2026, the underlying models are dramatically better. Context windows are measured in millions of tokens, not thousands. Reasoning is reliable enough that a single well-prompted model call can handle tasks that required a multi-step graph eighteen months ago. Function calling is precise. Structured output is native. For a meaningful slice of use cases, the question "do I need a framework to orchestrate this?" now has the answer "probably not, if the model is good enough."

This argument has real weight. We should not dismiss it. A developer building an agent in 2026 has at least three options that simply did not exist in 2024: a plain LLM-in-a-loop (which works for more cases than it used to), a vendor SDK with aggressive hosted features (which can eliminate most of the integration plumbing), and an AI coding assistant that will generate custom agent scaffolding on demand in ten minutes. All three compress the space where an agnostic framework is the right answer.

The abstraction tax matters too. LangGraph adds layers between the developer and the model. When something fails, you have to dig through those layers to find the prompt that actually produced the bad output. Developers call this "production archaeology" and it is a real cost. For simple agents, that cost exceeds the portability benefit.

The honest version of the pro-agnostic case in 2026 is narrower than it was eighteen months ago. Agnostic frameworks still win decisively when you have: durability needs that the vendor SDKs do not offer, multi-model routing requirements driven by compliance or cost, deep regulated-industry audit needs, or a serious organisational mandate against vendor lock-in. Outside those conditions, the case for paying the abstraction tax is weaker than it used to be.

This is not a rejection of LangGraph or CrewAI. It is a calibration. The agnostic frameworks are not default choices. They are the right choices for a specific, still-meaningful set of workloads — and the set is smaller than their advocates sometimes claim.

## When the Agnostic Case is Strongest

Put positively, here are the conditions where paying the abstraction tax is obviously worth it.

**Regulated industries where swap-ability is a compliance concern.** Banking, insurance, healthcare, public sector. When a regulator asks "can you demonstrate that this system does not depend on a single vendor's continued good behaviour?", you want a framework that lets you answer yes.

**Multi-model routing.** When part of the use case requires a local, open-weight model for compliance reasons and another part benefits from a frontier API, a framework that was designed for this routing is vastly easier to work with than one that assumes a single model.

**Long-running, high-stakes, human-in-the-loop.** Agents that pause for days or weeks, need bulletproof resumability, and carry audit-grade state through complex approval flows. LangGraph's durable execution is hard to replicate from scratch.

**Board-level lock-in mandates.** In some enterprises, the "must be model-agnostic" requirement is not a technical preference — it is a C-suite mandate with legal and commercial weight. In that case, the conversation about whether the vendor SDK is "good enough technically" is moot.

**Large engineering organisations with the bandwidth to absorb the learning curve.** The abstraction tax is more tolerable when you have ten engineers who can all contribute to the agent platform than when you have two engineers trying to ship before the quarter ends.

## An Honest Reading of the Agnostic Category

The agnostic frameworks are the insurance policy of the agent stack. Insurance policies have costs (the abstraction tax, the learning curve, the production-archaeology burden). They pay off in specific scenarios (vendor failures, forced migrations, regulatory shifts). Whether they are worth it depends on how much risk you are carrying and how much you believe the scenarios will come to pass.

For a typical enterprise in 2026, the honest answer is: probably one of the vendor SDKs today, with a realistic option to migrate to an agnostic framework in 2027 if your scale, regulatory environment, or vendor relationship makes that migration necessary. For a *regulated* enterprise in 2026 — particularly in Europe, where the compliance concerns we cover in Chapter 10 are sharper — the answer tips more strongly toward the agnostic camp from the start.

> **What to take from this chapter:** LangGraph and CrewAI are the two agnostic frameworks that matter. LangGraph plays the Kubernetes role: powerful, structural, production-grade, verbose. CrewAI plays the Docker Compose role: fast, intuitive, perfect for prototyping, less suited to long-term scale. The strongest counter-argument to agnostic frameworks in 2026 is that models have gotten good enough that the abstraction they provide is less necessary than it used to be. That argument has real weight for most use cases, but breaks down decisively for regulated industries, multi-model routing, durability-critical workloads, and organisations with hard lock-in mandates.

---

*Next: [Chapter 8 — Observability, Evaluation, and Cost Governance](08_observability_cost_governance.md)*
