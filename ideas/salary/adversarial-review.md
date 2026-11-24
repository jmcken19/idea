# Stage 6: Independent adversarial review

Reviewer: adversarial-reviewer (independent subagent, inverse-check + attack table), 2026-11-24

Input given to the reviewer: the claims and sources only, not the pitch. Files read: `system/research-standards.md`, `system/lessons-learned.md`, and `existing-solutions.md`, `competitor-analysis.md`, `market-research.md`, `commercial-analysis.md`, `technical-feasibility.md`, `sources.md`, plus this template. (`scorecard.md` was opened by accident while listing files; it was not used.) Searches: 2 WebSearch + 2 GitHub repository searches = 4, all logged. 0 fetches.

## Inverse check: is the Gate-2 rejection wrong?

The best case for "the rejection is unsafe":

1. **Pump.fun's native split is not a payroll tool.** It allows at most 10 wallets and can be edited once [V: S1]. A March 2026 change reportedly allows only one post-launch recipient change, after which the config is locked for good [S: S21]. A team whose members join and leave cannot run payroll on that alone, so calling it "Full" overlap overstates things for the *changeable, scheduled team pay* segment.
2. **The "Full" overlap for scheduled payday rests on a snippet.** pumpdev.io (S11) is tagged S. My search for it this session did not surface the page at all, and Pump's own `distribute_creator_fees` is a manual, permissionless call with no timer (search-result summary from developer guides; not added as a source). If pumpdev.io does not exist or does not work as described, the evidence that a scheduled-payday product already exists is gone.
3. **95.4% single-recipient does not, strictly, measure the absence of payroll demand.** Teams could route fees to one treasury and pay people off-chain.

Why each argument fails:

1. **Equivalence holds without pumpdev.io under R1 ("this plus a spreadsheet").** Pump split → one Squads vault as the recipient → Squads spending limits/Recipients or Streamflow streams gives changeable, scheduled pay to any number of people [V: S1 for Pump, Streamflow, Squads mechanics; S: S14, S15 for the payroll features]. Bags covers 1–100 editable claimers natively [C: S1, S10]. The lock that Pump added in S21 *blocks* any third party from routing fees to a changing team, except through a single vault. That vault pattern is exactly what Squads already offers.
2. **The rejection does not depend on pumpdev.io.** Take it out and point 1 still provides the equivalent. It also leaves the negative demand data untouched.
3. **Argument 3 is the reframing that Lesson L3/R3 forbids.** There is no new evidence that off-chain payroll teams exist or want a tool. My search for complaints about the 10-wallet cap or the lock found none (S21). There is still no level-2, level-3 or level-4 evidence for the difference. The only V-grade level-3 data is negative (95.4% single-recipient, 0/20 team locks) [V: S1, S17].
Also: **the differences are a feature, not a company.** The incumbent owns the fee program and changes it often. It added the anti-griefing lock [S: S21] and Holder Rewards [S: S22], so it directs where creator fees go.

**Result: rejection stands.** The precise framing should change, though. Pump native is a *partial* equivalent for changeable payroll. The full equivalent is Bags, or Pump plus Squads/Streamflow. pumpdev.io should be shown as an unverified lead, not as "Full".

## Attack table ((−) evidence first)

| Attack | Finding | Evidence | Does the idea survive? |
|---|---|---|---|
| Why will it fail? | (−) Teams do not use the free split they already have: 95.4% of sampled configs have one recipient, and 0/20 multi-wallet coins had team locks. A paid layer on top of an unused free feature has no pull. | [V: S1, S17] | No |
| Why won't customers care? | (−) No requests or complaints for "payroll from creator fees", and none about the 10-wallet cap or the lock (searched again 2026-11-24). Creator fees reportedly did little for the average deployer. | [U]; [S: S20, S21] | No |
| Which competitor already solves it? | Bags (1–100 editable claimers); Pump split + Squads vault/spending limits or Streamflow (changeable scheduled pay); Clanker/0xSplits on Base. Missed in Stage 2: open-source **openpumptrade/pumpkit** (fee-sharing building blocks, active 2026-11-18), **daronthedragon/dev-fee-harvester** (batch-claims team fee-sharing fees), **0xbl33p/pumpfun-tiktok-fee-share**, plus native **Pump Holder Rewards** as a competing use of creator fees. pumpdev.io is unverified. | [C: S1, S10]; [V: S1]; [S: S14, S15, S18]; [repo, descriptions only: S23]; [S: S22]; [S: S11] | No |
| Why is the business model weak? | No payer named; the 1% fee was withdrawn. The tool competes with free native and open-source options. Fees are concentrated in a few coins, so most teams have nothing to pay from. | [V: S2, S1]; concentration [S: S3, S4] | No |
| Why will distribution be hard? | It depends on Pump.fun's flow, and Pump can lock or reshape fee routing in one release (as it did in March 2026). Terminals and bots already sit at the claim step. | [S: S21, S11–S13]; [V: S1] | No |
| Why is the differentiation insufficient? | What remains is a USD view and a memo record, which are presentation features. The project's own doc says "real but thin … Pump.fun could copy". | [V: S2] | No |
| Which critical assumptions are unproven? | That multi-person meme teams with real fee income exist in numbers; that they want on-chain payroll rather than a treasury; that anyone would pay. All are H/U. | [H/U] | No |
| Does it need the token? | No. A token was only ever a fundraising mechanism. | [S2] | n/a, a token would hurt |
| Regulatory exposure | Routing other people's fees on a schedule looks like money transmission. That claim comes only from the legal table in the snippet-built research-v2. | [S: S3] | Unresolved, adds risk |

## Claims the reviewer could not verify

These claims rest only on snippet (S) or marketing (M) evidence and must not be presented as fact:

- **pumpdev.io scheduled hourly claim-and-distribute** [S: S11]. It was not found again in this session's search, and no page was opened. Its "Full" overlap rating should be downgraded to "unverified lead".
- The March 2026 one-change-then-lock rule [S: S21]. It comes from a search summary, and the exact source page was not opened.
- Pump Holder Rewards: only the title was seen [S: S22].
- Squads Recipients and recurring payments [S: S15], and Streamflow payroll with "40k+ projects" [S/M: S14].
- Clanker/Zora splits on Base [S: S18], and the crypto payroll category [S/M: S19].
- Bags fees down about 99%, Pump.fun revenue down about 75%, creator fees concentrated in "a few dozen coins" [S: S4, S3]. These come from research-v2, which was built from snippets.
- The co-founder quote that the fee model failed [S: S20].
- The money-transmission risk [S: S3].
- The open-source repos in S23: only their descriptions were read, not their code.
- "Four creator-fee changes in 2026" [C: S1, S7]. S7 is a snippet, so this holds only if S1 itself documents the four changes.
- The ≈42k multi-wallet coins figure is an extrapolation from a 3,000-config sample [E from V: S1].

## Reviewer's recommended verdict

**REJECTED (rejection stands).** The strongest reason: the only verified demand data is negative. Teams overwhelmingly do not use the free native split (95.4% single-recipient; 0/20 team locks) [V: S1, S17]. The "changeable, scheduled payroll" difference is already covered by Bags or by Pump plus Squads/Streamflow, with no level-2 to level-4 evidence that anyone wants it. Correct one detail in `existing-solutions.md`: pumpdev.io is an unverified lead, not a verified "Full" equivalent. The rejection does not depend on it.
