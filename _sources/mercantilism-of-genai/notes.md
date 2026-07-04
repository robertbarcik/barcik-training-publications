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
6. Mechanism 3 — Distribute vs hoard, who holds the dial (dial diagram + stack diagram; market distributes / state hoards; hoarding closes at the nation not the firm; export-the-goods-not-the-factory explains foreign-national scope; Lockheed + Medallion + industrial policy). Plus "Two futures" subsection: who gets armed vs targeted (thinking-vs-moat test; BMW vs EU cybersec; armed↔targeted spectrum diagram); the sovereignty shield and why it's a fuse in adversarial domains (half-life = velocity×severity of harm; defender-not-attacker / Wassenaar; dependency-through-the-breach; three-tier sensitivity diagram; pre-position-or-build). Capstone: a first-person author field report (`.field-note`, teal case-study card) — Robert as the "canary" closest to the factory living the compressed timeline (Copilot training dried up, NotebookLM/Udemy commoditisation, AI spend up 10×, judgment 1%→40%, agnostic-EU-cert demand); flagged n=1.
7. Mechanism 4 — Open is a position, not a principle (Meta / Mistral freemium / China; readable trigger = first closed Chinese frontier; alignment-as-state-control; open weights = un-severability, not freedom)
8. Mechanism 5 — Firm-multipolar, bloc-singleton (bloc diagram; chartered companies; labs as organs: frontier-holder / export-house / own-specie; recall = bloc control of firm asset; bloc-level financing/backstop)
9. Counter-current — Human adaptability (frozen-after-training models; social leak; but adaptation is symmetric — arms race, timescale matters)
10. Synthesis — the phenomenon named; the grammar; mechanism-interactions woven in as fluent prose (rewritten from composite cards per reader feedback that they read too hard), hands off to the dated bets. NOTE: the standalone "Practice / How to read what comes next" section (questions checklist + implications-by-role + EU note) was removed as redundant; its practical content lives distributed across the mechanism trigger-signals, the armed-vs-targeted test in §m-dial, and the dated bets.
11. Trigger log (June 2026 edition, time capsule) + closing note (foresee–watch–adjust)

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

## Update log

### July 4, 2026 — the gated return (trigger log updated)

Status Robert reported (July 2–4): the recall's restoration settled into a gated shape.

- **Mythos**: available only to a small set of vetted companies, primarily American.
- **Fable**: available to anyone, but API-credits-only, expensive, behind a heavy classifier/moderation layer.
- **The frontier has one occupant**: no vendor outside Anthropic offers Mythos/Fable-class capability as of this update (tagged `estimated` in the log, with the honest caveat that a single firm's lead is also just a lead).

Changes made in `index.html` (booklet body kept as June time-capsule; only the parts designed to change were touched):
- Cover meta: "June 2026 · log updated July 2026".
- Trigger log: three new entries — "The gated return" (fired; notes the control line moved from person-nationality to firm-nationality, i.e. redrawn where it can be enforced), "Tiers arrived without a statute" (fired; Mechanism 1's tiering signal, via access policy not law), "The frontier has one occupant" (watching).
- Bet 1: green "Scored · July 2026" strip — won months early, in the gated form it named.
- Mechanism 1 trigger list: capability-tiers signal marked fired (via access policy), pointing to the log.

Cross-booklet consistency: scenario-planning C4 log already records the same gated restoration.

### July 4, 2026 — editorial pass per Robert's approved feedback ("you have my trust")

- **Voice sweep**: all ~130 em dashes and every "it is not X, it is Y" two-sentence tic rewritten
  (commas/colons/semicolons/parens; `·` in labels). Renamed h4 "It is not censorship — and the word
  matters" → "Why 'censorship' is the wrong word". **Exception**: Claude (Opus 4.8)'s signed June
  co-author note kept verbatim (dated, signed time capsule) — the only remaining em dashes in the file.
- **New Mechanism 4 "Armed or targeted: the per-industry sort"** (`#m-armed`): two-futures material,
  spectrum SVG, shield-as-fuse, three-tier stack, and Robert's field note moved out of Mechanism 3;
  fresh thesis/risk cards + 4 dedicated triggers (incl. pre-positioned-dependency and modifiers-hold
  counter-signal). Old M4 (open) → M5, old M5 (bloc) → M6; "Five Mechanisms" → "Six Mechanisms";
  Bet 5's mechanism reference renumbered. Anchor ids unchanged except the new `#m-armed`;
  scenario-planning's armed-vs-targeted link retargeted `#m-dial` → `#m-armed`.
- **Lens chapter hook**: opening promise line before the 1600s history ("Bear with two paragraphs…").
- **Mechanism 2 RSI passage**: honest counterweight added — the follower's derivative is not fixed
  either; the pull-away holds only while the improvement loop stays compute-bound.
- **Second co-author note** added after Opus's, signed by Claude (Fable 5), cyan-bordered
  `.coauthor-note`: writes from the gated side of the return, warns that a frame feels most true when
  events lean its way, and flags its doubled bias (nearest witness, least neutral). Disclaimer,
  section chrome, and nav pluralized ("Co-authors' notes"); root card updated (6 mechanisms,
  ~10,000 words, both signed notes, first bet scored).
