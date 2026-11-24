# Final verdict

**Verdict:** REJECTED

Decided on: 2026-11-24 (historical test of the idea as of 2026-11-23)
Decided by: Research Lead, after the independent adversarial inverse check (rejection stands)

## One-paragraph reason

The core job, distributing a coin's creator fees across several wallets, was a free native Pump.fun feature 318 days before Salary's first commit. `sharingConfig` first appears in `@pump-fun/pump-sdk` 1.25.0 (2026-01-09) [V: S6], and its mechanics were verified on chain [V: S1]. Bags already offered 1–100 editable claimers [C: S1, S10]. The "salary" layer (changeable, scheduled team pay) is covered by sending the split to one Squads vault and paying out with Squads or Streamflow [V: S1; S: S14, S15], and by open-source claim and redistribute tools [V: S16]. The remaining differences (USD view, memo record) are presentation features that the project itself said Pump.fun could copy [V: S2]. The only verified demand data is negative: 95.4% of fee-sharing configs have a single recipient, and 0 of 20 multi-wallet coins had a team lock [V: S1, S17]. No payer was ever identified [V: S2].

## Fatal issues
1. A free native equivalent on the target platform (scorecard #2, fatal).
2. No meaningful, evidenced differentiation (the Salary gate: #1 ≤ 1 and #2 ≤ 1).
3. Negative behavioural demand evidence (#3 = 1).

## Reviewer corrections accepted
- Pump's native split is a *partial* equivalent for teams that change (≤10 wallets, one change after launch). The full equivalent for changing teams is Pump split → Squads vault → Squads/Streamflow, or Bags.
- pumpdev.io was downgraded to an unverified lead. The verdict does not rely on it.

## What evidence would change this verdict
Level-4 evidence that multi-contributor meme teams pay for scheduled, changeable payroll that they cannot get from Pump + Squads/Streamflow or Bags. For example, 10 or more teams paying for a hand-run payroll service. None exists today. This would be a new intake.

## Evidence quality and gaps
Native-feature and demand evidence is V (SDK, chain). Several third-party tools are S only (page fetches blocked). Not checked: token launches with the same pitch (DexScreener/CoinGecko blocked) and dead projects (Wayback blocked). None of these could rescue the idea, because the fatal issue is the native feature.

## Research completeness

| Stage | Complete / skipped (why) |
|---|---|
| 1 Intake | Complete |
| 2 Existence | Complete (failed gate); token-launch and Wayback channels blocked |
| 3–5 | Skipped by gate; existing Salary data recorded at no cost |
| 6 Adversarial | Inverse check and attack table complete (rejection stands) |
| 7 Decision | Complete |

## Historical cost of not doing this
59 commits, 7 branches, a website with about 8 visual directions, a read-only checker, design docs and two research rounds. The kill-check above cost about 16 searches. See `postmortem.md`.
