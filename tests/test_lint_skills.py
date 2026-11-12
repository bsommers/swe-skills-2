"""Tests for scripts/lint-skills.py word limits and documentation coverage checks."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = ROOT / "scripts" / "lint-skills.py"

SOFT = 900
HARD = int(SOFT * 1.15)


def _skill(name, words):
    body = " ".join(["word"] * words)
    return (
        f"---\nname: {name}\n"
        f"description: Use when testing the linter with the {name} fixture.\n---\n\n{body}\n"
    )


class TestLintSkills(unittest.TestCase):
    def _make_tree(self, root, alpha_words=100, omit_from=()):
        """Build a minimal repo: router + one skill `alpha-skill`, plus coverage docs."""
        skills = root / "skills"
        (skills / "alpha-skill").mkdir(parents=True)
        (skills / "using-swe-skills").mkdir()
        (skills / "alpha-skill" / "SKILL.md").write_text(_skill("alpha-skill", alpha_words), encoding="utf-8")
        router = _skill("using-swe-skills", 20) + "\nRoutes to `alpha-skill`.\n"
        (skills / "using-swe-skills" / "SKILL.md").write_text(router, encoding="utf-8")
        (root / "docs").mkdir()
        listing = "| `using-swe-skills` |\n| `alpha-skill` |\n"
        for doc in ("README.md", "docs/EVIDENCE.md", "docs/TESTING.md"):
            text = listing.replace("| `alpha-skill` |\n", "") if doc in omit_from else listing
            (root / doc).write_text(text, encoding="utf-8")

    def _lint(self, root):
        return subprocess.run(
            [sys.executable, str(LINT), "--root", str(root)],
            capture_output=True, text=True,
        )

    def test_clean_tree_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp))
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertNotIn("WARN", proc.stdout)

    def test_over_soft_limit_warns_but_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp), alpha_words=SOFT + 1)
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertIn("WARN  alpha-skill", proc.stdout)
            self.assertIn("soft limit", proc.stdout)

    def test_at_hard_limit_still_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp), alpha_words=HARD)
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_over_hard_limit_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp), alpha_words=HARD + 1)
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("ERROR alpha-skill", proc.stdout)
            self.assertIn("hard limit", proc.stdout)

    def test_skill_missing_from_each_coverage_doc_fails(self):
        for doc in ("README.md", "docs/EVIDENCE.md", "docs/TESTING.md"):
            with self.subTest(doc=doc), tempfile.TemporaryDirectory() as tmp:
                self._make_tree(Path(tmp), omit_from=(doc,))
                proc = self._lint(Path(tmp))
                self.assertEqual(proc.returncode, 1, proc.stdout)
                self.assertIn(f"coverage: {doc} does not mention `alpha-skill`", proc.stdout)

    def test_missing_coverage_doc_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp))
            (Path(tmp) / "docs" / "TESTING.md").unlink()
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("coverage: docs/TESTING.md is missing", proc.stdout)


    def _write_manifests(self, root, versions):
        (root / ".claude-plugin").mkdir(exist_ok=True)
        (root / ".cursor-plugin").mkdir(exist_ok=True)
        top, claude, cursor, market = versions
        (root / "plugin.json").write_text(json.dumps({"version": top}), encoding="utf-8")
        (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"version": claude}), encoding="utf-8")
        (root / ".cursor-plugin" / "plugin.json").write_text(json.dumps({"version": cursor}), encoding="utf-8")
        (root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps({"plugins": [{"name": "swe-skills", "version": market}]}), encoding="utf-8")

    def test_matching_manifest_versions_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp))
            self._write_manifests(Path(tmp), ("1.2.3",) * 4)
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_any_mismatched_manifest_version_fails(self):
        for i in range(4):
            versions = ["1.2.3"] * 4
            versions[i] = "1.2.4"
            with self.subTest(index=i), tempfile.TemporaryDirectory() as tmp:
                self._make_tree(Path(tmp))
                self._write_manifests(Path(tmp), versions)
                proc = self._lint(Path(tmp))
                self.assertEqual(proc.returncode, 1, proc.stdout)
                self.assertIn("manifests: versions differ", proc.stdout)

    def test_invalid_manifest_json_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_tree(Path(tmp))
            (Path(tmp) / "plugin.json").write_text("{not json", encoding="utf-8")
            proc = self._lint(Path(tmp))
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("manifests: invalid JSON", proc.stdout)


if __name__ == "__main__":
    unittest.main()
