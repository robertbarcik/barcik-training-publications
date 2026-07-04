# Chapter 7: Observability, Evaluation, and Cost

---

Walk into a room of engineers debating agent frameworks and you'll hear about control flow, state management, and multi-agent patterns. Walk into the room where the same engineers explain their agent deployment to the CFO and you'll hear three questions: *does it work, how do we know, and how much is it costing us?*

The first room is where technical arguments happen. The second is where budget approvals happen. Enterprises that succeed with agents have figured out that the second room is where most of their engineering effort actually needs to land. This chapter is about the layer that sits across every framework, every model, and every protocol, and that becomes the difference between a deployed pilot and a shelved one.

In cloud terms, this is the Datadog layer. The Splunk layer. The layer that in mature cloud deployments represents a significant fraction of total infrastructure spend, and in mature agent deployments will do the same.

## Why Agent Observability Is Harder Than Microservice Observability

In a classical web service, observability is well-understood. Log requests, trace distributed calls, measure latencies, alert on errors, compute SLOs. The surface is stable. The error modes are known. Agents break most of these assumptions.

**The "correct" output isn't well-defined.** A web service either returns 200 or it doesn't. An agent returns natural language, a tool call, a partial answer, a confidently-wrong answer. No single status code for "the agent was wrong."

**Execution is non-deterministic.** Same agent, same input, different tools called, in different orders, with different arguments across runs. Debugging by reproducing the failing case is harder.

**The feedback loop is slow.** A bug in a service produces an immediate alert. A quality bug in an agent may not surface until a user flags an inaccurate answer a week later, and by then the offending model version, prompt, and conversation may all be different.

**Cost is attached to quality.** A verbose, hallucination-prone agent isn't just wrong; it's also expensive, because it calls more tools, retries more often, and burns more tokens per interaction. Quality and cost are entangled.

The implication: classical observability is necessary but not sufficient. You need traces and errors like you do for a microservice. You also need an agent-specific layer (trajectory recording, evaluation, token-cost attribution, human-review workflows) with no equivalent in traditional tools.

## The Four Pillars

The agent-specific tools that emerged in 2025-2026 (LangSmith, Langfuse, Phoenix, Braintrust) are different attempts at the same problem. They organise around four pillars.

**Traces.** Every agent interaction produces a trace: the sequence of model calls, tool invocations, sub-agent delegations, state transitions that led to the output. A good trace lets you replay exactly what happened, with every prompt, response, and intermediate decision visible. For debugging, non-negotiable. For audit, often mandatory under regulatory frameworks like the EU AI Act.

**Evaluation.** An agent without an eval harness is an agent you can't improve. You can change the prompt, swap the model, tweak the graph, and hope; or run changes against a corpus of representative inputs with known expected outputs and measure the difference. Evaluation is the least glamorous part of agent engineering and one of the highest-leverage. Teams that invest in good eval sets ship faster, iterate with more confidence, and catch regressions before users do.

The trickiest part of agent eval is that the "correct" output is often a range, not a string. That's where *LLM-as-judge* evaluation comes in: using one model to grade another's outputs against rubrics. Done well, scales evaluation dramatically. Done badly, measures nothing while looking rigorous. For a booklet-length look at how LLM judges hold up under adversarial pressure, see our research report [Warden](/warden/).

**Cost attribution.** Agents produce costs at multiple layers: model inference, tool invocations (paid APIs), orchestration compute (LangGraph durability storage, OpenAI hosted sandbox), human review. Attributing these costs by user, workflow, feature, and team is what separates a deployment that stays under budget from one that burns through the quarterly AI budget in six weeks. Tooling is still early (most enterprises are building internal dashboards rather than buying off-the-shelf), but it's improving fast.

A specific warning: the token cost of a single agent interaction can vary by an order of magnitude depending on tool calls, context pulled in, and retries. Cost observability needs to be per-interaction, not just per-month, or the long tail will bite you.

**Quality signals.** Beyond structured evaluation, production agents need lightweight continuous signals. User thumbs-up/thumbs-down, drop-off rates, follow-up message patterns ("that's wrong," "no, I meant..."), time to resolution. The agent equivalents of error rate and latency percentiles. Capturing them and feeding them back into eval sets and prompt iteration is the machinery of continuous improvement.

## The Tool Landscape

| Tool | Positioning |
|---|---|
| LangSmith | LangChain/LangGraph ecosystem. Deepest integration with LangGraph, strongest eval + trace story in the agnostic camp. |
| Langfuse | Open-source alternative, vendor-agnostic, strong self-host story for data-sensitive deployments. |
| Phoenix (Arize) | Evaluation-centric, broad model support, ties to ML observability tooling. |
| Braintrust | Evaluation-first with focus on LLM-as-judge at scale. |
| W&B Weave | Weights & Biases extension into LLM observability. |
| Vendor native | Each vendor SDK ships its own basic observability. Serviceable for single-vendor, weak for multi-vendor. |

The strategic point: the agent observability layer is quickly becoming its own software category, analogous to APM for cloud. Enterprises will spend real money on the tools that make the difference between operational and dysfunctional.

## Cost Governance Is Not Optional

One of the easiest-to-ignore failures in early agent deployments is runaway spend. A well-designed agent calling three tools per interaction at €0.003 each is cheap. The same agent under pressure (more retries, more context, more tool calls, more self-reflection) can easily 10x its cost without anyone noticing until the invoice arrives.

A small set of practices separates disciplined deployments from undisciplined ones. **Per-interaction cost budgets** (the agent knows its own cost limit and stops when approaching it). **Per-user or per-tenant caps** (an abusive user or buggy integration shouldn't burn the monthly AI budget in a day). **Model routing for cost** (the expensive model for hard questions, the cheap model for routing and classification; savings compound quickly). **Tool-call budgeting** (if an agent calls five tools when two would do, that's both a quality and a cost issue). **Compaction and context hygiene** (context compaction, prompt caching, disciplined prompt engineering can cut costs by 3x+ without touching model quality).

This isn't exotic material. It's the same discipline cloud engineers developed around reserved instances, autoscaling, and tag-based chargeback. The agent era will develop its own version. The business side of that discipline (what tokens actually cost, who pays, and which pricing models survive contact with agents) is covered at booklet length in [The Token Economics](/token-economics/). Enterprises that build this discipline early will spend materially less per unit of agent value.

## The Regulatory Forcing Function

For European enterprises especially (and Chapter 9 returns to this), observability isn't just developer convenience. It's a regulatory requirement. The EU AI Act requires deployers of high-risk AI systems to maintain logs allowing traceability throughout the system's lifecycle, retain those logs for at least six months, and demonstrate human oversight. You cannot satisfy those requirements without an observability layer.

The implication: for regulated enterprises, the observability stack is **compliance infrastructure before it's quality infrastructure**. The choices (trace granularity, retention periods, access controls, audit workflows) have legal consequences, not just operational ones. Chapter 9 covers the architecture of a compliant EU deployment in detail.

**Very few enterprises in 2026 have a mature observability practice in place. Most are somewhere between "we log model calls" and "we have a dashboard but nobody looks at it." The gap between those two states and "this works" is the single biggest predictor of whether an agent program matures into something strategic.**

---

*Next: [Chapter 8: The Lock-In Question](08_lock_in_question.md)*
