#!/usr/bin/env python3
"""Tests for scripts/hooks/git_pre_commit.py. Stdlib only: python3 -m unittest discover tests"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "scripts" / "hooks" / "git_pre_commit.py"
INSTALLER = ROOT / "scripts" / "hooks" / "install-hooks.py"


class TestGitPreCommit(unittest.TestCase):
    def test_absolute_path_detected(self):
        """Pre-commit guard must flag absolute home paths in staged skill or doc files."""
        with tempfile.TemporaryDirectory() as tmp:
            bad_file = Path(tmp) / "SKILL.md"
            bad_file.write_text("Reference to /home/bill/secrets in skill.\n", encoding="utf-8")
            cmd = [sys.executable, str(GUARD), str(bad_file)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("absolute home path", proc.stdout + proc.stderr)

    def test_clean_file_passes(self):
        """Clean files must pass without errors."""
        with tempfile.TemporaryDirectory() as tmp:
            clean_file = Path(tmp) / "test.md"
            clean_file.write_text("Everything is relative and clean.\n", encoding="utf-8")
            cmd = [sys.executable, str(GUARD), str(clean_file)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)

    def test_version_manifest_mismatch_detected(self):
        """Mismatched versions across plugin manifests must be flagged."""
        sys.path.insert(0, str(ROOT / "scripts" / "hooks"))
        try:
            import importlib
            mod = importlib.import_module("git_pre_commit")
            manifests = {
                "plugin.json": json.dumps({"version": "0.1.0"}),
                ".claude-plugin/plugin.json": json.dumps({"version": "0.2.0"}),
            }
            errors = mod.check_manifest_versions_from_data(manifests)
            self.assertTrue(len(errors) > 0)
            self.assertIn("mismatch", errors[0].lower())
        finally:
            sys.path.pop(0)

    def test_install_git_hook_dry_run(self):
        """install-hooks.py --git --dry-run must preview installation."""
        cmd = [sys.executable, str(INSTALLER), "--git", "--dry-run"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("DRY:", proc.stdout)
        self.assertIn("pre-commit", proc.stdout)


if __name__ == "__main__":
    unittest.main()
