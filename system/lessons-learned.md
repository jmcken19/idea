# Lessons learned (permanent rules)

These rules guard against *building* something that already exists. They apply in deep validations (Mode B), and whenever Claude would suggest developing anything. They do **not** mean killing ideas during brainstorming: there, an existing competitor is a starting point for finding a different angle.

Each lesson comes from a real failure and has become a rule that the framework enforces. The full Salary record is in `lessons/salary/` (historical, closed). The postmortem is `lessons/salary/postmortem.md`. **Salary isn't re-investigated unless the founder asks.**

## From Salary (Nov 23–24, 2026)

### L1. The building blocks are the competitor
**What happened:** On day one, Salary's own research (`salary/docs/research.md`) documented that Pump.fun fee sharing already split creator fees across up to 10 wallets (live since Jan 9, 2026), that Bags allowed up to 100 claimers, and that Streamflow did payroll streams and Squads ran team treasuries. All four were filed as *infrastructure to build on*, never as *products a customer could already use instead*.
**Rule R1:** In Stage 2, every protocol, platform feature or SDK the idea would use must also be assessed as a competitor: "Can the target customer get the job done with this alone, or with this plus a spreadsheet?" If yes, that is an equivalent.

### L2. Technical verification is not market validation
**What happened:** The research was excellent at the wrong question. It decoded account layouts byte by byte, sealed fixtures and ran a blind on-chain study, all to prove the reader worked. Market and competitor research (`research-v2`) came about 11.5 hours later, after 45 of the 59 commits.
**Rule R2:** No technical-feasibility work beyond a one-paragraph sanity check until Gate 2 (existence) and Gate 4 (demand) have passed. `technical-feasibility.md` is last for that reason.

### L3. Read your own negative data as negative
**What happened:** Salary's own chain data said demand was thin. 95.4% of fee-sharing configs had a single recipient. Only 4.6% (≈42k coins) split at all. 0 of 20 multi-wallet coins had any team lock. These numbers were recorded and then explained away ("teams may fund payroll manually").
**Rule R3:** Every data point gets a direction label (supports / contradicts / neutral) at the moment it is recorded. The adversarial review lists all the *contradicts* items first. A finding that contradicts the hypothesis cannot be reframed as an opportunity without new evidence.

### L4. Repositioning is not differentiation
**What happened:** On discovering the overlap, the pitch moved to "Pump.fun splits fees. Salary runs your team." The decisions doc itself said those differences were "real but thin … Pump.fun could copy". The next proposal (Team Record / Builder Passport) was again not checked for existence. Deployer-history tools already existed (MadeOnSol Deployer Hunter, Mobula dev-history API, Rug Munch, Noesis dev analyzer).
**Rule R4:** A pivot is a new idea. It gets a new intake and its own Stage 2 before any of the old work is carried over. Differentiation must pass the four-question test in `existing-solutions.md`. If the incumbent could ship the difference in one release, it is a feature, not a company.

### L5. Narrative and aesthetics are not evidence
**What happened:** 35 commits went to the website: at least eight visual directions (Blue Hour Voxel, editorial title-card, record sleeve, Samurai ASCII, Chongqing skyline, black theme, ASCII New York skyline, Blender logo), plus an animated payday flow. All of this came before any customer conversation, demand test or revenue decision.
**Rule R5:** This repository produces no websites, logos, mockups, demos, smart contracts or tokenomics. Those only start after a VALIDATED or CONDITIONAL verdict *and* an explicit decision by the founder, in a different repository.

### L6. No payer, no product
**What happened:** A 1% payday fee and a Pro plan were added to the site and then removed. "Salary's revenue" stayed OPEN to the end. Creator fees were known to be concentrated in a few coins, so most teams had nothing to pay salaries from, let alone a fee.
**Rule R6:** Gate 5 needs a named payer, a reason they would pay instead of using the free or native option, and a price compared with what incumbents charge. "Decide later" is NEEDS MORE RESEARCH, never CONDITIONAL.

### L7. Snippets are not sources
**What happened:** research-v2 says it was compiled "from web search snippets only (most pages could not be fetched)". It still produced confident conclusions such as "That is the opening for Salary".
**Rule R7:** Search-snippet evidence is tagged `S` and can never alone support a material claim (existence of a gap, market size, traction). A claim that "nobody offers X" needs full Stage 2 coverage, logged in the search log.

### L8. The researcher should not grade their own idea
**What happened:** The same process that built Salary also researched, ranked and stress-tested it. The "stress test" used "existing research only" and every attack was answered "Yes" or "Partly".
**Rule R8:** Stage 6 is done by a separate agent with a fresh context. It gets the claims and the sources, not the pitch. It is told its job is to kill the idea.

### L9. Kill tests that never run are worthless
**What happened:** research-v2 defined good kill tests: an on-chain census, a 20-coin prototype shown to traders, a concierge launch for 100 teams, one terminal partner. None were run before the next round of design work.
**Rule R9:** A CONDITIONAL verdict must name its kill tests with thresholds and dates. The idea cannot move on until each test has a recorded result.

### L10. Speed hides the decision point
**What happened:** All 59 commits happened between 15:46 UTC Nov 23 and 03:18 UTC Nov 24. Development happened so fast that there was never a moment where someone asked "should we?" before "how do we?".
**Rule R10:** Stages are sequential gates with a written result in the idea's README stage log. A stage cannot start until the previous gate result is written.

### L11. Verify equivalence at primary grade, in both directions
**What happened:** the first-pass rejection said a scheduled fee-distribution tool (pumpdev.io) existed, on snippet evidence. Primary sources later showed it wasn't verified, so the "it already exists" claim was overstated for the salary layer. The fee-splitting part really was native.
**Rule R11:** "Already exists" and "nobody has built this" are both material claims. Neither is accepted on snippets. Overstating competition throws away real openings, just as understating it repeats Salary.

## Adding a lesson

When an idea is rejected late, or a verdict is reversed, add an entry here: what happened, the evidence, and the rule. Then change the framework file that enforces it.
