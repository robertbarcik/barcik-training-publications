# Chapter 2: The Layer Cake

---

## The Most Common Mistake

If you read technology press about agent development, you will quickly run into sentences like "should you use ADK or MCP?" or "companies are choosing between Claude Agent SDK and the Model Context Protocol." These sentences are nonsense. They treat a protocol and a framework as if they were competing options, which they are not. They sit at different layers of the stack and do different jobs.

This is not a pedantic complaint. It is the single most load-bearing clarification in the entire booklet. If you leave this chapter with one thing, let it be this: the agent stack has layers, and the pieces you hear debated in the press are not always on the same layer. Framework decisions happen at one layer; protocol decisions happen at another; model decisions happen at a third. You do not "choose between" items from different layers. You choose one item from each layer, and you combine them.

Compare this to cloud. Asking "should we use AWS or HTTP?" is a meaningless question. AWS is a cloud provider; HTTP is a protocol. You use both. You might use AWS for compute and HTTP to carry the traffic in and out. Those are not competing decisions — they are complementary decisions at different levels of the stack. The same is true for agents.

## The Layers

Here is the picture we will come back to throughout the booklet. Read it top-down, from what the user experiences to what is actually executing the work.

```
┌─────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER                                │
│  "When do we call what, with what state,            │
│   under what guardrails, across how many agents?"   │
│                                                     │
│  ADK · LangGraph · CrewAI · OpenAI Agents SDK ·     │
│  Claude Agent SDK · AWS Strands · Azure AI Agent    │
├─────────────────────────────────────────────────────┤
│  LLM LAYER                                          │
│  The reasoning engine that generates tool calls,    │
│  plans, and responses.                              │
│                                                     │
│  Gemini · Claude · GPT · Mistral · Llama · ...      │
├─────────────────────────────────────────────────────┤
│  TOOL/AGENT ACCESS LAYER                            │
│  How the LLM reaches tools, data, and other agents. │
│                                                     │
│  MCP (tools & data) · A2A (agent-to-agent) ·        │
│  Native function calling · Direct SDK calls         │
├─────────────────────────────────────────────────────┤
│  ACTUAL SYSTEMS                                     │
│  Databases, APIs, files, SaaS apps, other agents    │
└─────────────────────────────────────────────────────┘
```

Four layers. Each plays a distinct role. Each has its own technology choices. And — crucially — you choose something from each layer, then compose them.

### The orchestration layer

The orchestration layer is where the agent's "brain" lives. This is the control flow: deciding which tool to call, in what order, what to do if a tool fails, how to pass state from one step to the next, when to stop. In a simple agent, this might be a single loop that keeps calling the model until the model signals it is done. In a complex agent, this might be a multi-step state machine with branches, retries, parallel execution, and handoffs to sub-agents.

The orchestration layer is where most of the frameworks live. Google ADK, LangGraph, CrewAI, the OpenAI Agents SDK, the Claude Agent SDK, AWS Strands, Azure AI Agent Service — all of them are essentially different opinions about how to structure the orchestration of an agent. They disagree about whether the best abstraction is a state graph, a team of agents with roles, a sequence of handoffs, or a tree of sub-agents. They disagree about how much memory the framework should manage versus how much the developer should manage. They disagree about how observability should work. But they are all solving the same fundamental problem, and they all sit at this one layer.

### The LLM layer

The LLM layer is what it sounds like: the model that actually does the thinking. Gemini, Claude, GPT, Mistral, Llama — these are the engines. They take prompts and context as input; they emit tool calls, plans, and responses as output. An agent without a model is an empty shell. A model without an agent is a useful completion API but not yet an autonomous system.

The important thing about this layer is that it is *underneath* the orchestration layer. The framework decides *when* to call the model and *what to do* with the result. The model decides *what to say* when called. A good mental model is that the framework is the project manager; the model is the specialist being asked for an opinion.

### The tool and agent access layer

This is the layer the industry has been quietly standardising on throughout 2025 and 2026. It answers two questions. First: how does the agent reach tools and data that live outside the model? Second: how does the agent reach other agents?

For tools and data, the increasingly dominant answer is MCP — the Model Context Protocol. MCP is an open standard for how an agent discovers what tools are available, how it invokes them, how it fetches read-only data resources, and how it handles authentication and errors. Before MCP, every vendor had its own proprietary tool-calling format and every integration was custom. After MCP, the same tool server can be reused across Claude, ChatGPT, Cursor, Claude Desktop, and any custom agent built on any of the major frameworks. Chapter 3 goes deep on this.

For agent-to-agent communication, an analogous but separate protocol is emerging: A2A (Agent-to-Agent). If MCP is about "how does my agent talk to a database or an API," A2A is about "how does my agent talk to someone else's agent." Chapter 4 covers this.

The important thing about this layer — and the source of most of the confusion — is that it is *beneath* the orchestration layer. The framework decides to call a tool; the protocol is how the call gets made. The framework delegates to another agent; the protocol is how the delegation happens. Protocols do not orchestrate. They carry messages. This distinction matters because it is the crux of the "ADK vs MCP" category error.

### The actual systems

The bottom layer is where the real work happens. The agent calls a tool, and the tool does something: queries a database, sends an email, writes a file, posts to a Slack channel, invokes an ERP function, triggers a machine-learning pipeline. These are the systems that existed before any of this started and will continue to exist regardless of which framework wins.

For an enterprise, this is the layer you already know. You already have databases, APIs, SaaS apps, internal systems. The agent stack does not replace them — it plugs into them.

## Why "ADK vs MCP" Is a Category Error

With the layer cake in front of you, the "ADK vs MCP" question dissolves.

ADK is a framework. It lives at the orchestration layer. It decides the control flow of an agent: what to call, when, in what order, with what state.

MCP is a protocol. It lives at the tool access layer. It defines how an agent (built with ADK or anything else) reaches a tool.

An ADK agent can be an MCP client. When ADK wants to call a tool, and that tool happens to be exposed as an MCP server, ADK uses the MCP protocol to do the call. When the same tool is exposed as a plain Python function in the same codebase, ADK just calls the function directly. MCP is one of several ways ADK can reach tools — not a competitor to ADK.

Conversely, MCP does not care which framework is on the other end of the connection. An MCP server built by your enterprise data team does not know whether the agent talking to it was built with ADK, LangGraph, CrewAI, the OpenAI Agents SDK, or a plain Python loop. It just sees a client that speaks MCP.

The same logic applies to every apparent "framework vs protocol" debate:

- *Claude Agent SDK vs MCP*? Same category error. Claude Agent SDK is a framework; it can (and often does) use MCP as one of its tool-access methods.
- *LangGraph vs A2A*? Same category error. LangGraph is a framework; A2A is how its agents can talk to agents built with other frameworks.
- *OpenAI Agents SDK vs MCP*? Same category error. The OpenAI SDK can act as an MCP client.

> **The corrected mental model in one sentence:** Frameworks sit at the orchestration layer and decide what an agent does; protocols sit at the access layer and decide how the agent reaches the outside world. They compose. They do not compete.

## A Preview of the Two Protocols

Two protocols matter enough to get their own chapters, so we only gesture at them here.

**MCP (Model Context Protocol)** is the standard for agent-to-tool and agent-to-data access. Think of it as the HTTP of the agent stack. It is an open protocol, donated to the Linux Foundation's Agentic AI Foundation in late 2025, and as of early 2026 it sits at roughly 97 million monthly SDK downloads and more than 10,000 public server deployments. Every major framework supports it. Every major model vendor supports it. If your agent needs to reach an external tool in 2026, there is a strong default answer, and that answer is MCP.

**A2A (Agent-to-Agent)** is the emerging standard for agent-to-agent communication. If two agents — possibly built by different teams, on different frameworks, at different companies — need to cooperate, A2A is how they discover each other's capabilities and exchange tasks. A2A is younger than MCP and less universally adopted. Google ADK has native A2A support; most other frameworks are catching up. We return to this in Chapter 4.

These two protocols are genuinely important. They are also genuinely separate from the framework debate. You choose a framework at the orchestration layer; you adopt these protocols at the access layer; you combine them.

## What to Take From This Chapter

The layer cake is the scaffolding for everything that follows. Whenever you find yourself confused by a new agent announcement — *is this a framework? a protocol? a model? a platform?* — go back to the layers and ask which one the announcement fits into. Most of the apparent complexity of the agent landscape evaporates once you know what layer each piece belongs to.

A useful test: if you cannot answer the question *"what layer does this sit on?"* for a new technology you have just read about, you do not yet understand it well enough to have an opinion.

> **What to take from this chapter:** The agent stack has four layers — orchestration, LLM, tool/agent access, and actual systems. Frameworks live at the orchestration layer. Models live at the LLM layer. Protocols (MCP, A2A) live at the access layer. These are compositional, not competitive. The single most common mistake in agent-development discourse is treating a framework (ADK, LangGraph) as if it were competing with a protocol (MCP). It is not. You pick one of each, and you combine them. Everything in this booklet is an elaboration of that picture.

---

*Next: [Chapter 3 — MCP: The HTTP of the Agent Era](03_mcp_http_of_agents.md)*
