# Research standards

Evidence rules for every mode. The formal tagging, kill-first order and safeguards (§1–5, §8–9) apply to deep validations (Mode B) and discovery scans. Brainstorming (Mode A) only needs honesty: never invent facts, and say what is unverified.

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
2. Never claim something does not exist without full Stage 2 coverage (see `templates/validation/existing-solutions.md`), logged in `research/search-log.md`. An exact-name search returning nothing proves nothing.
3. Never present a product's marketing claims as verified performance (tag `M`).
4. Prefer primary sources: docs, source code, SDKs on npm, IDLs, chain reads. Use journalism for dates and context.
5. Verify important findings through two independent sources, or one primary source.
6. Write the publication date and the access date for every source. Mark anything older than its freshness window (`system/usage-budget.md`) as **stale**.
7. When sources conflict, record both and say which you trust and why.
8. Separate facts, estimates, hypotheses and unknowns in every summary.
9. An incomplete investigation is never presented as a completed validation. Say which stages were skipped.

## 3. Direction labels (Lesson L3)

When recording a finding, label its direction relative to the idea: **(+)** supports, **(−)** contradicts, **(0)** neutral. Negative findings are listed first in summaries and in the adversarial input.

## 4. Existence-first order (Mode B)

In a deep validation, research questions are asked in this order:

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

## 6. Scope discipline (Mode B)

In brainstorming (Mode A), widening an idea is the point: explore audiences, models, channels and adjacent opportunities freely. Inside a deep validation, keep the idea under test fixed:

- Capture the idea as submitted. Do not add features to make it viable.
- If an adjacent opportunity appears, record it in one line under "Adjacent observations" in `final-verdict.md`, with evidence. Do not research it. It needs its own intake.
- No product-building output: no contracts, sites, mockups, tokenomics designs, marketing or MVPs (Lesson L5).

## 7. Reuse before research

Before any search, run `python3 tools/ir.py searched <terms>` and read `research/INDEX.md`. Reuse a finding if it is inside its freshness window. Otherwise update the existing file instead of creating a new one.

## 8. Permanent safeguards (added 2026-11-24; enforced by `tools/ir.py lint`)

| ID | Requirement | How it is enforced |
|---|---|---|
| SG1 | **Fatal competitor findings rest on direct evidence wherever it exists**: the product's own docs, SDK/source code, repo, or a chain read. Not a news snippet or a vendor roundup. If direct evidence is truly unavailable (e.g. host blocked), say why under `Direct evidence unavailable:` in `final-verdict.md`, and name it as an uncertainty | Lint: any fatal or gating scorecard row must cite a source typed `primary`, `onchain` or `repo` |
| SG2 | **Small samples are never presented as representative market statistics.** Every sample statistic states `n=`, how the sample was drawn (random / convenience / hand-picked), and the population. Below about n=100, or for any non-random sample, write "illustrative, not representative" | Lint: lines quoting a sample/study statistic must contain `n=`; the adversarial reviewer checks the wording |
| SG3 | **Competitor research includes easy replicators**: products, platforms or tools that could ship the proposed function quickly, with evidence of their capability (an existing adjacent feature, an SDK primitive, a history of copying) | Lint: `existing-solutions.md` needs a non-empty `## Easy replicators` table |
| SG4 | **Recent launches (last 90 days) and discontinued projects are always investigated**, using GitHub `created:>` / `archived:true`, npm release history, the Wayback Machine and news | Lint: the coverage table must have `Recent launches` and `Discontinued` rows marked Yes or `Blocked: <reason>` |
| SG5 | **A lack of evidence is never evidence of opportunity.** "Nothing found" counts only after full coverage. Incomplete or blocked channels cap originality (#1) and competition (#2) at 3 | Lint: #1 or #2 ≥ 4 is an error while any coverage channel is No / Partly / Blocked |
| SG6 | **Every final verdict names its unresolved uncertainties**: what is still unknown, which evidence is weakest, and what could reverse the verdict | Lint: `final-verdict.md` needs a non-empty `## Unresolved uncertainties` section |

## 9. Demand versus engagement

Social engagement is not demand. In `market-research.md`, every demand signal goes in the `## Demand evidence` table with a **kind** from this fixed vocabulary. Each kind has a maximum demand level it can support (the lint rejects anything higher):

| Max level | Kinds |
|---|---|
| 1: discussing | engagement, likes, followers, views, upvotes, comments, stars, forks, community-members, waitlist, survey-interest, kol-mention, token-price, token-volume, press-coverage, discussion, complaint |
| 2: seeking | request, bounty-posted, rfp, search-for-tool, feature-request |
| 3: using | downloads, onchain-usage, active-users, integration, workaround-built, native-feature-usage |
| 4: paying | paid-product, revenue, fees-paid, price-paid, paid-preorder, contract |

The verified-demand score (#3) can be 3 or more only if a (+) row at level 3–4 has V or C evidence. A token's price or trading volume is speculation about the token, not demand for the product. GitHub stars and downloads can be bot-inflated, so downloads count as level 3 only with a stated reason.
