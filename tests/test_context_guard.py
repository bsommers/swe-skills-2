#!/usr/bin/env python3
"""Tests for scripts/hooks/context_guard.py. Stdlib only: python3 -m unittest discover tests"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "scripts" / "hooks" / "context_guard.py"


def transcript(path, used_tokens, sidechain_after=0):
    """A transcript whose last main-thread assistant turn holds `used_tokens`."""
    recs = [
        {"type": "user", "message": {"role": "user", "content": "hi"}},
        {"type": "assistant", "message": {"usage": {
            "input_tokens": 2,
            "cache_creation_input_tokens": 100,
            "cache_read_input_tokens": used_tokens - 102 - 50,
            "output_tokens": 50,
        }}},
    ]
    for _ in range(sidechain_after):
        recs.append({"type": "assistant", "isSidechain": True, "message": {"usage": {"input_tokens": 999999}}})
    path.write_text("".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8")
    return path


class GuardCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.state = self.dir / "state"
        self.addCleanup(self.tmp.cleanup)

    def run_guard(self, cmd, payload, **env):
        e = dict(os.environ)
        e.pop("SWE_SKILLS_CHECKPOINT_GLOBS", None)
        e["SWE_SKILLS_CONTEXT_GUARD_STATE_DIR"] = str(self.state)
        e["SWE_SKILLS_CONTEXT_LIMIT"] = e.get("SWE_SKILLS_CONTEXT_LIMIT", "200000")
        e.update({k: str(v) for k, v in env.items()})
        return subprocess.run(
            [sys.executable, str(GUARD), cmd], input=json.dumps(payload),
            capture_output=True, text=True, env=e,
        )

    def context(self, used_tokens):
        return transcript(self.dir / "t.jsonl", used_tokens)

    def checkpoint(self, age_seconds=0, body="# Checkpoint\nnext: pytest -q\n"):
        d = self.dir / "docs" / "plans"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "checkpoint.md"
        f.write_text(body, encoding="utf-8")
        if age_seconds:
            old = time.time() - age_seconds
            os.utime(f, (old, old))
        return f

    # ---------------------------------------------------------------- nudge

    def test_nudge_silent_below_threshold(self):
        r = self.run_guard("nudge", {"session_id": "s", "transcript_path": str(self.context(60000)),
                                     "cwd": str(self.dir)})
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "")

    def test_nudge_fires_above_threshold(self):
        r = self.run_guard("nudge", {"session_id": "s", "transcript_path": str(self.context(150000)),
                                     "cwd": str(self.dir)})
        self.assertEqual(r.returncode, 0)
        out = json.loads(r.stdout)["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "UserPromptSubmit")
        self.assertIn("compacting-context-safely", out["additionalContext"])
        self.assertIn("75%", out["additionalContext"])
        self.assertIn("No recent checkpoint", out["additionalContext"])

    def test_nudge_mentions_existing_checkpoint(self):
        self.checkpoint()
        r = self.run_guard("nudge", {"session_id": "s", "transcript_path": str(self.context(150000)),
                                     "cwd": str(self.dir)})
        self.assertIn("update it rather than starting a new one", json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_nudge_throttled_until_next_step(self):
        payload = {"session_id": "s", "transcript_path": str(self.context(150000)), "cwd": str(self.dir)}
        self.assertTrue(self.run_guard("nudge", payload).stdout.strip())
        self.assertEqual(self.run_guard("nudge", payload).stdout.strip(), "", "second nudge at same level")
        payload["transcript_path"] = str(transcript(self.dir / "t2.jsonl", 172000))
        self.assertTrue(self.run_guard("nudge", payload).stdout.strip(), "re-nudges after +10%")

    def test_nudge_ignores_subagent_usage(self):
        t = transcript(self.dir / "t3.jsonl", 60000, sidechain_after=2)
        r = self.run_guard("nudge", {"session_id": "s", "transcript_path": str(t), "cwd": str(self.dir)})
        self.assertEqual(r.stdout.strip(), "")

    # ----------------------------------------------------------- precompact

    def test_precompact_blocks_manual_without_checkpoint(self):
        r = self.run_guard("precompact", {"trigger": "manual", "cwd": str(self.dir)})
        self.assertEqual(r.returncode, 2)
        self.assertIn("Compaction blocked", r.stderr)
        self.assertIn("compacting-context-safely", r.stderr)

    def test_precompact_allows_manual_with_fresh_checkpoint(self):
        self.checkpoint()
        r = self.run_guard("precompact", {"trigger": "manual", "cwd": str(self.dir)})
        self.assertEqual(r.returncode, 0)

    def test_precompact_blocks_on_stale_checkpoint(self):
        self.checkpoint(age_seconds=3600)
        r = self.run_guard("precompact", {"trigger": "manual", "cwd": str(self.dir)})
        self.assertEqual(r.returncode, 2)

    def test_precompact_never_blocks_auto(self):
        r = self.run_guard("precompact", {"trigger": "auto", "cwd": str(self.dir)})
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr.strip(), "")

    def test_precompact_block_can_be_disabled(self):
        r = self.run_guard("precompact", {"trigger": "manual", "cwd": str(self.dir)},
                           SWE_SKILLS_CONTEXT_GUARD_BLOCK=0)
        self.assertEqual(r.returncode, 0)

    # --------------------------------------------------------- sessionstart

    def test_sessionstart_injects_checkpoint_after_compact(self):
        self.checkpoint(body="# Checkpoint\n**Status:** IN PROGRESS\nnext: pytest -q\n")
        r = self.run_guard("sessionstart", {"source": "compact", "cwd": str(self.dir)})
        ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("next: pytest -q", ctx)
        self.assertIn("verify these state claims", ctx)
        self.assertIn("expired", ctx)

    def test_sessionstart_warns_when_no_checkpoint_after_clear(self):
        r = self.run_guard("sessionstart", {"source": "clear", "cwd": str(self.dir)})
        ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("no checkpoint file was found", ctx)

    def test_sessionstart_ignores_stale_checkpoint_on_normal_startup(self):
        self.checkpoint(age_seconds=48 * 3600)
        r = self.run_guard("sessionstart", {"source": "startup", "cwd": str(self.dir)})
        self.assertEqual(r.stdout.strip(), "")

    def test_sessionstart_injects_recent_checkpoint_on_startup(self):
        self.checkpoint()
        r = self.run_guard("sessionstart", {"source": "startup", "cwd": str(self.dir)})
        self.assertIn("recent checkpoint", json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_sessionstart_truncates_long_checkpoint(self):
        self.checkpoint(body="x" * 20000)
        ctx = json.loads(self.run_guard("sessionstart", {"source": "compact", "cwd": str(self.dir)}).stdout)
        self.assertIn("truncated", ctx["hookSpecificOutput"]["additionalContext"])
        self.assertLess(len(ctx["hookSpecificOutput"]["additionalContext"]), 6000)

    # ------------------------------------------------------------ robustness

    def test_missing_transcript_is_silent(self):
        for cmd in ("nudge", "sessionstart"):
            r = self.run_guard(cmd, {"session_id": "s", "transcript_path": str(self.dir / "nope.jsonl"),
                                     "cwd": str(self.dir)})
            self.assertEqual((r.returncode, r.stdout.strip()), (0, ""), cmd)

    def test_truncated_transcript_line_is_tolerated(self):
        t = self.dir / "partial.jsonl"
        t.write_text(json.dumps({"type": "assistant", "message": {"usage": {"input_tokens": 150000}}}) +
                     "\n{\"type\": \"assist", encoding="utf-8")
        r = self.run_guard("nudge", {"session_id": "s", "transcript_path": str(t), "cwd": str(self.dir)})
        self.assertIn("compacting-context-safely", r.stdout)

    def test_garbage_stdin_is_silent(self):
        r = subprocess.run([sys.executable, str(GUARD), "nudge"], input="not json",
                           capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, ""))

    def test_unknown_subcommand_usage(self):
        r = subprocess.run([sys.executable, str(GUARD), "bogus"], input="{}", capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stderr)

    def test_report_prints_usage_and_checkpoint(self):
        self.checkpoint()
        r = self.run_guard("report", {"transcript_path": str(self.context(100000)), "cwd": str(self.dir)})
        self.assertIn("50% of 200000", r.stdout)
        self.assertIn("checkpoint.md", r.stdout)


class InstallerCase(unittest.TestCase):
    """The opt-in installer must be idempotent and must not disturb other settings."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.proj = Path(self.tmp.name)
        self.settings = self.proj / ".claude" / "settings.json"
        self.settings.parent.mkdir(parents=True)
        self.settings.write_text(json.dumps({
            "env": {"KEEP": "me"},
            "hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "echo mine"}]}]},
        }), encoding="utf-8")
        self.addCleanup(self.tmp.cleanup)

    def install(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "hooks" / "install-hooks.py"),
             "--claude", "--project", str(self.proj), *args],
            capture_output=True, text=True)

    def load(self):
        return json.loads(self.settings.read_text(encoding="utf-8"))

    def test_install_is_idempotent_and_reversible(self):
        before = self.load()
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual(self.install().returncode, 0)
        hooks = self.load()["hooks"]
        for event, count in (("UserPromptSubmit", 2), ("PreCompact", 2), ("SessionStart", 4)):
            self.assertEqual(len(hooks[event]), count, event)
        self.install("--uninstall")
        self.assertEqual(self.load(), before, "uninstall restores the original settings")

    def test_session_start_matchers_cover_startup(self):
        """A fresh session must match too, or a checkpoint only resurfaces after a reset."""
        self.install()
        matchers = [g.get("matcher") for g in self.load()["hooks"]["SessionStart"]]
        for m in ("startup", "compact", "clear", "resume"):
            self.assertIn(m, matchers)

    def test_dry_run_changes_nothing(self):
        before = self.settings.read_text(encoding="utf-8")
        r = self.install("--dry-run")
        self.assertIn("DRY:", r.stdout)
        self.assertEqual(self.settings.read_text(encoding="utf-8"), before)

    def test_invalid_settings_json_is_refused(self):
        self.settings.write_text("{not json", encoding="utf-8")
        r = self.install()
        self.assertEqual(r.returncode, 1)
        self.assertIn("not valid JSON", r.stderr)


if __name__ == "__main__":
    unittest.main()
