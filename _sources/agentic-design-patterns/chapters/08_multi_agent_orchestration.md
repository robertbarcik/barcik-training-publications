# Chapter 8: Multi-Agent Orchestration

> **Design Pattern: Swarm Orchestration with Shared Context**
> *Problem:* A single agent hits context window limits, cannot parallelize work, and produces worse results when forced to play planner, coder, and reviewer simultaneously.
> *Solution:* A lead orchestrator decomposes tasks and spawns specialized worker agents that share a common prompt cache, enabling parallel execution with logarithmic cost scaling.
> *Tradeoff:* Multi-agent systems introduce coordination overhead, new failure modes (cascading errors, circular delegation, cost explosions), and debugging complexity that single-agent systems avoid entirely.
> *When to use:* When tasks are naturally decomposable, when parallelism provides meaningful speedup, and when the coordination cost is justified by the complexity of the work.

<div class="key-points">
<div class="kp-title">Key Points</div>
<ul>
<li>Single agents hit a ceiling: <strong>context limits</strong>, <strong>sequential bottleneck</strong>, <strong>role confusion</strong></li>
<li>Lead agent (orchestrator) decomposes tasks and spawns <strong>specialized workers</strong></li>
<li>Shared prompt cache makes it affordable: <strong>90% discount</strong> on cached input tokens</li>
<li>Risk classification is <strong>non-delegable</strong> — HIGH-risk actions need human approval regardless of which agent proposes them</li>
<li><strong>MCP</strong> for agent-to-tool + <strong>A2A</strong> for agent-to-agent = cross-system orchestration</li>
</ul>
</div>

<div class="stat-row">
<div class="stat-card"><div class="stat-number">90%</div><div class="stat-label">Prompt cache discount on repeated context</div></div>
<div class="stat-card"><div class="stat-number">67%</div><div class="stat-label">Cost reduction with 5-agent swarm</div></div>
<div class="stat-card"><div class="stat-number">78%</div><div class="stat-label">Cost reduction with 10-agent swarm</div></div>
</div>

## Why Single-Agent Architectures Hit a Ceiling

A single AI agent operating on a complex task faces three hard constraints.

**Context window limits.** Even with million-token context windows, a single agent working on a large codebase cannot hold the entire project in memory. A monorepo with 500,000 lines of code, its test suite, its CI configuration, its documentation, and the conversation history from a multi-step task will exceed any current context window. The agent must choose what to include and what to drop --- and those choices have consequences. Dropping the test file means the agent writes code that passes a non-existent test. Dropping the type definitions means the agent invents interfaces that do not match reality.

**Sequential bottleneck.** A single agent processes one step at a time. When a task requires research (read 15 files to understand the current architecture), implementation (modify 8 files), and validation (run the test suite and fix failures), the agent must do these sequentially. The research phase alone might take minutes. If three of those research tasks are independent --- reading the database schema, reading the API routes, reading the test fixtures --- a single agent reads them one after another. Three parallel agents read them simultaneously.

**Role confusion.** When you ask a single agent to plan an approach, implement it, and then critically review its own work, you are asking for three cognitively distinct behaviors from one context. The planning mindset ("what is the best approach?") conflicts with the implementation mindset ("just get it working") which conflicts with the review mindset ("what is wrong with this?"). In practice, a single agent asked to review its own code finds far fewer issues than a separate agent reviewing the same code with fresh context. The sunk-cost bias is not just a human phenomenon --- language models that generated code in the same context are measurably less likely to identify problems with it.

These are not theoretical limits. They are the practical ceiling that every team building on single-agent architecture encounters once tasks exceed a certain complexity threshold. The question is what to do about it.

## The Swarm Topology

The Claude Code source revealed a multi-agent architecture built around what is best described as a swarm topology. The structure has four components:

```
                    ┌──────────┐
                    │   User   │
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  Lead /  │
                    │ Orchest- │
                    │  rator   │
                    └──┬─┬─┬───┘
                 ┌─────┘ │ └─────┐
                 │       │       │
           ┌─────▼──┐ ┌─▼────┐ ┌▼───────┐
           │Worker A│ │Worker│ │Worker C│
           │Research│ │ B    │ │Review  │
           │        │ │Code  │ │        │
           └────┬───┘ └──┬───┘ └───┬────┘
                │        │         │
           ┌────▼────────▼─────────▼────┐
           │    Shared Prompt Cache      │
           │  (project context, rules,  │
           │   conversation history)     │
           └────────────────────────────┘
```

<div class="visual-diagram">
<div class="diagram-title">Swarm Topology</div>
<div class="swarm-diagram">
<div class="swarm-row"><div class="swarm-node user">User / Human</div></div>
<div class="diagram-arrow">&#8595;</div>
<div class="swarm-row"><div class="swarm-node orchestrator">Lead Agent / Orchestrator</div></div>
<div class="diagram-arrow">&#8595;</div>
<div class="swarm-row">
<div class="swarm-node worker">Worker A<br>Research</div>
<div class="swarm-node worker">Worker B<br>Code</div>
<div class="swarm-node worker">Worker C<br>Review</div>
</div>
<div class="diagram-arrow">&#8595;</div>
<div class="swarm-row"><div class="swarm-node cache">Shared Prompt Cache<br><small>project context, rules, conversation history</small></div></div>
</div>
</div>

The **lead agent** (orchestrator) receives the user's request and decides how to decompose it. It does not do the work itself --- it plans the work and assigns it. Think of it as a senior engineer who reads the ticket, breaks it into subtasks, and assigns each subtask to the right person.

**Worker subagents** are spawned dynamically. Each worker gets an isolated execution context --- its own conversation thread, its own tool access, its own scratchpad. Critically, each worker gets restricted tool access tailored to its role. A research worker might get read-only file access and web search but no ability to write files. A coding worker gets file write access but no ability to push to remote repositories. A review worker gets read access and the ability to post comments but no ability to modify code.

The **shared prompt cache** sits beneath all agents. This is the architectural innovation that makes multi-agent economically viable, and it deserves its own section.

## The Shared Prompt Cache: Making Multi-Agent Affordable

The naive approach to multi-agent orchestration is to give each agent a complete copy of all relevant context. If the project context is 50,000 tokens and you spawn five agents, that is 250,000 tokens of input just for context --- before any of the agents do anything. At $5 per million input tokens for a frontier model, that is $1.25 in context loading alone. Do this dozens of times per session, and costs spiral fast.

The shared prompt cache solves this by caching the foundational context once and letting all agents reference it. The mechanism relies on a property of modern LLM API pricing: cached input tokens are dramatically cheaper than fresh input tokens. Anthropic's prompt caching, for example, charges a one-time write fee of 25% above the base input price, then subsequent reads from cache cost only 10% of the base input price --- a 90% discount on every cache hit.

Here is the math for a five-agent swarm with 50,000 tokens of shared context:

**Without cache:** 5 agents x 50,000 tokens = 250,000 input tokens at full price.

**With cache:** 50,000 tokens cached once (1.25x write cost = 62,500 token-equivalents), then 4 additional reads at 0.1x each (4 x 5,000 token-equivalents = 20,000). Total cost-equivalent: 82,500 tokens. That is a 67% reduction for five agents.

The savings increase with scale. Ten agents: without cache, 500,000 tokens. With cache, 50,000 x 1.25 + 9 x 50,000 x 0.1 = 62,500 + 45,000 = 107,500 token-equivalents --- a 78% reduction. The cost of adding each marginal agent approaches 10% of what it would cost without caching. This is what makes cost scale logarithmically rather than linearly, and it is what makes multi-agent commercially viable for real workloads.

> **Design insight:** The shared prompt cache is not an optimization. It is an enabling architecture. Without it, multi-agent systems are economically impractical for all but the highest-value tasks. With it, you can spawn specialized agents for subtasks that would not individually justify the context loading cost.

The cache works because the foundational context --- project structure, coding conventions, type definitions, conversation history up to the point of task decomposition --- is identical across all workers. Each worker adds its own task-specific context on top of the shared base. The orchestrator is responsible for deciding what goes into the shared cache (high-reuse, stable context) versus what goes into each worker's private context (task-specific, ephemeral).

## Role Specialization Patterns

Not all agents need the same capabilities, the same model, or the same cost profile. Role specialization is where multi-agent architecture pays the largest dividends.

### The planner agent

The planner receives the user's request and the project context, then produces a structured task decomposition. Its output is not code --- it is a plan: which files need to change, in what order, what dependencies exist between subtasks, and what constitutes success for each subtask.

The planner benefits from the most capable (and most expensive) model available, because poor planning wastes every downstream agent's work. A planner that misidentifies the files to modify or misjudges dependencies will produce a plan where workers step on each other or build on false assumptions. Spending $0.10 on a frontier-model planning step to save $2.00 in wasted coding agent work is straightforward economics.

### The coder agent

The coder receives a specific, scoped task: "Modify `src/auth/middleware.ts` to add rate limiting. The rate limiter should use a sliding window algorithm. Here are the relevant type definitions and the existing middleware pattern." The coder's context is narrow and deep --- it does not need to understand the entire project, just its assigned slice.

Coder agents are the most expensive per-invocation because they run on capable models and produce substantial output tokens. But because their context is narrow (only the files relevant to their task, not the entire project), the per-agent cost is lower than a single agent trying to hold everything in context simultaneously.

### The reviewer agent

The reviewer receives the coder's output and the original requirements, then evaluates the code for correctness, style, security issues, and adherence to the plan. Crucially, the reviewer operates in a fresh context --- it did not write the code, so it does not share the coder's blind spots.

Reviewer agents can often run on slightly cheaper models. Code review is primarily pattern matching and constraint checking, which mid-tier models handle well. The reviewer does not need to generate novel code; it needs to identify problems in existing code.

### The research agent

The research agent handles information gathering: reading files, searching documentation, querying APIs for context. Its output is structured information that other agents consume. Research agents are ideal candidates for the cheapest models in your roster. They are performing retrieval and summarization, not generation --- tasks where the difference between a $1/million-token model and a $15/million-token model is minimal.

The cost differential across roles matters at scale. A swarm that uses a frontier model for planning ($15/million output tokens), a capable model for coding ($5/million), a mid-tier model for review ($2/million), and a cheap model for research ($0.50/million) will cost 40--60% less than a swarm that uses the frontier model for everything, with negligible quality loss.

## The Orchestrator's Job

The orchestrator is the most complex component in the system, and its responsibilities go beyond "assign work to agents."

### Task decomposition

Given a user request ("add authentication to the API"), the orchestrator must decompose it into parallelizable subtasks with explicit dependencies. This requires understanding the codebase well enough to know which changes are independent (modifying the auth middleware and updating the database schema can happen in parallel) and which are sequential (writing the tests must happen after writing the implementation).

Poor decomposition is the single largest source of failure in multi-agent systems. If the orchestrator decomposes too coarsely (one giant task per agent), you lose the parallelism benefit. If it decomposes too finely (one function per agent), the coordination overhead dominates. If it gets the dependencies wrong, agents produce conflicting changes that the orchestrator must reconcile.

### Agent selection

For each subtask, the orchestrator selects the appropriate role, model tier, and tool permissions. This is where the cost optimization happens. A subtask that requires reading five files and summarizing their structure goes to a research agent on a cheap model. A subtask that requires implementing a complex algorithm goes to a coding agent on a frontier model. The orchestrator makes these decisions based on the task characteristics, not on a fixed mapping.

### Result aggregation

When workers complete their subtasks, the orchestrator must aggregate the results into a coherent whole. This is non-trivial. Two coding agents working on related files may produce changes that are individually correct but mutually incompatible --- they might both modify a shared import, or they might make conflicting assumptions about an interface. The orchestrator must detect these conflicts and resolve them, either by sending the conflicting changes to a reviewer agent or by re-assigning one of the subtasks with additional constraints.

### Conflict resolution

When agents disagree --- the coder produced code that the reviewer rejects, or two coders made incompatible changes --- the orchestrator must resolve the conflict. The simplest strategy is to defer to the reviewer (reject the code and send it back for revision). More sophisticated strategies involve having the conflicting agents present their reasoning and having a third agent adjudicate. The right approach depends on the cost and time budget.

## Communication Patterns

Multi-agent systems use three primary communication architectures, each with distinct tradeoffs.

### Shared memory

All agents read from and write to a common data store. The shared prompt cache is one form of shared memory. A shared scratchpad where agents can post intermediate results is another. Shared memory is simple to implement and efficient for broadcasting information, but it creates coordination challenges: agents may read stale data, and concurrent writes require conflict resolution.

### Message passing

Agents communicate by sending structured messages to each other, typically through the orchestrator. The orchestrator routes messages based on task dependencies. Message passing provides clean isolation between agents and makes the communication flow explicit and auditable. The cost is latency --- every inter-agent communication round-trips through the orchestrator.

### Blackboard architecture

A hybrid approach where agents post partial results to a shared "blackboard," and other agents monitor the blackboard for information relevant to their tasks. The orchestrator manages the blackboard and notifies agents when relevant information appears. This is useful when the dependencies between subtasks are not fully known in advance --- agents can adapt their behavior based on what other agents have discovered.

The Claude Code swarm uses primarily message passing through the orchestrator, with the shared prompt cache serving as a limited form of shared memory for foundational context. This is a pragmatic choice: message passing is the easiest to debug and audit, and the shared cache handles the highest-volume data sharing (project context) without the complexity of a full shared memory system.

## Failure Modes You Must Design For

Multi-agent systems introduce failure modes that do not exist in single-agent architectures. Designing for these failures is not optional --- they will occur in production.

### Cascading errors

Agent A completes its task but produces subtly incorrect output. Agent B, which depends on Agent A's output, proceeds with the incorrect input and produces its own output --- which is now wrong in a way that compounds Agent A's error. Agent C depends on Agent B. By the time the error is detected, three agents have done work that must be discarded.

The defense is validation at every handoff point. When the orchestrator passes Agent A's output to Agent B, it should validate that output against the original requirements and known constraints. Catching errors at the handoff is dramatically cheaper than catching them after three more agents have built on the flawed foundation.

### Circular delegation

Agent A encounters a subproblem it cannot solve and requests help from the orchestrator. The orchestrator spawns Agent B to handle it. Agent B encounters a related subproblem and requests help. The orchestrator, following the same logic, spawns an agent to handle it --- which produces a task equivalent to Agent A's original task. Without cycle detection, this loops indefinitely.

The defense is tracking the task ancestry. Every spawned agent carries a lineage record: which task spawned it, which task spawned that task, back to the original user request. If a new task is semantically equivalent to an ancestor task, the orchestrator rejects it and forces the requesting agent to handle it directly or report failure.

### Agents disagreeing on approach

A coder agent implements a solution using approach X. A reviewer agent rejects it and suggests approach Y. The coder agent revises using approach Y. The reviewer now has concerns about approach Y that it did not raise initially. This back-and-forth can continue indefinitely.

The defense is bounded iteration. Set a maximum number of review cycles (typically two to three). If agreement is not reached within the bound, escalate to the orchestrator, which either makes a decision or escalates to the human. Unbounded revision loops are the multi-agent equivalent of an infinite loop in code.

### Cost explosions from unbounded spawning

The orchestrator decomposes a task into subtasks. One subtask turns out to be complex, so its assigned agent requests further decomposition. The sub-subtasks also request decomposition. Without limits, a single user request can spawn dozens of agents, each consuming context tokens, model inference time, and tool invocations.

The defense is a cost budget. Before decomposing a task, the orchestrator allocates a token budget and a wall-clock time budget. Each spawned agent receives a fraction of the remaining budget. When an agent's budget is exhausted, it must produce its best result with what it has, not request more resources. The orchestrator tracks cumulative spend across all agents and can abort the entire swarm if the total exceeds a hard limit.

> **Design insight:** Every multi-agent failure mode has the same root cause: insufficient constraints on inter-agent interaction. The orchestrator's primary job is not assigning work --- it is enforcing boundaries. Budget limits, iteration caps, cycle detection, and handoff validation are the four non-negotiable constraints.

## Risk Classification in Multi-Agent Context

The risk classification system from Chapter 4 --- LOW, MEDIUM, HIGH --- becomes more important, not less, in a multi-agent architecture. The reason is that workers operate with less human oversight than a single agent would.

When a user interacts directly with a single agent, every proposed action is visible in the conversation. The user can see "I am about to run `rm -rf build/`" and intervene if needed. In a swarm, the user interacts with the orchestrator. The workers operate in background threads, potentially executing dozens of actions without direct user visibility.

This means the risk classification must be enforced at the worker level, not just at the orchestrator level. Every action proposed by any agent in the swarm goes through the same risk classification pipeline. A worker agent cannot execute a HIGH-risk action just because its orchestrator told it to. The authorization requirement is non-delegable: HIGH-risk actions require human approval regardless of which agent proposes them and regardless of the internal chain of delegation that led to the proposal.

The practical implementation is a centralized authorization service that all agents call before executing any action classified above LOW. The service checks the action against the risk classification rules, checks whether a blanket authorization exists for this session (the user said "approve all file writes in the `src/` directory"), and if not, queues the action for human approval. The swarm pauses that particular branch of work until approval is granted, while other branches continue in parallel.

## Beyond the Swarm: Inter-Agent Protocols

Everything described so far in this chapter assumes you control all the agents. The orchestrator, the workers, the shared cache --- they all live in your system, running your code, under your authority. This is within-system orchestration. The industry is now building protocols for a harder problem: cross-system orchestration, where agents built by different teams, running on different infrastructure, need to discover and collaborate with each other.

Two complementary protocols have emerged, both now under Linux Foundation governance with backing from Google, Anthropic, OpenAI, Microsoft, and AWS.

**MCP (Model Context Protocol)** solves the vertical problem: connecting an agent to tools and data sources. We discussed MCP's tool annotations in Chapter 4. In the multi-agent context, MCP matters because each worker agent in a swarm can consume specialized tool servers without the orchestrator needing to understand or proxy those tools. The tool servers are isolated --- they cannot see the conversation or each other --- which enforces least privilege at the protocol level.

**A2A (Agent2Agent Protocol)** solves the horizontal problem: connecting agents to other agents. Where MCP tools are transparent (you see the schema, the parameters, the return type), A2A agents are deliberately opaque. You know what skills a remote agent advertises --- it publishes a JSON metadata file called an Agent Card at `/.well-known/agent-card.json` declaring its capabilities, authentication requirements, and supported interaction modes --- but you do not know how it works internally. This opacity is intentional. It enables cross-vendor, cross-framework collaboration where you cannot inspect or control the remote agent's implementation.

A2A models work as stateful tasks with a well-defined lifecycle: `submitted`, `working`, `completed`, `failed`, `canceled`, or `rejected`. Critically, the state machine includes `input_required` --- the remote agent can pause and ask the client for more information, enabling multi-turn negotiation between agents. For long-running tasks, the protocol supports polling, server-sent event streaming, and push notifications via webhooks.

One architectural insight worth borrowing from Google's Agent Development Kit (ADK), which natively integrates both MCP and A2A: the **workflow/LLM agent duality**. ADK distinguishes between deterministic workflow agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) that orchestrate without LLM involvement, and LLM-driven agents that use a model for reasoning and routing. Real systems combine both. Use deterministic pipelines where the control flow is known, and reserve LLM-driven routing for decisions that genuinely require judgment. This prevents the common mistake of routing every decision through an expensive, unpredictable LLM call when a simple if-statement would suffice.

The practical takeaway: the swarm patterns in this chapter handle within-system orchestration. When your agents need to collaborate with external systems --- consuming a partner's specialized agent, exposing your agent's capabilities to a client's orchestrator, or integrating tool servers you do not control --- MCP and A2A are the emerging standards for how that communication happens.

## When Multi-Agent Is Overkill

Multi-agent orchestration is powerful, but it is not always the right tool. The overhead of decomposition, spawning, coordination, and result aggregation is real. For tasks that take a single agent less than a few minutes, the coordination overhead of a multi-agent approach often exceeds the time saved through parallelism.

Rules of thumb:

- **Single-file changes:** Use a single agent. The overhead of spawning workers for a task that touches one file is pure waste.
- **Multi-file changes with clear boundaries:** Two agents (planner + executor) are often enough. The planner identifies all files to change and the order of changes. The executor works through the plan sequentially.
- **Cross-cutting changes across many files:** A swarm with parallel coding agents and a reviewer pays for itself. Changing an API contract that affects 15 files is a task where three parallel coders are meaningfully faster than one sequential coder.
- **Research-heavy tasks:** A research swarm (multiple research agents gathering information in parallel, feeding a single coder agent) is one of the highest-ROI multi-agent configurations. Research is embarrassingly parallel and benefits from cheap models.
- **Tasks requiring diverse expertise:** If a task spans multiple domains (database migration + API changes + frontend updates + infrastructure config), specialized agents for each domain produce better results than a generalist agent attempting all four.

The cost-benefit calculation should be explicit. Before spawning a swarm, estimate: how long would a single agent take? How much would the swarm cost in additional tokens? Is the time saved worth the additional spend? If the answer is not clearly yes, use a single agent.

## Applying This Pattern

When building multi-agent orchestration into your own system, follow this progression:

- **Start with two agents, not a full swarm.** A planner and an executor give you 80% of the benefit with 20% of the complexity. The planner decomposes the task and produces a structured plan. The executor follows the plan step by step. This teaches you the decomposition problem without the coordination problem.

- **Add a reviewer as your third agent.** The highest-leverage addition to a two-agent system is a reviewer that checks the executor's output before it reaches the user. Fresh-context review catches errors that the executor, operating in its own context, will miss.

- **Implement the shared prompt cache before adding parallelism.** The cache is what makes multi-agent economically viable. Get the caching architecture right with sequential agents before introducing the complexity of parallel execution.

- **Design your cost budget before your agent topology.** Decide how much a single user request can cost in total. Work backward from that budget to determine how many agents you can afford to spawn, at which model tiers, with how much context each. The topology follows from the economics, not the other way around.

- **Enforce non-delegable authorization.** HIGH-risk actions require human approval regardless of which agent proposes them. This is not negotiable. An orchestrator that can bypass human authorization for dangerous actions because it has "internal alignment" from its workers is a system that will eventually execute a destructive action without human consent.

- **Instrument everything.** Log every agent spawn, every task assignment, every result, every inter-agent message, every cost. You cannot debug a multi-agent system without full observability. When a swarm produces a wrong answer, you need to trace the error back through the chain of agents to find where the reasoning went wrong.

- **Set hard limits on recursion depth and total agent count.** A maximum spawning depth of three levels (orchestrator spawns workers, workers do not spawn sub-workers) is a reasonable starting point. A maximum total agent count per user request (10--20 for most applications) prevents cost explosions. These limits can be raised later with evidence; they should never start uncapped.

- **Know when to stop.** Multi-agent orchestration is seductive because it maps to how human teams work. But human teams have judgment, shared culture, and the ability to walk over to someone's desk and resolve ambiguity in ten seconds. Agent swarms have none of these. The coordination overhead is real, the failure modes are novel, and the debugging is hard. Use the simplest architecture that solves your problem. Add agents only when you have evidence that the current architecture is the bottleneck.

- **Evaluate A2A and MCP for cross-system collaboration.** If your agents need to collaborate with external systems or agents you do not control, the Agent2Agent protocol handles inter-agent discovery and task delegation, while MCP standardizes tool access. These protocols solve cross-system problems that internal swarm orchestration cannot --- and they are converging as industry standards under the Linux Foundation.

> **What to take from this chapter**: Multi-agent orchestration solves real problems --- context limits, sequential bottlenecks, role confusion --- but introduces its own failure modes that require deliberate design. The shared prompt cache is the enabling architecture that makes multi-agent economically viable, reducing marginal agent cost by up to 90%. Start with two agents (planner + executor), add a reviewer third, and enforce cost budgets and authorization gates from the beginning. The orchestrator's primary job is not assigning work --- it is enforcing constraints. Design for the failure modes (cascading errors, circular delegation, cost explosions) before they find you in production.

---

*Next: [Chapter 9 --- Frontier Capabilities and Containment](09_frontier_capabilities.md)*
