# Chapter 3: The Protocol Layer: MCP and A2A

---

Two protocols sit at the access layer of the agent stack. MCP handles agent-to-tool and agent-to-data traffic. A2A handles agent-to-agent. They're peer standards, and almost every enterprise architecture conversation about agents eventually comes back to one or both.

MCP is settled. A2A is close behind, still firming up at the edges. This chapter covers both.

## MCP: The HTTP of the Agent Era

Most technology standards spend years in a messy middle period where competing protocols fight for adoption. MCP had an unusually short one. Announced by Anthropic in late 2024, it went from "interesting open-source proposal" to "effective industry default" in about eighteen months.

By early 2026 the numbers are hard to argue with: more than 97 million SDK downloads per month across the Python and TypeScript implementations, more than 10,000 publicly indexed MCP servers, native support in Claude, ChatGPT, Cursor, every major IDE that ships an AI feature, and every framework covered in this booklet. In December 2025, Anthropic donated MCP to the Linux Foundation, which formed the Agentic AI Foundation to govern it, co-founded by Anthropic, Block, and OpenAI, with additional backing from Google, Microsoft, AWS, Cloudflare, and Bloomberg. That's not the roster of a contested standard. That's the roster of a settled one.

The comparison everyone reaches for is HTTP. It's a good comparison. HTTP is also not something you "choose"; it's the ambient protocol that lets any browser reach any server. MCP is becoming that for agents: the ambient protocol that lets any agent reach any tool or data source. Increasingly, *not* supporting it is more expensive than supporting it.

### What MCP Actually Standardises

Three things, not one. Enterprises that treat it as a simple API gateway miss most of the value.

**Tools**: executable functions the agent can invoke. A tool has a name, a short description, an input schema with field-level descriptions, and structured error responses. The agent calls `tools/list` to see the catalog, then `tools/call` to invoke a specific tool with arguments. The important design choice is that tool descriptions are written for a language model to reason about, not for a human reading docs. A well-designed MCP server is closer to a prompt-engineered API than to a conventional REST endpoint; the linguistic quality of tool descriptions is part of the server's correctness.

**Resources**: read-only data the server makes available. Documents, database rows, configuration files, policy knowledge. The agent doesn't "call" a resource; it fetches it and places the content into its own context. For enterprise deployments, resources often matter more than tools. An internal policy bot wants a resource tree (`policies/hr/parental-leave.md`, `policies/security/acceptable-use.md`) the agent can browse and pull from, not a tool called `get_policy_document(id)` it has to guess how to invoke.

**Prompts**: reusable prompt templates the server offers to clients. The least-used of the three, but the reason it exists is principled: tools are things to do, resources are things to read, prompts are things to say. A complete MCP server can offer all three.

### The Handshake

MCP is a client-server protocol over a small JSON-RPC vocabulary. Initial connection does one round of negotiation (`initialize`): protocol version, capabilities, identity. After that, it's just method calls: `tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list`, `prompts/get`. The vocabulary is small on purpose. Most of the interesting design work happens inside the server (how you model your domain, how you write your tool descriptions, how you design your resource tree), not in the protocol itself.

### What MCP Looks Like in an Enterprise

The shape is almost always the same. A handful of internal MCP servers sit in front of existing systems: the CRM, the ticketing platform, the data warehouse, the internal knowledge base, the identity system. Each server is maintained by the team that owns the underlying system, because that team understands the domain semantics best. Any number of agents (built on any framework, using any model) connect as MCP clients.

This gives three enterprise-grade properties that explain most of the adoption curve. One: re-use across agents (one server, many consumers, dramatically better than the pre-MCP world where every agent integrated every backend separately). Two: re-use across frameworks (switch from LangGraph to ADK next year and the servers don't need to change). Three: foundation governance (no single commercial interest can break compatibility or shift licensing).

### The 2026 Roadmap: Enterprise Readiness

The Agentic AI Foundation's 2026 roadmap lists four priority areas, and the first is explicitly enterprise readiness. Concretely: **identity and access integration** (OAuth 2.1, enterprise SSO, scoped tokens), **management and observability** (gateway behaviour, audit trails, admin consoles), and **transport and configuration portability** (streaming, cancellation, resilience under enterprise network conditions).

The subtext is that MCP is consciously being reshaped from a developer protocol into an enterprise protocol. It's the same transition HTTP went through from 1993 to 1999, compressed into about a year.

### What MCP Does Not Do

MCP is deliberately dumb about a lot of things. It doesn't orchestrate; it doesn't know which tool to call, in what order, or what to do on failure. That's the orchestration layer's job. It doesn't authenticate end users on its own; the auth model is an enterprise deployment decision. It doesn't handle agent-to-agent communication; that's A2A, below. And it doesn't replace your existing APIs; it sits in front of them.

One prediction worth making explicit: in eighteen months, if you have a non-trivial internal platform, you'll almost certainly have MCP servers in front of it, written by your own team, maintained as part of normal platform engineering work. External vendors will ship MCP servers for their own products (GitHub, Linear, Notion already do), but your internal systems are yours to wrap. The enterprise-grade art of writing good MCP servers (tight tool surfaces, precise descriptions, strong auth, clean resource hierarchies) is an emerging platform-engineering craft that didn't exist two years ago. If you want to build that intuition hands-on, there is a free companion: [github.com/robertbarcik/MCP-tutorial](https://github.com/robertbarcik/MCP-tutorial) works through this chapter's concepts in code.

> **July 2026 note.** The enterprise-readiness roadmap above is arriving on schedule. The spec revision landing July 28 (already published as a release candidate) is MCP's largest since launch: a stateless core that scales on plain HTTP, hardened OAuth and OIDC alignment for enterprise identity providers, and two official extensions, MCP Apps for server-rendered UI and Tasks for long-running work. Nothing in this section changes as a result; the protocol is doing what settled protocols do, which is boring plumbing work.

## A2A: The Other Protocol

If MCP answers "how does my agent talk to a tool," A2A answers "how does my agent talk to another agent." These are the two traffic directions at the access layer, and they deserve symmetric attention. Most enterprise projects focus on tools and data first because that's where the immediate wins live. Agent-to-agent sounds like a future problem until, around the twelfth agent an organisation builds, it stops being a future problem and becomes urgent.

### Why It Becomes Urgent Faster Than Teams Expect

Specialisation: a general-purpose support agent hits its limits, and the team carves out a billing specialist, a technical specialist, a compliance specialist. Organisational boundaries: sales builds a sales agent, HR builds an HR agent, finance builds a finance agent, and when a sales rep asks about commission policy the three have to cooperate. External counterparts: a vendor's agent negotiates with your procurement agent, and the only viable way for them to cooperate is an open protocol. Composition: the microservices pattern is replaying at the agent level, and systems of agents need a protocol.

### What A2A Does

Three things. **Capability discovery**: an A2A-compatible agent advertises an "agent card" describing what it can do, what inputs it expects, what outputs it produces, how to authenticate. **Task delegation**: a structured way to hand off a task, supporting both synchronous request-response and longer-running asynchronous interactions with streaming progress. **Authentication and trust**: hooks for carrying authentication context across the delegation, so downstream agents can make their own authorisation decisions rather than trusting upstream blindly. The third point is the one enterprises underweight. Cross-agent calls can cross organisational or even company boundaries, and whose authority is being exercised at each hop becomes an interesting question.

### Where A2A Sits in the Landscape

Messier than MCP's. **Google ADK has native A2A support** and auto-generates agent cards, one of the strongest reasons to take ADK seriously for multi-agent architectures. **CrewAI also supports A2A**, reflecting its multi-agent-first design. **LangGraph, OpenAI Agents SDK, Claude Agent SDK** have partial or emerging support; all three have published roadmap items.

The would-be rivals have mostly folded in. IBM's Agent Communication Protocol merged into A2A in September 2025, and Google donated A2A to the Linux Foundation, where it now sits under the same Agentic AI Foundation umbrella as MCP. At its one-year mark in April 2026 the protocol counted over 150 member organisations, production use at Microsoft, AWS, Salesforce, SAP, and ServiceNow, and a 1.2 release with cryptographically signed agent cards. A payments layer is already forming on top of it: the Agent Payments Protocol (AP2), backed by Google, Coinbase, Mastercard, and PayPal, standardises how agents transact money, with cryptographic mandates proving a human authorised the purchase.

Our read in April 2026: A2A is the leading contender but not yet the slam-dunk consensus MCP is. The sensible bet for most enterprises is to design with A2A in mind, treat cross-agent protocols as an area where some rework may be needed in 2027, and avoid building a proprietary in-house variant.

### What to Do About A2A Today

Most enterprises should **not** over-invest in A2A infrastructure yet. If you're building your first agent, focus on MCP, focus on the orchestration layer, and treat A2A as something you'll adopt when it becomes relevant. Premature A2A usually means designing a multi-agent system before the business has a use case for one.

**Do not rule out A2A by accident.** When you pick a framework, check its A2A story. A framework with no credible A2A roadmap is a quiet bet that multi-agent architecture won't matter for your use case. Defensible for a single-purpose agent; risky for a platform.

**Start writing agent cards.** Even without formal A2A, the habit of documenting, for every agent you build, what it does, what it needs, what it returns is useful discipline. That discipline is cheap to formalise later.

> **What to take from this chapter:** MCP is the settled protocol for agent-to-tool and agent-to-data access. A2A is the emerging protocol for agent-to-agent, less settled but gaining consensus. Both live at the access layer of the stack, underneath the orchestration layer. Treat MCP as ambient infrastructure: consume the vendor servers, build your own for internal systems. Treat A2A as an architectural concern you'll act on when multi-agent needs become real, but pick frameworks with a credible A2A roadmap even if you're single-agent today.

---

*Next: [Chapter 4: The Orchestration Layer](04_orchestration_layer.md)*
