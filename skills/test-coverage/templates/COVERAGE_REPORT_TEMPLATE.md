# Test Suite & Coverage Report — `<repo name>`

**Date:** `<YYYY-MM-DD>`
**Tooling used:** `<e.g. kcov 43 + shell_function_reachability.sh, or pytest-cov 5.0, or vitest --coverage>`

---

## 1. Test Suite Inventory & Runner Composability

| Dimension | Value |
|---|---|
| Test framework(s) | `<e.g. bats-core, pytest, vitest, cargo test>` |
| Composable runner | `<e.g. scripts/verify.sh (--quick, --tier, --only, --match, --failed)>` |
| Structured logs & reports | `<e.g. target/verify/{STATUS,summary.tsv,report.md,junit.xml,<stage>/fail.txt}>` |
| Total test files / cases | `<N files / M cases>` |
| CI-enforced? | `<yes/no, workflow file>` |
| Runtime | `<quick vs. full wall-clock time>` |

### Tier Completeness Matrix

| Tier | Path / Marker | Cases | Status (`PASS`/`FAIL`/`MISSING`) | Select Command | Notes / Gaps |
|---|---|---|---|---|---|
| **Smoke** | `tests/smoke/` | `<N>` | `<status>` | `scripts/verify.sh --tier smoke` | `<boot, import, config sanity>` |
| **Unit** | `tests/unit/` | `<N>` | `<status>` | `scripts/verify.sh --tier unit` | `<isolated logic, negatives>` |
| **Integration** | `tests/integration/` | `<N>` | `<status>` | `scripts/verify.sh --tier integration` | `<adapters, contracts, property>` |
| **System / E2E** | `tests/system/` | `<N>` | `<status>` | `scripts/verify.sh --tier system` | `<CLI/API/UI full workflows>` |
| **Performance** | `tests/perf/` | `<N>` | `<status>` | `scripts/verify.sh --tier perf` | `<latency/throughput/memory budgets>` |
| **Stress** | `tests/stress/` | `<N>` | `<status>` | `scripts/verify.sh --tier stress` | `<concurrency, saturation, limits>` |
| **Torture / Chaos** | `tests/torture/` | `<N>` | `<status>` | `scripts/verify.sh --tier torture` | `<fuzz, corrupt I/O, crash recovery>` |
| **Security** | `tests/security/` | `<N>` | `<status>` | `scripts/verify.sh --tier security` | `<injection, authz, boundary scans>` |

---

## 2. Coverage Summary

| Metric | Value | Source |
|---|---|---|
| Line coverage | `<X%>` (`<covered>/<total>`) | `<tool>` |
| Function/reachability coverage | `<X%>` (`<reached>/<total>`) | `<tool, e.g. shell_function_reachability.sh>` |
| Branch coverage (if measurable) | `<X%>` | `<tool>` |

> Note any known measurement caveats here (e.g. "kcov's per-file attribution is unreliable for this bats-core project — see reachability numbers as the trustworthy floor").

---

## 3. Coverage Gaps (Prioritized)

### P0 — Untested code on the critical/security path
List functions/modules with zero test references that handle: auth, credential handling, command construction from user input, network egress, privilege boundaries, destructive operations (delete/rm/force).

| Function/Module | File | Why it matters |
|---|---|---|
| | | |

### P1 — Untested core execution paths
The main "does the thing actually work" logic with no coverage (e.g. the real backend-driver execution functions, not just their pure-text-generation helpers).

| Function/Module | File | Why it matters |
|---|---|---|

### P2 — Untested edge cases / error handling
Functions that ARE referenced by tests, but only on the happy path — error branches, timeouts, and cleanup-on-failure paths are unverified.

| Function/Module | File | Missing scenario |
|---|---|---|

---

## 4. Shell Test-Quality Checklist (if applicable)

- [ ] At least one test exercises the real code under `bash -euo pipefail`, not just bats' own (non-`-e`) test runner — catches the "bare `[[ cond ]] && cmd` as a branch's last statement silently returns non-zero" bug class.
- [ ] Every function that shells out to an external binary (docker, ssh, cloud CLI tools, ...) has at least one test with that binary faked/mocked on `PATH`.
- [ ] Every place a variable is spliced into a command *string* (vs. passed as an argv array) has a test proving shell metacharacters in that variable aren't interpreted.
- [ ] Every dispatch table (`case $mode in ...)` mapping an enum to behavior) has a test asserting unknown values fail loudly rather than silently no-op.

---

## 5. Failing Test Triage & Remediation Advice (if any failures)

Cluster related failures by root mechanism (`clustering-failures-by-root-cause`) before fixing individual tests:

| Cluster / Stage | Failing Test(s) | Root Cause (`code bug` vs `stale test` vs `seam/fixture`) | Recommended Fix | Cherry-Pick Verify Command |
|---|---|---|---|---|
| `<stage>` | `<test_name>` | `<mechanism & file:line from fail.txt>` | `<fix implementation at layer X / update seam>` | `scripts/verify.sh --only <stage> --match <test_name>` |

---

## 6. Recommended Additions (Action Plan)

1. `<Concrete test or missing tier to add, with the file/tier it belongs in>`
2. `<...>`

---

## 7. What's Already Solid

Don't bury the positives — list what's well-tested so the plan doesn't read as universally negative.
