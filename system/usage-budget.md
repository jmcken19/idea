# Usage budget and stop conditions

Spend scales with how serious the question is. The founder's usage is limited.

| Mode | Default spend |
|---|---|
| **Mode A: brainstorm** | Main session only, no subagents; **0 searches and 0 API calls by default** (1–3 only when a fact materially changes the discussion, or on request; the hook hard-caps it at 3 per session and blocks all agents); no files unless asked |
| **Discovery scan** (explicit request only) | 12 research calls in total (searches + fetches), at most 1 agent, and only if the founder asks for a broad scan. Hard-capped once `budget start … discover` is run |
| **Mode B: deep validation** | The stage budgets below; specialist agents only where they add value; at most 2 at once |
| **Historical records (`lessons/`)** | Zero. Never re-researched unless the founder asks |

## Mode B budget (one unit = one search or one fetch)

| Stage / role | Model | Research calls | Agent runs | Stop when |
|---|---|---|---|---|
| 1 Intake (lead) | Opus | 0 | 0 | n/a |
| 2 Existence check (lead, inline) | Opus | 12 | 0 | An equivalent is verified (V/C) *and* no evidenced alternative angle remains, or the allowance runs out |
| Evidence packet (lead, once) | Opus | 0 (reuses everything) | 0 | n/a |
| 3 Competitors (market-researcher) | Sonnet | 10 | 1 | Matrix complete, or allowance out |
| 4–5 Demand and money (commercial-analyst) | Sonnet | 10 | 1 | Level of demand established, or allowance out → NEEDS MORE RESEARCH |
| Feasibility (technical-researcher, only if it could change the outcome) | Sonnet | 5 | 0–1 | n/a |
| Mechanical extraction (extractor, optional) | Haiku | 0 (reads cache only) | 0–1 | n/a |
| 6 Independent review (adversarial-reviewer) | Sonnet | 8 (inverse check: 4) | 1 | n/a |
| 7 Decision (lead) | Opus | 0 | 0 | n/a |
| **Workflow cap (`budget start … validate`)** | | **45** | **5** | Hook blocks the next call |

Discovery scan cap (`budget start … discover`): **12 research calls, 1 agent.** Brainstorming, with no workflow started: **3 research calls per session, 0 agents.**

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

## Enforcement: what is hard, what is instruction

Audit 2 found one agent about 33% over its allowance, because budgets were instructions only. Now:

| Limit | How | Hard or prompt-level |
|---|---|---|
| Research calls per workflow / per brainstorm session | `tools/budget_hook.py` (PreToolUse hook in `.claude/settings.json`) counts WebSearch, WebFetch, web-fetch agents and `ir.py fetch / npm-grep / rpc / check-sources`, and **blocks** the call once the cap is reached | **Hard**, for calls made through those tools. Raw `curl` or `gh api` would bypass it |
| Agents per workflow (0 while brainstorming) | Same hook counts Agent/Task launches and SendMessage resumes during a workflow, and blocks beyond the cap | **Hard** |
| Context handed to an agent | Hook blocks any agent prompt over 16,000 chars; `ir.py packet-check` fails a packet over 12,000 chars | **Hard** for the prompt and packet; what an agent reads afterwards is prompt-level |
| Per-agent allowance within the workflow cap | Stated in each assignment and agent definition | Prompt-level (the workflow total is hard) |
| Research iterations | Every agent launch or resume counts against the agent cap, so re-running an agent costs budget; extra rounds need `budget extend` | Hard via the agent cap |
| No automatic retries | Failed calls are counted, so a retry consumes budget; agents are told never to retry | Hard (counted) + prompt |
| Raising a cap | `ir.py budget extend <kind> <n> --reason "..."` only; logged in the ledger and search log, and reported to the founder | Logged; it's an instruction that only the founder approves |
| Starting a workflow | `ir.py budget start` only after the founder explicitly asks for a validation or scan | Prompt-level (logged with the founder's request as the reason) |

If the ledger can't be read, the hook allows the call and prints a warning (fail-open), so a bug never blocks a session. The hook was tested locally by piping tool-call JSON through it. Its firing inside subagents follows Claude Code's hook behaviour and has not been observed live in this repo yet.

**When a budget is exhausted:** stop, summarize the evidence collected, list the unanswered questions, and return. Never exceed a budget silently.
