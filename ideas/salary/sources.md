# Sources

Type: `primary` · `onchain` · `repo` · `secondary` · `snippet` (search result only, page not opened).

| ID | Source | Locator | Type | Published | Accessed | Supports |
|---|---|---|---|---|---|---|
| S1 | Salary research log (SDK source, IDLs, live mainnet reads) | repo:jmcken19/salary/docs/research.md | primary | 2026-11-23 | 2026-11-24 | Pump fee sharing mechanics; 903,612 configs; 95.4% single-recipient; Bags claimers; Streamflow/Jupiter fees; DexScreener $299 |
| S2 | Salary product decisions (source of truth) | repo:jmcken19/salary/docs/PRODUCT-DECISIONS.md | primary | 2026-11-23/24 | 2026-11-24 | Repositioning; "real but thin" admission; revenue OPEN; 1% fee removed |
| S3 | Salary research-v2 consolidated report | repo:jmcken19/salary@claude/gracious-wozniak-andkx3/docs/research-v2/00-CONSOLIDATED.md | secondary (built from snippets) | 2026-11-24 | 2026-11-24 | Pivot to Team Record; legal risk table; untested kill tests |
| S4 | Salary research-v2 launchpad landscape | repo:jmcken19/salary@claude/gracious-wozniak-andkx3/docs/research-v2/01-landscape.md | secondary (built from snippets) | 2026-11-24 | 2026-11-24 | Launchpad fees and collapse data; switching patterns; "that is the opening for Salary" |
| S5 | Salary git history, all 7 branches (59 commits) | repo:jmcken19/salary (git log --all) | primary | 2026-11-23 to 2026-11-24 | 2026-11-24 | Timeline: 35 web/design commits; market research at commits 54–59 |
| S6 | `@pump-fun/pump-sdk` release history and package contents | https://registry.npmjs.org/@pump-fun/pump-sdk | repo | 2026-01-09 (v1.25.0) | 2026-11-24 | `sharingConfig` absent up to 1.24.0 (2025-12-05), present from 1.25.0 / 1.23.0-devnet.2 (2026-01-09) |
| S7 | The Block: Pump.fun overhauls creator fees | https://www.theblock.co/post/384975/pump-fun-overhauls-creator-fees-token-launches-highest-daily-count-since-september | snippet | 2026-01-09 | 2026-11-24 | Fee sharing launch, ownership transfer, revoke authority |
| S8 | Cointelegraph: Pump.fun revamps creator fees, fee sharing, CTO controls | https://cointelegraph.com/news/pumpfun-revamps-creator-fees-fee-sharing-cto-controls | snippet | 2026-01 | 2026-11-24 | Creators and CTO admins can assign fee shares |
| S9 | Brave New Coin: creator fee sharing system | https://bravenewcoin.com/insights/pump-fun-introduces-creator-fee-sharing-system-to-rebalance-platform-incentives | snippet | 2026-01-09 | 2026-11-24 | Launched Jan 9 2026, split across several wallets |
| S10 | Bags docs: changelog and fee-share API | https://docs.bags.fm/api-reference/create-fee-share-configuration | snippet | n/d | 2026-11-24 | 1–100 claimers, bps total 10,000 (S1 read the docs directly on 2026-11-23) |
| S11 | pumpdev.io: Distribute Pump.fun creator fees | https://pumpdev.io/claim-distribute | snippet | n/d | 2026-11-24 | Scheduled claim and split among shareholder wallets |
| S12 | docs.j.tools: Creator Fee Claim | https://docs.j.tools/tools/launch/creator-fee-claim | snippet | n/d | 2026-11-24 | Multi-wallet claim tool, 0.75% fee |
| S13 | PumpPortal: claiming creator fees | https://pumpportal.fun/creator-fee/ | snippet | n/d | 2026-11-24 | Programmatic claim API |
| S14 | Streamflow: web3 payroll | https://streamflow.finance/blog/web3-payroll | snippet | n/d | 2026-11-24 | Payroll streams, recurring payouts (vendor claims) |
| S15 | Squads docs: spending limits and treasury management | https://docs.squads.so/main/development/reference/spending-limits | snippet | n/d | 2026-11-24 | Per-member allowances, Recipients for recurring payments |
| S16 | GitHub repository search (creator-fee distributors, Solana payroll) | https://api.github.com/search/repositories?q=creator+fee+distributor+solana | repo | 2025-11 to 2026-11 | 2026-11-24 | 4 open-source creator-fee distributors; 94 "solana payroll" repos |
| S17 | Salary 20-coin blind study | repo:jmcken19/salary/docs/study-results.md | onchain | 2026-11-23 | 2026-11-24 | 20/20 splits locked; 0/20 team locks |
| S18 | Clanker docs: deploy token with splits / v4 recipients | https://clanker.gitbook.io/clanker-documentation/authenticated/deploy-token-w-splits-v3.1.0 | snippet | n/d | 2026-11-24 | Same feature on Base |
| S19 | Request Finance / Rise / Deel payroll roundups | https://www.riseworks.io/blog/complete-guide-to-crypto-payroll-in-2026 | snippet | 2026 | 2026-11-24 | Established crypto payroll category |
| S20 | Cointelegraph via Yahoo: Pump.fun co-founder says the fee model failed | https://finance.yahoo.com/news/pump-fun-co-founder-says-125617496.html | snippet | 2026-01 | 2026-11-24 | Creator fees had little effect on the average deployer |
| S21 | Search summary of Pump.fun March 2026 recipient-change restriction (Cointelegraph creator-fee-cap article / MEXC news reposts) | https://cointelegraph.com/news/pump-fun-creator-fee-cap-update-memecoin-model | snippet | 2026-03 (per snippet) | 2026-11-24 | Only one post-launch change to fee recipients, then the config is permanently locked ("anti-griefing"); no complaints about the 10-wallet cap found |
| S22 | Crypto Briefing: Pump.fun introduces Holder Rewards and sunsets Cashback mode | https://cryptobriefing.com/pumpfun-holder-rewards-cashback-deprecated/ | snippet | n/d (2026) | 2026-11-24 | A further native creator-fee routing option (to holders); title only |
| S23 | GitHub repository search "pumpfun fee sharing" | https://api.github.com/search/repositories?q=pumpfun+fee+sharing | repo | 2026-04 to 2026-11 | 2026-11-24 | openpumptrade/pumpkit (fee-sharing building blocks, pushed 2026-11-18), daronthedragon/dev-fee-harvester (batch-claims team fee-sharing fees), 0xbl33p/pumpfun-tiktok-fee-share; all 0–2 stars (descriptions only, code not read) |
