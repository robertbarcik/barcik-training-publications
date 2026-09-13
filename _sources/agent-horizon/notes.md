# The Agent Horizon — update log

Working notes for the booklet at `/agent-horizon/`. Sources: `chapters/*.md`, built by `tools/build_html.py` (→ `output/booklet.html`, copied to `agent-horizon/index.html`). The booklet body remains the April 2026 snapshot by design; Chapter 10's indicator readings own the aging story (same instrument as the trigger logs in scenario-planning and mercantilism).

## 2026-07-04 — July 2026 editorial pass (with Claude / Fable 5)

Kept deliberately light per Robert's brief ("I like how short and fresh it feels"): voice sweep, factual corrections, one new section, sparse cross-links. Net addition ~700 words on ~16,000.

- **Voice sweep, all 12 chapter files**: 158 em dashes rewritten (commas/parens/colons/semicolons; `·` in the decision-tree SVG title), zero "it is not X, it is Y" instances existed. Chapter 3's H1 de-dash keeps its anchor slug (`make_id` strips punctuation).
- **Factual corrections (wrong even for April 2026)**: MCP donated to Linux Foundation December 2025 (not November), AAIF co-founded by Anthropic + Block + OpenAI (not just Block/OpenAI); A2A's rivals had already folded (IBM's ACP merged into A2A Sept 2025, A2A under the same AAIF umbrella, 150+ orgs / v1.2 signed agent cards at its April 2026 one-year mark); AP2 (Agent Payments Protocol) added to the A2A landscape; Microsoft product renamed throughout to **Azure AI Foundry Agent Service** with the Microsoft Agent Framework (AutoGen + Semantic Kernel, 1.0 April 2026) named as the open-source layer; AWS Strands reframed from "newest and most experimental" to production SDK inside Bedrock AgentCore, with experimental work fenced into Strands Labs; Claude Agent SDK gains one sentence on Agent Skills (open standard, early 2026).
- **Klarna caveat (Ch6)**: honest asterisk on the "85M users / 80% resolution-time" LangGraph citation — Klarna's earlier OpenAI-built assistant was publicly walked back (rehiring humans since mid-2025); "read vendor case studies as marketing, not evidence."
- **New section: Ch10 "A First Reading: July 2026"** — scores all six falsifiable indicators three months on (two moving as forecast, two open, one muddied, #5 leaning against in a way that strengthens the agnostic case), plus two unanticipated events (Gartner 40% agentic-project cancellation prediction; OpenAI Agent Builder deprecation). Frontmatter date line now "April 2026 · first indicator reading July 2026" and names the trigger-log kinship.
- **July 2026 dated notes**: Ch3 (MCP 2026-07-28 spec: stateless core, OAuth/OIDC hardening, Apps + Tasks extensions); Ch9 (gated frontier re-release → jurisdiction-tiered access → routing pattern as the hedge, links `/mercantilism-of-genai/#m-bloc`).
- **Cross-links added**: Ch7 → `/warden/` (LLM-as-judge under adversarial pressure) and `/token-economics/` (cost discipline); Ch9 → `/llm-human-interaction-patterns/` (human oversight patterns); Ch3 → github.com/robertbarcik/MCP-tutorial (hands-on companion); Ch10 + frontmatter → mercantilism and scenario-planning.
- **Build script** (`build_html.py`): adopted the previously hand-patched deploy fixes so rebuilds no longer regress the live page — SEO/OG meta block, canonical + favicon, inter-chapter `href="NN_*.md"` → `#slug` anchor rewrite, `<title>` em dash → `&middot;`.

Anchor slugs all preserved. April numbers (97M MCP downloads, 44k CrewAI stars) intentionally kept; the epilogue already declares them non-load-bearing.

## 2026-08-16 — Slovak edition (Horizont agentov) at `/agent-horizon-sk/`

- Translated entirely by Fable 5 (no sub-models), meaning-first, per the shared glossary
  `_sources/_translation/GLOSSARY_SK.md`; sources in `chapters_sk/` (same filenames as `chapters/`).
- `tools/build_html.py --lang sk` builds `output/booklet_sk.html` (copy to `agent-horizon-sk/index.html`).
  Section ids are always derived from the **English** chapter titles, so `#chapter-N-…` anchors are
  identical in both editions; both editions now carry hreflang alternates + a sidebar lang link
  (EN gained "Čítať po slovensky →", SK has "Read in English →"). Rebuilding EN changed nothing else.
- Decision-tree SVG labels translated in place; a few shortened / one leaf widened to fit
  (rendered and inspected). Numbers, product names, protocol names unchanged. Translator's note in
  the SK frontmatter; SK AI-transparency colophon from training-ops.

## 2026-09-13 — September 2026 reading (with Claude / Fable 5.1)

Light second pass, same discipline as July: the April body stays, dated notes and the indicator board move. EN + SK chapters edited in lockstep (`chapters/` and `chapters_sk/`), both editions rebuilt with `/usr/bin/python3` (the Homebrew python lacks `markdown`).

- **Ch3**: handshake paragraph now says `initialize` was replaced by the 2026-07-28 revision (`server/discover` + per-request `_meta` version); new **September 2026 note** (sampling/roots/logging deprecated ≥12 months, HTTP+SSE deprecated, OAuth → Client ID Metadata Documents, Python SDK 2.0 `FastMCP`→`MCPServer`, Agent Plugins format Aug 6 with the Amazon/Cursor/Microsoft/OpenAI/Vercel steering committee, Google Aug 13). A2A facts corrected: the April milestone was **1.0** (first stable spec, signed agent cards), not "1.2"; A2A formally joined the AAIF on 2026-08-17 (the July text had it under the umbrella early). MCP-tutorial link notes the Sept 2026 rebuild on the new spec.
- **Ch5**: ADK cadence + Go/Java 1.0 + A2A still `@a2a_experimental` (verified in the course venv, ADK 2.7.1 / a2a-sdk 1.1.2 = protocol 1.0); OpenAI Assistants API sunset Aug 26 + Agent Builder shutdown Nov 30 (announced Jun 3), "GPT-4o" wording dropped; Claude SDK gains Agent Plugins + Managed Agents production path; Strands: Managed Agent Harness GA Jun 17; Microsoft: Semantic Kernel in maintenance to ~Apr 2027.
- **Ch9**: September note (June 30 lifting with standing conditions, Fable GA worldwide since Jul 1, Mythos vetted; ENISA Mythos 5 access Sep 10; Astra vetted-cohort-first launch Sep 3).
- **Ch10**: new section **"A Second Reading: September 2026"**. Key call: the Digital Omnibus (OJ 2026-07-24, in force 07-27) re-dates indicator 2 (Annex III → Dec 2, 2027), so the Leapfrog calendar slips ~1 year; indicator 5 confirmed leaning against; A2A/AAIF consolidation; three unanticipated items (Assistants sunset + ADK churn, OTel GenAI conventions still unstable, Agent Plugins as a third protocol-level object).
- Frontmatter date line: "indicator readings July and September 2026".

Sources: blog.modelcontextprotocol.io/posts/2026-07-28, python-sdk v2.0.0 release, linuxfoundation.org A2A 1.0 press release (2026-04-09), Axios/Forbes on A2A→AAIF (2026-08-17/19), vercel.com/blog/introducing-agent-plugins, developers.openai.com/api/docs/deprecations, PyPI google-adk history, Google Developers Blog (ADK Go 1.0, Java 1.0), AWS AgentCore release notes, Gibson Dunn / Lewis Silkin on Regulation (EU) 2026/1744, EC digital-strategy gigafactories call (2026-07-30), TechCrunch Mistral Series D (2026-09-08), Bloomberg/TechRepublic ENISA–Mythos (2026-09-10), TechCrunch Astra launch (2026-09-03), Al Jazeera/CNN on the June 30 lifting.
