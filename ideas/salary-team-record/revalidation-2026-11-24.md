# Revalidation of the Gate 2 rejection (second, deeper pass)

Run 2026-11-24. Question: does the rejection survive primary evidence? Tags V/C/S/M/E/H/U. Sources S19-S38 are in `sources.md`.
Budget: 12 WebSearch (cap 14). Roughly 40 npm-grep / github-raw / github-repos calls against a cap of 30. **The cap was exceeded by about a third** (5 github-raw calls returned 404 and 4 more were negative greps). Blocked channels are listed below.

**Result: the rejection holds.** The competitor evidence moved from snippet (S) to primary (V) and got stronger. One earlier claim was mis-described (Mobula, DexScreener). One piece of demand evidence is weaker than first written (DexScreener $299).

## Evidence upgrades

| Claim | Old tag | New tag | Source | Held? |
|---|---|---|---|---|
| Mobula has a dev-history endpoint | S | **V** | S19 (`fetchTokenDevHistory`, GET /api/2/token/dev-history) | Held, but **corrected**: it is per token (deployer fee claims, swaps, transfers on one token), not a list of a deployer's other launches |
| Mobula covers a deployer's other tokens across launchpads (cross-launchpad) | S | **V** (part) | S19: `WalletV2Deployer` takes wallet + blockchain and returns token positions; token objects carry `deployerTokensCount`, `deployerMigrationsCount`, `migrationRate`; dev-history protocols are pumpfun, pumpswap, meteoradbc, clanker | Held. Which launchpads the wallet endpoint indexes is U (code shows no list) |
| Mobula's feed spans Bags, Moonshot, Believe | S | S | S13 only. Code shows `meteoradbc` and `clanker`, not brand names | Not upgraded |
| Rug Munch classifies deployers at $0.06 per check | S | **V** | S23 (vendor README: `check_deployer_history` $0.06; free tier 1 call/day) | Held. Evidence is vendor-stated price, not a sale |
| MadeOnSol Deployer Hunter exists with history, tiers, bond rate | S/M | **V** | S21 (SDK: alerts, trajectory, stats, leaderboard) | Held. Free checker page itself still S |
| GMGN shows insiders, dev sell and any wallet's history | S (third-party guide) | **V** | S25 (official `gmgn-cli`: `dev.creator_open_count`, `creator_token_status`, `dev_team_hold_rate`, `rug_ratio`, /v1/user/created_tokens) | Held and **much stronger**: GMGN publishes a `gmgn-dev-score` skill that answers "is this token's team trustworthy / has this creator rugged before" |
| RugCheck flags creators with prior rugs | S | S | S35, S38. Client packages show no creator-history field | **Not confirmed.** Downgrade to U for "creator rug history", keep only "creator address and rugged flag" (S) |
| RugCheck cannot assess team credibility | S | S | S14, S35 | Held, still snippet |
| DexScreener $299 shows teams pay for trust signals | V (salary research) | V for price, **mis-described** for purpose | S33 (listing: info, socials, locked-supply wallets for market cap) | The price holds. "Trust badge" does not: it is an info and listing product. See Demand |
| Doxxxed.fun is listed for sale at $75k | M | M | S31 | Held. Dead or alive is U; 3 followers on Product Hunt |
| Axiom or Photon show dev history | U | U | S37 | Still unconfirmed. Dev Holding % filter only |
| Pump.fun creator profile shows past coins | U | U | S36 | Still unconfirmed |

## New competitors

| Product | Evidence | Why it matters |
|---|---|---|
| **GMGN official OpenAPI/CLI and dev-score skill** | **V** S25 | The strongest equivalent. Dev history, dev holdings, team-hold rate and creator rug label exist inside the largest memecoin terminal's own API, and a score-and-verdict skill is published |
| **MadeOnSol API and SDK family** (TS, Python, Rust, MCP, ElizaOS, Solana Agent Kit, Discord bot), paid x402 $0.005-$0.02 per call, Business EUR 400/mo | **V** code S21, S22; **S** price S34 | Deployer intelligence is sold as a paid API with five tiers |
| **Mobula `deployerTokensCount`, `migrationRate`** on every token object | **V** S19 | A trader-facing "dev launched N, M migrated" is already a field on a token |
| Hobby and hackathon deployer-reputation repos (daybreak, DeployerDNA, devcred-agent, mirror-deployer, fairsight, deployer-reputation-mcp, openbb-pumpdata) | **V** metadata S26 | 0 to 4 stars each. Commodity, and nobody has traction |
| DevCred (Colosseum agent hackathon entry) | **S** S32 | Same idea as the Team Record pitch, built in a hackathon |
| CertiK KYC (Gold/Silver/Bronze, 90-day reassess) | **S** S28 | Only paid team-verification service found. EVM-centred. Price U |
| Talent Protocol Builder Score | **C** S29, S30 | Builder reputation product (see Removed) |

## Competitors weakened or removed

- **Mobula "dev history" as a cross-launchpad deployer record: weakened.** The dev-history endpoint is per token. Cross-launchpad deployer listing comes from a separate wallet endpoint plus token-level counts. The reviewer's wording in `adversarial-review.md` (that the feed "lists a deployer's other tokens") conflated the two. The overlap is still real.
- **RugCheck "flags creators with prior rugs": unconfirmed (S to U).** No creator-history field was found in two client packages or a third-party wrapper.
- **DexScreener Enhanced Token Info as a team-trust badge: reclassified.** It updates info and socials and sets locked-supply wallets (S33). It is paid distribution, not a team-reputation signal. It remains a "teams pay the terminal" datapoint, but a weaker one.
- **Talent Protocol (adjacent, not a Solana competitor): dead as a business.** Commercial operations (API, Talent+) ended Aug 2026 after an acquisition by IPTS; Builder Score lives on as a public good (C, S30). This is **negative demand evidence** for paid builder reputation and does not add a live competitor.
- **Doxxxed.fun: not removed, status unknown.** Only a for-sale listing is visible. No evidence of operating traffic.
- **Rug Munch, MadeOnSol, Mobula:** all confirmed alive (pushes in Nov 2026 or SDK Aug 2026).

## Skipped channels

| Channel | Status | Notes |
|---|---|---|
| (a) GitHub deployer-history checkers, recent and archived | **Done** | Found 7+ repos (S26). The archived:true query returned 0. Created-in-last-90-days: 1 (openbb-pumpdata). Existing tools with 0 to 4 stars confirm commodity status |
| (b) Launches built on a "dev reputation / verified team" pitch | **Partly done** | Doxxxed.fun (for sale), DevCred (hackathon), BlockEden essay (S32). No live launchpad with a verified-creator score found. No token launch found with that pitch |
| (c) Discontinued team-verification or builder-reputation products | **Done** | Doxxxed.fun status U; Talent Protocol commercial wind-down C (S30) |
| (d) Other chains and adjacent systems | **Partly done** | Talent Protocol (done), CertiK KYC (done, no price). **Not done:** Gitcoin or Human Passport, Assure DeFi and SolidProof (searched, no result for pricing), Clanker or Base-side deployer checks beyond Mobula's `clanker` protocol flag |
| Blocked | **Blocked** | gmgn.ai, madeonsol.com, docs.mobula.io, RugCheck, DexScreener pages, Reddit, HN, Wayback, crypto data APIs. GitHub raw READMEs for MadeOnSol/Mobula/gmgn-skills returned 404 on `HEAD` and `main`; code was read from npm tarballs instead |

## Easy replicators (can add the Team Record in about one release)

| Product | Capability evidence | Tag |
|---|---|---|
| GMGN | Already returns creator launch count, dev hold/sell, dev-team hold rate, rug label, a creator's created tokens, and publishes a dev-score skill | **V** S25 |
| Mobula | Token-level deployer counts, per-token deployer activity, wallet deployer listing, SDK about 3,800 weekly downloads | **V** S19 |
| MadeOnSol | Deployer reputation leaderboard, bond-rate trajectory, tiers, alerts, x402 pay-per-call | **V** S21 |
| Rug Munch | Deployer classification at $0.06 | **V** S23 |
| Pump.fun itself | Native fee-sharing and update-authority revoke exist (S32, existing record). Whether it shows creator history is U | U |
| Axiom, Photon | Dev Holding % filter only; no public API (S37) | S |
| DexScreener | Public API exposes profiles, boosts, community takeovers (S27); no deployer history | **V** (negative) |

What nobody was shown to ship: a team roster, lock cancel authority, fee-split recipients and payday history in one record. No evidence anyone wants that (see below), so this remains the only unoccupied area and is unproven.

## Demand signals classified

| Signal | Class | Evidence |
|---|---|---|
| Repos with 0 to 4 stars across about 15 deployer-reputation projects; MadeOnSol repos 0 to 3 stars; Rug Munch 1 star; Mobula SDK 1 star | Social engagement (low) | S20, S22, S23, S26 |
| Doxxxed.fun: 3 Product Hunt followers | Social engagement (low) | S31 |
| `gmgn-cli` about 9,400 weekly npm downloads; Mobula SDK about 3,800; `@mobula_labs/types` about 29,600 | **Using** (APIs overall, not dev-history specifically) | S19, S25 |
| Third-party tutorials on recycled deployers and dev-sold (DEXTools) | Actively seeking (traders asking how to check devs) | S7, S17 |
| GMGN and Apify scrapers expose creator counts, and Mobula token objects expose `deployerTokensCount` | Using (vendors build it because traders consume it) | S19, S25 |
| Rug Munch $0.06 per deployer check; x402 $0.005 to $0.02 per call (MadeOnSol); MadeOnSol Business EUR 400/mo | **Paying (price listed)**, volume U | S21, S23, S34 |
| DexScreener Enhanced Token Info $299 (from $499) | **Paying (price listed; sellers: project teams)**, volume U | S33, S9 |
| Talent Protocol API (credits) and Talent+ shut down Aug 2026 | Paying that ended | S30 |
| CertiK KYC badge | Paying (teams), price unknown | S28 |

No paying evidence was found for team roster, lock or payday-history fields. All paying evidence is for trader-side checks (cents) and for project-side listing info.

## Evidence AGAINST the rejection

1. (+) **Trader-side deployer intelligence has paying buyers.** Rug Munch ($0.06), MadeOnSol (per-call and EUR 400/mo, five tiers) and the DexScreener $299 listing show people pay in this area. Payment evidence is for price lists only; sales volume is U. This weakens a "nobody pays" argument, but it is also evidence that the paying part is already served.
2. (+) **No tool was shown to combine roster, lock authority, fee-split recipients and payday history.** All the equivalents work from deployer wallet and trading behaviour. The Team Record extension is unoccupied, though no evidence of demand for it exists.
3. (+) **Pump.fun creator profile, Axiom and Photon dev history are unconfirmed (U).** If none show dev history natively, the terminals might want a data partner. A partner is the unrun kill test 4 from the original proposal.
4. (+) **CertiK KYC exists as a paid, tiered product with a 90-day reassessment**, so team verification can be sold on EVM. Price and volume are U.
5. (+) **The reviewer's "Mobula spans Bags, Moonshot, Believe" claim is only S.** If the wallet endpoint indexes fewer launchpads than claimed, the cross-launchpad differentiation is wider than the review stated. Primary evidence shows only `pumpfun`, `pumpswap`, `meteoradbc`, `clanker`.

None of these meets the bar to change the verdict: each is S or price-list evidence, and the extension still fails the "one release" and "no demand" tests.

## Still unverified

- Whether GMGN, Axiom, Photon or Pump.fun show a creator's past coins on the token page itself (the GMGN API fields exist; the UI is U).
- Which launchpads Mobula's wallet deployer endpoint covers.
- Prices of MadeOnSol Pro and Ultra, Mobula, GMGN API tiers, CertiK KYC, Assure DeFi, SolidProof.
- Whether RugCheck exposes creator history.
- Volume of any paid product (customers, revenue). Only price lists were found.
- Whether Doxxxed.fun operates or sold.
- Whether the free MadeOnSol checker page is as described (page blocked).
- Gitcoin or Human Passport and other adjacent systems (not searched).
