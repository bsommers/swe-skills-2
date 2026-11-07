---
name: layered-verification-gates
description: Use when deciding what "done" or "green" means, before committing, before a phase or release, when tests are skipped or unavailable, or when tempted to weaken a check to get past a gate.
---

# Layered Verification Gates

## Overview

"Passing" only means something if the right tests ran, nothing was silently skipped, and the bar wasn't lowered. Verify in **tiers**, gate at **three moments**, and **paste the output** as evidence.

## Tiers

Organize suites hierarchically (`tests/<tier>/` or runner markers/tags) so any tier, stage, or single test can be selected independently or composed into gates:

| Tier | Proves | Notes |
|---|---|---|
| **Smoke** | boots, imports, wiring, and config sanity | <2 s total; runs first to fail fast on broken builds/env |
| **Unit** | logic in isolation | fast (<1 s each); boundary values and malformed-input negatives |
| **Integration** | components, adapters, and pipelines together | property tests (100+ inputs); contract and toolchain checks |
| **System / E2E** | full user journeys and CLI/service workflows | subprocess/API/UI end-to-end against realistic state |
| **Performance** | latency, throughput, memory, and complexity budgets | regression ratchets against baseline percentiles |
| **Stress** | behavior under saturation and resource exhaustion | high concurrency, queue backpressure, pool/FD limits, rate-limit recovery |
| **Torture / Chaos** | resilience under adversarial, corrupt, and fault conditions | fuzz/property storms, kill `-9`/crash recovery, partial writes, clock skew, flaky I/O |
| **Security** | trust boundaries hold | injection payloads, authz bypass, secret/path scans, dependency audit |

## Gates

1. **Pre-commit (`--quick`):** lint, smoke, and unit green, zero warnings (`-Wall -Werror`, `clippy -D warnings`, strict lint), docs synced.
2. **Pre-phase/milestone (`--tier smoke,unit,integration,system,security`):** repeat full functional + security suites before starting *and* before declaring the phase finished.
3. **Pre-release (full suite):** all tiers including performance, stress, and torture/chaos, plus coverage/completeness check (`test-coverage`), clean-clone run, security scan, and changelog check.

## Rules

- **Exhaustive pre-build tests wired post-build.** Design the full test matrix before coding (`designing-exhaustive-test-cases`), add cases into `tests/<tier>/`, and run them after every build.
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
- **Reports & result tree** (`target/verify/`, gitignored): `STATUS`, `summary.tsv` (`stage<TAB>tier<TAB>PASS|FAIL<TAB>secs`), `report.md`, `junit.xml`, and per-stage `status`, `fail.txt` (≤40 lines), `log`.
- **Composable, hierarchical & cherry-picked selection:** `--quick` (lint+smoke+unit), `--tier <t1,t2>`, `--only <stage...>`, `--match <pattern>` (cherry-pick test case), `--failed`, `--list`, `--status`, `--report`.
- **Auto-discovery:** new test files under `tests/<tier>/` or `tests/` become stages automatically.
- **Not a loophole:** skips are counted/reported; opt-in stages are named in the script header.
- **Instrument for agents:** document the one-line contract in `AGENTS.md`/`CLAUDE.md`.

Templates & references: `verify.sh.template` (supports Rust/cargo and Python/pytest) and `references/TEST_TIERS_AND_TRIAGE.md`.

## Triage & Fixing Failing Tests

When a stage fails, follow `references/TEST_TIERS_AND_TRIAGE.md`:
1. **Read `fail.txt` first**, then cherry-pick (`scripts/verify.sh --only <stage> --match <test>`).
2. **Cluster multi-test failures** (`clustering-failures-by-root-cause`) by shared mechanism/layer.
3. **Fix code, not assertions:** assume a code regression (`debugging-across-layers`) unless the contract intentionally changed. Never weaken tolerances, delete assertions, or add sleeps to mask flakiness (`engineering-for-determinism`).
4. **Match fix to tier:** Smoke/Unit → logic/boundary; Integration/System → contract/seam (`designing-testable-seams`); Perf/Stress → complexity/contention/leak; Torture → atomicity/crash recovery.
5. **Re-verify in rings:** `--only` → `--failed` → `--quick` → full `scripts/verify.sh`.

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
