"""Tests for tools/ir.py. Run: python3 -m unittest discover -s tests -v
Offline: uses file:// URLs and temporary idea folders, never the real research log."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import ir  # noqa: E402


def run(fn, *args):
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            fn(list(args))
        except SystemExit as e:
            code = e.code or 0
    return out.getvalue(), err.getvalue(), code


class Sandbox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._saved = (ir.CACHE, ir.SEARCH_LOG, ir.RESEARCH_INDEX, ir.IDEAS, ir.IDEA_INDEX)
        ir.CACHE = os.path.join(self.tmp, "cache")
        ir.SEARCH_LOG = os.path.join(self.tmp, "search-log.md")
        ir.RESEARCH_INDEX = os.path.join(self.tmp, "INDEX.md")
        ir.IDEAS = os.path.join(self.tmp, "ideas")
        ir.IDEA_INDEX = os.path.join(ir.IDEAS, "INDEX.md")
        os.makedirs(ir.IDEAS)

    def tearDown(self):
        ir.CACHE, ir.SEARCH_LOG, ir.RESEARCH_INDEX, ir.IDEAS, ir.IDEA_INDEX = self._saved
        shutil.rmtree(self.tmp)


class TestCachingAndDedup(Sandbox):
    def test_fetch_caches_and_second_call_is_a_hit(self):
        page = os.path.join(self.tmp, "data.json")
        json.dump({"total24h": 42}, open(page, "w"))
        url = "file://" + page
        _, err1, _ = run(ir.cmd_fetch, "url", url)
        _, err2, _ = run(ir.cmd_fetch, "url", url)
        self.assertIn("fetched", err1)
        self.assertIn("cache hit", err2)
        log = open(ir.SEARCH_LOG).read()
        self.assertEqual(log.count(url), 1, "a cache hit must not be logged or paid for again")

    def test_max_age_zero_refetches(self):
        page = os.path.join(self.tmp, "d.json")
        json.dump({"a": 1}, open(page, "w"))
        run(ir.cmd_fetch, "url", "file://" + page)
        _, err, _ = run(ir.cmd_fetch, "url", "file://" + page, "--max-age", "0")
        self.assertIn("fetched", err)

    def test_searched_finds_prior_queries(self):
        run(ir.cmd_log, "WebSearch", "pump.fun fee sharing split", "salary", "native feature found")
        out, _, _ = run(ir.cmd_searched, "fee", "sharing")
        self.assertIn("native feature found", out)
        out, _, _ = run(ir.cmd_searched, "quantum", "toaster")
        self.assertIn("0 prior hit", out)

    def test_spend_counts_per_idea_and_flags_overruns(self):
        for i in range(51):
            run(ir.cmd_log, "WebSearch", f"q{i}", "x", "r")
        run(ir.cmd_log, "WebSearch", "other", "y", "r")
        out, _, _ = run(ir.cmd_spend, "x")
        self.assertIn("51 / 50", out)
        self.assertIn("OVER BUDGET", out)


def make_idea(base, slug, **overrides):
    d = os.path.join(base, slug)
    shutil.copytree(os.path.join(ROOT, "templates", "idea"), d)
    files = {
        "sources.md": "| ID | Source | Locator | Type | Published | Accessed | Supports |\n|---|---|---|---|---|---|---|\n"
                      "| S1 | SDK | https://registry.npmjs.org/x | repo | 2026-01-01 | 2026-11-24 | feature exists |\n"
                      "| S2 | News | https://news.example/x | snippet | 2026-01-01 | 2026-11-24 | feature exists |\n",
        "existing-solutions.md": "## Search coverage\n| Channel | Done? | Q | Hits |\n|---|---|---|---|\n"
                                 "| GitHub | Yes | q | 1 |\n| Recent launches (90d) | Yes | q | 0 |\n| Discontinued projects | Blocked: wayback | q | 0 |\n"
                                 "## Easy replicators\n| Who | Why | Evidence |\n|---|---|---|\n| Incumbent | owns the program | S1 |\n",
        "final-verdict.md": "# Final verdict\n\n**Verdict:** REJECTED\n\n## Unresolved uncertainties\n\nWhether the incumbent feature is still live; prices unknown.\n",
        "adversarial-review.md": "Reviewer: test, 2026-11-24\n",
    }
    rows = overrides.pop("scores", None) or [(1, 15, "1", "no", "S1"), (2, 15, "0", "yes", "S1"), (3, 15, "1", "no", "S1"),
                                             (4, 8, "1", "no", "S1"), (5, 10, "1", "no", "S1"), (6, 10, "1", "no", "S1"),
                                             (7, 10, "1", "no", "S1"), (8, 5, "4", "no", "S1"), (9, 7, "0", "no", "S1"),
                                             (10, 5, "2", "no", "S1")]
    files["scorecard.md"] = "| # | Criterion | Weight | Score | Fatal | Evidence | Rationale |\n|---|---|---|---|---|---|---|\n" + "".join(
        f"| {n} | c{n} | {w} | {s} | {f} | {e} | r |\n" for n, w, s, f, e in rows)
    files.update(overrides)
    for fn, text in files.items():
        open(os.path.join(d, fn), "w").write(text)
    return d


class TestSpendAttribution(Sandbox):
    def test_fetches_are_attributed_via_IR_IDEA(self):
        page = os.path.join(self.tmp, "x.json")
        json.dump({"k": 1}, open(page, "w"))
        os.environ["IR_IDEA"] = "attrib"
        try:
            run(ir.cmd_fetch, "url", "file://" + page)
        finally:
            del os.environ["IR_IDEA"]
        out, _, _ = run(ir.cmd_spend, "attrib")
        self.assertIn("fetch        1 / 60", out)


class TestLintAndSafeguards(Sandbox):
    def test_clean_record_passes(self):
        d = make_idea(ir.IDEAS, "good")
        self.assertEqual(ir.lint_one(d), [])

    def test_citation_to_missing_source_is_caught(self):
        d = make_idea(ir.IDEAS, "badcite", **{"market-research.md": "Claim [V: S9]\n"})
        self.assertTrue(any("S9" in p for p in ir.lint_one(d)))

    def test_SG1_fatal_on_snippet_only_is_caught(self):
        rows = [(1, 15, "1", "no", "S2"), (2, 15, "0", "yes", "S2")] + [(n, 5, "1", "no", "S1") for n in range(3, 11)]
        d = make_idea(ir.IDEAS, "sg1", scores=rows)
        self.assertTrue(any(p.startswith("SG1") for p in ir.lint_one(d)))

    def test_SG2_sample_without_n_is_caught(self):
        d = make_idea(ir.IDEAS, "sg2", **{"market-research.md": "In our sample 20 of 20 coins were locked.\n"})
        self.assertTrue(any(p.startswith("SG2") for p in ir.lint_one(d)))
        d2 = make_idea(ir.IDEAS, "sg2ok", **{"market-research.md": "In our sample 20 of 20 coins were locked (n=20, random, illustrative).\n"})
        self.assertFalse(any(p.startswith("SG2") for p in ir.lint_one(d2)))

    def test_SG3_SG4_missing_replicators_and_channels(self):
        d = make_idea(ir.IDEAS, "sg34", **{"existing-solutions.md": "| GitHub | Yes | q | 1 |\n"})
        probs = ir.lint_one(d)
        self.assertTrue(any(p.startswith("SG3") for p in probs))
        self.assertEqual(sum(p.startswith("SG4") for p in probs), 2)

    def test_SG5_absence_of_evidence_is_not_opportunity(self):
        rows = [(1, 15, "4", "no", "S1"), (2, 15, "5", "no", "S1")] + [(n, 5, "3", "no", "S1") for n in range(3, 11)]
        es = ("| GitHub | Partly | q | 0 |\n| Recent launches | Yes | q | 0 |\n| Discontinued | Blocked: x | q | 0 |\n"
              "## Easy replicators\n| Who | Why | Evidence |\n|---|---|---|\n| X | y | S1 |\n")
        d = make_idea(ir.IDEAS, "sg5", scores=rows, **{"existing-solutions.md": es})
        self.assertTrue(any(p.startswith("SG5") for p in ir.lint_one(d)))

    def test_SG6_verdict_without_uncertainties(self):
        d = make_idea(ir.IDEAS, "sg6", **{"final-verdict.md": "**Verdict:** REJECTED\n"})
        self.assertTrue(any(p.startswith("SG6") for p in ir.lint_one(d)))

    def test_validated_without_review_is_blocked(self):
        rows = [(n, 10, "5", "no", "S1") for n in range(1, 11)]
        d = make_idea(ir.IDEAS, "val", scores=rows, **{
            "final-verdict.md": "**Verdict:** VALIDATED OPPORTUNITY\n\n## Unresolved uncertainties\n\nplenty remain unknown here.\n",
            "adversarial-review.md": "Reviewer: TODO\n"})
        self.assertTrue(any("adversarial review" in p for p in ir.lint_one(d)))

    def test_verdict_above_ceiling_is_blocked(self):
        d = make_idea(ir.IDEAS, "ceil", **{"final-verdict.md": "**Verdict:** CONDITIONAL OPPORTUNITY\n\n## Unresolved uncertainties\n\nsomething important.\n"})
        self.assertTrue(any("exceeds the scorecard ceiling" in p for p in ir.lint_one(d)))


DEMAND_TABLE = "## Demand evidence\n| Evidence | Kind | Level | Direction | Tag + source |\n|---|---|---|---|---|\n"


class TestDemandVersusEngagement(Sandbox):
    """Item 9: the system must not count social engagement as customer demand."""

    def lint_with(self, rows, demand_score="3"):
        sc = [(1, 15, "3", "no", "S1"), (2, 15, "3", "no", "S1"), (3, 15, demand_score, "no", "S1")] + \
             [(n, 5, "3", "no", "S1") for n in range(4, 11)]
        mr = DEMAND_TABLE + "".join(f"| {e} | {k} | {l} | {dr} | {t} |\n" for e, k, l, dr, t in rows)
        d = make_idea(ir.IDEAS, "dem" + str(abs(hash(mr)) % 10**6), scores=sc, **{"market-research.md": mr})
        return [p for p in ir.lint_one(d) if p.startswith(("demand", "DEMAND"))]

    def test_viral_engagement_cannot_be_level_3_or_4(self):
        probs = self.lint_with([
            ("Launch tweet: 12k likes, 3k retweets", "likes", "3", "+", "[V: S1]"),
            ("Waitlist of 5,000 sign-ups", "waitlist", "4", "+", "[V: S1]"),
            ("Repo has 2k stars", "stars", "3", "+", "[V: S1]"),
            ("Token pumped 400%", "token-price", "4", "+", "[V: S1]"),
        ])
        self.assertEqual(sum("engagement is not demand" in p for p in probs), 4)

    def test_engagement_only_cannot_support_a_demand_score_of_3(self):
        probs = self.lint_with([("Viral thread", "engagement", "1", "+", "[V: S1]"),
                                ("KOL shout-out", "kol-mention", "1", "+", "[V: S1]")])
        self.assertTrue(any(p.startswith("DEMAND") for p in probs))

    def test_paid_usage_with_verified_evidence_supports_demand(self):
        probs = self.lint_with([("Competitor charges $49/mo; 300 paying teams on its public page", "paid-product", "4", "+", "[V: S1]")])
        self.assertEqual(probs, [])

    def test_snippet_paying_evidence_is_not_enough(self):
        probs = self.lint_with([("Article says teams pay for it", "paid-product", "4", "+", "[S: S2]")])
        self.assertTrue(any(p.startswith("DEMAND") for p in probs))

    def test_negative_usage_does_not_count_as_support(self):
        probs = self.lint_with([("95% of coins don't use the free split", "native-feature-usage", "3", "-", "[V: S1]")])
        self.assertTrue(any(p.startswith("DEMAND") for p in probs))

    def test_unknown_kind_is_rejected(self):
        probs = self.lint_with([("Vibes", "hype", "2", "+", "[V: S1]")], demand_score="1")
        self.assertTrue(any("unknown kind" in p for p in probs))


class TestScoringGates(unittest.TestCase):
    def rows(self, scores, fatal=(), ev="S1"):
        ws = [15, 15, 15, 8, 10, 10, 10, 5, 7, 5]
        return [dict(n=i + 1, criterion=f"c{i + 1}", weight=w, score=s, fatal=(i + 1) in fatal, evidence=ev)
                for i, (w, s) in enumerate(zip(ws, scores))]

    def test_high_total_cannot_hide_existing_equivalent(self):
        score, ceiling, _ = ir.evaluate(self.rows([1, 0, 5, 5, 5, 5, 5, 5, 5, 5]))
        self.assertGreater(score, 70)
        self.assertEqual(ir.VERDICTS[ceiling], "REJECTED")

    def test_fatal_flag_wins(self):
        self.assertEqual(ir.VERDICTS[ir.evaluate(self.rows([5] * 10, fatal=(10,)))[1]], "REJECTED")

    def test_scores_without_evidence_are_unverified(self):
        score, ceiling, _ = ir.evaluate(self.rows([5] * 10, ev=""))
        self.assertEqual(score, 0)
        self.assertEqual(ir.VERDICTS[ceiling], "NEEDS MORE RESEARCH")


if __name__ == "__main__":
    unittest.main()
