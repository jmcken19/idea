---
description: Produce the validated protocol-health one-pager for a Solana protocol.
argument-hint: <project or program_id> [days]
---

Run a full protocol-health analysis for **$ARGUMENTS** using the solana-analytics skill.

1. Load `references/03-protocol-kpis.md` and confirm the entity (`project` / `program_id`) and the
   window (default 30 days if not given).
2. Assemble the protocol-health one-pager: volume + trend, DAU with new-vs-returning, retention
   cohort, market share vs peers over time, revenue (kept, not gross), holder distribution headline,
   and one forensics sanity check (real vs wash-traded volume).
3. Use the matching templates from `assets/dune-query-library.sql` (4, 1-3, 13, 11, 10, 12, 17).
   Validate each via the Dune MCP or `scripts/dune_run.py` (`references/09-execution-playbook.md`);
   if you can't run them, deliver paste-ready and label them unrun.
4. End on the decision: is this protocol growing, defensible, and real — and what should the
   team/investor do next? Carry every caveat (wallet ≠ user, window-dependent share, proxy revenue).
