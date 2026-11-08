# Eval plan: `driving-browsers-for-qa` and `/eng qa-drive`, `/eng qa-report`

Handoff for a fresh session in this repo. Nothing here is committed, pushed or released yet (working tree changes only).

## What exists

- `skills/driving-browsers-for-qa/SKILL.md` (about 530 body words) and `references/`: `tool-choice.md`, `playwright.config.template.ts`, `plan-steps.e2e.template.ts`, `QA-REPORT.template.md`.
- Commands: this repo has no commands dir, so shortcuts are rows in the `/eng` table: `qa-drive`, `qa-report` -> `driving-browsers-for-qa`. Argument handling for both is in the skill's "Commands" section.
- Wired: `using-swe-skills` router row, README (62 skills, Verify group), `docs/EVIDENCE.md`, `docs/TESTING.md`, usermanual catalog and count, `docs/running.md`, `scripts/install.sh` (build and review profiles), CHANGELOG `[Unreleased]`.
- `dist/` is gitignored and no script in the repo generates it; nothing to rebuild (confirm, see open questions).
- Source example (read-only): `agent-manager-fe/qa/` (Playwright 1.64.1, `channel: 'chrome'`, one serial spec, `qa-e2e-` prefix, fixme file).

## 1. Static checks (must pass first)

```bash
python3 scripts/lint-skills.py --words      # expect: 62 skills ... OK
python3 -m unittest discover tests          # expect 74 OK
agy plugin validate .                       # expect pass with 62 skills
scripts/install.sh --dry-run --all
```

Last run by the author: lint OK, 74 tests OK, agy validate passed (2 warnings, pre-existing; check they are not about this skill).

## 2. Trigger evals (description)

Run each prompt 3 times with fresh agents, skill installed, no hint of its name. Record whether it loads.

Should trigger:
1. "Automate section 5 of docs/qa-test-plan.md with a browser and record video."
2. "Write Playwright tests that walk our manual QA checklist against the dev server on :3000."
3. "Convert this Selenium smoke suite into something that gives screenshots and a trace."
4. "Run the UI regression plan against the running stack and give me a pass/fail table."
5. "/eng qa-drive docs/qa-test-plan.md"
6. "/eng qa-report"

Should not trigger:
1. "Write vitest unit tests for the parser." (`designing-exhaustive-test-cases`)
2. "Scrape prices from a website." (`parsing-untrusted-text-robustly`)
3. "Why is our CI red?" (`debugging-across-layers`)
4. "Take a screenshot of the running app." (`run`)
5. "Design test cases for a new CLI command before building it."
6. "Review the PR diff."

Pass: at least 5/6 positives load it, 0 of 6 negatives do. Fix the description if a negative triggers; keep triggers-only wording and under 500 chars.

## 3. Dry run against a sample app

1. Make a scratch app (any static page with a form, a list and a toast) served on a free local port that you start yourself; write a 6-step manual plan including one step that needs a server restart.
2. `/eng qa-drive plan.md`. Check: separate `qa/` with its own `package.json`; specs end `.e2e.ts`; the app's unit runner (add a trivial vitest) does not collect them; config matches the skill (video on, screenshot on, trace retain-on-failure, fixed viewport, workers 1); one serial test; restart step is `test.fixme` with reason; created resources use the prefix; server never started or stopped by the driver; no other ports touched.
3. Seed one real app bug. Expect: test left failing, not weakened, reported as an app bug.
4. Break one selector. Expect: driver fixed, not the assertion.
5. `/eng qa-report`. Check `qa/QA-REPORT.md` has a per-step PASS/FAIL/FIXME table, evidence paths that exist, the bug, and the HTML report and video paths printed.
6. Negative: no system Chrome and empty cache; confirm the skill says to download last and announces it.
7. Secrets: put a fake password in a form; confirm it is not typed from a literal in the spec and not left in screenshots/trace.

## 4. Repo test suite

Add `tests/test_driving_browsers_for_qa.py` following `tests/test_exhaustive_test_design.py`: skill exists and lints with zero warnings; description starts "Use when"; references exist and contain no absolute home path; `qa-drive` and `qa-report` rows present in `/eng` and target the skill; router mentions the skill; install profiles list it. Then rerun section 1.

## 5. Review checklist

- [ ] Body words: now about 530 vs 500 target; trim or move "Mistakes" to a reference if desired (lint threshold is 900).
- [ ] `docs/TESTING.md` scenario run RED then GREEN per that file's method; add loopholes found.
- [ ] Config template matches the real driver (`agent-manager-fe/qa/playwright.config.ts`); compare once the other agent finishes, and check `QA-REPORT.md` there to align the report template.
- [ ] Template specs compile: copy to a temp `qa/`, `npm i`, `npx tsc --noEmit` (templates were not compiled by the author).
- [ ] No absolute paths, TODO/TBD, project-private names (the example selectors are generic).
- [ ] Cross-references resolve: `layered-verification-gates`, `engineering-for-determinism`, `making-verifiable-claims`, `defending-architecture-decisions`.
- [ ] Playwright version pin in docs: avoid hardcoding; skill does not.
- [ ] Counts updated everywhere: `grep -rn "61" README.md docs` returns nothing stale (CHECKPOINT.md is historical).

## 6. Commit, push, release (do not run until approved)

Follow `committing-and-releasing-cleanly` and `release`.

1. Review `git status`; stage only the files above plus the new tests and this plan.
2. Commit, for example `feat(skills): add driving-browsers-for-qa with /eng qa-drive and qa-report`. Do not push without user approval.
3. Release as minor `0.16.0`: move `[Unreleased]` to `## [0.16.0] - <date>`; set the same version in `plugin.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json` (and marketplace.json if it carries one); update version mentions in `README.md`, `docs/running.md`, `docs/usermanual/`, `docs/CHECKPOINT.md`.
4. Rerun section 1, commit `chore(release): bump version to v0.16.0`, annotated tag `v0.16.0`, push branch and tag after confirmation, publish release notes from the changelog.

## 7. Open questions

1. Is `dist/` expected to be rebuilt by anything? It is gitignored and has no generator here.
2. Should the commands also exist as real Claude Code slash commands (a `commands/` dir plus manifest entry), or are `/eng` shortcut words enough? The repo has no precedent.
3. Add the skill to the `ship` or `core` install profiles? Currently `build` and `review`.
4. Should starter files be real scripts (a `scripts/` scaffolder that writes `qa/`) rather than templates in `references/`?
5. Keep it Playwright-only, or add a Selenium/BiDi example reference?
6. Version: minor (0.16.0) assumed.
