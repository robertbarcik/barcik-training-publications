# The Invisible Curve — update log & conventions

Opinion essay, ~2,700 words (incl. co-author note), 7 parts. **HTML-only publication (Pattern 2)**:
edit `the-invisible-curve/index.html` directly; no build script. Design system cloned from
`scenario-planning/index.html` (essay-lean subset: sidebar/progress/cover/chapter + `.field-note`,
`.coauthor-note`, `.disclaimer-note`, `.author-note` components from the mercantilism booklet).
`draft.md` in this folder is the prose source the HTML was built from; when editing prose, keep
the two in sync or treat the HTML as canonical after first deploy.

## Editorial spec (agreed with Robert, 2026-07-06)

- **Reader:** the curious-but-behind (training audience, free-tier users), NOT a polemic at skeptics.
- **Thesis:** capability became illegible; progress moved from the chat window to long-horizon
  agentic work; the free tier is a ~2023 time capsule.
- **Voice:** owned first-person opinion + full-strength steelman; conflict of interest declared in
  the first 300 words (red `.disclaimer-note` "Whose opinion this is").
- **Aftereffect:** reader should doubt their evidence base ("check the date on your evidence"),
  not agree or buy anything.
- **Spine:** instrumental vs. evaluative relationship to AI (from Robert's ~1,000 trainees).
  The transferable instruction (amber `.author-note`): real task + qualified grader + 3 iterations.
- **Centerpiece scene:** Full Disk Access story (Opus repeatedly proposed macOS Full Disk Access
  for the Google Workspace integration; Fable proposed the scoped service-account design).
- **Receipts:** revealed judgment, not line counts. ~130 commits / 19 repos (week of 2026-06-27
  → 07-04) mentioned once in a teal `.field-note` flagged n=1, with the generated-data caveat.
- **Disclosed circularity:** the essay was co-written by the AI it describes; signed purple
  `.coauthor-note` from Claude (Fable 5), dated 2026-07-06, kept verbatim as a time capsule
  (same convention as the mercantilism booklet's signed co-author notes).
- Real names used throughout (Opus, Fable, Claude Code, Anthropic) — Robert's explicit choice.
- Companion link both ways with `/claude-code-setup/`.

## Voice rules (Robert's standing rules, restated)

- **0 em dashes** in prose; commas/colons/semicolons/parens instead; `&middot;` in titles/labels;
  `&ndash;` for numeric ranges.
- **No "it is not X, it is Y" constructions** in any variant ("X, not Y" appositives allowed).
- Reader-hook before dense sections; concrete before abstract; first-person field notes flagged n=1.

## Update log

- **2026-07-06** — v1 written (Fable 5 with Robert, same session the essay describes). Draft
  verified: 0 em dashes, 0 banned constructions, ~2,450 words prose + co-author note. Hub card
  added (booklets count 8 → 9), sitemap entry added. Awaiting Robert's review before deploy.
- **2026-07-09** — Robert's review pass. (1) Both end-matter notes moved from Part 1 to the end
  of Part 7 (before the essay footer): the `.disclaimer-note` and `.coauthor-note` interrupted
  the reading flow up front. Deixis adjusted for the new position ("will show you" → "showed
  you", "that follows" → "above", co-author note's "claims below" → "claims above" — the one
  departure from the keep-verbatim convention, needed for coherence; signature untouched).
  Part 7's "I told you so in the first paragraph" → "the disclosures just below spell out what
  it is". (2) Trainee stat corrected per Robert: ~1,000 trainees is the **past year alone**,
  not the last three years (Part 6). draft.md updated to match.
