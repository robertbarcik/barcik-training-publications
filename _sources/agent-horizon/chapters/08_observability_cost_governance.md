# Chapter 8: Observability, Evaluation, and Cost Governance

---

## The Chapter the Framework Debates Skip

Walk into a room of engineers debating agent frameworks and you will hear about control flow, state management, and multi-agent patterns. Walk into a room where the same engineers are explaining their agent deployment to the CFO and you will hear about three things: *does it work, how do we know it works, and how much is it costing us?*

The first room is where the interesting technical arguments happen. The second room is where budget approvals happen. Enterprises that succeed with agents have figured out that the second room is where most of their engineering effort actually needs to land. This chapter is about the observability, evaluation, and cost-governance layer of the agent stack — the layer that sits across every framework, every model, and every protocol, and that becomes the difference between a deployed pilot and a shelved one.

In cloud terms, this is the Datadog layer. The Splunk layer. The AWS Cost Explorer layer. The layer that, in mature cloud deployments, represents a significant fraction of total infrastructure spend — and in mature agent deployments will do the same.

> **The most underweighted reality in agent-stack discourse:** The framework choice determines at most a third of your engineering cost. The observability, evaluation, and cost-governance layer you build around your agents determines the other two-thirds — and it is the layer that separates pilots that die from systems that ship.

## Why Observability Is Harder for Agents Than for Microservices

In a classical web service, observability is well-understood. You log requests, trace distributed calls, measure latencies, alert on errors, compute SLOs. The surface is stable. The error modes are known. The instrumentation tools (Datadog, New Relic, Grafana, Splunk) are mature.

Agents break most of these assumptions.

**The "correct" output is not well-defined.** A web service either returns 200 or it does not. An agent returns natural language, or a tool call, or a partial answer, or a hallucinated confidence-rich wrong answer, or any of a dozen subtle failure modes. There is no single status code for "the agent was confidently incorrect."

**The execution path is non-deterministic.** The same agent, given the same input, may call different tools, in different orders, with different arguments on different runs. Debugging by reproducing the failing case is harder than in a deterministic system.

**The feedback loop is slow.** A web-service bug produces an immediate alert. An agent-quality bug may not surface until a user flags an inaccurate answer a week later — and by then the offending model version, prompt, and conversation may all be different.

**Cost is attached to quality.** A verbose, hallucination-prone agent is not just wrong — it is also expensive, because it calls more tools, retries more often, and burns more tokens per interaction. Quality and cost are entangled in ways they are not in traditional web services.

The implication is that classical observability is necessary but not sufficient. You need traces and errors like you do for a microservice. You also need a layer of agent-specific concerns — trajectory recording, evaluation, token-cost attribution, human-review workflows — that has no equivalent in traditional observability tools.

## The Four Pillars of Agent Observability

The agent-specific tools that have emerged in 2025 and 2026 — LangSmith, Langfuse, Phoenix, Braintrust, and others — are all different attempts to solve the same problem. They generally organise themselves around four pillars.

### 1. Traces

Every agent interaction produces a trace: the sequence of model calls, tool invocations, sub-agent delegations, and state transitions that led to the final output. A good trace lets a developer replay exactly what happened, with every prompt, every response, and every intermediate decision visible. For debugging, this is non-negotiable. For audit, this is often mandatory under regulatory frameworks like the EU AI Act.

The value of a trace is mostly in the details that are invisible without it. *Which tool was called with which arguments? What did the tool return? What did the model do with the result? Why did it choose to retry rather than ask the user?* None of this is visible in a log line. All of it is visible in a good trace.

### 2. Evaluation

An agent without an evaluation harness is an agent you cannot improve. You can change the prompt, swap the model, tweak the graph, and hope things got better — or you can run your changes against a corpus of representative inputs with known expected outputs and measure the difference.

Evaluation is the least glamorous part of agent engineering and one of the highest-leverage. Teams that invest in good eval sets ship faster, iterate with more confidence, and catch regressions before their users do. Teams that do not invest in eval sets end up making changes based on vibes and re-learning the same lessons repeatedly.

The trickiest part of agent evaluation is that the "correct" output is often not a single string. It is a range of acceptable outputs, a property the output must have, or a downstream effect in a system that is hard to measure. This is where the emerging art of *LLM-as-judge* evaluation comes in: using one model to grade another's outputs against rubrics. Done well, this scales evaluation dramatically. Done badly, it measures nothing while looking rigorous.

### 3. Cost attribution

Agents produce costs at multiple layers: model inference (tokens in, tokens out, per model and per run), tool invocations (each MCP call may have its own cost, particularly if it hits a paid API), compute for orchestration (LangGraph durability storage, OpenAI hosted sandbox, etc.), and human review (when agents escalate to a person).

Attributing these costs by user, by workflow, by feature, and by team is what separates an agent deployment that stays under budget from one that quietly burns through the quarterly AI budget in six weeks. The tooling for this is still early — most enterprises are building internal dashboards rather than buying off-the-shelf — but it is one of the areas seeing the most rapid improvement.

A specific warning: the token cost of a single agent interaction can vary by an order of magnitude depending on how many tools it calls, how much context it pulls in, and how many retries it does. Cost observability needs to be per-interaction, not just per-month, or the long tail will bite you.

### 4. Quality signals

Beyond structured evaluation, production agents need lightweight, continuous quality signals. User thumbs-up/thumbs-down ratings. Drop-off rates. Follow-up message patterns ("that's wrong," "no, I meant...", "never mind"). Time to resolution. These are the agent equivalents of the error rate and latency percentiles that cloud-era observability tools centred on.

Capturing these signals and feeding them back into evaluation sets and prompt iteration is the machinery of continuous improvement. Without it, your agent's quality is whatever it was on launch day, decaying slowly as the real world diverges from your training assumptions.

## The Tool Landscape

A short orientation to the tools in this space, because this is where much of the actual enterprise spend will land.

| Tool | Positioning |
|---|---|
| LangSmith | LangChain/LangGraph ecosystem. Deep integration with LangGraph, strongest eval and trace story in the agnostic camp. |
| Langfuse | Open-source alternative, vendor-agnostic, strong self-host story for data-sensitive deployments. |
| Phoenix (Arize) | Evaluation-centric, broad model support, ties to ML observability tooling. |
| Braintrust | Evaluation-first with a focus on LLM-as-judge at scale. |
| W&B Weave | Weights & Biases extension into LLM observability. |
| Vendor native | Each vendor SDK ships its own basic observability (OpenAI traces, Anthropic's console, Google's ADK visual debugger). Serviceable for single-vendor deployments, weak for multi-vendor. |

The strategic point: the agent observability layer is quickly becoming its own software category, analogous to the APM category for cloud. And like APM, enterprises will spend real money on the tools that make the difference between operational and dysfunctional.

## Cost Governance Is Not Optional

One of the easiest-to-ignore failures in early agent deployments is runaway spend. A well-designed agent that calls three tools per interaction at $0.003 per call is cheap. The same agent under pressure — more retries, more context, more tool calls, more self-reflection — can easily 10x its cost without anyone noticing until the invoice arrives.

A small set of practices separate disciplined deployments from undisciplined ones.

**Per-interaction cost budgets.** The agent knows its own cost limit and stops or asks for confirmation when approaching it. Surprisingly few early deployments build this in.

**Per-user or per-tenant caps.** An abusive user (or a buggy integration) should not be able to burn through the monthly AI budget in a day. Rate limits on tokens, tool calls, and interactions are table-stakes infrastructure.

**Model routing for cost.** For many tasks, a cheaper model is adequate. Sending every interaction to the flagship model is a budgeting choice dressed up as a quality choice. Production agents route by task type — the expensive model for hard questions, the cheap model for routing and classification — and the savings compound quickly.

**Tool call budgeting.** If an agent calls five tools when it should have called two, that is both a quality issue and a cost issue. The evaluation harness should surface tool-call efficiency alongside output quality.

**Compaction and context hygiene.** Agents that repeatedly send huge prompts burn tokens disproportionately. Context compaction, prompt caching (where the vendor supports it), and disciplined prompt engineering can cut costs by a factor of three or more without touching model quality.

This is not exotic material. It is the same cost discipline that cloud engineers developed in the 2010s around reserved instances, autoscaling, and tag-based chargeback. The agent era will develop its own version of FinOps — call it AgentOps, call it AIOps, call it what you will — and enterprises that build this discipline early will spend materially less per unit of agent value delivered.

## Audit and Compliance: The Enterprise Forcing Function

For European enterprises especially — and we come back to this in Chapter 10 — observability is not just a developer convenience. It is a regulatory requirement. The EU AI Act requires, among other things, that deployers of high-risk AI systems maintain logs that allow traceability throughout the system's lifecycle, retain those logs for at least six months, and demonstrate human oversight of the system's decisions. You cannot satisfy those requirements without an observability layer.

The implication is that the observability-and-evaluation stack is, for regulated enterprises, a compliance infrastructure project before it is an engineering-quality project. The choices you make here — trace granularity, retention periods, access controls, audit workflows — have legal consequences, not just operational ones.

This is also the layer where the vendor-versus-agnostic choice starts to re-emerge with fresh urgency. A vendor SDK with closed observability ties you to that vendor's audit artefacts. An agnostic framework with open tracing lets you centralise audit across multiple models and workflows. For regulated deployments, this is often what pushes organisations toward the agnostic camp regardless of their developer preferences.

## What Mature Looks Like

A mature agent observability practice, twelve months in, typically has these properties:

- Every production interaction produces a trace, retained for at least the compliance-required period.
- An evaluation suite of several hundred to several thousand representative interactions runs on every change to prompts, tools, or model configuration.
- Cost is attributed to individual interactions, users, features, and teams, with dashboards visible to both engineering and finance.
- Quality signals (user feedback, resolution rates, follow-up patterns) feed back into the evaluation suite.
- Anomalies (cost spikes, quality drops, tool-failure rates) produce alerts.
- Human review workflows handle the long tail of edge cases and feed outcomes back into the eval set.

Very few enterprises are here in 2026. Most are somewhere between "we log model calls" and "we have a dashboard but nobody looks at it." The gap is the single biggest predictor of whether an agent program matures into something strategic.

> **What to take from this chapter:** The observability, evaluation, and cost-governance layer is where agent deployments either mature or die. Framework choice gets the attention; this layer gets the budget. The four pillars — traces, evaluation, cost attribution, quality signals — are all genuinely necessary. The tooling market (LangSmith, Langfuse, Phoenix, Braintrust, vendor-native) is maturing quickly. For regulated enterprises, this layer is compliance infrastructure, not just engineering infrastructure — which is part of why regulated enterprises often end up in the agnostic framework camp regardless of their developer preferences.

---

*Next: [Chapter 9 — The Lock-In Question](09_lock_in_question.md)*
