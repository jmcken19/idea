---
name: kill-check
description: Mode B, Stage 2 existence check. Find who already does the idea's job (native features, products, open source, bots, other chains, recent and discontinued projects) and whether a real, wanted difference remains. Only inside a deep validation the founder asked for.
---
Run inline as Research Lead. Budget: 12 research calls (searches + fetches; ≤3 extended searches), counted against the workflow cap by the hook (`system/usage-budget.md`). If the allowance runs out, record coverage so far, list the unchecked channels, and stop.

1. Read `validations/<slug>/initial-hypothesis.md`, `research/INDEX.md` and `research/competitor-database/`. Run `python3 tools/ir.py searched <terms>` for each main phrasing and reuse fresh findings.
2. Native features first: the platform or protocol the idea sits on (docs, changelog, SDK release notes via `python3 tools/ir.py fetch npm <pkg>`). Every dependency is also a competitor (Rule R1).
3. Then GitHub (`python3 tools/ir.py fetch github-repos "<q>"`, several phrasings), web search with 3+ phrasings, bots and API sites, token launches (DexScreener/CoinGecko), other chains, adjacent industries, dead projects.
4. Log every WebSearch: `python3 tools/ir.py log WebSearch "<q>" <slug> "<one-line result>"`. Add sources to `sources.md` with dates and type. Snippets are type `snippet`.
5. Fill in the coverage table and the equivalents table in `existing-solutions.md`, with an overlap level for each.
6. Gate 2:
   - Equivalent found → run the four-question differentiation test. Before abandoning, list the other angles (audience, model, channel, experience) that the equivalent does *not* cover, and say whether any has evidence. If the framing as submitted has no real difference and no evidenced alternative angle, the outcome for that framing is REJECTED: fill in `scorecard.md`, write `final-verdict.md`, and hand the untested angles back to the founder as brainstorm threads. An inverse check by the reviewer is optional, and only worth it when the rejection rests on thin evidence.
   - Nothing equivalent after full coverage → record "why has nobody done this?" as a risk, and continue with `/validate <slug>`.
7. If the coverage is too wide for the budget, hand the remainder to the `market-researcher` agent with an explicit budget, instead of overspending inline.
8. Report to the founder straight away: what exists (with evidence), where an opening might remain, and the outcome. Be direct, not discouraging.
