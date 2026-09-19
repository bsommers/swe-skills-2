#!/usr/bin/env python3
"""Tests for scripts/run-scenarios.py. Stdlib only: python3 -m unittest discover tests"""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_SCRIPT = ROOT / "scripts" / "run-scenarios.py"


class TestRunScenarios(unittest.TestCase):
    def test_dry_run_passes(self):
        """scripts/run-scenarios.py --dry-run must exit 0 and find all scenarios."""
        proc = subprocess.run([sys.executable, str(SCENARIOS_SCRIPT), "--dry-run"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Error: {proc.stderr}")
        self.assertIn("OK: All", proc.stdout)

    def test_list_and_json_output(self):
        """scripts/run-scenarios.py --json must produce valid JSON with expected keys."""
        import json
        proc = subprocess.run([sys.executable, str(SCENARIOS_SCRIPT), "--json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertTrue(len(data) >= 38)
        self.assertIn("skill", data[0])
        self.assertIn("prompt", data[0])
        self.assertIn("pass_criterion", data[0])


if __name__ == "__main__":
    unittest.main()
