# Chapter 2: The Layer Cake

---

## The Most Common Mistake

If you read technology press about agent development, you'll run into sentences like "should you use ADK or MCP?" or "companies are choosing between the Claude Agent SDK and the Model Context Protocol." These sentences are nonsense. They treat a protocol and a framework as competing options, which they are not. They live on different layers of the stack and do different jobs.

This isn't a pedantic complaint. It's the single most load-bearing clarification in the booklet. If you leave this chapter with one thing, let it be this: the agent stack has layers, and the pieces you hear debated in the press are not always on the same one. Framework decisions happen at one layer, protocol decisions at another, model decisions at a third. You don't "choose between" items from different layers. You choose one of each and combine them.

The cloud-era equivalent would be asking "should we use AWS or HTTP?" AWS is a cloud provider; HTTP is a protocol. You use both. They aren't competing decisions; they're complementary decisions at different levels of the stack.

## The Layers

Read this picture top-down, from what the user experiences to what actually does the work.

```
┌─────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER                                │
│  "When do we call what, with what state,            │
│   under what guardrails, across how many agents?"   │
│                                                     │
│  ADK · LangGraph · CrewAI · OpenAI Agents SDK ·     │
│  Claude Agent SDK · AWS Strands · Azure AI Foundry  │
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

Four layers. Each has a distinct role. You pick something from each layer, then compose them.

**Orchestration layer.** The agent's "brain." Deciding which tool to call, in what order, what to do on failure, how to pass state step to step, when to stop. In a simple agent this might be a `while` loop that keeps calling the model until it says "done." In a complex agent it's a multi-step state machine with branches, retries, parallel execution, and handoffs to sub-agents. Google ADK, LangGraph, CrewAI, OpenAI Agents SDK, Claude Agent SDK, AWS Strands, Azure AI Foundry Agent Service. All live here. They disagree about whether the right abstraction is a graph, a team of agents with roles, a sequence of handoffs, or a tree of sub-agents. They're all solving the same fundamental problem.

**LLM layer.** The model that does the thinking. Gemini, Claude, GPT, Mistral, Llama. Framework decides *when* to call the model and *what to do* with the result; model decides *what to say* when called. Framework is the project manager; model is the specialist being asked for an opinion.

**Tool and agent access layer.** How the agent reaches tools, data, and other agents. Two protocols matter: **MCP** for tools and data (how does my agent talk to a database or API), **A2A** for agent-to-agent (how does my agent talk to someone else's agent). Both live at this layer. Chapter 3 covers them together.

**Actual systems.** Databases, APIs, SaaS apps, internal tools. The layer you already know. Agents don't replace it; they plug into it.

## Why "ADK vs MCP" Is a Category Error

With the layers in front of you, the question dissolves.

ADK lives at the orchestration layer. It decides what an agent does. MCP lives at the access layer. It defines how an agent (built with ADK or anything else) reaches a tool. An ADK agent can be an MCP client: when ADK wants to call a tool and that tool happens to be exposed as an MCP server, ADK uses MCP to make the call. When the same tool is a plain Python function, ADK calls the function directly. MCP is one of several ways ADK reaches tools, not a competitor to ADK.

Conversely, MCP doesn't care which framework is on the other end. An MCP server your data team ships doesn't know whether the agent talking to it was built with ADK, LangGraph, CrewAI, or a plain Python loop. It just sees a client speaking MCP.

The same logic applies to every apparent "framework vs protocol" debate: *Claude Agent SDK vs MCP*, *LangGraph vs A2A*, *OpenAI Agents SDK vs MCP*. All three are category errors. The framework does orchestration; the protocol does access. They compose.

> **The corrected mental model in one sentence:** Frameworks sit at the orchestration layer and decide what an agent does; protocols sit at the access layer and decide how the agent reaches the outside world. They compose. They do not compete.

A useful discipline: when you read about a new agent technology, ask *what layer does this sit on?* before you form an opinion. If you can't answer, you don't understand it well enough yet. Most of the apparent complexity of the agent landscape evaporates once you can slot each piece into the layer it belongs on.

> **What to take from this chapter:** The agent stack has four layers: orchestration, LLM, access (MCP + A2A), actual systems. Frameworks, models, and protocols are compositional, not competitive. The single most common mistake in agent-development discourse is treating a framework (ADK, LangGraph) as if it were competing with a protocol (MCP). It isn't. Everything in this booklet is an elaboration of that picture.

---

*Next: [Chapter 3: The Protocol Layer](03_protocol_layer.md)*
