# Stage 2: Existence check (kill-first)

First pass: 1 web search, 2026-11-24. **Second pass (audit 2, same day):** 12 WebSearch, about 40 npm/GitHub calls (about a third over budget), and a fresh adversarial review (5 WebSearch, 6 npm-grep). Full detail: `revalidation-2026-11-24.md`. The tables below reflect the second pass.

## Search coverage

| Channel | Done? | Where | Hits |
|---|---|---|---|
| Native platform features | Partly | Pump.fun split recipients are public on-chain data [V: S41]; Bags SDK returns each token's creators, fee shares and verified X handles [V: S39]; Pump.fun profile UI not verifiable (blocked) | 2 |
| Web search | Yes | "pump.fun dev history checker deployer past coins rug track record" | 6 tools [S2–S8] |
| GitHub | Yes | Deployer-reputation, dev-history and serial-rugger queries [V: S26] | 7+ small repos, 0–4 stars |
| Terminals (GMGN, Axiom, Photon, DexScreener, RugCheck) | Partly | GMGN official CLI code [V: S25, S40]; DexScreener API (no deployer history) [V]; Axiom/Photon/RugCheck pages blocked | GMGN full equivalent |
| Vendor APIs (Mobula, MadeOnSol, Rug Munch) | Yes | SDK/README code [V: S19, S21, S23] | 3 |
| Recent launches (last 90 days) | Yes | GitHub created:> queries [V: S26] | 1 (openbb-pumpdata) |
| Discontinued / abandoned projects | Yes | Talent Protocol commercial wind-down [C: S30]; Doxxxed.fun for sale [M: S16]; Wayback blocked | 2 |
| Other chains | Partly | Talent Protocol (Base, builder score), CertiK KYC [S: S28]; Gitcoin/Human Passport not searched | Adjacent |

## Equivalents found

| Product | Overlap | Evidence | Overlap |
|---|---|---|---|
| MadeOnSol Deployer Hunter | Every token a deployer launched, bond rate, tier; free checker; profile pages | [S: S2, S3] | **Full** for deployer history |
| Mobula token dev history API | Deployer activity feed (fee claims, swaps, transfers): the data layer a terminal badge needs | [S: S4] | Full (B2B) |
| Rug Munch Intelligence | Classifies deployers builder / suspicious / serial rugger, $0.06 per check | [S: S5] | Full (paid) |
| Noesis /dev, DEXTools, Apify profiler | Dev launch history and success rate | [S: S6, S7, S8] | Full / partial |
| Jupiter Studio vesting; Streamflow/Jupiter locks | Locked team allocations at launch | [S: S10] [V: S9] | Partial (Team Launch) |
| DexScreener Enhanced Token Info | Paid team/profile info on the dominant screener | [V: S9] | Partial (team-trust badge, owns distribution) |

## Second-pass equivalents (direct evidence)

| Product | Overlap | Evidence | Overlap |
|---|---|---|---|
| **GMGN OpenAPI / CLI + `gmgn-dev-score` skill** | Creator launch count, creator hold/sell status, dev-team hold rate, rug ratio, lock summary, a creator's created tokens; a skill answering "has this creator rugged before / is this team trustworthy" | [V: S25, S40] | **Full** for the trader-facing job (UI display U) |
| **Mobula** | Per-token deployer activity; wallet-deployer listing; `deployerTokensCount`, `migrationRate` on token objects; protocols pumpfun, pumpswap, meteoradbc, clanker | [V: S19] | Full for cross-launchpad deployer history (exact launchpad coverage U) |
| **MadeOnSol** | Deployer reputation leaderboard, trajectory, tiers; paid per call | [V: S21] | Full |
| **Rug Munch** | Deployer classification, $0.06 per check | [V: S23] | Full |
| **Bags SDK** | Per-token team list with fee-split shares and verified X handles | [V: S39] | Covers "team roster + fee recipients" for Bags coins |

Residual not shipped by anyone verified: **lock cancel authority + payday history** in one record. No demand evidence for it at any level.

## Easy replicators

| Who | Why they could ship it fast | Evidence |
|---|---|---|
| GMGN | Already returns lock summary, creator history, team hold rate; publishes a dev-score skill | [V: S25, S40] |
| Mobula | Token-level deployer fields and wallet deployer endpoint; widely used SDK | [V: S19] |
| MadeOnSol / Rug Munch | Deployer-reputation APIs already sold per call | [V: S21, S23] |
| Bags | Already exposes team roster and fee shares per token | [V: S39] |
| Any indexer | Split recipients and lock settings are public account reads | [V: S9, S41] |

## Gate 2 decision

- [x] An equivalent exists. Differentiation test:

1. **What would a customer get that the existing option does not give them?** Adding team roster, lock settings (who can cancel), fee-split recipients and payday history to deployer history, and showing it across launchpads. A real but small extension: these fields are a few account reads [V: S9]. Second pass: Bags already ships roster and fee shares [V: S39], and GMGN already ships lock summary [V: S40], so only lock cancel authority and payday history remain.
2. **Evidence customers want that difference?** **None.** The proposal's own tests (census, 20-coin prototype, concierge launch, terminal partner) were never run [S1]. (−) In Salary's blind study (n=20, random multi-wallet coins, illustrative, not representative) none had team locks [V: S9]. (−) Accountability demand appears only in curated raises (MetaDAO), not meme launches [S: S10]. (+) Teams do pay $299 for DexScreener profile info [V: S9], which shows willingness to pay for trust signals, to the platform that already owns the distribution.
3. **Could an incumbent ship it in one release?** Yes. Lock and split fields are public on-chain accounts; MadeOnSol, Mobula or a terminal could add them.
4. **Would you still pitch it if the incumbents didn't exist?** It was pitched as a gap ("no trusted developer reputation" [S1]) only because the existing tools hadn't been looked for.

**Gate 2 result (second pass): FAIL → REJECTED, now on vendor-code evidence.** The core is an existing, crowded, mostly free category. The extension is copyable and has no demand evidence.
