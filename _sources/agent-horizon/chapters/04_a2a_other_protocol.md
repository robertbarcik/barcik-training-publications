# Chapter 4: A2A — The Other Protocol

---

## The Layer Most People Forget

If MCP answers "how does my agent talk to a tool," A2A answers "how does my agent talk to another agent." These are the two traffic directions at the access layer of the stack, and they deserve symmetric attention — but they rarely get it. Most enterprise agent projects focus on tools and data first, because that is where the immediate productivity wins live. Agent-to-agent communication sounds like a future problem. Then, somewhere around the twelfth agent the company builds, it stops being a future problem and becomes an urgent one.

This chapter is about why the future problem will arrive faster than most enterprises expect, and why the protocol that solves it — Agent-to-Agent, or A2A — deserves a place in your 2026–2027 architecture thinking.

> **A2A in one sentence:** A2A is to agent-to-agent communication what MCP is to agent-to-tool communication — an open protocol that lets agents built by different teams, on different frameworks, by different vendors, discover each other and cooperate without custom integration work.

## Why Agent-to-Agent Is a Real Architectural Concern

It is tempting to file multi-agent systems under "interesting research but not yet production-relevant." For a single-agent deployment — a support bot, a coding assistant, an analytics helper — A2A is indeed irrelevant. You have one agent; it talks to tools via MCP; that is the whole system.

But enterprise agent architectures do not stay single-agent for long. The reasons are mundane.

**Specialisation.** A general-purpose support agent hits its limits quickly. At some point the team carves out a billing specialist agent, a technical specialist agent, a compliance specialist agent. Each has its own tool surface, its own knowledge base, its own guardrails. The front-line agent needs to route to them.

**Organisational boundaries.** The sales team builds a sales agent. The HR team builds an HR agent. The finance team builds a finance agent. They are owned by different groups, built on different stacks, deployed at different cadences. When a sales rep asks about commission policy, the sales agent needs to ask the HR agent, which needs to ask the finance agent.

**External counterparts.** A vendor's customer agent negotiates with your procurement agent. A client's intake agent delivers a request to your service agent. These counterparts are *not* built by your team. They will never be on the same framework or the same model. The only viable way for them to cooperate is an open protocol.

**Composition.** The same pattern that made microservices useful — a system of small, specialised components with clear contracts — is starting to replay at the agent level. Large-team enterprise agent deployments are rarely monoliths. They are systems of agents, and systems of agents need a protocol.

None of these scenarios are speculative. All of them are already showing up in enterprise deployments. What is speculative is *which* protocol wins. A2A is the leading contender and has the strongest foundation-backed governance story, but it is more contested than MCP and the final shape of the standard will still shift in the next twelve to eighteen months.

## What A2A Does

At its core, A2A does three things.

**Capability discovery.** An A2A-compatible agent can advertise a "card" (sometimes called an "agent card" in the specification) that describes what it can do, what inputs it expects, what outputs it produces, what domains it covers, and how to authenticate when calling it. Another agent — or a router sitting between agents — can query this card to decide whether to delegate to the agent in question.

This is architecturally analogous to service discovery in microservices. Before microservice meshes standardised discovery, every service had to know how to find every other service through ad-hoc configuration or DNS conventions. A2A is attempting the same thing for agents: you do not hard-code which agent handles HR questions; you discover it.

**Task delegation.** Once an agent knows another agent exists and what it can do, A2A defines a structured way to hand off a task. The delegating agent sends a task description (the request, the context, the expected output format); the receiving agent processes it (possibly over a long time, with intermediate updates); the result comes back. The protocol supports both synchronous request-response interactions and longer-running, asynchronous interactions with streaming progress updates.

**Authentication and trust.** Cross-boundary agent calls raise harder security questions than tool calls. If an agent owned by the sales team invokes an agent owned by the finance team, whose identity is the caller? The end user's? The sales agent's? The sales team's? A2A provides hooks for carrying authentication context across the delegation, so downstream agents can make their own authorisation decisions rather than trusting the upstream agent blindly.

This third point is the one enterprises underweight. Tool access is usually bounded by user identity — the user authorised the agent to act on their behalf, and the tool enforces user-level permissions. Agent-to-agent calls can cross organisational or even company boundaries, and the question of whose authority is being exercised at each hop becomes genuinely interesting.

## Where A2A Sits in the Landscape

As of April 2026, A2A's adoption picture is messier than MCP's. A few facts of the landscape.

**Google ADK has native A2A support** and auto-generates A2A-compatible agent cards. This is one of the strongest reasons to take ADK seriously for multi-agent architectures — it removes almost all of the boilerplate of making an agent addressable by other agents.

**CrewAI also supports A2A**, reflecting its multi-agent-first design philosophy. If your mental model is "a team of specialist agents cooperating on a task," A2A is the natural over-the-wire protocol for that team.

**LangGraph, the OpenAI Agents SDK, and the Claude Agent SDK have partial or emerging A2A support as of early 2026.** The gap is closing quickly — all three have published roadmap items for A2A compatibility — but today, if you want the smoothest multi-agent story, you are living in ADK or CrewAI territory.

**Several other agent-to-agent protocols exist.** Anthropic's internal coordination mechanisms, Microsoft's semantic-kernel-based agent protocols, and academic efforts like the Agent Communication Protocol (ACP) all overlap with A2A's scope. The politics of which protocol wins is messier than MCP's — partly because A2A is younger, partly because the governance has not yet coalesced under a single foundation, and partly because the design space is inherently broader.

Our read in April 2026 is that A2A has the strongest momentum, but it is not yet the slam-dunk consensus MCP is. The sensible bet for most enterprises is to design with A2A in mind, treat cross-agent protocols as an area where some rework may be needed in 2027, and avoid building a proprietary in-house agent-communication protocol that you will then need to deprecate.

## A Useful Analogy: Email as an Open Agent Protocol

One way to see why A2A matters is to imagine what happens without it.

For the last twenty years, enterprises have used email as the de facto agent-to-agent protocol. Not for software agents — for human agents. When the sales team needed something from finance, a sales rep wrote an email. Email worked because it was an open protocol: everyone's inbox could receive mail from everyone else's outbox, regardless of which client they used, which server they ran, or which company they worked for. The protocol was neutral. Content was structured enough to be useful but unopinionated about the work itself.

Imagine an alternative world where Microsoft, Google, and Yahoo each had their own incompatible messaging protocols. Sales at a Google-shop company could not email finance at a Microsoft-shop company without building a custom bridge. Every inter-organisation communication would have required a one-off integration. The productivity tax would have been crushing.

That alternative world is where the agent ecosystem sits *today*, minus A2A. Without a neutral protocol, every cross-agent call is a one-off integration. With A2A, the vendor owning your agent and the vendor owning their agent can be different, and the cooperation still works. This is not a niche capability. It is the precondition for multi-agent architectures reaching the scale that email has.

## The Protocol That Will Matter More Than Most Architects Think

Our expectation is that A2A (or a direct successor with near-identical design goals) will be genuinely ambient by 2027–2028 in the same way MCP is ambient today. The adoption curve will be slower, because the problems A2A solves become urgent only once an enterprise has multiple agents in production, and most enterprises have fewer than three agents in production as of early 2026. But the curve is accelerating, and the organisations that have deployed twenty agents are already deep in A2A work.

A2A belongs in your mental model of the stack for the same reason HTTP and SMTP both belong in your mental model of the internet: they do different things, at roughly the same layer, and any serious architectural discussion needs them both.

## What to Do About A2A Today

For most enterprises in 2026, the practical advice is simpler than it looks.

**Do not over-invest in A2A infrastructure yet.** If you are building your first agent, focus on MCP, focus on the orchestration layer, and treat A2A as something you will adopt when it becomes relevant. Premature A2A architecture usually means designing a multi-agent system before the business has a use case for one.

**Do not rule out A2A by accident.** When you pick a framework, check its A2A story. If you choose a framework with no A2A roadmap, you are making a quiet bet that multi-agent architecture will not matter for your use case. That bet is defensible for a single-purpose agent; it is risky for a platform.

**Start thinking in terms of agent cards.** Even if you are not formally using A2A yet, the habit of writing down "what can this agent do, what does it need, what does it return" in a structured way is useful discipline. That discipline becomes cheap to formalise later when you adopt a protocol.

**Watch which A2A variant your vendors converge on.** As of mid-2026, expect additional coalescence around a single protocol. When the foundation picture becomes clearer — which will happen through vendor announcements, foundation formations, or pragmatic consolidation — you want to be ready to adopt, not locked into an internal variant you now have to migrate away from.

> **What to take from this chapter:** A2A is the other protocol at the access layer of the agent stack, covering agent-to-agent communication rather than agent-to-tool. Its adoption is roughly a year behind MCP's and its governance is less settled, but it is the leading contender and will likely be ambient by 2027–2028. Enterprises should treat A2A as an architectural concern that becomes urgent when multi-agent deployments reach scale — which will happen faster than most single-agent teams expect. Pick frameworks with a credible A2A roadmap, even if you are not using multi-agent patterns today.

---

*Next: [Chapter 5 — The Orchestration Layer](05_orchestration_layer.md)*
