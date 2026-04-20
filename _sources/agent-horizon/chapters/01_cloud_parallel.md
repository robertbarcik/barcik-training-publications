# Chapter 1: The Cloud Parallel

---

## A Familiar Feeling

If you have been in enterprise IT for more than a decade, the way agent development is being debated in 2026 should feel suspiciously familiar.

In one corner, a handful of large foundation model vendors — Google, OpenAI, Anthropic — are pushing polished, opinionated development kits that make it easy to build an agent in an afternoon, provided you are willing to live inside their ecosystem. In the other corner, a small cluster of vendor-neutral frameworks — LangGraph, CrewAI, a few quieter contenders — insist that the only responsible choice is to build on top of abstractions that will survive a change in model provider. In between, a protocol called the Model Context Protocol (MCP) has quietly become the default way for agents to reach tools and data. It is open, it is governed by a foundation, it already has tens of millions of SDK downloads a month, and most of the industry has stopped arguing about it.

If you replace a few names, this is almost exactly the conversation the enterprise IT world had between 2010 and 2015.

Back then, the polished vendor kits were called AWS, Azure, and Google Cloud. The neutral frameworks were called Kubernetes and Docker. The quiet protocol everyone agreed on was HTTP. The debate was not *whether* to go to the cloud — it was whether to go to *one* cloud and accept the lock-in, or to build on portable abstractions and pay the abstraction tax upfront.

This booklet's central claim is that the agent landscape is re-running the cloud playbook. Not in every detail, and not at the same speed. But closely enough that if you have a clear mental model of how the cloud transition played out, you already have a working mental model for how the agent transition will play out. The rest of this booklet is about getting that mental model precise enough to be useful.

> **The core analogy in one sentence:** Foundation models are the new compute. MCP is the new HTTP. Vendor agent SDKs are the new Platform-as-a-Service. Agnostic frameworks like LangGraph are the new Kubernetes. And the companies paying attention are already deciding which layer to standardise on.

## Why the Parallel Holds

The parallel is not accidental. Both transitions share the same deep structure.

In both cases, a handful of hyperscale vendors have an unassailable cost advantage at the bottom of the stack. In the cloud era, nobody else could match AWS's per-core price, because AWS had amortised its infrastructure investment across millions of customers. In the agent era, nobody else can match OpenAI's or Anthropic's per-token price, because they have amortised their training costs across a similarly massive user base. In both cases, the cost curve is structural, not temporary. Renting is cheaper than owning, except for a narrow set of workloads where compliance, latency, or data sovereignty force a different choice.

In both cases, the vendors selling the cheap bottom layer are also trying to sell you the layer on top. AWS did not just sell EC2 instances — it aggressively pushed Elastic Beanstalk, Lambda, DynamoDB, SageMaker, and dozens of other managed services that are extraordinarily convenient as long as you never want to leave AWS. The foundation model vendors are doing the same thing today. Google is not just selling Gemini tokens — it is selling ADK, Vertex AI Agent Builder, and a growing stack of tightly integrated tools that make Gemini even more attractive. OpenAI is not just selling GPT tokens — it is selling the Agents SDK, hosted sandboxes, and its own managed tool layer. Anthropic is not just selling Claude tokens — it is selling the Claude Agent SDK with eight built-in tools that assume a Claude model underneath.

And in both cases, a neutral middle layer emerged in response. Not because the vendor offerings were bad, but because a critical mass of enterprises decided that being able to swap the bottom layer without rewriting the top layer was worth the engineering cost. Kubernetes was not designed because Docker Swarm or AWS ECS were unusable. It was designed because CIOs did not want a single vendor holding the keys to their entire application portfolio. The same logic is producing LangGraph today. It is not that ADK or the OpenAI Agents SDK are broken. It is that some enterprises — particularly large, regulated ones — have looked at the long-term implications of a vendor SDK and decided they would rather pay the abstraction tax upfront.

## Where the Parallel Breaks

A good analogy is one you can stress-test. This one has two cracks worth naming early, because we will come back to them throughout the booklet.

**The timeline is compressed.** The cloud transition took roughly a decade to reach its settled shape. The first AWS services launched in 2006. By 2010, early adopters were fully cloud-native. By 2015, Kubernetes was general-availability and enterprise anti-lock-in mandates were starting to emerge. By 2020, hybrid and multi-cloud were the dominant enterprise pattern. That is a fifteen-year arc from "interesting experiment" to "settled architecture." The agent stack has gone from "interesting experiment" (late 2022, when ChatGPT launched) to "settled protocol plus competing frameworks" (early 2026) in under four years. Whether this means the final shape will also arrive in four years or whether we are in the equivalent of the year 2010 and have another decade of churn ahead — that is an open question. We look at it directly in Chapter 11.

**The lock-in is deeper than in the cloud era.** When an enterprise migrated off AWS, the database was still PostgreSQL, the web server was still nginx, and the application was still written in Java or Python. The vendor-specific parts — queues, DNS routing, identity services — were replaceable, often painfully but tractably. The agent world is different. When an enterprise builds on Claude's computer-use capability, that capability is not a portable abstraction. It is baked into how Anthropic's model was trained. You cannot run the same workflow through GPT-4o and expect it to behave. The vendor lock-in in the cloud era was mostly about surrounding services. The vendor lock-in in the agent era can reach all the way down to model behaviour itself.

We will return to both of these cracks in due course. For now, file them as caveats. The cloud analogy is a strong scaffold, not an exact blueprint.

## What the EU Did Differently (and Might Do Again)

One feature of the cloud transition is particularly relevant for European readers, because we are very likely to see it replay.

The European cloud transition was slower than the US transition. This was partly a regulatory story — data protection rules made cross-border data transfer a real engineering concern, not just a legal one — and partly a cultural story about risk tolerance. For most of the 2010s, the dominant European posture toward AWS was cautious engagement. A typical regulated enterprise would run non-sensitive workloads in AWS, keep sensitive data on-premises or in a European private cloud, and wait to see how the regulatory landscape evolved before making bigger commitments.

The predictable consequence was that by the time European enterprises were ready to move seriously to the cloud, they had the luxury of skipping the painful early lessons. They did not need to live through the 2012–2014 lock-in panic, because by the time they were deploying at scale, Kubernetes already existed, multi-cloud was already a recognised pattern, and the vendors had already been forced to offer portability tools. The European market effectively leapfrogged Phase 1.

There is a credible argument — which we develop in Chapter 10 — that the EU will do this again with agents. The AI Act is a stronger forcing function than GDPR was for cloud; data sovereignty concerns are sharper, not softer, than they were a decade ago; and the sovereign AI movement across Europe is pushing a specific architectural pattern (model-agnostic routing with on-prem or EU-region execution for regulated data) that looks a lot like a mature agent stack rather than an early one.

Whether that leapfrog actually happens depends on things that are genuinely unknowable in April 2026 — how fast the EU AI Act gets enforced in practice, whether European open-weight models stay competitive with US frontier models, whether the cost of running private inference comes down fast enough. But the historical pattern is strong enough that any European enterprise planning its agent strategy should at least ask: *are we about to repeat the cloud cycle, or skip ahead?*

> **What to take from this chapter:** The agent landscape of 2026 is structurally similar to the cloud landscape of 2012. A small number of vendors dominate the bottom of the stack. A settled protocol (MCP, playing the role of HTTP) sits at the tool-access layer. Vendor PaaS-style SDKs are competing with a smaller pool of agnostic frameworks. The EU is likely to sit out the early lock-in phase, just as it did with cloud. Two important caveats: the timeline is running faster than it did with cloud, and the lock-in can reach deeper into model behaviour itself. Hold these two caveats in mind as you read the chapters that follow.

---

*Next: [Chapter 2 — The Layer Cake](02_layer_cake.md)*
