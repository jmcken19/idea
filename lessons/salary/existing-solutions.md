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
| Recent launches (last 90 days) | Yes (second pass) | GitHub created:>2026-08-25 queries [V: S34] | Splitdev (locked split, 2026-09-27) [V: S32]; no recent repo combines creator fees with scheduled team pay |
| Discontinued / abandoned projects | Yes (second pass); Wayback blocked | WebSearch + GitHub | Sablier maintenance mode / Solana UI shut [S: S37]; fee-split-vaults project abandoned after its own market test [V: S33] |

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

1. **What would a customer get that the existing option does not give them?** Salary's own list [S2]: change pay at any time, more than 10 people, pay on a schedule, SOL and USD view, a public payday record, payroll on coins whose split is already locked. Bags already covers more than 10 people and changeable recipients [C: S1, S10]. pumpdev.io reportedly covers scheduled payouts [S: S11] (*second pass: not verified; its repo shows an on-demand endpoint only [V: S30]*). Squads plus Streamflow cover changeable scheduled pay [S: S14, S15] (*second pass: Streamflow does scheduled auto-withdrawal [V: S27]; Squads spending limits are member-signed allowances, not automatic payouts [V: S26]*). What remains is a USD display and a memo record, which are presentation features.
2. **Is there evidence that customers want that difference?** **None found, and the evidence points the other way (−).** 95.4% of fee-sharing configs have one recipient (n=3,000, random sample of all 903,612 configs, not fee-weighted) [V: S1]. *Second pass: weakly negative only. A single recipient can be a team treasury, and the sample isn't weighted by fees.* None of the 20 multi-wallet coins in the blind study had a team lock (n=20, random, illustrative, not representative) [V: S17]. Pump.fun's co-founder said creator fees had little effect on the average deployer [S: S20]. No complaints or requests for "payroll from creator fees" were found.
3. **Could the incumbent ship that difference in one release?** Yes. Salary's own decisions doc says "real but thin differences that Pump.fun could copy" [V: S2]. Pump.fun shipped four creator-fee changes in 2026 [C: S1, S7].
4. **Would you still pitch it if the incumbent did not exist?** The core pitch ("split fees to your team") *is* the incumbent's feature. The repositioned pitch only exists in contrast to it [S2].

**First-pass Gate 2 result: FAIL → REJECTED** (revised below). Stages 3–5 were not required. Stage 3–4 tables below are filled from existing Salary data at no extra research cost, for the postmortem.

---

## Second pass (audit 2, 2026-11-24): primary-source re-check

Detail: `revalidation-2026-11-24.md`; independent review: `adversarial-review.md`. Spend: 13 + 4 WebSearch, 34 npm/GitHub calls.

### Revised overlap (segment: multi-contributor Solana meme teams wanting changeable, scheduled pay from creator fees)

| Product | Static split | Changeable | Scheduled | Fee-linked | Turnkey | Level (first pass → second) |
|---|---|---|---|---|---|---|
| Pump.fun native | Yes, ≤10 [V: S24] | Once, then locked [V: S24] | No: manual, permissionless distribute [V: S24] | Yes | Yes | Full → **Full for static splitting, Partial for the salary layer** |
| Bags native | Yes, ≤100 [V: S25] | Yes, admin [V: S25] | None found [S: S42] | Yes | Bags coins only | Full → **Partial-high** |
| Pump split → vault → Streamflow | Yes | Yes [V: S27] | Yes, auto-withdraw [V: S27] | Manual funding | DIY assembly | Partial → Partial |
| Pump split → vault → Squads | Yes | Yes | Member-signed allowance [V: S26] | Yes | DIY assembly | Partial → Partial (weaker) |
| pumpdev.io | Endpoint [V: S30] | U | Not verified | Yes | Dev API | Full (S) → **Building block** |
| Splitdev | ≤10 [V: S32] | No, locked by design | Manual | Yes | Yes | new: Partial, opposite design |
| Open-source distributors / pumpkit | Varies [V: S31] | Varies | Cron | Yes | Code | Partial → Building blocks |
| Clanker / 0xSplits (EVM) | Yes [V: S28, S29] | Yes | No | Yes | Other chains | Full on other chains |
| Meteora DBC | Two-party only [V: S41] | — | — | Yes | — | new: not equivalent |

### Easy replicators

| Who | Why they could ship it fast | Evidence |
|---|---|---|
| Bags | Admin-editable claimers to 100 already; a payday scheduler is the missing piece | [V: S25] |
| Streamflow | Scheduled, editable, top-up streams; markets "web3 payroll"; lacks a fee connector | [V: S27] |
| Squads | Spending limits, plus Solana Recurring Delegations tested with Squads | [V: S26] [S: S36] |
| Any developer (pumpkit / pumpdev API / cron) | `writeFeeSharing`, `distributeSharedFees`, claim-distribute endpoint: about a day of work | [V: S30, S31] |
| Pump.fun | Technically trivial, but it deliberately restricts edits (anti-griefing): low incentive | [V: S24] [S: S35] |

### Second-pass Gate 2 result

The idea has two parts, and they get different results:
- **Static distribution of creator fees across wallets: FAIL → REJECTED.** Native and free on Pump.fun and Bags, verified in their own SDK code [V: S24, S25].
- **Salary layer (changeable + scheduled + fee-linked, turnkey): no verified equivalent.** The first-pass claim that it already existed was **overstated**: the "scheduled" evidence (pumpdev.io) didn't hold, and Squads isn't automatic. The difference is real (Q1 passes). Demand evidence for it is **absent, not negative** (Q2 unknown). Bags, Streamflow or a one-day cron could replicate it (Q3: yes, but not Pump.fun).

The differentiation test fails on Q2 for lack of evidence. Under SG5 that is not an opportunity, but it is also not proof of no demand. The decisive evidence (do fee-earning teams route fees to a treasury and pay several people on a schedule?) needs on-chain reads that the network policy blocks. → Proceeds to the verdict as **NEEDS MORE RESEARCH, time-boxed** (see `final-verdict.md`).
