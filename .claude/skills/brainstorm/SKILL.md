---
name: brainstorm
description: Mode A, the default. Explore an idea, observation or "what if" with the founder. Understand it, widen it (audiences, business models, distribution, infrastructure combinations), name adjacent opportunities, challenge assumptions, and list unknowns. Cheap. Use whenever the founder brings an idea without asking for validation.
---
Run inline. No subagents, no records, no scores.

1. **Understand.** Restate the idea in one line. If it's ambiguous, ask one question.
2. **Check what we already know (free):** `python3 tools/ir.py searched <terms>`, `research/INDEX.md`, `lessons/README.md`.
3. **Explore the concept, not just the proposal.** What job does it do, and for whom? What other audiences, business models (who pays, for what), distribution channels, infrastructure combinations or user experiences could serve that job?
4. **Cross-industry and unexpected combinations:**
   - *Outside → in:* a proven business model from another industry (payments, insurance, franchising, marketplaces, subscriptions, cooperatives, ticketing…) that could be adapted.
   - *Inside → out:* crypto infrastructure (fee routing, streams, multisigs, token mechanics, on-chain data, automation) that could power a non-obvious business, including real-world services.
   - At least one combination of existing pieces that nobody seems to use together.
   Mark each as novel vs useful. Don't confuse the two, and don't invent demand.
5. **Adjacent opportunities:** 2–4 nearby directions worth thinking about, each in a line.
6. **Challenge assumptions:** which beliefs the idea rests on, and which look weakest.
7. **Existing players:** if something similar exists, show it, briefly, as context. Then ask where an opening could be. Don't invent one if none is visible.
8. **Honest take:** is it interesting, and why or why not?
9. **Unknowns:** what we don't know, and the 1–3 cheapest checks that would matter most.

Searches: 0–3 standard WebSearch, only when one fact would change the discussion. Log them (`python3 tools/ir.py log WebSearch "<q>" - "<result>"`).
Close by offering: save as a note (`python3 tools/ir.py note …`), keep exploring, or run a deep validation (`/validate`).
