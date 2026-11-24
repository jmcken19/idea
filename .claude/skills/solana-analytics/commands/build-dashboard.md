---
description: Plan and assemble a Dune dashboard build package for a Solana subject.
argument-hint: <token_mint | project | "A vs B"> [archetype]
---

Build a Dune dashboard package for **$ARGUMENTS** using the solana-analytics skill.

1. Load `references/08-dashboard-build.md`. Name the decision and pick the archetype
   (Market-Structure / Signal / Token Health / Protocol War).
2. Fill `assets/dashboard-spec-template.md`: entity, grain, window, KPI family (a level + a rate + a
   ratio + a behavioral cut), and the per-widget template numbers.
3. Write each widget query clean (`references/09-execution-playbook.md` Cleanliness Checklist),
   parameterized. If `DUNE_API_KEY` is set, `create` each so the package carries real query IDs/URLs.
4. Deliver the Dashboard Build Package: spec + per-widget queries + layout (top→bottom) + narrative
   findings + recommendation + Dune assembly steps. Validate before shipping; flag any unrun query.
