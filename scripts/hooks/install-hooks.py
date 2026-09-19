#!/usr/bin/env python3
"""Opt-in installer for the context-guard hooks (see docs/HOOKS.md).

Claude Code: merges UserPromptSubmit / PreCompact / SessionStart entries into a
settings.json (user-level by default, or a project's .claude/settings.json).
Antigravity (agy): writes a plugin-root hooks.json with the SessionStart entry
(agy has no PreCompact or UserPromptSubmit) and gitignores it, so installing the
plugin never activates hooks for anyone who did not ask for them.

Usage:
  scripts/hooks/install-hooks.py --claude [--project DIR] [--dry-run] [--uninstall]
  scripts/hooks/install-hooks.py --agy    [--dry-run] [--uninstall]
Stdlib only; idempotent; existing settings are backed up next to the file.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GUARD = ROOT / "scripts" / "hooks" / "context_guard.py"
MARK = "context_guard.py"
AGY_HOOKS = ROOT / "hooks.json"


def entry(cmd):
    return {"type": "command", "command": f"{sys.executable} {GUARD} {cmd}"}


def claude_hooks():
    return {
        "UserPromptSubmit": [{"hooks": [entry("nudge")]}],
        "PreCompact": [{"matcher": "manual", "hooks": [entry("precompact")]},
                       {"matcher": "auto", "hooks": [entry("precompact")]}],
        "SessionStart": [{"matcher": "compact", "hooks": [entry("sessionstart")]},
                         {"matcher": "clear", "hooks": [entry("sessionstart")]},
                         {"matcher": "resume", "hooks": [entry("sessionstart")]}],
    }


def agy_hooks():
    return {"hooks": {"SessionStart": [{"hooks": [entry("sessionstart")]}]}}


def strip_ours(groups):
    """Drop only the groups this installer added; leave the user's own hooks alone."""
    kept = []
    for g in groups:
        hooks = [h for h in g.get("hooks", []) if MARK not in str(h.get("command", ""))]
        if hooks:
            kept.append({**g, "hooks": hooks})
        elif not g.get("hooks"):
            kept.append(g)
    return kept


def install_claude(path, uninstall, dry):
    settings = {}
    if path.exists():
        try:
            settings = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            print(f"error: {path} is not valid JSON; fix it first", file=sys.stderr)
            return 1
    hooks = settings.get("hooks") or {}
    for event, groups in claude_hooks().items():
        existing = strip_ours(hooks.get(event) or [])
        hooks[event] = existing if uninstall else existing + groups
        if not hooks[event]:
            hooks.pop(event)
    if hooks:
        settings["hooks"] = hooks
    else:
        settings.pop("hooks", None)
    body = json.dumps(settings, indent=2) + "\n"
    verb = "uninstall from" if uninstall else "install into"
    if dry:
        print(f"DRY: would {verb} {path}:\n{body}")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    path.write_text(body, encoding="utf-8")
    print(f"{'removed context-guard hooks from' if uninstall else 'wrote context-guard hooks to'} {path}")
    return 0


def install_agy(uninstall, dry):
    gitignore = ROOT / ".gitignore"
    line = "/hooks.json\n"
    if uninstall:
        if dry:
            print(f"DRY: would remove {AGY_HOOKS}")
        elif AGY_HOOKS.exists():
            AGY_HOOKS.unlink()
            print(f"removed {AGY_HOOKS}")
        return 0
    body = json.dumps(agy_hooks(), indent=2) + "\n"
    if dry:
        print(f"DRY: would write {AGY_HOOKS}:\n{body}")
        return 0
    AGY_HOOKS.write_text(body, encoding="utf-8")
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if line.strip() not in [l.strip() for l in current.splitlines()]:
        gitignore.write_text(current + ("" if current.endswith("\n") or not current else "\n") + line, encoding="utf-8")
    print(f"wrote {AGY_HOOKS} (gitignored; agy loads a plugin's hooks from its root)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claude", action="store_true", help="install into Claude Code settings.json")
    ap.add_argument("--agy", action="store_true", help="install into the Antigravity plugin root")
    ap.add_argument("--project", metavar="DIR", help="project-level instead of user-level (Claude Code)")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not (a.claude or a.agy):
        ap.error("choose --claude and/or --agy")
    rc = 0
    if a.claude:
        path = Path(a.project).expanduser() / ".claude" / "settings.json" if a.project \
            else Path.home() / ".claude" / "settings.json"
        rc |= install_claude(path, a.uninstall, a.dry_run)
    if a.agy:
        rc |= install_agy(a.uninstall, a.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
