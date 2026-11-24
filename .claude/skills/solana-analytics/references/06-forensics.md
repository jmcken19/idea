# 06 — On-Chain Forensics

The question behind half of all serious analytics requests is "**is this real?**" Is the volume
organic or wash-traded; is this token a rug; are these 40,000 "users" one farmer; did the exploiter's
funds go through this wallet. Forensics is the part of analytics with the highest stakes and the
least documentation. These are heuristics, not verdicts — every signal here is *probabilistic*, and
you must say so. Used well, they turn "looks suspicious" into evidence.

> Ethics & scope: these techniques are for **defensive** analysis — risk assessment, fraud
> detection, incident response, due diligence. They read public on-chain data. They are not for
> deanonymizing individuals or harassment. Report findings as risk signals with confidence levels,
> never as accusations of identity.

## Wash trading

**What it is:** volume manufactured by an entity trading with itself (or a small ring) to fake
activity, farm rewards, or inflate a token. **Signals:**
- Same entity on both sides — `trader_id` buys and sells the same pair within seconds, repeatedly.
- Round-trip flows — token leaves a wallet and returns (directly or via 2–3 hops) with net ≈ 0.
- Volume with no price discovery — huge volume, flat price, tight wallet set.
- Funding ties — the "counterparties" are funded from one source (join to the sybil section).
- Reward-window clustering — volume spikes exactly during an incentive/airdrop snapshot window.

```sql
-- Q: which wallets show buy-then-sell of the same pair within a short window (wash signal)?
WITH t AS (
    SELECT trader_id, token_pair, block_time,
           token_bought_mint_address AS bought, token_sold_mint_address AS sold, amount_usd
    FROM dex_solana.trades
    WHERE project = '{{project}}'
      AND block_time >= now() - interval '{{days}}' day
)
SELECT
    a.trader_id,
    count(*)                              AS round_trips,
    sum(a.amount_usd + b.amount_usd)      AS wash_volume_usd
FROM t a
JOIN t b
  ON a.trader_id = b.trader_id
 AND a.token_pair = b.token_pair
 AND a.bought = b.sold AND a.sold = b.bought          -- opposite legs
 AND b.block_time BETWEEN a.block_time AND a.block_time + interval '{{window_seconds}}' second
GROUP BY 1
HAVING count(*) >= {{min_round_trips}}
ORDER BY wash_volume_usd DESC
LIMIT 50;
```

**Caveat:** legitimate market-makers also round-trip constantly. Wash-trading evidence is *self-
dealing with no economic purpose* — net-zero position, single funding source, no real price impact.
Report a **wash score** (round-trips, funding overlap, price-impact ≈ 0), not a binary.

## Rug-pull detection

A rug is a pre-meditated exit. The signals are mostly visible *before* it happens — that's the value.
**Pre-launch / structural signals:**
- **Mint authority not revoked** — the team can mint unlimited supply. Check the mint's authority
  (Helius DAS / RPC `getAccountInfo` on the mint). Revoked = good; active = severe risk.
- **Freeze authority active** — the team can freeze your tokens (honeypot vector).
- **Supply concentration** — top wallets (often dev-linked, funded pre-launch) hold the float (`05`).
- **LP not locked / not burned** — if the team holds the LP tokens, they can pull liquidity.

**Behavioral signals (the rug in progress):**
- **Liquidity removal** — a large `withdraw`/`removeLiquidity` from the pool, especially by a
  dev-linked wallet.
- **Dev wallet distribution then dump** — supply moves from the deployer to fresh wallets, then sells.
- **Honeypot / sell-tax** — buys succeed, sells fail or are taxed; detectable as a buy/sell success
  asymmetry per token.

```sql
-- Q: buy vs sell success asymmetry for a mint (honeypot smell test)
SELECT
    count_if(token_bought_mint_address = '{{token_mint}}') AS buys,
    count_if(token_sold_mint_address   = '{{token_mint}}') AS sells,
    1.0 * count_if(token_sold_mint_address = '{{token_mint}}')
        / nullif(count_if(token_bought_mint_address = '{{token_mint}}'), 0) AS sell_to_buy_ratio
FROM dex_solana.trades
WHERE block_time >= now() - interval '{{days}}' day
  AND ( token_bought_mint_address = '{{token_mint}}'
     OR token_sold_mint_address   = '{{token_mint}}' );
-- A near-zero sell_to_buy_ratio on a token with many buyers is a honeypot red flag.
```

Deliver a **rug-risk checklist** with each item RED/AMBER/GREEN and the evidence, not a yes/no. Mint
authority + LP lock + concentration are the three that matter most.

## Sybil / airdrop-farming detection

**What it is:** one operator running many wallets to multiply an airdrop or fake user counts. The
giveaway is **shared funding and lockstep behavior**, not any single wallet.
- **Common funder** — N wallets all first-funded from the same source address (the funding graph).
- **Lockstep timing** — wallets created/active in tight bursts, doing the identical action sequence.
- **Minimal-viable activity** — each wallet does exactly the qualifying action, nothing more.
- **Dust fan-out / fan-in** — one wallet sprays SOL to many, which later sweep back to one.

```sql
-- Q: clusters of wallets sharing a first funder (sybil suspicion)
WITH first_fund AS (
    SELECT to_owner AS wallet, from_owner AS funder,
           row_number() OVER (PARTITION BY to_owner ORDER BY block_time) AS rn
    FROM tokens_solana.transfers
    WHERE token_mint_address = 'So11111111111111111111111111111111111111112'   -- wrapped SOL
)
SELECT funder, count(*) AS funded_wallets, array_agg(wallet) AS wallets
FROM first_fund
WHERE rn = 1
GROUP BY 1
HAVING count(*) >= {{min_cluster_size}}
ORDER BY funded_wallets DESC
LIMIT 50;
```

**Caveat:** CEX withdrawal addresses and faucets fund thousands of legitimate wallets — exclude known
funders (`05` label list) before treating a cluster as sybil. The strong signal is shared funder
**plus** lockstep behavior **plus** minimal activity, together.

## MEV / sandwich detection

**What it is:** a bot brackets a victim's swap in the same block — buys just before (front-run) and
sells just after (back-run) — to extract the slippage. **Signals:** same attacker wallet appearing
immediately before and after a victim trade on the same pair within one slot/block, with profit.

Pattern: partition `dex_solana.trades` by `(token_pair, block_slot)`, order within slot, and look for
`attacker buy → victim buy → attacker sell` triplets on the same pair in the same slot, attacker net
positive. Solana's parallel execution and Jito bundles make the slot the right unit — block-level
ordering matters here, so use `block_slot` and intra-slot sequence, and validate against a known
sandwich before trusting counts. Output: sandwich count, extracted USD, top extractor wallets, and
the pairs/pools most targeted (a protocol-health signal — heavily sandwiched pools lose users).

## Fund tracing (incident response / stolen-funds)

When funds are exploited or a wallet must be followed, trace the flow hop by hop:
1. **Anchor on the source** — the exploiter/victim address and the incident time.
2. **Follow outflows** — recursively expand `from_owner → to_owner` transfers from the source,
   bounded by depth and time, keeping amounts so you can spot the main artery vs dust noise.
3. **Label terminals** — flag known CEX deposit addresses, bridges (Wormhole, deBridge,
   Allbridge), and mixer-like patterns; off-ramps are where tracing usually ends and where freezes
   can be requested.
4. **Watch the splits** — peel chains (split into many, recombine) are deliberate obfuscation; the
   recombination wallet is the one that matters.
5. **Deliver a flow map** — source → hops → terminals with amounts and labels, plus the specific
   addresses to report to exchanges/authorities. This is graph work; `scripts/dune_run.py` pulls the
   hops and a Python/graph step expands the tree.

**Caveat:** transfer graphs explode combinatorially — bound depth and a minimum amount, and follow
value, not every dust transaction. State confidence: "consistent with laundering via X" not "is."

## How to deliver forensics

- Always a **confidence level** (low/medium/high) and the evidence behind it.
- Always the **counter-explanation** (market-maker, CEX funder, legitimate burst) you ruled out.
- A **score or checklist**, never a bare accusation. The honest output is "here are the signals,
  here's how strong, here's what would confirm or refute it."
