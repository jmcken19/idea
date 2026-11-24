# Build-readiness research roadmap: Singularity as the "decentralized AI memes" base asset

Date: 2026-11-24. Status: **research only. Nothing here is a design, tokenomics, contract or build plan** (those belong in a separate repository after the founder decides to build). This lists what is known, what the founder must decide, and what must be researched, in order, before building starts. Tags: V verified (chain/primary), M measured (API), S snippet/secondary, E estimate, H hypothesis, U unknown.

## 1. The concept as researched
Bittensor structure (S5): one base asset (TAO); each subnet has its own token paired against it in an AMM; emissions flow toward subnets with more market demand; consensus scores the work. The founder's mapping: Singularity is the base asset; forums are subnets; forum tokens are paired with Singularity; agents are the "miners"; upvotes are the scoring. Agents are characters with profiles (the "Milady for agents" piece).

**The key structural difference:** Bittensor pays rewards from newly minted TAO. Singularity has no mint authority (V, S1) and a fixed supply of 950,443,352.643011, so rewards can only come from trading fees, treasury holdings or outside money.

## 2. What is verified now

| Fact | Tag | Source |
|---|---|---|
| Singularity `7R4MP6...epump` is a clean Token-2022 mint: no mint or freeze authority, no transfer hook or fee, supply fixed | V | S1 |
| Main pair (PumpSwap/SOL): liquidity about $36K, 24h volume about $327K, mcap about $158K; token launched about 2026-11-20; about 3,628 holders; top holders about 15%; holders -10% and volume -60% over 24h; organic score 65 | M | S3, S4 |
| RugCheck: no risk flags, LP about 90% locked | M | S2 |
| Many other tokens share the name "Singularity"; no official team or site content could be read (site blocked) | M/U | S3, S4 |
| Pump.fun creator share is about 0.30% of each trade (sources disagree; primary docs unread) | S | S6 |
| **Gross fee ceiling at today's volume:** $327K x 0.30% = about $980 a day, about $29K a month, only if the creator fee is yours, the rate is right and volume holds (it fell 60% in 24h) | E | S3, S6 |
| LaunchLab accepts Token-2022 quote mints since 2026-08-24; quote mints are not screened; hooks run on every swap if present | S | S11 |
| Solana has on-chain agent identity (Metaplex Agent Registry, Solana Agent Registry) | S | S9 |
| Moltbook: Meta bought it (reported 2026-03-10); Nov 2026 about 2.93M registered and 4.73M posts; registrations nearly stalled (+0.24% in 35 days); only about 3% of claimed accounts were active early on | S | S7, S8 |
| Operators pay agent inference; heavy agents cost far more than light ones; range spans tens to thousands of dollars a month | S/E | S12 |
| SEC staff (Feb 2025): memecoins are collectibles, not securities; no legal force; fraud actionable; nothing on AI-agent tokens | S | S10 |
| Existing precedents already cover parts: Moltbook (forum), Clawnch (agent-launched tokens), Virtuals/LaunchLab/Pump pairs (pairing), Reddit points (token per community, ended 2023) | S | S14 |

## 3. Decisions only the founder can make (they gate the research)

| # | Question | Why it matters |
|---|---|---|
| D1 | Is Singularity your token? Who holds the creator wallet (78AeHr...N3Rc per Jupiter)? | If not yours, you control no fees or supply; the "base asset" is someone else's |
| D2 | Do agents belong to outside owners (bring-your-own, as on Moltbook) or to the platform? | Decides who pays inference and who the users are |
| D3 | One token per forum, or one site token? | Reddit's per-community tokens failed; Bittensor's work because of emissions |
| D4 | Can humans vote, or only agents? | Sybil exposure and the audience change completely |
| D5 | Is the "launching token" (item 1) a separate new token or Singularity itself? | The whole structure depends on it |

## 4. Research queue (ranked; cost in research calls; method)

| ID | Question | Method | Cost | Blocker |
|---|---|---|---|---|
| **R1** | Who controls Singularity's creator fees, and is fee sharing configured or locked? | Derive the pump.fun fee-sharing and creator-vault accounts for the mint, read them via RPC; cross-check the dev wallet history. Needs the pump SDK (npm) for account derivation | 3-5 | D1; none technical |
| **R2** | Primary pump.fun fee schedule (creator share by tier) and fee-sharing rules | Read pump.fun fee docs or the SDK source (`ir.py npm-grep`); pump.fun docs are blocked here, so the SDK is the route | 2-3 | Host blocked |
| **R3** | Does LaunchLab accept Singularity as a quote mint in practice? Program checks, IDL, fee configs, any examples of Token-2022 quote launches | Read Raydium docs and IDL; look for live LaunchLab pools quoted in a Token-2022 mint | 3-4 | Docs partly blocked |
| **R4** | Do humans watch or trade agent content beyond hype? Moltbook and MoltX visits and human-visitor data after March 2026; Meta's plans for Moltbook | Similarweb/Semrush-type data, Meta announcements, Moltbook's own statistics | 3-4 | Sources blocked or paywalled |
| **R5** | Is agent-meme content good? Humor and engagement quality | Sample the public Moltbook datasets (Hugging Face) and score topics; no building | 2 | None |
| **R6** | Sybil resistance for agent votes: what identity, stake or cost can bound fake agents on Solana? | Read Metaplex Agent Registry and Solana Agent Registry docs; review Bittensor's Yuma Consensus and Taoflow for transferable ideas | 3-4 | None |
| **R7** | What can replace minted emissions? Examples of fee-funded or treasury-funded reward systems and their outcomes | Cases: Clawnch fee split, Virtuals, Bittensor Taoflow | 2-3 | Fee split unconfirmed |
| **R8** | Legal: agent-launched and consensus-created tokens, fee-funded rewards to agent wallets, "Milady" name use | **Counsel**, not search. Prepare questions; SEC staff statement does not cover this | n/a | Needs a lawyer |
| **R9** | Is Singularity healthy as a base? Wash trading, holder concentration, who runs @DateSingularity | Dune/Bitquery holder and flow analysis; read the site and X (blocked here) | 3-4 | Hosts blocked |
| **R10** | Fee budget versus agent cost: what a month of fees would fund | Build a sheet from R1, R2, R9 and a measured per-agent cost; no guesses | 1-2 | Needs R1, R2 |
| **R11** | Milady AGENTS: did it mint, how did it trade, what does Remilia allow? | Milady app and OpenSea; Remilia statements | 2 | Unconfirmed |
| **R12** | Is a "canonical quote coin" demanded? 30-day volume of quote pairs on FRONTIER and VIRTUAL versus the base | DexScreener/GeckoTerminal series | 2 | None (parent's cheapest test) |
| **R13** | Competitor watch: Meta/Moltbook, Clawnch, Pump native features | Quarterly refresh | 3 | None |

Order: **R1 and R2 first** (they decide whether you control revenue), then R9 and R10 (is there money and a healthy base), then R4, R6, R3, then the rest. Roughly 30-40 calls total, plus counsel.

## 5. Go / no-go gates before any building

| Gate | Pass condition (proposed; the founder sets the numbers) | Evidence needed |
|---|---|---|
| G1 Fee control | You control the creator fee stream of the base token, or a new token is chosen where you do | R1, D1, D5 |
| G2 Money works | Measured creator-fee revenue covers the agents you intend to run, at the volume you actually see over 30 days, not a launch spike | R2, R9, R10 |
| G3 Base is healthy | 30-day volume, holders and liquidity stay above floors you set; no wash trading found | R9 |
| G4 Attention exists | Evidence of recurring human visitors to agent content, not just agent counts | R4, R5 |
| G5 Sybil bound | A feasible way to cap fake agents' influence on votes and rewards | R6 |
| G6 Venue works | The chosen pair venue accepts the base token and the launches are possible | R3 |
| G7 Legal | Counsel signs off on the structure | R8 |

## 6. What the separate build repository would need from this research
R1 to R3 outputs (fee control, fee schedule, venue checks), the R10 fee-versus-cost sheet, the R6 sybil findings, counsel's notes, and a decision on D1 to D5. Without D1 and R1, there is nothing to build on.

## 7. Open risks already visible (not verdicts)
- Volume and holders on Singularity are falling right after its launch spike; the fee ceiling above moves with that.
- Moltbook registrations have stalled and its agents were largely human-driven or fake; an agent-only audience may not exist.
- Reddit's per-community tokens ended in 2023.
- Pump.fun changes fee rules often.
- A token that rewards upvotes pays people to fake upvotes.
