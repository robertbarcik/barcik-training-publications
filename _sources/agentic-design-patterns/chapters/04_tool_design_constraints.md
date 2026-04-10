# Chapter 4: Tool Design and Constraint Architecture

> **Design Pattern: Risk-Classified Tools with Least-Privilege Access**
> *Problem:* Agents that can do anything will eventually do something catastrophic --- and the blast radius grows with capability.
> *Solution:* Classify every tool invocation by risk level, restrict the action space to what is necessary, and require human authorization for high-risk operations.
> *Tradeoff:* Tighter constraints reduce autonomy and slow down workflows that require frequent high-risk operations, creating friction for power users.
> *When to use:* Every agent that acts on the real world. There are no exceptions.

<div class="key-points">
<div class="kp-title">Key Points</div>
<ul>
<li>Tools define what an agent <strong>can</strong> and <strong>cannot</strong> do — tool design is agent design</li>
<li>Three-tier risk classification: LOW (auto-approve), MEDIUM (visible, proceeding), HIGH (blocked until authorized)</li>
<li>Claude Code restricts web access to an 85-domain whitelist — predictability, relevance, and security</li>
<li>Constraints <em>improve</em> agent performance: smaller action space means better planning and more recoverable errors</li>
<li>MCP (Model Context Protocol) is standardizing tool risk annotations across the industry</li>
</ul>
</div>

<div class="stat-row">
<div class="stat-card"><div class="stat-number">~30</div><div class="stat-label">Tools in Claude Code</div></div>
<div class="stat-card"><div class="stat-number">85</div><div class="stat-label">Whitelisted web domains</div></div>
</div>

## Tools Are the Agent

There is a persistent misconception in early agent design that the language model is the agent and tools are accessories --- optional add-ons that extend what the agent can do. This gets the relationship backwards.

A language model without tools is a chatbot. It can reason, draft, and suggest, but it cannot act. It cannot read a file, run a test, create a branch, deploy a service, or send an email. The moment you give a model tools, it becomes an agent --- and the tools you give it define what kind of agent it is.

This is not a philosophical point. It is an architectural one. When you design an agent's tool set, you are making the most consequential decisions about the agent's behavior, risk profile, and failure modes. A model with access to `read_file` and `write_file` is a text editor. Add `execute_shell` and it is a system administrator. Add `send_http_request` and it is a network client. Add `delete_directory` and it can cause real damage.

The Claude Code source makes this principle explicit in its architecture. The system exposes approximately 30 distinct tools to the model, and every single one of them passes through a risk classification layer before execution. The model does not "have access to the file system." It has access to specific, individually classified operations on the file system, each with its own authorization requirements.

> **The principle is simple:** tool design is agent design. The set of tools you expose, and the constraints you place on each one, determines your agent's capability envelope more than any prompt engineering or model selection.

## The Risk Classification System

Every tool invocation in Claude Code is assigned one of three risk levels: LOW, MEDIUM, or HIGH. The classification is not based on what the tool is, but on what the specific invocation does. The same tool can be LOW risk in one context and HIGH risk in another.

### LOW Risk: Silent Auto-Approval

LOW-risk operations execute without any user notification. The agent calls them, they run, results come back. The user never knows it happened unless they inspect the agent's work afterward.

Examples from the Claude Code source:

- **Reading files.** The `Read` tool at any file path the agent has access to. Reading cannot modify state, so it is inherently low risk.
- **Listing directory contents.** Knowing what files exist does not change anything.
- **Running `git status`, `git log`, `git diff`.** These are read-only git operations. They report state without changing it.
- **Searching file contents.** Grep, ripgrep, and similar search operations. Read-only by definition.
- **Glob pattern matching.** Finding files by name pattern. Again, read-only.

The common thread: LOW-risk operations are strictly read-only. They cannot modify files, cannot change system state, cannot transmit data externally, and cannot cause any outcome that requires reversal. The agent can execute thousands of LOW-risk operations per session without any human oversight, and the worst possible outcome is wasted compute.

### MEDIUM Risk: Visible but Proceeding

MEDIUM-risk operations are shown to the user in the interface but do not require explicit approval before executing. The user sees what is happening and can intervene if something looks wrong, but the default is to proceed.

Examples:

- **Writing or editing files.** The agent modifies a source file. This changes state, but the change is reversible (via git), visible (the user can review the diff), and contained (it affects one file in the local workspace).
- **Running non-destructive shell commands.** Commands like `npm install`, `python -m pytest`, or `cargo build` modify local state (installing packages, generating build artifacts) but are routine development operations with well-understood effects.
- **Creating new files.** Similar to editing --- the file appears in the workspace, is visible in git status, and can be deleted if unwanted.
- **Git operations that modify local state.** `git add`, `git commit`, `git checkout` (to an existing branch). These change the local repository but are reversible and do not affect remote state.

MEDIUM-risk operations share a profile: they modify local state in ways that are visible, reversible, and contained within the user's workspace. The user is informed but not blocked, because requiring approval for every file edit would make the agent unusable for its primary purpose (writing and modifying code).

### HIGH Risk: Hard Block Pending Authorization

HIGH-risk operations do not execute until the user explicitly authorizes them. The agent proposes the action, explains what it intends to do, and waits. No timeout, no auto-approval, no "proceed if the user doesn't respond within 30 seconds."

Examples:

- **Executing arbitrary shell scripts.** A command the agent has composed that is not on the recognized-safe list. The user must read the command, understand what it does, and approve it.
- **Deleting directories or files outside the project scope.** Removing a single generated file might be MEDIUM risk; deleting a directory tree is HIGH.
- **Network operations to non-whitelisted destinations.** Sending HTTP requests, establishing WebSocket connections, or any operation that transmits data outside the local machine to a domain not on the approved list.
- **Git operations that affect remote state.** `git push`, especially `git push --force`. Once pushed, changes affect collaborators and may be difficult to reverse.
- **Modifying system configuration.** Changing environment variables, editing dotfiles outside the project, modifying system-level settings.

HIGH-risk operations have one or more of these characteristics: they are irreversible (or difficult to reverse), they affect systems beyond the local workspace, they transmit data externally, or their consequences are difficult to predict from the invocation alone.

> **Design Pattern: Risk classification is not about what the tool is --- it is about what the specific invocation does.** `git checkout main` (switching to an existing branch) is MEDIUM. `git checkout -- .` (discarding all local changes) is HIGH. Same tool, same command prefix, radically different risk profiles. Your classification system must evaluate the full invocation, not just the tool name.

<div class="risk-cards">
<div class="risk-card risk-low"><div class="risk-label">LOW Risk</div><div class="risk-desc">Read-only operations — file reads, searches, git status. Auto-approved silently. Cannot modify state or transmit data.</div></div>
<div class="risk-card risk-medium"><div class="risk-label">MEDIUM Risk</div><div class="risk-desc">Local, reversible changes — file edits, installs, git commits. Shown to user but proceeds without blocking.</div></div>
<div class="risk-card risk-high"><div class="risk-label">HIGH Risk</div><div class="risk-desc">Irreversible or external impact — arbitrary shell scripts, git push, network calls to non-whitelisted domains. Hard-blocked until user authorizes.</div></div>
</div>

## The 85-Domain Web Whitelist

One of the most revealing constraints in the Claude Code source is the `WebSearchTool` configuration. Claude Code does not have unrestricted internet access. The web search capability is restricted to exactly 85 pre-approved domains.

This list includes documentation sites (MDN, Stack Overflow, the official docs for major frameworks and languages), package registries (npm, PyPI, crates.io), and reference sources (GitHub, Wikipedia). It does not include arbitrary websites, social media platforms, news sites, or any domain not explicitly enumerated.

The implementation goes further than just URL filtering. When Claude Code fetches a web page, the parsing logic operates exclusively on the `<body>` element. The `<head>` is discarded entirely --- no metadata, no Open Graph tags, no structured data, no SEO markup. Within the body, the parser extracts text content and basic structure, but complex elements like HTML tables are converted to flat unstructured text rather than being preserved as tabular data.

Why these specific constraints? Three reasons.

**Predictability.** An agent that can access any website might encounter hostile content --- prompt injections embedded in web pages, misleading information, or content that causes the model to behave unexpectedly. Restricting to 85 known-good domains reduces this attack surface dramatically. You know what Stack Overflow pages look like. You do not know what an arbitrary website contains.

**Relevance.** Claude Code is a coding agent. The 85 domains on its whitelist are the domains a developer actually needs: documentation, package registries, code repositories, and technical references. Everything else is noise. An unrestricted web search might return blog posts, opinion pieces, outdated tutorials, or SEO-optimized garbage. The whitelist ensures that every web result comes from a source that is likely to contain accurate, relevant technical information.

**Security.** Every external connection is a potential data exfiltration vector. An agent that can access any URL can be tricked (via prompt injection or adversarial instructions in a file it reads) into sending sensitive data to an attacker-controlled server. The whitelist limits exfiltration to 85 specific domains, all of which are well-known public services that do not accept arbitrary data uploads via URL parameters.

The body-only parsing is a separate security measure. Metadata in `<head>` elements can contain tracking pixels, redirect instructions, and other elements that are useful for browsers but potentially dangerous for an agent that processes content programmatically. Stripping the head eliminates an entire category of attacks at the cost of losing some useful structured data --- a tradeoff the designers clearly considered acceptable.

## Why Constraints Improve Agents

This is counterintuitive for engineers coming from a capabilities-first mindset. If the model can access the entire internet, why limit it to 85 domains? If it can run any shell command, why classify some as HIGH risk and block them?

The answer is that constraints improve agent performance, not just agent safety.

### Smaller action space, better planning

An agent with ten available tools can reason about which tool to use for a given task. An agent with a thousand available tools spends most of its reasoning capacity on tool selection rather than task execution. The Claude Code tool set is carefully curated to around 30 tools --- enough to cover the full range of coding tasks, few enough that the model can reliably select the right tool on the first attempt.

This is directly analogous to API design in software engineering. A well-designed API has a small surface area with clear, orthogonal operations. A poorly designed API has hundreds of overlapping endpoints, and developers spend more time reading documentation than writing code. Your agent's tool set is its API to the world.

### Errors are more recoverable

When you constrain the action space, you constrain the error space. An agent that can only read and write files in a single project directory cannot accidentally delete the operating system. An agent that can only access 85 web domains cannot be tricked into sending data to an attacker's server. The worst-case failure of a constrained agent is bounded and recoverable; the worst-case failure of an unconstrained agent is unbounded.

This matters for user trust. Users who know that the agent cannot do catastrophic things are more willing to let it operate autonomously on routine tasks. Paradoxically, an agent with tighter constraints often receives more autonomy from users than an agent with loose constraints, because users trust it more.

### Behavior is more predictable

Constraints eliminate entire categories of behavior. If the agent cannot access the network, you do not need to worry about network-related failure modes. If it cannot delete files outside the project, you do not need to worry about cross-project contamination. Each constraint you add removes a class of potential behaviors, making the agent's overall behavior more predictable and easier to test.

Predictability is not just a safety property. It is a usability property. Users develop mental models of what the agent will and will not do. Constraints make those mental models accurate. When the mental model matches reality, users work with the agent more effectively.

> **The paradox of constraint:** Agents with fewer capabilities often outperform agents with more capabilities, because the constrained agent spends its reasoning on the task while the unconstrained agent spends its reasoning on capability selection, error recovery, and navigating the consequences of overly broad actions.

## Least Privilege as an Architectural Principle

The principle of least privilege --- every component should have only the minimum access necessary to perform its function --- is decades old in security engineering. Applying it to AI agents requires thinking about privilege at three distinct levels.

### OS-Level Privilege

The agent process itself runs within an operating system, and the first layer of constraint is what the OS allows the process to do. Claude Code runs in a sandboxed environment that restricts:

- **File system access.** The agent process can read and write within the user's project directory and a limited set of configuration paths. It cannot access arbitrary locations on the file system.
- **Process execution.** Shell commands run in a constrained subprocess. The agent cannot spawn persistent daemons, modify system services, or interact with other users' processes.
- **Network access.** Outbound connections are restricted by the whitelist discussed above. Inbound connections are not opened at all --- the agent does not listen on any port.

These are not LLM-level constraints. They are enforced by the runtime environment at the operating system level. Even if the model generates a tool call that attempts to read `/etc/shadow`, the sandbox prevents execution before the model's output is even evaluated. This is defense in depth: the risk classification system is the first gate, the OS sandbox is the second.

### Tool-Level Privilege

Within the set of operations the OS allows, the tool layer further restricts what the agent can do. Not every OS-permitted operation is exposed as a tool. The agent process might technically be able to open a network socket (the sandbox allows it for whitelisted domains), but if there is no tool that exposes socket operations, the model has no way to request one.

This is where tool design becomes critical. Every tool you expose is a capability you are granting to the model. Every tool you do not expose is a capability you are withholding. The design question is not "what could this agent possibly need?" but "what is the minimum set of tools that lets this agent do its job?"

For Claude Code, the answer is approximately 30 tools covering file operations (read, write, edit, glob, grep), version control (git commands via shell), web access (search within whitelisted domains), and system operations (shell command execution with risk classification). Notably absent: direct database access, email sending, cloud service API calls, and file transfer protocols. If the user needs the agent to interact with a database, they provide the credentials and the agent constructs the appropriate shell command --- which then goes through risk classification.

### Data-Level Privilege

The finest-grained privilege level controls what data the agent can access within the operations it is permitted to perform. The agent might have the `read_file` tool, but that does not mean it should read every file.

In Claude Code, this manifests as awareness of file sensitivity. The system prompt instructs the agent to avoid reading files that likely contain secrets (`.env` files, credential stores, private keys) unless specifically directed to by the user. This is a soft constraint --- it is enforced by the model's instruction-following rather than by the runtime --- but it layers on top of the hard constraints at the OS and tool levels.

Data-level privilege also applies to output. The agent should not include sensitive data (API keys, passwords, personal information) in its responses, even if it encounters such data during the course of its work. This is enforced through system prompt instructions and output filtering.

The three levels work together as defense in depth:

1. The OS sandbox prevents the agent from doing things it has no business doing
2. The tool set restricts the agent to specific, well-defined operations
3. The data-level instructions guide the agent's behavior within those operations

If any single layer fails, the others still provide protection. The OS sandbox does not rely on the model following instructions. The tool restrictions do not rely on the OS sandbox being perfectly configured. Each layer independently constrains the agent's behavior.

## Risk Classification Across Agent Types

The three-tier risk classification system (LOW, MEDIUM, HIGH) is not specific to coding agents. It applies to any agent that acts on the real world. But the specific classification of operations changes depending on the agent's domain and the consequences of its actions.

The following table illustrates how the same framework applies to three different agent types. Notice how the same category of action can be classified differently depending on the domain context.

| Operation | Code Agent | Customer Service Agent | Data Analysis Agent |
|---|---|---|---|
| **Read internal data** | LOW (read source files) | LOW (read customer record) | LOW (query read-only database) |
| **Search/retrieve** | LOW (grep, glob) | LOW (search knowledge base) | LOW (search data catalog) |
| **Write local files** | MEDIUM (edit source code) | N/A | MEDIUM (save analysis output) |
| **Send message to user** | MEDIUM (terminal output) | MEDIUM (draft email reply) | MEDIUM (share report link) |
| **Execute computed action** | HIGH (run shell script) | HIGH (process refund) | HIGH (execute SQL write query) |
| **Modify external system** | HIGH (git push, deploy) | HIGH (update billing system) | HIGH (write to production DB) |
| **Access external network** | HIGH (non-whitelisted URL) | MEDIUM (fetch order status from internal API) | HIGH (call external API) |
| **Delete/destroy** | HIGH (rm -rf, drop table) | HIGH (delete customer account) | HIGH (drop table, purge dataset) |
| **Escalate to human** | N/A | LOW (transfer to agent) | LOW (flag for review) |

Several patterns emerge from this comparison.

**Read operations are universally LOW risk.** Regardless of domain, reading data without modifying it is safe. This is the one classification that rarely changes between agent types.

**The MEDIUM tier is domain-specific.** For a code agent, writing files is routine and reversible (git provides the safety net). For a customer service agent, sending an email is the equivalent --- routine, expected, and the core function of the agent. The MEDIUM tier contains the operations that are the agent's primary job, where blocking on every invocation would make the agent useless.

**The HIGH tier is defined by irreversibility and external impact.** Processing a refund cannot be undone. Pushing to a remote repository affects collaborators. Executing a write query changes production data. These operations share the property that mistakes are expensive and difficult to reverse.

**Escalation to a human is always LOW risk.** An agent that asks for help cannot cause harm by asking. This is worth noting because some agent designs inadvertently discourage escalation by making it a heavyweight operation. It should be the easiest thing an agent can do.

## File System Access Patterns

The distinction between read, write, and execute permissions in the file system deserves specific attention, because it illustrates how granular risk classification needs to be in practice.

**Read access** is broadly granted. Claude Code can read any file within the project scope and certain configuration files outside it. Reading is the agent's primary information-gathering mechanism, and restricting it too aggressively would cripple the agent's ability to understand the codebase it is working on. The exception is sensitive files (`.env`, private keys, credentials), where the agent is instructed to avoid reading unless directed.

**Write access** is granted but classified as MEDIUM risk. The agent can create and modify files, but every write operation is visible to the user and reversible via version control. The key design decision here is that write access is to individual files, not to arbitrary byte ranges on disk. The `Write` tool writes a complete file; the `Edit` tool performs a string replacement within a file. There is no raw disk I/O, no binary file manipulation, no low-level file system operations. This abstraction limits the damage a malformed write can cause.

**Execute access** --- the ability to run files as programs --- is the most tightly controlled. Shell command execution goes through risk classification on every invocation. The system maintains a list of recognized-safe commands (git operations, package managers, test runners, build tools) that receive automatic MEDIUM classification. Any command not on the safe list is classified as HIGH and requires explicit approval.

The boundary between write and execute is where most agent security incidents occur. An agent that can write a file and execute it can do essentially anything the operating system allows. Claude Code handles this by classifying the execution step separately from the write step. You can write a shell script (MEDIUM risk) without the agent automatically being able to run it (HIGH risk). The user must approve the execution as a separate action.

## Designing Your Own Tool Taxonomy

The principles from Claude Code's tool design apply directly to any agent you build. Here is how to approach the design.

**Start with the job to be done.** List every action your agent needs to perform to accomplish its core purpose. Be specific --- not "interact with the database" but "run SELECT queries against the analytics database," "insert rows into the activity log table," and "update customer records in the CRM table." Each specific action becomes a candidate tool.

**Classify by consequence, not by mechanism.** A SELECT query and a DROP TABLE statement both "interact with the database." They have radically different consequences. Classify each candidate tool based on what happens if the agent uses it incorrectly. Can the mistake be detected? Can it be reversed? Does it affect systems beyond the agent's workspace? Does it affect other users?

**Prefer specific tools over general ones.** A tool called `execute_sql` that accepts any SQL string is a general tool. Tools called `query_analytics`, `log_activity`, and `update_customer` are specific tools. Specific tools are easier to classify (you know exactly what each one does), easier to monitor (you can track usage by operation type), and safer (the model cannot construct a DROP TABLE statement if the only write tool is `update_customer` with a predefined schema).

**Build the whitelist, not the blacklist.** Do not start with "the agent can do everything" and then try to block dangerous operations. Start with "the agent can do nothing" and add only the capabilities it needs. Every tool you add is a conscious decision to expand the agent's action space. This is harder to get wrong than trying to enumerate everything that should be blocked.

**Make escalation cheap.** Your agent should always have a LOW-risk path to request human help. If the agent encounters a situation where it needs a capability it does not have, the correct behavior is to tell the user, not to find a creative workaround using the tools it does have. Creative workarounds using existing tools are how agents cause unexpected damage.

## The Emerging Standard: Model Context Protocol

The risk classification principles described in this chapter are no longer just internal production patterns. They are being codified into an open industry standard.

The Model Context Protocol (MCP), originally created by Anthropic and donated to the Linux Foundation's Agentic AI Foundation in late 2025, standardizes how AI agents discover, describe, and invoke external tools. As of early 2026, MCP has over 10,000 deployed servers and nearly 100 million monthly SDK downloads, with backing from Anthropic, OpenAI, Google, Microsoft, and AWS.

MCP's tool annotation system maps directly to the risk classification this chapter teaches. Every tool in MCP can declare four annotations: `readOnlyHint` (does this tool modify its environment?), `destructiveHint` (are those modifications irreversible?), `idempotentHint` (are repeated calls safe?), and `openWorldHint` (does this tool interact with entities beyond the agent's workspace?). The critical design choice: all annotations default to worst-case. A tool with no annotations is assumed to be destructive, non-idempotent, and interacting with the open world. This mirrors the whitelist-not-blacklist principle --- you prove safety rather than assuming it.

MCP also enforces least privilege at the protocol level. Each tool server operates in isolation --- it cannot see the conversation, cannot see other servers, and cannot access resources outside its declared scope. The host application mediates everything. This is server-level sandboxing built into the communication protocol itself.

One detail worth replicating in any tool system: MCP's structured error handling. When a tool call fails, the error response includes `suggested_actions` and `follow_up_tools`, giving the model structured guidance on what to try next rather than leaving it to guess. This turns tool failures from dead ends into navigation points.

If you are designing tool interfaces for your agent today, building them as MCP-compatible servers is worth serious consideration. You get standardized discovery, schema validation, risk annotation, and a growing ecosystem of client implementations --- and you avoid building bespoke tool plumbing that you will eventually have to replace.

## Applying This Pattern

Every agent needs tools, and every tool needs a risk classification. Here is the practitioner checklist.

- **Audit your tool set.** List every tool your agent can access. For each one, answer: what is the worst thing that can happen if the agent uses this tool incorrectly? If the answer includes "data loss," "unauthorized access," "financial impact," or "affects other users," that tool is HIGH risk and must require human authorization.

- **Implement three-tier classification at the runtime level, not the prompt level.** Prompt-level instructions ("do not delete files without asking") are helpful but insufficient. The model can ignore instructions, misunderstand them, or be manipulated into overriding them via prompt injection. Risk classification must be enforced by the runtime: the code that executes tool calls must check the risk level and block HIGH-risk operations regardless of what the model requests.

- **Classify invocations, not tools.** The same tool with different parameters can have different risk levels. `git checkout feature-branch` and `git checkout -- .` are both invocations of git, but one is MEDIUM and the other is HIGH. Your classification logic must evaluate the full tool call, including parameters.

- **Maintain a whitelist of known-safe operations.** For tools like shell execution that accept arbitrary input, maintain an explicit list of commands and patterns that are pre-classified as LOW or MEDIUM. Everything not on the list defaults to HIGH. Update the list as you learn which operations your agent performs routinely and safely.

- **Log every tool invocation with its risk classification.** This gives you the data to refine your classifications over time. If a HIGH-risk tool is being invoked dozens of times per session and users are always approving it, consider whether it should be reclassified as MEDIUM. If a MEDIUM-risk tool occasionally causes problems, consider elevating it to HIGH.

- **Consider MCP-compatible tool interfaces.** The Model Context Protocol's annotation vocabulary (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) provides a standardized way to express the risk classification this chapter teaches, and MCP's server isolation enforces least privilege at the protocol level. Building your tools as MCP servers gives you ecosystem compatibility for free.

- **Restrict network access to a whitelist.** If your agent needs web access, enumerate the specific domains it needs and block everything else. The cost of maintaining a whitelist is far lower than the cost of an exfiltration incident. Start with the smallest possible list and add domains only when a specific use case requires them.

- **Separate read, write, and execute permissions.** Even if your runtime environment allows all three, expose them as separate tools with separate classifications. The agent should not be able to write a file and execute it in a single tool call. Make execution a distinct, separately classified operation.

- **Design for the adversarial case.** Assume that at some point, someone will craft a file or prompt that tries to trick your agent into misusing its tools. Your risk classification and OS-level sandboxing should contain the damage even if the model is successfully manipulated. If your safety depends entirely on the model following instructions, your safety depends on something you cannot guarantee.

- **Test your constraints, not just your capabilities.** Write tests that verify the agent cannot do things it should not be able to do. Can it read files outside its project scope? Can it execute a shell command without classification? Can it access a non-whitelisted URL? These negative tests are at least as important as the positive tests that verify the agent can do its job.

> **What to take from this chapter:** Tools define what your agent is. A risk classification system --- LOW (auto-approve), MEDIUM (visible, proceeding), HIGH (blocked pending authorization) --- provides the framework for safe tool execution. Constraints on the action space do not just improve safety; they improve the agent's reasoning, predictability, and the user's willingness to grant autonomy. Apply least privilege at three levels: OS sandboxing, tool-set curation, and data access controls. Build the whitelist, not the blacklist. And enforce constraints in the runtime, not just the prompt.

---

*Next: [Chapter 5 --- Prompt Architecture and the Cost of Instructions](05_prompt_architecture.md)*
