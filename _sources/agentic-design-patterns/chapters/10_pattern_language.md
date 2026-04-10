# Chapter 10: Building Your Own Agent

> **Design Pattern: Pattern Composition**
> *Problem:* Individual design patterns solve individual problems, but a real agent requires multiple patterns working together --- and some patterns conflict with others.
> *Solution:* Select patterns based on your deployment context, compose them into a coherent architecture using reference designs at the appropriate scale, and add complexity only when requirements demand it.
> *Tradeoff:* A minimal architecture ships faster and is easier to reason about, but may lack resilience; a comprehensive architecture handles more edge cases but costs more to build, operate, and debug.
> *When to use:* When you are moving from "I understand the patterns" to "I am building the system."

<div class="key-points">
<div class="kp-title">Key Points</div>
<ul>
<li>9 patterns compose into 3 reference architectures: solo, supervised, swarm</li>
<li>Solo agent for personal tools / supervised for enterprise / swarm for complex systems</li>
<li>Start simple — add complexity only from observed failures, not anticipated ones</li>
<li>Patterns are foundational; protocols (MCP, A2A) implement them</li>
<li>Answer 4 design questions before writing a line of code</li>
</ul>
</div>

## The Catalog

Over the previous nine chapters, we extracted nine design patterns from the Claude Code architecture and the broader agentic AI landscape. Before we compose them, let us have them in one place.

| # | Pattern | Core Idea | Chapter |
|---|---------|-----------|---------|
| 1 | Production Architecture Mindset | The model is one component; 90% of the work is orchestration, safety, and plumbing | Ch 1 |
| 2 | Skeptical Memory / Persistent Context | Maintain context across sessions, but treat recalled context as potentially stale and verify before acting | Ch 2 |
| 3 | Background Consolidation (AutoDream) | Compress and reorganize context during idle time to keep the working set relevant and within budget | Ch 3 |
| 4 | Risk-Classified Tool Constraints | Categorize every tool action by risk level and enforce graduated approval requirements | Ch 4 |
| 5 | Layered Prompt Architecture | Structure system prompts in priority tiers so critical instructions survive context pressure | Ch 5 |
| 6 | Output Calibration / Assertiveness Control | Tune the agent's confidence expression to match the stakes of the decision it is making | Ch 6 |
| 7 | Defense-in-Depth Security | Layer permission checks, sandboxing, monitoring, and deterministic overrides so no single failure compromises safety | Ch 7 |
| 8 | Multi-Agent Swarm Orchestration | Decompose complex tasks across specialized agents with shared context and coordinated execution | Ch 8 |
| 9 | Capability Gating / Containment | Systematically discover what your agent can do, then build containment around the gap between intended and actual capability | Ch 9 |

These patterns are not a checklist. Your agent does not need all nine, and some add complexity that is not justified for simpler deployments. The art is in selection and composition.

## How Patterns Compose

Patterns interact. Some reinforce each other. Some create tensions that you must resolve through design decisions.

**Reinforcing combinations.** Skeptical Memory (Pattern 2) and Background Consolidation (Pattern 3) are natural partners --- consolidation produces the compressed context that skeptical recall then verifies before use. Risk-Classified Tools (Pattern 4) and Defense-in-Depth Security (Pattern 7) are complementary layers of the same safety strategy. Layered Prompt Architecture (Pattern 5) makes Output Calibration (Pattern 6) more effective, because prompt priority tiers ensure calibration instructions survive context compression.

**Tension pairs.** Multi-Agent Swarm Orchestration (Pattern 8) creates tension with Defense-in-Depth Security (Pattern 7), because distributing work across agents multiplies the attack surface and complicates permission management. Background Consolidation (Pattern 3) creates tension with Capability Gating (Pattern 9), because background processes running unsupervised are exactly the kind of capability that gating should constrain. Output Calibration (Pattern 6) can conflict with the Production Architecture Mindset (Pattern 1) when calibration adds latency or token cost that violates your operational constraints.

These tensions are not bugs. They are design decisions. The right resolution depends on your deployment context --- which brings us to the three reference architectures.

## Three Reference Architectures

The following architectures represent three points on the complexity spectrum. They are not prescriptions. They are starting points that you adapt to your specific requirements.

### Architecture 1: Solo Agent

The solo agent is a single model instance with constrained tools, persistent memory, and basic prompt layering. It is the simplest architecture that qualifies as an "agent" rather than a chatbot.

**What it includes:**
- One model, one conversation thread, one user
- Skeptical Memory (Pattern 2) for cross-session continuity --- a local file or database that stores project context, with verification prompts before acting on recalled information
- Layered Prompt Architecture (Pattern 5) with two tiers: a core system prompt containing identity and safety rules, and a project-specific prompt injected from a configuration file
- Risk-Classified Tools (Pattern 4) at the simplest level: read-only tools execute freely, write tools require confirmation, destructive tools are blocked or require explicit opt-in
- Basic Output Calibration (Pattern 6) through prompt instructions that tell the model to express uncertainty when appropriate

**What it skips:**
- No background consolidation (the user manages context freshness manually)
- No multi-agent orchestration (one model does everything)
- No formal capability gating (the tool constraint layer provides basic containment)
- No defense-in-depth beyond the tool classification (acceptable when the user is also the operator)

**Cost profile:** Low. A single model instance, minimal infrastructure, token costs proportional to one user's usage. You can run a solo agent on a mid-tier model (Sonnet-class or equivalent) for most tasks, with selective routing to a frontier model for complex reasoning.

**Trust model:** The user trusts themselves. The agent operates within the user's own permission boundary. If the agent does something destructive, the blast radius is limited to the user's own environment.

**Good for:** Personal coding assistants, research tools, content drafting aids, individual productivity automation. Any use case where one person is both the user and the operator, and the consequences of agent errors are contained to that person's environment.

**Build time:** A competent developer can have a functional solo agent running in a week. Making it reliable takes a month.

### Architecture 2: Supervised Agent

The supervised agent adds human-in-the-loop oversight, comprehensive safety layers, calibrated output, and audit logging. It is the architecture for professional and enterprise contexts where the agent's actions affect others or operate in regulated environments.

**What it includes:**
- Everything in the solo agent, plus:
- Full Risk-Classified Tool Constraints (Pattern 4) with four tiers: safe (auto-execute), moderate (log and proceed), sensitive (require human approval), and critical (require approval with explanation)
- Defense-in-Depth Security (Pattern 7) with layered containment: prompt-level safety instructions, tool-level permission checks, orchestration-level policy enforcement, and infrastructure-level sandboxing
- Output Calibration (Pattern 6) with confidence thresholds --- the agent must express confidence levels, and actions below a configurable threshold are routed to human review
- Background Consolidation (Pattern 3) running on a schedule to keep context current, with consolidation outputs reviewed before injection into active sessions
- Capability Gating (Pattern 9) implemented as a pre-deployment audit checklist and periodic re-evaluation when the model is updated
- Comprehensive audit logging --- every tool invocation, every model response, every permission decision, every human approval or rejection, timestamped and retained

**What it skips:**
- No multi-agent orchestration (a single agent with human oversight is simpler to secure and audit than a swarm)
- Background consolidation runs but does not take autonomous action --- it prepares context for the next interactive session

**Cost profile:** Moderate. The model costs are similar to the solo agent, but you add infrastructure for logging, monitoring, the approval workflow, and the sandbox environment. Budget for a dedicated monitoring dashboard and alerting.

**Trust model:** Trust is distributed. The organization trusts the system (not just the model) because human oversight is embedded in the workflow. The audit log provides accountability. The permission tiers ensure that high-stakes actions always involve a human decision.

**Good for:** Enterprise code review and generation, customer-facing automation where errors have reputational or financial consequences, compliance-sensitive environments (finance, healthcare, legal), any context where "the agent did it" is not an acceptable explanation for a bad outcome.

**Build time:** Two to four months for a robust implementation. The tool permission system and approval workflow are the most time-consuming components. The audit logging is straightforward to build but requires thoughtful schema design to be useful for post-incident analysis.

### Architecture 3: Agent Swarm

The agent swarm distributes work across multiple specialized agents with shared context, coordinated execution, and centralized oversight. It is the architecture for complex autonomous systems where no single agent can hold the full problem in context.

**What it includes:**
- Everything in the supervised agent, plus:
- Multi-Agent Swarm Orchestration (Pattern 8) with a coordinator agent that decomposes tasks, assigns them to specialist agents, and synthesizes results
- Shared prompt cache and context store accessible to all agents in the swarm, with the Layered Prompt Architecture (Pattern 5) ensuring consistency of safety instructions across agents
- Background Consolidation (Pattern 3) running continuously, not just on a schedule --- dedicated consolidation agents that maintain the shared context store
- Full Capability Gating (Pattern 9) with continuous red-teaming: a dedicated adversarial agent that periodically probes the swarm for capability drift, escalation paths, and tool misuse patterns
- Defense-in-Depth Security (Pattern 7) extended to inter-agent communication: agents authenticate to each other, message integrity is verified, and no agent can escalate another agent's permissions
- Resource management: token budgets allocated per agent, per task, and per session, with the coordinator enforcing global budget constraints

**What it skips:**
- Nothing from the pattern catalog. A swarm architecture at production scale requires all nine patterns working together.

**Cost profile:** High. Multiple model instances running concurrently, shared infrastructure for context and coordination, monitoring and alerting across all agents, red-teaming overhead. Token costs scale with the number of agents and the complexity of coordination. Expect 3--5x the token cost of a supervised agent for the same task, with the payoff being the ability to handle tasks that a single agent cannot.

**Trust model:** Trust is systemic. No single agent is trusted unconditionally. The coordinator verifies specialist outputs. The adversarial agent probes for failures. Human oversight applies to swarm-level decisions (task decomposition, final outputs) rather than individual agent actions. The audit trail spans the entire swarm.

**Good for:** Large-scale codebase management (thousands of files, multiple repositories), continuous security auditing, complex multi-step autonomous workflows (deployment pipelines, incident response), research tasks that require synthesizing information across many sources simultaneously.

**Build time:** Six months to a year for a production deployment. The coordination protocol is the hardest part --- defining how agents communicate, how conflicts are resolved, and how the coordinator maintains coherence across parallel workstreams. Most teams underestimate this by at least 2x.

<div class="visual-diagram">
<div class="diagram-title">Three Reference Architectures</div>
<div class="diagram-flow">
<div class="diagram-box layer-1">Solo Agent<small>1 user, 1 model, basic tools</small></div>
<div class="diagram-arrow">&#8594;</div>
<div class="diagram-box layer-2">Supervised Agent<small>Human-in-the-loop, audit logs, defense in depth</small></div>
<div class="diagram-arrow">&#8594;</div>
<div class="diagram-box layer-3">Agent Swarm<small>Multi-agent, shared context, continuous red-teaming</small></div>
</div>
</div>

<div class="stat-row">
<div class="stat-card"><div class="stat-number">$0.50–5</div><div class="stat-label">Solo: per session / 1 month build</div></div>
<div class="stat-card"><div class="stat-number">$2–20</div><div class="stat-label">Supervised: per session / 2–4 months</div></div>
<div class="stat-card"><div class="stat-number">$10–100+</div><div class="stat-label">Swarm: per session / 6–12 months</div></div>
</div>

## Architecture Comparison

| Dimension | Solo Agent | Supervised Agent | Agent Swarm |
|-----------|-----------|-----------------|-------------|
| **Patterns used** | 2, 4 (basic), 5, 6 (basic) | 2, 3, 4, 5, 6, 7, 9 | All nine |
| **Model tier** | Mid-tier sufficient | Mid-tier + frontier for complex tasks | Frontier for coordinator, mid-tier for specialists |
| **Token cost per session** | $0.50--5 | $2--20 | $10--100+ |
| **Human oversight** | None (user = operator) | Embedded in workflow | At swarm decision points |
| **Deployment complexity** | Single process | Service + database + monitoring | Distributed system |
| **Build time** | 1 week -- 1 month | 2--4 months | 6--12 months |
| **Trust required** | Self-trust | Organizational trust | Systemic trust |
| **Best for** | Personal tools | Professional/enterprise | Complex autonomous systems |

## The Maturity Curve

The most common mistake in agent architecture is over-engineering early. Teams read about swarm orchestration and capability gating and defense-in-depth and conclude that they need all of it from day one. Six months of infrastructure work. No shipped agent.

Start at the simplest architecture that could work for your use case. Add patterns as requirements demand.

**Week 1--4: Build a solo agent.** Get a model calling tools, reading files, executing commands. Implement basic tool classification (read/write/destructive) and a simple memory file. Ship it to yourself. Use it daily. Learn where it breaks.

**Month 2--3: Harden based on real failures.** The failures you observe in daily use will tell you which patterns to add next. If the agent acts on stale context, invest in skeptical memory. If it takes destructive actions without warning, build out the tool permission system. If your token costs are too high, implement prompt tiering and context consolidation. Let the problems pull the solutions.

**Month 3--6: Add oversight if the use case demands it.** If your agent is serving users other than yourself, add the supervised architecture components: approval workflows, audit logging, output calibration with confidence thresholds. If it is still just you, these are overhead.

**Month 6+: Consider a swarm only if a single agent cannot hold the problem.** The only good reason to build a swarm is that your task requires more context, more specialization, or more parallelism than a single agent can provide. If a solo or supervised agent can do the job, it should. Swarms are powerful, but they are also the most expensive, most complex, and hardest-to-debug architecture in this booklet.

> **The maturity principle**: Add architectural complexity in response to observed problems, not anticipated ones. Every pattern you add before you need it is a pattern you must maintain, debug, and pay for without receiving value in return.

## The Clean-Room Question

One topic that runs through the entire booklet deserves explicit treatment here, because it affects how you can use what you have learned.

The architectural patterns in Claude Code are visible through its public behavior, its documentation, and the community analysis that has grown around it. But the specific source code is Anthropic's intellectual property. The question for practitioners is not "how do I replicate the code?" but "how do architectural patterns transfer between systems?"

The claurst project offers one answer. Claurst is a Rust reimplementation of Claude Code's functionality that used a two-phase abstraction process:

1. **Phase 1 (Specification):** One AI system analyzed Claude Code's observable behavior and produced 14 behavioral specifications --- documents describing what the system does, how its components interact, and what invariants it maintains. No code was included in the specifications, only architectural and behavioral descriptions.

2. **Phase 2 (Implementation):** A second AI system, working only from those behavioral specifications, wrote a complete implementation in Rust. The result is original code that solves the same problems through the same architectural patterns.

This two-phase process demonstrates something important: architectural patterns transfer without copying code. The specifications capture design intent --- the "what" and "why" --- while the implementation is entirely independent.

This matters because the patterns described in Chapters 1 through 9 are universal. They are engineering responses to engineering constraints that any agent builder faces. Skeptical memory, risk-classified tools, layered prompts, background consolidation --- different teams, working independently with different models and different languages, converge on these same solutions. You can implement them in any language, on any platform, with any model, because the constraints that produce them are shared.

## Open Questions

Some questions remain genuinely unresolved. They will shape agent architecture over the next two to five years, and the honest answer to most of them is "we do not know yet."

### How do you measure agent reliability in production?

Benchmarks measure task completion on standardized tests. Production reliability is different --- it includes consistency across varied inputs, graceful degradation under unexpected conditions, correct behavior over extended sessions, and the absence of rare but catastrophic failures. No widely accepted framework exists for measuring production agent reliability. Most teams rely on user feedback, error rates, and incident reports --- the same tools we use for conventional software, which may not capture the failure modes unique to probabilistic systems.

If you are building agents for enterprise contexts, you will need to develop your own reliability metrics. Start with: task completion rate, error recovery rate (how often the agent recovers from failures without human intervention), safety violation rate (how often the agent attempts actions that the permission system blocks), and context coherence over time (does the agent's behavior degrade in long sessions?).

### What is the right granularity for tool decomposition?

Should your "file management" capability be one tool with many parameters, or twenty specialized tools? Coarse-grained tools give the model flexibility but make permission management harder. Fine-grained tools enable precise permission control but increase the model's decision space and the probability of selecting the wrong tool.

Claude Code's approach --- moderately fine-grained tools with risk classification --- works well, but it was tuned for a specific model and a specific use case. Your optimal granularity depends on your model's tool-calling accuracy, your permission requirements, and your tolerance for incorrect tool selection. There is no universal answer.

### How should background agents negotiate with interactive agents?

When you have background consolidation agents and interactive agents sharing the same resources --- the same context store, the same token budget, the same model capacity --- how do they coordinate? If the background agent is compressing context while the interactive agent is trying to read it, you have a consistency problem. If both are consuming tokens from the same budget, you have a resource contention problem.

The current approaches --- priority queues, resource locks, dedicated capacity --- are borrowed from conventional distributed systems. They work, but they may not be optimal for the unique characteristics of AI workloads. This is an area where better solutions are likely to emerge as more teams build multi-agent systems.

### Can capability gating hold as models advance?

Chapter 9 described the capability overhang problem --- the gap between what a model can do and what you have tested for. The uncomfortable question is whether this gap is closable. If model capabilities advance faster than our ability to characterize them, then capability gating is a rearguard action --- useful for slowing down risk exposure, but not for eliminating it.

We do not know. The Mythos evaluation showed a 90x capability jump on a specific task. If jumps of that magnitude are common, containment strategies designed for the current capability level will be obsolete by the time they are deployed. This does not mean you should skip containment --- it means you should design containment that is easy to update, easy to re-evaluate, and not dependent on specific assumptions about what the model can do.

### How will standardized protocols reshape agent architecture?

The Model Context Protocol (agent-to-tool) and Agent2Agent Protocol (agent-to-agent) are converging as open standards under the Linux Foundation, backed by Anthropic, Google, OpenAI, Microsoft, and AWS. Google's Agent Development Kit already integrates both natively. As these protocols mature, the build-versus-integrate decision shifts fundamentally. The tool constraint patterns (Chapter 4), prompt layering (Chapter 5), and multi-agent orchestration (Chapter 8) in this booklet may increasingly be implemented via protocol-level standards rather than bespoke orchestration code. The question for practitioners is not whether to adopt these protocols, but when --- and how much of your custom orchestration they will eventually replace.

<div class="exercise">
<div class="exercise-title">Try It: Your Architecture in 15 Minutes (Capstone)</div>
<div class="exercise-body">
<p>This exercise ties the booklet together. Pick a real project — something you are working on or want to build. Open your coding agent and work through these four steps:</p>
<ol>
<li>Answer the four design questions from this chapter out loud (trust boundary, required patterns, token budget, worst-case action). Write the answers into a new file called ARCHITECTURE.md.</li>
<li>Based on your answers, choose Solo, Supervised, or Swarm as your starting architecture.</li>
<li>Ask your coding agent to generate a first-draft CLAUDE.md for this project, incorporating the patterns you selected — persistent context rules, tool constraints, risk classification levels, prompt structure.</li>
<li>Review what the agent produced. What did it get right? What did it miss? What would you change?</li>
</ol>
<p>You now have the skeleton of a real agent architecture. The next step is to build.</p>
</div>
</div>

## The Design Exercise

You have read nine patterns and three reference architectures. Now it is time to apply them. Before you write a line of code, answer these four questions for your specific use case. Write the answers down. They will become the first page of your architecture document.

**1. What is your agent's trust boundary?**

Who uses the agent? Who is affected by its actions? If the agent makes a mistake, who bears the consequences? If the answer is "only me," you can start with a solo architecture. If the answer includes other people, you need supervision. If the answer includes systems that serve many users, you need defense in depth.

**2. Which patterns from this booklet does your use case require?**

Start with the minimum. Some form of prompt architecture (Pattern 5) and some form of tool constraints (Pattern 4) are table stakes. Beyond those two, add patterns only when you can name the specific problem they solve in your context. "It seems like a good idea" is not sufficient. "Users will interact across sessions and the agent must maintain continuity" is.

**3. What is your token budget per session?**

This is not an abstract question. Run the arithmetic. If your model costs $5 per million input tokens and your typical session involves 100K tokens of context, that is $0.50 per session in input costs alone. Multiply by your expected usage volume. If the number is uncomfortable, you need to invest in context management (Patterns 2, 3, 5) to keep your working set small. If the number is trivial, you can afford to be less aggressive about context compression.

**4. What is the worst action your agent could take, and how do you prevent it?**

This is the capability gating question (Pattern 9), made personal. Be specific. Not "it could do something bad," but "it could delete the production database," or "it could send a customer email with hallucinated information," or "it could commit code that introduces a security vulnerability." For each worst case, trace the path the agent would take to get there and identify where your architecture would stop it. If you cannot identify the stopping point, you have found your next engineering task.

## Where This Leaves You

This booklet began with 513,000 lines of TypeScript and a claim: production agent architecture is fundamentally a systems engineering problem, not an AI problem. Nine chapters later, that should feel less like an assertion and more like an observation.

The patterns we have examined --- persistent context, background consolidation, risk-classified tools, layered prompts, output calibration, defense in depth, swarm orchestration, capability gating --- are engineering patterns. They are responses to engineering constraints: limited context windows, finite token budgets, probabilistic outputs, safety requirements, cost ceilings, latency bounds. The model provides the intelligence. The architecture provides the agency.

What studying Claude Code's architecture reveals --- and what this booklet has attempted to teach --- is that these patterns are not proprietary secrets. They are the natural solutions that emerge when capable engineers confront the real constraints of building AI agents for production use. Different teams, working independently, with different models and different codebases, arrive at similar patterns. The constraints are universal.

The field is young. The patterns will evolve. New constraints will emerge as models become more capable, as regulatory frameworks mature, as user expectations shift. The open questions listed in this chapter are real, and their answers will reshape agent architecture in ways we cannot fully predict.

But the foundations are solid. If you understand the nine patterns in this booklet --- not just what they are, but why they exist and when they apply --- you have a vocabulary for reasoning about agent architecture that will remain useful even as the specific implementations change. The patterns describe what agents need to do. The emerging protocols (MCP, A2A) describe how agents communicate. Frameworks like Google's ADK provide implementation scaffolding. Understanding the patterns gives you the judgment to evaluate which protocols and frameworks to adopt for your specific use case --- and, just as importantly, which to defer.

Start with the simplest architecture that could work. Add complexity in response to observed problems. Red-team your own systems before your users do. Remember those 460 lint suppressions in Claude Code's main file. Production agent code is not elegant. It is correct. Correctness is what matters.

Build the thing. Ship it. Learn from what breaks. Iterate.

> **What to take from this chapter**: Nine patterns compose into three reference architectures at different scales --- solo, supervised, and swarm. Start with the simplest architecture that addresses your trust boundary, add patterns only when observed problems demand them, and answer four questions before writing code: What is your trust boundary? Which patterns do you need? What is your token budget? What is the worst thing your agent could do? The patterns in this booklet are universal solutions to universal constraints. They will outlast any single product or model. Use them to build something that works.

---

*End of booklet.*
