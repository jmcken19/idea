# The Analyst-Shaped Hole
### A Mid-2026 Landscape of Solana On-Chain Analytics Tooling for AI Agents

*Research report · Sovereign Night palette · Hausa-leads register*
*Author: Muhammad Auwal Abdul Aziz (@Ghostieemoh), on-chain & data analyst*
*Period covered: January-June 2026*

> **[FIGURE. HERO / Data-led title card]**
> **Scene:** A dark control-room wall of Solana dashboards, volume curves, holder treemaps, a retention triangle, all glowing, but one panel in the center is blank, outlined in a thin gold frame, captioned "ANALYST". The blank panel is the subject of the report.
> **V7 prompt:** wide cinematic shot of a darkened analytics war-room, six wall-mounted screens showing purple-and-gold on-chain charts, one central screen dark and empty with a thin gold border, volumetric haze, deep navy and obsidian color grade with violet rim light, 35mm, no people, premium editorial, title text baked top-left "THE ANALYST-SHAPED HOLE" --ar 16:9 --s 300 --no watermark, extra text, deformed shapes
> **Palette:** Sovereign Night (obsidian, deep navy, violet, gold accent).

---

## 00 · Executive Summary

The Solana developer-agent stack matured fast in the first half of 2026. An agent can scaffold an
Anchor program, route a swap, index a webhook, and run a security pass, each backed by a dedicated,
well-formed skill. One capability is missing from all of it: the agent cannot **reason about the data
the chain produces.**

This report maps the on-chain analytics tooling available to AI coding agents on Solana as of
mid-2026 and reaches five findings.

1. **The analyst layer is empty.** Across foundation, DeFi, infrastructure, security, and GTM skill
   collections, no skill teaches an agent to write Solana-native analytics SQL, decode program logs
   into tables, or compute protocol KPIs. The work that data analysts do all day has no agent
   equivalent.
2. **Adjacent tools are mistaken for analytics.** Price APIs return a number, not a method.
   Execution kits act, they don't measure. Indexers move data, they don't interrogate it. Each is
   excellent at its job and none of them is analysis.
3. **The hard part is schema knowledge, not SQL.** Generic data-science skills know SQL. They do not
   know `dex_solana.trades`, Anchor discriminators, token decimals, or that a DEX trade logs two
   legs. That gap is where wrong answers are born.
4. **Forensics is the highest-value, least-served corner.** "Is this real?" (wash trading, rug risk,
   sybil farms, MEV) is the question builders and investors ask most, and the one no skill answers.
5. **The gap is closable today.** The data exists on Dune, Flipside, and Helius. What was missing was
   a skill that encodes the schema, the metric, and the validation path. This report documents one,
   and argues the category deserves a permanent seat in the standard kit.

---

## 01 · Context

In mid-2026 Superteam Brazil shipped the Solana AI Kit, a configuration that turns a coding agent
into a Solana builder by routing across the ecosystem's best skills. To grow the kit, they opened a
public bounty for new, cross-domain skills, and seeded three gaps they had spotted themselves: a
legal/compliance skill, a CLMM position manager, and an auditor. They were explicit that these were
prompts, not limits: the best submission might be something nobody had named.

This report exists to answer one question that the bounty surfaced: **of all the things a Solana
builder does, which one has no agent skill at all?** It is written for three readers, the founder
who needs numbers for a grant, the engineer who wants to stop hand-writing the same Dune query, and
the judge weighing what belongs in the kit.

The period under study is January to June 2026. The method is a census of public skill repositories
named in the bounty and their wider ecosystem, cross-referenced against the actual data questions
builders raise in Discord, grant applications, and due-diligence threads. Methodology sits in the
appendix. The short version: I read what every skill claims, then I checked what it could not do.

---

## 02 · The Stack That Can Build But Cannot Count

Walk the kit and the picture is one of genuine depth. Foundation skills cover Anchor and native Rust
[1][2]. DeFi is dense: SendAI's agent kit exposes sixty-plus on-chain actions [3], Jupiter ships a
skill spanning swap, lend, perps, and price data [4]. Infrastructure is covered by Helius for RPC and
DAS [5], with Light Protocol, Alchemy, and others around it. Security is unusually strong. Trail of
Bits maintains thirty-plus auditing skills [6], and formal-verification work runs as far as Lean
proofs [7]. Go-to-market has Colosseum's copilot over thousands of hackathon projects [8] and
SendAI's journey skills [9].

> **[FIGURE 1. Coverage map / horizontal bar]**
> **Spec:** Five rows. Build, Execute, Index, Secure, Go-to-Market, each a full violet bar. A sixth
> row, "Analyze," is an empty gold outline at 0%. Caption baked under. Sovereign Night grade.

Every one of those skills answers a *production* question: how do I build this, ship this, secure
this. None answers an *interpretation* question. The chain emits a firehose of accounts, instructions,
transfers, and logs every slot. Turning that exhaust into "is this protocol growing, and is the
growth real" is a separate craft, and the stack does not practice it.

That is the analyst-shaped hole. It is not a small one.

---

## 03 · Four Tools, Four Misses

The reflex objection is that analytics is already covered. It is not. Four categories of tool get
mistaken for the analyst layer, and each misses in a specific way.

**Price and market-data APIs.** Birdeye, CoinGecko, and GMGN return the last price, a chart, or a
trending list [10][11][12]. They are fast and good. They are also point estimates: they hand you a
number without the schema beneath it, the metric family around it, or the method to defend it. A
founder who needs "retained users by cohort, organic only" gets nothing from a price endpoint.

**Execution kits.** SendAI's agent kit and similar tools *do* things: swap, stake, transfer [3].
Doing is the inverse of measuring. An action library has no opinion about whether the action worked
at the level of a protocol's whole user base.

**Indexers.** Indexing skills, including a strong one submitted to this very bounty, ingest events
into your own database with reorg-safe finality [13]. That is the plumbing analytics sits on top of.
It tells you how to *store* the data, never which question to ask of it.

**Generic SQL and data-science skills.** Dune and Flipside skills teach SQL; pandas skills teach
dataframes [14][15]. They are chain-blind. They do not know that `dex_solana.trades` already carries
`amount_usd`, that `amount` in a transfer table is raw base units needing a decimals divisor, that a
swap logs both legs and double-counts if you are careless. Chain-blind SQL produces confident,
wrong charts.

> **[FIGURE 2. Four-quadrant miss diagram]**
> **Spec:** 2×2 grid. Price APIs (returns a number), Execution (acts), Indexers (ingests), Generic
> SQL (no chain context). Center node "Analysis" connecting to none. Gold center, violet edges.

Four capable categories. A hole precisely in the middle.

---

## 04 · What "Solana-Native Analytics" Actually Requires

The reason the gap persisted is that closing it properly demands four kinds of knowledge that live
nowhere together.

**Schema fluency.** Knowing that activity lives in `solana.transactions`, swaps in
`dex_solana.trades`, transfers in `tokens_solana.transfers`, and prices in `prices.usd`, and which
one answers which question. The wrong table is the most common analytical error, and it happens
before a single line of SQL.

**Decoding.** Solana instructions are Borsh-encoded bytes; an Anchor program tags each with an
eight-byte discriminator derived as `sha256("global:<name>")[.8]` [16]. Events ride inside
`Program data:` log lines as base64 payloads. Most "there is no data for this protocol" walls are
really "nobody decoded this program yet" walls, and they fall the moment an analyst submits the IDL
to a decoder or matches the discriminator on raw tables.

**Metric families.** A level alone, "$40M volume", is unfalsifiable. A level paired with a rate, a
ratio, and a behavioral cut is an analysis. KPI literacy means knowing that revenue is the kept
share, not gross fees; that market share is window-dependent; that wallet is not user.

**Forensics.** The defensive read, wash trading, rug risk, sybil clusters, MEV extraction, fund
tracing, done as probabilistic risk scores with confidence levels, never as accusations.

> **[FIGURE 3. The four-layer requirement stack]**
> **Spec:** Vertical stack, bottom to top. Schema, Decoding, Metric Families, Forensics, each a
> band, narrowing upward toward a gold cap labeled "Decision." Sovereign Night.

No price API has all four. No SQL skill has any. That is the bar a real analytics skill must clear.

---

## 05 · The Bounty as a Natural Experiment

The skill-bounty repository is, conveniently, a live readout of what the ecosystem thinks is missing.
By mid-2026 it held over a hundred pull requests [17]. Reading them is instructive.

The submissions cluster where the ecosystem is already strong and competition is fierce: indexers,
stablecoin tooling, DePIN, RWA, secops, more auditing. Several are genuinely good. A rugcheck
submission touches one corner of forensics; an indexer submission touches the pipeline beneath
analytics; an RWA submission touches holder distribution [13][18]. Each grazes the analyst layer at
its edge.

None occupies the center. Not one submission, at the time of this study, teaches an agent the full
arc, schema to decoding to KPI to forensics to a validated, runnable query. The crowd confirmed the
map: everyone built near the existing strength, and the analyst-shaped hole stayed open.

> **[FIGURE 4. Submission cluster scatter]**
> **Spec:** Scatter of ~100 dots grouped into labeled clusters (Indexing, Security, Stablecoins,
> DePIN, RWA, GTM). A gold ring marks the empty region labeled "On-chain analytics." Violet dots,
> gold annotation.

A gap that survives a hundred attempts is not an accident of attention. It is a gap of supply, the
knowledge to fill it is concentrated in working analysts, and working analysts had not yet shipped a
skill.

---

## 06 · Case Study: Building Into the Hole

**Background.** Over 2026 I reverse-engineered eight professional Dune dashboards, built by analysts
publishing as dune, cryptokoryo, 21shares research, and web3precious, into a private mastery system:
fifteen tested SQL templates, an operator playbook, and a dependency-free Dune client [19].

**The Moment.** The bounty reframed that private system as a public gap. The dashboards already
encoded the schema, the metric families, and the validation discipline. What they lacked was the
kit's shape, a routing `SKILL.md`, focused load-on-demand references, an executable layer, agents
and commands, and the two corners the dashboards under-served: program decoding and forensics.

**The Lesson.** The fastest credible way to fill an ecosystem gap is rarely net-new invention. It is
to take expertise that already exists in one form, here, working dashboards, and reshape it into
the interface the ecosystem can consume. The resulting skill ships twenty-two templates, an Anchor
discriminator deriver, a Dune-plus-Helius execution layer, and a forensics module, with offline
tests and a clean-SQL CI gate. The expertise was real before the skill existed. The skill made it
reusable.

---

## 07 · Outlook

The near-term trajectory is clear. As agents take on more of the build, the bottleneck moves
downstream to judgment, and judgment on Solana is data work. Grant committees will keep asking for
retention and real volume. Investors will keep asking who holds the float. Protocol teams will keep
asking whether their growth survives the end of emissions. Those questions do not have execution
answers; they have analytical ones.

The finding this report opened with, that the analyst layer is empty while everything around it is
full, will not hold for long, precisely because it is so easy to feel its absence. The first skills
to fill it well will become infrastructure the way the auditing skills already have. The category
belongs in the standard kit, not as a price-API wrapper, but as the layer that teaches an agent the
schema, the metric, and the honesty to say "no data is a finding; fake data is fraud."

The bet I would make: within a year, "analyze this protocol" is a first-class agent command, and the
skills that own it are the ones that treated decoding and forensics as core rather than garnish.

> **[FIGURE 5. Outlook timeline]**
> **Spec:** Horizontal timeline H2-2026 → H2-2027, three milestones, "analytics skills land", "grant
> reporting standardizes on-chain", "analyze-protocol becomes a default command". Gold milestone pins.

---

## 08 · Impact / Reflection

I have spent years answering the question "is this real" for tokens, protocols, and traders. The
honest truth of the craft is that the chain hands you everything and explains none of it. Every
strong analysis I have ever delivered came from refusing to trust a pretty chart until I had checked
the decimals, the both-legs double count, and the funding graph behind the wallets.

Encoding that refusal into a skill felt less like writing software and more like writing down a
discipline. The blockchain never lies. It simply does not volunteer the truth, and until now,
neither could the agents we build on top of it.

---

## References

1. Solana Foundation, solana-dev-skill. github.com/solana-foundation/solana-dev-skill
2. Superteam Brazil. Solana AI Kit. github.com/solanabr/solana-ai-kit
3. SendAI. Solana Agent Kit (60+ actions). github.com/sendaifun/solana-agent-kit
4. Jupiter, agent-skills. github.com/jup-ag/agent-skills
5. Helius, core-ai / DAS API. github.com/helius-labs/core-ai · docs.helius.dev
6. Trail of Bits, security skills. github.com/trailofbits/skills
7. QEDGen, solana-skills (formal verification). github.com/QEDGen/solana-skills
8. Colosseum, colosseum-copilot. github.com/ColosseumOrg/colosseum-copilot
9. SendAI, solana-new (journey skills). github.com/sendaifun/solana-new
10. Birdeye, token/market data API. birdeye.so
11. CoinGecko. Solana on-chain DEX data. coingecko.com
12. GMGN, gmgn-skills (smart-money tracking). github.com/GMGNAI/gmgn-skills
13. Superteam Brazil skill-bounty PR, solana-indexer-skill. github.com/solanabr/skill-bounty/pull/106
14. Dune Analytics. DuneSQL / Spellbook. docs.dune.com · github.com/duneanalytics/spellbook
15. Flipside Crypto. Solana schemas. flipsidecrypto.xyz
16. Anchor. IDL and discriminator conventions. anchor-lang.com
17. Superteam Brazil, skill-bounty (104+ PRs). github.com/solanabr/skill-bounty
18. Superteam Brazil skill-bounty PRs, solana-rugcheck-skill (#101), solana-rwa (#100). github.com/solanabr/skill-bounty/pulls
19. solana-analytics-skill, this work. (repo link on submission)
20. DefiLlama. TVL reference. defillama.com
21. Nansen. Solana on-chain data methodology. nansen.ai/solana-onchain-data
22. RugCheck. Solana rug-pull detection. rugcheck.xyz
23. Solana Foundation, awesome-solana-ai. github.com/solana-foundation/awesome-solana-ai
24. Reference skill, solana-game-skill. github.com/solanabr/solana-game-skill

---

## Appendix · Methodology

**Scope.** Public skill repositories named in the Solana AI Kit bounty listing and their immediate
ecosystem, plus the skill-bounty PR set, observed January-June 2026.

**Procedure.** For each repository, I recorded the skills it contains and the problem each solves,
then tested each against a fixed battery of analyst questions (active wallets, market share, holder
concentration, retention, wash-traded volume, decoded-instruction adoption, grant-report metrics). A
skill "covers" a question only if it teaches the schema and method, not merely returns a number.

**Limitations.** Skill repositories change daily; coverage is a mid-2026 snapshot. "Gap" is a claim
about public skills, not about the existence of standalone platforms (Dune, Nansen, Flipside all
exist as tools, none ships as an agent skill encoding its method). Forensics signals discussed are
probabilistic heuristics, not verdicts.
