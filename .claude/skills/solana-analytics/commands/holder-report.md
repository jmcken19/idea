---
description: Holder distribution & concentration risk report for an SPL token.
argument-hint: <token_mint> <decimals> [days]
---

Produce a holder & concentration report for mint **$ARGUMENTS** using the solana-analytics skill.

1. Load `references/05-holder-wallet.md`. Confirm the mint and its `decimals` (look them up — never
   assume).
2. Reconstruct balances (template 8), bucket the distribution (template 12), and compute top-N supply
   share. Exclude/label known CEX, mint authority, and program/LP accounts before reporting.
3. Add the whale/retail/bot read and, if relevant, a smart-money PnL list (template 9, realized-PnL
   caveat).
4. Validate via MCP or `scripts/dune_run.py`; warn that balance reconstruction can time out and give
   the optimized/bounded version if so.
5. Close with the one-line ownership risk sentence a non-analyst can act on.
