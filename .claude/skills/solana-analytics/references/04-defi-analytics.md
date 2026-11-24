# 04 — DeFi Analytics by Vertical

DeFi is not one thing. A DEX, a lending market, a liquid-staking token, and a perp exchange each
have their own metric family and their own failure modes. Using DEX metrics on a lending protocol is
how analysts produce confident nonsense. Here is the right family per vertical, the Solana protocols
and tables involved, and the trap in each.

## DEX (AMM & CLMM)

**Protocols:** Raydium (AMM + CLMM), Orca (Whirlpools CLMM), Meteora (DLMM), Phoenix (orderbook),
Lifinity, SolFi. **Table:** `dex_solana.trades` (`project`, `amount_usd`, `trader_id`, `token_pair`).

**Metric family**
- Volume (Template 4), trades, unique traders, avg trade size (Template 5).
- Market share over time (Template 11) — the competitive story.
- Pair/liquidity concentration (Template 6) — is volume one-pair-dependent (risk) or diversified?
- Fees → revenue (Template 10) with the protocol's real fee tier; separate LP vs protocol cut.
- **CLMM-specific:** active-vs-inactive liquidity (concentrated liquidity means TVL can be large but
  *in-range* liquidity small), fee APR for LPs, and impermanent-loss exposure. In-range liquidity,
  not raw TVL, is what backs a quoted price — say which you mean.

**Trap:** aggregator routing (Jupiter) means a single user swap can touch several DEXs; attributing
that volume requires care about inner instructions (see `02`) — don't double count the aggregator
and the underlying venue.

## Lending markets

**Protocols:** Kamino, MarginFi, Solend, Drift (also perps). These are mostly **Anchor programs**;
check for a decoded table first, else decode deposit/borrow/repay/liquidate instructions per `02`.

**Metric family**
- **Supplied / borrowed (TVL & open debt)** per asset — the levels.
- **Utilization** = borrowed ÷ supplied per market. The single most important lending number: it
  drives interest rates and liquidation risk. High utilization = high yield but thin exit liquidity.
- **Net deposits flow** — daily supplied − withdrawn; reveals confidence shifts before TVL moves.
- **Liquidations** — count, USD value, and *who* got liquidated; spikes mark stress events and are a
  forensics/risk signal.
- **Health-factor distribution** — share of debt sitting near the liquidation threshold = systemic
  fragility. A protocol can look healthy on TVL and be one wick from a cascade.
- **Bad debt** — positions underwater past liquidation (collateral < debt); the real solvency metric.

**Trap:** rates and health factors are *point-in-time* and oracle-dependent. Reconstructing them
historically means replaying deposits/borrows/price — heavy. For current state, Helius/RPC or the
protocol's own API is often the honest source; say so rather than faking a historical curve.

## Liquid staking (LST) & native staking

**Protocols:** Marinade (mSOL), Jito (JitoSOL), Sanctum, native stake accounts. **Tables:** staking /
`solana.rewards` models, transfer tables for the LST mint, `prices.usd`.

**Metric family**
- **Staked SOL / LST supply** and its growth — the adoption level.
- **Exchange rate (LST ↔ SOL)** over time — should grind upward as rewards accrue; a *de-peg* in the
  market price vs the redemption rate is a risk/forensics signal.
- **Staking yield (APY)** from epoch rewards; compare LSTs on net yield after fees.
- **Validator/stake-pool concentration** — decentralization & MEV-capture read; concentration is a
  network-health story (the 21shares/BTC-metrics mindset applied to staking).
- **LST DeFi penetration** — how much LST is used as collateral elsewhere (composability & contagion
  surface).

**Trap:** market price ≠ redemption rate. An LST trading below its redemption value isn't always
broken (it can be a liquidity/withdrawal-queue discount) — distinguish a temporary market discount
from a real solvency de-peg before you call it.

## Perpetuals / derivatives

**Protocols:** Drift, Jupiter Perps, Zeta, Adrena. Mostly Anchor — decode or use a decoded table.

**Metric family**
- **Open interest (OI)** long/short and net skew — the core exposure level.
- **Volume** and **trader count** (like DEX, but leveraged notional ≠ spot).
- **Funding rate** over time — who pays whom; persistent skew is a positioning signal.
- **Liquidations** — count, USD, cascade clustering around price wicks.
- **PnL leaderboards / trader segmentation** — realized PnL per trader (Template 9 pattern), with the
  realized-vs-unrealized caveat.
- **Fees → revenue** for the protocol.

**Trap:** leveraged notional inflates "volume" vs spot — never compare a perp DEX's volume to a spot
DEX's without saying one is leveraged notional. OI is the honest size metric for perps.

## Cross-vertical: the composability / contagion view

Solana DeFi is densely composable: an LST is collateral in a lending market that backs a perp. When
analyzing systemic risk, trace the dependency: *if this LST de-pegs, which lending markets hold it,
and which perp/vault positions sit on those markets?* That cross-protocol exposure map — not any
single TVL — is the analysis that matters in a stress event, and it's a genuine gap most dashboards
ignore. Build it from holder/collateral tables (see `05`) joined across protocols.
