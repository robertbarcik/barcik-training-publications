# Chapter 10: The Lock-In Power Shift

Every IT services provider understands lock-in. You may not call it that in client meetings — you say "deep partnership" or "institutional knowledge" — but the mechanism is the same. The more entangled your systems become with the client's operations, the harder it is for them to leave. The harder it is for them to leave, the more predictable your revenue.

This chapter is about what happens when that lock-in migrates away from you and toward the model vendors. It is a shift many providers have not fully reckoned with, because the daily work feels familiar even as the power dynamics underneath are quietly rearranging.

---

## The Old World: Lock-In Favored the IT Provider

Let us be honest about how the traditional IT services model actually worked.

A mid-sized European company hires you to manage their infrastructure. Over the first year, you learn their environment — the legacy ERP system that requires a specific JDK version, the VPN configuration that was set up by a contractor who left in 2019, the backup schedule that accounts for a batch job running every Thursday at 3 AM. You document some of this. Much of it lives in the heads of your operations team.

By year two, the client is deeply dependent on you. Not because your technology is superior, but because the switching cost is enormous. A competing provider would need months to understand the environment. The migration risk is real. Your contract renewal conversations are comfortable, because both sides know the alternative is painful.

This was the business moat. The more complex the client's environment, the stickier the relationship. Providers who accumulated institutional knowledge about their clients' systems built durable businesses with high retention rates and healthy margins. The lock-in was not malicious — it was a natural consequence of infrastructure complexity. The client was not locked in because you tricked them. They were locked in because the work was hard, and you were the ones who knew how to do it.

> **The old lock-in formula**: Complexity of the client's environment multiplied by your accumulated knowledge of it equaled switching cost. High switching cost equaled sticky revenue. This was not a side effect of the business model — it was the business model.

---

## The New World: Lock-In Runs Toward the Model Vendors

Now consider what happens when a client's most important technology interaction is not a managed server fleet but an API call to a large language model.

A European logistics company wants GenAI for customer support automation and document processing. A developer writes integration code using OpenAI's function calling format, defines tool schemas in OpenAI's JSON structure, and builds workflows around the Assistants API. The prompts are engineered for GPT-4o's strengths. The evaluation metrics are calibrated against GPT-4o's output patterns.

Lock-in has migrated. The logistics company is now deeply dependent on OpenAI — their tool definitions, their API schema, their model's behavioral quirks. But the IT services provider who helped set this up? Far more replaceable. Another provider could read the API documentation and take over in weeks. The complexity that created switching cost has been abstracted away by the model vendor.

The platform captured the lock-in that used to belong to the middleman.

This shift is structural. In traditional IT, the abstraction layer sat low — close to the hardware. Managing it required deep operational expertise, which is exactly what IT services providers sold. With GenAI APIs, the abstraction is much higher. A competent developer can integrate the OpenAI API in an afternoon. The "we will manage it for you" pitch loses force when the thing being managed is a REST API call, not a multi-server deployment with failover and disaster recovery.

---

## Where Lock-In Now Lives

To understand the new competitive landscape, map where lock-in has migrated. It now lives in the model-specific choices that accumulate as organizations build AI-powered workflows.

**Model-specific prompt engineering.** Prompts that work well with Claude do not necessarily work well with GPT-4o. Organizations that invest months refining system prompts, few-shot examples, and chain-of-thought templates for a specific model have created assets that are partially non-portable.

**Tool and function calling formats.** This is one of the most concrete lock-in vectors. OpenAI's function calling schema differs from Anthropic's tool use format, which differs from Google's function declarations. If a client has built 50 tool definitions in OpenAI's format, migrating to Claude requires more than a format conversion — it requires retesting every tool interaction because different models interpret tool descriptions differently.

**Context window strategies.** An application designed around Claude's 200K context window works differently from one designed around GPT-4o's 128K window. Switching to a model with a smaller effective window means rearchitecting the pipeline — chunking strategies, retrieval augmentation, summarization layers.

**Evaluation pipelines.** Perhaps the most subtle form of lock-in. Organizations that build serious AI applications develop test suites and quality benchmarks calibrated to a specific model's output patterns. Switching models means recalibrating what "good" looks like — expensive, time-consuming, and a source of real organizational resistance.

**Fine-tuning investments.** If a client has invested in fine-tuning a model — curating training data, running training jobs, evaluating iterations — that investment is entirely locked to the provider's platform. A fine-tuned GPT-4o cannot be ported to Claude. The training data might be portable, but the training investment is not.

> **Where lock-in lives now**: It is in prompt libraries, tool schemas, context window architectures, evaluation pipelines, and fine-tuning investments. The more you build around one model, the harder it is to switch. And none of these lock-in vectors benefit the IT services provider in the middle — they all benefit the model vendor.

---

## Defensive Strategies for IT Services Providers

Understanding the power shift is step one. Step two is building a defensible position despite it. The new lock-in landscape creates specific opportunities for providers who think architecturally rather than operationally.

**Abstract the model layer.** This is the single most important architectural decision you can make on behalf of your clients. Build an abstraction layer between the client's application logic and the model provider's API. Tool definitions stored in a provider-neutral format, translated at the integration layer. Prompts templated with model-specific variants. No hardcoded references to `api.openai.com`. When you control the abstraction layer, you control the switching capability — and switching capability is negotiating power.

**Own the integration layer.** Your value is not in the model. It is in connecting the model to the client's business systems — their ERP, CRM, document management, compliance workflows. This integration work is genuinely complex, deeply client-specific, and hard for a competitor to replicate quickly. It creates healthy lock-in that favors you, not the model vendor.

**Build switching capability as a service.** If you can swap Claude for GPT-4o for Gemini within days rather than months, you have something valuable. The client gets resilience against price increases, model deprecation, or quality regressions. You get a defensible position as the provider who ensures vendor independence. The old value proposition reframed: complexity management, but now vendor abstraction rather than server management.

**Own the data layer.** RAG pipelines, knowledge bases, vector databases, fine-tuning datasets — these make AI work in a specific business context. Design them model-agnostic and they become portable assets that you manage. The client depends on your knowledge of their data architecture and embedding strategies. This is the new institutional knowledge — the GenAI equivalent of knowing where the legacy VPN config lives.

**Build evaluation frameworks.** If you can objectively compare model performance for a client's specific use case — measuring quality, latency, and cost across providers — you become the trusted advisor. This is a defensible, recurring advisory relationship that no model vendor can replicate, because the model vendor has an inherent conflict of interest in the comparison.

---

## The Uncomfortable Truth

Let us not sugarcoat this. Defensive strategies are real and valuable, but they do not change the fundamental math for every provider.

Some IT services providers will have fewer clients who need them, regardless of how well they execute. When a solo developer can integrate an LLM API in an afternoon, the pool of clients who need a managed services provider shrinks. Not to zero, but meaningfully.

The "we will manage it for you" pitch requires redefining what "it" means. If "it" is API integration and prompt engineering, the pitch is weak. If "it" is multi-model orchestration, compliance architecture, evaluation frameworks, and ongoing optimization across a portfolio of AI applications — that is a different proposition entirely. But it demands capabilities most traditional IT services providers do not currently have.

The value must shift from "we run your stuff" to "we make AI work in your specific context." That implies understanding the client's business domain, not just their infrastructure. It implies advisory capability, not just operational capability. And it implies willingness to be measured on outcomes rather than uptime.

> **The uncomfortable truth**: The structural simplification of AI infrastructure means some clients will not need an IT services provider at all. The providers who thrive will be the ones whose value clearly exceeds what the client can do with an API key and an afternoon of reading documentation.

---

## The Opportunity in Abstraction

There is a genuine, defensible business in being the layer between organizations and model vendors — but it looks nothing like traditional infrastructure management.

**Multi-model orchestration as a service.** Route different request types to different models based on complexity, cost, and quality requirements. A customer support chatbot handling routine questions uses a fast, cheap model. The same system escalating to complex reasoning dynamically routes to a more capable model. Building and operating this routing layer — with quality monitoring, cost tracking, and continuous optimization — is real, recurring work.

**Vendor management and cost optimization.** When a client uses three model providers across a dozen applications, someone needs to track spend, negotiate enterprise agreements, monitor rate limits, and detect when a provider's price change or model update breaks a workflow. This is procurement and operations expertise applied to a new domain.

**Model evaluation and selection.** The model landscape changes quarterly. A provider who maintains current benchmarks across models for common enterprise use cases — and can advise clients on when to switch, when to stay, and when to hedge — provides ongoing strategic value.

These services share a characteristic: they are more valuable the more model providers exist and the faster the market moves. In a world with five or six competitive providers releasing new models every quarter — which is the world we are in — the complexity of navigating the landscape is itself a source of value.

> **The opportunity**: The same market fragmentation that threatens your old business model creates demand for your new one. Multi-model complexity is the new infrastructure complexity. If you can manage it, you have a business.

---

## From Passive to Active Indispensability

In the old model, you were indispensable because leaving you was painful — passive lock-in. In the new model, you must be indispensable because the alternative is worse — the client managing multi-model orchestration, evaluation, compliance, and optimization on their own. This is active indispensability: the client stays because your contribution is visible and measurable, not because switching is hard.

Active indispensability is harder to build but more durable. It depends on expertise the client can see and value, not on information asymmetry. The providers who internalize this earliest will have a significant head start — not because the work is impossibly complex, but because the transformation from infrastructure operators to intelligence advisors takes time. The window is open now.

---

*Next: [Chapter 9 — EU AI Act: Your Compliance Opportunity](09_eu_ai_act.md)*
