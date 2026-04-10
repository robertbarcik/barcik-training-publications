# Chapter 6: Output Calibration and the Assertiveness Problem

> **Design Pattern: Confidence Calibration**
> *Problem:* More capable models can produce more confidently wrong outputs, and users cannot distinguish confident-correct from confident-wrong at interaction speed.
> *Solution:* Instrument false claim rates per model and task type, implement assertiveness controls, and route tasks to models whose reliability profile matches the risk level.
> *Tradeoff:* Reducing false confidence makes the agent slower and more hesitant; users prefer decisiveness, but decisiveness without calibration causes harm.
> *When to use:* Any agent that takes autonomous actions or produces outputs that downstream systems or humans will act on without independent verification.

<div class="key-points">
<div class="kp-title">Key Points</div>
<ul>
<li>Capybara v8 nearly doubled false claims (16.7% → 30%) — a capability upgrade caused a reliability regression</li>
<li>Confident errors are worse than hesitant ones — they bypass the human's verification instinct</li>
<li>Assertiveness counterweight: a prompt-level behavioral control that handicaps autonomy to improve accuracy</li>
<li>Model selection is runtime routing, not a one-time choice — route by task risk profile</li>
<li>Self-critique catches what the counterweight prevents — prevention + correction, not either/or</li>
</ul>
</div>

<div class="stat-row">
<div class="stat-card"><div class="stat-number">16.7% → 30%</div><div class="stat-label">False Claims Regression (v4 → v8)</div></div>
<div class="stat-card"><div class="stat-number">~10%</div><div class="stat-label">Stop Sequence Failure Rate</div></div>
<div class="stat-card"><div class="stat-number">90×</div><div class="stat-label">Capability Jump (Mythos vs Opus)</div></div>
</div>

---

## The Capybara v8 Regression

Anthropic's internal model taxonomy, exposed in the leaked source, uses animal codenames to identify the models powering different product tiers. Tengu refers to the Claude Code application itself. Fennec is the codename for Opus 4.6, the flagship model. Capybara designates an advanced intermediate-tier model --- more capable than the lightweight options, less expensive than the frontier tier. Numbat references an unreleased future model, and Mythos refers to the frontier research models.

The codenames are not the interesting part. The telemetry data attached to them is.

Internal evaluation metrics revealed that Capybara v8 --- a model upgrade intended to improve capability --- exhibited a 29-30% false claims rate in production. This was not a marginal increase. Capybara v4, the version it replaced, had a false claims rate of 16.7%. The upgrade nearly doubled the rate at which the model confidently asserted things that were not true.

Let that number settle. In an autonomous coding agent, a 30% false claims rate means that roughly one in three factual assertions the model makes --- about function signatures, variable types, API behaviors, file contents --- could be wrong. And the model does not flag these assertions as uncertain. It states them with the same confidence it uses for assertions that happen to be correct.

This was documented internally as an "actual regression." Not a cosmetic issue. Not a style problem. A measurable degradation in the reliability of the model's outputs, introduced by an upgrade that improved the model's capabilities in other dimensions.

## Why Confident Errors Are Worse Than Hesitant Ones

An agent that says "I am not sure whether this function exists --- let me check" and then reads the file is being slow but safe. An agent that says "The `processData` method accepts three arguments: the input array, a callback function, and an options object" --- when the method actually accepts two arguments --- is being fast and dangerous.

The danger compounds in an agent architecture. Consider the chain of events. The model asserts that a function has a particular signature. Based on that assertion, it writes code that calls the function with the wrong number of arguments. The code is syntactically valid. The agent commits it. The tests fail, but the failure message is about a runtime error, not about the hallucinated signature. The developer now has to debug backward from the runtime error to discover that the agent fabricated a function signature. Time lost: 15 minutes. Trust eroded: significant.

Now multiply this by every developer on a team, across every session, over weeks. A 30% false claims rate does not mean 30% of sessions fail. It means that the fabric of trust between the developer and the agent degrades until the developer starts treating every assertion as suspect --- at which point the agent's productivity benefit collapses.

> **The core problem:** An agent that confidently executes wrong actions is worse than one that hesitates, because confident errors bypass the human's verification instinct. When the agent sounds certain, the human stops checking.

This is not a hypothetical concern. It is the fundamental challenge of deploying autonomous agents in production. The model's confidence is not correlated with its accuracy in the way human confidence (imperfectly) correlates with human expertise. A model can be maximally confident and maximally wrong simultaneously. The user has no reliable signal to distinguish the two states.

## The Assertiveness-Accuracy Tradeoff

Users want decisive agents. In user research and product feedback, the consistent signal is clear: people prefer agents that act quickly, commit to a course of action, and explain what they did --- rather than agents that hedge, ask clarifying questions, and present multiple options for the user to choose from.

This preference is rational. The entire point of an agent is to reduce the human's cognitive load. An agent that asks "should I use method A or method B?" for every decision is not much better than a search engine. Users want the agent to pick the better method, use it, and move on.

But this creates a direct tension with accuracy. A model that always commits to its first interpretation, never hedges, and never asks for clarification will be faster and more pleasant to use --- and it will also be wrong more often, with no warning. A model tuned for maximum assertiveness is a model tuned to suppress its own uncertainty signals.

Anthropic's response to the Capybara v8 regression was to implement what the internal documentation calls an "assertiveness counterweight" --- a behavioral control layered into the system prompt that explicitly instructs the model to limit its autonomous actions, verify assumptions before acting, and flag uncertainty rather than suppressing it.

This is a remarkable architectural choice. Rather than retraining the model to be less confident (which risks degrading its capabilities), they added a prompt-level behavioral constraint that handicaps the model's autonomy. The agent is told, in effect: you are capable of making bold decisions, but we are going to make you hesitate anyway, because your confidence is not calibrated to your accuracy.

The tradeoff is real. The assertiveness counterweight makes the agent slower. It increases the number of turns required to complete a task. It introduces more "let me verify" steps that feel redundant when the model happens to be correct. Users who upgraded to the new model version noticed the change and some complained about the agent being "less helpful." But the alternative --- an agent that confidently introduces bugs into codebases at a 30% rate --- is not a viable product.

## Stop Sequence Failures and the Fragility of Model Upgrades

The Capybara v8 issues went beyond false claims. Internal telemetry also documented a roughly 10% failure rate involving false triggers of stop sequences. When `<functions>` tags appeared at the tail of the prompt --- a normal occurrence in the tool-calling protocol --- the model would sometimes interpret the tag as a signal to stop generating rather than as context to process. The result: truncated or empty responses that broke the agent's execution loop.

A separate failure mode involved complete stalls on empty `tool_result` messages. When a tool returned no output (a successful but silent operation, like writing a file with no errors), the model would sometimes fail to continue generating, treating the empty result as an error condition or end-of-conversation signal.

These failures illustrate a principle that matters for any production agent system: model upgrades are not safe by default. A model that passes all your benchmark evaluations can still introduce novel failure modes that your test suite never anticipated, because the failure modes emerge from the interaction between the model's behavior and your system's protocol, not from the model's capabilities in isolation.

The `<functions>` tag issue is a particularly instructive example. The model was trained on vast amounts of markup, including XML-like tags. The v8 model had learned to associate certain tag patterns with stopping behavior, creating a subtle interference between the model's language understanding and the application protocol built on top of it. No amount of capability benchmarking would have caught this. Only production telemetry --- monitoring actual agent behavior across thousands of sessions --- revealed the pattern.

> **The operational lesson:** When you upgrade the model powering your agent, your unit tests and capability benchmarks are necessary but not sufficient. You need production telemetry that monitors behavioral metrics: stop rate, empty response rate, tool call success rate, and false claim rate. These are the metrics that tell you whether the upgrade is safe to ship.

## Model Selection as an Architectural Decision

The Claude Code architecture does not use a single model for all tasks. The leaked source reveals a routing layer that selects different models based on the nature of the operation. This is not just a cost optimization. It is a reliability architecture.

Consider the spectrum of tasks an agent performs in a typical coding session:

- **Classification tasks:** Is this a question about the codebase or a request to modify it? Does this file match the user's intent? These are low-stakes, high-frequency decisions where speed matters more than depth.
- **Search and retrieval:** Finding relevant files, reading documentation, locating function definitions. Moderate complexity, moderate stakes.
- **Code generation:** Writing new functions, modifying existing code, creating test cases. High complexity, high stakes --- errors here directly produce bugs.
- **Reasoning and planning:** Deciding on an approach, evaluating tradeoffs, sequencing multi-step operations. The highest complexity, where the model's full capabilities are needed.

Using a frontier model for classification tasks is wasteful --- you are paying $5.00 per million tokens for a task that a model at $0.30 per million tokens can handle with equivalent accuracy. But using a cheap model for code generation is reckless --- the few dollars you save on tokens will cost you hours of debugging time.

The architectural pattern is model routing by task risk profile:

| Task type | Risk level | Model tier | Rationale |
|-----------|-----------|------------|-----------|
| Intent classification | Low | Fast/cheap | Speed matters, errors are recoverable |
| File search and reading | Low-Medium | Fast/cheap | High volume, straightforward accuracy |
| Code generation | High | Capable/expensive | Errors create bugs, hard to detect |
| Multi-step planning | High | Capable/expensive | Errors cascade through subsequent steps |
| Safety-critical decisions | Critical | Most capable | False negatives cause harm |

This routing table is not static. It should be tuned based on your observed false claim rates per model per task type. If your production telemetry shows that your cheap model handles code generation at an acceptable error rate for a specific language or framework, you can route that traffic to the cheaper tier. If your capable model shows regression on a specific task type after an upgrade, you can temporarily route that traffic to the previous version.

The key insight: model selection is not a one-time decision made at architecture time. It is a runtime decision made per-task, informed by ongoing measurement.

## The "Say I Don't Know" Problem

One of the hardest calibration challenges in language models is getting them to accurately express uncertainty. The fundamental issue is asymmetric training incentives.

During training, models are rewarded for producing correct, helpful responses. They are penalized for producing harmful or incorrect responses. But the penalty structure creates a perverse incentive: it is almost always safer (from the model's training perspective) to produce a confident-sounding answer than to say "I don't know." A confident answer that happens to be correct receives full reward. A confident answer that happens to be wrong receives a penalty. But "I don't know" receives neither reward nor penalty --- and in a training regime optimized for helpfulness, neutral is worse than risky.

The result is models that almost never say "I don't know" even when they should. The Capybara v8 false claims rate of 30% is a direct manifestation of this: the model asserts things it is uncertain about because its training has optimized for asserting rather than abstaining.

Training models to refuse is comparatively straightforward. Safety training has produced reliable refusal behavior for harmful requests. But training models to refuse when they are uncertain about factual claims --- not when the claim is harmful, but when it is likely wrong --- is a different and harder problem. It requires the model to maintain an accurate internal estimate of its own reliability, which is a metacognitive capability that current architectures support only partially.

For agent builders, the practical implication is that you cannot rely on the model to self-report its uncertainty. You need external calibration mechanisms:

- **Retrieval verification:** Before the agent asserts a fact about the codebase (a function signature, a file's contents, a dependency version), require it to read the source of truth first. The Claude Code system prompt enforces this pattern: "Read the file before editing it."
- **Tool-based grounding:** Structure your agent so that factual claims are grounded in tool outputs rather than model memory. An agent that says "the test passed" because it ran the test and saw the output is more reliable than an agent that says "the test should pass" based on its understanding of the code.
- **Confidence thresholds in prompts:** Explicitly instruct the model to flag low-confidence assertions. "If you are uncertain whether a function exists, check the file rather than assuming." This does not solve the calibration problem, but it adds a prompt-level nudge toward verification.

## The Non-Linear Scaling Insight

There is a counterintuitive relationship between model capability and reliability that the Capybara regression illustrates. More capable models are not linearly more reliable. In some cases, they are less reliable in specific dimensions.

The mechanism is this: as models gain the ability to perform more complex reasoning and abstraction, they also gain the ability to construct more elaborate --- and more plausible-sounding --- incorrect explanations. A small model that hallucinates a function name produces an obviously wrong output that a developer spots immediately. A large model that constructs a coherent but incorrect explanation of why a race condition occurs in a specific code path produces an output that a developer might spend 30 minutes investigating before realizing the entire analysis was fabricated.

This is not a speculative concern. The jump from 16.7% to 30% false claims between Capybara v4 and v8 happened alongside improvements in the model's benchmark scores. The model got better at coding tasks on standard evaluations and simultaneously got worse at accurately reporting what it knew. It became more capable and less calibrated in the same upgrade.

The implication for agent architects: do not assume that upgrading to a more powerful model will improve your agent's end-to-end reliability. It may improve capability (the agent can handle harder tasks) while degrading calibration (the agent is wrong more often on easy tasks, and wrong more convincingly on hard ones). You need separate metrics for both dimensions.

> **The scaling paradox:** A more capable model can be a less reliable agent. Capability measures what the model can do at its best. Reliability measures what the model does on average, including how it handles the cases where it is wrong. These are different properties, and they do not scale together.

## Building Calibration Into Your Agent

Production calibration is not a one-time exercise. It is an ongoing operational discipline, similar to monitoring latency or error rates in a traditional service. Here is what it requires.

### Instrument false claim rates

Define what constitutes a "false claim" in your agent's domain. For a coding agent, this might be: asserting a function exists when it does not, reporting a test passed when it failed, or stating a dependency is installed when it is not. Build automated checks that sample agent outputs and verify claims against ground truth. Track this rate per model version and per task type.

### Define accuracy thresholds per task type

Not all tasks require the same accuracy. A code search that returns 90% relevant results is acceptable. A code modification that introduces a bug 10% of the time is not. Define your thresholds explicitly, and use them to drive model selection and assertiveness tuning.

### Monitor behavioral regressions across model upgrades

When your model provider ships an update, do not just run your benchmark suite. Run your behavioral telemetry for 48 hours on a canary deployment before rolling out to all users. Watch for: changes in false claim rates, changes in stop/stall rates, changes in tool usage patterns, and changes in the ratio of assertive to hedging responses.

### Design assertiveness controls

Build the equivalent of Anthropic's assertiveness counterweight into your agent. This is a tunable parameter --- a section of your system prompt that you can adjust to make the agent more or less autonomous. In high-risk deployments (financial systems, healthcare, production infrastructure), dial assertiveness down. In low-risk deployments (prototyping, documentation, exploratory analysis), dial it up.

The control does not need to be binary. You can structure it as a spectrum:

- **Level 1 (cautious):** Agent proposes actions and waits for approval on every step.
- **Level 2 (balanced):** Agent executes low-risk actions autonomously, proposes high-risk actions for approval.
- **Level 3 (autonomous):** Agent executes most actions autonomously, only pausing for irreversible operations.

The appropriate level depends on the task, the user's expertise, and the consequences of failure. A senior developer debugging a prototype can tolerate Level 3. A junior developer modifying a production database schema should be working at Level 1.

### Self-critique as a calibration mechanism

The assertiveness counterweight is an externally imposed constraint --- you are telling the model to be less confident. A complementary approach is to build self-correction into the agent's workflow: have the agent evaluate its own output before presenting it to the user.

This is the Producer-Critic pattern. The producing agent generates output (code, a plan, a refactoring proposal). A separate evaluation pass --- either a distinct agent or a second LLM call with a different prompt --- reviews the output for hallucinated functions, nonexistent variables, logical errors, and violations of the project's conventions. The evaluation pass does not need to be perfect. It needs to catch enough errors to shift the balance.

In practice, one reflection pass on a coding agent's output typically catches a meaningful fraction of the errors that would otherwise reach the user. Diminishing returns set in quickly: a second pass catches fewer new issues, and a third pass rarely justifies its cost. For most use cases, a single reflection cycle is the right balance between quality and latency.

The counterweight and self-critique address different failure modes. The counterweight is preventive --- it makes the agent less likely to propose aggressive changes in the first place. Self-critique is corrective --- it catches errors in what the agent has already produced. A well-calibrated agent uses both. The counterweight reduces the volume of mistakes. Self-critique catches the ones that get through.

The cost is real: each reflection cycle is an additional LLM call, adding both latency and token spend. Route this decision by task risk. For a low-stakes file rename, skip the reflection. For a database migration script, the cost of one additional LLM call is trivial compared to the cost of a broken migration in production.

## Applying This Pattern

- **Measure before you trust.** Before deploying any model in your agent, establish baseline false claim rates for your specific task types. Do not rely on the provider's benchmark scores --- they measure capability, not calibration. Run your own evaluations on your own data.

- **Treat model upgrades as risky deployments.** When your model provider ships an update, canary it. Monitor behavioral metrics for at least 48 hours before full rollout. The Capybara v4-to-v8 regression was caught by internal telemetry --- if it had been caught only by user complaints, the damage would have been far greater.

- **Build model routing, not model selection.** Do not pick one model and use it for everything. Build a routing layer that selects models based on task type and risk level. Use cheap models for cheap tasks and expensive models for expensive mistakes.

- **Implement assertiveness controls as a tunable parameter.** Build a mechanism to adjust how autonomously your agent acts. Make it configurable per deployment context. What works for a hackathon prototype is not appropriate for a production banking system.

- **Ground claims in tool outputs.** Structure your agent to verify factual assertions through tool calls rather than relying on the model's parametric memory. An agent that reads the file before claiming what it contains is more reliable than one that guesses from training data.

- **Accept the assertiveness-accuracy tradeoff explicitly.** You cannot have an agent that is both maximally decisive and maximally accurate. Decide where your product sits on this spectrum, communicate it to your users, and instrument both dimensions so you know when the balance shifts.

- **Design for graceful uncertainty.** Train your agent's prompts to express uncertainty constructively. "I believe this function takes two arguments, but let me verify" is better than both "this function takes two arguments" (when wrong) and "I don't know anything about this function" (when the model actually has useful partial knowledge). The goal is calibrated confidence, not zero confidence.

- **Plan for the non-linear scaling trap.** When evaluating newer, more capable models, test specifically for overconfidence regressions. A model that scores higher on coding benchmarks but produces more plausible-sounding errors is a net negative for your agent's reliability. Measure both dimensions independently.

---

*Next: [Chapter 7 — Security Architecture for Agentic Systems](07_security_architecture.md)*
