# Scorecard

Rules: `system/scoring-framework.md`. Run `python3 tools/ir.py score salary`.

| # | Criterion | Weight | Score | Fatal | Evidence | Rationale |
|---|---|---|---|---|---|---|
| 1 | Originality and differentiation | 15 | 1 | no | S1, S2, S10, S11 | The remaining differences (USD view, memo record, schedule) are presentation features; Bags and tools cover the rest |
| 2 | Existing competition (5 = none, 0 = equivalent exists) | 15 | 0 | yes | S1, S6, S7, S10 | A free native equivalent on the target platform, live 318 days earlier |
| 3 | Verified demand | 15 | 1 | no | S1, S17 | Level-3 data is negative: 95.4% don't split; 0/20 team locks |
| 4 | Market size | 8 | 1 | no | S1, S3 | About 42k multi-wallet coins; fees concentrated in a few dozen |
| 5 | Revenue potential | 10 | 1 | no | S2 | No payer; fee withdrawn |
| 6 | Business model strength | 10 | 0 | no | S1, S2 | Competes with free |
| 7 | Distribution feasibility | 10 | 1 | no | S4 | Depends on Pump.fun's flow; nobody switches for features |
| 8 | Technical feasibility | 5 | 4 | no | S1 | Existing programs suffice |
| 9 | Defensibility | 7 | 0 | no | S2, S7 | The incumbent controls the fee program; its own doc says "Pump.fun could copy" |
| 10 | Regulatory and operational risk (5 = low) | 5 | 2 | no | S3 | Fee routing looks like money transmission; holder-pot ideas add securities risk |
