# Chapter 12: Pricing Models and Packaging

You have built the capability. You understand the infrastructure economics, the business models, the compliance landscape. Now comes the question that determines whether any of it generates revenue: how do you actually price this?

Pricing GenAI services is harder than pricing traditional IT services, and the reason is simple. Your client has a reference point, and that reference point is devastating. ChatGPT Team costs $30 per seat per month. Claude Pro costs $20. Microsoft Copilot costs $30. These are frontier-level AI products, built by companies with tens of billions in infrastructure investment, offered at prices that would not cover your team's coffee budget.

If what you are selling looks anything like "access to an AI chatbot," you have already lost. No amount of positioning, no sales deck, no carefully worded value proposition will overcome the basic arithmetic: why would a client pay you $80 per user per month when they can get ChatGPT for $30?

The answer, of course, is that you are not selling an AI chatbot. You are selling a solution to a specific business problem, and the language model is one component of that solution — your cost of goods sold, not your product. The model cost is to your AI service what flour is to a bakery. Nobody walks into a bakery and says "I can buy flour for $0.50 per kilo, so this bread should cost $0.60." But if your storefront looks like a flour shop, that is exactly the comparison they will make.

> **The pricing principle**: You are not selling LLM access. You are selling an AI-powered solution. The moment a client can compare your offering line-by-line with a $30/seat consumer product, you have a positioning problem, not a pricing problem.

This chapter walks through five pricing models, a packaging framework, and the service-level price ranges you need to build a viable commercial practice.

## Five Pricing Models

There is no single correct way to price GenAI services. The right model depends on your delivery architecture, your client's risk tolerance, and where you sit on the spectrum from infrastructure provider to solution partner. Here are the five models that work in practice, with honest assessments of each.

### 1. Per-Seat Subscription

**Structure**: $40-100 per user per month, flat rate regardless of usage.

This is the model most familiar to enterprise buyers. It is easy to budget, easy to compare, and easy to procure. The client knows exactly what they will spend: 200 users at $50 per seat equals $10,000 per month, no surprises.

**Where it works**: Per-seat pricing works best when your underlying cost structure is predominantly fixed — which means it is a natural fit for the local deployment model discussed in Chapter 6. If you have deployed a model running on the client's own hardware or on your managed infrastructure, your costs do not scale meaningfully with per-user activity. A user who sends 500 queries per day and a user who sends 5 queries per month cost you roughly the same in infrastructure. The fixed subscription captures this reality cleanly.

A practical example: $50 per user per month for a managed local AI deployment including guardrails, model updates, basic RAG over company documents, and 8/5 support. At 100 users, that is $5,000 per month in revenue against perhaps $1,500-2,000 in infrastructure and support costs. The margins are healthy because the heavy users are subsidized by the light ones.

**The risk**: That subsidy cuts both ways. If your client's usage pattern is heavily skewed — a small group of power users generating 80% of the load — the light users may question why they are paying the same rate. And if a competitor offers a usage-based alternative, the light users have a reason to leave while the heavy users (who are expensive to serve) stay. This is classic adverse selection, and it can erode your margins quietly.

**Mitigation**: Tier your per-seat pricing. A "standard" tier at $40 per user with reasonable usage limits and a "power user" tier at $80 per user with higher limits and priority support. This segments demand without abandoning the subscription model's predictability.

### 2. Per-Token Passthrough with Markup

**Structure**: Client pays actual API costs plus a 20-40% margin.

This is the most transparent model and, for that reason, the most dangerous. The client can see exactly what the underlying API calls cost, exactly what your markup is, and exactly how much they would save by going direct.

**Where it works**: The passthrough model makes sense for the privacy proxy architecture (Chapter 5), where your value-add is demonstrably not the model itself but the compliance layer, PII stripping, and audit trail you wrap around it. A client paying $5,000 per month in API costs plus a $1,500 compliance premium understands they are paying for the privacy infrastructure, not for a more expensive version of the same API.

It also works during early-stage engagements where the client wants to experiment with AI without committing to a fixed subscription. "Pay for what you use, plus our management fee" is a low-friction way to start a relationship.

**The risk**: Margins are thin and structurally capped. If you are marking up API costs by 30%, your gross margin on a $10,000 monthly API spend is $3,000. Out of that $3,000 you need to cover your engineering time, support, infrastructure, and sales costs. At the typical EU IT services cost structure, you need a substantial number of clients to make this model viable as a standalone offering.

Worse, the client has a permanent incentive to disintermediate you. Every time they look at their invoice, they see the API cost and the markup as separate line items. When they eventually hire someone who can call an API, you lose the account.

**Mitigation**: Never present token passthrough as your only value. Bundle it with monitoring, cost optimization (you can often reduce their API costs by 30-50% through model routing and prompt optimization), compliance, and support. The markup should be the smallest visible part of a larger service fee.

### 3. Fixed Monthly Retainer

**Structure**: $5,000-25,000 per month covering infrastructure, support, and a defined usage tier.

The retainer model shifts usage risk from the client to you, and in exchange gives you predictable monthly recurring revenue. The client pays a flat fee; you deliver a defined service level including a certain amount of AI capacity, monitoring, support, and regular updates.

**Where it works**: Retainers are the natural pricing model for managed AI infrastructure engagements with enterprise clients. The client wants a budget line item they can plan around. They do not want to think about tokens, GPU hours, or API calls. They want "our AI works, someone competent is making sure it keeps working, and we know what it costs."

A practical structure:

| Retainer tier | Monthly fee | Included capacity | Support level |
|---|---|---|---|
| Standard | $5,000-8,000 | Up to 50 users, standard models | Business hours, 4-hour response |
| Professional | $10,000-15,000 | Up to 200 users, premium models, RAG | Extended hours, 1-hour response |
| Enterprise | $18,000-25,000 | Unlimited users, custom models, full integration | 24/7, 15-minute response for critical |

**The risk**: You absorb usage spikes. If a client on a $10,000 retainer suddenly doubles their AI usage because they rolled out a new internal tool, your costs jump while your revenue stays flat. You can manage this with fair-use clauses and usage caps, but enforcing those caps damages the client relationship.

**Mitigation**: Define usage tiers clearly in the contract, include overage pricing for usage beyond the included tier (at a per-token rate, but positioned as an exception rather than the norm), and build a 20-30% buffer into your pricing to absorb normal variation.

### 4. Project-Based Fee Plus Ongoing Retainer

**Structure**: $20,000-50,000 implementation project plus $3,000-10,000 per month ongoing.

This is the highest total-value pricing model and the one that most naturally aligns with how enterprise AI deployments actually work. There is an upfront phase — discovery, architecture, integration, testing, deployment — followed by an ongoing phase of maintenance, monitoring, updates, and optimization.

**Where it works**: This model is a natural fit for compliance-heavy engagements (Chapter 9), custom RAG implementations, and any deployment that requires significant integration with existing client systems. The project fee covers your intensive engineering effort during setup; the retainer covers the long tail of keeping it running, keeping it compliant, and keeping it current as models evolve.

Example engagement:
- **Phase 1 — Assessment and Architecture** (4-6 weeks): $15,000-25,000. Discovery, data audit, architecture design, compliance gap analysis.
- **Phase 2 — Implementation** (8-12 weeks): $30,000-60,000. Model selection, deployment, RAG pipeline, guardrails, integration with client systems, testing.
- **Phase 3 — Ongoing Management**: $5,000-10,000 per month. Monitoring, model updates, compliance documentation maintenance, support.

Over a 24-month engagement, the total value ranges from $165,000 to $325,000. This is meaningful revenue from a single client, with the ongoing retainer providing the recurring base that makes the business sustainable.

**The risk**: Longer sales cycles. Enterprise procurement for a six-figure engagement involves more stakeholders, more approvals, and more competition than a simple subscription sale. You need to budget 3-6 months from initial conversation to signed contract, and you need a pipeline large enough to absorb the deals that stall or fall through.

**Mitigation**: Start small. Offer the assessment phase as a standalone engagement at $5,000-15,000. This gives the client a low-risk entry point and gives you an opportunity to demonstrate competence before asking for the larger commitment. Most implementation contracts grow from successful assessments, not from cold proposals.

### 5. Outcome-Based and Value-Based Pricing

**Structure**: Price linked to a measurable business outcome — documents processed, tickets resolved, hours saved, accuracy achieved.

This is the model with the highest potential margin and the hardest execution. Instead of pricing your inputs (time, tokens, infrastructure), you price your outputs (business results). If your AI-powered document processing system handles 10,000 invoices per month that previously required 3 full-time employees, you charge based on the value created, not the compute consumed.

**Where it works**: Outcome-based pricing works for mature, well-tested vertical applications where you have high confidence in the solution's reliability and can clearly measure the outcome. If you have deployed the same invoice processing solution for five similar clients and you know it consistently achieves 95%+ accuracy, you can price at, say, $0.50 per invoice processed — delivering clear ROI to the client while capturing margins far above your actual compute costs.

**The risk**: You are betting on your solution's performance. If accuracy drops, if the client's data is messier than expected, if edge cases multiply — you are still committed to the outcome while your costs spiral. You also need robust measurement and attribution: both you and the client must agree on what constitutes a "processed document" or a "resolved ticket," and that agreement needs to survive contact with messy operational reality.

**Mitigation**: Only offer outcome-based pricing for solutions you have deployed at least 2-3 times successfully. Include a pilot period (60-90 days) with traditional time-and-materials pricing before switching to outcome-based. Define the metrics precisely in the contract, including exclusions for edge cases and data quality issues.

## Packaging: The Three-Tier Framework

Individual pricing models work for individual engagements, but building a scalable practice requires packaging — predefined bundles that clients can evaluate, compare, and buy without starting from scratch each time.

The three-tier model is not original, but it is effective. Here is a framework calibrated for EU IT services providers selling GenAI solutions:

| | Starter | Professional | Enterprise |
|---|---|---|---|
| **Target** | SMBs, 10-50 users | Mid-market, 50-200 users | Enterprise, 200+ users |
| **Deployment** | Local AI on existing hardware | Local + cloud hybrid | Full managed AI infrastructure |
| **Models** | Standard open-source models, quarterly updates | Premium open-source + API access, monthly updates | Custom fine-tuned models, continuous updates |
| **Features** | Basic guardrails, standard RAG | Custom guardrails, advanced RAG, document processing | Full compliance suite, custom integrations, analytics |
| **Support** | Email, next business day | 8/5 phone + email, 4-hour response | 24/7, dedicated account manager, 1-hour critical response |
| **Compliance** | Basic documentation | EU AI Act risk assessment, GDPR documentation | Full compliance management, audit support, regulatory liaison |
| **Price range** | $20-40/user/month | $50-80/user/month | $100-200/user/month or custom retainer |
| **Minimum commitment** | Monthly | Annual | Multi-year |

> **Packaging principle**: Never sell "AI hosting" in isolation. The LLM is one component of a vertical solution. Bundle the model with integration, compliance, support, and domain expertise. The bundle is what creates value; the model alone is a commodity.

The tiers serve a dual purpose. They give the client a clear upgrade path (start at Starter, grow into Professional as usage matures), and they give your sales team anchoring (the Enterprise tier at $200 per user makes the Professional tier at $60 look reasonable by comparison).

### Vertical Bundles

Beyond the horizontal tiers, consider packaging vertical solutions for specific industries:

- **"AI-Powered Document Processing for Legal"**: Local model deployment + RAG over case law and precedents + GDPR-compliant data handling + EU AI Act compliance documentation + integration with document management systems. Price: $15,000-25,000 implementation + $8,000-15,000 per month.

- **"Internal Knowledge Assistant for Manufacturing"**: Local model on-premise + safety guardrails for operational procedures + integration with ERP and maintenance systems + multilingual support for factory floor staff. Price: $20,000-40,000 implementation + $5,000-10,000 per month.

- **"Compliant Customer Service AI"**: API proxy with privacy layer + compliance documentation + conversation monitoring and quality scoring + integration with CRM and ticketing. Price: $10,000-20,000 implementation + $5,000-12,000 per month.

Vertical bundles command higher prices because they solve a complete problem. A legal firm does not want "an AI model" — they want a system that helps their associates research case law faster while maintaining client confidentiality. That is a different sale at a different price point.

## Service-Level Price Guide

Beyond packaged products, you will sell professional services. Here are realistic price ranges for the EU market as of 2026, reflecting rates that Central and Eastern European providers can charge while remaining competitive against Western European consultancies:

| Service | Price range | Duration | Notes |
|---|---|---|---|
| **Initial AI assessment** | $5,000-15,000 | 2-4 weeks | Use case identification, feasibility analysis, architecture recommendation. Often the entry point for larger engagements. |
| **Implementation and integration** | $20,000-80,000 | 6-16 weeks | Full deployment including model selection, infrastructure setup, RAG pipeline, integration with client systems, testing. |
| **Fine-tuning engagement** | $10,000-30,000 | 4-8 weeks | Data preparation, fine-tuning runs, evaluation, deployment. Requires ML engineering capability. |
| **Monthly managed service** | $3,000-25,000/month | Ongoing | Infrastructure monitoring, model updates, support, optimization. The recurring revenue engine. |
| **EU AI Act compliance assessment** | $20,000-50,000 | 6-12 weeks | Risk classification, documentation, conformity assessment support. High-value, expertise-intensive. |
| **Training and workshops** | $2,000-5,000/day | 1-5 days | Staff enablement, executive briefings, hands-on technical training. Good relationship builder. |

> **A note on rates**: These ranges assume delivery from Central or Eastern European teams. If you are operating from Western Europe with higher cost structures, adjust upward by 30-50%. The ranges also assume the client is a mid-market or enterprise organization — SMB pricing is typically 30-40% lower.

## Cost Structure and Margin Dynamics

Different pricing models interact differently with your cost structure, and understanding these dynamics is essential for maintaining healthy margins.

**Local deployment model**: High fixed costs during development and setup, low variable costs during operation. Your initial investment in engineering, hardware procurement, and deployment is significant — $50,000-100,000 per client for a full implementation. But once deployed, the incremental cost of serving additional users is minimal. No per-token charges, no API bills that scale with usage. This means your margin improves with scale and time: the longer the engagement lasts and the more users adopt the system, the better your economics get. Per-seat subscription pricing captures this dynamic well.

**API passthrough model**: Low fixed costs (your proxy infrastructure is lightweight), but variable costs that scale linearly with client usage. Every query the client sends costs you tokens, and that cost rises in direct proportion to adoption. Your margin stays roughly flat regardless of scale — you earn your percentage on every dollar of API spend, but you never benefit from the operating leverage that makes the local deployment model attractive. Token passthrough with markup is the honest pricing model here, but the margins are permanently thin.

**Retainer model**: Both your costs and your revenue are predictable month to month, which makes this the easiest model to manage from a financial planning perspective. The risk is in the mismatch between contracted price and actual cost of delivery — if you price the retainer too low relative to the service level required, you eat the difference. Build your retainers with a 25-30% margin buffer above your expected cost of delivery.

| Model | Fixed costs | Variable costs | Margin trend | Best pricing approach |
|---|---|---|---|---|
| Local deployment | High | Low | Improves with scale | Per-seat subscription |
| API passthrough | Low | High (linear) | Stays flat | Token markup + service fee |
| Managed retainer | Medium | Medium | Stable if well-priced | Fixed retainer with tiers |
| Project + retainer | High (front-loaded) | Low (ongoing phase) | High on retainer after payback | Project fee + monthly retainer |

## The Bundling Imperative

If there is one commercial lesson in this chapter, it is this: never sell a component when you can sell a solution.

The AI model is a component. Infrastructure is a component. Compliance documentation is a component. Support is a component. Individually, each of these can be compared to a cheaper alternative or done in-house. Bundled into a solution that solves a specific business problem, they become something the client cannot easily replicate or replace.

Your client does not want to buy an LLM, a RAG pipeline, a compliance audit, and a support contract separately. They want to buy "our legal research is now 3x faster and fully GDPR compliant." Price accordingly.

This means your sales team needs to stop talking about technology and start talking about outcomes. Not "we deploy Llama 4 locally with RAG" but "we make your engineers' knowledge searchable and keep your proprietary data on your premises." Not "we provide EU AI Act compliance documentation" but "we make sure you pass the audit." The pricing follows the positioning: outcome-oriented packaging supports premium pricing in a way that component-level pricing never will.

> **What to take from this chapter**: Your biggest pricing risk is not charging too much — it is being compared to $30/seat consumer AI products. Avoid this by selling solutions, not components. Start new clients with a low-risk assessment ($5,000-15,000), grow into implementation ($20,000-80,000), and anchor long-term relationships with managed service retainers ($3,000-25,000/month). Bundle aggressively. Price on value delivered, not tokens consumed. And remember: the model is your cost of goods sold, not your product.

---

*Next: [Chapter 11 — Talent and Team Structure](11_talent_team.md)*
