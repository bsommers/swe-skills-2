---
name: layered-verification-gates
description: Use when deciding what "done" or "green" means, before committing, before a phase or release, when tests are skipped or unavailable, or when tempted to weaken a check to get past a gate.
---

# Layered Verification Gates

## Overview

"Passing" only means something if the right tests ran, nothing was silently skipped, and the bar wasn't lowered. Verify in **tiers**, gate at **three moments**, and **paste the output** as evidence.

## Tiers

| Tier | Proves | Notes |
|---|---|---|
| Unit | logic in isolation | fast (<1 s each); malformed-input negatives |
| Integration | components and pipelines together | property tests (100+ inputs); downstream toolchain smoke tests |
| Functional | user journeys | CLI via subprocess, E2E, REPL scripts |
| Security | boundaries hold | injection payloads, secret/path scans, dependency audit |

## Gates

1. **Pre-commit:** full local suite green, zero warnings (`-Wall -Werror`, `clippy -D warnings`, strict lint), docs synced.
2. **Pre-phase/milestone:** repeat the full suite, before starting *and* before declaring the phase finished.
3. **Pre-release:** all of the above plus clean-clone run, security scan, and changelog check.

## Rules

- **Skipped ≠ passed.** A test skipped because a service is down proves nothing. Print the skip reason, report the skip count, and run the skipped tier somewhere (a container run) before release.
- **Evidence before assertion.** State results with the command and its output ("`pytest -q` → 384 passed in 6.1s"), never "should be fine".
- **Never lower the bar to reach green.** No deleting tests, `@ts-ignore`/`noqa` sprees, assertions removed, thresholds edited down, stubs left. If a check is wrong, fix it in its own reviewed change with the reason.
- **Coverage is a tripwire**, not a goal. Use a threshold (e.g. ≥ 90% line, ≥ 85% branch) to catch untested code; then read the untested code (`hunting-silent-failures`).
- **Conserve CI.** Run everything locally before pushing; batch commits; avoid WIP pushes that burn remote minutes.
- **Scripted verification beats quiet flags.** Use the scripted gate above where one exists. Otherwise:
- **Quiet verification by default.** Run test and build commands with quiet flags (`cargo test -q`, `pytest -q`, `npm test -s`). Routine progress lines (`Compiling <crate>`, `test ... ok`) permanently bloat conversation context and replay on every subsequent turn; quiet flags cut output tokens by ~90% while preserving failures.
- **Counts are derived.** Don't hand-type "530 tests" in docs (`keeping-docs-in-sync`).
- **Clean clone.** Suites must pass without optional generated outputs present.

## Scripted, silent-on-success gates

Prefer a script over an agent running tests and reading output. The script runs everything, writes details to files, and prints **one line**. The agent reads the line, and only on FAIL opens one small file.

- **Contract:** `scripts/verify.sh` prints `PASS 31/31 9s` or `FAIL 2/31: <stages> -> <path>`; exit 0/1. PASS means done: do not inspect logs.
- **Result tree** (e.g. `target/verify/`, gitignored): `STATUS` (PASS|FAIL), `summary.tsv` (stage, status, secs), and per stage `status`, `fail.txt` (compact excerpt, ≤40 lines: error lines, failing test names, `file:line`), `log` (full output, last resort).
- **Granular stages:** one per tier, per test file/suite, per gate (lint, unit, each integration file, security, perf, arch). Small stages localize failure so the agent reads kilobytes, not megabytes.
- **Cheap re-runs:** `--quick` (lint+unit), `--failed` (only last failures), `--only <stage>`, `--list`, `--status` (re-print last result without running).
- **Auto-discovery:** new test files become stages without editing the script; new gates are added as stages with the same file contract.
- **Not a loophole:** skips are counted/reported in the excerpt; a stage that is opt-in (e.g. `fmt` with legacy drift) is named in the script header, never silently dropped. Don't lower the bar to get PASS.
- **Instrument for agents:** document the one-line contract in `AGENTS.md`/`CLAUDE.md` and put the script in every subagent/agy task's verify step so logs never enter context.

Template: `verify.sh.template` in this skill (Rust/cargo flavored; swap `cmd_for` and `all_stages` for pytest/npm/etc.).

## Gate script skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
pytest -q -rs            # -rs prints skip reasons
ruff check . && mypy .   # or cargo clippy -- -D warnings
./scripts/scan_secrets_and_paths.sh
git diff --exit-code -- generated/   # regeneration produced no drift
```

## Multi-layer review

Executor self-check → independent reviewer (fresh context) → security/test auditor → optionally a second model → human. See `orchestrating-subagents`.

## Common mistakes

- Green because the interesting tests skipped.
- "Tests pass" reported from memory of an earlier run.
- Fixing the failing test instead of the code without saying so.
- Different local vs CI commands.
