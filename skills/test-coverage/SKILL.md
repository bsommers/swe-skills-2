---
name: test-coverage
description: Use when auditing a repository's test suite to measure real coverage across languages, identify untested critical paths, evaluate shell test quality, or produce a prioritized gap-closing plan.
---

# Test Coverage & Suite Robustness Skill

Audits an existing test suite, measures real coverage (not just "tests pass"), and produces a prioritized, saved-to-repo plan for closing the gaps that matter most — critical/security paths first, raw percentage last.

**Core principle:** a coverage percentage is a proxy, not the goal. A codebase at 95% line coverage with every external command unmocked and every dispatch table silently no-op-ing on bad input is less safe than one at 70% that has deliberately targeted the failure modes that actually bite. This skill treats percentage as one input among several, not the deliverable.

---

## Agent Detection & Mode Tuning

Detect the active runtime environment. See `references/AGENT_TUNING.md` for tool selection and output conventions.

---

## Workflow Overview

```mermaid
flowchart TD
    Start(["Start"]) --> Step1["Step 1: Detect language(s) + existing test/coverage tooling"]
    Step1 --> Step2["Step 2: Select coverage tool (references/COVERAGE_TOOLS_MATRIX.md)"]
    Step2 --> Gate{"Tool installed?"}
    Gate -- No --> Ask["Ask user: install it, or proceed with static fallback?"]
    Ask -- Install --> Step3
    Ask -- Fallback --> Step3b["Static fallback: shell_function_reachability.sh or language equivalent"]
    Gate -- Yes --> Step3["Step 3: Run instrumented test suite"]
    Step3 --> Step4["Step 4: Generate reports (terminal, HTML, machine-readable)"]
    Step3b --> Step4
    Step4 --> Step5["Step 5: Gap analysis (P0/P1/P2, not just raw %)"]
    Step5 --> Step6["Step 6: Shell Test-Quality Checklist (if Bash/shell project)"]
    Step6 --> Step7["Step 7: Save report + plan into repo"]
    Step7 --> Step8["Step 8: Offer CI wiring + threshold gate"]
    Step8 --> End(["Done"])
```

---

## Step 1: Detect Language(s) & Existing Tooling

Inspect project manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `Gemfile`, `*.csproj`, `composer.json`, `*.bats`). Check for existing configured tooling in CI or scripts before introducing new tools:
```bash
grep -rn "coverage\|kcov\|nyc\|c8\|pytest-cov\|tarpaulin\|jacoco\|coverlet" package.json pyproject.toml Makefile .github/workflows/*.yml 2>/dev/null
```

---

## Step 2: Select the Coverage Tool

Consult `references/COVERAGE_TOOLS_MATRIX.md` for tool selection. For **Bash/shell projects**, review `references/BASH_COVERAGE_NOTES.md` for kcov+bats failure modes.

### Installation Gate
If the selected tool is uninstalled, ask the user before installing:
> *"`<tool>` isn't installed. Install it via `<command>`, or proceed with static reachability fallback?"*

---

## Step 3: Run the Instrumented Suite

Run the language-specific tool per `references/COVERAGE_TOOLS_MATRIX.md`:
- **Python:** `pytest --cov=<package> --cov-report=term-missing --cov-report=html --cov-report=xml`
- **Node/TS:** `vitest run --coverage` or `jest --coverage`
- **Go:** `go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out`
- **Rust:** `cargo llvm-cov --html`
- **Bash / bats-core:** Run direct CLI `kcov` invocations per `references/BASH_COVERAGE_NOTES.md`. Always run `scripts/shell_function_reachability.sh` for static floor reachability.

---

## Step 4: Generate Reports

Produce:
1. **Terminal summary:** Display to user immediately.
2. **Machine-readable:** lcov/cobertura/JSON for CI gating.
3. **HTML:** For human inspection (keep gitignored).
The deliverable committed to repo is `templates/COVERAGE_REPORT_TEMPLATE.md` filled in.

---

## Step 5: Gap Analysis — Beyond the Percentage

Classify uncovered functions by risk:
- **P0:** Auth, credentials, user-input command construction, network egress, privilege boundaries, destructive operations (rm/force/delete).
- **P1:** Core execution paths (backend/driver logic). Tool fails completely if broken.
- **P2:** Error-handling/edge cases in otherwise tested modules.

Name specific functions and the concrete failure scenarios if broken silently.

---

## Step 6: Shell Test-Quality Checklist

Apply whenever the target includes Bash/shell code (details in `references/SHELL_TEST_QUALITY.md`):
1. **`set -e` interaction check:** Assert functions exit cleanly under `bash -euo pipefail -c '...; echo REACHED_END'`.
2. **External-command mocking:** Mock external CLIs (`docker`, `ssh`, `curl`) via fake scripts on `PATH` instead of skipping.
3. **Command-string injection check:** Assert string-interpolated shell commands safely handle metacharacters (or use argv arrays).
4. **Dispatch-table completeness:** Ensure every `case` statement has a loud `*) die ...` default branch rather than silent fallthrough.

---

## Step 7: Save the Report

Write the filled-in `templates/COVERAGE_REPORT_TEMPLATE.md` to:
- `docs/TEST_COVERAGE.md` (preferred if `docs/` exists), or
- `.planning/research/TEST_COVERAGE_<date>.md` (GSD/planning-structured projects), or
- `TEST_COVERAGE.md` at repo root otherwise.

Diff against prior reports if present to highlight regressions vs. improvements.

---

## Step 8: Offer CI Wiring

Propose:
1. CI job running coverage and uploading artifacts.
2. Threshold gate ("never drop below baseline").
3. For Bash: `shell_function_reachability.sh` as a deterministic blocking check.

---

## Anti-Patterns to Avoid

1. **Do NOT treat a raw percentage as the deliverable.** A number with no gap analysis or prioritization is not actionable.
2. **Do NOT claim instrumented coverage works when it doesn't.** If kcov+bats produces a report attributing everything to a bats temp file (see `BASH_COVERAGE_NOTES.md`), say so and lean on the reachability script instead of reporting a misleading number.
3. **Do NOT skip a function's tests just because the required external tool isn't installed in this environment.** Mock it instead — that's the whole point of the External-command mocking checklist item.
4. **Do NOT install packages/tools without asking first** (matches the pattern in `code-architecture-review`'s Graphify gate).
5. **Do NOT silently overwrite an existing coverage report** — diff and note deltas.
6. **Do NOT stop at "tests pass."** A suite that passes 100% of its tests while never exercising the riskiest code paths (per Step 5's P0/P1 classification) is not robust, regardless of the percentage.
