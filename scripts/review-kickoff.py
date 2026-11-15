#!/usr/bin/env python3
"""Create a review workspace: docs/reviews/<date>/ with a baseline note, one prompt file per lens, and a REVIEW.md skeleton.

Harness-neutral: the prompt files can be handed to subagents or run one at a time.
Never overwrites an existing file. Stdlib only.
"""
import argparse
import datetime
import sys
from pathlib import Path

OUTPUT = ("Return at most 40 lines. Each finding: `severity (high/med/low) | file:line | evidence "
          "(command + output, or quote) | proposed fix`. Reproduce before reporting; put anything "
          "unreproduced under `UNVERIFIED`. Do not edit files. Do not read other lenses' results.")

LENSES = [
    ("goal-fit", "frontier", "Does the repo deliver its stated goals? Read the README, purpose and roadmap, "
     "list the goals, then find where behavior, scope or structure falls short or sprawls."),
    ("correctness", "standard", "Wrong results, edge cases, error paths, off-by-one, unvalidated input, "
     "swallowed exceptions, dead or duplicated logic."),
    ("security", "frontier", "Injection, secrets, permissions, unsafe shell or path handling, supply chain "
     "(pinned CI, dependencies), untrusted input at every boundary."),
    ("tests", "standard", "Run the suite. What is untested, skipped, flaky or only asserts that code runs? "
     "Are past incidents covered by regression tests?"),
    ("docs-and-plans", "standard", "Compare README, agent files, docs/, plans, changelog and manifests with "
     "the code and each other. Use `auditing-doc-alignment` and `scripts/doc-claims.py`."),
    ("portability", "standard", "Hard-coded paths, OS or shell assumptions, tool and harness lock-in, "
     "install and uninstall on each supported platform."),
    ("operations", "fast", "CI, release process, versioning, changelog, contributor experience, "
     "reproducibility, observability."),
]
GATES = ("scripts/verify.sh", "Makefile", "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "tox.ini")


def write(path, text, dry):
    if path.exists():
        print(f"keep   {path}")
        return
    print(f"{'would write' if dry else 'write'} {path}")
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def lens_prompt(n, key, tier, ask, goal):
    return (f"# Lens {n:02d}: {key}\n\nRecommended tier: **{tier}** (see `routing-work-across-harnesses`).\n\n"
            f"Project goal: {goal}\n\n## Ask\n\n{ask}\n\n## Output contract\n\n{OUTPUT}\n\n"
            f"Write your answer to `results/{n:02d}-{key}.md`.\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="repository root (default .)")
    ap.add_argument("--goal", default="<fill in: one sentence from the README/purpose doc>")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--lenses", help="comma-separated subset of: " + ",".join(k for k, *_ in LENSES))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"no such directory: {root}", file=sys.stderr)
        return 2
    wanted = {s.strip() for s in args.lenses.split(",")} if args.lenses else None
    known = {k for k, *_ in LENSES}
    if wanted and wanted - known:
        print(f"unknown lens: {', '.join(sorted(wanted - known))}", file=sys.stderr)
        return 2
    out = root / "docs" / "reviews" / args.date
    gates = [g for g in GATES if (root / g).exists()]

    write(out / "baseline.md",
          "# Baseline\n\nRun the gate first; record the exact command, result and skips.\n\n"
          f"Gate candidates found: {', '.join(gates) or 'none'}\n\n```\n$ <command>\n<output tail>\n```\n"
          "\nPass: _  Fail: _  Skipped: _\n", args.dry_run)
    n = 0
    for key, tier, ask in LENSES:
        n += 1
        if wanted and key not in wanted:
            continue
        write(out / "prompts" / f"{n:02d}-{key}.md", lens_prompt(n, key, tier, ask, args.goal), args.dry_run)
    write(out / "results" / ".gitkeep", "", args.dry_run)
    write(out / "REVIEW.md",
          f"# Review {args.date}\n\nGoal: {args.goal}\n\nHarness/tiers: run `scripts/detect-harness.py`; "
          "record substitutions here.\n\n## 1. Verdict and grades\n\n## 2. Findings\n\n"
          "| sev | location | evidence | fix |\n|---|---|---|---|\n\n## 3. Doc conformance\n\n"
          "## 4. Uplift plan and milestones (`planning-grade-a-uplift`)\n\n## 5. Not checked\n", args.dry_run)
    print(f"\nnext: run each prompts/*.md (parallel if the harness has subagents), then synthesize REVIEW.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
