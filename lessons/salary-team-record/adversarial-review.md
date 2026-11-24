# Stage 6: Independent adversarial review

Reviewer: adversarial-reviewer (independent subagent, full review of revised evidence), 2026-11-24

Input: claims and sources only (existing-solutions, competitor-analysis, market-research, commercial-analysis, technical-feasibility, sources, scorecard, revalidation-2026-11-24, plus system research-standards and lessons-learned). README, initial-hypothesis and final-verdict not read. Spend this pass: 5 WebSearch (standard), 6 npm-grep calls; all logged. New sources S39-S46.

## Previous review (first pass)

1. Recommended REJECTED: deployer history and the dev-sell signal are served free, across launchpads, by six or more tools and terminals.
2. All of the competitor evidence was snippets (S). Mobula's "lists a deployer's other tokens / spans Bags, Moonshot, Believe" and "RugCheck flags prior rugs" were overstated.
3. The residual (roster, locks, splits) had no demand evidence and was judged a one-release feature.

## Contradicting (−) evidence first

- (−) **GMGN, the largest memecoin terminal, ships this job in its own API.** Creator launch count, creator token status, dev and team hold rate, rug ratio, a creator's created tokens, and a published `gmgn-dev-score` skill that answers "has this creator rugged before / is this team trustworthy" [V: S25]. The same package exposes per-token lock summary and detail (locked or burned supply), per-dev fee income (`coin_creator_fee`) and the CTO flag [V: S40].
- (−) **NEW, missed by both earlier passes: the team roster plus fee-split recipients is native on Bags.** `getTokenCreators(mint)` returns each fee claimer with `royaltyBps`, `isCreator` and `twitterUsername` [V: S39]. Docs show a roster endpoint and claimers enriched with verified social profiles (X, TikTok, Kick, GitHub) [S: S42]. This is the "roster + split recipients" half of the residual, sitting on the launchpad itself.
- (−) **Pump.fun fee-sharing recipients are public program state** (shareholders in the fee-sharing config) [V: S41]. Any indexer, or Pump.fun itself, reads them in one call. Whether the coin page displays them is U [S: S43].
- (−) Mobula puts `deployerTokensCount`, `deployerMigrationsCount` and `migrationRate` on every token object, and has a wallet-deployer endpoint [V: S19]. MadeOnSol sells deployer reputation via SDKs and pay-per-call [V: S21]. Rug Munch sells a deployer check [V: S23]. There are 7+ hobby and hackathon repos [V: S26].
- (−) Lock verification is already routed through Solscan, Explorer and RugCheck; Streamflow markets its locks as non-cancellable [M: S44]. Bubblemaps exposes team-wallet clusters against disclosed allocations to traders [S/M: S45].
- (−) Talent Protocol's paid builder-reputation business shut down in Aug 2026 [C: S30]. Doxxxed.fun (KYC creator launchpad) is for sale with 3 followers [M: S31]. Traders and Solana's co-founder are sceptical that social accountability works for memecoins [S: S46].
- (−) 0/20 multi-wallet coins had a team lock (n=20, hand-picked sample from the Salary census, illustrative, not representative) [V: S9]. The lock fields would mostly be empty.
- (+) Nobody was shown to expose **lock cancel authority** or **payday (claim/payout) history** as a trader-facing field [U]. GMGN shows lock percent, not who can cancel [V: S40, negative grep].
- (+) Pump.fun, Axiom and Photon UI display of creator history or split recipients is still U [S: S36, S37, S43].

## Answers to the coordinator's questions

1. **Does the Gate 2 rejection survive on direct evidence?** Yes, and the evidence now covers more than before. The trader-facing job (has this dev or team launched before, rugged, sold, how much is held or locked) is covered by vendor code: GMGN [V: S25, S40], Mobula [V: S19], MadeOnSol [V: S21] and Rug Munch [V: S23]. That is the **same job**, not part of it. Caveats: (a) it is API-level evidence; whether GMGN's UI renders these fields for a trader is U, though GMGN shipping a dev-score skill for agents shows it serves the job; (b) cross-launchpad coverage is only shown for pumpfun, pumpswap, meteoradbc and clanker [V: S19].
2. **The residual.** Its four parts are no longer all uncovered. Roster plus fee-split recipients: native on Bags [V: S39] and public on Pump.fun [V: S41]. Locks: GMGN shows lock percent and detail [V: S40]. Still uncovered: lock cancel authority and payday history, plus the bundling of all four into one record. **Demand evidence for the residual: none at any level** (no request, bounty, feature request, workaround or payment found; S46 is level-1 scepticism). The case against it is partly direct and partly absence. Direct: the components are shipped or trivially readable [V: S39, S40, S41], and 0/20 coins had locks (illustrative) [V: S9]. Absence: no demand found, after a search that was partial (Reddit, X and Discord blocked). Absence of demand does not prove there is none. But under SG5 it also cannot be read as an opportunity, and R4 (one release) is met directly by the Bags/GMGN code.
3. **Prices.** Rug Munch $0.06 per check [V: S23], MadeOnSol $0.005-0.02 per call [V: S21] and EUR 400/month [S: S34] are §9 kind **paid-product** (max level 4). But they are a listed price, not `price-paid`, `revenue` or `fees-paid`: no buyer or volume is shown. They are demand for a **different job**: trader- or agent-side deployer screening, which incumbents already serve. Their direction for this idea is (−) (the paying part is taken, at cents) or at best (0). They are not level-4 evidence for the Team Record. The EUR 400 tier is only a snippet, so it cannot support a material claim. DexScreener's $299 is a paid-product for listing info, paid by teams [S: S33], and is not trust-badge demand.
4. **Verdict.** REJECTED, not NEEDS MORE RESEARCH. A false reject is possible only if traders demand lock cancel authority and payday history specifically. No level-2+ signal for that exists. Both fields are one-release additions for GMGN or Bags, which already hold the adjacent data and the distribution. The NMR path would need new evidence, not more searching of the same space.
5. **Safeguard violations** (lint confirms 6, plus reviewer findings):
   - SG1: scorecard #2 (gating) cites only snippets S2-S6. The V sources S19, S21, S23, S25, S39 and S40 were never written into the scorecard.
   - SG3: `existing-solutions.md` has no `## Easy replicators` table. It exists only in the revalidation file.
   - SG4: the coverage table in `existing-solutions.md` lacks `Recent launches` and `Discontinued` rows. The work was done (revalidation (a) and (c)) but not recorded there.
   - SG2: final-verdict.md:10 quotes a sample statistic without `n=` (lint). The "0/20" in existing-solutions and the prior review also lacked sampling wording.
   - SG6: final-verdict.md has no `## Unresolved uncertainties` section.
   - §9: `market-research.md` has no `## Demand evidence` table with kinds. It uses a free-form level table. The revalidation misclassifies DEXTools tutorials as "actively seeking" (they are press-coverage/discussion, level 1), and "vendors build it" as "using", which is not a §9 kind. It also counts npm downloads as level-3 usage without a bot-inflation reason, and for API use in general, not this job. The S34 EUR 400 price is shown as V-adjacent "paying" while it is snippet-only.
   - Records: existing-solutions and competitor-analysis still carry the overstated S-claims (Mobula "spans Bags, Moonshot, Believe"; RugCheck creator flag) that the revalidation corrected. The revalidation exceeded its ir.py call cap by about a third (self-reported). The Mobula SDK "about 3,800 weekly downloads" figure has no source row.

## Attack table

| Attack | Finding | Evidence | Does the idea survive? |
|---|---|---|---|
| Why will it fail? | The core job (dev or team history, rugs, holdings, locks) is in GMGN's own API and in three paid vendor APIs. The residual fields are mostly empty (0/20 locks, illustrative) | [V: S19, S21, S23, S25, S40]; [V: S9] | No |
| Why won't customers care? | Traders decide inside terminals that already show dev history, team hold and locks. No request for cancel authority or payday history found. Traders are sceptical of social accountability | [V: S25, S40]; [S: S46] | No |
| Which competitor already solves it? | GMGN (dev score, lock detail, fee income), Bags (native roster + fee-split + verified socials), Pump.fun (public shareholders), Mobula, MadeOnSol, Rug Munch, Bubblemaps (team clusters), 7+ repos | [V: S19, S21, S23, S25, S26, S39, S40, S41]; [S: S42, S45] | No |
| Why is the business model weak? | Trader side priced at cents per call, with volume U. Team side: a comparable reputation business shut down (Talent Protocol), KYC launchpad for sale. No named payer | [V: S21, S23]; [C: S30]; [M: S31] | No |
| Why will distribution be hard? | GMGN and Bags own both the data and the screen. A badge needs a terminal partner; that test was never run | [V: S25, S39]; [S1] | No |
| Why is the differentiation insufficient? | What is left (cancel authority, payday history) is a few account reads. Bags or GMGN already hold the adjacent fields and can ship it in one release (fails R4) | [V: S9, S39, S40, S41] | No |
| Which critical assumptions are unproven? | That traders weight cancel authority or payday history; that teams opt in; that a terminal displays it. Also U: Pump.fun, Axiom and GMGN UI display | [S1]; [U] | Unproven |
| Does it need the token? | No. It is an indexing service | [V: S9] | n/a |
| Regulatory exposure | Defamation risk from "rugger" labels; identity claims are unregulated | [S: S11, S46] | Manageable with facts-only wording |

## Claims still unverified

- GMGN, Axiom, Photon and Pump.fun UI display of creator history, split recipients or lock authority [U]. The GMGN evidence is API and skill code only.
- Bags token-page display of the claimer roster [S: S42]. The SDK field is V [S39].
- Which launchpads Mobula's wallet-deployer endpoint covers [U].
- Sales volume for every listed price: Rug Munch, MadeOnSol, DexScreener, CertiK [U]. The EUR 400 tier is S only [S34].
- RugCheck `lockers` and creator history [S: S44, S35].
- Demand in the channels that were blocked (Reddit, X, Discord) [U].

## Reviewer's recommended verdict

**REJECTED (rejection stands, now on direct evidence).** Strongest reason: vendor code shows GMGN already serves the trader-facing dev and team track record, including lock detail and fee income [V: S25, S40], and Bags natively exposes the team roster with fee-split shares and verified X handles [V: S39]. What remains (lock cancel authority, payday history) has zero demand evidence at any level and is a one-release addition for the incumbents that hold the data and the screen.
