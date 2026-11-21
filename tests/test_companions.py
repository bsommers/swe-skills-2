"""Tests for companions.json (schema, pinning), its lint check, and install.sh --companion."""
import copy
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = ROOT / "scripts" / "install.sh"
spec = importlib.util.spec_from_file_location("lint_skills", ROOT / "scripts" / "lint-skills.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

DATA = json.loads((ROOT / "companions.json").read_text(encoding="utf-8"))


def trigger_match(companion, task):
    low = task.lower()
    return any(t.lower() in low for t in companion["triggers"])


def detected(companion, home):
    return any(Path(p.replace("~", str(home), 1)).exists() for p in companion["detect"])


class TestCompanionsFile(unittest.TestCase):
    def _check(self, data):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "companions.json").write_text(json.dumps(data), encoding="utf-8")
            return lint.check_companions(Path(d))

    def test_repo_file_is_valid(self):
        self.assertEqual(lint.check_companions(ROOT), [])

    def test_security_skills_pinned(self):
        c = DATA["companions"][0]
        self.assertEqual(c["id"], "security-skills")
        self.assertEqual(c["repo"], "https://github.com/bsommers/security-skills")
        self.assertEqual(c["ref"], "v1.0.0")
        self.assertIn("--branch v1.0.0", c["install"])

    def test_unpinned_ref_rejected(self):
        bad = copy.deepcopy(DATA)
        bad["companions"][0]["ref"] = "main"
        self.assertTrue(any("pinned" in e for e in self._check(bad)))

    def test_install_ref_mismatch_rejected(self):
        bad = copy.deepcopy(DATA)
        bad["companions"][0]["install"] = bad["companions"][0]["install"].replace("v1.0.0", "main")
        self.assertTrue(any("--branch" in e for e in self._check(bad)))

    def test_ssh_and_piped_install_rejected(self):
        for repo_cmd in ("git@github.com:bsommers/security-skills", "x | sh"):
            bad = copy.deepcopy(DATA)
            c = bad["companions"][0]
            c["install"] = c["install"] + " ; " + repo_cmd
            self.assertTrue(self._check(bad), repo_cmd)

    def test_non_https_repo_rejected(self):
        bad = copy.deepcopy(DATA)
        bad["companions"][0]["repo"] = "git@github.com:bsommers/security-skills"
        self.assertTrue(any("repo" in e for e in self._check(bad)))

    def test_duplicate_id_rejected(self):
        bad = copy.deepcopy(DATA)
        bad["companions"].append(copy.deepcopy(bad["companions"][0]))
        self.assertTrue(any("duplicate" in e for e in self._check(bad)))

    def test_unknown_key_rejected(self):
        bad = copy.deepcopy(DATA)
        bad["companions"][0]["extra"] = 1
        self.assertTrue(self._check(bad))

    def test_detect_must_be_home_relative(self):
        bad = copy.deepcopy(DATA)
        bad["companions"][0]["detect"] = ["/etc/passwd"]
        self.assertTrue(any("detect" in e for e in self._check(bad)))


class TestMatching(unittest.TestCase):
    c = DATA["companions"][0]

    def test_positive_triggers(self):
        for task in ("fix this CVE-2026-1234", "OWASP review of login", "remediate the findings"):
            self.assertTrue(trigger_match(self.c, task), task)

    def test_negative_triggers(self):
        for task in ("rename a variable", "write release notes"):
            self.assertFalse(trigger_match(self.c, task), task)

    def test_detect_expansion(self):
        with tempfile.TemporaryDirectory() as home:
            self.assertFalse(detected(self.c, home))
            p = Path(home) / ".claude/skills/security-scan"
            p.mkdir(parents=True)
            (p / "SKILL.md").write_text("x")
            self.assertTrue(detected(self.c, home))


class TestInstallerCompanion(unittest.TestCase):
    def _run(self, *args, stdin=subprocess.DEVNULL):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home)
            r = subprocess.run(["bash", str(INSTALL), *args], capture_output=True, text=True,
                               stdin=stdin, env=env, timeout=30)
            return r, sorted(os.listdir(home))

    def test_non_tty_prints_command_and_never_runs(self):
        r, left = self._run("--companion", "security-skills")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("git clone --depth 1 --branch v1.0.0", r.stdout)
        self.assertIn("Not running it", r.stdout)
        self.assertEqual(left, [])

    def test_yes_on_piped_stdin_does_not_install(self):
        r = subprocess.run(["bash", str(INSTALL), "--companion", "security-skills"], input="y\n",
                           capture_output=True, text=True, env=dict(os.environ, HOME="/nonexistent"),
                           timeout=30)
        self.assertEqual(r.returncode, 0)
        self.assertIn("Not running it", r.stdout)

    def test_unknown_companion_fails(self):
        r, _ = self._run("--companion", "nope")
        self.assertEqual(r.returncode, 2)

    def test_missing_id_fails(self):
        r, _ = self._run("--companion")
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
