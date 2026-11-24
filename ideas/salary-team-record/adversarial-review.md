# Stage 6: Independent adversarial review

Reviewer: adversarial-reviewer (independent subagent, inverse-check + attack table), 2026-11-24

Input given to the reviewer: the claims and sources only, not the pitch. Files read: existing-solutions, competitor-analysis, market-research, commercial-analysis, technical-feasibility, sources, plus system research-standards and lessons-learned. Mode: inverse check of the Gate 2 rejection (4 web searches, 0 fetches; fetching blocked by network policy).

## Contradicting (−) evidence first

- (−) Deployer history is offered by at least six products; Mobula's Wallet Deployer endpoint lists a deployer's other tokens and its feed already spans PumpFun, PumpSwap and Meteora DBC (Bags, Moonshot, Believe), i.e. the "across launchpads" part of the differentiation already exists as an API [S: S4, S13].
- (−) GMGN token pages flag insiders, snipers and bundled buyers, offer a Dev Sell auto-exit and let anyone inspect any wallet's history [S: S12]; "dev sold" is a mainstream terminal signal [S: S17].
- (−) RugCheck is reported to flag creators with prior rugged tokens [S: S15].
- (−) A KYC "verified creator" launchpad (Doxxxed.fun) exists and is listed for sale at $75k, a weak sign that team-verification as a product has not found traction [M/S: S16].
- (−) 0/20 multi-wallet coins had team locks, so the extra "team" fields would mostly be empty [V: S9].
- (+) Gaps on the incumbent side: RugCheck reportedly cannot assess team credibility [S: S14]; no source found shows Axiom or GMGN natively displaying a team roster, lock cancel authority or fee-split recipients [U]. This is the only room left, and it has no demand evidence.

## Inverse check: is the rejection wrong?

- **Is the "equivalent" really equivalent for the segment?** For traders checking a dev: yes. The core job (has this deployer rugged before, has the dev sold) is served free by checkers and terminals [S: S2, S6, S12, S17]. For the team-side record (roster, locks, splits, payday history) there is no exact equivalent found, but the closest substitutes are DexScreener paid profiles (owns distribution) [V: S9] and launch-time vesting (Jupiter Studio, Streamflow) [S/V: S9, S10].
- **Level-3/4 evidence for the difference?** None. No usage or payment data for team fields; the four kill tests were never run [S1]. The only payment evidence ($299 DexScreener profiles) goes to the incumbent that would add the fields [V: S9].
- **Result: rejection stands.**

| Attack | Finding | Evidence | Does the idea survive? |
|---|---|---|---|
| Why will it fail? | Core (deployer history, dev sells) is commodity and free; the add-on fields are empty for most coins | [S: S2, S6, S12, S13]; [V: S9] | No |
| Why won't customers care? | Traders decide in seconds inside terminals that already flag dev sells/bundles; teams already buy trust signals from DexScreener | [S: S12, S17]; [V: S9] | No |
| Which competitor already solves it? | MadeOnSol, Mobula (incl. cross-launchpad deployer endpoint), Rug Munch, Noesis, DEXTools, Apify, RugCheck creator flag, GMGN dev-sell/wallet tools, DexScreener profiles, Doxxxed.fun (KYC) | [S: S2–S8, S12–S15]; [M: S16]; [V: S9] | No |
| Why is the business model weak? | Trader side is free or cents per check; team side depends on the small fee-concentrated segment; a comparable trust product is for sale at $75k | [S: S5]; [M: S16]; [S1] | No |
| Why will distribution be hard? | Terminals and DexScreener own attention; a badge needs a terminal partner (test 4 never run) | [S1]; [V: S9] | No |
| Why is the differentiation insufficient? | Lock/split fields are public account reads; Mobula/terminals could ship them in one release (fails R4) | [V: S9]; [S: S13] | No |
| Which critical assumptions are unproven? | That teams will adopt a Team Launch; that a terminal will show the badge; that traders weight team fields | [S1] | Unproven (U) |
| Does it need the token? | No; it is an indexing/reputation service | [V: S9] | n/a (no token needed) |
| Regulatory exposure | Labelling wallets as ruggers invites defamation claims; KYC claims are unregulated | [S: S11, S16] | Manageable if facts only, but adds cost |

## Claims the reviewer could not verify

- That GMGN, Axiom, Photon or DexScreener natively show a deployer's past coins on token pages (no official docs found) [U]; GMGN features rest on one third-party guide [S: S12].
- That RugCheck flags creator rug history [S: S15] (third-party write-up only).
- That Photon rebranded to Axiom (single unreliable guide) [S: S18]; treat as false until confirmed.
- That Pump.fun creator profiles show past coins [U].
- All competitor evidence remains snippet-level (S); no page was opened. Coverage of GitHub and other chains still not done.
- Doxxxed.fun traction and sale price [M: S16].

## Reviewer's recommended verdict

**REJECTED (rejection stands).** Strongest reason: the core job, a dev's history and dev-sell signal, is already served free and cross-launchpad by multiple tools and terminals, and the only uncovered extension (team roster, locks, splits) has zero demand evidence and is a one-release feature for incumbents. Caveat: the existence evidence is snippet-level (S) only; it is consistent across many independent hits, so the rejection is safe, but it is not V-grade.
