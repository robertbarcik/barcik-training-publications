# Chapter 3: Background Consolidation

> **Design Pattern: AutoDream**
> *Problem:* Agent memory accumulates noise, contradictions, and stale data over days and weeks, degrading reasoning quality.
> *Solution:* Spawn a dedicated subagent during idle time that prunes, merges, and restructures memory asynchronously.
> *Tradeoff:* Background processing consumes tokens and compute even when no user task is active, and aggressive consolidation can discard context that turns out to be relevant later.
> *When to use:* Any agent that persists memory across sessions and operates over days or weeks --- which is most production agents worth building.

## The Decay Problem

If you have ever maintained a shared wiki at work, you already understand the core issue. Day one, the wiki is clean. Every page is accurate and relevant. By month six, half the pages describe processes that no longer exist, three different pages give conflicting instructions for the same task, and the search results are so noisy that people stop trusting the wiki and start asking colleagues directly.

Agent memory has the same failure mode, but worse. A production agent like Claude Code accumulates memory entries from every session: user preferences, project conventions, environment details, debugging observations, file locations, architectural decisions. Over days and weeks of active use, this memory grows. And as it grows, it rots.

The rot takes specific forms:

**Staleness.** An entry says "the API endpoint is at `/v2/users`." That was true last Tuesday. The endpoint moved to `/v3/accounts` on Thursday. The agent still reads the old entry, generates code pointing at a dead route, and the user spends twenty minutes debugging what should have been a two-minute task.

**Contradiction.** One entry from Monday says "the team uses Jest for testing." Another from Wednesday says "tests run with Vitest." Both are in memory. Which one does the agent trust? In practice, it often trusts whichever entry it encounters first in its context window --- which is determined by file ordering, not by recency or accuracy.

**Redundancy.** Twelve separate entries all note, in slightly different words, that the project uses TypeScript. Each one consumes tokens in the context window. Twelve entries saying the same thing do not make the agent twelve times more confident --- they just waste space that could hold something useful.

**Vagueness.** An early-session observation reads: "the database setup seems complicated." This was a fleeting impression, not a concrete fact. But it persists in memory, and the agent now approaches database-related tasks with unwarranted caution, hedging its responses and suggesting simpler alternatives when the user needs the actual complex solution.

Left unmanaged, these problems compound. A study of Claude Code's memory files in active use showed that after two weeks of daily sessions without consolidation, approximately 40% of memory entries were stale, redundant, or vague enough to be counterproductive. The agent was spending context window capacity --- the single most expensive resource it has --- on information that actively degraded its performance.

This is not a theoretical concern. It is a measurable engineering problem with a measurable engineering solution.

## The AutoDream Pattern

The Claude Code source reveals a pattern called AutoDream. The name is deliberate: it draws an analogy to sleep consolidation in biological brains, where memories formed during the day are reorganized, strengthened, or discarded during sleep. The analogy is imperfect --- we will address its limits shortly --- but the operational principle is sound.

AutoDream activates during user inactivity. When the system detects that the user has been idle for a configurable period (the default threshold in the source is tied to session gaps rather than a fixed timer), it spawns a dedicated subagent whose sole purpose is memory maintenance.

This subagent is not the primary agent running a side task. It is a separate, forked process with its own context window, its own system prompt optimized for maintenance operations, and its own model allocation. The primary agent's state is untouched. If the user returns mid-consolidation, the primary agent responds immediately with its existing context --- the maintenance work either completes in the background or is discarded without consequence.

The subagent performs three distinct operations, always in this order.

### Operation 1: Systematic Pruning

The consolidation subagent reads every memory entry and evaluates it against three criteria:

**Recency.** When was this entry created or last confirmed? Entries older than a configurable threshold (the source suggests a default window scaled to project activity) are flagged for review. This does not mean old entries are automatically deleted --- a foundational architectural decision from week one may still be the most important thing in memory. But old entries must justify their continued presence.

**Redundancy.** Does this entry duplicate information found elsewhere? The subagent identifies clusters of entries that express the same fact in different words. If five entries all describe the project's deployment target, four of them can go. The surviving entry is the most specific and recent one.

**Relevance.** Does this entry relate to the current state of the project? If memory contains detailed notes about a migration from PostgreSQL to MongoDB, but the migration completed three weeks ago and the project is now fully on MongoDB, those migration notes are consuming space without providing value. The relevant fact is "the project uses MongoDB" --- the historical journey to get there is noise.

Pruning is aggressive by design. The operating assumption is that it is better to lose a marginally useful memory entry than to keep the context window cluttered with marginal entries that collectively degrade every response. This is a deliberate engineering choice, and it has consequences --- occasionally, a pruned entry turns out to have been relevant. The system accepts this tradeoff because the alternative (keeping everything) has a higher and more consistent cost.

### Operation 2: Semantic Merging

After pruning, the subagent works on the surviving entries. Raw session observations are often fragmented, context-dependent, and vague. Merging transforms them into consolidated knowledge.

Consider a concrete example. After three sessions, memory might contain:

- "User prefers functional components over class components"
- "Saw user refactor a class component to a function today"
- "React components in this project use hooks, not lifecycle methods"
- "User corrected me when I suggested a class-based approach"

These four entries all point at the same underlying fact. The consolidation subagent merges them into a single, concrete entry:

- "Project convention: all React components must be functional components using hooks. Do not generate class components."

The merged entry is more useful than any of the four originals. It is specific (functional components with hooks), actionable (do not generate class components), and authoritative (stated as a convention, not an observation).

Merging also resolves contradictions. When two entries conflict, the subagent applies a resolution strategy: more recent entries override older ones, explicit user corrections override agent observations, and specific facts override general impressions. If the resolution is ambiguous, the subagent may flag the contradiction for the user rather than guessing.

The vague-to-concrete transformation is particularly valuable. "The database setup seems complicated" becomes either a specific observation ("the database uses a multi-schema PostgreSQL setup with cross-schema foreign keys") or gets pruned entirely if the subagent cannot ground the vague impression in concrete facts from other entries.

### Operation 3: Structural Optimization

The final operation reorganizes the memory file for retrieval efficiency. This is not cosmetic --- it directly affects how much useful information the agent can extract from its memory within the constraints of its context window.

The Claude Code source enforces a 200-line cap on memory files. This is a hard limit, and it is intentionally tight. Two hundred lines of well-organized, concrete memory entries provide more value than two thousand lines of unstructured session notes. The cap forces the consolidation subagent to make hard choices about what matters most.

Structural optimization involves grouping related entries (all deployment-related facts together, all coding conventions together, all user preferences together), ordering groups by access frequency (the facts the agent needs most often appear earliest, where they are more likely to fall within any truncation window), and formatting entries for fast parsing (consistent structure, no narrative prose, each entry self-contained).

The result is a memory file that reads less like a session log and more like a project configuration file: dense, organized, and immediately actionable.

## Why a Separate Subagent?

You might wonder: why not just have the primary agent tidy up its own memory at the start of each session? Or at the end? Why spawn a separate process?

The answer is context contamination.

When the primary agent is working on a user's task, its context window contains the conversation history, the relevant code, the system prompt, and the memory entries. Every token in that window contributes to the agent's reasoning about the task at hand. If you ask the same agent to simultaneously reason about memory maintenance --- which entries are stale, which should merge, how to restructure --- you are forcing it to divide its attention between two unrelated cognitive tasks.

In practice, this manifests as degraded performance on both fronts. The task reasoning suffers because the agent is "thinking about" memory organization. The memory maintenance suffers because the agent is biased toward preserving entries that seem relevant to the current task, even if they are objectively stale or redundant in the broader context.

The subagent pattern eliminates this interference. The maintenance agent has a clean context window dedicated entirely to memory evaluation. It can read the full memory file, compare entries systematically, and make restructuring decisions without any bias from an ongoing task. Meanwhile, the primary agent is either idle (waiting for the user) or active (working on a task) --- in neither case is its reasoning compromised by maintenance overhead.

This is the same principle behind why database maintenance operations --- vacuum, reindex, analyze --- run as background processes rather than inline with query execution. You do not want your query planner distracted by garbage collection.

## The Sleep Consolidation Analogy

The AutoDream name invites comparison to biological memory consolidation during sleep, and the analogy is genuinely useful --- up to a point.

During human sleep, the hippocampus replays the day's experiences and selectively strengthens, reorganizes, or discards memories. Emotionally significant memories are preferentially retained. Redundant or irrelevant sensory details are pruned. Fragmented experiences are integrated into existing knowledge structures. You go to sleep with a jumble of impressions and wake up with clearer, more organized understanding.

AutoDream does something structurally similar. It takes the raw impressions of multiple sessions (fragmented observations, redundant notes, vague feelings about the codebase) and consolidates them into organized, actionable knowledge. The timing is analogous too --- it runs during inactivity, the agent's equivalent of sleep.

But the analogy breaks down in important ways. Human sleep consolidation is deeply tied to emotional salience --- we preferentially remember what mattered to us emotionally. AutoDream has no emotional valence; it uses heuristics about recency, redundancy, and relevance. Human consolidation also creates new associative connections between memories, sometimes producing creative insights. AutoDream does not generate new knowledge; it only reorganizes existing entries. And human memory consolidation is not optional --- skip sleep and cognitive performance degrades rapidly. AutoDream is a maintenance optimization; skip it and the agent still works, just with increasing noise in its context.

Use the analogy to build intuition. Do not use it to make architectural decisions.

## From AutoDream to KAIROS: The Always-On Daemon

AutoDream handles memory consolidation during idle time. But the Claude Code source reveals a more ambitious extension of the same principle: a persistent background daemon called KAIROS.

Where AutoDream is reactive (triggered by detecting user inactivity), KAIROS is proactive. It operates as a long-running background process that continues working even when the user is entirely AFK --- away from keyboard, logged out, asleep. KAIROS extends the "do useful work during downtime" concept from memory maintenance to active project monitoring.

KAIROS maintains subscriptions to external event sources: GitHub webhooks (new PRs, failed CI runs, review comments), Slack and Discord channel activity, and system-level notifications. When an event arrives that matches the agent's project context, KAIROS can triage it, prepare a summary, draft a response, or flag it for the user's attention when they return.

The operational constraints on KAIROS are strict and deliberate. Each processing cycle has a 15-second blocking budget --- if a task takes longer than 15 seconds of wall-clock time, it is deferred or broken into smaller units. This prevents the daemon from consuming excessive resources or getting stuck on a complex reasoning chain while the user is not watching. All KAIROS output uses "brief output mode" --- machine-readable structured logs rather than conversational prose --- because no human is reading the output in real time.

The 15-second budget is an interesting design choice. It means KAIROS cannot perform deep reasoning or complex multi-step operations. It can read a GitHub notification, classify it, and write a one-paragraph summary. It cannot review a 500-line pull request in detail. This is intentional: KAIROS is a triage and preparation layer, not an autonomous decision-maker. It prepares the ground so that when the user returns and the primary agent activates, the agent has a clean, pre-processed queue of events to work through rather than a raw firehose of notifications.

This is the background consolidation pattern taken to its logical conclusion. AutoDream consolidates memory. KAIROS consolidates the project's event stream. Both run asynchronously, both use dedicated processing contexts separate from the primary agent, and both are designed to make the primary agent's interactive sessions more efficient.

## The Economics of Background Work

Background consolidation consumes tokens. Every pruning decision, every merge operation, every structural reorganization requires the subagent to read memory entries, reason about them, and write updated versions. This is not free.

But it is cheap. And the economics are deliberately designed to make it so.

The consolidation subagent does not need a frontier model. It is not writing code, not reasoning about complex architectural tradeoffs, not engaging in nuanced conversation with a user. It is performing structured maintenance operations: compare these two entries, decide which is more recent, merge them into one. This is well within the capability of smaller, faster, cheaper models.

The cost differential is substantial. As of early 2026, a frontier model like Claude Opus 4.6 costs $15 per million input tokens and $75 per million output tokens (the blended interactive rate with extended thinking). A capable mid-tier model suitable for consolidation tasks --- something in the class of Claude Haiku or a similarly positioned model --- costs roughly 1/20th of that. Running a full consolidation pass over a 200-line memory file might consume 10,000--15,000 tokens total. At mid-tier rates, that is less than a cent.

Compare that to the cost of not consolidating. A cluttered memory file means longer context windows in every interactive session (more tokens read per request), degraded response quality (leading to more back-and-forth correction cycles), and stale information causing incorrect outputs (leading to debugging sessions). A single wasted correction cycle in an interactive session with a frontier model easily costs more than a dozen consolidation passes.

> **The economics are clear:** spend fractions of a cent on background maintenance to save dollars on interactive correction cycles. Use cheap models for maintenance, reserve expensive models for the work that needs them.

## Applying This Pattern

If you are building an agent that persists memory across sessions, background consolidation is not optional --- it is as fundamental as garbage collection in a runtime. Here is how to implement it.

- **Choose your trigger.** The simplest approach is time-based: if the user has been idle for N minutes, trigger consolidation. A more sophisticated approach monitors session boundaries --- consolidate after every session ends, before the next one begins. Avoid triggering mid-session; even though the subagent runs separately, the I/O operations on memory files can create brief inconsistencies if the primary agent reads memory while the subagent is writing it.

- **Define what gets kept versus discarded.** Establish explicit retention criteria before you build the consolidation logic. At minimum: explicit user corrections are never pruned (they represent ground truth), entries confirmed in the most recent session are retained, and entries not referenced in any session for a configurable window are candidates for removal. Write these criteria into the consolidation subagent's system prompt so they are applied consistently.

- **Enforce a size cap.** The 200-line limit in Claude Code is not arbitrary --- it reflects the practical tradeoff between memory richness and context window cost. Your cap will depend on your agent's context window size and how much of it you can afford to dedicate to memory. A good starting point: memory should consume no more than 5--10% of your total context budget. If your agent has an 128K-token context window, that is 6,400--12,800 tokens for memory --- roughly 100--200 lines of concise entries.

- **Validate consolidated output.** After the subagent rewrites the memory file, run a basic validation pass. Are there duplicate entries? Does the file exceed the size cap? Are all entries in the expected format? This is a simple programmatic check, not an LLM call --- do not spend tokens validating what a deterministic script can verify.

- **Use the cheapest model that works.** Profile your consolidation tasks against multiple model tiers. You will almost certainly find that the cheapest tier that can reliably follow structured instructions (compare, merge, prune) produces results indistinguishable from a frontier model on these maintenance tasks. The consolidation subagent does not need to be creative or nuanced --- it needs to be consistent and fast.

- **Log what was changed.** Every consolidation pass should produce a diff or changelog: which entries were pruned, which were merged, which were restructured. This serves two purposes. First, it lets you audit consolidation quality --- if the subagent is pruning entries that the primary agent later needs, you will see it in the logs and can adjust your retention criteria. Second, it gives the user transparency into what happened to their agent's memory while they were away.

- **Handle the cold-start case.** A brand-new agent with an empty memory file does not need consolidation. An agent with three entries does not need consolidation. Build in a minimum-threshold check: only trigger consolidation when memory exceeds a meaningful size (50+ entries is a reasonable floor). Below that threshold, the overhead of spawning a subagent exceeds the benefit of cleanup.

- **Plan for the KAIROS extension.** Even if you do not build a full event-monitoring daemon today, design your consolidation architecture with extensibility in mind. The subagent pattern --- separate context, separate model, background execution, structured output --- is the same pattern you will use for event triage, notification processing, and proactive monitoring when you are ready to add those capabilities. Build the subagent infrastructure once, reuse it across all background operations.

> **What to take from this chapter:** Agent memory is not a write-once store --- it is a living system that degrades without active maintenance. The AutoDream pattern solves this by running a dedicated maintenance subagent during idle time, performing three operations: pruning stale entries, merging fragmented observations into concrete facts, and restructuring for retrieval efficiency. The pattern extends naturally into always-on background daemons like KAIROS that monitor external events between sessions. Background work uses cheap models for structured tasks, saving expensive frontier models for interactive reasoning. If your agent persists memory, build consolidation from day one.

---

*Next: [Chapter 4 --- Tool Design and Constraint Architecture](04_tool_design_constraints.md)*
