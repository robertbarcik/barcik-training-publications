# The Mercantilism of Generative AI — source notes

**Type:** HTML-only, hand-built booklet (no build script). Canonical source is `mercantilism-of-genai/index.html`.
**Design system:** cloned from `scenario-planning/index.html` (sibling). Same `:root`, fonts (Inter), components, nav/progress script. Chart-rendering scripts dropped (this piece uses static CSS/SVG diagrams). One CSS addition: `.disclaimer-note` (red callout).
**Edition:** June 2026.

## Thesis (the spine)

Frontier intelligence is being reclassified — from a *product* the market wants to distribute into a *strategic national resource* a state wants to hoard for advantage over rivals. The grammar of that reclassification is **mercantilism**: accumulate the scarce input (compute = bullion), wall the means of production (export controls + the kill switch = non-tariff barriers), charter competing national champions (the labs), and export the *finished goods of intelligence* while keeping the *factory* at home. The piece offers a **lens, not a forecast** — a structure for interpreting future events and planning, not predictions. The June 12, 2026 recall of Mythos 5 / Fable 5 is the **dress rehearsal**: the AGI-hoarding question run early, in public, on one narrow capability.

## Section outline

0. Cover
1. Disclaimer (red) — grain of salt; interpretation not reporting; the value is the lens
2. Introduction — the morning it went dark (June 12; foreign-national scope; jailbreak = "read a codebase and fix flaws"; disproportion → look past the stated reason)
3. The Lens — concrete "world under mercantilism" picture (1600s powers, colonies, Navigation Acts, chartered monopolies) FIRST, then the plain primer + mapping table (bullion→compute, goods→outputs, tariffs→export controls/kill switch, chartered companies→labs, "money must move"→export goods/keep factory). Rewritten concrete→abstract for accessibility.
4. Mechanism 1 — Intelligence is a utility, not a product (not censorship → rationing → arms control → licensed critical infrastructure; electricity-as-regulated-utility)
5. Mechanism 2 — The bullion is compute (leak vs controllable diagram; AC/DC disanalogy = capital not knowledge; efficiency acid; RSI acts on the derivative, compute-gated)
6. Mechanism 3 — Distribute vs hoard, who holds the dial (dial diagram + stack diagram; market distributes / state hoards; hoarding closes at the nation not the firm; export-the-goods-not-the-factory explains foreign-national scope; Lockheed + Medallion + industrial policy). Plus "Two futures" subsection: who gets armed vs targeted (thinking-vs-moat test; BMW vs EU cybersec; armed↔targeted spectrum diagram); the sovereignty shield and why it's a fuse in adversarial domains (half-life = velocity×severity of harm; defender-not-attacker / Wassenaar; dependency-through-the-breach; three-tier sensitivity diagram; pre-position-or-build).
7. Mechanism 4 — Open is a position, not a principle (Meta / Mistral freemium / China; readable trigger = first closed Chinese frontier; alignment-as-state-control; open weights = un-severability, not freedom)
8. Mechanism 5 — Firm-multipolar, bloc-singleton (bloc diagram; chartered companies; labs as organs: frontier-holder / export-house / own-specie; recall = bloc control of firm asset; bloc-level financing/backstop)
9. Counter-current — Human adaptability (frozen-after-training models; social leak; but adaptation is symmetric — arms race, timescale matters)
10. Synthesis — the phenomenon named; the grammar; three composite cards (compute×bloc, efficiency×open, hoard×adaptability)
11. Practice — "questions to ask of any future event" checklist + implications by role (individual / enterprise / nation / everyone) + EU note
12. Trigger log (June 2026 edition, time capsule) + closing note (foresee–watch–adjust)

## Static diagrams (CSS/SVG, non-interactive)

1. The dial (market ↔ state) with era markers — §6
2. The stack (goods exported / factory home / bullion held) — §6
3. Leak vs controllable (weights/talent/algorithms/level leak; compute holds) — §5
4. Firm-multipolar / bloc-singleton map — §8

## Sources & frames

- **Primary:** Anthropic, "Statement on the US government directive to suspend access to Fable 5 and Mythos 5" — https://www.anthropic.com/news/fable-mythos-access
- **Corroboration:** CNBC (2026-06-12), 9to5Mac (2026-06-12), The Week (2026-06-13)
- **Companion:** Scenario Planning for Generative AI, Current 4 (Sovereignty) — `/scenario-planning/`
- **Concept:** Wikipedia, "Mercantilism"
- **Analogy frames:** 1990s Crypto Wars / ITAR classification of encryption; 2013 Wassenaar Arrangement "intrusion software" controls (defender-not-attacker pathology); AC vs DC current; AlphaFold released as a controlled scientific commons; Renaissance Technologies' Medallion fund; the complementary-assets / "profiting from innovation" theory of value capture (Teece); industrial policy (MITI; contemporary Chinese champion strategy); EU tariffs on Chinese EVs (slow-half-life shield vs fast-half-life cyber shield)

## Epistemic tagging convention (same as sibling)

- `tag-reported` — actually happened / from a published source
- `tag-speculation` — author's interpretation or inference; not established fact

## Origin

Written by Robert Barcik in conversation with Claude (Opus 4.8), June 2026, in the days after the recall — itself a sequel to *Scenario Planning for Generative AI*, co-written with Fable the day before the recall.
