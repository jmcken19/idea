---
name: discover
description: Opportunity discovery scan on request. Look for opportunities the founder hasn't named in an area (e.g. Solana token launches, creator economics, new infrastructure), separating "unbuilt" from "wanted". Use when the founder asks what opportunities exist somewhere.
---
Budget: up to 10 standard WebSearch, plus cheap primary checks (`ir.py npm-grep`, `fetch github-repos`). One `market-researcher` agent only if the founder asks for a broad scan. Reuse `research/` first (`python3 tools/ir.py searched <terms>`).

1. Scope the area in one line with the founder (chain, segment, time window).
2. Find what changed recently: new infrastructure, launch mechanisms, protocol economics and policy changes, with dates and sources.
3. Look for underserved users of existing products, recurring developer and community pain, poor UX, and existing tools that could be combined in a new way. Look beyond crypto narratives: traditional business models that could be adapted to crypto, and crypto infrastructure that could enable different businesses (payments, financial and developer tooling, consumer apps, incentives, automation, community-owned ecosystems, real-world services).
4. For each candidate, record: why now, the evidence of a real need (kind and level per `system/research-standards.md` §9), who already plays there, and whether it is merely **unbuilt** or actually **wanted**. A missing product is not demand.
5. Write `discovery/YYYY-MM-DD-<area>.md` from `templates/discovery-scan.md`. Add any reusable facts to `research/` and log every search.
6. Report the 3–5 most interesting threads to brainstorm next. Don't validate them unless asked.
