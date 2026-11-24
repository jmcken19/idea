---
name: kill-check
description: Stage 2 existence check, kill-first. Find who already solves the idea's job (native features, products, open source, bots, other chains) and decide Gate 2. Use right after intake and before any business planning.
---
Run inline as Research Lead. Budget: 12 web searches (≤3 extended), 5 page fetches, 10 API fetches (`system/usage-budget.md`).

1. Read `ideas/<slug>/initial-hypothesis.md`, `research/INDEX.md` and `research/competitor-database/`. Run `python3 tools/ir.py searched <terms>` for each main phrasing and reuse fresh findings.
2. Native features first: the platform or protocol the idea sits on (docs, changelog, SDK release notes via `python3 tools/ir.py fetch npm <pkg>`). Every dependency is also a competitor (Rule R1).
3. Then GitHub (`python3 tools/ir.py fetch github-repos "<q>"`, several phrasings), web search with 3+ phrasings, bots and API sites, token launches (DexScreener/CoinGecko), other chains, adjacent industries, dead projects.
4. Log every WebSearch: `python3 tools/ir.py log WebSearch "<q>" <slug> "<one-line result>"`. Add sources to `sources.md` with dates and type. Snippets are type `snippet`.
5. Fill in the coverage table and the equivalents table in `existing-solutions.md`, with an overlap level for each.
6. Gate 2:
   - Equivalent found → run the four-question differentiation test. If there is no evidence for questions 1–2, the verdict is REJECTED: fill in `scorecard.md` (#1, #2 ≤ 1), write `final-verdict.md`, then run the inverse check (`adversarial-reviewer` agent, inverse-check mode, 4 searches). Stop. Do not run Stages 3–5.
   - Nothing equivalent after full coverage → record "why has nobody done this?" as a risk, and continue with `/validate <slug>`.
7. If the coverage is too wide for the budget, hand the remainder to the `market-researcher` agent with an explicit budget, instead of overspending inline.
8. Report to the user straight away: the competitor, the evidence and the verdict. Be blunt.
