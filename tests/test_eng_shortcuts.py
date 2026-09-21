#!/usr/bin/env python3
"""Tests for the /eng shortcut table checked by scripts/lint-skills.py. Stdlib only: python3 -m unittest discover tests"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def lint_with_eng_edit(edit):
    """Copy skills/ and the linter to a temp tree, apply edit(text) to the eng skill, and lint that tree."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copytree(ROOT / "skills", tmp / "skills")
        (tmp / "scripts").mkdir()
        shutil.copy(ROOT / "scripts" / "lint-skills.py", tmp / "scripts" / "lint-skills.py")
        eng = tmp / "skills" / "eng" / "SKILL.md"
        eng.write_text(edit(eng.read_text(encoding="utf-8")), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(tmp / "scripts" / "lint-skills.py")], capture_output=True, text=True
        )


class TestSweShortcuts(unittest.TestCase):
    def test_repo_shortcuts_are_clean(self):
        proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "lint-skills.py")], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_unknown_target_is_an_error(self):
        proc = lint_with_eng_edit(lambda t: t.replace("| `pr` | `writing-pull-requests` |", "| `pr` | `writing-pull-request` |"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("targets unknown skill `writing-pull-request`", proc.stdout)

    def test_shortcut_shadowing_a_skill_name_is_an_error(self):
        proc = lint_with_eng_edit(lambda t: t.replace("| `pr` |", "| `pr`, `right-sizing-process` |"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("shortcut `right-sizing-process` shadows a skill name", proc.stdout)

    def test_duplicate_shortcut_is_an_error(self):
        proc = lint_with_eng_edit(lambda t: t.replace("| `pr` |", "| `pr`, `review` |"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("shortcut `review` is defined twice", proc.stdout)


if __name__ == "__main__":
    unittest.main()
