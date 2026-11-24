---
name: intake
description: Stage 1 of idea validation. Register a new idea verbatim, restate it without expansion, write falsifiable hypotheses and the keyword expansion list. Use when the user submits a new business idea or a pivot.
---
1. Check whether it already exists: `python3 tools/ir.py searched <2-3 key terms>` and `ideas/INDEX.md`. If a record exists, reopen that one (only with new evidence) instead of creating a duplicate.
2. `python3 tools/ir.py new <slug> "<the idea exactly as the user wrote it>"`. A pivot is a new slug that links its parent (Rule R4).
3. Fill in `ideas/<slug>/initial-hypothesis.md`:
   - problem, specific segment, solution, why now, and the revenue model as submitted (leave it blank if none was given; do not invent one);
   - hypotheses H1…Hn, each with a kill condition. H1 is always "nothing equivalent exists for this segment";
   - at least 8 alternative phrasings for the job (incumbent feature names, adjacent-industry words, tool words, other chains).
4. Do not add features, suggest improvements or design anything.
5. If the problem or segment is too vague to search for, ask the user once, then stop.
6. Write the Gate 1 result in the idea's README stage log. Next step: `/kill-check <slug>`.
