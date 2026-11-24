# Crypto Idea Lab

A place to bring random ideas, observations, questions and possible opportunities (crypto, token launches, blockchain infrastructure, emerging markets) and turn the interesting ones into researched opportunities. A brainstorming partner with market-intelligence research behind it. It does not build products.

## How to use it

| You say | What happens | Cost |
|---|---|---|
| "What if we created something around creator fees?" / "Why doesn't X exist?" | **Mode A: brainstorm.** Explore the concept, alternative audiences, models and channels, adjacent opportunities, assumptions and unknowns. Uses existing research; at most a few quick searches | Low |
| "Save this idea" | One short note in `ideas/<slug>.md` | Minimal |
| "What opportunities exist in the Solana ecosystem?" / `/discover <area>` | **Discovery scan**: emerging infrastructure, underserved users, new combinations. Separates "unbuilt" from "wanted" | Medium |
| "Validate this" / "Deep dive" / `/validate <idea>` | **Mode B: deep validation.** Competitors, GitHub, token launches, demand, revenue models, feasibility, distribution, risks, with sourced evidence and an independent challenge. Outcome: pursue further / needs more research / abandon | Higher |

## Layout

| Path | What |
|---|---|
| `CLAUDE.md` | How Claude behaves here (modes, evidence, usage) |
| `ideas/` | Brainstorm notes (Mode A) |
| `discovery/` | Opportunity scans |
| `validations/` | Deep validation records (Mode B), from `templates/validation/` |
| `research/` | Shared intelligence: `market-landscape/`, `competitor-database/`, `industry-trends/`, `crypto-infrastructure/`, `token-economics/`, `INDEX.md`, `search-log.md` (sources and deduplication) |
| `lessons/` | Failed ideas and lessons, including the Salary postmortem (historical, not active) |
| `system/` | Research standards, validation framework, scoring, agents, usage budget, tooling, lessons-learned rules |
| `tools/ir.py` | CLI: `searched`, `log`, `fetch` (cached data APIs), `npm-grep`, `rpc`, `note`, `new`, `score`, `lint`, `spend`, `check-sources` |
| `.claude/` | Skills (`brainstorm`, `discover`, `validate`, `intake`, `kill-check`, `adversarial-review`, `solana-analytics`) and four specialist agents used in Mode B |

## Setup still needed
Most crypto data APIs and web pages are blocked by the cloud environment's network policy. The host list to allow is in `system/tooling.md` §3; the current status is in §5.
