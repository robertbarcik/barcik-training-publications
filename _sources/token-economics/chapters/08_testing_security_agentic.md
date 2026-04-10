# Chapter 8: Business Model: Testing, Security, and Agentic Infrastructure

The previous two chapters examined business models built around a single core capability — the privacy proxy in Chapter 6, local model deployment in Chapter 7. This chapter covers three related opportunities that share an important characteristic: they are emerging as distinct service categories that enterprises will need but cannot easily build internally.

Testing and validation, GenAI-specific security, and agentic infrastructure each represent high-margin work for providers who invest in the right skills early. They span a wide range of difficulty, time to revenue, and alignment with existing IT services capabilities. The common thread is that none are about running models. They are about everything that surrounds the model — the evaluation, the protection, and the plumbing that makes AI systems work in production.

---

## Testing and Validation

The EU AI Act entered into force in August 2024, with obligations phasing in through 2027. For IT services providers, the most commercially significant requirement is conformity assessment for high-risk AI systems — and the ongoing monitoring that follows.

### What the Regulation Requires

High-risk AI systems must undergo conformity assessments before deployment, evaluating accuracy, robustness, cybersecurity, transparency, human oversight, and non-discrimination. These are not one-time events. The Act requires continuous monitoring: detecting drift, identifying emerging biases, and documenting everything.

This is not a checkbox exercise. Testing for distributional bias across protected characteristics, evaluating robustness against adversarial inputs, and measuring calibration under real-world conditions goes well beyond what most enterprises can staff internally.

### The Economics

| Service | Price Range | Frequency |
|---|---|---|
| Initial conformity assessment | $20,000 - $50,000 per system | One-time (per deployment) |
| Ongoing monitoring and evaluation | $3,000 - $10,000/month per system | Continuous |

A provider with 20 clients, each running two to three high-risk AI systems, generates $120,000 to $300,000 in initial assessments and $1.4 to $7.2 million annually in ongoing monitoring. The margins are high — the primary cost is skilled labour, not infrastructure.

### The Talent Problem

This is not traditional IT operations work. Proper AI testing requires people who understand ML evaluation methodology — not just "run the test suite" but the statistical reasoning behind why certain approaches are valid and others are misleading. You need people who can design adversarial test cases, determine whether a 2% accuracy difference across demographic groups is noise or systematic bias, and navigate the fact that different fairness definitions are often mutually exclusive.

This is research and engineering talent. These people are scarce, expensive, and currently employed at AI labs, universities, and the handful of companies with dedicated AI safety teams. Recruiting them requires a compelling pitch — interesting work, competitive compensation, and genuine commitment to building a practice.

> **Key economics:** Testing and validation offers the highest margins and the highest barriers of the three opportunities in this chapter. Budget 12-18 months from initial investment to meaningful revenue. The regulatory demand is certain — the EU AI Act is law. The question is whether you can build the team fast enough to capture it.

---

## GenAI-Specific Security

If you run a security practice today, you have a head start — but a smaller one than you might think. GenAI security is a distinct discipline. The threat surface is different, the attack vectors are novel, and the defensive tools are still maturing.

### The Threat Landscape

GenAI systems are vulnerable to traditional security threats plus a set with no direct analogue in conventional IT:

**Prompt injection** — an attacker crafts input that causes the model to ignore its instructions and follow the attacker's instead. This is a structural property of how language models process instructions and data in the same channel. Defences exist but none are complete.

**Data exfiltration through outputs** — a model inadvertently reveals training data, RAG context, or system prompts in its responses. Carefully constructed queries can coax a model into surfacing internal documents, confidential instructions, or patterns from fine-tuning data.

**Model poisoning via fine-tuning** — fine-tuning data introduces malicious behaviour. A poisoned model might behave normally on most inputs but produce subtly wrong outputs in attacker-chosen scenarios. Detection requires evaluation beyond standard accuracy metrics.

**Supply chain risks with open-source weights** — the AI equivalent of dependency vulnerabilities. When you download a model from Hugging Face, you trust that weights have not been tampered with and training data was not poisoned. The open-source AI ecosystem lacks the maturity of tools like npm audit or Dependabot.

**Jailbreaking** — bypassing safety guardrails to produce harmful or policy-violating outputs. New techniques emerge faster than providers can patch them.

### Security Audits and Red-Teaming

A security audit for a GenAI deployment covers prompt injection resistance, data leakage testing, access control, logging adequacy, and policy alignment. A mid-complexity audit runs $15,000 to $40,000.

Red-teaming is more intensive — a dedicated team spends days or weeks attempting to break the system through adversarial inputs, extraction attacks, and exploitation of tool-use capabilities. Red-teaming engagements run $30,000 to $80,000 and are increasingly expected in regulated industries.

### The Skills Transfer

Your existing security engineers understand threat modelling, attack surfaces, and defence in depth. That foundation transfers. What does not transfer is the specific knowledge of how language models fail — the mechanics of prompt injection, statistical methods for detecting data leakage, evaluation frameworks for model robustness.

Expect a six to twelve month ramp-up. This is faster than building testing from scratch because the security mindset — think like an attacker, assume vulnerability, verify rather than trust — is already present. The domain-specific knowledge layers on top.

> **Key takeaway:** GenAI security is a natural extension of existing security practices, but requires significant new technical knowledge. The threat surface is genuinely different, and the tools are still immature. Providers who invest in upskilling their security teams now will own a market that every enterprise deploying AI will need to buy from.

---

## Agentic Infrastructure as a Service

Of the three opportunities, agentic infrastructure is the most accessible for IT services providers — and most likely to generate revenue within the first year.

### The Shift to Agentic AI

Enterprise GenAI is moving beyond simple prompt-response interactions toward tool use, multi-step workflows, autonomous agents, and orchestration layers. The model itself — Claude, GPT-4o, Gemini, or open-source — is just one component. Increasingly, it is the least differentiated component.

The value is in everything around the model:

**MCP servers** (Model Context Protocol) provide standardized interfaces between AI models and external data sources, tools, and services. Building and maintaining MCP servers for enterprise environments — connecting models to databases, document repositories, ticketing systems, CRM platforms — is integration work that IT services providers have done for decades in a new protocol.

**RAG pipelines** require document ingestion, chunking strategies, embedding model selection, vector database management, and continuous evaluation of retrieval quality. A RAG pipeline that works in a demo and one that works reliably in production with millions of documents are entirely different engineering challenges.

**Tool integrations** give agents the ability to act — creating tickets, querying databases, updating records, triggering workflows. Each integration requires authentication, error management, rate limiting, audit logging, and guardrails preventing unauthorized actions.

**Workflow orchestration** coordinates multiple agents, tools, and data sources into multi-step processes. A customer service agent that looks up an order, checks inventory, initiates a return, updates the CRM, and sends a confirmation is a choreographed sequence of tool uses, conditional logic, and human-in-the-loop checkpoints.

**Guardrails** — input and output filtering, content policies, usage limits, and safety boundaries — are table-stakes infrastructure every enterprise deployment needs.

### Why This Maps to Existing Skills

MCP servers are API integrations. RAG pipelines are data engineering. Tool integrations are systems integration. Workflow orchestration is business process automation. Guardrails are policy enforcement. The specific technologies are new — embedding models and vector databases instead of ETL and relational databases — but the underlying disciplines are the same. Your team that connects Salesforce to SAP can learn to connect Claude to your client's document repository.

The model is just an API call. Your value is the plumbing.

### The Economics

| Phase | Revenue | Duration |
|---|---|---|
| Discovery and architecture | $15,000 - $40,000 | 2-4 weeks |
| Build and deploy | $50,000 - $200,000 | 2-4 months |
| Ongoing management and optimization | $5,000 - $20,000/month | Continuous |

The ongoing management is where recurring revenue lives. RAG pipelines need tuning as document corpora change. Tool integrations need maintenance as APIs evolve. Guardrails need updating as new threats emerge. This is managed services work at higher margins than traditional infrastructure monitoring because the skills are more specialized.

> **Key takeaway:** Agentic infrastructure is the most natural transition for IT services providers. The model is just an API call — your value is in the MCP servers, RAG pipelines, tool integrations, workflow orchestration, and guardrails that make it useful. This maps directly to integration and automation skills you already have.

---

## Multi-Model Management

No serious enterprise will run a single model for all use cases. The emerging pattern:

- **Frontier API models** (Claude, GPT-4o, Gemini) for complex reasoning and customer-facing interactions
- **Smaller API models** (Claude Haiku, GPT-4o mini) for high-volume, lower-complexity tasks
- **Locally deployed open-source models** for sensitive data that cannot leave the organization
- **Fine-tuned models** for domain-specific tasks — medical terminology, legal analysis, industry classification

Each model has different capabilities, costs, latency, data handling guarantees, and update cycles. Managing this complexity across dozens of AI-powered applications is a significant operational challenge.

### The Multi-Cloud Analogy

This is structurally similar to multi-cloud management — a market that has sustained viable businesses for over a decade. The services include:

**Model lifecycle management** — tracking deployments, managing version updates, coordinating migrations when providers deprecate models.

**Evaluation and testing** — when a provider releases a new model version, someone must evaluate whether it performs better or worse on the organization's specific use cases. This requires systematic A/B testing, regression evaluation, and benchmarking against actual workloads.

**Cost optimization** — routing requests to the most cost-effective model that meets quality requirements. Intelligent routing can reduce costs by 30-50% without degrading quality.

**Unified observability** — consistent logging, monitoring, and alerting across all models. When a model produces degraded outputs, you need to detect it regardless of provider.

Multi-model management is the connective tissue tying together agentic infrastructure, testing, and security. Like multi-cloud management, this is a complexity tax that enterprises will pay someone to manage.

---

## The Talent Reality

These opportunities span a wide range of talent requirements, and honesty is critical for planning.

**Testing and validation** requires the scarcest talent: ML evaluation expertise, statistical rigour, and research mindset. Hard to find, expensive to hire, longest to become productive. Budget 12-18 months.

**GenAI security** requires traditional security expertise plus AI-specific knowledge. The security mindset transfers; the AI knowledge is genuinely new. Budget 6-12 months to upskill.

**Agentic infrastructure** is most accessible. API integration, data engineering, workflow automation — these skills already exist. New knowledge (MCP, embeddings, vector databases, prompt engineering) can be learned in three to six months. Budget 3-6 months to first engagements.

**Multi-model management** builds on all three and emerges naturally with experience.

| Opportunity | Key Talent | Ramp Time | Margin | Barrier |
|---|---|---|---|---|
| Testing & validation | ML evaluation, statistics, adversarial testing | 12-18 months | Highest | Highest |
| GenAI security | Security + AI-specific knowledge | 6-12 months | High | High |
| Agentic infrastructure | Integration, data engineering, automation | 3-6 months | Moderate-high | Moderate |
| Multi-model management | Operational + AI breadth | Builds over time | High | Moderate-high |

---

## The Recommendation

Start with agentic infrastructure. Not because it is the most valuable — testing and validation commands higher margins long-term — but because it is the natural transition from what you already do. Your integration engineers can start building MCP servers and RAG pipelines within months. Revenue comes faster because the skills gap is smallest.

Use agentic infrastructure engagements to build credibility and client relationships. As you deploy and maintain AI systems, you will naturally encounter testing, security, and multi-model management challenges — each an opportunity to expand.

In parallel, invest in testing and security:

- **Months 1-6:** Deliver first agentic infrastructure engagements. Designate one to two people to build testing and security expertise. Send security staff to AI-specific training.
- **Months 6-12:** Offer basic AI security audits alongside infrastructure deployments. Pilot testing services with existing clients.
- **Months 12-18:** Launch formal testing and validation practice. Offer EU AI Act conformity assessments. Position multi-model management as a managed services extension.
- **Months 18-24:** All four capabilities operate as an integrated practice. Agentic infrastructure generates client relationships. Testing and security generate the highest margins. Multi-model management generates the stickiest recurring revenue.

> **What to take from this chapter:** Three related opportunities — testing, security, and agentic infrastructure — plus multi-model management offer high-margin services that enterprises cannot easily build in-house. Start with agentic infrastructure because it maps closest to existing skills and generates revenue fastest. Invest in testing and security in parallel — regulatory demand is certain and margins are highest, but talent requirements are steeper and time to revenue is longer. The model is just an API call. Everything around it is your business.

---

*Chapter 9 examines how the same AI you are learning to sell to clients is simultaneously transforming how you deliver your existing services — and why that internal disruption may be the most important strategic challenge you face.*
