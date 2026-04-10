# Building Agentic AI

## Design Patterns from Production

---

**April 2026**

*By Robert Barcik*
*LearningDoe s.r.o.*

---

### About This Booklet

In early 2026, the complete source code of Anthropic's Claude Code became publicly available --- approximately 513,000 lines of TypeScript across nearly 1,900 files. Not a research prototype. Not a conference demo. A production coding agent serving millions of developers daily.

This booklet treats that codebase as a case study. We extract the architectural patterns, explain why they exist, and translate them into practical guidance for anyone building their own AI agents. The patterns are what matter --- they will outlast any single product or vendor.

Each chapter teaches one design pattern: the problem it solves, how it works in production, the tradeoffs, and concrete steps for applying it in your own systems. Most chapters include a hands-on exercise you can try with your own coding agent.

### Who This Booklet Is For

- **Software engineers** building AI-powered tools, coding agents, or autonomous systems
- **Technical architects** designing agent orchestration for enterprise environments
- **Engineering managers** evaluating the build-versus-buy decision for agentic infrastructure
- **AI practitioners** who want to move beyond chatbot wrappers toward production-grade agent design
- **Anyone technically curious** about how frontier AI agents actually work under the hood

### How to Read This Booklet

Chapters 1--2 build the foundation --- what production agent architecture looks like and why context management is the central problem. Chapters 3--5 cover the core operational patterns: memory consolidation, tool design, and prompt economics. Chapters 6--7 address calibration and security --- the patterns that determine whether your agent is trustworthy enough to deploy. Chapters 8--9 tackle advanced orchestration and frontier capabilities. Chapter 10 synthesizes everything into three reference architectures you can use as starting points for your own design.

Read in order if you are new to agent architecture. Jump to individual chapters if you are looking for guidance on a specific pattern.

---

### Table of Contents

1. Why Production Architecture Matters
2. The Persistent Context Problem
3. Background Consolidation
4. Tool Design and Constraint Architecture
5. Prompt Architecture and the Cost of Instructions
6. Output Calibration and the Assertiveness Problem
7. Security Architecture for Agentic Systems
8. Multi-Agent Orchestration
9. Frontier Capabilities and Containment
10. Building Your Own Agent --- A Pattern Language
