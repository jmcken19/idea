# 01 — Solana Analytics Data Sources

Pick the table before you write the SQL. Most bad analyses are bad table choices. This is the map of
where Solana on-chain truth lives, what each source is good and bad at, and the idioms (decimals,
USD, double-counting) that bite analysts.

## The three places Solana data lives for an analyst

| Source | What it is | Best for | Watch out |
| --- | --- | --- | --- |
| **Dune** (DuneSQL / Trino) | Curated **Spellbook** models + raw tables | KPI/metric SQL, dashboards, cross-protocol & cross-chain comparison | Spellbook coverage lags brand-new programs; some heavy reconstructions time out |
| **Flipside** (Snowflake SQL) | Curated `solana.*` schemas | Fast curated DeFi/NFT/staking tables, free tier | Dialect differs from Dune (Snowflake, not Trino); column names differ |
| **Helius** (DAS + RPC + webhooks) | Real-time RPC, Digital Asset Standard, enhanced txns | Current state (balances, token metadata, asset ownership), live alerts | Point-in-time, not historical aggregation; rate-limited; not SQL |

Rule of thumb: **history & aggregation → Dune/Flipside; current state & metadata & realtime →
Helius DAS**. A good answer often joins both (e.g. Dune for the trend, Helius DAS for the live
holder snapshot or token metadata).

## Dune Spellbook — the Solana tables you actually use

These are the curated, decoded, USD-normalized models. Reach for raw `solana.*` only when Spellbook
doesn't cover your program.

**Activity / base layer**
- `solana.transactions` — one row per transaction. Key cols: `signer`, `block_time`, `block_slot`,
  `success`, `fee`. Use for DAU (`approx_distinct(signer)`), tx counts, fee/priority-fee analysis.
- `solana.instructions` — one row per instruction. Key col: `program_id`. Join to scope activity to
  a specific program (protocol-level DAU, instruction mix).
- `solana.account_activity` — account read/write touch per tx (writable accounts, balance deltas).

**DEX / trading**
- `dex_solana.trades` — **the workhorse.** One curated row per swap leg with `amount_usd`,
  `project` (`raydium`, `meteora`, `orca`, `phoenix`, `lifinity`, `solfi`, …), `trader_id`,
  `token_bought_mint_address`, `token_sold_mint_address`, `token_pair`, `block_date`, `block_time`.
- `dex.trades` — the **multi-chain unified** model (EVM chains + Solana). Use for cross-chain share;
  taker column is `taker` (vs Solana's `trader_id`).

**Tokens / transfers / balances**
- `tokens_solana.transfers` — curated SPL transfers: `token_mint_address`, `from_owner`,
  `to_owner`, `amount` (raw), `block_time`. Basis for holder growth and balance reconstruction.
- `spl_token_solana.transfers` — lower-level transfer events when you need raw fidelity.
- `prices.usd` — token USD price by minute/hour: join on `(blockchain, contract_address, minute)` to
  price anything `amount_usd` doesn't already cover. For Solana, `contract_address` = the mint.
- `tokens_solana.fungible` / token metadata models — decimals, symbol, name (avoid hardcoding
  decimals — look them up; see the decimals idiom below).

**Staking / native**
- `solana.rewards` and staking models — epoch rewards, validator/stake activity (for LST and native
  staking analytics; see `04`).

> Spellbook is open source. If a table name drifts, search it: in the Dune editor the schema
> sidebar is authoritative, and `references/resources.md` links the Spellbook repo. Never invent a
> column — confirm it.

## Flipside equivalents (when you use Flipside instead)

Same questions, different schema. Common Flipside Solana tables: `solana.core.fact_transactions`,
`solana.core.fact_events`, `solana.defi.fact_swaps`, `solana.core.fact_transfers`,
`solana.price.ez_prices_hourly`, `solana.gov.fact_staking`. Dialect is Snowflake SQL
(`COUNT(DISTINCT …)`, `DATE_TRUNC('day', block_timestamp)`), not Trino. This skill's templates are
DuneSQL-first; port to Flipside by swapping table names and the distinct/`date_trunc` idioms.

## Helius DAS & RPC (current state + realtime)

Use Helius when the question is "**right now**" or needs metadata Dune doesn't carry:
- **`getAsset` / `getAssetsByOwner` / `searchAssets`** (DAS) — NFT & token ownership, compressed
  assets, metadata. Great for a live holder snapshot or verifying a mint's authority/freeze state.
- **Enhanced Transactions / parsed history** — human-readable txn type per signature.
- **Webhooks / LaserStream** — push alerts on addresses/programs (feeds the live monitoring in `06`
  and the dashboards' "alert" widgets).

The bundled MCP layer (`.mcp.json`) wires Helius so the agent can call DAS directly; without it,
fall back to documenting the exact RPC call. Helius is **state, not history** — never try to compute
a 90-day retention curve from RPC; that is Dune/Flipside's job.

## Idioms that bite every analyst

1. **Decimals are raw.** `amount` in transfer tables is integer base units. Human balance =
   `amount / power(10, decimals)`. SOL has 9, USDC 6, most SPLs 6–9. **Look decimals up** per mint;
   do not assume. `amount_usd` in `dex_solana.trades` is already normalized — prefer it.
2. **USD via `amount_usd` or `prices.usd`.** Don't recompute price×amount when a curated USD column
   exists. When you must price, join `prices.usd` on the mint and the truncated minute/hour.
3. **DEX trades log both legs.** A swap is one economic event but can appear as buy-leg and sell-leg.
   The Spellbook usually deduplicates to one row per trade — verify your totals against a known
   source (e.g. DefiLlama) before trusting a new query.
4. **wallet ≠ human.** One person can run thousands of wallets; bots dominate raw counts. Use
   `approx_distinct` for cheap cardinality, then segment (see `05`/`06`) before claiming "users."
5. **Time zones & grain.** `block_time` is UTC. Pick the grain that matches the decision; `block_date`
   is a partition column — filter/group on it where possible for speed.
6. **Failed transactions.** Filter `success = true` for engagement metrics; *keep* failures when you
   are studying congestion, bot spam, or priority-fee behavior.

## Choosing the source — a 10-second decision

- "How did X trend over the last N days?" → **Dune** (`dex_solana.trades` / `tokens_solana.transfers`).
- "Who owns this NFT collection / what's this mint's metadata right now?" → **Helius DAS**.
- "I want a free curated swaps table fast" → **Flipside** `solana.defi.fact_swaps`.
- "Alert me when this whale moves" → **Helius webhook** (+ `06` heuristics).
- "Compare Solana vs EVM for a sector" → **Dune** unified `dex.trades`.
