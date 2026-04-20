# The Agent Horizon

## A Strategic Guide to the Enterprise Agent Development Stack

---

**April 2026**

*By Robert Barcik*
*LearningDoe s.r.o.*

---

### About This Booklet

Every few weeks, a new framework launches. A new protocol gets announced. A new vendor SDK promises to make building agents easier than ever. For an enterprise engineer or a business stakeholder trying to plan a 2026–2028 technology roadmap, the signal-to-noise ratio is terrible — and the stakes are high.

This booklet is not another comparison table of agent frameworks. It is a conceptual map. Its goal is to help you understand **what sits where** in the emerging agent stack, **why each layer exists**, and **how the pieces will most likely play out** over the next two to three years. We borrow heavily from an analogy you already know: the rise of cloud computing. The parallels are imperfect, but they are close enough that mapping agent primitives onto familiar cloud concepts gives you a mental model that will survive the next wave of rebranding.

When you finish reading, you should be able to answer four questions with confidence. What is MCP, and why does everyone treat it as settled? What is the difference between Google ADK, the OpenAI Agents SDK, the Claude Agent SDK, and LangGraph — and when does each one make sense? Where does the lock-in live, and how much does it matter? And for a European enterprise, is the sensible bet to ride the vendor wave first and worry about portability later, or to invest in agnostic infrastructure on day one?

No hype. No breathless predictions. Just a map you can hand to a colleague.

### Who This Booklet Is For

- **Enterprise engineers** evaluating agent frameworks for production deployment
- **Architects** designing multi-agent systems that need to outlive a single vendor
- **Technology leaders** (CTOs, heads of AI, heads of engineering) shaping a 2026–2028 roadmap
- **Business stakeholders** trying to understand what their engineers are arguing about
- **Consultants and trainers** who need to speak about the agent landscape without oversimplifying

If you have heard the terms *MCP*, *ADK*, *LangGraph*, or *A2A* used in conversation and nodded along while quietly wondering which is a protocol and which is a framework — this booklet is for you.

### How to Read This Booklet

Chapters 1 and 2 set up the core mental model — read these first, even if you are already deep in the space. They will save you arguments later. Chapters 3 and 4 cover the two protocols (MCP and A2A) that sit at the bottom of the stack. Chapter 5 introduces the orchestration layer in general terms, and Chapters 6 and 7 then survey the two families of frameworks sitting at that layer: vendor-first and agnostic. Chapter 8 addresses observability, evaluation, and cost — the topics that tend to be underweighted in framework debates and overweighted in actual procurement meetings. Chapters 9 through 11 cover strategic dynamics: vendor lock-in, the EU angle, and the contested question of how fast the timeline actually squeezes. Chapter 12 offers a decision framework. Chapter 13 closes with durable principles, not a dated roadmap — the landscape will shift before any specific calendar advice survives contact with reality.

The booklet is intentionally conceptual. You will not find code samples here, and the framework comparisons are philosophical rather than line-by-line. Specifics change monthly; mental models change much more slowly.

---

### Table of Contents

1. The Cloud Parallel
2. The Layer Cake
3. MCP: The HTTP of the Agent Era
4. A2A: The Other Protocol
5. The Orchestration Layer
6. The Vendor Frameworks
7. The Agnostic Frameworks
8. Observability, Evaluation, and Cost Governance
9. The Lock-In Question
10. The EU Angle
11. Will the Timeline Actually Squeeze?
12. Picking Your Stack
13. A Pragmatic Horizon
