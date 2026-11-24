# The Blockchain Never Lies, But Your Agent Can't Read It

*Long-form article · Standard mode · Sovereign Night palette · first-person*
*Muhammad Auwal Abdul Aziz (@Ghostieemoh) · on-chain & data analyst*

> **[FIGURE. HERO]**
> **Scene:** A lone analyst at a dark desk in Kano, three monitors of purple Solana charts, an AI
> chat window open and stalled mid-answer, a single desk lamp throwing warm light across his face.
> **V7 prompt:** cinematic portrait, young Nigerian man with warm brown skin and subsurface
> scattering, seated at a darkened desk in Kano, three monitors glowing violet with on-chain charts,
> a stalled AI chat reflected in his glasses, warm desk-lamp light from camera left, obsidian and
> navy grade with gold rim, 50mm, subject 40% of frame lower-right, title baked top "THE BLOCKCHAIN
> NEVER LIES, BUT YOUR AGENT CAN'T READ IT" --ar 16:9 --s 320 --no watermark, extra fingers,
> deformed hands, default Western features, generic AI face
> **Palette:** Sovereign Night.

---

## 1.0 · The World

In mid-2026, an AI coding agent on Solana can do almost everything. It scaffolds an Anchor program in
a minute. It wires a Jupiter swap. It stands up a Helius webhook, runs a Trail of Bits security pass,
and drafts your pitch from a thousand hackathon projects. The kit that powers this routes across the
whole ecosystem, and it is genuinely good.

Then a founder asks it a different kind of question. Not "build me this." Instead: *is my protocol
actually growing, or am I renting users with emissions?* Who really holds my token? Is the volume on
my chart real, or is one wallet trading with itself to fake a number for the next round?

The agent goes quiet. Not because the data is missing. It is all there, every slot, on Dune and
Flipside and Helius. The agent goes quiet because nobody taught it to read. Sixty thousand wallets
touched your program last month, and the smartest tool you own cannot tell you how many were human.

---

## 2.0 · Meet the Analyst

I have done this work by hand for years. My name appears on dashboards as Ghostiemoh, and most of my
nights look the same: a mint address, a half-finished query, and a stubborn refusal to trust a chart
until I have checked what is under it.

The wound is small and it never heals. I would watch an AI agent confidently write a query that
counted transactions when the question was unique signers. I would watch it sum `amount` straight out
of a transfer table, raw base units, no decimals divisor, and report a holder owning nine billion
tokens. I would watch it pull volume and miss that a swap logs both legs, and double the number
without blinking. The agent was fast, fluent, and wrong, and it had no idea it was wrong.

Gaskiya, that is the part that kept me up. A confident wrong number is worse than no number, because
someone acts on it.

---

## 3.0 · The Structural Pain

The failure was never the model. It was the absence of a specific kind of knowledge, and it broke in
named, repeatable ways.

**Chain-blind SQL.** A generic data skill knows `GROUP BY`. It does not know that `dex_solana.trades`
already carries `amount_usd`, so it recomputes price times amount and drifts.

**No decoding.** Solana instructions are Borsh-encoded bytes behind an eight-byte Anchor
discriminator. Ask an agent "how many times was this instruction called," and it has no path from the
instruction's name to its data. The protocol looks dataless. It is not. It is undecoded.

**Price API as analytics.** Reach for Birdeye or CoinGecko and you get the last price, beautifully.
You do not get retention by cohort, organic-only, which is the number that actually moves a grant.

**The holder query that times out.** Reconstructing balances from net transfer flow is the right
technique and the one that melts on a large token if you do not bound history or pre-aggregate.

**No forensics.** "Is this real", the single most common high-stakes question, had no method at
all. Not wash detection, not rug risk, not sybil clusters. The corner that matters most was empty.

> **[FIGURE 1. Failure-mode panel]**
> **Spec:** Four stacked "wrong answer" cards, double-count, missing decimals, chain-blind SQL, no
> forensics, each crossed in gold. Sovereign Night grade, no people.

Five failures. One root cause: the schema, the metric, and the validation lived in analysts' heads,
not in a skill.

---

## 4.0 · Enter the Skill

So I asked a narrower question than "can AI do analytics." I asked: what would it take to hand an
agent the exact discipline I use at 2am, the tables, the templates, the decoding tricks, the honesty
rules, in a shape the Solana AI Kit could load?

That question became **solana-analytics-skill**. The bet behind it is unfashionable. I did not try to
invent intelligence. I took eight professional Dune dashboards I had already reverse-engineered (volume, holders, retention, market share, launchpad wars) and reshaped that working knowledge into
the kit's structure: a routing entry point, focused references that load only when their intent
fires, an executable layer, agents, and commands. The expertise was real before the skill. The skill
made it reusable.

---

## 4.1 · Why Dune, Helius, and a 200-Line Script?

Because the honest stack is the boring one. Dune's Spellbook already curates Solana into
`dex_solana.trades`, `tokens_solana.transfers`, and `prices.usd`, already USD-normalized and decoded.
Helius owns current state: mint authority, freeze authority, live token accounts, the
facts a historical table cannot give you. Between them they answer almost any question, history from
Dune and "right now" from Helius.

The skill prefers a connected Dune MCP, falls back to a dependency-free Python client when only an API
key is present, and degrades to paste-ready SQL when neither exists. No heavy install. No opaque
binary. A clean path that runs the query it wrote, or tells you plainly that it did not.

---

## 4.2 · Features Snapshot

1. A routing `SKILL.md` that loads one focused reference per intent, token-efficient by design.
2. Twenty-two parameterized, tested DuneSQL templates, Solana-first and EVM-aware.
3. A decoding reference plus a built-in Anchor discriminator deriver (`global:swap` →
   `0xf8c69e91e17587c8`).
4. KPI families: TVL, volume, fees, revenue-kept, DAU/MAU, retention, cohorts, market share.
5. DeFi-by-vertical: DEX/CLMM, lending utilization and liquidations, LST de-peg, perps OI and funding.
6. A forensics module: wash score, rug checklist, sybil clusters, MEV sandwiches, fund tracing.
7. A grant-reporting playbook that leads with durable metrics and an honesty appendix.
8. An executable layer. Dune + Helius MCP, env-keyed, with a script fallback.
9. Three agents (architect, SQL engineer, forensics) and five slash commands.
10. Offline unit tests and a CI gate that rejects placeholder slop in shipped SQL.

---

## 4.3 · The Tests

I will not claim it works. I will show what I ran.

**Test 1, "Which DEX is winning on Solana this month?"** The skill reaches for the market-share
template, scopes the window, and returns share over time across projects, not a snapshot pie, the
stacked-area that shows who is *taking* share. It flagged, unprompted, that share is window-dependent.

> **[FIGURE 2. Screenshot: market-share stacked area]**
> **Spec:** Stacked-area chart of Solana DEX share over 30 days, violet/gold series, real-data look.

**Test 2, "Top holders of this mint, and the risk."** It reconstructed balances, bucketed the
distribution Whale-to-Shrimp, and, this is the part I cared about, warned that the reconstruction
can time out, then handed me the bounded version. It also reminded me to exclude CEX and program
accounts before calling anything a whale.

> **[FIGURE 3. Screenshot: holder distribution buckets]**
> **Spec:** Horizontal bar of holders and supply % per cohort, gold whale bar dominant.

**Test 3, "Is this volume wash-traded?"** It ran the round-trip detector and the honeypot smell
test, cross-checked counterparties against a shared-funder cluster, and returned a *wash score* with
the counter-explanation it had ruled out. Not an accusation. A confidence level and the evidence.

**Test 4, "How often is this instruction called?"** It derived the discriminator from the
instruction name, matched it on raw instructions, and charted adoption, turning an "undecoded"
program into a measured one.

Four questions a price API cannot touch. Four answers, each carrying its own caveat.

---

## 5.0 · The Honest Critique

If I only praised it, you should not believe me. So here is where it is thin.

**First, it leans on Dune's Spellbook coverage.** When a brand-new program is not yet decoded, the
skill can match discriminators on raw tables, but the smooth path, curated, USD-normalized tables, isn't there until someone submits the IDL. The skill tells you this honestly; it does not make the
work disappear.

**Second, the MCP endpoints move.** The Dune and Helius MCP servers are young and their package names
and URLs drift. The skill pins them in config and documents the official sources, but a user may have
to confirm the current command. The dependency-free script exists precisely because the MCP layer is
the least stable part.

**Third, balance and graph reconstructions are heavy.** Holder balances and fund-tracing graphs can
time out or fan out combinatorially on large tokens. The skill ships bounded, pre-aggregated versions
and warns you, but "warns you" is not the same as "magically fast." This is honest on-chain analytics,
not a free lunch.

**Fourth, forensics is probabilistic.** Every signal, wash, rug, sybil, is a heuristic, not a
verdict, and a determined adversary can dress their behavior to dodge it. The skill is built to say
"medium confidence, here is the evidence, here is what I ruled out." It will never hand you certainty,
because the chain rarely offers it.

The outlook is still up and to the right. None of these are design flaws; they are the real texture of
the problem, and naming them is the difference between a tool and a toy.

---

## 6.0 · Return to the Analyst

It is 2am again as I write this, the same mint address open, the same three monitors. The difference
is the chat window no longer stalls. I ask it who holds the float, and it reconstructs the balances,
excludes the exchange wallets, and closes with a single risk sentence I can act on.

The blockchain never lies, but your agent can't read it, so I taught it to. That is the whole of the
work, really: not a smarter model, but a literate one. A skill that knows which table, which decimals,
which double-count, and when to admit it did not run the query.

> *The blockchain never lies, but your agent can't read it.*

The truth was always on-chain. Now the thing answering my questions can finally see it.

---

## 7.0 · Conclusion

In mid-2026 an agent on Solana can build, ship, and secure almost anything, and still go quiet when a
founder asks whether the growth is real. That silence was never a missing model. It was a missing
discipline, the schema, the metric, and the honesty an analyst carries to every chart. I packed that
discipline into one skill, eight dashboards' worth of hard-won method reshaped for the kit. The chain
was always talking. The point was to build something that could finally listen, and tell you the
truth even when the truth is "no data is a finding; fake data is fraud."

---

## 8.0 · References

1. Solana AI Kit, github.com/solanabr/solana-ai-kit
2. skill-bounty, github.com/solanabr/skill-bounty
3. Reference skill: solana-game-skill, github.com/solanabr/solana-game-skill
4. Dune Analytics / Spellbook, docs.dune.com · github.com/duneanalytics/spellbook
5. Flipside Crypto, flipsidecrypto.xyz
6. Helius DAS & RPC, docs.helius.dev
7. SendAI Solana Agent Kit, github.com/sendaifun/solana-agent-kit
8. Jupiter agent-skills, github.com/jup-ag/agent-skills
9. Trail of Bits skills, github.com/trailofbits/skills
10. Anchor (discriminators/IDL), anchor-lang.com
11. Birdeye, birdeye.so
12. CoinGecko, coingecko.com
13. GMGN skills, github.com/GMGNAI/gmgn-skills
14. DefiLlama, defillama.com
15. RugCheck, rugcheck.xyz
16. solana-analytics-skill (this work), repo link on submission
