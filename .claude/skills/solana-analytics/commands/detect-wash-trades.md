---
description: Assess wash-trading and manipulation risk for a token/venue.
argument-hint: <project or token_mint> [days]
---

Run a wash-trading / manipulation assessment for **$ARGUMENTS** using the solana-analytics skill.

1. Load `references/06-forensics.md`. Stay defensive: produce risk signals with confidence levels,
   never identity claims.
2. Run the round-trip detector (template 17) and the honeypot smell test (template 19); cross-check
   suspect counterparties against sybil funder clusters (template 18).
3. Compute a **wash score** from: round-trip count, funding overlap, and near-zero price impact.
   State the counter-explanation you ruled out (legitimate market-making).
4. Validate via MCP or `scripts/dune_run.py`. Deliver the wash-filtered "real volume" next to gross,
   with the method, and a clear medium/high/low confidence verdict.
