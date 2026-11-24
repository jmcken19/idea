# Usage budget and stop conditions

Spend scales with how serious the question is. The founder's usage is limited.

| Mode | Default spend |
|---|---|
| **Mode A: brainstorm** | Main session only, no subagents; **0 searches and 0 API calls by default** (1–3 only when a fact materially changes the discussion, or on request); no files unless asked |
| **Discovery scan** (explicit request only) | Up to 10 WebSearch + cheap primary checks; one market-researcher agent only if the founder asks for a broad scan |
| **Mode B: deep validation** | The stage budgets below; specialist agents only where they add value; at most 2 at once |
| **Historical records (`lessons/`)** | Zero. Never re-researched unless the founder asks |

## Mode B budgets

## Budget per stage (defaults; the lead can lower them, and raising one needs a written reason in the README)

| Stage | Web searches | Page fetches | API fetches (`ir.py fetch`) | Subagent runs | Stop early when |
|---|---|---|---|---|---|
| 1 Intake | 0 | 0 | 0 | 0 | n/a |
| 2 Existence | 12 (standard mode; ≤ 3 extended) | 5 | 10 | 0 (1 if coverage is wide) | An equivalent is verified (V/C) **and** the differentiation test fails |
| Inverse check after a reject | 4 | 2 | 2 | 1 (reviewer, short) | It finds no evidence the rejection is wrong |
| 3 Competitors | 10 | 8 | 10 | ≤ 1 | The matrix shows saturation |
| 4 Demand | 10 | 6 | 15 | ≤ 1 | Only level-1/2 evidence after budget → NEEDS MORE RESEARCH |
| 5 Financials | 6 | 4 | 10 | (same run as 4) | No credible payer |
| 6 Adversarial | 10 | 6 | 10 | 1 (required) | n/a |
| 7 Decision | 0 | 0 | 0 | 0 | n/a |
| **Full pipeline cap** | **~50** | **~30** | **~60** | **≤ 4** | |

A Gate-2 rejection should cost about 16 searches and one short reviewer run.

## Rules that save usage

1. **Check before searching:** `python3 tools/ir.py searched <terms>`. Reuse anything within its freshness window.
2. **Log everything:** `ir.py fetch` logs itself. Log WebSearch and web-fetch calls with `ir.py log`. The log is the deduplication layer across sessions and agents.
3. **Standard search first.** Use extended mode only when a standard result is thin, stale or off-target, or for niche facts.
4. **APIs before pages.** A JSON endpoint through `ir.py fetch` is cached, costs no model tokens to fetch again, and is more reliable than a scraped page.
5. **No MCP servers by default.** Every MCP server loads its tool schemas into every session's context. Free REST data goes through `ir.py fetch` instead. Dune and Helius MCP are optional and turned on only for on-chain stages (see `system/tooling.md`).
6. **Subagents only when the volume of work justifies the cold start.** Never more than two at once.
7. **Read summaries first.** Read `research/INDEX.md` and the idea's `final-verdict.md` and `README.md` before opening long files.
8. **One-line handoffs.** Subagents return a short report. Details stay in files.

## Freshness windows (after which a finding is stale and must be re-checked)

| Kind of finding | Re-check after |
|---|---|
| Prices, TVL, fees, volume, market share | 30 days |
| Whether a competitor or feature exists | 90 days |
| Protocol mechanics (program rules, SDK behaviour) | 90 days, or on a new SDK major version |
| Funding, team, partnerships | 180 days |
| Regulation and lawsuits | 90 days |
| Historical facts (launch dates, past events) | Never stale |

Cached API data (`research/.cache/`) defaults to a 7-day reuse window (`--max-age` to change).

## Enforcement (audit 2 finding, 2026-11-24)

The budgets were advisory. In audit 2, one researcher agent overran its tool-call budget by about 33% (about 40 calls against 30), and `spend` didn't notice. Tool fetches were logged without an idea slug, so only WebSearch was counted. Fixed:
- every `ir.py` call made with `IR_IDEA=<slug>` is attributed to that idea;
- each agent definition requires `IR_IDEA` and a `spend` check before finishing;
- the Research Lead runs `python3 tools/ir.py spend <slug>` after each agent run and records the spend in the idea README.

Budgets remain soft limits, because a model can't be hard-stopped mid-run by this tool. An overrun is recorded in the idea README with a reason.
