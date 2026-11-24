# Crypto Idea Intelligence & Validation

An independent research system that takes business ideas (crypto, Solana, DeFi, token launches) from **0 → researched → challenged → validated or rejected**. It builds no products.

**The success metric is how many bad opportunities are rejected before resources are spent on them.**

## How an idea is evaluated

```
/intake  →  /kill-check  →  /validate  →  /adversarial-review  →  verdict
Stage 1     Stage 2         Stages 3–5     Stage 6 (separate       Stage 7
            "who already                   agent, claims +
            solves this?"                  sources only)
```

Verdicts: **REJECTED** · **NEEDS MORE RESEARCH** · **CONDITIONAL OPPORTUNITY** · **VALIDATED OPPORTUNITY**. Most ideas should die at Stage 2, for about 16 searches.

To submit an idea, tell Claude in this repo: *"New idea: …"*. It runs `/intake` and `/kill-check`, and reports back bluntly.

## Layout

| Path | What |
|---|---|
| `CLAUDE.md` | Operating rules loaded by every session (Research Lead role, kill-first, no build output) |
| `system/` | `research-standards.md` (evidence tags, anti-hallucination), `validation-framework.md` (stages and gates), `scoring-framework.md`, `agent-architecture.md`, `usage-budget.md`, `tooling.md` (what is installed and what needs keys), `lessons-learned.md` (the Salary rules) |
| `ideas/` | One folder per idea; `INDEX.md` registry |
| `templates/idea/` | The record every idea starts from |
| `research/` | Reusable findings: `INDEX.md`, `competitor-database/`, `market-landscape/`, `crypto-infrastructure/`, `token-economics/`, `industry-trends/`, `failed-ideas/`, plus `search-log.md` (deduplication) |
| `tools/ir.py` | CLI: `new`, `searched`, `log`, `fetch` (cached data APIs), `score`, `lint` |
| `.claude/agents/` | market-researcher, technical-researcher, commercial-analyst (sonnet); adversarial-reviewer (opus) |
| `.claude/skills/` | intake, kill-check, validate, adversarial-review, solana-analytics |

## Quick commands

```bash
python3 tools/ir.py searched fee split          # what do we already know?
python3 tools/ir.py fetch github-repos "creator fee distributor"
python3 tools/ir.py fetch defillama-fees pump.fun   # needs the host allowlisted (system/tooling.md)
python3 tools/ir.py score salary
python3 tools/ir.py lint
```

## Records so far

- [`ideas/salary`](ideas/salary/): the historical test. **REJECTED** at Gate 2. See [`postmortem.md`](ideas/salary/postmortem.md).
- [`ideas/salary-team-record`](ideas/salary-team-record/): Salary's pivot. **REJECTED** at Gate 2.

## Setup still needed
See `system/tooling.md` § 3: allow the free crypto data API hosts in the cloud environment (one-time, free); optional free CoinGecko and Helius keys; Dune only if a later idea needs paid on-chain studies.
