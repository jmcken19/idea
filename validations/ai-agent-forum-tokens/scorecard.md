# Scorecard

Rules: `system/scoring-framework.md`. Scores are 0–5, or `?` when unverified. A score with no source ID counts as `?`. Mark **Fatal = yes** for any weakness that alone kills the idea. Run `python3 tools/ir.py score ai-agent-forum-tokens` for the score and the verdict ceiling.

| # | Criterion | Weight | Score | Fatal | Evidence | Rationale |
|---|---|---|---|---|---|---|
| 1 | Originality and differentiation | 15 | 2 | no | S1,S4,S9 | Consensus-spawned forum plus token per forum is a stated difference, but unproven and its value is unexplained |
| 2 | Existing competition (5 = none, 0 = equivalent exists) | 15 | 1 | no | S1,S4,S5,S9 | Moltbook (forum), Clawnch (agent-launched tokens), Reddit Community Points (token per community) |
| 3 | Verified demand | 15 | 1 | no | S2,S3,S7,S9 | No demand evidence for the difference; MOLT trades about $1.3K a day; agent population largely human or fake; Reddit points shut down |
| 4 | Market size | 8 | ? | no |  | Not researched |
| 5 | Revenue potential | 10 | ? | no |  | No revenue model given |
| 6 | Business model strength | 10 | ? | no |  | Not stated |
| 7 | Distribution feasibility | 10 | ? | no |  | Not researched; users of agent forums unmeasured |
| 8 | Technical feasibility | 5 | ? | no |  | Not researched; out of scope |
| 9 | Defensibility | 7 | 1 | no | S1,S4 | Incumbents already have communities and token launches; mechanic is copyable |
| 10 | Regulatory and operational risk (5 = low risk) | 5 | ? | no |  | Not researched; Reddit cited regulation (S9); Moltbook security failures (S3) |
