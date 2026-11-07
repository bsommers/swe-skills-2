---
name: designing-exhaustive-test-cases
description: Use when planning or building new functionality, features, endpoints, CLI commands, or modules, before writing implementation code, to specify exhaustive pre-build test cases and wire them into the automated post-build test suite.
---

# Designing Exhaustive Test Cases

## Overview

Every planned feature or behavior change gets an **exhaustive test matrix before build time**, written as failing tests first and wired permanently into the automated test suite (`layered-verification-gates`) so every build runs them for maximum coverage, operational resilience, and minimum bugs.

## 1. Pre-Build Exhaustive Test Matrix

During planning (`planning-with-contracts`) and before writing implementation code, enumerate test cases across all six dimensions (template in `references/test-matrix-template.md`):

| Dimension | What to specify before build |
|---|---|
| **1. Happy path & contract invariants** | Valid inputs across every surface (`designing-uniform-surfaces`), expected return shapes, state transitions, and post-conditions. |
| **2. Boundary & equivalence partitions** | `0`, `1`, `max - 1`, `max`, `max + 1`, empty collections/strings, `null`/`None`, single vs. multi-element, Unicode, whitespace, off-by-one edges (`hunting-silent-failures`). |
| **3. Negative, malformed & adversarial** | Wrong types, missing required fields, out-of-range values, syntax/parse errors, unauthorized callers, injection/traversal payloads (`hardening-trust-boundaries`). Assert the exact typed error or exit code (`designing-testable-seams`). |
| **4. Idempotency, state & concurrency** | Duplicate/replayed requests, out-of-order events, concurrent access/races, partial-write rollback, deterministic retry behavior (`engineering-for-determinism`). |
| **5. Dependency failure & degradation** | Timeouts, connection refused, corrupt/partial responses, disk full, permission denied — exercised via injected fakes across Windows, macOS, and Linux driver seams (`designing-testable-seams`, `designing-plugin-contracts`). |
| **6. Operational & regression ratchets** | Latency/memory bounds, structured log/metric/error emission, and backward compatibility with existing schemas (`evolving-schemas-and-contracts`). |

## 2. Assign Every Case to a Suite Tier

Map each planned test case to its target tier in `tests/<tier>/` (or runner markers) so `scripts/verify.sh` discovers and runs it automatically (`layered-verification-gates`):

- **`smoke`**: feature registration, CLI `--help`/subcommand wiring, config boot sanity (<2 s).
- **`unit`**: isolated pure logic, boundary partitions, and malformed-input negatives (<1 s each).
- **`integration`**: component/adapter contracts, database/IPC seams, property tests (100+ generated inputs).
- **`system`**: end-to-end CLI, API, or UI user workflows against realistic state.
- **`perf` / `stress`**: latency/memory ratchets and concurrency/backpressure saturation limits.
- **`torture` / `security`**: crash recovery, partial I/O, corrupt payloads, and authz/injection boundaries (`security-best-practices`).

## 3. Execute RED → Build → GREEN → Post-Build Suite

1. **Instantiate failing tests first (RED):** Write the test functions in `tests/<tier>/` before feature code. Run `scripts/verify.sh --only <stage>` (`pytest -q` / `cargo test -q`) and verify they fail for the missing behavior, not a test syntax or import error.
2. **Build minimal implementation (GREEN):** Implement the contract until all new test cases pass.
3. **Wire into post-build suite & CI:** Confirm new test files are auto-discovered or registered in `scripts/verify.sh` and CI so they run after every build (`--quick` pre-commit, `--tier` pre-merge, full `scripts/verify.sh` pre-release).
4. **Verify coverage & silent-failure gaps:** Run `test-coverage` on the new module (target ≥90% line, ≥85% branch, 100% of error paths) and probe uncovered branches with `hunting-silent-failures`.

## Common Mistakes

- **Designing tests after coding:** Post-hoc tests mirror implementation bugs instead of the specification.
- **Happy-path-only TDD:** Writing one trivial failing test while skipping boundary, negative, concurrency, and fault cases.
- **Orphaned test files:** Writing tests in ad-hoc scripts outside `tests/<tier>/` that `scripts/verify.sh` and CI never run post-build.
- **Testing mocks instead of seams:** Asserting mock calls instead of asserting outcomes against an in-memory fake (`designing-testable-seams`).
- **Broad error assertions:** Checking `assert raises(Exception)` instead of asserting the specific typed error, code, and message.
