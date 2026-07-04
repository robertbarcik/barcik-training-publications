# Chapter 1: The Cloud Parallel

---

If you've been in enterprise IT for more than a decade, the way agent development is being debated in 2026 should feel suspiciously familiar.

Three foundation-model vendors (Google, OpenAI, Anthropic) are pushing polished, opinionated development kits that make it easy to build an agent in an afternoon, provided you stay in their ecosystem. A smaller cluster of vendor-neutral frameworks (LangGraph, CrewAI) insists the only responsible choice is portable abstractions that outlive a model-provider change. In between, a protocol called the Model Context Protocol (MCP) has quietly become the default way for agents to reach tools and data. It's open, foundation-governed, already at tens of millions of SDK downloads per month, and most of the industry has stopped arguing about it.

Swap names and this is almost exactly the conversation we had between 2010 and 2015. The polished vendor kits were AWS, Azure, GCP. The neutral frameworks were Kubernetes and Docker. The quiet protocol was HTTP. The debate was not *whether* to go to the cloud; it was whether to commit to *one* cloud and accept the lock-in, or build on portable abstractions and pay the abstraction tax upfront.

The claim of this booklet is that the agent landscape is re-running the cloud playbook. Not in every detail, and not at the same speed. But closely enough that a working mental model of how the cloud transition played out already gets you most of the way to a working mental model of how the agent transition will.

**Foundation models are the new compute. MCP is the new HTTP. Vendor agent SDKs are the new Platform-as-a-Service. Agnostic frameworks like LangGraph are the new Kubernetes.** That is the one-sentence version of the rest of this book.

## Why the Parallel Holds

A handful of hyperscale vendors have an unassailable cost advantage at the bottom of the stack. Nobody could match AWS's per-core price in 2012 because AWS had amortised its infrastructure across millions of customers. Nobody can match OpenAI's or Anthropic's per-token price today because they've amortised training costs across a similarly massive user base. The cost curve is structural, not temporary. Renting is cheaper than owning, except for a narrow set of workloads where compliance, latency, or data sovereignty force a different choice.

The vendors selling the cheap bottom layer are also trying to sell you the layer on top. AWS didn't just sell EC2: it pushed Elastic Beanstalk, Lambda, SageMaker, and dozens of other managed services that are extraordinarily convenient as long as you never want to leave AWS. Foundation-model vendors are doing the same thing: Google pushes ADK + Vertex, OpenAI pushes the Agents SDK with hosted sandboxes, Anthropic pushes the Claude Agent SDK with built-in computer-use tools. The gravitational pull is identical.

And in both cases, a neutral middle layer emerged in response. Not because the vendor offerings were bad, but because a critical mass of enterprises decided that being able to swap the bottom layer without rewriting the top layer was worth the engineering cost.

## Where the Parallel Breaks

A good analogy is one you can stress-test. This one has two cracks worth flagging up front.

**The timeline is compressed.** The cloud transition took about a decade to reach its settled shape. The agent stack has gone from "interesting experiment" (late 2022) to "settled protocol plus competing frameworks" (early 2026) in under four years. Whether that means the final shape arrives in another four years or whether we're in the equivalent of 2010 with another decade of churn ahead is an open question. Chapter 10 takes it seriously.

**The lock-in is deeper.** When an enterprise migrated off AWS, PostgreSQL was still PostgreSQL and Java was still Java. Vendor-specific parts (queues, DNS, identity) were replaceable. In the agent world, when an enterprise builds on Claude's computer-use capability, that capability isn't a portable abstraction; it's baked into how Anthropic's model was trained. You cannot run the same workflow through GPT-4o and expect it to behave. Vendor lock-in in the cloud era was mostly about surrounding services. Vendor lock-in in the agent era can reach all the way down to model behaviour itself.

File both caveats and keep them in mind as you read. The cloud analogy is scaffolding, not blueprint.

## The EU Wrinkle

One cloud-era feature is worth calling out early because it will likely replay. The European cloud transition was slower than the US transition. GDPR wasn't fully in force yet, but data-protection norms made cross-border data transfer a live engineering concern, not just a legal one. The predictable consequence: by the time European enterprises moved seriously to the cloud, they could skip the painful early lessons. Multi-cloud was already a recognised pattern; vendors had already been forced to offer portability tools. The European market effectively **leapfrogged Phase 1**.

There is a credible argument that the EU does this again with agents. The AI Act is a stronger forcing function than GDPR was for cloud. Sovereignty concerns are sharper, not softer. And the sovereign-AI movement across Europe is pushing an architectural pattern (model-agnostic routing with on-prem or EU-region execution for regulated data) that looks a lot like a mature agent stack rather than an early one.

Whether the leapfrog actually happens depends on things that are genuinely unknowable in April 2026. But the pattern is strong enough that any European enterprise planning its agent strategy should at least ask: *are we about to repeat the cloud cycle, or skip ahead?* Chapter 9 develops this directly.

The rest of this booklet is an elaboration of the picture above. The goal through Chapter 11 is to be specific enough that when you finish, you can tell a colleague what MCP is, why ADK and LangGraph are not in the same category, and what your organisation should actually do about any of it.

---

*Next: [Chapter 2: The Layer Cake](02_layer_cake.md)*
