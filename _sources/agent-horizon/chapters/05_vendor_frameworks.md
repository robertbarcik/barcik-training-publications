# Chapter 5: The Vendor Frameworks

---

Every major AI vendor now ships an agent development framework. Google has ADK. OpenAI has the Agents SDK. Anthropic has the Claude Agent SDK. AWS has Strands. Microsoft has the Azure AI Foundry Agent Service. In cloud terms, each is something close to Platform-as-a-Service: an opinionated environment that makes building agents extraordinarily fast provided you stay within the vendor's walled garden.

This chapter is a tour. For each framework: the design philosophy, what it's genuinely good at, and the gravitational pull it exerts toward its parent vendor. Feature-by-feature comparisons go out of date in weeks. What's stable is *what kind of tool each framework is* and *what kind of bet you're making when you pick it*. Chapter 8 handles the switching-cost question directly; here the frameworks get described on their own terms.

## Google ADK

Hierarchical agent trees. A root agent receives the user's request and delegates to sub-agents, which may delegate further. Execution is managed by structural primitives ADK calls Sequential, Parallel, and Loop agents. The agent system is a tree; the framework runs the tree.

Three genuine strengths. **Visual debugging**: ADK ships with a CLI and a web UI where you chat with your agent, watch its internal reasoning, and step through execution. For complex multi-agent deployments, one of the better developer experiences in the market. **Native A2A support**: ADK auto-generates agent cards and handles the protocol plumbing. If cross-boundary multi-agent work is on your roadmap, ADK gives you the smoothest on-ramp. **Multimodal capability**: ADK agents natively process images, audio, and video through Gemini's multimodal API, opening visual inspection, voice-based customer support, and document-understanding use cases.

Gravitational pull: Gemini, Vertex AI, BigQuery, Google Cloud. Technically model-agnostic, but every friction point in the ecosystem quietly points back to Gemini. This isn't a criticism; vendor frameworks are supposed to do this.

**Take ADK seriously if** you're already on Google Cloud, prioritise multi-agent with cross-boundary communication, have meaningfully multimodal use cases, or find the visual debugging accelerates you more than the framework's opinions slow you down.

## OpenAI Agents SDK

Explicitly anti-graph. Where LangGraph wants you to draw a state machine, OpenAI wants you to define a small number of agents, each with a clear specialty, and let them hand off to each other as needed. Mental model: a team of specialists with a receptionist who routes calls, not a flowchart. Four primitives: Agents, Tools, Handoffs, Guardrails. That's the whole vocabulary.

Strengths. **Developer velocity**: fast to learn, fast to read, fast to maintain. For a team that wants an agent architecture they can fit in one file, the framework that most respects your time. **Hosted tools and sandboxing**: web search, file search, code interpreter run on OpenAI's infrastructure with no setup. For agents that need to write and run code, the managed sandbox is a real differentiator. **Voice and multimodal**: the Realtime API is first-class, GPT-4o's multimodality exposed cleanly.

Gravitational pull: OpenAI models, hosted infrastructure, structured-output reliability tuned for OpenAI. Swap models via routing libraries and you keep the control-flow semantics but lose most of the managed infrastructure that made the framework attractive.

**Take it seriously if** you're committed to OpenAI models, voice or code execution matters, and you want the fastest possible path from concept to running agent without architectural ceremony.

## Claude Agent SDK

Different tack. Built around the assumption that the agent will operate in a computer-like environment, reading files, running shell commands, writing code, searching the web. Ships with eight built-in tools out of the box (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch). Design mentality: give the agent a computer and let it work.

Orchestration model: **hooks and subagents**. Hooks intercept lifecycle events ("before tool call," "after model response") so you can enforce guardrails or track behaviour. Subagents delegate tasks to child agents with their own tool surfaces and instructions. Where OpenAI organises work by handoffs between peers, Claude organises by delegation to children.

Strengths. **Long-running autonomous work**: tasks that take hours or days rather than seconds. Context compaction, state checkpointing, asynchronous execution are baked in. For "review this codebase and produce a migration plan" or "analyse the last year of tickets and propose top five automation candidates," the framework that handles the long-running shape most naturally. **Built-in tool surface**: eight tools means agents start with real capabilities rather than empty registries. Meaningful head-start for developer-assistant use cases. **Hooks as control surface**: precise control over agent behaviour at lifecycle points, which enterprises appreciate for compliance and observability reasons. A newer addition, Agent Skills (folders of instructions, scripts, and resources the agent loads on demand), shipped as an open standard in early 2026 and gives the SDK a portable packaging story for procedural knowledge.

Gravitational pull: this is the deepest coupling in the vendor-framework category. Claude has been specifically trained on computer-use tasks (file systems, shell commands, browsers). Other models have no equivalent training. Running the same SDK through a non-Claude model produces noticeably worse results. This is model-level behavioural coupling, not just ecosystem affinity.

**Take it seriously if** you're building engineering-heavy workloads (coding assistants, system-administration agents), long-running autonomous tasks, and want a framework with real opinions about computer-use safety.

## AWS Strands

The youngest of the five, though no longer the experiment it launched as: Strands is now the production SDK at the centre of Amazon Bedrock AgentCore, AWS's managed agent runtime, while the frontier work has moved to a separate Strands Labs organisation. The design bet is unchanged. Lean heavily on letting the LLM drive rather than constraining it. Where LangGraph makes you define edges in a graph, Strands makes you define goals in natural language and relies on the model to decide how to achieve them. A bet that models are now capable enough to handle orchestration autonomously, and the framework's job is to provide safe execution + AWS integration, not to impose control flow.

Strengths. **AWS integration**: deep wiring into Bedrock (models), Lambda (tools), DynamoDB (state). If your infra is AWS-native, Strands removes a lot of plumbing. **Flexibility within Bedrock**: native access to Claude, Llama, Mistral, and others; more model flexibility than the foundation-vendor frameworks *within the constraint that you're using Bedrock for model access*. **A managed runtime**: AgentCore wraps Strands agents in managed sessions, memory, identity, and observability, so the gap between prototype and production is unusually short. The experimental primitives ("AI Functions" and their kin) now live in Strands Labs, clearly fenced off from the production SDK.

Gravitational pull: AWS infrastructure, not a single model. Inverted lock-in from the foundation-vendor frameworks.

**Take it seriously if** your infrastructure centre of gravity is AWS and Bedrock-mediated model flexibility is concretely useful.

## Microsoft Azure AI Foundry Agent Service

Microsoft's agent story has two layers. The open-source layer is the Microsoft Agent Framework, the unification of AutoGen's multi-agent research patterns with Semantic Kernel's enterprise plumbing (it reached 1.0 in April 2026). The managed layer is the Azure AI Foundry Agent Service, which runs those patterns in production and emphasises integration with the Microsoft enterprise ecosystem: agents that trigger from Azure events, read SharePoint, post to Teams, coordinate with Microsoft 365 copilots.

Strengths. **Integration breadth**: for organisations on Microsoft 365, Dynamics, SharePoint, Power Platform, depth no other framework matches. **Identity and compliance posture**: decades of Microsoft enterprise compliance infrastructure inherited natively. SSO, conditional access, audit trails, data residency, sovereign cloud support all there from day one. **Absorbed AutoGen patterns**: multi-agent conversation patterns (debate, consensus, hierarchical coordination) carried forward from Microsoft's open-source research into the Agent Framework and the managed service on top of it.

Gravitational pull: Microsoft ecosystem. Default model is OpenAI through the partnership, default runtime is Azure, default integrations are Microsoft 365. Live in that world and the framework accelerates you; don't and you're paying for integrations you can't use.

**Take it seriously if** you're a Microsoft-shop organisation, need the compliance posture, or are building agents that heavily interact with Microsoft 365 data and workflows.

## Summary

| Framework | The Pitch in One Line |
|---|---|
| Google ADK | Best-in-class multi-agent + A2A, best debugging, deep Gemini/GCP pull |
| OpenAI Agents SDK | Fastest path from zero to running agent, OpenAI ecosystem, handoffs model |
| Claude Agent SDK | Strongest computer-use and long-running task story, deepest model coupling |
| AWS Strands | AWS-native, Bedrock-mediated model flexibility, AgentCore managed runtime |
| Azure AI Foundry Agent Service | Deepest Microsoft 365 integration, strongest enterprise compliance posture |

Each is a reasonable choice for the organisation it was built for. None is a reasonable choice for every organisation.

> **What to take from this chapter:** Vendor frameworks are the PaaS of the agent era: opinionated, fast, and deeply aligned with the vendor that built them. Each has a genuine strength and a specific gravitational pull. The right choice depends on which ecosystem you already live in and how much portability you'll trade for speed. Chapter 8 handles lock-in consequences per vendor; this chapter established what each framework is on its own terms.

---

*Next: [Chapter 6: The Agnostic Frameworks](06_agnostic_frameworks.md)*
