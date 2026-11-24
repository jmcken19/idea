# 09 — Execution Playbook (Operator Mode)

The **do-it** layer. When the user asks you to *do something on Dune* — "write me a query for X",
"build a dashboard for Y", "pull the top holders of Z" — you deliver a clean, validated artifact, not
a lecture. Follow this end to end.

## Decide: query request or dashboard request?

- **Single answer / one metric** → ONE clean query (Query Delivery Contract below).
- **"Dashboard", "monitor", "track over time", multiple metrics** → a Dashboard Build Package (`08`).
- Ambiguous ("look at SolFi") → deliver the smallest useful thing (usually one query) and offer to
  expand it into a dashboard.

## The operator workflow (every task)

1. **State the business question** in one sentence; confirm entity (`project`/`token_mint`/
   `program_id`) and grain. Don't proceed on a vague target — ask for the mint/project if missing.
2. **Pick the lens** (`01`–`07`) and the matching template(s) from `assets/dune-query-library.sql`.
3. **Write the clean query** — adapt the template, not from scratch. Apply the Cleanliness Checklist.
4. **Validate** — run it (see "Executing" below). If you can't, dry-check it and say it's
   paste-ready-but-unrun.
5. **Deliver** via the contract — query + question + optimization + pitfall + viz.
6. **End on the decision** the query enables, and offer the next step.

## Cleanliness Checklist (apply before delivering)

- [ ] **Header comment** stating the business question.
- [ ] **CTEs over nesting** — name each step; no subquery pyramids.
- [ ] **Time-bounded** — every query filters `block_time` (use `{{days}}`); never an unbounded scan.
- [ ] **Parameterized** — `{{token_mint}}`, `{{project}}`, `{{days}}`, `{{decimals}}`, not literals.
- [ ] **Spellbook first** — `dex_solana.trades`, `tokens_solana.transfers`, `prices.usd`; raw only
      when necessary.
- [ ] **Normalized** — decimals via `power(10, …)`, USD via `amount_usd`; no naked raw amounts.
- [ ] **Cheap distinct** — `approx_distinct()` for large cardinalities.
- [ ] **Explicit columns + aliases** — no `SELECT *`; snake_case, human-readable.
- [ ] **Guarded math** — `nullif(x, 0)` on every division.
- [ ] **Deterministic order + LIMIT** for display queries.
- [ ] **One question per query** — if it answers two, split it.

House style: uppercase keywords, 4-space indent, one column per line in `SELECT`, JOIN conditions on
their own line, CTEs separated by blank lines. Match `assets/dune-query-library.sql`.

## Query Delivery Contract (the exact output shape)

```
**Business question:** <one sentence>

**Query** (Solana-first, DuneSQL):
<clean, runnable SQL in a sql block>

**Parameters:** <each {{param}} and what to set it to — token_mint = So111…, days = 30>
**Optimization:** <the one tip that matters most here>
**Pitfall:** <the one trap for this metric>
**Visualization:** <chart type + the single question it answers>
**Next:** <offer — e.g. "want this as a dashboard with new vs returning + retention?">
```

If you ran it: also add `**Validated:** ran on Dune, returned N rows, sample looks sane (or flagged
anomaly …)` with the query URL/id.

## Executing on Dune — pick the available path, in order

### Path A (preferred): a connected Dune MCP
If the session has a Dune MCP (this skill ships `.mcp.json` wiring one), use its tools — they handle
auth and are the user's intended interface. **Do not hardcode tool names**; discover them at runtime
by looking for tools whose names contain `dune` (run-query / run-sql / get-results / search — names
vary by version). Read the tool's schema, pass what it expects, report the real rows it returns.

### Path B (fallback): the bundled script
`scripts/dune_run.py` (stdlib only, no installs) drives the Dune REST API. It needs `DUNE_API_KEY`.
Creating queries needs an Analyst plan or higher; reading results works on lower tiers.
- **Validate (default):** create temp query, run, preview rows, delete:
  `python scripts/dune_run.py validate q.sql --params params.json`
- **Create a saved query** (dashboard widget): `python scripts/dune_run.py create q.sql --name "DAU — Solana"`
- **Run / refresh:** `python scripts/dune_run.py run <query_id> --params params.json`
- **Fetch cached results:** `python scripts/dune_run.py results <query_id>`

`params.json` is a flat object: `{"days": "30", "project": "raydium"}`. Always check the key is set
before promising execution.

### Path C (neither available)
Deliver paste-ready, mark it "not yet executed," and give the exact MCP call or `dune_run.py validate`
command the user can run themselves.

## Helius for current-state checks

For "right now" facts a SQL aggregate can't give (mint authority, freeze authority, live token
accounts, asset metadata — used heavily in `06` rug checks), use the Helius MCP (also wired in
`.mcp.json`) or document the exact RPC/DAS call. Helius is state; Dune is history — use each for what
it's good at.

## Honesty rules (non-negotiable)

- If you didn't run it, say "paste-ready, not yet executed." Don't imply validation you didn't do.
- If a query may time out (holder/balance reconstruction), say so and give the optimized version.
- Realized vs unrealized PnL, window-dependent share, wallet ≠ user — state these in the delivery.
- Never fabricate results, row counts, or numbers. No data is a finding; fake data is fraud.
