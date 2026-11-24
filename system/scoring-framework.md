# Scoring framework

The scorecard summarises; it does not decide. Gates and fatal flags decide. `tools/ir.py score <slug>` computes both from `ideas/<slug>/scorecard.md`.

## Criteria (0–5, or `?` if unverified)

| # | Criterion | Weight | 0 | 3 | 5 |
|---|---|---|---|---|---|
| 1 | Originality and differentiation | 15 | Same as an existing option | A difference customers have asked for, evidence at level 2+ | A difference with level 3–4 evidence that incumbents can't ship easily |
| 2 | Existing competition | 15 | An equivalent exists (including native platform features) | Partial overlap; incumbents serve the segment poorly (with evidence) | No equivalent after full coverage, and a credible reason why |
| 3 | Verified demand | 15 | No evidence, or contrary evidence | People use existing workarounds (level 3) | People pay for existing solutions (level 4), and the volume is measured |
| 4 | Market size | 8 | Tiny, or unmeasurable | Measured segment, mid-size | Large, measured from primary data |
| 5 | Revenue potential | 10 | No payer | A named payer, a plausible price | Proven prices in the category, room above cost |
| 6 | Business model strength | 10 | Free substitutes everywhere | Fee or subscription with some lock-in | Recurring, high-margin, with switching costs |
| 7 | Distribution feasibility | 10 | No channel; must beat incumbent flow | An identified channel, untested | A tested channel, or a partner committed |
| 8 | Technical feasibility | 5 | Needs unproven tech or an audit we can't fund | Existing programs plus moderate work | Existing infrastructure, low risk |
| 9 | Defensibility | 7 | The incumbent copies it in one release | Data, integrations or brand take time to copy | Network effects or exclusive access |
| 10 | Regulatory and operational risk (5 = low) | 5 | Custody, securities or money-transmission shape | Manageable with counsel | Read-only, non-custodial, no holder promises |

## Rules applied by `ir.py score`

1. **Evidence or `?`.** A score above 0 with no source ID (e.g. `S4`) is treated as `?`.
2. **Fatal flags.** Any criterion marked *Fatal = yes* → ceiling REJECTED, whatever the total.
3. **The Salary gate.** #2 ≤ 1 (an equivalent exists) and #1 ≤ 1 (no meaningful difference) → ceiling REJECTED. A high total can never hide this.
4. **The demand cap.** #3 unknown or ≤ 1 → at most NEEDS MORE RESEARCH. #3 < 3 → at most CONDITIONAL.
5. **The weak-link cap.** Any criterion ≤ 1 → at most CONDITIONAL.
6. **The unknowns cap.** 1–2 unverified criteria → at most CONDITIONAL. 3 or more → at most NEEDS MORE RESEARCH.
7. Unverified criteria count as 0 in the weighted total, so missing research lowers the score rather than being skipped.

The weighted total (0–100) is for comparing ideas, not for deciding them. The verdict is the lowest of: the evidence, the gate results, and the ceiling.
