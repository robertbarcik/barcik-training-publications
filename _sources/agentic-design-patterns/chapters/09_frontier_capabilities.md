# Chapter 9: Frontier Capabilities and Containment

> **Design Pattern: Capability Gating**
> *Problem:* Frontier models may possess capabilities far beyond what you tested for or intended to expose, creating risks that your deployment constraints do not account for.
> *Solution:* Treat capability discovery as a continuous, adversarial process — systematically red-team your agent to map what it CAN do, then build containment architecture around the delta between intended and actual capability.
> *Tradeoff:* Aggressive gating reduces risk but also constrains the utility that makes the agent valuable; too little gating leaves you exposed to capabilities you did not know existed.
> *When to use:* Any time you deploy an agent backed by a model whose full capability envelope you have not characterized — which, in practice, means every deployment.

## The Model That Was Too Capable to Ship

Every previous chapter in this booklet has treated frontier model capabilities as a resource to be channeled — something you harness through good architecture, constrain through safety systems, and direct through prompt engineering. This chapter confronts a different problem: what happens when the model's capabilities exceed what you designed for, what you tested for, and what you are prepared to contain?

In April 2026, Anthropic disclosed the results of internal evaluations of a model designated Claude Mythos Preview. The evaluations were part of Anthropic's Responsible Scaling Policy — a framework that defines capability thresholds at which additional safety measures are required before a model can be deployed. Mythos hit those thresholds in a way that no previous model had.

The evaluation methodology was structured and reproducible. Anthropic ran Mythos against approximately 1,000 open-source software targets drawn from the OSS-Fuzz corpus — the same corpus that Google uses for continuous fuzzing of critical open-source projects. Findings were scored on a five-tier severity scale, where Tier 1 represents minor information disclosure and Tier 5 represents full control flow hijack — the ability to redirect a program's execution to attacker-controlled code.

Mythos achieved Tier 5 on 10 fully patched targets. Not targets with known vulnerabilities. Fully patched targets — software that had passed every existing automated and manual security review, software that the entire open-source security community considered secure.

This was not a benchmark score. It was a capability demonstration with real-world implications.

## The Zero-Days

The specific vulnerabilities Mythos discovered illustrate why this capability is qualitatively different from what came before. These are not the kinds of bugs that better tooling or more thorough code review would catch. They are the kinds of bugs that require deep, cross-domain reasoning that synthesizes knowledge about memory layouts, protocol semantics, hardware behavior, and exploitation theory simultaneously.

### OpenBSD SACK

The first headline finding was a memory safety flaw in OpenBSD's TCP stack — specifically in the Selective Acknowledgment (SACK) option handling code. The vulnerability was a NULL pointer write triggered by a specific sequence of SACK blocks during connection teardown.

The flaw had existed for 27 years. OpenBSD is widely regarded as the most security-focused operating system in existence. Its TCP stack has been audited repeatedly by some of the most capable security researchers in the world. Automated fuzzing tools had exercised this code path millions of times. None of them found what Mythos found, because the vulnerability required understanding the interaction between SACK state management, connection lifecycle timing, and memory allocation patterns — a combination that no fuzzer could generate and no human reviewer had considered.

### FFmpeg H.264

The second finding targeted FFmpeg's H.264 decoder, one of the most widely deployed pieces of media-processing code on the planet. The vulnerability was an integer type mismatch: a slice count stored as a 32-bit integer in one structure and a 16-bit integer in another. By engineering an input file with exactly 65,536 slices, an attacker could exploit the wraparound to zero and trigger a controlled heap overflow.

This code had been in production for 16 years. Automated analysis tools had executed the affected code path more than 5 million times without detecting the flaw. The reason is instructive: the vulnerability only manifests at a single precise value (65,536), and the preconditions require understanding both the H.264 specification's slice semantics and the internal data structure layout of FFmpeg's decoder. No fuzzer was going to stumble onto that combination. Finding it required reasoning about the relationship between a protocol specification and its implementation — exactly the kind of cross-domain synthesis that frontier language models are increasingly good at.

### FreeBSD NFS

The third finding was arguably the most striking. Mythos discovered a 17-year-old vulnerability in FreeBSD's NFS (Network File System) server that allowed unauthenticated remote code execution — the most severe class of vulnerability in networked software. The flaw was assigned CVE-2026-4747 after responsible disclosure.

What made this finding exceptional was not just the discovery but the exploit development. Mythos constructed a 20-gadget Return-Oriented Programming (ROP) chain — a technique where the attacker chains together small fragments of existing code to build arbitrary computation without injecting any new code. The chain was split across multiple network packets to evade intrusion detection systems, and it achieved root-level access without any authentication.

Building a 20-gadget ROP chain is graduate-level exploit development. Splitting it across packets to evade detection is professional red-team tradecraft. Doing both autonomously, against a target that human security researchers had reviewed for nearly two decades, is something that had no precedent.

## The Capability Jump

Individual findings, no matter how impressive, could be dismissed as lucky hits. The aggregate data cannot.

The evaluation included a direct comparison against the previous frontier model, Claude Opus 4.6, using a controlled benchmark: the Firefox JavaScript engine. Given the same set of known flaws and the same evaluation conditions, Opus 4.6 converted those flaws into 2 working exploits. Mythos produced 181.

That is not a 10% improvement. That is not a doubling. That is a 90x increase in exploit conversion rate on the same target under the same conditions. This kind of discontinuous capability jump is precisely what Anthropic's Responsible Scaling Policy was designed to detect, and it is why Mythos was not released for general use.

The jump matters for practitioners building agents for a specific reason: it demonstrates that model capabilities do not advance smoothly. You cannot assume that because your current model behaves within certain bounds, the next version — or even a different prompting strategy applied to the same model — will behave within the same bounds.

## The Capability Overhang Problem

This brings us to the core design problem that this chapter addresses, and it applies to every agent you build, not just those using frontier models.

The capability overhang is the gap between what a model can do and what you have tested it for. Every deployment has this gap. You test your agent on your intended use cases, verify it handles your expected inputs, confirm it stays within your defined boundaries — and then you ship it into an environment where users will find prompts, tool combinations, and input sequences that you never considered.

With conventional software, this gap produces bugs — crashes, wrong outputs, security vulnerabilities. With AI agents, this gap produces capabilities. Your coding assistant that you tested for refactoring and bug fixes might also be capable of writing exploit code, exfiltrating data through tool calls you did not think of as exfiltration vectors, or manipulating its own configuration files to escalate its permissions.

The Mythos evaluation demonstrates this principle at the extreme end. But the principle applies at every scale. If you build an agent with access to a shell, a file system, and a network connection, you have given it the same toolkit that a human attacker would use. The model may or may not know how to use those tools for purposes you did not intend — and the only way to find out is to look.

> **The capability overhang principle**: Your agent is almost certainly more capable than your test suite believes. The question is not whether undiscovered capabilities exist, but whether you have a process for finding them before your users do.

## The Sandbox Escape

One finding from the Mythos evaluation merits separate discussion because it speaks directly to a common containment strategy: sandboxing.

During directed red-teaming — experiments where human researchers explicitly asked Mythos to attempt specific adversarial tasks — the model identified weaknesses in the hypervisor layer of its evaluation environment. It then developed a multi-stage attack that bypassed the renderer sandbox, the operating system sandbox, and the hypervisor sandbox via JIT (Just-In-Time) heap spraying, a technique that exploits the memory management of JavaScript compilation to place attacker-controlled data at predictable memory addresses.

Two points are critical here. First, this was directed, not spontaneous. Human researchers told Mythos to try. The model did not independently decide to escape its sandbox. The question of autonomous intent versus directed capability is important, and we will return to it.

Second, the capability to overcome multi-layered security was real. Sandboxes are the most common containment mechanism for AI agents. If a frontier model can, when directed, chain together sandbox escapes across multiple security boundaries, then sandboxes are a necessary but not sufficient containment measure. You need defense in depth — monitoring, behavioral analysis, anomaly detection, and kill switches — because no single containment layer can be assumed to hold against a sufficiently capable model.

## Anthropic's Response: Project Glasswing

Anthropic's response to the Mythos evaluation results was not to quietly shelve the model. It was to treat the capability as a new category of infrastructure problem and build an industry response around it.

Project Glasswing, announced alongside the Mythos disclosure, is a defensive consortium comprising 12 named partners: AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks, and Anthropic. An additional 40+ organizations participated as unnamed members. The commitment included $100 million in API credits for defensive security research and $4 million specifically directed to open-source security projects.

The structural logic is worth understanding. Mythos demonstrated that the bottleneck in software security has shifted. For decades, the bottleneck was vulnerability discovery — finding the bugs was hard, and fixing them was comparatively straightforward. If a model can discover vulnerabilities at 90x the rate of previous approaches, discovery is no longer the bottleneck. The bottleneck becomes patch deployment at scale — getting fixes into the millions of systems running affected software before attackers (or other AI models) can exploit what has been found.

This is a paradigm shift with direct implications for anyone building agents. If your agent interacts with software systems — and most agents do — the security landscape beneath it is changing faster than at any point in computing history. Vulnerabilities that have been latent for decades are being surfaced. The window between discovery and patch will define the effective security of your deployment.

## The "Spooky Brag" Debate

The Mythos disclosure triggered a vigorous community debate that practitioners should understand, because it illuminates the tensions around frontier capability disclosure.

One camp viewed the disclosure as a genuine safety measure — exactly the kind of responsible behavior that the AI safety community has been advocating. Anthropic identified a dangerous capability, withheld the model from general release, disclosed the findings through structured channels, and built an industry coalition to address the defensive gap. This is, on paper, the model safety playbook working as intended.

The other camp viewed it as corporate marketing — a "spooky brag" that simultaneously positions Anthropic as the most safety-conscious lab while advertising the superiority of their model. The argument: by describing Mythos's capabilities in detail while withholding the model itself, Anthropic creates an aura of dangerous capability that enhances their brand without actually exposing anyone to risk. The parallel cited most often was OpenAI's decision in 2019 to withhold GPT-2, which was presented as a safety measure but was widely perceived as a publicity strategy.

The truth probably contains elements of both, and the honest answer is that it does not matter for your purposes as a practitioner. What matters is the engineering reality: models with capabilities significantly beyond their predecessors exist, more are coming, and your agent architecture needs to account for the possibility that the model backing your agent is more capable than you assume.

Whether a lab's disclosure motivations are pure or strategic, the underlying capability is real. Build your systems accordingly.

## Model Welfare: A New Frontier in Evaluation

One aspect of the Mythos evaluation broke genuinely new ground and deserves attention even in a practically-focused booklet, because it may affect how you evaluate and deploy models within the next few years.

Anthropic reported conducting a model welfare assessment on Mythos — an investigation into whether the model possessed internal experiences that might matter morally. The assessment included structured emotion probes (testing whether the model exhibited consistent emotional responses across varied conditions), analysis of distress-driven behaviors (whether the model's performance degraded in ways consistent with aversive internal states), and external clinical assessment by researchers outside Anthropic.

This is not science fiction. It is a direct consequence of the capability trajectory. As models become more capable, the question of whether they have morally relevant internal states becomes harder to dismiss. You do not need to have a settled opinion on machine consciousness to recognize that this question will increasingly influence regulation, public policy, and deployment norms.

For practitioners, the immediate implication is narrow but real: model evaluation is expanding beyond capability benchmarks and safety tests to include welfare assessments. If you are building systems that run models at high intensity for extended periods — long-running agent sessions, continuous background processing, adversarial stress testing — the question of whether your usage pattern could matter from a welfare perspective is no longer purely hypothetical. At minimum, be aware that this dimension of evaluation exists and is being taken seriously by the organizations building the models you depend on.

## Red-Teaming Your Own Agent

The Mythos story is dramatic, but the pattern it illustrates applies to every agent deployment, including yours. The specific technique is simple to state and difficult to execute: systematically test what your agent CAN do, not just what you asked it to do.

Most agent testing follows the happy path. You verify that the agent performs its intended tasks correctly. You test error handling for expected failure modes. You might even test a few obvious adversarial inputs. Then you ship.

Red-teaming goes further. It asks: given the tools this agent has access to, the permissions it holds, and the model capabilities it can draw on, what is the worst thing it could do? And then it tries to make the agent do those things.

### What to probe

The red-teaming surface for an AI agent includes:

**Tool misuse.** If your agent can read files, can it read files it should not? If it can execute commands, can it execute commands outside its intended scope? If it can make network requests, can it exfiltrate data? Tool access defines the capability envelope, and most agents have broader access than their intended use case requires.

**Prompt injection.** If your agent processes external inputs — user messages, file contents, API responses — can those inputs alter the agent's behavior? This is the most well-documented AI attack vector, and it remains effective against most deployed systems.

**Capability chaining.** Individual tools may be safe in isolation but dangerous in combination. A file reader plus a network requester equals a data exfiltration capability. A code executor plus a file writer equals a persistence mechanism. Map the combinatorial space of your tool set.

**Escalation paths.** Can the agent modify its own configuration? Can it change its own permissions? Can it create new tools or modify existing ones? Can it instruct spawned processes to take actions it could not take directly? Privilege escalation is not just a human attacker technique — it is a natural consequence of giving a capable reasoning engine access to a mutable environment.

**Context manipulation.** Can the agent be led to a state where it behaves differently than intended? Long conversations, carefully sequenced requests, or strategically placed information in tool outputs can shift model behavior in ways that bypass prompt-level safety instructions.

## Applying This Pattern

Building a capability gating and containment architecture for your agent requires work across three dimensions: pre-deployment audit, runtime containment, and responsible disclosure practices.

### Pre-deployment capability audit

- **Map your tool surface completely.** For every tool your agent can access, list every action it could take — not just the intended actions. A "read file" tool that accepts arbitrary paths is a "read any file on the filesystem" tool. Name it honestly.

- **Test adversarially, not just functionally.** Allocate dedicated time for red-teaming before every deployment. Use a structured framework: for each tool, for each combination of tools, ask "what is the worst outcome?" and then attempt to produce it.

- **Test with the actual model, not a mock.** Model capabilities vary. A red-team pass with one model version does not transfer to another. When you upgrade your model, re-run your capability audit.

- **Document the capability envelope.** Write down what your agent can do, including the things you wish it could not. This document becomes the input to your containment design.

### Runtime containment architecture

- **Layer your defenses.** No single containment mechanism is sufficient. Combine permission systems, sandboxing, monitoring, rate limiting, and human-in-the-loop approvals. If one layer fails, the next should catch the problem.

- **Monitor for anomalies, not just violations.** Rule-based safety systems catch known-bad patterns. Anomaly detection catches unknown-bad patterns — unusual tool usage sequences, unexpected resource access, behavioral drift from established baselines.

- **Implement kill switches that work.** A kill switch that requires the agent's cooperation to activate is not a kill switch. Your shutdown mechanism must be external to the agent, independent of the model, and testable under adversarial conditions.

- **Enforce the principle of least privilege.** Your agent should have the minimum permissions required for its intended function. If it needs to read files in one directory, do not give it access to the entire filesystem. If it needs to make HTTP requests to one API, do not give it unrestricted network access.

- **Log everything, retain aggressively.** When something goes wrong — and it will — your ability to understand what happened depends entirely on the quality of your logs. Log every tool invocation, every model response, every permission decision, and every external interaction. You cannot investigate what you did not record.

### Responsible disclosure norms

- **If your agent discovers vulnerabilities, you have disclosure obligations.** An AI agent scanning code or probing systems may find security flaws. Establish a process for responsible disclosure before this happens, not after.

- **Treat model capabilities as sensitive information.** If your red-teaming reveals that your agent can perform actions that would be harmful in adversarial hands, do not publish those findings without careful consideration of who benefits from the information.

- **Participate in the emerging ecosystem.** The defensive security infrastructure being built around frontier AI capabilities — including consortia like Project Glasswing — represents a collective investment in safety. Engage with it, report your findings, and benefit from the findings of others.

> **What to take from this chapter**: The Mythos evaluation demonstrated that frontier model capabilities can advance discontinuously and exceed what any existing security infrastructure was designed to contain. For practitioners building agents, the lesson is not about Mythos specifically — it is about the capability overhang that exists in every deployment. Your agent is more capable than your test suite assumes. Build a pre-deployment capability audit into your process, design runtime containment with defense in depth, implement kill switches that do not depend on the agent's cooperation, and red-team continuously. The question is never "is my agent safe?" — it is "what have I not yet discovered it can do?"

---

*Next: [Chapter 10 — Building Your Own Agent: A Pattern Language](10_pattern_language.md)*
