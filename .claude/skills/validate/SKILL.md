---
name: validate
description: Run the remaining validation stages (3 to 7) for an idea that passed the Stage 2 kill-check. Staged and budgeted, uses specialist agents only where they add value, and ends with an adversarial review and a verdict.
---
Preconditions: Gate 2 is passed and written in `ideas/<slug>/README.md`. If not, run `/kill-check` first.

1. **Stage 3:** finish `competitor-analysis.md`. Do it inline if Stage 2 already found the players; otherwise use the `market-researcher` agent (budget 10 searches). Gate 3: a defensible opening in one sentence with evidence, or REJECTED.
2. **Stages 4–5:** run the `commercial-analyst` agent with the slug and budget. Gate 4: level-3/4 demand evidence, or stop at NEEDS MORE RESEARCH with the cheapest test named. Gate 5: a named payer and a price, or REJECTED / NEEDS MORE RESEARCH.
3. **Technical:** run the `technical-researcher` agent only if custody, admin keys, closed programs or audit needs could change the verdict. It may run in parallel with step 2 once Gate 3 has passed. Never more than two agents at once.
4. **Stage 6:** run the `adversarial-reviewer` agent in a fresh context (see `/adversarial-review`). Required before CONDITIONAL or VALIDATED.
5. **Stage 7:** fill in `scorecard.md` with source IDs and run `python3 tools/ir.py score <slug>`. Write `final-verdict.md` at or below the ceiling. Where you disagree with the reviewer, cite the evidence that settles it; if nothing settles it, the lower verdict stands. CONDITIONAL needs kill tests with thresholds and dates.
6. Run `python3 tools/ir.py lint <slug>` and fix any problems. Update `ideas/INDEX.md` and `research/INDEX.md`, and copy reusable findings into `research/`. If REJECTED, add it to `research/failed-ideas/README.md`.
7. Report to the user: the verdict, the fatal or strongest issue, evidence quality, what was not verified, and the research spend.

After each gate, write the result in the README stage log before starting the next stage. Never upgrade a verdict because the user is enthusiastic.
