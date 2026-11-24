# Tooling: audit, evaluation and configuration

Audited 2026-11-24 in a Claude Code cloud session. Re-audit when the environment changes.

## 1. What the environment has

| Capability | Status | Notes |
|---|---|---|
| WebSearch (standard and extended) | **Works** | Server-side; returns results plus summaries. Results are `S`-grade evidence until a page is opened |
| web-fetch (open a page) | **Blocked** for hosts outside the environment's allowed list (DNS failure). This is the main gap | Same network policy as the container |
| GitHub search (`gh api -X GET search/...`, `ir.py fetch github-repos`) | **Works** | Repo/code search across GitHub. Reading a repo's README or files needs the repo attached (`add_repo`) |
| npm registry (`ir.py fetch npm <pkg>`) | **Works** | SDK versions and publish dates; good primary evidence for when a protocol feature shipped |
| Python 3.13, Node 22, jq, curl, gh | Installed | `tools/ir.py` needs only the Python standard library |
| DefiLlama, CoinGecko, GeckoTerminal, DexScreener, Jupiter, RugCheck, Solana RPC, Dune, Reddit, HN, Wayback | **Blocked** by the network policy (proxy 403), as of 2026-11-24 | Endpoints are already wired into `ir.py fetch`; they work as soon as the hosts are allowed |
| MCP servers | posty and a thumbnail maker configured at user level, both failing (blocked hosts); unrelated to research | No research MCP installed, by design (see 4) |
| Skills | `solana-analytics` installed in this repo (MIT, from the Salary repo). Social-media and design skills exist at user level and are irrelevant here | |
| Build skills (pumpfun, helius, squads, solana-dev) | Deliberately **not** installed (Rule R5) | Readable in `jmcken19/salary/.claude/skills/` for protocol facts |

## 2. Data sources evaluated

Pricing as found on 2026-11-24 from the providers' docs via search (`S`/`C` grade). Check each pricing page before paying.

| Source | Use in validation | Cost / limits | Setup | Verdict |
|---|---|---|---|---|
| **DefiLlama free API** (`api.llama.fi`, `coins.llama.fi`) | Fees, revenue and TVL per protocol; category landscapes; demand evidence at levels 3–4 | Free, no key. Pro API about $300/month (not needed) | Allow hosts | **Configured** in `ir.py` (`defillama-*`). Needs host allowlisting |
| **DexScreener API** | Token launches with the same pitch, pair traction, volume | Free, no key; about 60–300 requests/min by endpoint | Allow host | **Configured** (`dexscreener-*`) |
| **CoinGecko API** | Token existence, market cap, categories | Keyless shared pool, or free Demo key: 10k calls/month | Optional free key → `COINGECKO_DEMO_API_KEY` | **Configured** (`coingecko-*`) |
| **GeckoTerminal** | Pool search on Solana | Free, no key | Allow host | **Configured** |
| **Jupiter token API** (`lite-api.jup.ag`) | Token lookup and verification status | Free | Allow host | **Configured** |
| **RugCheck** | Token risk summaries (a competitor *and* a data source for trust-tool ideas) | Free endpoints | Allow host | **Configured** |
| **GitHub search** | Existing implementations, abandoned projects | Free; about 10 searches/min unauthenticated, 30 with a token | Works now | **Configured** (`github-*`; `gh api`) |
| **npm registry** | SDK release history = when a feature shipped | Free | Works now | **Configured** (`npm`, `npm-search`) |
| **Reddit JSON, HN Algolia** | Complaints, requests for alternatives (demand levels 1–2) | Free | Allow hosts | **Configured** (`reddit`, `hn`) |
| **Wayback CDX** | Dead and abandoned products, launch dates | Free | Allow host | **Configured** (`wayback`) |
| **Solana RPC** (public, or Helius) | Direct on-chain reads (account counts, configs) | Public RPC free but rate-limited. Helius Free: $0, 1M credits/month, 10 RPC req/s, 2 DAS req/s; Developer $49/month | Free Helius key via the environment's credential form | Use the public RPC first; Helius only for heavy on-chain stages |
| **Dune** (API / MCP) | Behavioural on-chain demand: cohorts, usage of competitors | The free plan is now view-only, with **no API**. API access needs a trial (2,500 credits) or a paid plan (Analyst about $65–75/month) | Paid key; `solana-analytics` skill has `scripts/dune_run.py` | **Not configured. Do not pay** until an idea reaches Stage 4 and needs on-chain behaviour that free sources can't provide |
| **X / Twitter** | Sentiment, launches, complaints | API is paid; the site blocks automated fetching | n/a | Use WebSearch for X content (`S` grade); no integration |
| **Birdeye, CoinMarketCap, Solscan Pro** | Overlap with the free sources above | Keys required | n/a | **Not configured**: redundant with free sources |
| Data MCP servers (DexScreener, DefiLlama, Dune MCP) | Same data as REST | Free/paid | | **Not installed**: an MCP adds tool schemas to every session's context, while the cached REST CLI costs nothing until used |

## 3. What needs the founder

1. **Allow research hosts** (one-time, free). The automatic environment proposal was rejected by the service, so add these under the environment's *Network access → Allowed domains* (keep "Allow package managers" ticked). Use a dedicated environment for this repo rather than your Default, so other projects don't get these hosts:
   ```
   api.llama.fi coins.llama.fi api.coingecko.com api.geckoterminal.com api.dexscreener.com
   lite-api.jup.ag api.rugcheck.xyz api.mainnet-beta.solana.com www.reddit.com hn.algolia.com web.archive.org
   ```
   Optional, for opening docs pages directly: the docs domains of protocols under research (e.g. `docs.bags.fm`, `pump.fun`, `docs.squads.so`, `docs.streamflow.finance`).
   Docs: https://code.claude.com/docs/en/cloud-environments#network-access
2. **Optional free keys:** CoinGecko Demo (`COINGECKO_DEMO_API_KEY`); Helius Free (save it via the environment's network-secret form for `mainnet.helius-rpc.com`, never in chat or in the repo).
3. **Paid, only if needed later:** Dune Analyst (about $65–75/month) for behavioural on-chain demand studies.

## 4. Configuration in this repo

- `tools/ir.py`: cached fetcher, search log, deduplication lookup, idea scaffolding, scorer, linter.
- `.claude/agents/`: four specialist agents (see `system/agent-architecture.md`).
- `.claude/skills/`: `intake`, `kill-check`, `validate`, `adversarial-review`, plus `solana-analytics`.
- No `.claude/settings.json` was committed: an agent shouldn't grant itself permissions. If permission prompts get in the way, the founder can add this to `.claude/settings.json`:
  ```json
  { "permissions": { "allow": ["Bash(python3 tools/ir.py:*)", "Bash(gh api -X GET search/:*)", "WebSearch"] } }
  ```
- `.gitignore`: excludes `research/.cache/`.
