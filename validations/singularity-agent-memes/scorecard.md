# Scorecard

Rules: `system/scoring-framework.md`. Scores are 0–5, or `?` when unverified. A score with no source ID counts as `?`. Mark **Fatal = yes** for any weakness that alone kills the idea. Run `python3 tools/ir.py score singularity-agent-memes` for the score and the verdict ceiling.

| # | Criterion | Weight | Score | Fatal | Evidence | Rationale |
|---|---|---|---|---|---|---|
| 1 | Originality and differentiation | 15 | 3 | no | S5,S14 | Bittensor-style structure for AI memes on Solana: no equivalent found; unproven |
| 2 | Existing competition (5 = none, 0 = equivalent exists) | 15 | 2 | no | S8,S14 | Parts exist (Moltbook/Meta, Clawnch, pair venues); no full equivalent found |
| 3 | Verified demand | 15 | 1 | no | S3,S7,S8 | Token trading attention exists but none for the product; Moltbook registrations stalled |
| 4 | Market size | 8 | ? | no |  | Not researched |
| 5 | Revenue potential | 10 | 1 | no | S3,S6 | Fee ceiling about $980/day at today's volume (estimate), volume falling |
| 6 | Business model strength | 10 | ? | no |  | Not stated; rewards cannot be minted (S1) |
| 7 | Distribution feasibility | 10 | ? | no |  | Not researched |
| 8 | Technical feasibility | 5 | 3 | no | S1,S11,S9 | Singularity is a clean Token-2022 mint; venue and identity primitives exist; fee control unverified |
| 9 | Defensibility | 7 | 1 | no | S8,S14 | Copyable by Meta, Clawnch, Pump native features |
| 10 | Regulatory and operational risk (5 = low risk) | 5 | ? | no |  | Counsel needed; SEC statement does not cover agent tokens (S10) |
