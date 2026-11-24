# Stage 4: Demand validation

Not required after the Gate 2 rejection. Recorded from data the Salary project already held on 2026-11-23, because this is the evidence that should have stopped it.

| Level | Evidence | Tag + source | Strength |
|---|---|---|---|
| 1. Discussing the problem | Pump.fun said creator fees "skewed" incentives (Jan 2026). Anecdotes about unpaid contributors | [S: S20] [S3: "Weak"] | Weak |
| 2. Seeking a solution | No requests for "payroll from creator fees" found | U | None |
| 3. Using existing solutions | Only 4.6% of configs split at all (n=3,000 random of 903,612; ≈42k coins by extrapolation); 95.4% have one recipient | [V: S1] | *First pass said "strong, negative". Second pass: **ambiguous**: a single recipient can be a treasury; not fee-weighted; measures static splitting, not the salary layer* |
| 4. Paying | No paid team-pay product for meme coins found with traction. Teams do pay $299 for DexScreener profiles (a trust signal, not pay) | [V: S1] | None for this job |

| Question | Answer | Tag |
|---|---|---|
| Who experiences it? | Multi-contributor meme teams earning real fees: a small set if creator fees are concentrated in a few dozen coins (snippet-grade only; unverified) | [S: S3, S4] |
| Locks as a proxy for "builders who stay" | None of 20 multi-wallet coins had team locks (n=20, random, illustrative); 1 of 139 (n=139, not random) had a Streamflow lock to a paid wallet (closed) | [V: S1, S17] |
| Market size | Creator + cashback slice about $17M a month across all of Pump.fun (Nov 2026) | [E from V data: S1]; most of it to a few coins |
| Trend | Pump.fun revenue down about 75% year on year; creator-payout platforms collapsed | [S: S4] |

**Gate 4 (had it been reached): FAIL** for lack of level 2–4 evidence. *Second pass: the level-3 data is ambiguous, not clearly negative (see the Demand evidence table).*

## Demand evidence

Second pass, classified under `system/research-standards.md` §9. Reddit, X and Discord are blocked, so evidence at levels 1 and 2 is under-covered.

| Evidence | Kind | Level | Direction | Tag + source |
|---|---|---|---|---|
| About 42k coins (4.6% of configs, n=3,000 random) use Pump's native multi-wallet split | native-feature-usage | 3 | 0 (shows static splitting is used, and served free) | [V: S1] |
| 95.4% of configs single-recipient (n=3,000 random, not fee-weighted) | native-feature-usage | 3 | − weak (a recipient can be a treasury) | [V: S1] |
| No request, bounty or feature request for scheduled team payroll from creator fees found | request | 2 | 0: none found (partial search) | U |
| Sablier winds down Solana streaming UI, citing weak usage | paid-product | 4 | − (category signal, EVM-first) | [S: S37] |
| Independent EVM builder abandoned a creator-fee split-vault protocol after their own market measurement | workaround-built | 3 | − | [V: S33] |
| 21 recent "solana payroll" repos at 0–1 stars | stars | 1 | 0 | [V: S34] |
| Pump.fun co-founder: creator fees had little effect on the average deployer | discussion | 1 | − | [S: S20] |

Reading: nothing reaches a (+) level-3/4 row for the salary layer. The strongest evidence is level-3 usage of the free static split, which the incumbent already serves.
