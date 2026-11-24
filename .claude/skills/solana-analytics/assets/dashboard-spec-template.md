# Dashboard Spec — <Dashboard Title>

Fill this in *before* writing any SQL. The spec is the argument; the queries are the evidence.
See `references/08-dashboard-build.md` for the build playbook and archetypes.

## 1. Decision
- **Reader:** <who looks at this — trader / investor / protocol team / foundation reviewer>
- **Decision it drives:** <what they will do differently after reading>
- **One-line thesis:** <the claim the dashboard is built to prove or test>

## 2. Archetype
- [ ] Market-Structure (who's winning a sector)
- [ ] Signal (is it time to act)
- [ ] Token Health (is this token sound)
- [ ] Protocol War (A vs B)

## 3. Entity & grain
- **Entity:** <project / token_mint / program_id> = `<value>`
- **Grain:** <hour / day / week / month>
- **Window:** last `<N>` days
- **Comparison set (if any):** <peers / the other protocol>

## 4. KPI family (a level + a rate + a ratio + a behavioral cut — not five levels)
| # | KPI | Template | Entity/param | Chart |
| - | --- | -------- | ------------ | ----- |
| 1 | <level — e.g. volume> | 4 | project=… | line |
| 2 | <rate — e.g. new wallets/day> | 2 | … | bars |
| 3 | <ratio — e.g. market share> | 11 | … | stacked area |
| 4 | <behavioral — e.g. retention> | 13 | … | heatmap |
| 5 | <risk — e.g. concentration> | 12 | token_mint=… | bar |
| 6 | <real-volume sanity — wash filter> | 17 | … | table |

## 5. Layout (top → bottom)
1. Title + thesis (text)
2. Exec-summary counters (the 3–4 headline numbers)
3. Trend (the level over time)
4. Behavior (new vs returning / retention)
5. Concentration / risk
6. Competitive (share vs peers)
7. Verdict (text — the decision + re-check cadence)

## 6. Data sources
- Tables: <dex_solana.trades, tokens_solana.transfers, prices.usd, …>
- Validation reference (sanity-check totals): <DefiLlama / protocol API / known figure>

## 7. Narrative findings (one line per section, filled after validation)
- Trend: …
- Behavior: …
- Risk: …
- Competitive: …

## 8. Recommendation & cadence
- **Decision:** <the explicit call this dashboard supports>
- **Re-check:** <daily / weekly> · **Owner:** <who maintains it>

## 9. Honesty appendix
- Wash-filtered vs gross volume: …
- Organic vs incentivized split: …
- Proxy definitions (revenue, CAC/LTV): …
- Live query URLs: …
