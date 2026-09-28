#!/usr/bin/env python3
"""Tests for scripts/hooks/model_router.py. Stdlib only: python3 -m unittest discover tests"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTER = ROOT / "scripts" / "hooks" / "model_router.py"


class ModelRouterCase(unittest.TestCase):
    def run_router(self, mode, payload=None, **env):
        e = dict(os.environ)
        e.update({k: str(v) for k, v in env.items()})
        inp = json.dumps(payload) if payload is not None else ""
        return subprocess.run(
            [sys.executable, str(ROUTER), mode],
            input=inp,
            capture_output=True,
            text=True,
            env=e,
        )

    def test_evaluate_high_complexity(self):
        r = self.run_router(
            "evaluate",
            {"role": "Reviewer", "prompt": "Audit architecture for concurrency deadlocks and race conditions"},
        )
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["tier"], "pro")

    def test_evaluate_sensitive_files(self):
        r = self.run_router(
            "evaluate",
            {"role": "Coder", "prompt": "Update logic", "files": ["src/auth/session.ts"]},
        )
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["tier"], "pro")

    def test_evaluate_low_complexity(self):
        r = self.run_router(
            "evaluate",
            {"role": "Worker", "prompt": "Format code, fix typos in docs, and sync readme"},
        )
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["tier"], "flash_lite")

    def test_evaluate_default_baseline(self):
        r = self.run_router(
            "evaluate",
            {"role": "Worker", "prompt": "Write helper utility function to add numbers"},
        )
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["tier"], "flash")

    def test_pretooluse_overwrites_subagent_to_pro(self):
        payload = {
            "toolCall": {
                "name": "invoke_subagent",
                "args": {
                    "Subagents": [
                        {
                            "Role": "Architect",
                            "Prompt": "Perform security audit on token verification",
                            "Model": "inherit",
                        }
                    ]
                },
            }
        }
        r = self.run_router("pretooluse", payload)
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["decision"], "allow")
        self.assertIn("overwrite", data)
        sub = data["overwrite"]["Subagents"][0]
        self.assertEqual(sub["Model"], "pro")

    def test_pretooluse_overwrites_subagent_to_lite(self):
        payload = {
            "toolCall": {
                "name": "invoke_subagent",
                "args": {
                    "Subagents": [
                        {
                            "Role": "Formatter",
                            "Prompt": "Run linter and fix formatting errors",
                            "Model": "inherit",
                        }
                    ]
                },
            }
        }
        r = self.run_router("pretooluse", payload)
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["decision"], "allow")
        self.assertIn("overwrite", data)
        sub = data["overwrite"]["Subagents"][0]
        self.assertEqual(sub["Model"], "flash_lite")

    def test_pretooluse_ignores_non_subagent_tools(self):
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "npm test"},
            }
        }
        r = self.run_router("pretooluse", payload)
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data, {"decision": "allow"})

    def test_preinvocation_injects_hint_for_complex_tasks(self):
        payload = {"userPrompt": "We need to architect a distributed consensus engine with fault tolerance"}
        r = self.run_router("preinvocation", payload)
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertIn("injectSteps", data)
        self.assertTrue(len(data["injectSteps"]) > 0)
        self.assertIn("ephemeralMessage", data["injectSteps"][0])

    def test_preinvocation_noop_for_simple_tasks(self):
        payload = {"userPrompt": "Fix typo in line 12 of README"}
        r = self.run_router("preinvocation", payload)
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data, {})

    def test_disabled_env_var(self):
        payload = {
            "toolCall": {
                "name": "invoke_subagent",
                "args": {
                    "Subagents": [
                        {
                            "Role": "Architect",
                            "Prompt": "Perform security audit",
                            "Model": "inherit",
                        }
                    ]
                },
            }
        }
        r = self.run_router("pretooluse", payload, SWE_SKILLS_MODEL_ROUTER_ENABLED="0")
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data, {"decision": "allow"})
        self.assertNotIn("overwrite", data)

    def test_resilience_on_invalid_input(self):
        proc = subprocess.run(
            [sys.executable, str(ROUTER), "pretooluse"],
            input="invalid { json",
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data, {"decision": "allow"})


if __name__ == "__main__":
    unittest.main()
