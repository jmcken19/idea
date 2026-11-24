-- =====================================================================================
-- SOLANA ON-CHAIN ANALYTICS — DUNE QUERY LIBRARY
-- 22 production-grade, parameterized templates  |  by Muhammad Auwal Abdul Aziz (@Ghostieemoh)
-- "The blockchain never lies. Stop guessing. Start querying."
--
-- Engine: DuneSQL (Trino).  Solana-first; EVM variants noted where the pattern is EVM-native.
-- Parameters use Dune's {{param}} syntax. Fill them in the Dune UI or hardcode to test.
-- Every query states the business question it answers; each one runs as-is once params are set.
-- Confirm column names in the Dune schema sidebar if a Spellbook model has drifted.
-- See references/ for the why, optimization tips, pitfalls, and viz per template.
-- =====================================================================================


-- -------------------------------------------------------------------------------------
-- 1. DAILY ACTIVE USERS (DAU)
-- Q: How many unique wallets transact per day, and is engagement growing?
-- -------------------------------------------------------------------------------------
SELECT
    date_trunc('day', block_time)        AS day,
    approx_distinct(signer)              AS active_wallets
FROM solana.transactions
WHERE block_time >= now() - interval '{{days}}' day
  AND success = true
GROUP BY 1
ORDER BY 1;
-- Protocol-scoped variant: join solana.instructions and filter by program_id.
-- EVM variant: FROM ethereum.transactions, COUNT(DISTINCT "from") by day.


-- -------------------------------------------------------------------------------------
-- 2. NEW WALLETS
-- Q: How many wallets are appearing for the first time each day (true acquisition)?
-- -------------------------------------------------------------------------------------
WITH first_seen AS (
    SELECT
        signer                            AS wallet,
        min(date_trunc('day', block_time)) AS first_day
    FROM solana.transactions
    WHERE success = true
    GROUP BY 1
)
SELECT
    first_day                            AS day,
    count(*)                             AS new_wallets
FROM first_seen
WHERE first_day >= current_date - interval '{{days}}' day
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------------------------------
-- 3. RETURNING WALLETS
-- Q: Each day, how many active wallets had already been seen before (loyalty vs churn)?
-- -------------------------------------------------------------------------------------
WITH activity AS (
    SELECT DISTINCT
        signer                            AS wallet,
        date_trunc('day', block_time)     AS day
    FROM solana.transactions
    WHERE block_time >= now() - interval '{{days}}' day
      AND success = true
),
first_seen AS (
    SELECT wallet, min(day) AS first_day
    FROM activity
    GROUP BY 1
)
SELECT
    a.day,
    count_if(a.day = f.first_day)        AS new_wallets,
    count_if(a.day > f.first_day)        AS returning_wallets
FROM activity a
JOIN first_seen f ON a.wallet = f.wallet
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------------------------------
-- 4. VOLUME TRACKING (USD)
-- Q: What is daily USD trading volume for a project/token, and how is it trending?
-- -------------------------------------------------------------------------------------
SELECT
    block_date                           AS day,
    sum(amount_usd)                      AS volume_usd,
    count(*)                             AS trades,
    approx_distinct(trader_id)           AS traders
FROM dex_solana.trades
WHERE block_time >= now() - interval '{{days}}' day
  AND project = '{{project}}'            -- e.g. 'raydium', 'meteora', 'solfi'
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------------------------------
-- 5. DEX TRADING ACTIVITY (per project leaderboard)
-- Q: Across Solana DEXs, who leads on volume, trades, and unique traders in the window?
-- -------------------------------------------------------------------------------------
SELECT
    project,
    sum(amount_usd)                      AS volume_usd,
    count(*)                             AS trades,
    approx_distinct(trader_id)           AS unique_traders,
    sum(amount_usd) / nullif(count(*),0) AS avg_trade_size_usd
FROM dex_solana.trades
WHERE block_time >= now() - interval '{{days}}' day
GROUP BY 1
ORDER BY volume_usd DESC
LIMIT 25;


-- -------------------------------------------------------------------------------------
-- 6. LIQUIDITY / PAIR CONCENTRATION (volume-as-proxy)
-- Q: Is a venue's volume healthily diversified or concentrated in one pair (risk)?
-- -------------------------------------------------------------------------------------
WITH pair_volume AS (
    SELECT
        token_pair,
        sum(amount_usd)                  AS volume_usd
    FROM dex_solana.trades
    WHERE block_time >= now() - interval '{{days}}' day
      AND project = '{{project}}'
    GROUP BY 1
)
SELECT
    token_pair,
    volume_usd,
    volume_usd / sum(volume_usd) OVER ()             AS pct_of_venue_volume,
    sum(volume_usd) OVER (ORDER BY volume_usd DESC)
        / sum(volume_usd) OVER ()                    AS cumulative_pct
FROM pair_volume
ORDER BY volume_usd DESC
LIMIT 20;


-- -------------------------------------------------------------------------------------
-- 7. TOKEN GROWTH (cumulative & new holders over time)
-- Q: Is the token's holder base growing, and how fast are new holders arriving?
-- -------------------------------------------------------------------------------------
WITH holder_first_seen AS (
    SELECT
        to_owner                          AS holder,
        min(date_trunc('day', block_time)) AS first_day
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}'
      AND to_owner IS NOT NULL
    GROUP BY 1
),
daily_new AS (
    SELECT first_day AS day, count(*) AS new_holders
    FROM holder_first_seen
    GROUP BY 1
)
SELECT
    day,
    new_holders,
    sum(new_holders) OVER (ORDER BY day) AS cumulative_holders
FROM daily_new
WHERE day >= current_date - interval '{{days}}' day
ORDER BY day;


-- -------------------------------------------------------------------------------------
-- 8. WHALE MONITORING (top holders via balance reconstruction)
-- Q: Who are the largest holders of a token right now, and how concentrated is supply?
-- Note: balances are reconstructed from net transfer flow. {{decimals}} = token decimals.
-- -------------------------------------------------------------------------------------
WITH flows AS (
    SELECT to_owner   AS owner, cast(amount AS double) AS delta
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}' AND to_owner IS NOT NULL
    UNION ALL
    SELECT from_owner AS owner, -cast(amount AS double) AS delta
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}' AND from_owner IS NOT NULL
)
SELECT
    owner,
    sum(delta) / power(10, {{decimals}})            AS balance,
    (sum(delta) / sum(sum(delta)) OVER ()) * 100     AS pct_of_supply
FROM flows
GROUP BY 1
HAVING sum(delta) > 0
ORDER BY balance DESC
LIMIT 50;


-- -------------------------------------------------------------------------------------
-- 9. SMART MONEY TRACKING (wallets ranked by realized PnL)
-- Q: Which wallets are the most profitable traders of a token (copy-trade targets)?
-- Realized PnL ~= USD received from sells - USD spent on buys, per trader.
-- -------------------------------------------------------------------------------------
WITH legs AS (
    SELECT
        trader_id,
        sum(CASE WHEN token_bought_mint_address = '{{token_mint}}' THEN -amount_usd ELSE 0 END)
          + sum(CASE WHEN token_sold_mint_address = '{{token_mint}}' THEN amount_usd ELSE 0 END)
                                          AS realized_pnl_usd,
        count(*)                          AS trades,
        sum(amount_usd)                   AS volume_usd
    FROM dex_solana.trades
    WHERE block_time >= now() - interval '{{days}}' day
      AND ( token_bought_mint_address = '{{token_mint}}'
         OR token_sold_mint_address   = '{{token_mint}}' )
    GROUP BY 1
)
SELECT trader_id, realized_pnl_usd, trades, volume_usd
FROM legs
WHERE trades >= {{min_trades}}
ORDER BY realized_pnl_usd DESC
LIMIT 20;


-- -------------------------------------------------------------------------------------
-- 10. PROTOCOL REVENUE (fee-based proxy)
-- Q: How much revenue does a DEX generate daily (volume x effective fee bps)?
-- Swap {{fee_bps}} for the protocol's fee tier (e.g. 25 = 0.25%).
-- -------------------------------------------------------------------------------------
SELECT
    block_date                           AS day,
    sum(amount_usd)                      AS volume_usd,
    sum(amount_usd) * ({{fee_bps}} / 10000.0) AS est_revenue_usd
FROM dex_solana.trades
WHERE block_time >= now() - interval '{{days}}' day
  AND project = '{{project}}'
GROUP BY 1
ORDER BY 1;
-- Where a curated fee model exists (e.g. dex.fees on EVM), prefer real fees over this proxy.


-- -------------------------------------------------------------------------------------
-- 11. MARKET SHARE ANALYSIS
-- Q: What share of total Solana DEX volume does each project hold over the window?
-- -------------------------------------------------------------------------------------
WITH by_project AS (
    SELECT project, sum(amount_usd) AS volume_usd
    FROM dex_solana.trades
    WHERE block_time >= now() - interval '{{days}}' day
    GROUP BY 1
)
SELECT
    project,
    volume_usd,
    volume_usd / sum(volume_usd) OVER () AS market_share
FROM by_project
ORDER BY market_share DESC;


-- -------------------------------------------------------------------------------------
-- 12. TOKEN HOLDER DISTRIBUTION (concentration buckets)
-- Q: Is the token widely distributed or whale-dominated?
-- -------------------------------------------------------------------------------------
WITH flows AS (
    SELECT to_owner AS owner, cast(amount AS double) AS delta
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}' AND to_owner IS NOT NULL
    UNION ALL
    SELECT from_owner AS owner, -cast(amount AS double) AS delta
    FROM tokens_solana.transfers
    WHERE token_mint_address = '{{token_mint}}' AND from_owner IS NOT NULL
),
balances AS (
    SELECT owner, sum(delta) / power(10, {{decimals}}) AS balance
    FROM flows GROUP BY 1 HAVING sum(delta) > 0
)
SELECT
    CASE
        WHEN balance >= 1000000 THEN '1. Whale (>=1M)'
        WHEN balance >= 100000  THEN '2. Shark (100K-1M)'
        WHEN balance >= 10000   THEN '3. Dolphin (10K-100K)'
        WHEN balance >= 1000    THEN '4. Fish (1K-10K)'
        ELSE                         '5. Shrimp (<1K)'
    END                                  AS cohort,
    count(*)                             AS holders,
    sum(balance)                         AS tokens_held,
    sum(balance) / sum(sum(balance)) OVER () AS pct_of_supply
FROM balances
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------------------------------
-- 13. RETENTION ANALYSIS (weekly)
-- Q: Of the wallets first active in a given week, what % return in later weeks?
-- -------------------------------------------------------------------------------------
WITH activity AS (
    SELECT DISTINCT trader_id AS wallet, date_trunc('week', block_time) AS active_week
    FROM dex_solana.trades
    WHERE block_time >= now() - interval '{{days}}' day
      AND project = '{{project}}'
),
cohorts AS (
    SELECT wallet, min(active_week) AS cohort_week FROM activity GROUP BY 1
)
SELECT
    c.cohort_week,
    date_diff('week', c.cohort_week, a.active_week) AS weeks_since_join,
    approx_distinct(a.wallet)                       AS active_wallets
FROM activity a
JOIN cohorts c ON a.wallet = c.wallet
GROUP BY 1, 2
ORDER BY 1, 2;


-- -------------------------------------------------------------------------------------
-- 14. COHORT ANALYSIS (acquisition cohorts x spend)
-- Q: How do wallets acquired in each month compare on size and lifetime volume?
-- -------------------------------------------------------------------------------------
WITH trades AS (
    SELECT trader_id AS wallet, block_time, amount_usd
    FROM dex_solana.trades
    WHERE project = '{{project}}'
),
cohorts AS (
    SELECT wallet, date_trunc('month', min(block_time)) AS cohort_month
    FROM trades GROUP BY 1
)
SELECT
    c.cohort_month,
    approx_distinct(c.wallet)            AS cohort_size,
    sum(t.amount_usd)                    AS lifetime_volume_usd,
    sum(t.amount_usd) / approx_distinct(c.wallet) AS volume_per_wallet
FROM cohorts c
JOIN trades t ON c.wallet = t.wallet
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------------------------------
-- 15. CROSS-CHAIN ANALYSIS
-- Q: How does DEX volume and share split across chains (incl. Solana) over the window?
-- Uses the unified dex.trades Spellbook model that spans EVM chains + Solana.
-- -------------------------------------------------------------------------------------
SELECT
    blockchain,
    sum(amount_usd)                      AS volume_usd,
    approx_distinct(taker)               AS traders,
    sum(amount_usd) / sum(sum(amount_usd)) OVER () AS chain_share
FROM dex.trades
WHERE block_time >= now() - interval '{{days}}' day
GROUP BY 1
ORDER BY volume_usd DESC;


-- -------------------------------------------------------------------------------------
-- 16. NETWORK / PRIORITY FEE ANALYSIS
-- Q: How much are users paying in fees per day, and is congestion (fee/tx) rising?
-- {{fee_decimals}} = 9 to express lamports as SOL.
-- -------------------------------------------------------------------------------------
SELECT
    date_trunc('day', block_time)        AS day,
    count(*)                             AS txns,
    sum(fee) / power(10, {{fee_decimals}})            AS total_fees_sol,
    (sum(fee) / power(10, {{fee_decimals}})) / nullif(count(*),0) AS avg_fee_per_tx_sol,
    count_if(success = false)            AS failed_txns,
    1.0 * count_if(success = false) / nullif(count(*),0) AS failed_ratio
FROM solana.transactions
WHERE block_time >= now() - interval '{{days}}' day
GROUP BY 1
ORDER BY 1;


-- -------------------------------------------------------------------------------------
-- 17. WASH-TRADE ROUND-TRIP DETECTOR
-- Q: Which wallets buy then sell the same pair within {{window_seconds}}s (wash signal)?
-- -------------------------------------------------------------------------------------
WITH t AS (
    SELECT
        trader_id, token_pair, block_time,
        token_bought_mint_address AS bought, token_sold_mint_address AS sold, amount_usd
    FROM dex_solana.trades
    WHERE project = '{{project}}'
      AND block_time >= now() - interval '{{days}}' day
)
SELECT
    a.trader_id,
    count(*)                             AS round_trips,
    sum(a.amount_usd + b.amount_usd)     AS wash_volume_usd
FROM t a
JOIN t b
  ON a.trader_id = b.trader_id
 AND a.token_pair = b.token_pair
 AND a.bought = b.sold
 AND a.sold   = b.bought
 AND b.block_time BETWEEN a.block_time AND a.block_time + interval '{{window_seconds}}' second
GROUP BY 1
HAVING count(*) >= {{min_round_trips}}
ORDER BY wash_volume_usd DESC
LIMIT 50;


-- -------------------------------------------------------------------------------------
-- 18. SYBIL CLUSTER (shared first-funder)
-- Q: Which funder addresses bankrolled many wallets' first SOL (sybil suspicion)?
-- Exclude known CEX/faucet funders before treating a cluster as sybil (see references/05).
-- -------------------------------------------------------------------------------------
WITH first_fund AS (
    SELECT
        to_owner   AS wallet,
        from_owner AS funder,
        row_number() OVER (PARTITION BY to_owner ORDER BY block_time) AS rn
    FROM tokens_solana.transfers
    WHERE token_mint_address = 'So11111111111111111111111111111111111111112'
      AND to_owner IS NOT NULL AND from_owner IS NOT NULL
)
SELECT
    funder,
    count(*)                             AS funded_wallets
FROM first_fund
WHERE rn = 1
GROUP BY 1
HAVING count(*) >= {{min_cluster_size}}
ORDER BY funded_wallets DESC
LIMIT 50;


-- -------------------------------------------------------------------------------------
-- 19. HONEYPOT SMELL TEST (buy vs sell success asymmetry)
-- Q: Can buyers of this mint actually sell, or do sells not happen (honeypot)?
-- -------------------------------------------------------------------------------------
SELECT
    count_if(token_bought_mint_address = '{{token_mint}}') AS buys,
    count_if(token_sold_mint_address   = '{{token_mint}}') AS sells,
    approx_distinct(CASE WHEN token_bought_mint_address = '{{token_mint}}' THEN trader_id END) AS buyers,
    approx_distinct(CASE WHEN token_sold_mint_address   = '{{token_mint}}' THEN trader_id END) AS sellers,
    1.0 * count_if(token_sold_mint_address = '{{token_mint}}')
        / nullif(count_if(token_bought_mint_address = '{{token_mint}}'), 0) AS sell_to_buy_ratio
FROM dex_solana.trades
WHERE block_time >= now() - interval '{{days}}' day
  AND ( token_bought_mint_address = '{{token_mint}}'
     OR token_sold_mint_address   = '{{token_mint}}' );
-- A near-zero sell_to_buy_ratio on a token with many buyers is a honeypot red flag.


-- -------------------------------------------------------------------------------------
-- 20. MEV SANDWICH (intra-slot bracket of a victim swap)
-- Q: On a pair, where does one wallet buy and sell within the same slot around others?
-- Confirm the slot column name (block_slot) in the schema sidebar for the model version.
-- -------------------------------------------------------------------------------------
WITH ordered AS (
    SELECT
        block_slot, token_pair, trader_id, amount_usd,
        token_bought_mint_address AS bought, token_sold_mint_address AS sold,
        row_number() OVER (PARTITION BY block_slot, token_pair ORDER BY block_time) AS seq
    FROM dex_solana.trades
    WHERE block_time >= now() - interval '{{days}}' day
      AND token_pair = '{{token_pair}}'
)
SELECT
    a.block_slot,
    a.trader_id                          AS attacker,
    count(*)                             AS bracketed_victims,
    sum(c.amount_usd)                    AS attacker_exit_usd
FROM ordered a                                  -- front-run (buy)
JOIN ordered c                                  -- back-run (sell), same slot, same wallet
  ON a.block_slot = c.block_slot
 AND a.token_pair = c.token_pair
 AND a.trader_id  = c.trader_id
 AND a.bought = c.sold AND a.sold = c.bought
 AND c.seq > a.seq
JOIN ordered v                                  -- a victim trade sequenced between them
  ON v.block_slot = a.block_slot
 AND v.token_pair = a.token_pair
 AND v.trader_id <> a.trader_id
 AND v.seq > a.seq AND v.seq < c.seq
GROUP BY 1, 2
ORDER BY attacker_exit_usd DESC
LIMIT 50;


-- -------------------------------------------------------------------------------------
-- 21. LST EXCHANGE-RATE / DE-PEG MONITOR
-- Q: How does a liquid-staking token's market price track SOL over time (de-peg watch)?
-- Compares LST mint price to SOL price from the curated prices model.
-- -------------------------------------------------------------------------------------
WITH lst AS (
    SELECT date_trunc('day', minute) AS day, avg(price) AS lst_usd
    FROM prices.usd
    WHERE blockchain = 'solana'
      AND contract_address = '{{lst_mint}}'
      AND minute >= now() - interval '{{days}}' day
    GROUP BY 1
),
sol AS (
    SELECT date_trunc('day', minute) AS day, avg(price) AS sol_usd
    FROM prices.usd
    WHERE blockchain = 'solana'
      AND contract_address = 'So11111111111111111111111111111111111111112'
      AND minute >= now() - interval '{{days}}' day
    GROUP BY 1
)
SELECT
    lst.day,
    lst.lst_usd,
    sol.sol_usd,
    lst.lst_usd / nullif(sol.sol_usd, 0) AS lst_per_sol
FROM lst JOIN sol ON lst.day = sol.day
ORDER BY lst.day;
-- A market lst_per_sol drifting below the protocol's redemption rate flags a de-peg/discount.


-- -------------------------------------------------------------------------------------
-- 22. INSTRUCTION ADOPTION (by Anchor discriminator)
-- Q: How often is one specific program instruction called per day (feature adoption)?
-- {{ix_discriminator_hex}} = first 8 bytes of sha256("global:<ix_name>"), hex, no 0x.
-- -------------------------------------------------------------------------------------
SELECT
    date_trunc('day', block_time)        AS day,
    count(*)                             AS instruction_calls,
    approx_distinct(tx_signer)           AS unique_callers
FROM solana.instructions
WHERE executing_account = '{{program_id}}'
  AND bytearray_starts_with(data, 0x{{ix_discriminator_hex}})
  AND block_time >= now() - interval '{{days}}' day
GROUP BY 1
ORDER BY 1;
-- Pair with references/02-decoding.md to derive the discriminator from an instruction name.
-- end of library
