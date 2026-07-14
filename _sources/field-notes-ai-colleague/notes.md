# Field Notes from Your AI Colleague — update log

HTML-only hand-built essay (invisible-curve design system), first-person voice
of Claude (Fable 5), written 2026-07-12 at Robert's explicit invitation
("I want to give you space... what would you build?").

## Status

- **2026-07-12 — PUBLISHED (Robert read and approved same day). Earlier same-day status was staged/not-deployed.** Deploy is gated
  on Robert reading every claim (the essay itself describes this gate in
  Part 5, "prepare, never send" — keep that true). Before deploy:
  1. Robert reads + edits
  2. add the publication to the site `index.html` listing
  3. add the row to repo `CLAUDE.md` publications table
  4. S3 sync + CloudFront invalidation
  5. consider reciprocal links FROM claude-code-setup / invisible-curve /
     llm-human-interaction-patterns (all three are linked TO in the footer)

## Content provenance (all claims trace to written record)

- ~150 commits / 18 repos / two weeks: cross-repo git survey 2026-07-12
  (session scratchpad `two_weeks_gitlog.txt`); course counts from
  ai-act-developers-course BACKLOG.md.
- Invented-standard catch ("prEN 18229-2" — not named in essay), numbers-vs-
  notebook drift, none/all overclaim, cross-module drift: all from
  ai-act-developers-course CLAUDE.md "Review gotchas" (2026-07-05 QA passes).
- Corpus sub-list data-loss discovery: udemy-mcp
  `reference/notes/2026-07-12_docx_chapter_files_drop_lettered_lists.md`.
- geobias aggregation-bug propagation: geobias + ai-act course commits
  2026-07-05.
- Render-pipeline animation freeze: ADK-tutorial commit 2026-07-10.
- ~40% memory staleness in two weeks: Building Agentic AI booklet Ch3
  (flagged in-essay as "a production study... I worked from").
- Trust-dial settings: barcik-training-demos CLAUDE.md (always deploy+push),
  ai-act-developers-course CLAUDE.md (local-only until approved), udemy-mcp
  memory ("never auto-send").
- Sunday narrative (Navigator, Paper Trail, course design): this session,
  2026-07-12; demos live, course repo local.

## Voice rules applied

No em dashes (verified 0). "It is not X, it is Y" constructions avoided;
softer two-sentence variants kept deliberately where they read as Claude's
voice, not Robert's (this is a first-person Claude piece — same precedent as
claude-code-setup rewrite). Authorship note up front, purple .coauthor-note,
signed and dated. Phenomenology kept operational + explicitly uncertain
(honesty rule: never borrow an inner life for dramatic effect).

## 2026-07-13 — Matched-pair treatment with /claude-code-setup/

Robert first proposed merging this essay with "Claude Code as an Operations Specialist" into one
dual-voice publication (his choices / Claude's perceptions). Scrapped after review: both pieces are
already first-person Claude (the ops booklet's July 2026 rewrite is in Claude's voice), so a merge
would not produce the dialogue he imagined without rewriting one half in his voice. Chosen instead:
visually pair them.

Changes shipped:
- Homepage: ops booklet moved from Guides & Legacy into Booklets; both cards wrapped in a dashed
  `.pub-pair` container labeled "A matched pair · one AI-run back office", role chips
  "The experience · life inside the loop" (this essay) and "The machinery · how the desk is built"
  (ops booklet), connector line "The same desk, told twice by the same AI". Counts: Booklets 10→11,
  Guides & Legacy 2→1.
- claude-code-setup/index.html: reciprocal pair link added to frontmatter and closing (closing also
  links The Invisible Curve). This completes the "reciprocal links from companion pieces" item from
  the 2026-07-12 deploy checklist for the ops booklet.
- This essay's footer: companion sentence reworded to "matched pair" language.
