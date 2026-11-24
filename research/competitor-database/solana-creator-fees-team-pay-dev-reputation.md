# Competitor database: creator-fee distribution, team pay and deployer reputation (Solana and EVM)

Last updated 2026-11-24. Freshness: existence 90 days (re-check after 2027-02-22); traction 30 days.
Tags: V verified · C corroborated · S snippet only · M vendor marketing · U unknown (see `system/research-standards.md`).
"Seen in" lists the source IDs in the idea records that use these rows (`ideas/salary/sources.md`, `ideas/salary-team-record/sources.md`).

## A. Splitting creator / trading fees across wallets

| Product | What it does | Audience | Pricing / model | Traction (dated) | Evidence | Notes |
|---|---|---|---|---|---|---|
| **Pump.fun fee sharing** (native) | Splits a coin's creator fees by percentage across up to 10 wallets. Live Jan 9, 2026. Editable once since Mar 25, 2026. Any member can trigger distribution | Every Pump.fun coin | Free; part of the platform | 903,612 SharingConfig accounts on mainnet; 4.6% of a 3,000 sample had more than one recipient (slot ≈473.0M, Nov 23 2026) | **V** (SDK source, IDL, chain reads in salary `docs/research.md`) + **C** (The Block, Cointelegraph, CoinMarketCap, Brave New Coin, Jan 2026) | The native incumbent. CTO admin key can override a locked split |
| **Bags fee share** (native) | 1–100 fee claimers per launch, bps must total 10,000; claimers identified by X/Kick/GitHub handles; admin can edit claimers | Bags creators and partner apps | Free; 1% of volume to the royalty pool; partner program | Monthly fees $20.06M (Jan 2026) → about $186K (Oct 2026), DefiLlama via research-v2 | **C** (docs.bags.fm read Nov 23 per salary research; changelog and API reference seen Nov 24 as S) | Supports more payees than Pump, changeable recipients |
| **pumpdev.io: claim and distribute** (unverified lead; the reviewer could not find it again) | Claims Pump.fun creator fees and splits them among shareholder wallets on a recurring schedule (interval in hours); fee-sharing API | Pump.fun teams, devs | U | U | **S** (search summary, page not opened) | Closest match to Salary's "payday". Verify the page when hosts are allowed |
| **docs.j.tools: Creator Fee Claim** | Scans several creator wallets and claims from all of them in one action | Multi-coin creators | 0.75% of the claimed value | U | **S** | Claiming, not splitting |
| **PumpPortal: creator-fee API** | API to claim creator fees programmatically (can be scheduled by a bot) | Devs | U | U | **S** | A building block for DIY payroll |
| **xBot** | Claims creator fees about every 10 minutes, swaps them and pays holders | Holder-reward coins | U | U | **S** | Holder payouts, not team pay |
| **GitHub: fartnode, FARTNODESOL, hymet-distributor, best_buddy, openpumptrade/pumpkit, daronthedragon/dev-fee-harvester, 0xbl33p/pumpfun-tiktok-fee-share** | Open-source distributors that claim Pump.fun/Meteora creator fees and redistribute them (holders, creators, lenders) | Devs | Open source | 0–2 stars; pushed 2025-11 to 2026-11 | **V** for existence (GitHub search API metadata, Nov 24 2026); READMEs not read | Shows that DIY distributors are common and trivial |
| **Clanker splits (Base)** | Multiple reward recipients / custom splits at deploy (v4); older splits endpoint being retired | Base / Farcaster deployers | Protocol take: 20% of LP fees | Over $50M cumulative fees (research-v2, M) | **S** | Same feature on EVM |
| **Zora (Base) + 0xSplits** | Fixed reward split per coin; 0xSplits recipient contracts for multi-party payouts | Base creators | Protocol fee share | Volume down about 99.8% from peak (research-v2, M) | **S** | 0xSplits is the general EVM primitive for "split revenue to many wallets" |

## B. Team payroll / recurring contributor pay

| Product | What it does | Audience | Pricing / model | Traction (dated) | Evidence | Notes |
|---|---|---|---|---|---|---|
| **Streamflow** | Token vesting, payroll streams, recurring payouts, batch payments, locks (Solana) | Solana teams and DAOs | Locks: 0.16 SOL + 0.5% of tokens; verification $750 one time (salary research); stream fees U | Claims 40,000+ projects and $286M TVL | **V** program layout (salary decoders); **M** traction; **S** payroll features | Markets itself as "web3 payroll" |
| **Squads** | Multisig treasury, spending limits (per-member allowance that resets each period), recurring "Recipients", sub-accounts, USDC-to-bank payouts | Solana teams | Multisig 0.1 SOL one time (salary research); app plans U | Audited by Neodyme, OtterSec, Trail of Bits (vendor-stated) | **S/M**; Squads docs cited in salary review notes | Runs a team treasury with approval controls; the "who can change pay" problem |
| **Zebec** | Streaming payroll, enterprise payroll | Teams, enterprises | U | Claims $500M+ annual payroll volume for 250+ clients | **M/S** | |
| **Request Finance, Rise, Deel, Franklin** | Crypto/stablecoin payroll, invoicing, contributor payments, KYC | DAOs, web3 companies | SaaS / fees | U | **S/M** | The web2-grade payroll layer, with compliance |
| **Sablier / Superfluid / LlamaPay** | Token streaming (EVM) | EVM teams | Protocol | U | Not checked in this pass (U) | Add on the next refresh |

## C. Deployer / team track record ("dev history")

| Product | What it does | Audience | Pricing / model | Traction | Evidence | Notes |
|---|---|---|---|---|---|---|
| **MadeOnSol Deployer Hunter** | Lifetime launches, bond rate, tier and full token history per Pump.fun deployer wallet; free checker; profile pages | Traders | Free checker (other tiers U) | Claims 561,645 deployer wallets tracked; 1.89% bond rate (2026) | **S/M** | Direct overlap with the "Team Record" pivot |
| **Mobula: token dev history API** | Chronological feed of a deployer's fee claims, swaps and transfers, for rug detection | Devs / terminals | API pricing U | U | **S** (docs.mobula.io) | B2B data layer: what a terminal badge would be built on |
| **Rug Munch Intelligence** (MCP) | Classifies deployers as legitimate builder / suspicious / serial rugger | Agents, devs | $0.06 per check | U | **S** (Glama listing) | |
| **Noesis bot /dev** | Telegram dev analyzer: past launches, success rate | Traders | U | U | **S** | |
| **DEXTools** | Guidance and tooling for spotting recycled deployers | Traders | Freemium | U | **S** | |
| **Apify: Pump.fun dev wallet profiler** | Scraper actor that profiles dev wallets and PnL | Devs | Pay-per-use | U | **S** | |
| **DexScreener Enhanced Token Info** | Paid profile/verification for a token's team info | Token teams | $299 (list $499), salary research Nov 23 | U | **S** (salary research) | Evidence that teams pay for trust signals; also owns the distribution |
| **GMGN** | Token pages flag insiders, snipers, bundled buyers; Dev Sell auto-exit; wallet lookup | Traders | Trading fees | U | **S** (salary-team-record S12) | Terminal owns trader attention |
| **Mobula Wallet Deployer endpoint** | A deployer's other tokens across PumpFun, PumpSwap, Meteora DBC launchpads (Bags, Moonshot, Believe) | Devs / terminals | U | U | **S** (salary-team-record S13) | Removes the "cross-launchpad" difference |
| **Doxxxed.fun** | KYC-verified creator launchpad on Solana; listed for sale at $75k | Builders | U | Listed for sale (weak traction signal) | **M** (salary-team-record S16) | A team-trust launchpad that didn't take off |
| **RugCheck, Axiom, Photon, Bubblemaps** | Risk reports, dev holdings/sells, holder clusters on trading terminals | Traders | Free/terminal fees | U | Existence widely known; dev-history features **U** in this pass | Check on refresh; terminals own the trader's attention |
