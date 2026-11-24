# 08 — Dashboard Build Playbook

A dashboard is an argument, not a pile of charts. Each widget answers exactly one question, and the
top-to-bottom order walks a reader from "what is this" to "so what should I do." This is the 10-step
build and the four archetypes the source dashboards reduce to.

## The 10 steps

1. **Name the decision.** Who reads this and what will they *do* differently? ("Should I LP in
   SolFi?" / "Is Pump.fun losing share?") No decision → no dashboard.
2. **Pick the archetype** (below) — it fixes the layout and the metric set.
3. **List the KPIs** as a metric family (`03`): a level, a rate, a ratio, a behavioral cut. Not five
   levels.
4. **Map each KPI to a template** in `assets/dune-query-library.sql`; note the entity and grain.
5. **Write each widget query clean** (`09` Cleanliness Checklist), parameterized.
6. **Validate every query** (MCP → `dune_run.py`) — zero rows or absurd values get fixed *before*
   they reach the dashboard. The dashboards that failed (BTC/MON timeouts) failed here.
7. **Order the layout**: title + thesis → exec-summary counters → trend → behavior → concentration /
   risk → competitive → verdict.
8. **Add narrative widgets** — one-line finding under each section; the reader shouldn't have to
   infer the point.
9. **Set the refresh cadence** and parameters (so it's reusable, not a one-off snapshot).
10. **End on the recommendation** — the explicit decision + when to re-check.

## The four archetypes

- **Market-Structure** (who's winning a sector): leaderboard + market-share-over-time + concentration.
  Templates 5, 11, 6, 15. Reader: trader/investor picking a venue or a sector.
- **Signal** (is it time to act): a regime/ratio indicator over a long horizon (MVRV-style, priced
  in BTC, accumulation signal). Reader: allocator timing entries/exits.
- **Token Health** (is this token sound): holder growth + distribution + whale/concentration +
  retention. Templates 7, 12, 8, 13. Reader: due-diligence / risk.
- **Protocol War** (A vs B): the same metric family for two protocols side by side — users, creation,
  graduation, revenue, share. Reader: competitive strategy / investment thesis.

Most real requests are one of these four. Identify it first; it tells you the widgets before you
write any SQL.

## The Dashboard Build Package (what you hand over)

There is **no public API to create a Dune dashboard** — dashboards are assembled in the UI from saved
queries. So deliver everything needed to stand one up in minutes:

1. **Spec** — fill `assets/dashboard-spec-template.md` (archetype, objective, KPIs, datasets).
2. **Queries** — one clean query per widget, each passing the Cleanliness Checklist. If a
   `DUNE_API_KEY` is set, `create` each so the package carries real `query_id`s and URLs (then it's
   drag-and-drop).
3. **Layout** — the top→bottom order above, each widget mapped to its query and chart type.
4. **Narrative** — the section findings and the thesis text widgets.
5. **Recommendation + cadence** — the decision it drives and when to re-check.
6. **Assembly steps** — "in Dune: New dashboard → add visualization → pick query `<id>` → set chart
   type → arrange per layout."

Deliver as one organized response (or a saved `.md`) with all SQL paste-ready and the spec filled.

## Chart choices that answer one question

- Trend over time → line/area. Share snapshot → pie. Share over time → stacked area. Ranking →
  table (sorted) or horizontal bar. Distribution → bucketed bar. Retention → heatmap/triangle.
  Concentration → Pareto (ranked bar + cumulative line). Two-protocol compare → grouped bars.
- One question per chart. If a widget needs two sentences to explain, split it.
