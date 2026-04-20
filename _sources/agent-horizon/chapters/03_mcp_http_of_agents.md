# Chapter 3: MCP — The HTTP of the Agent Era

---

## The Protocol That Stopped Being Debated

Most technology standards spend years in a messy middle period where a handful of competing protocols fight for adoption, enterprises hedge their bets, and nobody wants to commit until a clear winner emerges. The Model Context Protocol has had an unusually short middle period. Announced by Anthropic in late 2024, MCP went from "interesting open-source proposal" to "effective industry default" in roughly eighteen months — a faster standardisation curve than any enterprise-relevant protocol in recent memory.

By early 2026, the numbers were hard to argue with. More than 97 million SDK downloads per month across the Python and TypeScript implementations. More than 10,000 publicly indexed MCP servers. Native support in Claude, ChatGPT, Cursor, every major IDE that ships an AI feature, and every framework covered in this booklet. In November 2025, Anthropic donated MCP to the Linux Foundation, which announced the formation of the Agentic AI Foundation (AAIF) to govern it — with co-founding support from Block and OpenAI, and additional backing from Google, Microsoft, AWS, Cloudflare, and Bloomberg. That is not the roster of a contested standard. That is the roster of a settled one.

The comparison everyone reaches for is HTTP. It is a good comparison. HTTP is also not something you "choose" — it is the ambient protocol that lets any browser reach any server. MCP is becoming that for agents: the ambient protocol that lets any agent reach any tool or data source. And just like HTTP, MCP's ubiquity means that, increasingly, *not* supporting it is more expensive than supporting it.

> **The MCP situation in one sentence:** MCP is the protocol standard at the tool-access layer of the agent stack. It is governed by the Linux Foundation, supported by every major model vendor and every major framework, and it is the default assumption in enterprise agent architecture as of 2026.

## What MCP Actually Standardises

The first misconception to clear up is that MCP is "just a wrapper for APIs." That is *almost* right, but it undersells the protocol by a wide margin. MCP standardises three distinct things — not one — and enterprises that treat it as a simple API gateway miss most of its value.

### Tools

This is the part most people already understand. A tool, in MCP terms, is an executable function the agent can invoke: "query the customer database," "send an email," "create a Jira ticket," "run this SQL statement." The MCP server exposes a catalog of tools; the agent queries the catalog (`tools/list`) and then invokes specific tools (`tools/call`) with structured arguments.

The important design choice here is that tool descriptions are written for a language model to reason about, not for a human developer to read documentation. A good MCP tool has a name, a one- or two-sentence description, an input schema with field-level descriptions, and structured error responses. The descriptions are treated by the model as prompt context. This means a well-designed MCP server is closer to a prompt-engineered API than to a conventional REST endpoint. The linguistic quality of the tool descriptions is genuinely part of the server's correctness — something that takes enterprise developers coming from a traditional software background a few weeks to internalise.

### Resources

This is the part most people miss. A resource, in MCP terms, is a read-only piece of data the server makes available to the agent: a document, a database row, a configuration file, a policy document, a customer record. Resources are conceptually different from tools. A tool is *executed*; a resource is *read*. The agent does not "call" a resource — it fetches it and places the content into its own context.

For enterprise deployments, resources often matter more than tools. Imagine an internal policy bot. You do not want to expose a tool called "get_policy_document(id)" that the model has to guess how to invoke — you want the agent to be able to browse a resource tree ("policies/hr/parental-leave.md", "policies/security/acceptable-use.md") and pull the documents it needs into its context. Resources are also the right primitive for document-heavy workflows, contextual grounding, and any case where the model needs to *read* something rather than *do* something.

The distinction matters in architecture discussions. If someone is building an MCP server for your enterprise knowledge base and has only modelled tools, they have probably built the wrong thing.

### Prompts

This is the least-used of the three capabilities, but it is worth understanding. Prompts, in MCP terms, are reusable prompt templates that the server offers to clients. A server can advertise "here is a proven prompt for summarising a support ticket," and a compatible client (e.g., Claude Desktop) can present this prompt as a selectable option to the user.

In most enterprise deployments, prompts are a curiosity rather than a core feature. But they exist, and the reason they exist is principled: the MCP designers wanted the protocol to be symmetric about what a server can offer. Tools are "things to do." Resources are "things to read." Prompts are "things to say." A complete MCP server can advertise all three.

## The Handshake, Demystified

MCP is a client-server protocol. Something initiates the connection (the client — usually an agent or an agent framework acting on its behalf); something else accepts the connection (the server — usually a thin wrapper around an internal API or data source). Once connected, they exchange messages using a small JSON-based RPC vocabulary.

The initial connection has one round of negotiation that the protocol calls the "initialize" exchange. It does three things:

- **Protocol version**: "I speak MCP version 2025-06-18; do you?"
- **Capabilities**: the server announces which of {tools, resources, prompts} it offers; the client announces which optional capabilities it supports (sampling, roots, notifications).
- **Identity**: names and versions, for logging and debugging.

After that, the interaction is just method calls over the transport (stdio for local connections, HTTP with server-sent events for remote ones):

- `tools/list` → server returns catalog
- `tools/call` → client invokes a tool with arguments; server returns result
- `resources/list`, `resources/read` → same pattern for data
- `prompts/list`, `prompts/get` → same for prompt templates

That is it. The vocabulary is small on purpose. Most of the interesting design work in an MCP deployment happens inside the server — how you model your domain, how you write your tool descriptions, how you design your resource tree — not in the protocol itself.

A useful intuition: the protocol is roughly as thin as HTTP. It does not know what your business does. It is a way for two processes to discover each other's capabilities and exchange structured calls. Everything interesting happens at the application layer above it.

## What MCP Looks Like in an Enterprise

When an enterprise adopts MCP seriously, the resulting architecture is almost always the same shape. At the centre is a handful of internal MCP servers, each wrapping some part of the company's existing systems — the CRM, the ticketing platform, the data warehouse, the internal knowledge base, the identity system. These servers are maintained by the teams that own the underlying systems, because those teams understand the domain semantics best.

Around them, any number of agents — built on any framework, using any model — can connect as MCP clients. The agents do not need to know how the CRM's API is structured. They just need to speak MCP and the internal server handles the translation.

This arrangement has three enterprise-grade properties that explain most of MCP's adoption curve.

**It is re-usable across agents.** When the data team builds an MCP server for the warehouse, that server is immediately usable by the customer support agent, the finance agent, the analytics agent, and the "help me write a SQL query" developer tool. One server, many consumers. This is a dramatically better reuse story than the pre-MCP world, where every agent integrated with every backend separately.

**It is re-usable across frameworks.** If your platform team builds MCP servers this year and your product team decides to switch from LangGraph to ADK next year, the servers do not need to change. The framework on top is a different decision from the protocol underneath. This is one of the strongest arguments against premature framework standardisation — even if you have not picked a framework, you can start building MCP servers that will work with whichever framework you eventually choose.

**It is governed by an external body, not a vendor.** With MCP under the Linux Foundation, no single commercial interest can break compatibility or shift the licensing. Enterprises who spent the 2010s watching vendors try to extract rent from technically open standards are reasonably sensitive to this, and MCP's governance path was designed with those memories in mind.

## The 2026 Roadmap: Enterprise Readiness

MCP's 2026 roadmap, published by the steering committee under the Agentic AI Foundation, lists four priority areas, and the first one is explicitly enterprise readiness. In practice this means three concrete workstreams.

**Identity and access management integration.** The 2025-era MCP spec assumed each client managed its own credentials and auth flows. Enterprises hate this — they want agent access brokered through their existing identity layer, with SSO in and scoped tokens out, auditable centrally. The 2026 work is about specifying how MCP integrates with OAuth 2.1, enterprise SSO providers, and scoped-token issuance.

**Management and observability.** IT administrators need to be able to see which MCP servers are connected, which agents are calling which tools, and what the audit trail looks like — ideally from the same console where they already manage SaaS and cloud access. This is gateway and admin-console work, with specifications emerging for how MCP traffic should be logged, monitored, and managed in production.

**Transport and configuration portability.** The original MCP transport choices (stdio, HTTP+SSE) are being evolved to support streaming, cancellation, and better resilience under enterprise network conditions. Configuration portability — being able to take an MCP deployment from one environment to another without rewriting client configs — is also on the roadmap.

The subtext of this roadmap is that MCP is now consciously being reshaped to look less like a developer protocol and more like an enterprise protocol. That is the same transition HTTP went through from 1993 to 1999 as it accumulated the enterprise scaffolding (caching, authentication standards, proxy behaviour, TLS) that distinguishes a toy protocol from a load-bearing one. MCP is in roughly that same rapid maturation phase, compressed into about a year.

## What MCP Does Not Do

It is just as important to be clear about the limits of the protocol. MCP is deliberately dumb about a lot of things.

**MCP does not orchestrate.** It does not know which tool to call, in what order, or what to do when one fails. That is the job of the orchestration layer (the framework, or a plain LLM-in-a-loop). MCP just delivers the call and returns the result.

**MCP does not authenticate end users.** It can carry bearer tokens and integrate with identity providers, but the authentication model is an enterprise deployment decision, not something MCP dictates. Getting this wrong in production is one of the common failure modes of early MCP deployments.

**MCP does not handle agent-to-agent communication.** That is A2A, covered in the next chapter. The two protocols live at the same layer but serve different directions of traffic.

**MCP does not replace your existing APIs.** It sits in front of them. For an enterprise, the question is not "should we rewrite our APIs in MCP?" The question is "should we build MCP servers that wrap our existing APIs?" The answer for almost any system an agent needs to touch is yes.

## Why You Will Be Writing MCP Servers, Not Just Using Them

One prediction worth making explicitly: in eighteen months, if you have a non-trivial internal platform, you will almost certainly have MCP servers in front of it — written by your own team, maintained as part of your normal platform engineering work.

The reason is simple. External vendors will happily provide MCP servers for their own products (GitHub has one, Linear has one, Notion has one, most major SaaS vendors either ship one or are working on it). But your internal systems — your proprietary CRM customisation, your policy knowledge base, your internal data warehouse, your bespoke workflow engine — no vendor is going to write those servers for you. If you want agents to reach those systems safely, somebody on your team is writing the server.

This is why MCP is more interesting to enterprise platform teams than it might first appear. It is not just a protocol you consume. It is also a protocol you produce. The enterprise-grade art of writing good MCP servers — tight tool surfaces, precise descriptions, strong auth, clean resource hierarchies — is an emerging platform-engineering craft that didn't exist eighteen months ago and is rapidly becoming a core skill.

> **What to take from this chapter:** MCP is the settled standard at the tool-access layer of the agent stack. It standardises three things — tools, resources, prompts — over a small client-server protocol. It is governed by the Linux Foundation, supported by every major vendor, and as of 2026 effectively mandatory for enterprise agent architectures. The near-term roadmap is about enterprise readiness: identity, observability, and management. Plan to both consume MCP servers (from vendors) and produce them (for your own internal systems) — both halves are part of the discipline.

---

*Next: [Chapter 4 — A2A: The Other Protocol](04_a2a_other_protocol.md)*
