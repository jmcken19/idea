#!/usr/bin/env python3
"""
Offline unit tests for dune_run.py - run with: python -m unittest discover -s scripts -p "test_*.py"
No network and no DUNE_API_KEY required; only the pure helpers are exercised.
"""
import json
import os
import tempfile
import unittest

import dune_run


class TestAnchorDiscriminator(unittest.TestCase):
    # Reference vectors (first 8 bytes of sha256("<namespace>:<name>"), hex).
    KNOWN = {
        ("global", "initialize"): "afaf6d1f0d989bed",   # the canonical Anchor `initialize`
        ("global", "swap"): "f8c69e91e17587c8",
        ("account", "State"): "d8926b5e684bb6b1",
        ("event", "TradeEvent"): "bddb7fd34ee661ee",
    }

    def test_known_vectors(self):
        for (ns, name), expected in self.KNOWN.items():
            self.assertEqual(dune_run.anchor_discriminator(ns, name), expected,
                             msg=f"{ns}:{name}")

    def test_is_eight_bytes_hex(self):
        d = dune_run.anchor_discriminator("global", "anything")
        self.assertEqual(len(d), 16)                       # 8 bytes -> 16 hex chars
        int(d, 16)                                         # raises if not valid hex

    def test_deterministic(self):
        self.assertEqual(
            dune_run.anchor_discriminator("global", "swap"),
            dune_run.anchor_discriminator("global", "swap"),
        )

    def test_distinct_names_differ(self):
        self.assertNotEqual(
            dune_run.anchor_discriminator("global", "swap"),
            dune_run.anchor_discriminator("global", "deposit"),
        )

    def test_namespace_matters(self):
        self.assertNotEqual(
            dune_run.anchor_discriminator("global", "State"),
            dune_run.anchor_discriminator("account", "State"),
        )

    def test_bad_namespace_raises(self):
        with self.assertRaises(ValueError):
            dune_run.anchor_discriminator("instruction", "swap")


class TestBuildCreatePayload(unittest.TestCase):
    def test_minimal_payload(self):
        p = dune_run.build_create_payload("SELECT 1", "q", {}, private=False)
        self.assertEqual(p["name"], "q")
        self.assertEqual(p["query_sql"], "SELECT 1")
        self.assertFalse(p["is_private"])
        self.assertNotIn("parameters", p)                  # no params -> no key

    def test_params_become_typed_entries(self):
        p = dune_run.build_create_payload("SELECT {{days}}", "q", {"days": 30}, private=True)
        self.assertTrue(p["is_private"])
        self.assertEqual(p["parameters"], [{"key": "days", "type": "text", "value": "30"}])

    def test_param_values_stringified(self):
        p = dune_run.build_create_payload("x", "q", {"a": 1, "b": "raydium"}, private=False)
        values = {e["key"]: e["value"] for e in p["parameters"]}
        self.assertEqual(values, {"a": "1", "b": "raydium"})  # ints coerced to str


class TestLoadParams(unittest.TestCase):
    def test_none_returns_empty(self):
        self.assertEqual(dune_run.load_params(None), {})

    def test_reads_flat_object(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump({"days": "30", "project": "raydium"}, f)
            self.assertEqual(dune_run.load_params(path), {"days": "30", "project": "raydium"})
        finally:
            os.remove(path)

    def test_non_object_rejected(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump([1, 2, 3], f)
            with self.assertRaises(ValueError):
                dune_run.load_params(path)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
