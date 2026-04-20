# Chapter 6: The Vendor Frameworks

---

## The Platform-as-a-Service of the Agent Era

Every major AI vendor now ships an agent development framework. Not a marketing slide. Not a reference architecture. An actual SDK with primitives, documentation, and examples. Google has ADK. OpenAI has the Agents SDK. Anthropic has the Claude Agent SDK. AWS has Strands. Microsoft has Azure AI Agent Service. Each one is, in cloud terms, something close to Platform-as-a-Service: a polished, opinionated environment that makes building agents extraordinarily fast provided you stay within the vendor's walled garden.

This chapter is a tour of those five frameworks. For each, we cover its design philosophy, what it is genuinely good at, and the gravitational pull it exerts toward its parent vendor. We are intentionally not turning this into a feature-by-feature comparison table — those go out of date in weeks. What we want to give you is a stable mental model of *what kind of tool each framework is* and *what kind of bet you are making when you pick it*.

Chapter 9 handles the switching-cost question directly, so here we are describing the frameworks on their own terms rather than debating lock-in. The lock-in conversation is important, but it lives in its own chapter.

## Google ADK (Agent Development Kit)

**The pitch.** "Enterprise-grade multi-agent orchestration, built for scale."

**The design philosophy.** ADK organises an agent system as a hierarchical tree. A root agent receives the user's request and delegates to sub-agents, which may delegate further, with execution managed by structural primitives the framework calls Sequential, Parallel, and Loop agents. The agent system is a tree; the framework runs the tree.

**What it is genuinely good at.** Three things stand out in 2026.

*Visual debugging and iteration.* ADK ships with a CLI and a web UI where you can chat with your agent, watch its internal reasoning, and step through its execution. For complex multi-agent deployments, this is genuinely one of the better developer experiences in the market — equivalent to the shift from printf-debugging to a real debugger for most developers encountering it for the first time.

*Native A2A support.* As covered in Chapter 4, ADK auto-generates A2A agent cards and handles the protocol plumbing automatically. If multi-agent communication across teams or organisations is in your roadmap, ADK gives you the smoothest on-ramp.

*Multimodal capability.* ADK agents can natively process images, audio, and video through Gemini's multimodal API. This opens use cases — visual inspection, voice-based customer support, document understanding — that are awkward or impossible in text-first frameworks.

**The gravitational pull.** ADK is optimised for Gemini. It is also optimised for Vertex AI deployment, for BigQuery as the default data warehouse, and for Google Cloud as the default runtime. You can technically use ADK with non-Google models, but every friction point in the ecosystem subtly points you back to Gemini. This is not a criticism — vendor frameworks are supposed to do this. It is a statement of fact about where ADK fits best.

**Who should take ADK seriously.** Organisations already on Google Cloud, teams prioritising multi-agent architectures with cross-boundary communication, use cases that are meaningfully multimodal, or projects where the visual debugging experience accelerates development more than the framework's opinions slow it down.

## OpenAI Agents SDK

**The pitch.** "Lightweight, no-nonsense delegation."

**The design philosophy.** The OpenAI Agents SDK is explicitly anti-graph. Where LangGraph wants you to draw a state machine, the OpenAI SDK wants you to define a small number of agents, each with a clear specialty, and let them hand off to each other as needed. The mental model is a team of specialists with a receptionist who routes calls, not a flowchart. Four primitives: Agents, Tools, Handoffs, and Guardrails. That is the entire vocabulary.

**What it is genuinely good at.**

*Developer velocity.* It is fast to learn, fast to read, fast to maintain. For a team that wants an agent architecture they can fit in one file, this is the framework that most respects your time.

*Hosted tools and sandboxing.* Agents built on the OpenAI SDK can use hosted tools (web search, file search, code interpreter) that run on OpenAI's infrastructure with no setup. For agents that need to write and run code, OpenAI's managed sandbox environment is a real differentiator — you do not have to build the container infrastructure yourself.

*Voice and multimodal.* Through the Realtime API, agents built on the OpenAI SDK handle voice interactions well, and GPT-4o's multimodal capabilities are exposed cleanly through the SDK.

**The gravitational pull.** OpenAI Agents is designed for OpenAI models. You can wire it to other providers through routing libraries (LiteLLM and similar), but the hosted tools, the sandbox, and the tuning of the handoff mechanism all assume OpenAI underneath. If you use the framework and swap models, you keep the control-flow semantics but lose the managed infrastructure that made the framework attractive in the first place.

**Who should take it seriously.** Teams already committed to OpenAI models, use cases where voice or code execution matters, and organisations that want the fastest possible path from concept to running agent without a lot of architectural ceremony.

## Claude Agent SDK

**The pitch.** "The ultimate digital worker that knows how to use a computer."

**The design philosophy.** Anthropic's framework takes a different tack from the other two foundation-vendor SDKs. It is built around the assumption that the agent will need to operate in a computer-like environment — reading files, executing shell commands, writing code, searching the web. The SDK ships with eight built-in tools out of the box (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch), and the design mentality is "give the agent a computer and let it work."

The orchestration model is based on two primitives: hooks and subagents. Hooks intercept lifecycle events ("before tool call," "after model response") so you can enforce guardrails or track behaviour. Subagents delegate tasks to child agents with their own tool surfaces and instructions. Where OpenAI Agents organises work by handoffs between peers, Claude Agent SDK organises work by delegation to children.

**What it is genuinely good at.**

*Long-running, autonomous work.* Claude Agent SDK is the framework that most visibly targets tasks that take hours or days rather than seconds or minutes. Context compaction, state checkpointing, and the assumption of asynchronous execution are baked in. For tasks like "review this codebase and produce a migration plan" or "analyse the last year of tickets and propose the top five automation candidates," this is the framework that handles the long-running shape most naturally.

*Built-in tool surface.* The eight built-in tools mean Claude Agent SDK agents start with real capabilities rather than empty tool registries. For developer-assistant use cases especially, this is a meaningful head-start.

*Hooks as a control surface.* The hooks model gives precise control over agent behaviour at lifecycle points, which enterprises appreciate for compliance and observability reasons. Guardrails can be enforced centrally rather than sprinkled through tool code.

**The gravitational pull.** Claude Agent SDK leans on Claude's computer-use training. Claude has been specifically trained on how to interact with file systems, run shell commands safely, and use browsers — and the SDK is built to exploit that training. Other models do not have equivalent training, so running the same SDK through a non-Claude model produces noticeably worse results. This is a deeper coupling than ADK's Gemini preference or the OpenAI SDK's OpenAI preference. It is model-level behavioural coupling, not just ecosystem affinity.

**Who should take it seriously.** Engineering-heavy workloads (coding assistants, system-administration agents), long-running autonomous tasks, and teams that want a framework with real opinions about computer-use safety and hooks for enforcing them.

## AWS Strands

**The pitch.** "Model-centric agents wired into AWS."

**The design philosophy.** AWS Strands is the newest of the major vendor frameworks and the most explicitly experimental. Its approach leans heavily on letting the LLM drive, rather than constraining the LLM with structural primitives. Where LangGraph makes you define edges in a graph, Strands makes you define goals in natural language and relies on the model to decide how to achieve them. It is a bet that models are now capable enough to handle orchestration autonomously, and the framework's job is to provide the safe execution environment and the AWS integration, not to impose control flow.

**What it is genuinely good at.**

*AWS integration.* Strands is deeply wired into Bedrock (for model choice), Lambda (for tool execution), DynamoDB (for state), and the rest of the AWS primitives. If your infrastructure is AWS-native, Strands removes a lot of integration plumbing.

*Flexibility in model choice.* Strands uses Bedrock underneath, which means it has native access to Anthropic's Claude, Meta's Llama, Mistral, and other models. This gives it more model flexibility than the foundation-vendor frameworks, within the constraint that you are using Bedrock for model access.

*Experimental primitives.* Strands includes primitives like "AI Functions" where you describe a goal in natural language and the framework generates validation logic for the model's output — a pattern that is interesting but not yet battle-tested.

**The gravitational pull.** Strands is AWS's answer, not Anthropic's or OpenAI's. The gravitational pull is toward AWS infrastructure, not toward a single model. If you are all-in on AWS, that is a feature. If you are cloud-portable, Strands is not for you.

**Who should take it seriously.** Organisations whose infrastructure centre of gravity is AWS, teams that want Bedrock-mediated model flexibility, and projects where the AWS integration depth is a concrete advantage rather than an accidental constraint.

## Microsoft Azure AI Agent Service

**The pitch.** "The enterprise integration powerhouse."

**The design philosophy.** Microsoft's agent story has had several phases. AutoGen, the company's open-source multi-agent framework, pioneered much of the conversation-between-agents pattern. Those ideas have been absorbed into Azure AI Agent Service, which is Microsoft's production-oriented offering. The framework emphasises integration with the Microsoft enterprise ecosystem: agents that can trigger from Azure events, read SharePoint documents, post to Teams channels, and coordinate with Microsoft 365 copilots.

**What it is genuinely good at.**

*Enterprise integration breadth.* For organisations running on Microsoft 365, Dynamics, SharePoint, Power Platform, and the rest of the Microsoft enterprise stack, Azure AI Agent Service offers integration depth no other framework can match. Agents can read, write, and react to events across the entire Microsoft surface with minimal glue code.

*Identity and compliance posture.* Microsoft has decades of enterprise compliance infrastructure, and Azure AI Agent Service inherits it. SSO, conditional access, audit trails, data residency, sovereign cloud support — all of the enterprise scaffolding is there from day one. For regulated enterprises, this matters.

*Absorbed AutoGen patterns.* The multi-agent conversation patterns pioneered in AutoGen (debate, consensus, hierarchical coordination) have been carried forward into the managed service, giving organisations a well-trodden path from "multi-agent research prototype" to "managed enterprise deployment."

**The gravitational pull.** Azure AI Agent Service is built for the Microsoft ecosystem. The default model is OpenAI through Microsoft's partnership, the default runtime is Azure, and the default integrations are Microsoft 365 and related products. If you live in that world, the framework accelerates you. If you do not, you are paying for integrations you cannot use.

**Who should take it seriously.** Microsoft-shop organisations, regulated enterprises valuing Microsoft's compliance posture, and teams building agents that heavily interact with Microsoft 365 data and workflows.

## How to Read This Chapter

It is tempting, after a tour like this, to draw up a comparison matrix and tick boxes. We have deliberately avoided that, because the most important dimensions of framework choice are not in any matrix. They are: which ecosystem does your organisation already live in; which model provider do you trust for the next eighteen months; how much does agent-to-agent interoperability matter to your roadmap; how much orchestration do you actually need before you start; how much lock-in can you tolerate.

A genuine summary of the vendor-framework landscape in one sentence per vendor:

| Framework | The Pitch in One Line |
|---|---|
| Google ADK | Best-in-class multi-agent + A2A, best debugging, deep Gemini/GCP pull |
| OpenAI Agents SDK | Fastest path from zero to running agent, OpenAI ecosystem, handoffs model |
| Claude Agent SDK | Strongest computer-use and long-running task story, deepest model coupling |
| AWS Strands | AWS-native, Bedrock-mediated model flexibility, most experimental primitives |
| Azure AI Agent Service | Deepest Microsoft 365 integration, strongest enterprise compliance posture |

Each is a reasonable choice for the organisation it was built for. None is a reasonable choice for every organisation.

> **What to take from this chapter:** The vendor frameworks are the PaaS of the agent era — opinionated, fast, and deeply aligned with the vendor that built them. Each one has a genuine strength: multi-agent for ADK, velocity for OpenAI, computer use for Claude, AWS integration for Strands, Microsoft-ecosystem integration for Azure. The right choice depends on which ecosystem you already live in and how much portability you are willing to trade for speed. Chapter 9 handles the lock-in consequences of each; this chapter established what they are on their own terms.

---

*Next: [Chapter 7 — The Agnostic Frameworks](07_agnostic_frameworks.md)*
