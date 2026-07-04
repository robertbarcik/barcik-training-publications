# Chapter 14: The "Do Nothing" Scenario and Your 18-Month Roadmap

> **At a glance**
>
> - Doing nothing is not neutral. AI becomes the front door to the client relationship, and whoever walks through it first takes the hosting contract with them.
> - The 18-month roadmap: Foundation (months 1-6: learn, build one internal tool) → First clients (7-12: two or three friendly pilots, APIs not self-hosting) → Scale (13-18: one or two packaged offerings, 5-10 paying clients).
> - Eight mistakes early movers already made, from competing with OpenAI on price to promising "your own GPT." Skip them.
> - The reframe that drives everything: you are an expertise company that sometimes operates infrastructure. Invest, hire, sell, and price accordingly.
>
> **The number to remember:** 18 months, the head start a competitor who begins today has over you if you wait. It cannot be bought back.

---

## The Comfortable Default

Doing nothing feels reasonable right now. Your hosting contracts are still renewing. Nobody in your client base has called to say they are cancelling because you do not offer AI services. The monthly recurring revenue continues to arrive, predictable and familiar.

So the temptation is to treat generative AI like every other technology wave: watch from a distance, wait for the market to mature, step in when the path is clear. This approach worked with cloud, containers, and DevOps.

It will not work this time.

## The Slow Erosion You Will Not See Coming

Your infrastructure revenue will probably not collapse in 2026 or 2027. Hosting contracts have inertia. But here is what happens over 3-5 years if you do nothing.

Your clients start exploring AI. A junior developer builds a prototype, or a department head sees what a competitor is doing and asks the CTO to investigate. They need someone to help evaluate models, build integrations, handle EU AI Act compliance, and eventually operate AI systems at scale. They look at you first: you are their IT services provider, you understand their environment. And when your answer is "not yet," they call someone else.

The risk is that AI becomes the entry point for the client relationship, not that infrastructure dies. Whoever helps a client with their first AI deployment earns trust and positions themselves as the strategic technology partner. That partner then says: "By the way, we also do infrastructure management. Want us to take a look at your hosting?"

> **The real threat: AI becomes the front door to the client relationship, and whoever walks through that door first takes the hosting contract with them.**

This played out with cloud migration consulting in the 2010s. The firms that helped clients move to AWS captured not just the migration project but the ongoing management, security monitoring, and eventually the entire IT relationship.

## Your Competitors Are Already Moving

The IT services provider in your market who starts today will, by the time you begin, have 18+ months of learning, 2-3 client references, and engineers who have been through the full cycle of deploying, debugging, and improving AI systems in production. You cannot buy that experience on the open market. You cannot shortcut it with a strategy deck. It comes only from doing the work.

The cost of starting late is always higher than the cost of starting imperfectly. A failed pilot with a friendly client is infinitely more valuable than a flawless plan that never executes. And the learning compounds: each project makes the next one faster, cheaper, and better scoped.

## What Not to Do: Lessons from Early Movers

Before we lay out the roadmap, here are the mistakes that early movers have already made across the European IT services market. These are not hypothetical.

1. **Do not try to compete with OpenAI on price.** You will lose. Chapter 4 laid out why the hyperscaler cost advantage is structural. Your value is better integration, compliance, and client context, not cheaper inference.

2. **Do not promise "we will build you your own GPT."** Clients hear this and expect frontier-level capability running privately. What they get is a noticeably less powerful system that costs more to operate. Set expectations honestly.

3. **Do not underestimate the ops burden of self-hosting.** Running GPU inference infrastructure is not like hosting a web server. The failure modes, monitoring requirements, and talent are all different. Several providers have learned this the hard way.

4. **Do not assume your current team can transition without significant upskilling.** ML inference optimization, prompt engineering, and AI evaluation are genuinely different disciplines from cloud operations. Plan for a 6-12 month learning curve.

5. **Do not ignore shadow AI.** Your clients' employees are already using ChatGPT and Claude with company data, without IT's knowledge, without compliance review. Solving this is an excellent entry point for broader AI services.

6. **Do not build around a single model or provider.** The landscape shifts quarterly. Build model-agnostic architectures from the start.

7. **Do not start with the hardest use case.** Pick low-risk, high-visibility wins first: a chatbot over company docs, document classification, meeting summaries. Build credibility before attempting agentic workflows.

8. **Do not sell "AI" as a buzzword.** "We will add AI to your business" means nothing. "We will classify incoming support tickets and route them automatically, reducing response time by 40%" means everything.

## The Portfolio View

Before the roadmap, one page that answers the question the previous nine chapters raise one model at a time: which of these do I actually pick? The table below puts every business model in this booklet side by side. No new numbers; every cell restates what its own chapter already claimed, so you can argue with any row by rereading its source.

| Business model | Chapter | Margin | Time to first revenue | Defensibility | What kills it |
|---|---|---|---|---|---|
| Managed on-prem AI infrastructure | 3-4 | 40-55% | 6-12 months | High: operational, compliance-anchored | Client insourcing at 500+ users |
| Vendor ecosystem play (Copilot, Joule, Now Assist) | 5 | ~20% licenses, 50-70% services | Immediate | Low: every partner sells the same thing | Partner-term changes; vendors making adoption self-service |
| Privacy proxy | 6 | Thin (~10% of API spend) | 3-6 months | Low as a product, fair as a layer | One vendor data-residency announcement |
| Local deployment on employee devices | 7 | 70-85% at scale | 6-12 months | High: fleet, lifecycle, and guardrail muscle | OS vendors shipping local AI as the default |
| Testing and validation | 8, 11 | Highest | 12-18 months | High: scarce evaluation expertise | Price compression once the market matures |
| GenAI security | 8 | High | 6-12 months | High | Audit tooling commoditizing the low end |
| Agentic infrastructure | 8 | Moderate-high | 3-6 months | Medium: integration skills are learnable | Standardization (MCP and successors) lowering the barrier |
| Oversight as a service (AgentOps) | 8 | High, retainer-shaped | 6-9 months | High: 24/7 desk plus a regulatory requirement | Oversight tooling automating the desk itself |
| Multi-model management | 8, 10 | High | Builds over time | High: conflict-free advisor position | Provider consolidation reducing the complexity you manage |
| EU AI Act compliance services | 11 | High, premium consulting | 3-9 months | High until the market catches up | Rate compression after the August 2026 crunch passes |
| Data sovereignty hosting | 11 | Premium | 6-12 months | High: jurisdictional, not just technical | EU-hosted third-party inference eating the middle |
| AI-augmented capacity (nearshoring 2.0) | 9 | Expanding, if repriced in time | Immediate, existing contracts | Medium | Clients clawing the productivity delta back through rates |
| Productized vertical IP | 12 | Product-level at scale | 18+ months | Highest: owned IP | Billable pressure starving the product team |

Read the table as a portfolio, not a menu. The pattern that works is one cash engine plus one differentiator. The cash engines sit at the top of the time-to-revenue column: the vendor ecosystem play and repriced staff augmentation monetize relationships and contracts you already have, this quarter. The differentiators sit at the bottom of the defensibility column: local deployment, testing, oversight, productized IP. They take 12-18 months to build and cannot be taken away by someone else's partner program. The cash engine funds the differentiator; the differentiator is why you still have margins in 2029. A provider running only cash engines is commoditized in three years. A provider building only differentiators runs out of money in one. Pick one of each, deliberately, and let the roadmap below sequence them.

## The 18-Month Roadmap

What follows is a phased action plan designed for an EU IT services provider with 30-500 employees, existing infrastructure clients, and little to no current AI capability. Adjust the specifics to your situation, but respect the sequencing: each phase builds on the one before it.

### Phase 1: Foundation (Months 1-6)

The goal of this phase is learning, not revenue.

1. **Conduct an honest internal skills assessment.** Map your team against what AI services require: ML engineering, prompt engineering, evaluation methodology, AI compliance. Be unflinching about the gaps.

2. **Identify 2-3 team members for AI upskilling.** Choose people who combine technical aptitude with curiosity. They do not need to be your most senior engineers; they need to be your most adaptable. Invest in structured training, certifications, and hands-on workshops.

3. **Build one internal AI tool for your own company.** This is the most important item on this list. Eat your own cooking. A chatbot over internal docs, automated ticket classification, AI-assisted proposal writing. It does not matter what. What matters is going through the full cycle of building, deploying, and iterating. This single project will inform every client engagement that follows.

4. **Start with API integration, not self-hosting.** Use frontier APIs from OpenAI, Anthropic, Google, or Mistral. Learn what the models can do before you worry about hosting them. The application layer is where most of the value sits. Infrastructure comes later.

5. **Research EU AI Act obligations relevant to your clients' industries.** This knowledge becomes a differentiator faster than any technical capability.

6. **Have conversations with 3-5 clients about their AI pain points.** Do not sell anything yet. Listen. These conversations will shape your offerings more than any market report.

**Budget**: EUR 20,000-50,000 for training, tools, API credits, and experimentation time.

### Phase 2: First Client Engagements (Months 7-12)

The goal is learning with real clients. Revenue is welcome but secondary.

1. **Launch 2-3 pilot projects with friendly clients.** Choose clients who trust you and are forgiving of imperfection. Offer favourable pricing in exchange for patience and detailed feedback.

2. **Start small.** A chatbot over company documentation, automated document processing, an internal knowledge base with natural language search. Well-understood use cases with manageable complexity and high visibility.

3. **Use frontier APIs; do not self-host yet.** Focus on building good prompt templates, evaluation pipelines, clean integrations, and monitoring that catches quality issues before the client does.

4. **Build your first repeatable delivery template.** Document the discovery process, architecture decisions, implementation steps, and handoff procedure. The second pilot should be faster than the first.

5. **Develop initial pricing models and packaging.** Test different approaches: per-user fees, project-based pricing, token pass-through, or hybrids. Review Chapter 12.

6. **Hire or contract 1-2 AI-experienced engineers if budget allows.** Even one person who has deployed AI in production dramatically accelerates your team's learning.

7. **Start evaluating local deployment feasibility.** Test llama.cpp and MLX on standard hardware. Benchmark open-source models against the APIs you have been using, so you are ready for Phase 3.

**Budget**: EUR 40,000-80,000 for hiring or contracting, client pilots, tools, and API costs.

### Phase 3: Scale and Specialize (Months 13-18)

The goal is productizing what you have learned.

1. **Double down on what works.** Your pilots will reveal which use cases resonate, which delivery approaches are efficient, and which pricing sticks. Deprioritize what did not work; sunk cost discipline matters.

2. **Develop 1-2 packaged offerings.** Based on the business models explored in Chapters 5-8, build repeatable service packages with clear scope, pricing, and deliverables. Local deployment plus compliance for privacy-sensitive clients, or agentic infrastructure monitoring, whatever your pilots validated.

3. **Build model-agnostic architecture capabilities.** Ensure your framework can swap models without rebuilding the application. This protects clients from lock-in and protects you from the next model landscape shift.

4. **Consider your first local deployment client.** If you have the talent, the client need is genuine, and the hardware is adequate, then execute it. This adds a high-value capability that few competitors will have.

5. **Formalize EU AI Act compliance services.** By month 13, you should have enough practical experience to offer compliance advisory with credibility.

6. **Train your sales team.** They need to articulate business value and handle objections, not explain transformer architectures.

7. **Target: 5-10 paying clients by month 18.** A mix of pilot conversions, new clients, and upsells to existing infrastructure clients.

**Budget**: EUR 60,000-120,000 for team growth, marketing, sales enablement, and infrastructure.

## Key Metrics to Track

You cannot manage what you do not measure. From month one:

- **Revenue from AI-related services**: should be greater than zero by month 12
- **Number of client pilots and conversion rate**: a healthy rate is 40-60%; lower means your pilots may be too ambitious or pricing misaligned
- **Team capabilities**: how many people can independently scope, deliver, and support an AI engagement?
- **Client NPS on AI services specifically**: measure separately from infrastructure; early satisfaction predicts referrals
- **Pipeline of AI-related opportunities**: your leading indicator of future revenue

## Infrastructure or Expertise: The Five-Year Question

We return, in this final chapter, to the question posed in Chapter 1:

> **In five years, will your company's primary revenue come from infrastructure you operate, or from expertise you deliver?**

The twelve chapters between that question and this answer have built the case from every angle: the economics of self-hosting, the structural advantages of hyperscalers, the business models that work, the regulatory landscape, the talent market, the pricing dynamics. Here is what all of it points to.

The infrastructure margin in generative AI is being compressed to near zero for anyone who is not a hyperscaler. The GPU is becoming a commodity input, not the product. The companies that try to compete on compute will find themselves in an unwinnable race against providers with trillion-dollar capital bases and global-scale infrastructure.

The expertise margin (knowing how to make AI work in a specific client's context, how to evaluate its output, how to keep it safe, how to integrate it into workflows, how to navigate the EU AI Act, how to manage the model lifecycle) is where value is migrating. And it is migrating fast.

This is actually good news.

Because you own the client relationship. You understand their environment, their constraints, their industry, their regulatory obligations, and their organizational culture. A hyperscaler in Mountain View or Seattle does not have that knowledge and cannot easily acquire it. An AI startup in San Francisco does not have your 15 years of trust with the CTO.

Your value is in the last mile: getting AI to work reliably in a specific context, for a specific client, with their specific data and their specific compliance requirements. That last mile is messy, complex, context-dependent, and enormously valuable. It is also exactly the kind of work that IT services providers have always done well.

You just need to stop thinking of yourself as an infrastructure company. You are an expertise company that sometimes operates infrastructure. The distinction matters, because it changes what you invest in, what you hire for, what you sell, and how you price it.

> **The companies that internalize this shift early will thrive. They will capture the advisory relationships, build the delivery muscle, and establish the client references that create compounding competitive advantage. The ones that keep trying to sell compute, that keep looking for a way to mark up GPU hours the way they once marked up virtual machines, will find the margins thinner every year and the competition more intense.**

## Start This Week

The best strategic plan is worthless without the first step. And the first step is small enough to take this week.

Pick one AI project. It does not need to be for a client; it can be for your own company. Build a chatbot over your internal wiki. Automate the weekly status report that nobody enjoys writing. Set up a document classifier for your support tickets. Give two engineers API keys and a week to experiment.

The project will be imperfect. The first prototype will be clumsy. The model will hallucinate something embarrassing. The integration will break in a way that makes everyone laugh. Good. That is learning. That is what month one looks like. And month eighteen looks nothing like month one, but only if month one actually happens.

The window for building AI capability in the EU IT services market is open right now. The technology is accessible. The client demand is real and growing. The regulatory environment, for once, favours local providers who understand European requirements. And the competition, while moving, has not yet locked up the market.

Eighteen months from now, you will either be a provider with AI capabilities, client references, and a growing pipeline, or you will be a provider watching from the sidelines as your competitors capture the relationships that used to be yours.

The math is clear. The path is laid out. The first step is yours to take.

> **Freshness Watch** · *verified April 2026 · estimated half-life: ~12+ months*
>
> The 18-month roadmap structure is framework-level and will age slowly. Specifics to re-verify:
>
> - **Budget ranges per phase** (EUR 20-50K Phase 1, EUR 40-80K Phase 2, EUR 60-120K Phase 3) reflect 2026 EU cost structures; re-calibrate against your actual salary, tooling, and API-credit costs before committing.
> - **Starting-technology defaults** ("use frontier APIs in Phase 1, consider local deployment in Phase 3") follow the capability curve of the most recent model generation. If open-source models close the frontier gap faster than expected, Phase 2 and Phase 3 timing compresses.
> - **The 2028 "AI as default entry point" claim** is a market-trajectory bet grounded in current consolidation data (Chapter 9). If that consolidation stalls, the urgency argument weakens; if it accelerates, the window closes faster than 18 months.
>
> The core argument (doing nothing is not neutral, the competitor who starts today has an 18-month head start you cannot buy) is structural and durable.

---

*End of The Token Economics: A Strategic Guide for EU IT Services Providers Navigating GenAI*
