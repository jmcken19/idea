# 05 — Holder & Wallet Analysis

"Who holds it, how concentrated is it, and who's behind the wallets" — ownership analysis is where
token risk and quality actually live. This reference covers balance reconstruction (the technique
everything else depends on), distribution, segmentation, and smart-money tracking.

## Balance reconstruction — the technique you reuse everywhere

Solana has no Spellbook "current balances of mint X" table you can trust universally, so you
reconstruct balances from net transfer flow: every `to_owner` is `+amount`, every `from_owner` is
`−amount`, summed per owner, divided by decimals.

```sql
-- net balance per owner for a mint (Template 8/12 core)
WITH flows AS (
    SELECT to_owner   AS owner,  cast(amount AS double) AS delta
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}' AND to_owner IS NOT NULL
    UNION ALL
    SELECT from_owner AS owner, -cast(amount AS double) AS delta
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}' AND from_owner IS NOT NULL
)
SELECT owner, sum(delta) / power(10, {{decimals}}) AS balance
FROM flows GROUP BY 1 HAVING sum(delta) > 0;
```

This is **the query that times out** on large/old tokens. Mitigations:
- Bound history; or pre-aggregate daily net flow per owner into a CTE, then sum.
- Build an incremental balances table (materialized) and refresh it, instead of scanning all
  transfers every run.
- For a *current* snapshot, Helius DAS (`getTokenAccounts` / `getAssetsByOwner`) gives live state
  without the scan — use it for "right now," Dune for the trend.

**Never** trust reconstructed balances without dividing by decimals and excluding mint/burn and
program/CEX accounts (next section).

## Distribution & concentration

- **Cohort buckets** (Whale / Shark / Dolphin / Fish / Shrimp by balance) with holder count and
  `pct_of_supply` per bucket — Template 12. The health read: broad distribution vs whale dominance.
- **Top-N supply share** (Template 8) and a Gini/HHI-style concentration number. "Top 10 wallets
  hold 78%" is a one-line risk headline.
- **USD vs token-count buckets.** Fixed token thresholds ignore price; for cross-token comparison,
  bucket by USD value instead.

**Trap — label your non-holders.** CEX hot wallets, the mint authority, program/vault PDAs, and LP
pools all look like giant "whales." Maintain an exclude/label list (known CEX addresses, the token's
own program accounts) before reporting concentration, or you'll call Binance a whale.

## Wallet segmentation: human, whale, bot, sybil

Raw active-wallet counts are almost always inflated. Segment before you call anything "users":
- **Bots** — extreme tx frequency, regular timing, tiny or round amounts, high failed-tx ratio,
  priority-fee patterns. Often the majority of raw activity on hot tokens.
- **Whales vs retail** — by balance and by trade size distribution (avg trade size hides the
  distribution — bucket it).
- **Sybil clusters** — many wallets funded from one source, acting in lockstep (see `06` for the
  funding-graph technique; sybil detection is forensics-grade).
- **Smart money** — wallets with consistent realized profit (next section).

## Smart-money tracking

Rank wallets by realized PnL on a token (Template 9): `+amount_usd` when they sell the target mint,
`−amount_usd` when they buy it, per `trader_id`, gated by `{{min_trades}}` to cut noise.

```sql
-- most profitable traders of a mint (realized PnL only)
SELECT trader_id, realized_pnl_usd, trades, volume_usd
FROM ( /* legs CTE per Template 9 */ )
WHERE trades >= {{min_trades}}
ORDER BY realized_pnl_usd DESC
LIMIT 20;
```

Caveats to **always** state: this is *realized* PnL (ignores current inventory value); cost-basis on
chain is genuinely hard; and wash trading can fake profitability (cross-check with `06`). A
smart-money list is a watchlist, not gospel — drill into a winner's actual holdings before copying.

## Wallet cohorts & lifetime value

- **Acquisition cohort × spend** (Template 14): group wallets by first-seen month, join all their
  activity, compare cohort size and lifetime volume per wallet. Did later cohorts spend more or less?
- **Retention by cohort** (Template 13): the stickiness triangle.
- **LTV proxy** for growth/grant reporting: lifetime volume (or fees paid) per acquired wallet,
  segmented by cohort and by acquisition channel where identifiable. Feeds `07`.

## The ownership one-liner

Every holder analysis should end with a single risk sentence a non-analyst can act on, e.g.:
*"Supply is whale-dominated (top 10 = 78%, 3 of them funded from one wallet two days pre-launch) —
distribution risk is high; treat rallies as exit liquidity until concentration falls."* That
sentence is the deliverable; the buckets are the evidence.
