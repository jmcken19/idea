# 03 — Protocol KPIs

The metric families every protocol question reduces to, what each one actually measures, the trap in
each, and which `assets/dune-query-library.sql` template implements it. When a founder asks "how is
my protocol doing," you answer with a *family* of these, never a single number.

## The four KPI families (and why one number lies)

| Family | Question it answers | Examples | Template(s) |
| --- | --- | --- | --- |
| **Level** | How big? | volume, TVL, fees, revenue, holders | 4, 7, 10, 16, 17 |
| **Rate** | How fast changing? | DAU growth %, new wallets/day, holder arrival | 1, 2 |
| **Ratio** | How does it compare? | market share, graduation rate, fee-to-TVL | 5, 11, 18 |
| **Behavioral** | Who and how sticky? | new vs returning, retention, cohorts, whale mix | 3, 12, 13, 14 |

A level alone ("$40M volume") is unfalsifiable hype. A level + its rate + a ratio + a behavioral cut
is an analysis.

## Activity & users

- **DAU / WAU / MAU** — `approx_distinct(signer)` over `solana.transactions` (chain-level) or joined
  to `solana.instructions` on `program_id` (protocol-level). Template 1. Use `approx_distinct`
  (HyperLogLog) — `COUNT(DISTINCT)` over Solana volumes is slow and often unnecessary.
- **New vs returning** — the quality companion to DAU. First-seen CTE → `count_if(day = first_day)`
  vs `count_if(day > first_day)`. Templates 2 & 3. The split must sum to DAU — validate it.
- **DAU/MAU stickiness ratio** — DAU divided by MAU; >0.2 is sticky for a consumer protocol. Cheap,
  powerful, rarely shown.
- **Trap:** wallet ≠ user. Bots and sybils inflate every active-wallet count. Caveat it, and where it
  matters, segment with `05`/`06` before calling them "users."

## Volume, TVL, fees, revenue — the money metrics

- **Volume (USD)** — `sum(amount_usd)` over `dex_solana.trades` by `project`/`token`. Template 4.
  The most comparable cross-protocol metric. Beware both-legs double counting — verify totals.
- **TVL** — value locked in a protocol's accounts. There is **no single Spellbook "tvl" column**;
  TVL is reconstructed: net token balances held by the protocol's program/vault accounts × price.
  For a quick, reliable read prefer **DefiLlama** (it already does this and is the market's trust
  metric); reconstruct on-chain only when you need a custom or real-time cut. Document the method.
- **Fees** — what users pay. Real fee models beat proxies; where none exists, proxy as
  `volume × fee_bps` (Template 10) and **label it a proxy**.
- **Revenue** — what the protocol keeps (protocol fee share), distinct from total fees (which include
  the LP/supply-side cut). Conflating fees and revenue is the most common founder-deck error —
  separate them explicitly.
- **Revenue quality ratios** — fee-to-TVL (capital efficiency), revenue-per-active-user, take rate
  (protocol revenue ÷ total fees). These separate a business from a hype machine.

## Growth, retention, cohorts

- **Holder / user growth** — cumulative + arrival rate (Template 7). Cumulative-only hides a stall;
  always show the new-per-day bars next to the running total.
- **Retention** — of wallets first active in week *w*, what share return in later weeks (Template
  13). Define "active" explicitly (a trade? any tx?). Render as a cohort triangle/heatmap.
- **Acquisition cohorts × value** — monthly cohort size vs lifetime volume per wallet (Template 14):
  did the users you acquired in March spend more or less than April's? Annotate survivorship (recent
  cohorts have had less time to accrue).
- **Trap:** incentive-bought growth isn't growth. When an emissions program or airdrop farm is live,
  separate organic from incentivized cohorts (see `06` sybil section) before reporting retention.

## Competitive position

- **Market share** — `volume / sum(volume) OVER ()` across projects (Template 11). The normalization
  that makes levels meaningful; always state the window, because share is window-dependent.
- **Share over time** — stacked-area of share, not just level — shows who's *taking* share, the real
  competitive story (the Pump.fun vs LetsBonk and DEX-Metrics pattern).
- **Graduation / funnel rates** — for launchpads, the % of created tokens that reach a milestone
  (e.g. bonding-curve graduation). A ratio that exposes whether activity is healthy or churn.

## The protocol-health one-pager (what to actually deliver)

When asked "analyze this protocol," return this set, each with its caveat:
1. Volume + trend (level + rate).
2. Active wallets: DAU with new-vs-returning split (engagement + quality).
3. Retention cohort (does it keep users).
4. Market share vs peers over time (competitive position).
5. Revenue (kept, not just fees) + a capital-efficiency ratio.
6. Holder distribution headline (concentration risk — see `05`).
7. One forensics sanity check (is the volume real — see `06`).
8. **The decision:** is this growing, defensible, and real? What should the team/investor do?

That one-pager, validated and caveated, is worth more than any single chart — and it's exactly what
the dashboard playbook (`08`) and the grant report (`07`) assemble from.
