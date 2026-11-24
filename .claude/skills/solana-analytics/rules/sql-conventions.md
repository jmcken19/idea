# Rule: Solana Analytics SQL Conventions

Apply to every query this skill produces. These are not style preferences — they are what separates a
runnable, trustworthy query from slop. The full rationale is in `references/09-execution-playbook.md`.

## Correctness
- **Question-first.** A header comment states the business question before any SQL.
- **Real columns only.** Use Spellbook/Flipside table and column names that exist
  (`references/01-data-sources.md`). Never invent a column; confirm in the schema sidebar.
- **Normalize.** Decimals via `power(10, {{decimals}})`; USD via `amount_usd` or a `prices.usd` join.
  No naked raw `amount`.
- **Guarded math.** Wrap every divisor in `nullif(x, 0)`.
- **One question per query.** If it answers two, split it.

## Performance
- **Always time-bound** with `{{days}}` on `block_time`. No unbounded scans.
- **`approx_distinct`** for large-cardinality counts, not `COUNT(DISTINCT)`.
- **Pre-aggregate before joins**; balance reconstruction (templates 8/12) is timeout-prone — bound
  history or pre-aggregate daily net flow.
- Group/filter on partition columns (`block_date`) where available.

## Reusability
- **Parameterize** with `{{ }}`: `{{token_mint}}`, `{{project}}`, `{{days}}`, `{{decimals}}`.
- **Explicit columns + snake_case aliases.** No `SELECT *`.
- **Deterministic order + LIMIT** on display queries.

## Formatting
Uppercase keywords · 4-space indent · one column per line in `SELECT` · JOIN conditions on their own
line · CTEs separated by blank lines. Match `assets/dune-query-library.sql`.

## Honesty
- If you didn't run it, say "paste-ready, not yet executed."
- Flag realized-vs-unrealized PnL, window-dependent share, wallet ≠ user, proxy revenue, and
  reconstruction timeouts in the delivery. Never fabricate results or row counts.
