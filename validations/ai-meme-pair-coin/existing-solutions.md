# Stage 2: Existence check (kill-first)

Question: **who already solves this, and why should this exist anyway?**

Scope note: the founder's note is four moves, not one product, and the gist has not arrived. Each component is checked separately. "Canonical AI meme pairing coin + pairs site" (component A) is the core.

## Search coverage

| Channel | Done? | Queries / where | Hits |
|---|---|---|---|
| Native platform features | Yes | Pump.fun custom pairs, Raydium LaunchLab, Pump Mayhem/tokenized agents (S1, S2, S5, S12) | Pump Custom Pairs (Sep 2026), LaunchLab any-pair, Mayhem Mode |
| Web search, 3+ phrasings | Yes | 9 searches (custom pairs; AI index token; Milady AGENTS; LaunchLab; agent post-mortem; tracker sites; Virtuals pairing; Mayhem; plus first-pass searches) | see equivalents |
| GitHub repositories | Partly | 1 query ("memecoin pairs explorer quote token solana") = 0 repos | none found; thin coverage |
| npm / crates / PyPI | No | not needed for the verdict | n/a |
| Protocol docs and directories | Partly | None opened (pages blocked); relied on news snippets | gap |
| Token launches with the same pitch | Yes | DexScreener + Jupiter + GeckoTerminal name and CA lookups (S6-S9) | FRONTIER-quoted pairs; AI Frontier; Singularity copies |
| Bots, trackers and APIs | Partly | 1 search (S13) | general trackers; no AI-pair leaderboard |
| Other chains | Yes (EVM) | Virtuals on Base (S3); Clanker on Base (S12) | Virtuals is the incumbent AI pairing coin |
| Web2 or adjacent industries | No | | n/a |
| Recent launches (last 90 days) | Yes | Pump Custom Pairs and LaunchLab (Sep 2026) | native features |
| Discontinued / abandoned projects | Blocked: no Wayback or archive access (proxy 403); news snippets only | OSOL100 AI index (Dec 2024, status unknown, S11); Accelerando token dormant (S8) | |

## Equivalents found

| Component | Product | What overlaps | Evidence | Overlap |
|---|---|---|---|---|
| A. Canonical AI pairing coin | **Virtuals ($VIRTUAL)** | Every agent token pairs against VIRTUAL; about 17,000 launched; the incumbent "canonical AI pair" | S3, S4 [S] | **Full** (concept), on Base |
| A. Pairing coin | **Pump.fun Custom Pairs** | Launch tokens against non-SOL assets (93 quote assets); thin depth | S1 [S] | Partial/full (native feature) |
| A. Pairing coin | **Raydium LaunchLab any pair; StonkFun** | Any supported quote token for launches | S2 [S] | Full (native feature) |
| A. Pairing in practice | **FRONTIER already quoted by other tokens** | BUBBLE, BUTTHOLE, Frongus trade quoted in FRONTIER | S7 [M] | Full (it already exists, informally) |
| A. Pairs site | DexScreener / GeckoTerminal token pages list every pair of a token; Solmemecap, MemeScout, MadeOnSol | Pair display and trackers | S7, S13 [M/S] | Partial. No AI-pair ratio leaderboard found (a gap, not demand) |
| A. Index | OSOL100 (AI index, Dec 2024), Basket, MemDex | Basket/index tokens | S11 [S] | Adjacent; no verified active AI memecoin index |
| B. AI agent runs fees | Clanker, Agency, Metaplex agent treasuries, Pump Tokenized Agents, Mayhem Mode | Agent controls treasury/fees/buybacks | S5, S12 [S] | Full for the mechanic |
| B. Accelerando precedent | Accelerando itself ("AI religion", paid bounty) | The founder's own reference token is dormant ($6.8K, 0 volume) | S6, S8 [M] | n/a (it is evidence against, not a competitor) |
| C. Milady for agents | Milady AGENTS drop (ERC-8004/8041) | Same brand, same concept | S10 [S] | Full if minted; mint status unconfirmed |

## Easy replicators

| Who | Why they could ship it fast | Evidence |
|---|---|---|
| Pump.fun | Already shipped Custom Pairs, Mayhem Mode, tokenized agents within a year | S1, S5, S14 |
| Raydium / StonkFun | Any quote token already supported | S2 |
| Virtuals, Clanker | Already operate agent launchpads with their own base pairs | S3, S12 |
| DexScreener | Can add a pair view in a release | S7 (assumption, no evidence of intent) |

## Gate 2 decision

- [x] An equivalent exists (A: Virtuals plus native pairs; B: several; C: Milady).
- [ ] No equivalent found.

### Differentiation test

1. **What would a customer get that the existing option does not?** The founder's note names no difference. Not stated, so none can be credited.
2. **Evidence customers want it?** No. The one observable proxy for demand for a pairing coin is the FRONTIER-quoted pairs, and they are tiny: BUBBLE/FRONTIER about $1.5K a day, Frongus about $67, BUTTHOLE about $3, against liquidity of $4K to $16K, while FRONTIER itself trades about $2.2M a day (S6, S7) [M]. AI agent tokens fell 75-90% (S4) [S].
3. **Could the incumbent ship it in a release?** Yes for Pump.fun, Raydium and DexScreener (native features, S1, S2, S14).
4. **Would you pitch it if the incumbent did not exist?** Not answerable; no pitch beyond "canonical" is given.

**Outcome for the framing as submitted: no evidenced real difference (questions 1 and 2 unanswered). Per rule, that points to REJECTED.** It is held at NEEDS MORE RESEARCH rather than REJECTED because (a) the gist with the actual scope has not been read, (b) every competitor claim is snippet or secondary grade (no primary doc opened), and (c) a differentiator may exist that the founder has not stated yet. Do not read this as "promising".

### Angles the equivalents do not cover (untested; none has evidence, they are brainstorm threads only)
- Pump.fun Custom Pairs is a fixed whitelist (93 assets) and permanent; LaunchLab accepts any quote token. A venue for AI-themed launches quoted in an AI coin is not covered by Pump.fun. No evidence anyone wants it; Bags, Believe and Zora launch venues collapsed 90%+ (S14).
- A neutral "pairs map" of which AI coins are quoted in which. Not found as a product (S13). A gap is not demand.
- The agent-run fee mechanic aimed at a different audience (for example holders, not traders). No evidence either way.
