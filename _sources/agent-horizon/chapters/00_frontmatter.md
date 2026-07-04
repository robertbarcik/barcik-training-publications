# The Agent Horizon

## A Strategic Guide to the Enterprise Agent Development Stack

---

**April 2026 &middot; first indicator reading July 2026**

*By Robert Barcik*

*LearningDoe s.r.o.*

*Contact: [robert@barcik.training](mailto:robert@barcik.training)*

---

### About This Booklet

Every few weeks, a new agent framework launches. A new protocol gets announced. Another vendor SDK promises to make things easier. For an engineer or business stakeholder planning a 2026–2028 roadmap, the signal-to-noise ratio is terrible, and the stakes are high.

This booklet is a conceptual map, not a feature comparison. Its goal is to help you see **what sits where** in the emerging agent stack, **why each layer exists**, and **how the pieces will most likely play out** over the next two to three years. The scaffold is an analogy you already know: the cloud transition. The parallels aren't perfect, but mapping agent primitives onto familiar cloud concepts gives you a mental model that survives the next rebranding cycle.

When you finish, you should be able to answer four questions with confidence. What is MCP, and why does everyone treat it as settled? What's the real difference between Google ADK, the OpenAI Agents SDK, the Claude Agent SDK, and LangGraph? And when does each make sense? Where does the lock-in live, and how much should you care? And for a European enterprise specifically, is the sensible bet to ride the vendor wave first and worry about portability later, or to invest in agnostic infrastructure now?

The booklet closes with a worked case study: a regulated European bank resolving the 5-question framework into a specific stack (including the one decision where the framework said one thing and we did another, and why that was right).

No hype. No breathless predictions. Just a map and a specific example.

### Who This Booklet Is For

- **Enterprise engineers** evaluating agent frameworks for production deployment
- **Architects** designing multi-agent systems that need to outlive a single vendor
- **Technology leaders** shaping a 2026–2028 roadmap
- **Business stakeholders** trying to understand what their engineers are arguing about

If you've heard the terms *MCP*, *ADK*, *LangGraph*, or *A2A* used in conversation and nodded along while quietly wondering which is a protocol and which is a framework, this booklet is for you.

### How to Read It

Chapters 1 and 2 set up the mental model. Read these first even if you're deep in the space. Chapter 3 covers the two settled protocols (MCP and A2A). Chapter 4 introduces the orchestration layer; Chapters 5 and 6 survey its two families (vendor and agnostic). Chapter 7 addresses observability. Chapters 8 through 10 cover strategy: lock-in, EU angle, timeline. Chapter 11 brings it all together with a decision framework, a worked bank case study, and a short epilogue.

Chapter 10 made its forecast falsifiable with six named indicators; this edition adds a dated first reading of them (July 2026). The rest of the text remains the April snapshot, the same discipline our [scenario-planning](/scenario-planning/) and [mercantilism](/mercantilism-of-genai/) booklets follow with their trigger logs.

---

### Table of Contents

1. The Cloud Parallel
2. The Layer Cake
3. The Protocol Layer: MCP and A2A
4. The Orchestration Layer
5. The Vendor Frameworks
6. The Agnostic Frameworks
7. Observability, Evaluation, and Cost
8. The Lock-In Question
9. The EU Angle
10. Will the Timeline Actually Squeeze?
11. Picking Your Stack: with a Worked Case
