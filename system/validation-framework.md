# Validation framework

Seven sequential stages with written gates. A stage starts only after the previous gate result is written in the idea's `README.md` stage log (Rule R10). Budgets are in `system/usage-budget.md`.

```
1 Intake ─▶ 2 Existence ─┬─(equivalent, no real difference)──▶ REJECTED (+ inverse check)
                         ▼
                   3 Competitors ─▶ 4 Demand ─┬─(only talk, no behaviour)──▶ NEEDS MORE RESEARCH
                                              ▼
                                         5 Financials ─┬─(no payer)──▶ REJECTED / NEEDS MORE RESEARCH
                                                       ▼
                                          6 Adversarial review (separate agent) ─▶ 7 Decision
```

## Stage 1: Intake (Research Lead, inline)
- `python3 tools/ir.py new <slug> "<idea verbatim>"`.
- Fill `initial-hypothesis.md`: problem, segment, solution, falsifiable hypotheses with kill conditions, and 8+ alternative phrasings.
- Do not expand the idea or suggest features.
- **Gate 1:** the problem and segment are specific enough to search for. If not, ask the submitter one round of questions, then stop.

## Stage 2: Existence check (Research Lead inline; Market Researcher only if coverage is wide)
- Cover every channel in `existing-solutions.md`. Native platform features come first (Rule R1).
- Every dependency the idea relies on is also assessed as a competitor.
- Log every query (`tools/ir.py log` / `fetch`).
- **Gate 2:**
  - Equivalent found + differentiation test fails → **REJECTED**. Stop. Skip Stages 3–5. Run the *inverse check*: one short pass by the adversarial reviewer arguing that the rejection is wrong. A false reject is also an error.
  - Equivalent found + differentiation has evidence → Stage 3, and the differentiation becomes the hypothesis under test.
  - Nothing found after full coverage → Stage 3. "Nothing found" is itself suspicious, so record it as a risk ("why has nobody done this?").

## Stage 3: Competitor analysis
- Complete the matrix in `competitor-analysis.md`. Add the rows to `research/competitor-database/`.
- Name adjacent players who could enter quickly.
- **Gate 3:** a defensible opening is stated in one sentence with evidence, or → REJECTED.

## Stage 4: Demand validation (Commercial Analyst if needed)
- Separate the four levels: discussing / seeking / using / paying.
- Prefer behaviour: on-chain usage, paid products, search for workarounds, fees paid.
- **Gate 4:** level 3–4 evidence → continue. Only level 1–2 → **NEEDS MORE RESEARCH**, plus the cheapest test that would produce level 3–4 evidence.

## Stage 5: Financial validation (Commercial Analyst)
- Named payer, reason to pay, price compared with incumbents, cost, margin, break-even arithmetic.
- Tokens: run `research/token-economics/token-necessity-test.md` and judge the product without the token.
- **Gate 5:** no credible payer → REJECTED (fundamental) or NEEDS MORE RESEARCH (missing data).

## Stage 6: Independent adversarial review (Adversarial Reviewer agent, fresh context)
- Input: `existing-solutions.md`, `competitor-analysis.md`, `market-research.md`, `commercial-analysis.md`, `sources.md`. **Not** the pitch, and not the README narrative.
- The reviewer may run its own searches (budgeted) to find competitors that were missed.
- Output: `adversarial-review.md`, with a recommended verdict.
- Mandatory before any CONDITIONAL or VALIDATED verdict (`ir.py lint` enforces this).

## Stage 7: Decision (Research Lead)
- Run `python3 tools/ir.py score <slug>`. The verdict may not exceed the ceiling.
- Where the lead and the reviewer disagree, the lead writes down which evidence settles it. If none does, the lower verdict stands.
- Write `final-verdict.md`. Update `ideas/INDEX.md`. If REJECTED, add a one-line entry to `research/failed-ideas/README.md`. If the rejection taught something new, add a lesson to `system/lessons-learned.md`.

## Safeguards
SG1–SG6 and the demand-versus-engagement rules in `system/research-standards.md` §8–9 apply at every gate. `tools/ir.py lint` enforces them.

## Outcomes

| Verdict | Meaning | Requires |
|---|---|---|
| **REJECTED** | Fundamental flaw: existing equivalent, no demand, no payer, fatal risk | One fatal issue with evidence |
| **NEEDS MORE RESEARCH** | Missing evidence could change the answer | A list of exactly what is missing and the cheapest way to get it |
| **CONDITIONAL OPPORTUNITY** | Potential exists; named assumptions are unproven | Kill tests with thresholds and dates (Rule R9); adversarial review done |
| **VALIDATED OPPORTUNITY** | Evidence supports investing further; not a guarantee | Gates 2–5 passed with V/C evidence; adversarial review done; no fatal flags; score ceiling allows it |

Founder enthusiasm is not evidence and never raises a verdict. Only new evidence can change a verdict, and the change is recorded with that evidence.

## Re-opening an idea
Allowed only with new evidence. Add a dated section to `final-verdict.md`: "Re-opened because …". A pivot is a new idea (Rule R4): run `ir.py new` again and link the parent.
