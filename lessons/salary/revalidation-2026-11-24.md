# Salary: second Stage 2/3 investigation (revalidation), 2026-11-24

Question: does the Gate 2 rejection survive deeper, primary-source investigation? Segment tested: **multi-contributor Solana meme teams that want changeable, scheduled pay from creator fees.**

Budget used: 13 WebSearch (all logged); 29 npm-grep / github-raw / github-repos calls (14 npm-grep, 6 github-raw, 9 github-repos), plus 5 `fetch npm` metadata calls and 9 read-only `git clone --depth 1` reads (nothing run). Network blocks confirmed: DexScreener, CoinGecko, DefiLlama, Wayback, pump.fun, pumpdev.io website, docs sites and `github-raw .../HEAD/README.md` (404; clone used instead).

## Bottom line

The rejection **holds, but its foundation moves**. At primary grade, no verified product delivers *changeable AND scheduled AND fee-linked* team pay turnkey. The "Full" overlap rating for Pump.fun and the "scheduled" claim for pumpdev.io were overstated. The rejection now rests on (1) Bags, which natively covers changeable multi-payee splits [V: S25], (2) cheap composition and replication, and (3) the negative demand data (Gate 4 side), not on a verified turnkey equivalent. Direction label: the changes below mostly **support the opportunity's technical gap** and **do not change the demand evidence**.

## Evidence upgrades

| Claim | Old tag | New tag | Source | Did it hold? |
|---|---|---|---|---|
| Pump max shareholders = 10 | V (S1) | V (second primary) | S24 `MAX_SHAREHOLDERS = 10`, `TooManyShareholdersError` | Held |
| Pump split changeable once, then locked | S (S21) | **V** | S24 IDL msgs "Reward split can only be updated once"; "Sharing config authority has been revoked - sharing config can only be updated once"; README "Reward distribution can be configured only once" | Held. Corroborated C: S35 |
| Pump distribution is manual and permissionless, no scheduler | S (reviewer note) | **V** | S24 `distributeCreatorFees` documented "Permissionless"; no interval or scheduler in SDK; S31 dev-fee-harvester README: "takes no signer, anyone may crank it" | Held. Pump itself offers no payday timer |
| Bags 1-100 claimers, bps total 10,000 | C (S1, S10) | **V** | S25 `Total BPS must be 10000`, `totalFeeClaimers > 100` check | Held. Note: the 100 limit needs lookup tables above 15 claimers (S25 constants) |
| Bags admin can edit claimers after launch | C | **V** (code) + S (docs) | S25 `FeeShareAdminService` posts `/fee-share/admin/update-config` and `/admin/transfer-tx`; S38 | Held: Bags is changeable, no one-change cap found |
| Squads spending limits with periods | S (S15) | **V** | S26 `Period` OneTime/Day/Week/Month; `spending_limit_use.rs` requires `member: Signer` | **Partly**: it is a per-period allowance a member must sign to pull. It is **not** an automatic scheduled payout |
| Squads "Recipients" recurring payments | S | S | S36 | Snippet says it creates reminders and pre-filled payments, i.e. manual approval each cycle. Weaker than "scheduled pay" implied |
| Streamflow recurring/scheduled payroll | S/M (S14) | **V** | S27 `automaticWithdrawal`, `withdrawFrequency`, `amountPerPeriod`, `canTopup`; client `update`, `topup`, `transfer`, `cancel` | **Held, and stronger**: it really pushes scheduled payments, editable. It cannot ingest creator fees itself (no such feature found; S search) |
| Clanker multi-recipient rewards with admins | S (S18) | **V** | S28 `rewardAdmins`, `rewardRecipients`, `rewardBps` | Held (Base only) |
| 0xSplits mutable multi-recipient splits | S | **V** | S29 split `controller` field, `distributeToken`, `transferOwnership` | Held; not sunset (S: S39) |
| pumpdev.io claim-and-distribute, scheduled hourly | S (S11) | **V that it exists; scheduled NOT verified** | S30 repo `pumpdev3/pumpdev.io` README lists `POST /api/claim-distribute`, no scheduler or interval text | **Did not hold as described.** It is a trading/launch API with an on-demand distribute endpoint; "recurring hourly schedule" stays S/U |

### What the open-source distributors actually do (READMEs read, S31)

| Repo | What it does | Team payroll? |
|---|---|---|
| tradewife/fartnode | Cron-style distributor: claims creator fees, snapshots `$FARTNODE` holders, pays them pro rata. Last commit 2025-11-18 | No (holders) |
| Hymetdotfun/hymet-distributor | Anchor program for the HYMET launchpad: collects Meteora fees, 20% to HYMET, rest to creator and holders | No (one launchpad) |
| dullbenz/best_buddy | Four-bucket distributor program for one coin ("Buddy"): staking pool, holders, influencers (streamed), team (12-month stream with cliff) | No (single-coin, frozen parameters) |
| openpumptrade/pumpkit | JS library of building blocks: claims, burns, airdrops, `writeFeeSharing`, `readSharingConfig`, `distributeSharedFees` (permissionless). A DIY payroll cron is a few calls | Toolkit, not a product |
| daronthedragon/dev-fee-harvester | CLI: finds fees across a creator's own wallets (including shared-config balances), batches claims, can crank `distribute_creator_fees` | No (claim-for-yourself) |
| 0xbl33p/pumpfun-tiktok-fee-share | Web app: custodial per-TikTok-handle share wallet that a TikToker later claims; README says Pump fee-share "is single-shot" | No (creator-to-influencer) |

None is a team payroll product. All of them confirm that claim/distribute building blocks are trivial and public.

## New competitors

| Product | What it does | Evidence | Overlap for the segment |
|---|---|---|---|
| **Splitdev** (furkan3152/ponsplit, splitdev.app) | Pump.fun launchpad front-end: up to 9 GitHub devs + treasury; locks the split permanently; permissionless "Distribute now" | V (README, S32); live status U | Partial: multi-contributor, but **locked by design**, the opposite of changeable pay. Zero stars, created 2026-09-27 |
| **Solana Recurring Delegations program** (Solana Foundation, 2026-06-02) | Audited native program for scheduled delegated pulls; integration-tested with Squads | S (S36) | Building block for scheduled pay, not fee-linked |
| omarpatel/fee-split-vaults-postmortem | Not a competitor: an independent EVM builder who built a creator-fee vault protocol and abandoned it after a market measurement returned STOP | V for existence (S33); the analysis is the author's (E) | Corroborates the rejection (see below) |
| Recent GitHub items (S34): streampad (75/25 streamer split), callers, spore (50/50 split), Solana private-payroll hackathon repos | Launch-time splits or generic payroll; none links creator fees to scheduled changeable team pay | V (metadata), descriptions only | Adjacent |

## Competitors weakened or removed

| Cited as | Finding | Effect |
|---|---|---|
| **Pump.fun fee sharing = "Full"** | One change then permanent lock, 10 wallets, no scheduler, and Pump deliberately restricts edits ("anti-griefing", S35) [V: S24] | **Downgrade to Partial** for changeable, scheduled team pay. Still Full for static splits |
| **pumpdev.io = scheduled distribution** | Exists, but repo shows on-demand endpoint only [V: S30] | Downgrade to a building block; the "scheduled" evidence is gone again |
| **Squads = scheduled pay** | On-chain: allowance a member must sign [V: S26]. App Recipients: reminders [S: S36] | Downgrade: it is approval-gated, not automatic |
| **Sablier (EVM streaming)** | Maintenance mode 2026-07-13; Solana UI shut end of June 2026, weak usage cited [S: S37] | Removed as a live competitor; also a **negative demand signal** for streaming-payroll as a category |
| Request/Rise/Deel/Zebec | Zebec self-reports about 243 enterprise clients (M); not tested for meme teams | Still adjacent, not weakened |
| Pump "scrapped creator fees" (dailycoin headline) | Not scrapped: Jan overhaul, Feb cashback option, Mar one-change cap [S: S35] | No change |

## Skipped channels

| Channel | Status | Result |
|---|---|---|
| (a) Tokens pitching payroll/team pay/fee-split tooling | **Blocked** for DexScreener/CoinGecko (proxy 403). Done via WebSearch + GitHub | No token or project found pitching payroll from creator fees. No launchpad pays payroll automatically (S: WebSearch, logged) |
| (b) Discontinued/dead tools | Done (WebSearch + GitHub); **Wayback blocked** | Sablier winding down (S37). No dead creator-fee split tool found. fartnode last pushed 2025-11-18 (stale, not a competitor) |
| (c) GitHub, including last 90 days | Done (S34) | Zero recent repos combine creator fees with scheduled team payroll. Splitdev (locked), pumpkit (toolkit), 21 generic "solana payroll" repos with 0-1 stars |
| (d) Other chains | Done | Clanker V (S28), 0xSplits V (S29), Sablier S dead. four.meme: no split feature found (S40). Superfluid, LlamaPay, Hedgey: no 2026 news found either way (U). Base/Ethereum primitives support splits and streams but no meme-team payroll product found |
| pumpdev.io website | **Blocked** | Primary evidence from GitHub repo only |

## Easy replicators (could ship scheduled, changeable team pay from creator fees)

| Product | Capability evidence | Effort to ship | Incentive |
|---|---|---|---|
| **Bags** | Admin-editable claimers up to 100 [V: S25]; fees flow natively | Add a scheduler or payday UI on existing config | High: it already sells fee share to partner apps (S38). No scheduler found |
| **Streamflow** | Scheduled auto-withdrawal, editable, top-up [V: S27] | A fee-source connector plus a dashboard; fee routing needs Pump recipient = a funded vault | Medium: markets "web3 payroll" (S14, M) |
| **Squads** | Spending limits [V: S26]; Recipients + native Recurring Delegations tested with Squads [S: S36] | Auto-execution of recurring recipients | Medium: not meme-focused |
| **Pump.fun** | Permissionless distribute [V: S24] | Trivial technically | **Low**: it chose to restrict edits as anti-griefing (S35), and says fees are for "trenchers" |
| **DIY bot / pumpkit / pumpdev API** | `writeFeeSharing`, `distributeSharedFees`, claim-distribute endpoint [V: S30, S31] | A cron plus a wallet list, about a day | n/a: the free substitute |
| Terminals (Axiom, Photon, GMGN, BullX) | No fee-share management found (S) | Unknown | Unknown |

## Revised overlap table (segment: multi-contributor Solana meme teams, changeable and scheduled pay)

| Product | Static split | >10 payees | Changeable | Scheduled | Fee-linked | Turnkey for meme teams | Revised level (old) |
|---|---|---|---|---|---|---|---|
| Pump.fun native | Yes V | No V | One time V | No (manual crank) V | Yes | Yes | **Partial** (Full) |
| Bags native | Yes V | Yes V | Yes V (admin) | No found | Yes | Bags coins only | **Partial-high** (Full) |
| Pump split to one vault + Squads | Yes | Yes | Yes | Reminders / member-signed (V/S) | Yes | No, DIY assembly | Partial (composite) |
| Pump split to vault + Streamflow | Yes | Yes | Yes V | Yes V (auto-withdraw) | Needs manual funding | No, DIY assembly | Partial (composite) |
| pumpdev.io | Endpoint V | U | U | Not verified | Yes | Developer API | **Building block** (Full/unverified) |
| Splitdev | Yes V | No (10) | **No, locked** | Manual | Yes | Yes (GitHub devs) | Partial, wrong direction |
| Open-source distributors | Varies | Varies | Varies | Cron | Yes | No, code | Building blocks |
| Clanker / 0xSplits | Yes V | Yes | Yes V | No | Yes | Base/EVM only | Full on another chain |
| Request/Rise/Zebec | No | Yes | Yes | Yes | No | Not for meme coins | Adjacent |

Reading: nothing verified is a full equivalent *for this segment turnkey*. Bags is the nearest. The remaining overlap is composition (R1: "this plus a spreadsheet"), which the original review argued, and it still works but needs user effort.

## Evidence AGAINST the rejection (equal weight)

1. **The overlap was overstated.** The Gate 2 table called Pump "Full" and relied on pumpdev.io for "scheduled". Primary evidence shows a one-change lock, 10-wallet cap, no scheduler [V: S24], and pumpdev.io's schedule is unverified [V: S30]. Squads is approval-gated [V: S26]. A turnkey changeable-and-scheduled tool does not exist in anything I could verify.
2. **Pump's lock is a structural gap.** Because Pump allows one change then freezes, a team that changes cannot use the native split; it must route to a single vault. That is where a product could live. Note that the 95.4% single-recipient figure [V: S1] could include teams that route to a treasury; Salary's data cannot distinguish this (unknown).
3. **Pump's incentives are not to replicate.** It restricts editing on purpose (S35), lowering the "incumbent ships it in one release" risk for Pump specifically. Bags, Streamflow and Squads remain able to.
4. **No complaints found are not proof of absence.** My searches found no developer complaint about the one-change limit, but also no one asked for the feature; the absence cuts both ways (U).

Evidence that supports the rejection and surfaced in this pass:
- Sablier retreated citing weak usage (S37): payroll streaming is a hard category.
- An independent builder reached STOP on a near-identical creator-fee split product on another venue because incumbents' distributors had already captured recipients (S33; author's own measurement, E).
- Splitdev launched the opposite design (permanent lock) for multi-dev coins, suggesting the market values trust over changeability (inference, H).
- 21 recent "solana payroll" repos at 0-1 stars; none ties to creator fees (V metadata).
- No new demand evidence found anywhere.

## Still unverified

- pumpdev.io scheduled/recurring distribution and traction (website blocked).
- Squads Payments exact automation level (docs blocked; snippet says reminders).
- Whether any teams route Pump fees to a treasury and pay manually (the real demand question; needs on-chain read, which this network blocks).
- Superfluid, LlamaPay, Hedgey status and meme-team use in 2026.
- Terminal (Axiom, Photon, GMGN, BullX) fee-share features.
- Splitdev live traffic and whether the site is up.
- Token launches pitching payroll (DexScreener/CoinGecko blocked).
- Streamflow's actual price for the stream and any creator-fee connector.
- Bags' scheduler roadmap, and whether more than 15 claimers work in practice.
