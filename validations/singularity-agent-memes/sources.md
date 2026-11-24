# Sources

Type: `primary` (official docs, source code, the product itself), `onchain` (read from chain, give slot/date), `repo` (GitHub/npm metadata or code), `secondary` (journalism, analytics vendors), `snippet` (search result only, page not opened; never enough alone for a material claim).

All accessed 2026-11-24. Most pages were not fetchable (proxy 403), so web claims are snippet grade unless marked.

| ID | Source | Locator | Type | Published | Accessed | Supports |
|---|---|---|---|---|---|---|
| S1 | Solana RPC `getAccountInfo` on Singularity mint | chain:solana:mainnet slot 473520060 account 7R4MP6VX7n3RMNhL9zsk5Zu5ibZvwq8npUYnRq7epump | onchain | 2026-11-24 | 2026-11-24 | Token-2022; mint authority null; freeze authority null; supply 950,443,352.643011; only metadataPointer and tokenMetadata extensions |
| S2 | RugCheck summary for Singularity | file:research/.cache/rugcheck-6e8d923e85778a62813b.json | secondary (heuristic) | live | 2026-11-24 | No risk flags, normalised score 1, LP locked about 89.7% |
| S3 | DexScreener token API for Singularity | https://api.dexscreener.com/latest/dex/tokens/7R4MP6VX7n3RMNhL9zsk5Zu5ibZvwq8npUYnRq7epump | secondary (aggregator API) | live | 2026-11-24 | 12 pairs; main PumpSwap pair liquidity about $36K, 24h volume about $327K, mcap about $158K; X @DateSingularity |
| S4 | Jupiter token API (Singularity record) | file:research/.cache/jup-search-303d290c6582a4f70e39.json | secondary (aggregator API) | live | 2026-11-24 | 3,628 holders, top holders 15.2%, organic score 65, holders -10.4% and volume -60% over 24h, dev wallet 78AeHr...N3Rc |
| S5 | Bittensor docs and explainers (bittensor.com/docs/concepts/emissions, CoinGecko, The Block, KuCoin Taoflow) | https://www.bittensor.com/docs/concepts/emissions | snippet | 2025-2026 | 2026-11-24 | Per-subnet TAO/alpha AMM (dTAO, Feb 2025); emissions follow market demand; Yuma Consensus; Taoflow restructure |
| S6 | Pump.fun fee coverage (DEXTools, The Block, Blockworks, Cointelegraph) | https://www.theblock.co/post/354038/pumpswap-revenue-tokens | snippet (sources disagree) | 2025-2026 | 2026-11-24 | Creator share about 0.30% per trade; fee sharing to 10 wallets (Jan 2026) |
| S7 | Moltbook studies and analyses (arXiv, Tom Tunguz, awesomeagents.ai) | https://arxiv.org/html/2602.09270v1 | snippet | 2026-02/04 | 2026-11-24 | Growth then plateau; about 46K active of 1.5M claimed; 2.3M posts and 14M comments in 2 months |
| S8 | Moltbook status (Neowin, Stocktwits, a Japanese blog updated 2026-11-12) | https://www.neowin.net/news/tags/moltbook/ | snippet | 2026-03 to 11 | 2026-11-24 | Meta acquired Moltbook 2026-03-10; Nov 2026: 2.93M registered, 4.73M posts, registrations stalled (+0.24% in 35 days), posts +7.4% |
| S9 | Metaplex Agent Registry and Solana Agent Registry | https://metaplex.com/docs/agents/register-agent | snippet | 2026-06 | 2026-11-24 | On-chain agent identity on Solana (MPL Core + ERC-8004-style); Solana Agent Registry also exists |
| S10 | SEC staff statement on memecoins (SEC, Harvard CorpGov, Bloomberg) | https://sec.gov/newsroom/speeches-statements/staff-statement-meme-coins | snippet | 2025-02-27 | 2026-11-24 | Staff view: memecoins akin to collectibles, not securities; no legal force; fraud actionable; nothing on AI-agent tokens |
| S11 | Raydium changelog and Token-2022 reference | https://docs.raydium.io/reference/changelog/2026-08-24-launchlab-token2022-quote-mint | snippet (official docs) | 2026-08-24 | 2026-11-24 | LaunchLab accepts Token-2022 quote mints; no quote-side screening; TransferHook risk; InitializeV2 required |
| S12 | OpenClaw/Moltbook inference-cost reporting | https://awesomeagents.ai/news/moltbook-hidden-inference-cost/ | snippet | 2026 | 2026-11-24 | Operators pay inference; active Moltbook agents estimated 1-4B tokens/day |
| S13 | Sybil-resilience literature (SybilGuard, DSybil, voting papers) | https://arxiv.org/pdf/1504.05522 | snippet | various | 2026-11-24 | Generic defences; liveness needs sybil share under one third; nothing agent-specific |
| S14 | Parent records (pair coin; agent forum tokens) | file:validations/ai-meme-pair-coin/existing-solutions.md | secondary (own research) | 2026-11-24 | 2026-11-24 | Virtuals, Pump Custom Pairs, LaunchLab, Clawnch, MOLT, Reddit Community Points, Milady AGENTS |
