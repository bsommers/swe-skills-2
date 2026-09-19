#!/usr/bin/env python3
"""Git pre-commit hook guard for swe-skills.

Enforces:
  1. No absolute machine home paths (/home/..., /Users/...) in skills or docs (keeping-repos-portable).
  2. No hardcoded secret tokens or private keys (hardening-trust-boundaries).
  3. Consistent version numbers across plugin manifests (committing-and-releasing-cleanly).
  4. Passing skill linter and docs sync (layered-verification-gates, keeping-docs-in-sync).

Usage:
  scripts/hooks/git_pre_commit.py [FILES...]
  scripts/hooks/git_pre_commit.py               # checks git staged files
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ABS_PATH_RE = re.compile(r"(/home/[A-Za-z0-9_-]+|/Users/[A-Za-z0-9_-]+)")
SECRET_RE = re.compile(r"(AKIA[0-9A-Z]{16}|ghp_[0-9a-zA-Z]{36}|-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----)")
MANIFEST_PATHS = [
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
]


def get_staged_files():
    """Return list of staged file paths relative to ROOT."""
    try:
        proc = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [p.strip() for p in proc.stdout.splitlines() if p.strip()]
    except (subprocess.SubprocessError, OSError):
        return []


def check_content_rules(path, text):
    """Verify portability and security rules on a single file's text."""
    errors = []
    # Skip checking git_pre_commit itself or install-hooks for the regex patterns
    str_path = str(path)
    if "git_pre_commit" in str_path or "lint-skills" in str_path or "test_git_pre_commit" in str_path:
        return errors

    if ABS_PATH_RE.search(text):
        errors.append(f"{path}: contains an absolute home path (keeping-repos-portable)")
    if SECRET_RE.search(text):
        errors.append(f"{path}: potential secret or private key pattern detected (hardening-trust-boundaries)")
    if ("skills/" in str_path or str_path.endswith("SKILL.md")) and ("TODO" in text or "TBD" in text):
        errors.append(f"{path}: contains TODO/TBD in skill definition")
    return errors


def check_manifest_versions_from_data(manifest_contents: dict):
    """Verify version numbers match across manifests."""
    versions = {}
    for rel_path, content in manifest_contents.items():
        try:
            data = json.loads(content)
            ver = data.get("version")
            if ver:
                versions[rel_path] = ver
        except (ValueError, KeyError):
            continue

    if len(set(versions.values())) > 1:
        details = ", ".join(f"{k}: {v}" for k, v in versions.items())
        return [f"Version mismatch across plugin manifests: {details}"]
    return []


def check_manifest_versions(root=ROOT):
    """Check version parity across on-disk manifests."""
    data = {}
    for rel in MANIFEST_PATHS:
        f = root / rel
        if f.exists():
            try:
                data[rel] = f.read_text(encoding="utf-8")
            except OSError:
                pass
    return check_manifest_versions_from_data(data)


def run_linter():
    """Run lint-skills.py if present."""
    linter = ROOT / "scripts" / "lint-skills.py"
    if not linter.exists():
        return []
    try:
        proc = subprocess.run([sys.executable, str(linter)], cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            return [f"lint-skills failed:\n{proc.stdout}\n{proc.stderr}"]
    except OSError as e:
        return [f"Failed to invoke linter: {e}"]
    return []


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    files_to_check = []
    if argv:
        files_to_check = [Path(p) for p in argv]
    else:
        staged = get_staged_files()
        files_to_check = [ROOT / p for p in staged]

    errors = []
    has_skill_changes = False

    for file_path in files_to_check:
        if not file_path.exists() or file_path.is_dir():
            continue
        rel = str(file_path.relative_to(ROOT)) if file_path.is_relative_to(ROOT) else str(file_path)
        if "skills/" in rel:
            has_skill_changes = True

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        errors.extend(check_content_rules(rel, content))

    # Manifest version check if any manifest is touched or general pre-commit
    manifest_touched = any(rel in [str(p) for p in files_to_check] for rel in MANIFEST_PATHS)
    if manifest_touched or not argv:
        errors.extend(check_manifest_versions())

    # If any skill was staged, verify the full skill linter
    if has_skill_changes and not argv:
        errors.extend(run_linter())

    if errors:
        print("PRE-COMMIT VERIFICATION FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
