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
- **Counts are derived.** Don't hand-type "530 tests" in docs (`keeping-docs-in-sync`).
- **Clean clone.** Suites must pass without optional generated outputs present.

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
