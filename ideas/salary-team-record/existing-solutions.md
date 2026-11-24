# Stage 2: Existence check (kill-first)

Research spend: 1 web search (standard) plus reuse of the Salary searches and data. Run 2026-11-24. Coverage is partial (see the table). The first search was enough to show the category exists.

## Search coverage

| Channel | Done? | Where | Hits |
|---|---|---|---|
| Native platform features | Partly | Pump.fun creator profiles show past coins (common knowledge, not verified in this pass: U) | U |
| Web search | Yes | "pump.fun dev history checker deployer past coins rug track record" | 6 tools [S2–S8] |
| GitHub | No | Not needed after a full-overlap hit | n/a |
| Terminals (GMGN, Axiom, Photon, DexScreener, RugCheck) | No | Pages blocked; dev-sell/dev-holding indicators on terminals are widely reported but not verified here | U |
| Other chains | No | n/a | n/a |

## Equivalents found

| Product | Overlap | Evidence | Overlap |
|---|---|---|---|
| MadeOnSol Deployer Hunter | Every token a deployer launched, bond rate, tier; free checker; profile pages | [S: S2, S3] | **Full** for deployer history |
| Mobula token dev history API | Deployer activity feed (fee claims, swaps, transfers): the data layer a terminal badge needs | [S: S4] | Full (B2B) |
| Rug Munch Intelligence | Classifies deployers builder / suspicious / serial rugger, $0.06 per check | [S: S5] | Full (paid) |
| Noesis /dev, DEXTools, Apify profiler | Dev launch history and success rate | [S: S6, S7, S8] | Full / partial |
| Jupiter Studio vesting; Streamflow/Jupiter locks | Locked team allocations at launch | [S: S10] [V: S9] | Partial (Team Launch) |
| DexScreener Enhanced Token Info | Paid team/profile info on the dominant screener | [V: S9] | Partial (team-trust badge, owns distribution) |

## Gate 2 decision

- [x] An equivalent exists. Differentiation test:

1. **What would a customer get that the existing option does not give them?** Adding team roster, lock settings (who can cancel), fee-split recipients and payday history to deployer history, and showing it across launchpads. A real, but small, extension: Salary's own reader gets these fields from a few account reads [V: S9].
2. **Evidence customers want that difference?** **None.** The proposal's own tests (census, 20-coin prototype, concierge launch, terminal partner) were never run [S1]. (−) 0/20 multi-wallet coins had team locks, so there is little for the "team" fields to show [V: S9]. (−) Accountability demand appears only in curated raises (MetaDAO), not meme launches [S: S10]. (+) Teams do pay $299 for DexScreener profile info [V: S9], which shows willingness to pay for trust signals, to the platform that already owns the distribution.
3. **Could an incumbent ship it in one release?** Yes. Lock and split fields are public on-chain accounts; MadeOnSol, Mobula or a terminal could add them.
4. **Would you still pitch it if the incumbents didn't exist?** It was pitched as a gap ("no trusted developer reputation" [S1]) only because the existing tools hadn't been looked for.

**Gate 2 result: FAIL → REJECTED.** The core is an existing, crowded, mostly free category. The extension is copyable and has no demand evidence.
