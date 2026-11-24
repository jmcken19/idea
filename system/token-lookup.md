# Token lookup rule: assume a name might be a memecoin

Added at the founder's request, 2026-11-24. The founder often names things that are memecoins (e.g. "Accelerando", "Singularity", "Frontier"). A name from the founder is **a token until shown otherwise**. Never fall back on the book, film or common word, and never use generic web-search snippets for token facts. They gave wrong tokens and numbers in the first pass.

## Procedure
1. **Ask for the contract address (CA) or ticker** if the name is ambiguous. Many tokens share one name (30 pairs came back for "singularity"). A CA settles it; a name does not.
2. **Look up by CA when given, by name otherwise**, through `ir.py fetch`. These are cached and logged. Try them in order and **do not stop at the first empty result**:
   1. `dexscreener-token <CA>` / `dexscreener-search <name>`
   2. `geckoterminal-pools <CA or name>` (found the Accelerando pool that DexScreener did not list)
   3. `jup-search <name or CA>` (Solana token list)
   4. `coingecko-search <name>` / `coingecko-coin <id>` (listed tokens)
   5. `rugcheck <CA>` (creator history, risk flags; a heuristic, not proof)
   6. Only then a web search, and say it is S-grade.
3. **Empty is not "doesn't exist".** DexScreener `pairs: null` can mean new, dormant or unindexed. State which sources were tried and what each said.
4. **Report per token:** chain, CA, DEX, pair age, liquidity, 24h volume, market cap (rough), creator flags, and what is still unknown (holders, who is behind it).
5. **Cached files are wrapped:** read `["body"]["pairs"]` from `research/.cache/*.json`, not the top level.

## Data caveats
- Pair-level market caps are noisy (one BSC pair showed $690B). Use as rough, tag M or lower.
- The same token appears under several pairs and quote tokens. Dedupe by base-token address.
- Pairs quoted in another small token (a "pairing coin") are a real mechanic; note the quote token when it matters.
- Numbers go stale in 30 days (`system/usage-budget.md`).

## Budget
These lookups count toward the research caps: 3 per brainstorm session, or the workflow cap once `budget start` has been run by the founder. When the cap is hit, stop and ask.

## Status of the tools (verified 2026-11-24)
DexScreener, GeckoTerminal and RugCheck responded in this session. `system/tooling.md` still lists them as blocked; that table is out of date.
