---
name: adversarial-review
description: Mode B, Stage 6. Launch the independent adversarial-reviewer agent in a fresh context to stress-test an idea under deep validation: the strongest case against it, and the strongest case for it. Not used in brainstorming.
---
1. Confirm the evidence files exist: `existing-solutions.md`, `competitor-analysis.md`, `market-research.md`, `commercial-analysis.md`, `sources.md` (some may be marked skipped after a Gate-2 reject).
2. Launch the `adversarial-reviewer` agent (not a fork, so it does not inherit this conversation's narrative). The prompt contains only: the slug; the packet path; the specialists' output files to challenge; the mode (`full`, or `inverse-check` after a Gate-2 reject); the allowance (full: 8 research calls; inverse: 4); and the output file `adversarial-review.md`. Do not include the pitch, your own opinion or your draft verdict. That keeps the review independent, and it challenges conclusions rather than redoing the research.
3. When it returns, read `adversarial-review.md`. Every missed competitor or unverified claim it reports must be reflected in the scorecard and verdict.
