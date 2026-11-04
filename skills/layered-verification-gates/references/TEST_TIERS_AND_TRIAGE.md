# Test Tiers & Failure Triage Reference

## 1. Full Test Suite Taxonomy

Organize test suites hierarchically under `tests/<tier>/` (or runner markers/tags) so any tier, stage, or single test can be executed independently or composed into verification gates:

| Tier | Path / Marker | Proves | Typical Budget & Inputs |
|---|---|---|---|
| **Smoke** | `tests/smoke/` | Package imports, binary boots, CLI `--help`/`--version`, config & schema load | < 2 s total; runs first in every gate |
| **Unit** | `tests/unit/` | Pure functions, state transitions, boundary values, malformed-input negatives | < 1 s per file; zero network/DB/FS side effects |
| **Integration** | `tests/integration/` | Multi-module wiring, DB/adapter contracts, property tests (100+ cases), downstream toolchain parse | Seconds; uses local containers or faithful fakes |
| **System / E2E** | `tests/system/` | Full user journeys, CLI subprocess flows, HTTP/IPC round-trips against realistic state | Seconds to minutes; black-box entry points |
| **Performance** | `tests/perf/` | Latency percentiles ($p_{50}/p_{95}/p_{99}$), throughput, memory ceiling, algorithmic complexity | Compares against committed baseline ratchet |
| **Stress** | `tests/stress/` | High concurrency, queue backpressure, connection-pool / FD / memory saturation, rate-limit recovery | Pushes beyond nominal load; asserts graceful degradation |
| **Torture / Chaos** | `tests/torture/` | Fuzz/property storms, corrupt/truncated payloads, `SIGKILL`/crash recovery, partial writes, clock skew, flaky I/O | Asserts zero silent corruption and clean recovery |
| **Security** | `tests/security/` | Injection payloads, authz/tenant boundaries, path traversal, secret scans, dependency CVEs | Negative boundary assertions |

---

## 2. Composable Runner & Report Contract (`scripts/verify.sh`)

Every repository should expose a single composable entry point (`scripts/verify.sh`, templated in `verify.sh.template`) that supports:

- **Fast & tiered selection:**
  - `scripts/verify.sh` — runs all tiers (`lint`, `smoke`, `unit`, `integration`, `system`, `perf`, `stress`, `torture`, `security`)
  - `scripts/verify.sh --quick` — runs `lint,smoke,unit`
  - `scripts/verify.sh --tier smoke,unit,integration` — runs any comma-separated tier subset
- **Hierarchical & cherry-picked execution:**
  - `scripts/verify.sh --list` — prints `stage<TAB>tier` inventory
  - `scripts/verify.sh --only unit:parser integration:db` — runs specific stage(s)
  - `scripts/verify.sh --only unit:parser --match test_empty_input` — cherry-picks a single test case/function
  - `scripts/verify.sh --failed` — re-runs only stages that failed on the previous run
- **Structured reports & logs (`target/verify/`, gitignored):**
  - `STATUS` — `PASS` or `FAIL`
  - `summary.tsv` — `stage<TAB>tier<TAB>PASS|FAIL<TAB>secs`
  - `report.md` — human-readable Markdown table with links to stage logs/excerpts
  - `junit.xml` — machine-readable JUnit XML for CI and test reporters
  - `<stage>/fail.txt` — deduplicated ≤ 40-line failure excerpt (`file:line`, error, failing test names)
  - `<stage>/log` — full raw stage output (inspected only if `fail.txt` is insufficient)

---

## 3. Triage & Fixing Failing Tests

Follow this sequence whenever tests fail:

1. **Localize from `fail.txt`:** Read `target/verify/<stage>/fail.txt` first. Reproduce with `scripts/verify.sh --only <stage> --match <test>`.
2. **Cluster multi-test failures (`clustering-failures-by-root-cause`):** When ≥ 3 tests fail, group them by shared root mechanism and layer before editing code.
3. **Code bug vs. stale test:**
   - **Default to code bug:** Assume the test caught a real regression, broken invariant, or unhandled edge case (`debugging-across-layers`).
   - **When to update a test:** Only when the specification or contract intentionally changed; cite the contract change in the commit message.
   - **Forbidden fixes:** Never delete assertions, widen tolerances to hide regressions, add arbitrary `sleep` calls, or mark tests `@skip`/`#[ignore]` to get green (`engineering-for-determinism`).
4. **Failure playbook by tier:**
   - **Smoke / Unit:** Broken import, missing export, off-by-one/null boundary, or uninitialized config default.
   - **Integration / System:** Schema/DTO drift between producer and consumer, fixture state leakage across tests, hardcoded path/port, or unmocked external binary (`designing-testable-seams`).
   - **Performance / Stress:** Accidental $O(n^2)$ loop, N+1 query, lock contention, unbounded channel/buffer, or leaked file descriptors/connections.
   - **Torture / Chaos:** Non-atomic file update (write-without-rename), missing idempotency key on retry, partial-read assumption, or uncaught panic on corrupt input.
5. **Verify the fix in widening rings:**
   - Cherry-pick: `scripts/verify.sh --only <stage> --match <test>`
   - Failed stages: `scripts/verify.sh --failed`
   - Quick gate: `scripts/verify.sh --quick`
   - Full suite: `scripts/verify.sh`
