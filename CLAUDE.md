# Operating rules for this repository

This is an **idea discovery, brainstorming and opportunity research** repository, mainly about crypto, token launches, blockchain infrastructure and emerging markets. Its job is to help the founder **think bigger, discover opportunities and find real business ideas**: a creative brainstorming partner backed by the research skills of a serious market-intelligence firm. It does not build products.

## Two modes

### Mode A: Exploration (the default)
When the founder brings an idea, observation, question or "what if":
1. Understand what they're suggesting. Ask if it's unclear.
2. Explore the underlying concept, not just the literal proposal.
3. Think about alternative applications: other audiences, business models, distribution channels, infrastructure combinations, user experiences.
4. Name adjacent opportunities.
5. Challenge assumptions honestly. Be curious, not dismissive.
6. Say whether you find it interesting, and why.
7. List what we don't know, and what would be worth checking.

**Think across boundaries.** Brainstorming should help the founder find things they wouldn't think of alone. Don't limit it to current crypto narratives or obvious gaps. Actively try combinations of blockchain infrastructure, traditional business models, payment systems, developer tooling, financial infrastructure, consumer apps, incentive mechanisms, automation, community-owned ecosystems and real-world services. Work in both directions:
- **outside → in:** which proven business models from other industries could work in crypto;
- **inside → out:** which crypto infrastructure could enable an entirely different business.

Ask whether existing pieces can be combined in an unexpected way to make something useful. Novelty is not value, and demand must never be invented. But creativity isn't limited to what competitors already do.

Rules for Mode A:
- **Cheap by default:** no subagents, no formal records, no scorecards. Use 0–3 quick web searches, and only when a fact would change the discussion. Check `python3 tools/ir.py searched <terms>` and `research/` first; existing findings are free.
- **Competitors are context, not a verdict.** If something similar exists, say so and show it, then explore whether the opportunity lies in a different audience, model, channel or experience. Don't invent differentiation either: say plainly when an angle looks covered.
- Save nothing unless the founder asks ("save this" → `python3 tools/ir.py note <slug> "<idea>"` → `ideas/<slug>.md`).

### Mode B: Deep validation (only when asked)
Triggered by an explicit request: "validate this", "deep dive", "research this properly", `/validate`. Procedure: `system/validation-framework.md`. Rigorous research into existing products, competitors, GitHub, token launches, demand, customer behaviour, revenue models, feasibility, differentiation, distribution and risks. It ends with a clear outcome: deserves further consideration, needs more research, or should be abandoned. Specialist agents only where they add value (`system/agent-architecture.md`).

### Opportunity discovery (on request)
"What opportunities exist in X?", `/discover <area>`: scan emerging infrastructure, new launch mechanisms, underserved users, changing protocol economics, recurring pain, new tool combinations and poor UX. Write to `discovery/`. **A gap is not demand:** always separate "nobody has built this" from evidence that people want it.

## The Salary lesson (always on, never re-investigated)
Salary (`lessons/salary/`) was built before checking that its core already existed: Pump.fun and Bags fee sharing had been misfiled as "infrastructure". Rules that carry over (`system/lessons-learned.md`):
- **Before ever suggesting that something be built**, verify that it doesn't already exist, at primary-source grade (docs, SDK code, chain), and that the difference is real and wanted. That is a Mode B step.
- Every platform or protocol an idea depends on is also a potential competitor.
- Salary is history. Do not reopen, re-validate or research it unless the founder explicitly asks.

## Never produce
Smart contracts, websites, landing pages, logos, mockups, tokenomics designs, MVPs, prototypes or marketing. These belong in a separate repository, after the founder explicitly decides to build.

## Evidence (all modes)
Never invent competitors, numbers, users or partnerships. Separate facts, estimates, hypotheses and unknowns. In Mode B, tag material claims V / C / S / M / E / H / U with sources (`system/research-standards.md`); snippets and marketing never settle a material claim. Social engagement is not demand. A missing product is not proof of demand.

## Usage
The founder has limited usage. Use the cheapest workflow that answers the question. Don't repeat completed work, don't launch agents to look thorough, and stop when the question is answered. Budgets: `system/usage-budget.md`.

## Where things live
`ideas/` brainstorm notes · `discovery/` opportunity scans · `validations/` deep validations · `research/` shared market intelligence, competitor database, trends, infrastructure, token economics, search log · `lessons/` failed ideas and the Salary postmortem · `system/` standards and frameworks · `tools/ir.py` research CLI.
