---
name: intake
description: Mode B, Stage 1. Start a deep-validation record for an idea the founder has explicitly asked to validate. Captures it verbatim, with falsifiable hypotheses and the keyword list. Not for casual brainstorming (use brainstorm).
---
0. Start the hard budget, since deep validation begins here: `python3 tools/ir.py budget start <slug> validate --reason "<founder's exact request>"` (45 research calls, 5 agents; the hook blocks anything beyond).
1. Check whether it already exists: `python3 tools/ir.py searched <2-3 key terms>`, `validations/INDEX.md`, `ideas/` notes and `lessons/README.md`. If a brainstorm note exists, carry over its angles and unknowns. If a record exists, reopen that one (only with new evidence) instead of creating a duplicate.
2. `python3 tools/ir.py new <slug> "<the idea exactly as the user wrote it>"`. A pivot is a new slug that links its parent (Rule R4).
3. Fill in `validations/<slug>/initial-hypothesis.md`:
   - problem, specific segment, solution, why now, and the revenue model as submitted (leave it blank if none was given; do not invent one);
   - hypotheses H1…Hn, each with a kill condition. H1 is always "nothing equivalent exists for this segment";
   - at least 8 alternative phrasings for the job (incumbent feature names, adjacent-industry words, tool words, other chains).
4. Record the idea as framed. Alternative framings from brainstorming go in the hypotheses list, not into the idea itself.
5. If the problem or segment is too vague to search for, ask the user once, then stop.
6. Write the Gate 1 result in the idea's README stage log. Next step: `/kill-check <slug>`.
