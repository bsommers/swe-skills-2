#!/usr/bin/env python3
"""Tests for designing-exhaustive-test-cases skill and pre-build/post-build test suite integration."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NEW_SKILL_DIR = SKILLS_DIR / "designing-exhaustive-test-cases"
NEW_SKILL_MD = NEW_SKILL_DIR / "SKILL.md"
NEW_SKILL_TEMPLATE = NEW_SKILL_DIR / "references" / "test-matrix-template.md"


class TestExhaustiveTestDesignSkill(unittest.TestCase):
    def test_skill_and_reference_template_exist(self):
        """designing-exhaustive-test-cases SKILL.md and reference matrix template must exist."""
        self.assertTrue(NEW_SKILL_MD.is_file(), f"Missing {NEW_SKILL_MD}")
        self.assertTrue(NEW_SKILL_TEMPLATE.is_file(), f"Missing {NEW_SKILL_TEMPLATE}")

    def test_skill_covers_pre_build_dimensions_and_post_build_suite(self):
        """Skill must mandate pre-build exhaustive matrix design, 8-tier mapping, RED-first, and post-build suite execution."""
        text = NEW_SKILL_MD.read_text(encoding="utf-8")
        required_terms = [
            "name: designing-exhaustive-test-cases",
            "Use when",
            "Happy path",
            "Boundary",
            "Negative",
            "Idempotency",
            "Dependency failure",
            "smoke",
            "unit",
            "integration",
            "system",
            "perf",
            "stress",
            "torture",
            "security",
            "scripts/verify.sh",
            "`planning-with-contracts`",
            "`layered-verification-gates`",
            "`test-coverage`",
            "`hunting-silent-failures`",
            "`designing-testable-seams`",
        ]
        for term in required_terms:
            self.assertIn(term, text, f"Missing required concept {term!r} in designing-exhaustive-test-cases/SKILL.md")

    def test_reference_template_has_exhaustive_matrix_and_suite_checklist(self):
        """Reference template must provide a concrete pre-build test matrix table and post-build suite checklist."""
        text = NEW_SKILL_TEMPLATE.read_text(encoding="utf-8")
        for section in (
            "Pre-Build Exhaustive Test Matrix",
            "Happy Path",
            "Boundary & Equivalence",
            "Negative, Malformed & Adversarial",
            "Idempotency, Concurrency & State",
            "Dependency & Fault Injection",
            "Post-Build Suite Integration Checklist",
            "scripts/verify.sh",
        ):
            self.assertIn(section, text, f"Missing {section!r} in references/test-matrix-template.md")

    def test_cross_skill_integration_in_planning_verification_and_coverage(self):
        """planning-with-contracts, layered-verification-gates, and test-coverage must enforce designing-exhaustive-test-cases."""
        plan_skill = (SKILLS_DIR / "planning-with-contracts" / "SKILL.md").read_text(encoding="utf-8")
        plan_tmpl = (SKILLS_DIR / "planning-with-contracts" / "references" / "plan-template.md").read_text(encoding="utf-8")
        gates_skill = (SKILLS_DIR / "layered-verification-gates" / "SKILL.md").read_text(encoding="utf-8")
        cov_skill = (SKILLS_DIR / "test-coverage" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("`designing-exhaustive-test-cases`", plan_skill)
        self.assertIn("Exhaustive Test Matrix", plan_tmpl)
        self.assertIn("`designing-exhaustive-test-cases`", gates_skill)
        self.assertIn("`designing-exhaustive-test-cases`", cov_skill)

    def test_router_eng_installer_and_docs_sync(self):
        """Router, /eng shortcuts, install.sh profiles, README, EVIDENCE, and TESTING must include designing-exhaustive-test-cases."""
        router = (SKILLS_DIR / "using-swe-skills" / "SKILL.md").read_text(encoding="utf-8")
        eng = (SKILLS_DIR / "eng" / "SKILL.md").read_text(encoding="utf-8")
        install_sh = (ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        evidence = (ROOT / "docs" / "EVIDENCE.md").read_text(encoding="utf-8")
        testing = (ROOT / "docs" / "TESTING.md").read_text(encoding="utf-8")

        self.assertIn("`designing-exhaustive-test-cases`", router)
        self.assertIn("`designing-exhaustive-test-cases`", eng)
        self.assertIn("designing-exhaustive-test-cases", install_sh)
        self.assertIn("`designing-exhaustive-test-cases`", readme)
        self.assertIn("`designing-exhaustive-test-cases`", evidence)
        self.assertIn("`designing-exhaustive-test-cases`", testing)

    def test_router_routes_exhaustive_test_design_prompts(self):
        """eval-router must route pre-build exhaustive test case prompts to designing-exhaustive-test-cases."""
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import importlib
            mod = importlib.import_module("eval-router")
            rules = mod.load_router_rules()
            predicted = mod.route_prompt(
                "Design exhaustive test cases for the new feature before build time and add them to the test suite.",
                rules=rules,
            )
            self.assertIn("designing-exhaustive-test-cases", predicted)
        finally:
            sys.path.pop(0)

    def test_lint_skills_zero_errors_and_zero_warnings(self):
        """scripts/lint-skills.py --words must exit 0 with zero warnings and zero errors."""
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "lint-skills.py"), "--words"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertNotIn("WARN", proc.stdout)
        self.assertNotIn("ERROR", proc.stdout)


class TestTriOSCoverageAndDriverArchitecture(unittest.TestCase):
    def test_driver_architecture_skill_and_reference_support_windows_macos_linux(self):
        """designing-plugin-contracts and its reference must specify Windows, macOS, and Linux driver architecture."""
        driver_skill = (SKILLS_DIR / "designing-plugin-contracts" / "SKILL.md").read_text(encoding="utf-8")
        driver_ref_path = SKILLS_DIR / "designing-plugin-contracts" / "references" / "cross-platform-driver-architecture.md"
        self.assertTrue(driver_ref_path.is_file(), f"Missing {driver_ref_path}")
        driver_ref = driver_ref_path.read_text(encoding="utf-8")

        for os_name in ("Windows", "macOS", "Linux"):
            self.assertIn(os_name, driver_skill, f"Missing {os_name} in designing-plugin-contracts/SKILL.md")
            self.assertIn(os_name, driver_ref, f"Missing {os_name} in cross-platform-driver-architecture.md")

        for concept in ("ConPTY", "Named Pipe", "Unix domain socket", "APPDATA", "XDG_CONFIG_HOME", "Library/Application Support"):
            self.assertIn(concept, driver_ref, f"Missing {concept!r} in cross-platform-driver-architecture.md")

    def test_test_coverage_supports_windows_macos_linux(self):
        """test-coverage skill, tool matrix, and report template must cover Windows, macOS, and Linux."""
        cov_skill = (SKILLS_DIR / "test-coverage" / "SKILL.md").read_text(encoding="utf-8")
        cov_matrix = (SKILLS_DIR / "test-coverage" / "references" / "COVERAGE_TOOLS_MATRIX.md").read_text(encoding="utf-8")
        cov_template = (SKILLS_DIR / "test-coverage" / "templates" / "COVERAGE_REPORT_TEMPLATE.md").read_text(encoding="utf-8")

        for os_name in ("Windows", "macOS", "Linux"):
            self.assertIn(os_name, cov_skill, f"Missing {os_name} in test-coverage/SKILL.md")
            self.assertIn(os_name, cov_matrix, f"Missing {os_name} in COVERAGE_TOOLS_MATRIX.md")
            self.assertIn(os_name, cov_template, f"Missing {os_name} in COVERAGE_REPORT_TEMPLATE.md")

    def test_verify_sh_template_is_portable_across_macos_linux_windows(self):
        """verify.sh.template must not use Bash-4-only mapfile or GNU-gawk-only gensub."""
        verify_tmpl = (SKILLS_DIR / "layered-verification-gates" / "verify.sh.template").read_text(encoding="utf-8")
        self.assertNotIn("mapfile", verify_tmpl, "verify.sh.template must not use Bash 4+ mapfile (breaks macOS Bash 3.2)")
        self.assertNotIn("gensub(", verify_tmpl, "verify.sh.template must not use GNU-awk-only gensub (breaks macOS BSD awk)")

    def test_shell_function_reachability_handles_crlf_and_runs_cleanly(self):
        """shell_function_reachability.sh must handle CRLF (Windows) and LF (macOS/Linux) shell files."""
        import tempfile
        reach_script = SKILLS_DIR / "test-coverage" / "scripts" / "shell_function_reachability.sh"
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            lib_dir = tmp_path / "lib"
            test_dir = tmp_path / "tests"
            lib_dir.mkdir()
            test_dir.mkdir()
            # Write lib and test files with Windows CRLF line endings
            (lib_dir / "driver.sh").write_bytes(
                b"#!/usr/bin/env bash\r\ninit_driver() {\r\n  echo ok\r\n}\r\nunused_helper() {\r\n  echo no\r\n}\r\n"
            )
            (test_dir / "test_driver.bats").write_bytes(
                b"@test 'driver init' {\r\n  run init_driver\r\n}\r\n"
            )
            proc = subprocess.run(
                ["bash", str(reach_script), str(lib_dir), "--", str(test_dir)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("Functions defined     : 2", proc.stdout)
            self.assertIn("Referenced in tests   : 1", proc.stdout)
            self.assertIn("UNREACHED (0 refs)    : 1", proc.stdout)
            self.assertIn("unused_helper", proc.stdout)


if __name__ == "__main__":
    unittest.main()
