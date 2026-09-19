#!/usr/bin/env python3
"""Unit tests for scripts/eval-router.py. Stdlib only: python3 -m unittest discover tests"""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_ROUTER = ROOT / "scripts" / "eval-router.py"


class TestEvalRouter(unittest.TestCase):
    def test_benchmark_cases_count(self):
        """Benchmark must define exactly 10 diverse cases per docs/TESTING.md."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import importlib
            mod = importlib.import_module("eval-router")
            cases = mod.BENCHMARK_CASES
            self.assertEqual(len(cases), 10)
            scales = {c["scale"] for c in cases}
            self.assertTrue({"Tool", "App", "System"}.issubset(scales))
        finally:
            sys.path.pop(0)

    def test_scoring_logic_pass_and_fail(self):
        """Scoring checks constraints: 1-3 skills expected, <= 4 skills max."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import importlib
            mod = importlib.import_module("eval-router")
            case = {
                "id": "test_case",
                "prompt": "build a small CLI tool",
                "scale": "Tool",
                "expected": ["building-small-cli-tools"],
            }
            # Perfect match (1-3 skills) -> Pass
            res_pass = mod.score_prediction(case, ["building-small-cli-tools"])
            self.assertTrue(res_pass["passed"])

            # Over-budget (> 4 skills) -> Fail
            res_too_many = mod.score_prediction(
                case,
                ["building-small-cli-tools", "scaffolding-new-projects", "right-sizing-process", "choosing-tools-and-substrates", "planning-with-contracts"]
            )
            self.assertFalse(res_too_many["passed"])
            self.assertIn("exceeds max limit", res_too_many["reason"])

            # Missing expected skill -> Fail
            res_missing = mod.score_prediction(case, ["choosing-tools-and-substrates"])
            self.assertFalse(res_missing["passed"])
            self.assertIn("missing", res_missing["reason"])
        finally:
            sys.path.pop(0)

    def test_cli_self_test(self):
        """CLI execution in --self-test mode must achieve >= 80% accuracy and exit 0."""
        cmd = [sys.executable, str(EVAL_ROUTER), "--self-test"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        self.assertIn("Accuracy:", proc.stdout)
        self.assertIn("PASS", proc.stdout)


if __name__ == "__main__":
    unittest.main()
