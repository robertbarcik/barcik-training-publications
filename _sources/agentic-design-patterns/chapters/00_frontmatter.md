# Building Agentic AI

## Design Patterns from Production

---

**April 2026**

*By Robert Barcik*
*LearningDoe s.r.o.*

---

### About This Booklet

In late March 2026, an inadvertent source map inclusion in an npm package exposed the complete, unobfuscated source code of Anthropic's Claude Code --- approximately 513,000 lines of TypeScript across nearly 1,900 files. This was not a research prototype or a conference demo. It was a production-grade AI coding agent serving millions of developers daily.

This booklet extracts the architectural patterns from that codebase and translates them into practical guidance for anyone building their own AI agents. The patterns are what matter. They will outlast any single product.

Each chapter teaches one design pattern. The structure is consistent: we explain the problem the pattern solves, show how it was implemented in production, discuss the tradeoffs, and provide concrete guidance for applying it in your own systems. No hype, no hand-wringing about the leak itself --- just the engineering and what it means for your work.

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
