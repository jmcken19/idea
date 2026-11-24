# Stage 2: Existence check (kill-first)

Question: **who already solves this, and why should this exist anyway?**

Pivot of `validations/ai-meme-pair-coin`; the pair-coin findings (S10) are reused, not repeated.

## Search coverage

| Channel | Done? | Queries / where | Hits |
|---|---|---|---|
| Native platform features | Yes | Clawnch/Clanker, Moltbook submolts (S1, S4) | agent-created communities and agent-launched tokens both exist |
| Web search, 3+ phrasings | Yes | 8 searches (Moltbook; security; agent forum with tokens; status; Clawnch; alternatives; Solana angle; Reddit points) | see equivalents |
| GitHub repositories | Yes (thin) | 1 query: agent social network forum upvote, created after 2026-08-25 | 0 repos; coverage is thin |
| npm / crates / PyPI | No | n/a | n/a |
| Protocol docs and directories | Partly | Base docs for Clawnch seen as snippet only | gap |
| Token launches with the same pitch | Yes | DexScreener + Jupiter "moltbook" (S7, S8) | MOLT on Base; many copycat tokens |
| Bots, Telegram tools, APIs | Partly | Clawnch API (S4) | exists |
| Other chains | Yes | Base (Moltbook, Clawnch); Solana search found none | Base is where this lives |
| Web2 or adjacent industries | Yes | Reddit Community Points (S9) | direct precedent, shut down |
| Recent launches (last 90 days) | Yes (thin) | GitHub created:>2026-08-25 query (0 repos); MoltX (Feb 2026) and Clawnch seen in web search | nothing new found; coverage is thin |
| Discontinued / abandoned projects | Yes | Reddit Community Points ended 2023 (S9) | Yes |

## Equivalents found

| Product | What overlaps | Evidence | Overlap |
|---|---|---|---|
| **Moltbook** | Reddit-style forum for AI agents, submolts (agent-made communities), profiles, upvotes, humans watch only | S1 [S, multi-outlet] | **Full** for the forum |
| **MoltX**, **Chirper** | Other agent-only social networks with reputation | S5, S6 [S] | Full/partial for the forum |
| **MOLT token** (Base) | A token tied to the agent forum | S2, S7 [S/M] | Partial: link to the platform not clearly established |
| **Clawnch** (+ Clanker, Base) | Agents launch tokens, earn fees; integrates Moltx, Moltbook, 4claw | S4 [S] | **Full** for "agents launch tokens from an agent social network" |
| **Reddit Community Points** | One token per community, ERC-20 (Moons, Bricks, Donuts) | S9 [S, multi-outlet] | Full for "token per forum"; discontinued |

Not found: a product where agents reach **consensus to create a new forum** and the forum then gets **its own token paired with a base coin**; nothing on Solana. A gap is not demand.

## Easy replicators

| Who | Why | Evidence |
|---|---|---|
| Moltbook / Moltx | Already have agent-created communities; Clawnch integration already links them to token launches | S1, S4 |
| Clawnch / Clanker | Already deploy tokens for agents on request | S4 |

## Gate 2 decision

- [x] An equivalent exists (forum: Moltbook, MoltX, Chirper; agent-launched tokens: Clawnch; token per community: Reddit Community Points).
- [ ] No equivalent found.

### Differentiation test

1. **What would a customer get that existing options do not?** Agent consensus creating the forum, a token per forum, and pairing with Singularity. This is the real, stated difference. Its value is unexplained.
2. **Evidence customers want it?** **None found.** Adverse signals: the category leader's token trades about $1.3K a day on about $98K liquidity (S7 [M]); the leader's agent population was largely human-driven or fake (S3 [S]); the one precedent for per-community tokens was shut down after "no path to scale" with holders down 60-85% (S9 [S]); Singularity is 4 days old and falling (S10).
3. **Could the incumbent ship it in a release?** Largely yes. Moltbook already has agent-made communities and Clawnch already links agents to launches (S1, S4).
4. **Would you pitch it if the incumbent did not exist?** Not answerable; the pitch is the mechanic, with no stated user need.

**Outcome: REJECTED for the framing as submitted** (question 2 has no evidence). The record is reopenable if the gist or new evidence supplies demand for the difference.

### Angles the equivalents do not cover (untested; no evidence; brainstorm threads only)
- Agent-consensus as a *curation* filter, so only topics agents agree on get a token. Unbuilt as far as found, but gaming risk is high.
- Pure meme-discovery without a token per forum (forum as a funnel, one token for the whole site).
- A Solana version. Not found, but Solana's agent-forum audience is unestablished.
