# AI meme pair coin: pre-gist context research

Date: 2026-11-24. Status: **context only, not validated.** Written before the founder's gist arrives. Used 3 of 3 brainstorming searches (standard mode), all web-search snippets, so everything below is S-grade at best. Nothing in this folder is a verdict.

## The founder's raw note (verbatim)
1. Launching token
2. Singularity paired w/ Frontier index. Then we make it the canonical AI meme pairing coin. Make a website that shows all of the pairs etc
3. Do some shit with an AI agent at the helm with creator fees. Could probably run back Accelerando idea in some regards
4. Milady but for AI agents

Gist with full scope: to come.

## What the three searches found

### 1. "Singularity" + "Frontier index" (no pairing found)
Nothing links a Singularity token to a Frontier index. Separate things that share the words:
- [The Singularity (SINGULARITY)](https://fxempire.com/crypto/the-singularity): Base project built around an AI robot character (ION).
- [Singularry (SINGULARRY)](https://invezz.com/markets/crypto/singularry/): AI-themed memecoin on BNB Chain ("hyperstition", meme distribution). Different token.
- [AI Frontier (FRONTIER)](https://phantom.com/tokens/solana/BEJv7pgReBcjN623K55HGLyQL95BzzF7d7ZEGzbC5mRV): Solana token, about $40K market cap, 15 holders, unverified.
- [Ornn Token Price Indices (OTPI)](https://theinnermostloop.substack.com/p/the-first-frontier-ai-token-price): benchmark pricing the API tokens of frontier AI labs (Anthropic, OpenAI). Not a memecoin index.
- Unknown which, if any, the founder means. Wait for the gist.

### 2. AI agent at the helm of creator fees (crowded, active)
- [Clanker](https://cointelegraph.com/news/clanker-ai-memecoin-fees-355k-tokens): 355,179 tokens deployed, ecosystem cap about $172.3M, $34.4M creator fees earned (snippet figures).
- [Agency](https://coinranking.com/coin/S-OPFAGWQ+agency-agency/about): each token gets an AI "mind" managing treasury, buybacks, burns, holder rewards.
- [Metaplex agent finance](https://www.metaplex.com/docs/agents/agent-finance): creator fees route to an agent-controlled treasury (Asset Signer PDA); an off-chain operator signs claims, revocable per asset.
- [Pump.fun Tokenized Agents](https://thedefiant.io/news/defi/pumpfun-launches-automated-buyback-tool-for-ai-agent-tokens): agent SOL/USDC earnings tied to a buyback and burn schedule.
- [Pump.fun fee redirect lock](https://www.kucoin.com/news/flash/pump-fun-restricts-creator-fee-changes-to-prevent-abuse-on-memecoin-launchpad): one post-launch change, then permanently locked.
- Not covered: Truth Terminal, Aeon (search returned nothing on them).
- "Accelerando" returned nothing. Working assumption (from model knowledge, unverified here): Charles Stross, 2005, AI-run corporations and "Economics 2.0". Confirm in the gist.

### 3. "Milady for AI agents" (partly adjacent already)
- Milady Maker: [10,000 PFPs by Remilia](https://opensea.io/collection/milady/overview), Ethereum, Aug 2021; CULT token.
- Community-run elizaOS notes ([Feb 2026 update](https://elizaos.github.io/knowledge/ai-news/elizaos/md/2026-02-22.md)): Milady announced an **AGENTS** drop on ERC-8004 / ERC-8041, free mint plus upgraded mints for elizaOS holders, 2,138 per chain across ETH, BSC, Base, Solana. Unconfirmed; mint status unknown.
- Jan 2026 report: Milady volume rose about 100% to about $500K after Vitalik changed his avatar to one.

## Reused from existing repo research (S/M grade, see research/INDEX.md)
- Pump.fun made about 78% of new Solana tokens Nov 2025 to Oct 2026; fees concentrated in a few dozen coins.
- Creator-payout platforms (Bags, Zora, Believe) fell 90-99%+ from peaks.
- Native features absorb tools; flow beats features; challengers' leads faded in 4-8 weeks.
- Source: `research/market-landscape/solana-launchpads-2026.md`, `research/industry-trends/memecoin-platform-patterns.md`.

## Open questions for the gist
- What exactly are "Singularity" and "Frontier index": existing tokens, ones to be launched, or an index of AI-lab tokens?
- What is a "pair" here: a trading pair, a thematic pairing, or a basket?
- Which chain and launchpad?
- What does the agent actually decide, and what is the token necessary for?
- How does item 4 differ from Milady's own AGENTS drop and the ERC-8004 agent-identity work?
- Is there any evidence that people want a "canonical pair" site, as opposed to it being unbuilt?

## Not yet checked (needs budget, only on request)
Whether a pair/ratio-tracking site for AI memecoins exists; Truth Terminal and Aeon details; Milady AGENTS mint status; ERC-8004 adoption.

---

## Correction and DexScreener check (2026-11-24, 6 of 12 discovery calls used)

Founder flagged that my token and market sourcing was off and that Accelerando is a memecoin. The web-search token facts above are **S-grade and should not be relied on**; the figures below come from DexScreener search (`ir.py fetch dexscreener-search`, cached in `research/.cache/`). Pair-level market caps are noisy (e.g. one BSC "Singularity dot Com" pair shows a bogus $690B), so treat them as rough.

- **Accelerando:** DexScreener search returns **0 pairs** for "accelerando", "accelerand" and "accelerando ai". Not found by name. Needs the contract address or ticker from the gist (could be unlaunched, renamed, or indexed under another name).
- **Singularity:** many unrelated tokens share the name. Most liquid Solana one: `7R4MP6VX7n3RMNhL9zsk5Zu5ibZvwq8npUYnRq7epump` (pumpswap, pair created about 2026-11-20, 24h volume about $320K on the main pair, about $30K liquidity, market cap roughly $100-200K, site singularitydotcom.com, X @DateSingularity). Also a Base "Singularity AGI" (`0x2631c4...fb3C`), a BSC and a Solana "Singularity dot Com", and older "The Singularity" tokens on Solana, Ethereum and BSC (small). Which one the founder means is unknown.
- **Frontier:** "AI Frontier" on Solana (`58QyXQ1UDgHh64EiTsCeevVM9cLPqBDNf3qZE6EdfUhZ`, pairs created 2026-10-19 onward, market cap roughly $175K on the SOL pair, 24-hour volume about $2K on the SOL pair at the time of the check). Also copies of "AI Frontier" on Robinhood chain and Arc, and unrelated "We Must Pace the Frontier" and "The Frontier" tokens. The earlier "AI Frontier, $40K, 15 holders" snippet was a different address (`BEJv7...`) and should be disregarded.
- **Observed pairing mechanic (the most useful finding):** other tokens are trading **quoted in FRONTIER** (`BUBBLE/FRONTIER`, `BUTTHOLE/FRONTIER`, `Frongus/FRONTIER`), and Singularity and AI Frontier also show pairs quoted in other small tokens (CSR, CAJUNR, ILR). So a "canonical AI meme pairing coin" plausibly means a token that other launches use as their quote asset. This is consistent with the repo's earlier note that Pump.fun shipped custom pairs. Unverified: how these pairs were created, and whether volume is real.
- **Not shown to exist by this check:** a site that lists AI-meme pairs. Not searched yet.

## Accelerando CA check (2026-11-24)

CA from founder: `HiNkp9CdKqTgPtB6WnnrrUAu9YwQqnrvT6Ceuxoypump` (Solana).
- **DexScreener** `/tokens/<CA>`: `pairs: null` (not listed or not indexed). Cause unconfirmed; the pool is dormant, which may be why.
- **GeckoTerminal** finds it: pool "Accelerando / SOL" on **PumpSwap** (`E3ryCiBNosokYEg84pCHx6j5bfZ8tJbkqQzJxrV7ZxZe`), created 2026-01-30, FDV and market cap about $6.8K, liquidity about $9K, **zero transactions and zero volume in the last 24h** (so effectively dormant). One pool only.
- **RugCheck** summary: one risk flag, "Creator history of rugged tokens" (danger, normalised score 53). That is an automated heuristic on the creator wallet, not proof about this token. LP locked 0%.
- Why my name searches missed it: DexScreener has no entry for it at all, so "accelerando" returned nothing there.
- Unknown: holder count and concentration, creator wallet and its history, who is behind it, what the coin's story is, whether it is the founder's own token or one they want to build around.
