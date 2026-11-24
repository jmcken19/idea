---
description: Build a grant/fundraising growth report from on-chain data.
argument-hint: <project or program_id> [days]
---

Produce a grant/fundraising growth report for **$ARGUMENTS** using the solana-analytics skill.

1. Load `references/07-growth-reporting.md`. Lead with durability, not levels: retained users,
   organic-vs-incentivized split, returning-user share, revenue kept, market-share trajectory.
2. Compute the metrics with templates 1-3, 13, 14, 10, 11; reconstruct distribution (12) for the
   trust section; run the wash filter (17) so the volume you report is the real number.
3. Build CAC/LTV proxies (label them proxies, state the method). Validate every query via MCP or
   `scripts/dune_run.py` and include live query URLs so a reviewer can re-run them.
4. Assemble the report skeleton (thesis → traction → stickiness → economics → competition →
   distribution → what-the-grant-funds → honesty appendix). Pre-empt the skeptic in the open.
