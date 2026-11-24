# Stage 2: Existence check (kill-first)

Question: **who already solves this, and why should this exist anyway?**

Research spend: 11 web searches (1 extended), 6 GitHub searches, 1 npm fetch plus 8 package downloads, 0 page fetches (blocked by network policy), reuse of the Salary repo's own primary research. Run 2026-11-24.

## Search coverage

| Channel | Done? | Queries / where | Hits |
|---|---|---|---|
| Native platform features | Yes | Pump.fun fee sharing (SDK history S6, mechanics S1, news S7–S9); Bags fee share (S10, S1) | **2 full equivalents** |
| Web search, 3+ phrasings | Yes | "creator fee sharing split", "pay team developers salary", "claim and pay team wallets schedule bot" | pumpdev.io, j.tools, PumpPortal, xBot |
| GitHub repositories | Yes | 6 queries (S16) | 4 creator-fee distributors; 94 Solana payroll repos |
| npm packages | Yes | `@pump-fun/pump-sdk` release history (S6) | `sharingConfig` from 2026-01-09 |
| Protocol docs and directories | Partly | Streamflow, Squads, Bags docs via search; DefiLlama blocked | Streamflow payroll, Squads spending limits |
| Token launches with the same pitch | No | DexScreener/CoinGecko blocked by network policy | U |
| Bots / API sites | Yes | Extended search | pumpdev.io (scheduled distribution), j.tools, PumpPortal, xBot |
| Other chains | Yes | Clanker, Zora, 0xSplits | Same feature on Base |
| Web2 / adjacent | Yes | Crypto payroll (Request, Rise, Deel, Zebec) | Established category |
| Dead or abandoned attempts | No | Wayback blocked | U |

## Equivalents found

| Product | Overlap | Evidence | Overlap level |
|---|---|---|---|
| **Pump.fun fee sharing** | Splits creator fees by percentage across up to 10 wallets; anyone can trigger distribution; live since 2026-01-09, 318 days before Salary's first commit | [V: S1, S6] [C: S7, S8, S9] | **Full** for "distribute creator fees across wallets"; **partial** for teams that change (≤10 wallets, one change after launch [V: S1]). Pointing the split at one Squads vault removes that limit |
| **Bags fee share** | 1–100 claimers, editable by admin | [C: S1, S10] | **Full**, and goes beyond Pump on team size and changeability |
| **pumpdev.io claim-and-distribute** | Claims Pump.fun creator fees and splits them among wallets on a recurring hourly schedule | [S: S11] | **Unverified lead.** The reviewer could not find the page again. The rejection does not depend on it |
| Streamflow payroll streams | Scheduled contributor pay from a funded stream | [V: S1] layout; [S/M: S14] payroll | Partial (no fee collection) |
| Squads spending limits / Recipients | Team treasury with recurring payments and approval controls | [S: S15] | Partial |
| j.tools, PumpPortal, open-source distributors and toolkits (fartnode, hymet-distributor, pumpkit, dev-fee-harvester, pumpfun-tiktok-fee-share) | Claim / batch-claim / redistribute creator fees | [S: S12, S13] [V: S16] (descriptions only) | Partial |
| Clanker / Zora / 0xSplits (Base) | Multi-recipient fee splits | [S: S18] | Full, on another chain |
| Request Finance, Rise, Deel, Zebec | Crypto payroll for contributors | [S/M: S19] | Adjacent |

## Gate 2 decision

- [x] An equivalent exists. Differentiation test below.

### Differentiation test

1. **What would a customer get that the existing option does not give them?** Salary's own list [S2]: change pay at any time, more than 10 people, pay on a schedule, SOL and USD view, a public payday record, payroll on coins whose split is already locked. Bags already covers more than 10 people and changeable recipients [C: S1, S10]. pumpdev.io reportedly covers scheduled payouts [S: S11]. Squads plus Streamflow cover changeable scheduled pay [S: S14, S15]. What remains is a USD display and a memo record, which are presentation features.
2. **Is there evidence that customers want that difference?** **None found, and the evidence points the other way (−).** 95.4% of 3,000 sampled fee-sharing configs have one recipient, so teams overwhelmingly don't split at all [V: S1]. 0 of 20 multi-wallet coins had any team lock [V: S17]. Pump.fun's co-founder said creator fees had little effect on the average deployer [S: S20]. No complaints or requests for "payroll from creator fees" were found.
3. **Could the incumbent ship that difference in one release?** Yes. Salary's own decisions doc says "real but thin differences that Pump.fun could copy" [V: S2]. Pump.fun shipped four creator-fee changes in 2026 [C: S1, S7].
4. **Would you still pitch it if the incumbent did not exist?** The core pitch ("split fees to your team") *is* the incumbent's feature. The repositioned pitch only exists in contrast to it [S2].

**Gate 2 result: FAIL → REJECTED.** Stages 3–5 are not required. Stage 3–4 tables below are filled from existing Salary data at no extra research cost, for the postmortem.
