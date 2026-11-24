# 07 — Growth & Grant Reporting

The cross-domain payoff: a founder doesn't need a query, they need a **report** that wins a grant,
closes a round, or proves traction to a foundation. This reference turns the metrics from `03`–`05`
into a credible narrative — and, just as important, keeps it honest, because foundations and
investors can read the chain too. A report that inflates gets caught; a report that pre-empts the
skeptic wins.

## The numbers that actually move a grant/raise decision

Reviewers have seen a thousand "we did $40M volume" decks. They discount levels and reward **quality
and durability**. Lead with these:

| Signal | Why reviewers trust it | Source |
| --- | --- | --- |
| **Retained users** (cohort retention) | Can't be faked with one-off incentives | Template 13 / `03` |
| **Organic vs incentivized split** | Shows what survives when emissions stop | `06` sybil + cohort tag |
| **Returning-user share trend** | Stickiness, not just acquisition | Template 3 |
| **Revenue kept** (not gross fees) | Real business vs volume theater | Template 10 / `03` |
| **Market-share trajectory** | Taking share > absolute size | Template 11 |
| **Holder distribution** | De-risks "is this just insiders" | `05` |
| **Real volume** (wash-filtered) | Pre-empts the obvious skeptic question | `06` |

A grant report built on *retention + revenue + share + clean volume* beats one built on *TVL + total
volume* every time, because the first set is the one a sophisticated reviewer can't wave away.

## CAC / LTV proxies on-chain (use carefully)

You rarely have true CAC (off-chain spend), but you can build defensible proxies and **label them as
proxies**:
- **Acquisition cost proxy** — incentive/emissions spend in a period ÷ net new retained wallets in
  that period. Frames "what did each kept user cost in tokens."
- **LTV proxy** — lifetime fees paid (or lifetime volume × take rate) per acquired wallet, by cohort
  (`05`). Pair with retention to project forward, and annotate survivorship.
- **Payback read** — LTV proxy ÷ acquisition-cost proxy per cohort: are later cohorts paying back
  faster or slower? A rising payback curve is a strong fundraising signal.

Never present these as audited financials — present them as on-chain-derived estimates with the
method stated. Reviewers respect "here's our proxy and its limits" far more than a suspiciously clean
number.

## The report skeleton (what to assemble)

1. **One-line thesis + the headline number** that survives scrutiny (usually a retention or
   revenue-quality figure, not gross volume).
2. **Traction** — DAU/MAU with new-vs-returning, the growth rate, and the trend chart.
3. **Stickiness** — the retention cohort triangle. This is the slide that wins or loses.
4. **Economics** — revenue kept, a capital-efficiency ratio, and the CAC/LTV proxy with method note.
5. **Competitive position** — market-share-over-time vs named peers.
6. **Distribution & trust** — holder distribution headline + the wash-filtered "real volume" number.
7. **What the grant/round funds** — the specific metric you'll move and the current baseline, so the
   foundation can measure you later (foundations love a pre-committed, measurable KPI).
8. **Method & honesty appendix** — sources (Dune query URLs), proxy definitions, and the caveats you
   already know they'd raise (wallet ≠ user, realized PnL, window-dependent share).

## Honesty floor (non-negotiable, and it's a feature)

- Show the **wash-filtered** volume next to gross, and explain the filter. Volunteering this builds
  more credibility than any inflated figure.
- Separate **organic from incentivized** growth explicitly. Reviewers will assume the worst if you
  don't.
- State every proxy's method. "Revenue" = protocol's kept share, not gross fees — say which.
- Link the **live queries** so reviewers can re-run them. Reproducibility is the strongest possible
  signal that the numbers are real.

## Output formats

- **Foundation/grant report** — the skeleton above as a tight doc, every chart sourced to a live Dune
  query, with the honesty appendix. Pair with `08` to ship a live dashboard the reviewer can poke.
- **Investor update** — the same numbers, monthly, with the delta vs last month foregrounded.
- **Narrative companion** — for a public-facing traction post, hand off to a narrative skill; this
  skill provides the validated numbers and caveats it must not contradict.

The deliverable is a report a skeptical reviewer *can't easily discount* — because you already did
the discounting for them, in the open. That is what wins the grant.
