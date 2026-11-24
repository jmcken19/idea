# Agent architecture

The main session does almost everything. In brainstorming (Mode A) and most discovery scans **no agents run at all**. The four specialists exist for deep validations (Mode B) the founder asks for, and run only when their work materially improves the answer. No swarms.

## Roles

| Role | Where it runs | Model | When it is activated | Writes |
|---|---|---|---|---|
| **Research Lead** | The main session | `claude-opus-5-5` (set in `.claude/settings.json`) | Always. A brainstorming partner in Mode A. In Mode B it runs Stages 1, 2 and 7 inline, and explains the opportunity, not just the score | `initial-hypothesis.md`, `existing-solutions.md`, `final-verdict.md`, `scorecard.md` |
| **Market Researcher** | `.claude/agents/market-researcher.md` | `claude-sonnet-5-5` | Stage 2 needs more than about 15 searches, or Stage 3 needs a full matrix | `existing-solutions.md` (additions), `competitor-analysis.md`, `research/competitor-database/` |
| **Technical Researcher** | `.claude/agents/technical-researcher.md` | `claude-sonnet-5-5` | Only after Gate 4, and only if feasibility could change the verdict (custody, closed programs, admin keys) | `technical-feasibility.md`, `research/crypto-infrastructure/` |
| **Commercial Analyst** | `.claude/agents/commercial-analyst.md` | `claude-sonnet-5-5` | Stages 4–5, after Gate 3 passes | `market-research.md`, `commercial-analysis.md` |
| **Adversarial Reviewer** | `.claude/agents/adversarial-reviewer.md` | `claude-sonnet-5-5` | Stage 6 always, before any CONDITIONAL/VALIDATED. Optional *inverse check* only when a rejection rests on thin evidence | `adversarial-review.md` |

| **Extractor** | `.claude/agents/extractor.md` | `claude-haiku-5-5` | Optional, for mechanical work: extracting fields from cached responses, classifying sources or demand kinds, deduplicating lists, formatting packet tables. No web access, no judgement | The table or file it is asked for |

Every subagent's model is pinned by full ID in its frontmatter (no inheritance). Opus is kept for the main session's brainstorming, the evidence packet and the final synthesis, where reasoning quality matters most. Research and review run on Sonnet, and mechanical work on Haiku.

**Shared evidence instead of re-reading.** In Mode B the lead reads the material once and writes `validations/<slug>/evidence-packet.md` (≤12,000 chars, checked by `ir.py packet-check`): compact claims with tags, sources, what's already been searched, open questions, and one assignment per agent. Agents start from the packet, read only the extra files their assignment names, and reach their own conclusions. The packet carries no conclusions. The adversarial reviewer gets the packet plus the specialists' outputs, never the pitch or the lead's view, so it stays independent and challenges conclusions instead of redoing the research.

The main session acts as Research Lead and does not need a separate agent file. Its rules are in `CLAUDE.md`.

## Execution order (staged, not parallel)

```
Lead: Stage 1 ─▶ Lead: Stage 2 kill-check ──REJECT──▶ Reviewer: inverse check ─▶ Lead: verdict
                      │ pass
                      ▼
             (Market Researcher if wide) Stage 3
                      ▼
             Commercial Analyst: Stages 4–5   (Technical Researcher only if it can change the verdict)
                      ▼
             Adversarial Reviewer: Stage 6  (fresh context, claims + sources only)
                      ▼
             Lead: Stage 7 decision
```

Parallel runs are allowed only for two specialists whose inputs are independent and complete, e.g. Technical Researcher and Commercial Analyst after Gate 3. Never more than two at once.

## Why this shape

- **Kill-first is cheap inline.** Most ideas should die in Stage 2, which needs a dozen targeted searches, not five agents. Running it in the lead's own context avoids the cost of a subagent re-deriving context.
- **Specialists start cold.** Each subagent re-reads its inputs, so it is used only when the volume of work beats that overhead.
- **Independence where it matters.** The Adversarial Reviewer is the one role that *must* be separate (Lesson L8). It gets claims and sources, not the narrative, so it can't be steered by the pitch.
- **Shared artifacts, not chat.** Agents read and write the idea folder and `research/`, and log every query in `research/search-log.md`, so nobody repeats a search.

## Handoff contract

Every subagent prompt includes: the idea slug, the stage, the files to read, the budget (searches/fetches), the stop condition, and the instruction to log queries and tag every claim. Every subagent returns: what it wrote, its budget used, its top three (−) findings, and what it could not verify.

## Available skills

- `/intake`, `/kill-check`, `/validate`, `/adversarial-review` (in `.claude/skills/`): the stage procedures.
- `solana-analytics` (MIT, copied from the Salary repo): Dune SQL, holder analysis, forensics, protocol KPIs. On-chain demand evidence. Needs `DUNE_API_KEY` and network access to `api.dune.com`.
- Build skills from the Salary repo (pumpfun, helius, squads, solana-dev) were **not** installed. They are for building, which this repository does not do (Rule R5). Their reference files can still be read at `jmcken19/salary/.claude/skills/` for protocol facts.
