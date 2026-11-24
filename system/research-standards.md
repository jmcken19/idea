# Research standards

Mandatory for every agent and every session.

## 1. Evidence tags

Every material claim carries a tag and source IDs (from the idea's `sources.md`), e.g. `[V: S3, S7]`.

| Tag | Meaning | Enough for a material claim? |
|---|---|---|
| **V**: verified | Primary source read (official docs, source code, the product itself), or read from chain with slot/date | Yes |
| **C**: corroborated | Two or more independent secondary sources agree, pages actually opened | Yes, with a note |
| **S**: snippet | Seen only in a search result or summary; page not opened | **No.** Leads only |
| **M**: marketing | The product's own claims about itself (users, TVL, "first", "only") | No, for performance and traction |
| **E**: estimate | Derived number; assumptions and confidence (low/med/high) must be written next to it | Only as an estimate |
| **H**: hypothesis | Believed, untested | No |
| **U**: unknown | Looked for, not found or not verifiable | n/a. Say so plainly |

A *material claim* is anything a verdict depends on: that a competitor exists or doesn't, traction, market size, prices, revenue, demand, legal status.

## 2. Anti-hallucination rules

1. Never invent competitors, statistics, market sizes, revenue, partnerships or user counts. If a number is not in a source, it is `U` or an `E` with arithmetic shown.
2. Never claim something does not exist without full Stage 2 coverage (see `templates/idea/existing-solutions.md`), logged in `research/search-log.md`. An exact-name search returning nothing proves nothing.
3. Never present a product's marketing claims as verified performance (tag `M`).
4. Prefer primary sources: docs, source code, SDKs on npm, IDLs, chain reads. Use journalism for dates and context.
5. Verify important findings through two independent sources, or one primary source.
6. Write the publication date and the access date for every source. Mark anything older than its freshness window (`system/usage-budget.md`) as **stale**.
7. When sources conflict, record both and say which you trust and why.
8. Separate facts, estimates, hypotheses and unknowns in every summary.
9. An incomplete investigation is never presented as a completed validation. Say which stages were skipped.

## 3. Direction labels (Lesson L3)

When recording a finding, label its direction relative to the idea: **(+)** supports, **(−)** contradicts, **(0)** neutral. Negative findings are listed first in summaries and in the adversarial input.

## 4. Kill-first order

Research questions are asked in this order and the order is not optional:

1. Who has already solved this? (native platform features first, then products, open source, bots, other chains, adjacent industries)
2. Why would customers not switch to us from what they use now?
3. Why don't the economics work?
4. Why isn't a token necessary?
5. Only then: how could this work?

## 5. Source hunting beyond keywords

Search for the **job**, not the name. For each idea, list at least 8 alternative phrasings in `initial-hypothesis.md`, including:
- the incumbent platform's own feature names (e.g. "fee sharing", "claimers", "royalties", "rewards");
- adjacent-industry words (payroll, splits, royalties, revenue share, vesting, streams, allowance, treasury);
- tool-category words (bot, API, SDK, terminal, dashboard, checker, analyzer, tracker);
- other chains' words (EVM "splits", Base "rewards recipients").

Channels, by priority: native platform docs and changelogs → GitHub and npm → web search (3+ phrasings) → protocol directories (DefiLlama categories) → token search (CoinGecko, DexScreener) → bots and API sites → Reddit, X and forums for complaints → funding announcements → Wayback for dead projects.

## 6. Scope discipline

- Capture the idea as submitted. Do not add features to make it viable.
- If an adjacent opportunity appears, record it in one line under "Adjacent observations" in `final-verdict.md`, with evidence. Do not research it. It needs its own intake.
- No product-building output: no contracts, sites, mockups, tokenomics designs, marketing or MVPs (Lesson L5).

## 7. Reuse before research

Before any search, run `python3 tools/ir.py searched <terms>` and read `research/INDEX.md`. Reuse a finding if it is inside its freshness window. Otherwise update the existing file instead of creating a new one.
