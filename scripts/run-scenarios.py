#!/usr/bin/env python3
"""Run and validate pressure-test scenarios defined in docs/TESTING.md.

Usage:
  scripts/run-scenarios.py --list
  scripts/run-scenarios.py --dry-run
  scripts/run-scenarios.py --skill using-swe-skills
  scripts/run-scenarios.py --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTING_MD = ROOT / "docs" / "TESTING.md"
SKILLS_DIR = ROOT / "skills"


def parse_scenarios():
    """Extract scenarios from docs/TESTING.md markdown table."""
    text = TESTING_MD.read_text(encoding="utf-8")
    scenarios = []
    # | `skill` | "prompt" | Pass criterion |
    table_pattern = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
    for line in text.splitlines():
        m = table_pattern.match(line)
        if m:
            skill = m.group(1).strip()
            prompt = m.group(2).strip().strip('"')
            criterion = m.group(3).strip()
            scenarios.append({
                "skill": skill,
                "prompt": prompt,
                "pass_criterion": criterion,
            })
    return scenarios


def dry_run_scenarios(scenarios):
    """Verify all scenarios map to existing skills on disk."""
    errors = []
    for sc in scenarios:
        skill_dir = SKILLS_DIR / sc["skill"]
        if not skill_dir.is_dir():
            errors.append(f"Scenario targets nonexistent skill directory: {sc['skill']}")
        elif not (skill_dir / "SKILL.md").exists():
            errors.append(f"Missing SKILL.md for skill: {sc['skill']}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Scenario runner for swe-skills.")
    parser.add_argument("--list", action="store_true", help="List all scenario definitions")
    parser.add_argument("--dry-run", action="store_true", help="Verify scenario definitions and skills on disk")
    parser.add_argument("--skill", type=str, help="Display scenario for a specific skill")
    parser.add_argument("--json", action="store_true", help="Output scenarios as JSON")
    args = parser.parse_args()

    scenarios = parse_scenarios()

    if args.list:
        print(f"Loaded {len(scenarios)} pressure scenarios from docs/TESTING.md:")
        for idx, sc in enumerate(scenarios, 1):
            print(f"  {idx:2d}. `{sc['skill']}`")
            print(f"      Prompt: \"{sc['prompt']}\"")
            print(f"      Pass:   {sc['pass_criterion']}")
        return 0

    if args.dry_run:
        errors = dry_run_scenarios(scenarios)
        if errors:
            print(f"FAILED: {len(errors)} error(s) found in scenario registry:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1
        print(f"OK: All {len(scenarios)} scenarios map to valid, existing skills.")
        return 0

    if args.skill:
        matched = [sc for sc in scenarios if sc["skill"] == args.skill]
        if not matched:
            print(f"No scenario found for skill: {args.skill}", file=sys.stderr)
            return 1
        for sc in matched:
            print(f"Skill: {sc['skill']}")
            print(f"Scenario Prompt: {sc['prompt']}")
            print(f"Pass Criterion:  {sc['pass_criterion']}")
        return 0

    if args.json:
        print(json.dumps(scenarios, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
