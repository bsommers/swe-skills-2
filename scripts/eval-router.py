#!/usr/bin/env python3
"""Evaluate router accuracy against the benchmark scenarios defined in docs/TESTING.md.

Benchmark criterion:
  Given 10 varied tasks (tool, app, system; build, debug, ship).
  Pass when the router loads the correct 1–3 skills for >= 8 of them (>= 80%)
  and never loads more than 4 skills.

Usage:
  python3 scripts/eval-router.py --self-test
  python3 scripts/eval-router.py --prompt "write a python CLI tool"
  python3 scripts/eval-router.py --self-test --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
ROUTER_FILE = SKILLS_DIR / "using-swe-skills" / "SKILL.md"

BENCHMARK_CASES = [
    {
        "id": "tool_build_cli",
        "scale": "Tool",
        "task_type": "build",
        "prompt": "Write a small CLI tool that converts CSV to JSON with proper arguments and help text.",
        "expected": ["building-small-cli-tools"],
    },
    {
        "id": "tool_debug_determinism",
        "scale": "Tool",
        "task_type": "debug",
        "prompt": "The generated output file differs across consecutive runs; fix the flakiness and diff churn.",
        "expected": ["engineering-for-determinism"],
    },
    {
        "id": "tool_ship_commit",
        "scale": "Tool",
        "task_type": "ship",
        "prompt": "Commit and push this single-file fix with a conventional message after running tests.",
        "expected": ["committing-and-releasing-cleanly"],
    },
    {
        "id": "app_plan_contracts",
        "scale": "App",
        "task_type": "plan",
        "prompt": "Write an implementation plan for adding retry logic and external API seams across 4 modules.",
        "expected": ["planning-with-contracts", "designing-testable-seams"],
    },
    {
        "id": "app_build_scaffold",
        "scale": "App",
        "task_type": "build",
        "prompt": "Scaffold a new project directory with src, tests, docs, and input/output structure.",
        "expected": ["scaffolding-new-projects"],
    },
    {
        "id": "app_debug_silent_failures",
        "scale": "App",
        "task_type": "debug",
        "prompt": "Test coverage is only 60%; review the untested modules for silent failures and edge case bugs.",
        "expected": ["hunting-silent-failures"],
    },
    {
        "id": "app_ship_pr",
        "scale": "App",
        "task_type": "ship",
        "prompt": "Draft a pull request grouping fixes for issues #12 and #15 with verified test commands.",
        "expected": ["writing-pull-requests"],
    },
    {
        "id": "system_plan_pipeline",
        "scale": "System",
        "task_type": "plan",
        "prompt": "Design an ETL data pipeline with DAG workflows and interchangeable database storage backends.",
        "expected": ["designing-data-pipelines", "designing-plugin-contracts"],
    },
    {
        "id": "system_build_agent_loop",
        "scale": "System",
        "task_type": "build",
        "prompt": "Build an unattended agent execution loop that runs code, retries on failure, and sizes limits from measurement.",
        "expected": ["building-unattended-agent-loops", "sizing-limits-from-measurement"],
    },
    {
        "id": "system_debug_compaction",
        "scale": "System",
        "task_type": "debug",
        "prompt": "Context window is filling up mid-refactor; create a checkpoint before running compact or clear.",
        "expected": ["compacting-context-safely"],
    },
]


STOP_WORDS = {
    "use", "when", "for", "and", "or", "to", "in", "with", "a", "an",
    "the", "that", "this", "from", "on", "as", "at", "by", "is", "it", "of", "before"
}


def _stem(word: str) -> str:
    """Lightweight suffix normalizer without external dependencies."""
    w = word.lower()
    for sfx in ("ing", "ies", "es", "ed", "s"):
        if w.endswith(sfx) and len(w) > len(sfx) + 2:
            return w[:-len(sfx)]
    return w


def load_router_rules():
    """Extract keyword and trigger patterns from using-swe-skills and skill frontmatter."""
    text = ROUTER_FILE.read_text(encoding="utf-8")
    rules = []
    # Match markdown table lines: | <trigger> | `<skill>` |
    for line in text.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*`([a-z0-9-]+)`\s*\|", line)
        if m:
            trigger_text = m.group(1).strip()
            skill_name = m.group(2).strip()
            if trigger_text.lower() not in ("when you…", "---"):
                # Table trigger tokens get high weight (3x)
                trigger_tokens = {_stem(w) for w in re.findall(r"[A-Za-z0-9]+", trigger_text) if w.lower() not in STOP_WORDS}
                skill_name_tokens = {_stem(w) for w in skill_name.split("-") if w not in STOP_WORDS}
                
                # Frontmatter description tokens get normal weight (1x)
                desc_tokens = set()
                skill_file = SKILLS_DIR / skill_name / "SKILL.md"
                if skill_file.exists():
                    f_text = skill_file.read_text(encoding="utf-8")
                    fm_match = re.match(r"^---\n(.*?)\n---", f_text, re.S)
                    if fm_match:
                        desc_tokens = {
                            _stem(w) for w in re.findall(r"[A-Za-z0-9]+", fm_match.group(1))
                            if w.lower() not in STOP_WORDS
                        }
                rules.append({
                    "skill": skill_name,
                    "trigger": trigger_text,
                    "trigger_tokens": trigger_tokens | skill_name_tokens,
                    "desc_tokens": desc_tokens,
                })
    return rules


def route_prompt(prompt: str, rules=None) -> list[str]:
    """Deterministic reference router matching prompt against swe-skills routing rules."""
    if rules is None:
        rules = load_router_rules()
    prompt_tokens = {_stem(w) for w in re.findall(r"[a-z0-9-]+", prompt.lower()) if w not in STOP_WORDS}

    # Direct skill name mention in prompt
    explicit_skills = [
        r["skill"] for r in rules
        if r["skill"] in prompt.lower()
    ]
    if explicit_skills:
        return explicit_skills[:3]

    scores = []
    for r in rules:
        trigger_overlap = len(prompt_tokens & r["trigger_tokens"])
        desc_overlap = len(prompt_tokens & r["desc_tokens"])
        total_score = (trigger_overlap * 3) + desc_overlap
        if total_score > 0:
            scores.append((total_score, r["skill"]))

    scores.sort(key=lambda x: x[0], reverse=True)
    selected = []
    for _, skill in scores:
        if skill not in selected:
            selected.append(skill)
        if len(selected) >= 3:
            break

    # Fallback to general process sizing if nothing matched
    if not selected:
        selected = ["right-sizing-process"]
    return selected[:3]


def score_prediction(case: dict, predicted_skills: list[str]) -> dict:
    """Score a router prediction against case requirements and constraint rules."""
    expected = case.get("expected", [])
    if len(predicted_skills) > 4:
        return {
            "passed": False,
            "reason": f"Predicted {len(predicted_skills)} skills; exceeds max limit of 4.",
            "predicted": predicted_skills,
            "expected": expected,
        }
    if not (1 <= len(predicted_skills) <= 3):
        return {
            "passed": False,
            "reason": f"Predicted {len(predicted_skills)} skills; must load 1–3 skills.",
            "predicted": predicted_skills,
            "expected": expected,
        }
    missing = [s for s in expected if s not in predicted_skills]
    if missing:
        return {
            "passed": False,
            "reason": f"Required skills missing: {missing}",
            "predicted": predicted_skills,
            "expected": expected,
        }
    return {
        "passed": True,
        "reason": "All expected skills present and load budget respected.",
        "predicted": predicted_skills,
        "expected": expected,
    }


def run_benchmark(cases=None, router_func=None):
    """Run the 10 benchmark test cases and return aggregate performance."""
    if cases is None:
        cases = BENCHMARK_CASES
    if router_func is None:
        router_func = route_prompt

    results = []
    passed_count = 0
    for case in cases:
        predicted = router_func(case["prompt"])
        score = score_prediction(case, predicted)
        score["case_id"] = case["id"]
        score["scale"] = case["scale"]
        score["prompt"] = case["prompt"]
        if score["passed"]:
            passed_count += 1
        results.append(score)

    accuracy = passed_count / len(cases) if cases else 0.0
    overall_passed = accuracy >= 0.80
    return {
        "passed": overall_passed,
        "accuracy": accuracy,
        "passed_count": passed_count,
        "total_cases": len(cases),
        "cases": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate swe-skills router.")
    parser.add_argument("--self-test", action="store_true", help="Run 10 benchmark cases")
    parser.add_argument("--prompt", type=str, help="Route a single prompt")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if args.prompt:
        selected = route_prompt(args.prompt)
        if args.json:
            print(json.dumps({"prompt": args.prompt, "skills": selected}))
        else:
            print(f"Loaded skills ({len(selected)}): {', '.join(selected)}")
        return 0

    if args.self_test:
        report = run_benchmark()
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Benchmark Results: {'PASS' if report['passed'] else 'FAIL'}")
            print(f"Accuracy: {report['passed_count']}/{report['total_cases']} ({report['accuracy'] * 100:.1f}%)")
            for c in report["cases"]:
                status = "PASS" if c["passed"] else "FAIL"
                print(f"  [{status}] {c['case_id']} ({c['scale']}): expected {c['expected']} -> got {c['predicted']}")
                if not c["passed"]:
                    print(f"         Reason: {c['reason']}")
        return 0 if report["passed"] else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
