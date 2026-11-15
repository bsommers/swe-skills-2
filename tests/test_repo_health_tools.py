#!/usr/bin/env python3
"""Tests for detect-harness, review-kickoff and doc-claims. Stdlib only: python3 -m unittest discover tests"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


detect = load("detect-harness")
kickoff = load("review-kickoff")
claims = load("doc-claims")


class TestDetectHarness(unittest.TestCase):
    def test_override_wins(self):
        self.assertEqual(detect.detect({"SWE_HARNESS": "pi", "CLAUDECODE": "1"}, [])[0], "pi")

    def test_bad_override_is_unknown_not_a_guess(self):
        self.assertEqual(detect.detect({"SWE_HARNESS": "vim", "CLAUDECODE": "1"}, [])[0], "unknown")

    def test_env_var(self):
        self.assertEqual(detect.detect({"CLAUDECODE": "1"}, [])[0], "claude")

    def test_ancestor_process(self):
        self.assertEqual(detect.detect({}, ["bash", "opencode", "systemd"])[0], "opencode")

    def test_unknown(self):
        r = detect.report({}, ["bash"])
        self.assertEqual((r["harness"], r["subagents"]), ("unknown", "unknown"))

    def test_pi_has_no_subagents(self):
        self.assertEqual(detect.report({"SWE_HARNESS": "pi"}, [])["subagents"], "no")

    def test_every_harness_has_three_tiers(self):
        for h, (_, _, _, tiers) in detect.HARNESSES.items():
            self.assertEqual(set(tiers), {"fast", "standard", "frontier"}, h)


class TestKickoff(unittest.TestCase):
    def run_kickoff(self, root, *extra):
        return kickoff.main(["--root", str(root), "--date", "2000-01-01", "--goal", "g", *extra])

    def test_creates_workspace_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(self.run_kickoff(t), 0)
            out = Path(t) / "docs/reviews/2000-01-01"
            self.assertTrue((out / "REVIEW.md").exists())
            self.assertEqual(len(list((out / "prompts").glob("*.md"))), len(kickoff.LENSES))
            (out / "REVIEW.md").write_text("mine", encoding="utf-8")
            self.run_kickoff(t)
            self.assertEqual((out / "REVIEW.md").read_text(encoding="utf-8"), "mine")

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            self.run_kickoff(t, "--dry-run")
            self.assertFalse((Path(t) / "docs").exists())

    def test_lens_subset_and_unknown_lens(self):
        with tempfile.TemporaryDirectory() as t:
            self.run_kickoff(t, "--lenses", "security")
            self.assertEqual(len(list((Path(t) / "docs/reviews/2000-01-01/prompts").glob("*.md"))), 1)
            self.assertEqual(self.run_kickoff(t, "--lenses", "nope"), 2)


class TestDocClaims(unittest.TestCase):
    def test_finds_broken_link_path_and_count(self):
        with tempfile.TemporaryDirectory() as t:
            r = Path(t)
            (r / "skills" / "a").mkdir(parents=True)
            for n in "bcdef":
                (r / "skills" / n).mkdir()
            (r / "real.md").write_text("x", encoding="utf-8")
            (r / "README.md").write_text(
                "See [ok](real.md) and [bad](gone.md). Path `docs/gone.py` and `real.md`.\n"
                "We ship 9 skills.\n```\n`docs/ignored.py`\n```\n", encoding="utf-8")
            broken, counts = claims.scan(r)
            kinds = {(k, t) for _, _, k, t in broken}
            self.assertIn(("link", "gone.md"), kinds)
            self.assertIn(("path", "docs/gone.py"), kinds)
            self.assertNotIn(("link", "real.md"), kinds)
            self.assertFalse(any("ignored" in t for _, t in kinds))
            self.assertEqual(len(counts), 1)

    def test_cli_exit_code(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "README.md").write_text("[x](nope.md)", encoding="utf-8")
            p = subprocess.run([sys.executable, str(ROOT / "scripts/doc-claims.py"), t], capture_output=True, text=True)
            self.assertEqual(p.returncode, 1)


if __name__ == "__main__":
    unittest.main()
