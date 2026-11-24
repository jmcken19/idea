# Salary postmortem (historical)

Investigated 2026-11-24 from `jmcken19/salary`: 59 commits across 7 branches, plus every doc in `docs/` and `docs/research-v2/` (the latter on branch `claude/gracious-wozniak-andkx3`, never merged). Times are UTC.

## 1. The original problem
Meme coin creator fees go to one wallet. The people building a coin (devs, mods, CTO leads) are paid informally or by selling tokens, which hurts holders. The idea was to point creator fees at the team as salaries, so builders are "paid by volume, not by selling" (`docs/design.md`).

## 2. How the solution evolved (all within about 11.5 hours)

| Time (Nov 23–24) | Concept | Evidence |
|---|---|---|
| 15:46 → 16:12 | A **read-only checker** for a coin's Pump fee split, team locks and override keys is already built, with sealed fixtures and a 20-coin blind study | commits `07cddb1`, `e913118` |
| 16:38 | **Vault design:** a Salary program owns the fee split; builders lock tokens to stay on payroll; a broken lock triggers buybacks | `docs/design.md` |
| 16:45 | "No paid audit, no mainnet deploy": pivot to **existing programs** (Squads + Streamflow + Jupiter Lock) | `docs/infrastructure.md`, `design-existing-programs.md` |
| 17:27–18:30 | Holder pot, setup wizard, weekly payday, lock rules (80% rule), side-wallet flags | `docs/review-notes-2026-11-23.md` |
| 18:30 → 23:40 | **Website**: about 8 visual directions, an animated payday flow, a $FARTCOIN demo dashboard; pricing (1% payday fee, Pro plan) added and then removed | 35 `web:` / design commits |
| 22:12–22:17 | Product decisions: "Salary is a payroll platform"; MVP spec | `PRODUCT-DECISIONS.md`, `MVP-SPEC.md` |
| 00:06 | **Reposition:** "Pump.fun splits fees. Salary runs your team." The doc admits the differences are "real but thin … Pump.fun could copy" | commit `87294d6` |
| 03:14–03:18 | **Market research (research-v2)**, written from search snippets; proposes the **Team Record + Team Launch** pivot; defines kill tests and runs none | commits `983aa16`…`e38c4e9` |

## 3. Research that was done
- **Excellent technical research:** account layouts decoded from SDK source and IDLs, independent sealed decodes, live mainnet census (903,612 fee-sharing configs; 420,580 Jupiter Lock escrows; 80,332 Streamflow contracts), and override keys identified.
- **Market research came last:** five parallel reports and a consolidation, built from search snippets because pages couldn't be fetched. It concluded that gaps exist ("That is the opening for Salary") without checking for deployer-history tools.

## 4. Competitors and products that were overlooked, or seen but misfiled

| Product | Status in the Salary work | What it actually meant |
|---|---|---|
| **Pump.fun fee sharing**: up to 10 wallets, live 2026-01-09 (SDK 1.25.0), 318 days before the first commit | Documented on day one as *infrastructure* | **The core idea already existed, free, on the target platform** |
| **Bags fee share**: up to 100 claimers, editable | Documented as *infrastructure* | Covered "more than 10 people" and "change pay later" |
| **Streamflow payroll / Squads spending limits and Recipients** | Chosen as *building blocks* | Together they are a team payroll stack. "Salary on existing programs" was a setup guide for products teams could use directly |
| **pumpdev.io scheduled claim and distribute**, j.tools, PumpPortal, open-source distributors | Never found | The "payday" layer already existed as tools (pumpdev.io S-grade, to verify) |
| **Clanker / Zora / 0xSplits** on Base | Never considered | The same feature is standard on other chains |
| **MadeOnSol Deployer Hunter, Mobula dev-history API, Rug Munch, Noesis /dev** | Never found; research-v2 claimed "there's no trusted developer reputation" | The pivot also targets an existing, crowded category |

## 5. Was the differentiation meaningful?
No. After removing what Pump.fun, Bags, Squads and Streamflow already did, what was left was a USD display, a memo-based payday record and a 3-day notice rule. These are presentation and policy features, and the project's own decision log said Pump.fun could copy them. The "durable" differentiators that were proposed (rule-based pay, smoothing, work history) were unbuilt, untested hypotheses. One of them, work history, is a category that already exists.

## 6. Where the research and validation process failed
1. **Wrong first question.** "How do we build it?" came before "who already does it?". The checker was built within 26 minutes of the repo's creation (L2, L10).
2. **Dependencies were not assessed as competitors.** The equivalents were found and filed as infrastructure (L1).
3. **Negative data was explained away.** 95.4% of coins don't split; 0/20 team locks; fees concentrated in a few coins. All recorded, none acted on (L3).
4. **Repositioning replaced rejection.** When the overlap became undeniable, the pitch moved instead of stopping (L4).
5. **Design work stood in for validation.** 35 of 59 commits were website and brand work (L5).
6. **No payer.** Revenue was "OPEN" to the end (L6).
7. **Snippet evidence was treated as confident findings** (L7).
8. **Self-review.** The same process built, ranked and "stress tested" its own idea (L8).
9. **Kill tests were defined but never run** (L9).

## 7. What should have been investigated before development
In this order (about 20 searches and an hour of work):
1. Pump.fun's own docs and changelog: "fee sharing" (one search; it was in the news in January 2026).
2. Bags, Meteora/Jupiter Studio and Raydium LaunchLab fee-recipient features.
3. Search "claim and distribute creator fees", "creator fee bot", and GitHub "creator fee distributor".
4. Streamflow and Squads as **substitutes**: "can a team do salaries with these today?" (Yes.)
5. On-chain: how many coins use the free split at all? (4.6%.) How many teams lock tokens? (≈0.) Who earns fees? (A few dozen coins.)
6. Who would pay, and how much, given the free native feature? (Nobody identified.)

Any one of steps 1, 4 or 5 should have stopped development.

## 8. Rules created
L1–L10 in `system/lessons-learned.md`. Enforced by `system/validation-framework.md` (gates and order), `system/scoring-framework.md` (the Salary gate: an existing equivalent plus no meaningful difference means REJECTED, whatever the total), `tools/ir.py lint` (no CONDITIONAL/VALIDATED without an independent adversarial review) and `CLAUDE.md` (no build output).
