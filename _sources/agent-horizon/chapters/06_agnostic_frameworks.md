# Chapter 6: The Agnostic Frameworks

---

There's a smaller, noisier corner of the framework landscape where the defining feature is *not* being aligned with a model vendor. These are the agnostic frameworks. They assume you'll want to swap models, clouds, and tool surfaces, and they optimise for that flexibility even at the cost of developer velocity.

Two dominate: **LangGraph** and **CrewAI**. Both predate most of the vendor SDKs, both have larger communities than any single vendor framework, and both are currently positioning themselves as the neutral middle layer (the Switzerland) that large enterprises will eventually want between themselves and the foundation-model vendors.

The cloud analogy holds tightly here. If the vendor frameworks are PaaS, **LangGraph is Kubernetes** and **CrewAI is Docker Compose**.

## LangGraph as Kubernetes

Agent workflows as state machines. Nodes (steps). Edges (transitions). State flows through the graph. The framework is explicit about persistence: at every step the state is checkpointed, so if the server crashes or the agent pauses for human approval, the workflow resumes from exactly where it left off. Its insistence on structural explicitness is what gives it power, and what generates most of the complaints.

Strengths.

**Durable execution.** LangGraph's defining capability. Long-running agents can pause for hours or days, wait for human input, survive server restarts, and resume without losing state. For regulatory approvals, multi-step workflows with human-in-the-loop steps, agents that run overnight; often the only tractable solution.

**Observability and audit.** LangGraph pairs naturally with LangSmith, which provides deep traces, evaluation harnesses, and audit-grade records of every model call, tool invocation, and state transition. For regulated enterprises, this paper trail can be the difference between a deployable agent and a blocked one.

**Model agnosticism.** LangGraph doesn't care whether the underlying model is Claude, GPT, Gemini, Mistral, or a local Llama. The framework's primitives are model-neutral. You can swap the model layer without rewriting the workflow, which is the entire point.

**Production scale.** The most mature production story of any agent framework. More than 400 production deployments publicly documented, including high-scale cases (Klarna's customer support agent at 85 million users, 80% reduction in resolution time). The boring reliability features (connection pooling, retry semantics, backoff, rate limiting) that matter more in production than in demos.

One honest asterisk on that flagship number. Klarna is also the industry's cautionary tale: its earlier, OpenAI-built support assistant fronted an AI-first strategy that cut roughly 700 support roles, degraded service quality, and had the company publicly rehiring humans into a hybrid model by mid-2025. The LangGraph deployment is a different, later system, and the scale figure is real. But when the same logo appears in a vendor case study and a corporate walk-back, read the case study as marketing, not evidence.

The cost is a real learning curve. Developers coming from "just write the agent code" find LangGraph's graph formalism verbose for simple cases. Critics call it "a very fancy if-else statement," and for a three-step linear agent, they have a point. LangGraph's value shows up at scale, in production, under edge conditions, not in demos.

**Take LangGraph seriously if** you're in regulated industries, running long or human-in-the-loop agents, doing multi-model routing, facing board-level anti-lock-in mandates, or large enough to absorb the learning curve.

## CrewAI as Docker Compose

Work organised the way a human team does. Create agents, give each a role ("Senior Data Analyst"), a goal ("find trends in Q2 sales data"), and a backstory. Assemble into a "crew" and give the crew a task. CrewAI orchestrates the team. Business stakeholders can read a CrewAI agent definition and understand what's happening, and that friendliness is both the greatest strength and the greatest weakness.

Strengths.

**Prototyping speed.** Nothing in either framework category can get a multi-agent prototype running as fast. For workshops, proofs-of-concept, demos, often the fastest path.

**Role-based reasoning.** For tasks where the natural breakdown is "a team of specialists" (research pipelines, content creation, analysis workflows), the role-based abstraction is elegant. Fits the shape.

**Protocol support.** Native MCP and A2A support, earlier than most frameworks. Multi-agent-first design.

**Community momentum.** 44,000+ GitHub stars, active Discord, a growing commercial ecosystem. Wealth of examples you can borrow.

The cost: abstractions optimised for prototyping, not production. Thinner state management, limited checkpointing. For a long-running mission-critical agent, CrewAI forces you to solve enterprise concerns outside the framework, at which point its main value (quick prototyping) has been outgrown.

**Take CrewAI seriously if** you're running rapid POCs, workshops, or multi-agent workflows where role-based decomposition fits naturally and time-to-demo matters more than time-to-five-nines.

## "But Models Got Too Good": the Counter-Argument

Before anyone adopts an agnostic framework, they should understand the strongest argument against doing so.

Agnostic frameworks exist in part because early LLMs were weak. Context windows were small, so frameworks added summarisation and memory management. Reasoning was unreliable, so frameworks added structured control flow. Function calling was crude, so frameworks added tool-validation scaffolding. Hallucinations were frequent, so frameworks added retry and validation layers. A significant portion of what LangGraph does was developed to patch model limitations.

By 2026, underlying models are dramatically better. Context windows in millions of tokens, not thousands. Reasoning reliable enough that a single well-prompted model call handles tasks that required a multi-step graph eighteen months ago. Function calling precise. Structured output native. For a meaningful slice of use cases, "do I need a framework to orchestrate this?" now answers "probably not, if the model is good enough."

This argument has real weight. A developer building an agent in 2026 has at least three options that didn't exist in 2024: a plain LLM-in-a-loop (works for more cases than it used to), a vendor SDK with aggressive hosted features (eliminates most integration plumbing), and an AI coding assistant that generates custom agent scaffolding in ten minutes. All three compress the space where an agnostic framework is the right answer.

The abstraction tax is real too. LangGraph adds layers between developer and model. When something fails, you have to dig through those layers to find the prompt that actually produced the bad output, "production archaeology." For simple agents, that cost exceeds the portability benefit.

The honest version of the pro-agnostic case in 2026 is **narrower than it was eighteen months ago**. Agnostic frameworks still win decisively when you have: durability needs vendor SDKs don't offer, multi-model routing driven by compliance or cost, deep regulated-industry audit needs, or a serious organisational mandate against vendor lock-in. Outside those, the case for paying the abstraction tax is weaker than it used to be.

## When the Agnostic Case Is Strongest

**Regulated industries** where swap-ability is a compliance concern. When a regulator asks "can you demonstrate that this system doesn't depend on a single vendor's continued good behaviour?", you want a framework that lets you answer yes.

**Multi-model routing.** When one workflow requires a local, open-weight model for compliance reasons and another benefits from a frontier API, a framework designed for routing is vastly easier than one assuming a single model.

**Long-running, high-stakes, human-in-the-loop.** Agents that pause for days or weeks, need bulletproof resumability, and carry audit-grade state through complex approval flows. LangGraph's durable execution is hard to replicate from scratch.

**Board-level lock-in mandates.** In some enterprises the "must be model-agnostic" requirement is a C-suite directive with legal and commercial weight. The conversation about whether the vendor SDK is "good enough technically" is moot.

**Large engineering organisations** with bandwidth to absorb the learning curve. Easier to tolerate the abstraction tax with ten engineers contributing to the platform than two trying to ship before quarter-end.

For a typical enterprise in 2026, the honest answer is: probably a vendor SDK today, with a realistic option to migrate to an agnostic framework in 2027 if scale, regulatory environment, or vendor relationship demands. For a *regulated* enterprise (particularly in Europe, where Chapter 9's compliance concerns bite), the answer tips more strongly toward the agnostic camp from the start.

**Insurance policies have costs. They pay off in specific scenarios. Whether they're worth it depends on how much risk you're carrying and how much you believe the scenarios will come to pass.** That's the agnostic case, honestly stated.

---

*Next: [Chapter 7: Observability, Evaluation, and Cost](07_observability_cost_governance.md)*
