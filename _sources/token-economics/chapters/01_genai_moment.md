# Chapter 1: The GenAI Moment for IT Services Providers

---

## A Business That Made Perfect Sense

For twenty years, the math worked beautifully.

A mid-sized European IT services provider — the kind with 50 to 500 employees, operating from Prague or Bratislava or Warsaw or Munich — built its business on a layered proposition. At the base: hosting and infrastructure services generating steady recurring revenue. On top: professional services — architecture consulting, systems integration, security audits, compliance work — where the real margins lived.

This distinction matters. Many IT services providers make 30-60% gross margins on professional services and consulting, while infrastructure hosting runs at 15-30%. The hosting was often the anchor that got you into the client relationship; the services revenue was what made the business profitable. A typical portfolio included co-location and hosting, managed infrastructure operations with SLAs, cloud migration projects, and a growing layer of advisory and integration work on top.

This model was resilient. When the cloud wave hit in the early 2010s, providers adapted. Instead of selling physical server space, they resold cloud capacity from AWS, Azure, or Google Cloud, adding management, migration, and optimization services on top. The infrastructure margins compressed, but the services layer expanded — cloud architecture consulting, cost optimization, multi-cloud management. The total economics still worked.

When the mobile revolution came, it barely touched the core business. Mobile apps needed backends. Backends needed hosting. The cycle continued.

Even the shift to DevOps and containers, while demanding new skills, did not fundamentally threaten the model. Kubernetes clusters need to run somewhere. Someone needs to operate them. The value chain shifted, but the underlying logic — *we operate infrastructure so you don't have to* — remained intact.

This is no longer the case.

## Why GenAI Breaks the Middleman Model

Every previous technology shift preserved a basic economic structure: the IT services provider sat between the technology vendor and the client, adding value by reducing complexity and providing operational expertise. The provider's margin came from the difference between what they paid for compute and what they charged clients for managed compute.

Generative AI inverts this structure, and understanding why requires looking at how the economics actually work.

When you resell cloud hosting, you buy compute at a bulk rate and sell it at a markup. A virtual machine that costs you EUR 200 per month from a hyperscaler might go to your client at EUR 300-350 with management included. The client pays the premium willingly because they are buying your operational expertise, your monitoring, your SLA guarantees — your human labour wrapped around the compute.

Now consider what happens with large language models. The leading API providers — OpenAI, Anthropic, Google, Mistral — operate at scales that produce extraordinary unit economics. A million tokens processed through a capable mid-tier model like Gemini 2.5 Flash costs $0.30 on input and $2.50 on output through the API. A flagship model like Claude Opus 4.6 costs $5.00 per million input tokens and $25.00 per million output tokens. These prices have been falling steadily and show no signs of stopping.

Here is the uncomfortable arithmetic. If you wanted to self-host a comparable open-source model — say, a 120-billion parameter model running on your own GPU infrastructure — the hardware alone for serving 100 concurrent users would cost between $600,000 and $1.2 million to purchase. Renting the equivalent cloud GPU capacity runs $25,000 to $50,000 per month. And that is before you account for the ML engineering talent to operate it, the inference optimization work, the model updates, and the inevitable hardware refresh cycle.

For most workloads at most scales that EU IT services providers operate at, the API is 5 to 10 times cheaper than self-hosting. Not slightly cheaper. Not marginally cheaper. Dramatically, structurally cheaper.

> **The core problem**: In traditional IT services, the middleman was cheaper than the vendor because the middleman aggregated demand. In GenAI, the vendor is cheaper than the middleman because the vendor aggregates supply at a scale no middleman can match.

This is not a temporary market condition. It is a structural consequence of how large language models work. Training a frontier model costs hundreds of millions of dollars, but once trained, the marginal cost of serving one more request is tiny — and it gets tinier as the provider's infrastructure scales. The hyperscalers who train and serve these models operate at a scale where they have already amortized their training costs across millions of paying users. You cannot replicate that cost structure with a rack of GPUs in a Frankfurt data centre.

## Two Kinds of Clients, Two Different Realities

Before concluding that the old model is dead, we need to make an important distinction. Not all clients are the same, and the economics play out very differently depending on which kind you serve.

**Cloud-comfortable clients** can send data to external APIs. They may have some data governance policies, but their core business data is already in AWS or Azure. For these clients, the middleman economics described above apply in full force. They can sign up for an OpenAI API key tomorrow, and the case for your self-hosted infrastructure is a hard sell on price.

**On-premises-required clients** cannot or will not send data to external API providers. This includes banks under strict regulatory frameworks, healthcare providers handling patient data, defense contractors, public sector organizations, law firms with client confidentiality obligations, and any enterprise whose compliance or legal teams have drawn a hard line against external AI APIs. For these clients, the hyperscaler API price is irrelevant — it is not an option they can choose.

This distinction matters enormously, because for on-prem clients, the economic comparison is not "your self-hosted price vs. the API price." It is:

- Your managed AI service vs. the client building their own GPU infrastructure and hiring their own ML team
- Your managed AI service vs. the client having no AI at all

That is traditional IT services economics. And it works. A client who needs on-prem AI and does not have the expertise to run it themselves will pay a reasonable premium for your operational expertise — just as they did for managed servers, managed databases, and managed Kubernetes clusters.

The proportion of your client base that falls into each category will determine how much of your traditional business model survives the GenAI shift. In heavily regulated EU markets — particularly Central and Eastern Europe, where banking, insurance, healthcare, and public sector clients often have strict data residency requirements — the on-prem segment may be larger than you think.

> **Key distinction:** For cloud-comfortable clients, the API providers are 5-10x cheaper than you, and the middleman model is broken. For on-prem-required clients, you are not competing with API providers — you are competing with the client's alternative of doing it themselves or going without. These are two fundamentally different economic games, and you need to know which one you are playing with each client.

We explore both sets of economics in detail in Chapter 3. For now, understand that the picture is more nuanced than "self-hosting never works." It depends entirely on who you are serving and why.

## The Previous Playbook Does Not Transfer (For Half Your Clients)

IT services providers have survived technology transitions before, and there is a tempting pattern to fall into: "We adapted to cloud. We adapted to containers. We will adapt to AI."

For cloud-comfortable clients, this confidence is misplaced. GenAI is not primarily a new infrastructure category — another thing to host, another thing to manage. The infrastructure layer is increasingly commoditized by the model providers themselves. OpenAI, Anthropic, and Google do not just sell models — they sell fully managed inference infrastructure. There is no server for you to manage. There is no cluster for you to optimize. The client can sign up for an API key in five minutes and start sending requests.

For on-prem-required clients, however, the adaptation instinct is actually correct. These clients still need someone to procure GPU hardware, deploy models, optimize inference, handle updates, and monitor production systems. This is operational expertise wrapped around infrastructure — exactly the service you have been selling for decades. The technology changes (GPUs instead of CPUs, vLLM instead of Apache), but the relationship is the same: you operate complex infrastructure so the client does not have to.

The challenge is that even for on-prem clients, the skill requirements have shifted. Managing GPU clusters and ML inference pipelines is different from managing virtual machines and databases. We cover this transition in detail in Chapter 11.

### What the client actually needs now

The real challenges clients face with GenAI are different from what they faced with cloud or mobile:

- **Which model do I use for which task?** The landscape changes monthly. A model that was best for code generation six months ago may now be outperformed by three competitors at half the price.
- **How do I keep my data private?** Many European organizations, especially in regulated industries, cannot send customer data to US-based API providers without careful architectural work.
- **How do I integrate AI into my existing workflows?** This is not an infrastructure question — it is a systems integration and business process question.
- **How do I evaluate quality?** Unlike a web server that either responds or does not, an LLM can produce subtly wrong, biased, or hallucinated output. Testing and validation require entirely new approaches.
- **How do I comply with the EU AI Act?** The regulatory requirements for deploying AI systems in Europe are real and growing, and most clients have no idea where to start.

Notice what these questions have in common: none of them are primarily about hosting or infrastructure. They are about expertise, integration, evaluation, and compliance. This is the shift — from selling compute to selling intelligence about intelligence.

## The Five-Year Question

Here is the question every IT services provider leadership team in Europe should be sitting with right now:

> **In five years, will your primary revenue come from infrastructure you operate, or from expertise you deliver?**

This is not a rhetorical question, and the answer is not obvious. Both paths can work, but they require fundamentally different investments, different talent, different client relationships, and different pricing models.

The infrastructure path is broader than many commentators suggest — particularly in the European market. Regulated industries that cannot use external APIs, organizations with strict data sovereignty requirements, high-volume workloads where the cost curve tips in favour of owned hardware, and edge deployment scenarios all represent real demand for managed AI infrastructure. In some EU markets, this segment may represent the majority of enterprise AI demand. We examine these economics in detail in Chapters 3 and 4.

The expertise path is broader but demands transformation. If your organization pivots toward AI advisory, integration, testing, compliance, and managed intelligence services, the addressable market is large and growing. But this is a different business than the one you have been running. It requires different people, different sales motions, and a willingness to let go of the comfortable predictability of infrastructure-based recurring revenue.

Most providers will end up with some combination of both. The question is which one leads.

## There Are Viable Paths — But Not the Old One

Let us be direct about what this booklet is and is not arguing.

We are not arguing that EU IT services providers are doomed. The European IT services market is large, growing, and shaped by regulatory and cultural factors that create genuine competitive advantages for local providers. Data sovereignty concerns, EU AI Act compliance requirements, language and cultural specificity, and the sheer complexity of integrating AI into existing enterprise workflows — these all create demand that hyperscalers alone cannot satisfy.

We are also not arguing that every provider must become an AI company overnight. The transformation is a spectrum, and the right position on that spectrum depends on your current capabilities, your client base, and your appetite for risk.

What we are arguing is this: **the old playbook needs fundamental modification — but not wholesale abandonment.** For cloud-comfortable clients, selling compute at a markup does not work against hyperscaler API prices. For on-prem-required clients, managed AI infrastructure is a natural and profitable extension of your existing business. For both, adding expertise, integration, compliance, and evaluation services on top of the infrastructure creates significantly more value than the infrastructure alone.

Providers who recognize the dual nature of this market — and invest accordingly — have a window of opportunity. The GenAI market is still young enough that expertise is scarce, best practices are not yet established, and clients are genuinely uncertain about how to proceed. That uncertainty is your opportunity. For some clients, it means "we will host it for you, because you cannot go to the cloud." For others, it means "we will make AI work in your context, regardless of where the model runs."

## What This Booklet Will Show You

The chapters that follow build the case systematically.

**Chapters 2-4** lay the economic foundation. We walk through how large language models actually run at the hardware level, then build a detailed cost comparison between self-hosting and API usage at different scales — for both cloud-comfortable and on-prem-required clients. We explain why the hyperscaler cost advantage is structural, not temporary, and identify where self-hosting still makes economic sense.

**Chapter 5** examines the path of least resistance: reselling and implementing embedded AI from your existing vendor partners — Microsoft Copilot, SAP Joule, ServiceNow AI, and others. For many providers, this is the fastest route to AI revenue.

**Chapters 6-8** explore three more independent business models: the Privacy Proxy (routing AI through a compliant European layer), Local Deployment on Employee Devices (a growing market as on-device models improve), and Testing, Security, and Agentic Infrastructure (where the provider's operational expertise maps directly to new AI requirements).

**Chapter 9** addresses the uncomfortable internal question: how AI transforms your own service delivery model. If AI can handle 40-60% of L1 tickets, that changes your cost structure, your staffing, and your pricing.

**Chapters 10-14** cover the broader strategic landscape: how lock-in dynamics are shifting, how the EU AI Act creates a genuine compliance opportunity, how to price and package AI services, where to find talent in the Central and Eastern European market, and what happens if you do nothing. The final chapter provides a concrete 18-month roadmap.

Throughout, we use real numbers. The pricing data referenced in this booklet is current as of April 2026 and drawn from public pricing pages, published GPU rental rates, and hardware market prices. Where we estimate, we show our assumptions. Where the numbers are uncertain, we say so.

> **What to take from this chapter**: The GenAI shift creates two distinct realities. For cloud-comfortable clients, the API providers are 5-10x cheaper than you at serving AI — the middleman markup model is broken. For on-prem-required clients, managed AI infrastructure is a viable, profitable business that builds on your existing expertise. Most EU IT services providers will serve both segments, and the winners will be those who understand which economic game they are playing with each client. The rest of this booklet gives you the numbers and the strategies for both.

---

*Next: [Chapter 2 — How Large Language Models Actually Run](02_how_llms_run.md)*
