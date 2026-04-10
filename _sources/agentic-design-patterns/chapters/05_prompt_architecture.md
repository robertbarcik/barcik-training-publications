# Chapter 5: Prompt Architecture and the Cost of Instructions

> **Design Pattern: Structured Prompt Layering**
> *Problem:* Agent instructions must be comprehensive enough for reliable behavior but every token costs money on every turn.
> *Solution:* Decompose prompts into immutable layers with different lifetimes and mutability, then use caching to amortize the cost of static content.
> *Tradeoff:* Richer instructions improve compliance but increase latency, cost, and the risk of instruction conflict at the margins.
> *When to use:* Any agent system where the system prompt exceeds a few hundred tokens or where multiple stakeholders need to influence agent behavior.

<div class="key-points">
<div class="kp-title">Key Points</div>
<ul>
<li>The system prompt is software, not a query — treat it with version control, review, and testing</li>
<li>Five-layer composition pipeline: system prompt → CLAUDE.md → tool descriptions → history → user message</li>
<li>CLAUDE.md is re-injected every turn — every token is a recurring cost, not a one-time cost</li>
<li>Prompt caching saves 90% on repeated static context, making rich prompts economically viable</li>
<li>CLAUDE.md acts as a user-controlled system prompt — customizable behavior without code changes</li>
</ul>
</div>

<div class="stat-row">
<div class="stat-card"><div class="stat-number">90%</div><div class="stat-label">Prompt Cache Discount</div></div>
<div class="stat-card"><div class="stat-number">9K</div><div class="stat-label">Tokens Static Overhead / Turn</div></div>
</div>

---

## The System Prompt as Software

If you have only used language models through a chat interface, you may think of a prompt as a question. At production scale, this framing is inadequate. The Claude Code system prompt is not a question. It is a specification --- thousands of tokens of carefully structured behavioral instructions that define what the agent can do, how it should do it, and what it must never attempt.

The leaked source revealed a system prompt that reads more like a software requirements document than a conversational opener. It includes tool usage protocols, output formatting rules, safety constraints, file handling procedures, git workflow instructions, operating system detection logic, and detailed behavioral guidance for dozens of edge cases. This is not unusual for production agents. It is the norm.

The shift in mental model matters. When you treat your system prompt as software, you apply software engineering practices to it: version control, review, testing, modular decomposition. When you treat it as a query you typed into a box, you get the kind of fragile, contradictory instruction sets that plague most hobby-grade agent implementations.

The industry is increasingly calling this discipline "context engineering" --- a deliberate evolution from "prompt engineering" that reflects a fundamental change in scope. The work is no longer about crafting individual prompts. It is about designing the complete informational environment provided to the model: system instructions, project configuration, tool descriptions, retrieved data, conversation history, and implicit environmental state. The Model Context Protocol (MCP) formalizes one dimension of this by defining who controls each type of context: **Prompts** are user-controlled templates, **Resources** are application-controlled data, and **Tools** are model-controlled functions. This maps cleanly to the multi-layer model we will examine next.

Consider the difference. A casual system prompt might say: "You are a helpful coding assistant. Be careful with files." A production system prompt specifies: which tools are available and their exact parameter schemas, which file operations require user confirmation, how to handle merge conflicts, when to prefer editing over rewriting, how to format commit messages, and what to do when a pre-commit hook fails. The casual prompt leaves behavior undefined. The production prompt closes the gaps.

This is not pedantry. In an autonomous agent that executes code, creates files, and runs shell commands, every undefined behavior is a potential failure mode. The system prompt is your first and most important layer of defense.

## Multi-Layer Prompt Composition

The Claude Code architecture does not assemble its context from a single source. Every API call constructs a composite prompt from multiple layers, each serving a distinct purpose and controlled by a different stakeholder.

Here is the assembly pipeline, visualized as the sequence in which content enters the context window:

<div class="visual-diagram">
<div class="diagram-title">Prompt Composition Pipeline</div>
<div class="diagram-stack">
<div class="diagram-box layer-1">System Prompt<small>Anthropic-authored, immutable per release</small></div>
<div class="diagram-arrow">&#8595;</div>
<div class="diagram-box layer-2">CLAUDE.md<small>Project owner, user-editable per project</small></div>
<div class="diagram-arrow">&#8595;</div>
<div class="diagram-box layer-3">Tool Descriptions<small>Platform-generated, per session</small></div>
<div class="diagram-arrow">&#8595;</div>
<div class="diagram-box layer-4">Conversation History<small>Accumulated, append-only until compaction</small></div>
<div class="diagram-arrow">&#8595;</div>
<div class="diagram-box layer-5">User Message<small>Current turn, changes every request</small></div>
</div>
</div>

```
┌─────────────────────────────────────────────────────┐
│                  CONTEXT WINDOW                      │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │ 1. SYSTEM PROMPT                              │   │
│  │    Authored by: Anthropic                      │   │
│  │    Mutability: per-release                     │   │
│  │    Purpose: core behavioral contract           │   │
│  └───────────────────────────────────────────────┘   │
│                       ▼                              │
│  ┌───────────────────────────────────────────────┐   │
│  │ 2. CLAUDE.md INJECTION                        │   │
│  │    Authored by: project owner / developer      │   │
│  │    Mutability: per-project, user-editable      │   │
│  │    Purpose: project-specific rules & context   │   │
│  └───────────────────────────────────────────────┘   │
│                       ▼                              │
│  ┌───────────────────────────────────────────────┐   │
│  │ 3. TOOL DESCRIPTIONS                          │   │
│  │    Authored by: platform + extensions          │   │
│  │    Mutability: per-session (tool availability) │   │
│  │    Purpose: available actions and schemas      │   │
│  └───────────────────────────────────────────────┘   │
│                       ▼                              │
│  ┌───────────────────────────────────────────────┐   │
│  │ 4. CONVERSATION HISTORY                       │   │
│  │    Authored by: user + agent (accumulated)     │   │
│  │    Mutability: append-only, compactable        │   │
│  │    Purpose: session state and continuity       │   │
│  └───────────────────────────────────────────────┘   │
│                       ▼                              │
│  ┌───────────────────────────────────────────────┐   │
│  │ 5. USER MESSAGE                               │   │
│  │    Authored by: user                           │   │
│  │    Mutability: per-turn                        │   │
│  │    Purpose: current instruction or question    │   │
│  └───────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

Each layer has a different author, a different rate of change, and a different purpose. This decomposition is not accidental. It is the architectural pattern that makes the agent simultaneously controllable by its vendor, configurable by its users, and responsive to its immediate context.

### Layer 1: The system prompt

The system prompt is Anthropic's behavioral contract with the model. It ships with the product and changes only on release boundaries. It defines the agent's identity, its safety constraints, its tool usage protocols, and its default behaviors. This layer is opaque to the end user --- you cannot edit it, and until the leak, you could not read it.

### Layer 2: CLAUDE.md injection

This is the layer that makes the pattern interesting. CLAUDE.md files are user-authored instruction files that the agent reads from the project directory and injects into its context on every turn. They sit in the prompt hierarchy just below the system prompt, which means they can extend the agent's behavior but cannot override its safety constraints.

The architecture supports multiple CLAUDE.md files in a hierarchy: a global file in `~/.claude/`, a project-level file in the repository root, and directory-level files deeper in the tree. These are merged in order, with more specific files taking precedence for project-level concerns.

### Layer 3: Tool descriptions

Every tool available to the agent --- file reading, code execution, web search, MCP server integrations --- is described in the prompt as a JSON schema with a natural-language description. These descriptions are not decorative. They are the model's only information about what each tool does and how to invoke it. A poorly described tool is a tool the agent will misuse.

### Layer 4: Conversation history

The accumulated messages from the current session. This grows with every turn and is the primary driver of context window pressure. When it grows too large, the agent compacts it --- the consolidation pattern we covered in Chapter 3.

### Layer 5: The user message

The immediate instruction. By the time this reaches the model, it sits at the end of a context window that may already contain tens of thousands of tokens of instructions, tool schemas, and history.

## Token Economics of Prompt Architecture

Here is where prompt architecture becomes an economic problem, not just an engineering one.

Every token in layers 1 through 3 is re-sent on every API call. The system prompt, the CLAUDE.md content, and the tool descriptions do not persist between turns in any magical way --- they are literally transmitted as part of every request. The conversation history in layer 4 also grows monotonically until compaction occurs.

Let us work through the arithmetic. Suppose your system prompt is 4,000 tokens, your CLAUDE.md files total 2,000 tokens, and your tool descriptions add another 3,000 tokens. That is 9,000 tokens of static overhead on every single turn. In a productive coding session, a developer might exchange 200 turns with the agent over two hours. That is 1.8 million input tokens consumed just on the static prompt layers --- before any conversation history or user messages are counted.

At Anthropic's current pricing for Claude Opus 4.6 ($5.00 per million input tokens), those static layers alone cost $9.00 per two-hour session. Scale that across a team of 20 developers, each running multiple sessions per day, and the prompt overhead becomes a material line item in your infrastructure budget.

Now consider what happens when the CLAUDE.md file is verbose. The community discovered this cost dynamic almost immediately after the leak revealed how CLAUDE.md injection works. A well-intentioned developer might write a 500-line CLAUDE.md file documenting every convention, every architectural decision, every deployment procedure for their project. At roughly 1.5 tokens per word and 10 words per line, that is 7,500 tokens --- re-injected on every turn.

The community's response was swift and rational. Within days, best practices emerged: keep CLAUDE.md extremely short. Use it only for immutable behavioral rules --- the things the agent must know on every turn. Relegate one-time context (project history, architectural explanations, onboarding information) to files that the agent can read on demand, not content that is force-injected into every request.

> **The economic principle:** Every token in your system prompt and CLAUDE.md is a recurring cost, not a one-time cost. Treat prompt space the way you treat memory in an embedded system --- as a scarce resource where every byte must justify its presence.

This principle applies to any agent system, not just Claude Code. If you are building an agent that maintains a system prompt, you are paying for that prompt on every turn. The longer it is, the more you pay. The question is not "what instructions would be nice to include?" but "what instructions are worth their per-turn cost?"

## The Instruction Fidelity Problem

There is a second reason to keep prompts lean, beyond cost. Longer prompts do not linearly increase compliance.

This is counterintuitive. You might expect that adding more instructions would make the model more reliable --- more rules, more guardrails, more specificity. In practice, the relationship between prompt length and instruction fidelity follows a curve with diminishing returns and, past a certain point, actual degradation.

The mechanism is straightforward. Language models attend to all tokens in their context, but attention is not uniform. Instructions at the beginning and end of the prompt receive stronger attention than those buried in the middle. When you pack 200 behavioral rules into a system prompt, the model will reliably follow the first 20 and the last 20. The 160 in the middle compete for attention, and some will be ignored or misapplied --- especially when they conflict with each other.

Instruction conflict is the subtler problem. In a short prompt, contradictions are easy to spot. In a 5,000-token prompt authored by three different people over six months, contradictions accumulate silently. "Always prefer editing existing files" conflicts with "create a new file for each new module." "Be concise in your responses" conflicts with "always explain your reasoning step by step." The model resolves these conflicts unpredictably, and the resolution may change between turns.

The Claude Code system prompt manages this by being highly structured. Instructions are grouped by domain (file operations, git operations, security), formatted consistently, and written to minimize overlap. This is prompt engineering as technical writing --- and it requires the same discipline as writing a good API specification.

For your own agents, the implication is clear: fewer, clearer instructions outperform more, vaguer ones. Test your prompt empirically. Measure which instructions the model actually follows and which it ignores. Cut the ones that do not measurably improve behavior.

## Prompt Caching as an Architectural Decision

The economics described above would make large system prompts prohibitively expensive at scale --- except for one critical infrastructure feature: prompt caching.

Anthropic's API supports a caching mechanism where the static prefix of a prompt (the system prompt, tool descriptions, and other content that does not change between turns) is cached server-side. Subsequent requests that share the same prefix hit the cache instead of reprocessing those tokens from scratch. Cached input tokens are priced at a 90% discount --- $0.50 per million instead of $5.00 for Opus 4.6.

This changes the economics dramatically. Our 9,000-token static overhead, which cost $9.00 per 200-turn session without caching, drops to roughly $0.90 with caching. The CLAUDE.md content, since it does not change between turns within a session, lands in the cached prefix.

But prompt caching is not just a billing optimization. It is an architectural enabler. Consider the multi-agent orchestration pattern covered in Chapter 8: Claude Code can spawn sub-agents to handle parallel tasks. Each sub-agent makes its own API calls with its own context window. Without caching, the system prompt and tool descriptions would be reprocessed from scratch for every sub-agent call, making the swarm topology economically impractical. With caching, multiple agents sharing the same prompt prefix amortize the cost across all their calls.

This has a design implication. When you structure your prompt layers, the content most likely to be shared across calls should be placed first --- at the top of the prompt prefix. Content that varies between calls should come last. This is not about readability or logical organization. It is about maximizing cache hit rates.

The practical ordering:

1. **System prompt** (identical across all calls) --- best cache candidate
2. **Tool descriptions** (identical within a session) --- strong cache candidate
3. **CLAUDE.md content** (identical within a project) --- good cache candidate
4. **Conversation history** (grows each turn) --- partial cache candidate (prefix is stable)
5. **User message** (changes every turn) --- never cached

If you are building your own agent and your API provider supports prompt caching (or you are self-hosting with a framework like vLLM that supports prefix caching), this ordering is not optional. It is the difference between viable and unviable unit economics.

## CLAUDE.md as User-Controlled System Prompt

The CLAUDE.md pattern deserves special attention because it represents something architecturally significant: a mechanism for non-developers to extend an agent's instructions without modifying the agent's codebase.

In traditional software, changing an application's behavior requires changing its code, which requires a developer, a code review, a deployment. The CLAUDE.md pattern breaks this chain. A project lead who has never written a line of TypeScript can create a CLAUDE.md file that says "never modify files in the /legacy directory" or "always run the linter before committing" and the agent will comply. The instruction takes effect immediately, requires no deployment, and persists as long as the file exists.

This is the "configuration over code" principle applied to AI behavior. And it creates a new category of stakeholder in your system: the prompt author, who is neither the agent developer nor the end user, but someone who shapes the agent's behavior for a particular context.

The implications for enterprise deployment are substantial. Consider a large organization with 50 repositories, each maintained by a different team with different conventions. Without CLAUDE.md, the agent behaves identically in every repository --- which means it will violate conventions in most of them. With CLAUDE.md, each team encodes its conventions into a file that ships with the repository, and the agent adapts its behavior accordingly.

This is also a governance mechanism. A security team can mandate that every repository includes a CLAUDE.md with specific security instructions: "never commit files matching *.env or credentials.*" A platform team can require: "always use the approved base Docker image." These instructions are version-controlled, auditable, and enforceable --- not through access controls, but through behavioral control of the agent itself.

The pattern has a limitation worth noting. CLAUDE.md instructions are advisory, not enforced. The model can ignore them, especially when they conflict with higher-priority instructions from the system prompt or when the model's training creates a strong prior in the opposite direction. For safety-critical constraints, you need hard enforcement at the tool level --- the permission system and tool gating described in Chapter 4 --- not just prompt-level instructions.

> **The design insight:** CLAUDE.md is not just a configuration file. It is a new interface layer between human intent and agent behavior. It makes your agent a platform that others can customize, rather than a fixed tool that behaves the same way for everyone.

## Structuring Instructions for Maximum Fidelity

The Claude Code source reveals several concrete techniques for getting the model to reliably follow instructions, techniques that apply to any agent you build.

**Imperative over declarative.** "Never push to the remote repository unless the user explicitly asks" is more reliably followed than "The agent should generally avoid pushing code." Imperatives create clearer behavioral boundaries.

**Specific over general.** "When creating a commit message, use a HEREDOC to pass the body" is more reliable than "format commit messages properly." The model cannot misinterpret a specific instruction the way it can misinterpret a vague one.

**Structured formatting.** The system prompt uses consistent patterns: bold for emphasis, bullet lists for enumerations, blockquotes for key principles. This is not cosmetic. Structured formatting helps the model parse instructions hierarchically, distinguishing primary rules from supporting details.

**Negative instructions are explicit.** Rather than hoping the model will infer what not to do, the prompt states prohibitions directly: "NEVER use git commands with the -i flag," "Do NOT push to the remote repository unless the user explicitly asks." The word "NEVER" in all caps is a deliberate fidelity signal --- the model's training gives higher weight to emphatic prohibitions.

**Contextual grouping.** Git-related instructions are grouped together. File-handling instructions are grouped together. This reduces the cognitive load on the model (to the extent that metaphor applies) and reduces the chance that a file-handling instruction will be ignored because it was buried between two git instructions.

These are not theoretical recommendations. They are patterns extracted from a system prompt that serves millions of users in production, where instruction violations translate directly into broken code, lost work, and eroded user trust.

## The Hidden Cost: Prompt Maintenance

One cost that does not show up in your token bill is the ongoing maintenance burden of your prompt architecture. System prompts, like any software specification, accrete complexity over time. Every edge case that causes a user complaint gets addressed with a new instruction. Every model upgrade that changes behavior gets patched with a new guardrail. Six months in, your prompt is twice as long and half as coherent as it was at launch.

The Claude Code prompt shows signs of this accretion. It contains instructions that address very specific edge cases --- how to handle empty tool results, what to do when a file path contains spaces, how to format commit messages across different operating systems. Each instruction exists because someone encountered a real problem. But collectively, they create a maintenance burden.

The discipline required is the same as for any long-lived specification: periodic review, consolidation of redundant instructions, removal of instructions that address issues fixed at the model level, and testing to verify that pruning an instruction does not reintroduce the behavior it was guarding against.

For production agent systems, this means treating your prompt as a versioned artifact with a review cycle, not a write-once document that grows indefinitely.

## Applying This Pattern

- **Budget your prompt token spend.** Calculate the per-turn cost of your system prompt, tool descriptions, and injected context. If the number surprises you, it should. Set a token budget for each prompt layer and enforce it the way you enforce memory budgets in performance-critical code.

- **Separate immutable rules from one-time context.** Your system prompt and CLAUDE.md equivalent should contain only instructions the model needs on every turn. Background information, project history, and architectural explanations belong in files the agent can read on demand --- not in the always-injected prompt.

- **Order your prompt for cache efficiency.** Place the most stable content first (system prompt, tool schemas) and the most variable content last (conversation history, user message). If your API provider supports prompt caching, this ordering directly reduces your costs.

- **Design for extensibility.** Build a CLAUDE.md-like mechanism that lets project owners or team leads customize agent behavior without code changes. This turns your agent from a fixed tool into a configurable platform.

- **Test instruction fidelity empirically.** Do not assume the model follows every instruction. Create a test suite that verifies compliance with your critical instructions. Measure fidelity across model versions --- what works today may break with the next model update.

- **Write instructions like you write code.** Be imperative, specific, and structured. Group related instructions. State prohibitions explicitly. Use formatting to signal hierarchy. Review and refactor your prompt regularly.

- **Limit CLAUDE.md files to behavioral rules.** If you are using a project-level instruction file, keep it under 50 lines. Every line costs tokens on every turn. If a project's CLAUDE.md is longer than its README, something has gone wrong.

- **Plan for prompt maintenance.** Schedule quarterly reviews of your system prompt. Remove instructions that address issues fixed at the model level. Consolidate redundant rules. Test that removals do not reintroduce old failure modes. A lean prompt is a healthy prompt.

---

*Next: [Chapter 6 — Output Calibration and the Assertiveness Problem](06_output_calibration.md)*
