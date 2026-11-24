# Stage 6: Independent adversarial review

Reviewer: adversarial-reviewer (independent subagent, full review of revised evidence), 2026-11-24

Input given to the reviewer: claims and sources only. Files read: `system/research-standards.md`, `system/lessons-learned.md`, `system/validation-framework.md`, and from this folder `existing-solutions.md`, `competitor-analysis.md`, `market-research.md`, `commercial-analysis.md`, `technical-feasibility.md`, `sources.md`, `scorecard.md`, `revalidation-2026-11-24.md`. Not read: README, initial hypothesis, final verdict, postmortem. I also read one line of `research/crypto-infrastructure/solana-fee-and-payment-primitives.md` to find how the single-recipient sample was drawn (n=3,000, random). Spend: 4 WebSearch (all logged), 5 tool calls (1 github-raw, which returned 404 on S1 so S1 cannot be re-read independently; 4 npm-grep), plus `ir.py lint`.

## Previous review (first pass)

1. Rejection stands: Bags, or Pump plus Squads/Streamflow, was taken as the full equivalent under R1 ("this plus a spreadsheet"). pumpdev.io was downgraded to an unverified lead.
2. The strongest reason was the negative demand data: 95.4% single-recipient (random sample, n=3,000 of 903,612 configs) and 0/20 team locks (blind study, n=20).
3. It flagged Squads and Streamflow "payroll" as snippet-only. The second pass has since shown that Squads is approval-gated, not scheduled [V: S26].

## Split the idea in two

| Part | Equivalent? | Evidence | Gate 2 |
|---|---|---|---|
| **A. Static fee splitting** (spread creator fees across wallets) | Yes, free and native. Pump: ≤10 shareholders, permissionless distribute. Bags: ≤100 claimers, admin-editable | [V: S24, S25]; EVM [V: S28, S29] | **REJECTED. The rejection is safe.** Meteora DBC and LetsBonk add nothing here: Meteora is a two-party split [V: S41], BonkFun is moving to zero creator fees [S: S43] |
| **B. Salary layer** (changeable + scheduled + fee-linked team pay) | No turnkey equivalent verified. Pump allows one change and has no scheduler [V: S24]. Bags is changeable, but each claimer must claim and there is no schedule [V: S25; S: S42]. Squads is member-signed [V: S26]. Streamflow is scheduled but has no fee source [V: S27]. The open-source repos are building blocks [V: S31] | V | **Rejecting for "an equivalent exists" is unsafe for B.** The R1 composite (Pump split to one vault, then Streamflow) works only if someone tops up manually each cycle. That makes it a workaround, not an equivalent |

## (−) evidence first

| # | Finding | Grade | Direct negative, or absence? |
|---|---|---|---|
| 1 | Pump deliberately locks fee recipients after one change ("anti-griefing") [V: S24; C: S35]. The platform the idea depends on is pushing against changeable routing | V | Direct, but it is a platform-risk argument, not a demand argument |
| 2 | 95.4% of configs have a single recipient (random sample, n=3,000; population: 903,612 SharingConfig accounts, Nov 23 2026) [V: S1] | V for the number | **Ambiguous** (see below) |
| 3 | 0/20 multi-wallet coins had a team lock (blind study, n=20; how the coins were selected is not stated: illustrative, not representative) [onchain: S17] | V | Weak and indirect. A lock is not payroll |
| 4 | An independent builder stopped a near-identical EVM fee-split vault after measuring the market [repo: S33]. The analysis is the author's own (E) | E | Direct, but on another venue |
| 5 | Sablier is winding down and cites weak usage [S: S37] | S | Adjacent category, snippet only |
| 6 | Creator fees are concentrated in "a few dozen coins" [S: S3, S4] | S | **Would be the strongest kill if verified. It is snippet-only** |
| 7 | No request, complaint, bounty or workaround for payroll from creator fees has been found in roughly 20 searches across both passes, including 3 of mine (bots, treasury routing, Bags schedule) | U | **Absence of evidence** |
| 8 | No payer has ever been named. The product competes with free native features and a DIY cron [V: S2, S30, S31] | V | Direct for "no payer yet". Under the framework, missing data is not proof that none exists |

**Is the 95.4% figure negative demand evidence?** Only weakly. (a) It is unweighted. Most of the 903,612 configs belong to coins that earn close to nothing, and those coins would never run payroll. The relevant population is coins with fee income, and nobody has measured that. (b) A single recipient can be a Squads vault or a team treasury. Salary's data cannot tell them apart (U). (c) Whether a config is created by default at launch or opted into is U. I grepped the SDK [S24] and could not settle it. If configs are created by default, 95.4% just means "nobody touched the default". It is fair negative evidence for demand for **static splitting** (part A). It does not test part B. Using it as the decisive kill for B treats ambiguity as a verdict.

**Is the rest of the case direct or absence?** For part B it is mostly absence (#7) plus indirect or low-grade negatives (#3–#6). None of it is a V/C level-3/4 negative measured on the right population.

## Attack table

| Attack | Finding | Evidence | Does the idea survive? |
|---|---|---|---|
| Why will it fail? | The target segment (multi-person teams on coins with sustained fee income) is probably tiny, because fees are concentrated. Pump locks recipients, so the product must sit behind a single vault, where a DIY cron already works | [S: S3, S4]; [V: S24, S31] | Probably not, but the segment size is unverified |
| Why won't customers care? | No level-2 to level-4 signal for scheduled, changeable pay. Splitdev shipped the opposite design (a permanent lock), which suggests traders reward immutability [V: S32; H on the inference] | [U]; [V: S32] | Unknown, and leaning no |
| Who already solves it? | Part A: Pump and Bags natively [V: S24, S25]. Part B: nobody turnkey. Workarounds: Pump to vault plus Streamflow [V: S27], pumpkit or dev-fee-harvester cron [V: S31], pumpdev `/api/claim-distribute` [V: S30]. My searches found no missed competitor: no Telegram payroll bot, no LetsBonk or Meteora team split [V: S41; S: S43], and no Bags scheduler [S: S42] | V | A: no. B: yes on existence |
| Why is the model weak? | Competes with free plus a one-day DIY build. Revenue would be a cut of volatile, concentrated fees. No payer has been named | [V: S2]; [E, low] | No, unless a payer appears |
| Why is distribution hard? | It depends on Pump and Bags. Bags could add a scheduler on top of its admin-editable config in one release [V: S25]. Pump controls routing and has changed creator fees several times in 2026 [C: S35, S7] | V/C | Weak |
| Why is the differentiation insufficient? | "Scheduled" can be copied by Bags or Streamflow. "Changeable" only works through a vault, and anyone can set that up. The project's own doc calls the differences "real but thin" [V: S2] | V | Thin, but not yet shown to be zero demand |
| Unproven assumptions | That teams with fee income exist in numbers; that they route fees to a treasury and pay people by hand today; that they would pay rather than write a cron | H/U | Untested |
| Token necessity | None. A token would only have been a fundraising mechanism | [S2] | A token would hurt |
| Regulatory exposure | Routing other people's fees on a schedule may count as money transmission. That claim rests only on S3, a report built from snippets. A non-custodial design (team-owned vault plus stream) reduces the exposure | [S: S3] | Unresolved |

## Safeguard violations in the existing records (§8–9)

- **SG1:** Scorecard #2 (fatal) still says "free native equivalent", which S24 contradicts for part B. Its evidence still includes S7 and S10 (snippets), and #1 still cites S11 (overturned by S30). S1 is a private repo: github-raw returned 404, so no one outside the project can re-read the core statistic.
- **SG2:** The 95.4% figure appears without `n=` in `existing-solutions.md:42`, `market-research.md:9` and `sources.md:23` (lint). "0/20 team locks" never states how the coins were selected and is never labelled "illustrative, not representative". "≈42k coins" is an extrapolation with no interval. The 44% figure in S33 has no n.
- **SG3:** `existing-solutions.md` has no `## Easy replicators` table. One exists only in the revalidation file.
- **SG4:** The coverage table has no `Recent launches` or `Discontinued` rows. "Token launches" and "Dead attempts" are marked "No" instead of `Blocked: <reason>`.
- **SG6:** `final-verdict.md` has no `## Unresolved uncertainties` section (lint).
- **§9:** `market-research.md` has no `## Demand evidence` table with kinds. The negative level-3 row is measured on the wrong population (all configs, not coins with fee income).
- **Stale claims never corrected:** `existing-solutions.md` and `competitor-analysis.md` still rate Pump as "Full", say pumpdev.io "already does payday", and say Squads gives "changeable scheduled pay". S24, S26 and S30 contradict all three.
- **Snippet or marketing used as fact:** "four creator-fee changes in 2026" [C: S1, S7] has only one opened page. Bags "fees down 99%", Pump "revenue down 75%" and fee concentration [S: S3, S4]. The money-transmission risk [S: S3]. Streamflow "40k+ projects" [M: S14].
- **Lint:** the locators for S24–S33 are not in the accepted format (repo:/URL).

## Recommended verdict

**Split verdict.** Part A (static fee splitting): **REJECTED**, because a free native equivalent exists [V: S24, S25]. Part B (salary layer): **NEEDS MORE RESEARCH**, not REJECTED. The Gate 2 ground ("an equivalent exists") no longer holds at primary grade. What remains is absence of demand evidence plus negatives that are ambiguous or snippet-grade. Under the framework, Gate 4 with no level-3/4 evidence gives NEEDS MORE RESEARCH, and REJECTED needs one fatal issue with evidence. The most likely fatal issue, fee concentration, is S-grade.

**Strongest kill reason (still unverified):** the paying segment may barely exist. Fees are concentrated in a few coins, and those teams can write a free one-day cron.

**Cheapest decisive test (an on-chain read, possible once the RPC or Bitquery block is lifted):** take the top 200 Pump coins by creator fees over the last 30 days (fee-weighted, n=200, ranked by fees, not random). For each, classify the recipients (one wallet, a Squads vault, or several) and trace outflows from the recipient wallets for recurring payments to 3 or more wallets. **Kill threshold:** if fewer than 10 of the 200 show a treasury-plus-recurring-payout pattern or a multi-payee split with a used change, then **REJECTED**. If 10 or more do, contact those teams: fewer than 3 of 20 agreeing to a stated price also means **REJECTED**. Deadline: 2026-12-08. If the test is not run by then, the lower verdict (REJECTED) stands. This verdict does not authorise any building (R5).
