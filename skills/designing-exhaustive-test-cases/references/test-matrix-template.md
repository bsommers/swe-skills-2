# Pre-Build Exhaustive Test Matrix Template

Copy this matrix into the feature plan (`docs/plans/` or `.planning/`) **before writing implementation code**, then translate each row into failing test cases inside `tests/<tier>/`.

## Feature: `<Feature / Command / Endpoint Name>`

### 1. Pre-Build Exhaustive Test Matrix

| ID | Dimension | Scenario & Input | Expected Outcome / Invariant | Tier (`tests/<tier>/`) | Test File & Function | Pre-Build Status (RED) | Post-Build Status (GREEN) |
|---|---|---|---|---|---|---|---|
| TC-01 | **Happy Path** | Standard valid input across primary surface | Returns expected contract output; state updated | `unit` / `system` | `tests/unit/test_<feat>.py::test_valid_standard` | [ ] Fails as expected | [ ] Passes |
| TC-02 | **Happy Path (Surface Parity)** | Same capability invoked via CLI / API / UI / MCP | Identical result & exit status across surfaces | `system` | `tests/system/test_<feat>_parity.py::test_surface_parity` | [ ] Fails as expected | [ ] Passes |
| TC-03 | **Boundary & Equivalence** | Empty (`""`, `[]`, `{}`), zero (`0`), single-element (`[x]`) | Handled cleanly without panic or silent drop | `unit` | `tests/unit/test_<feat>.py::test_empty_and_single_boundaries` | [ ] Fails as expected | [ ] Passes |
| TC-04 | **Boundary & Equivalence** | Exact limit (`max - 1`, `max`) and overflow (`max + 1`) | Accepts `<= max`; rejects `max + 1` with typed limit error | `unit` | `tests/unit/test_<feat>.py::test_capacity_boundaries` | [ ] Fails as expected | [ ] Passes |
| TC-05 | **Boundary & Equivalence** | Unicode, whitespace-only, embedded nulls, special delimiters | Preserves encoding or rejects invalid control chars loudly | `unit` | `tests/unit/test_<feat>.py::test_unicode_and_special_chars` | [ ] Fails as expected | [ ] Passes |
| TC-06 | **Negative, Malformed & Adversarial** | Missing required fields, wrong types, malformed schema | Raises specific `ValidationError` / exits non-zero with field name | `unit` | `tests/unit/test_<feat>.py::test_malformed_inputs` | [ ] Fails as expected | [ ] Passes |
| TC-07 | **Negative, Malformed & Adversarial** | Injection payloads (shell metachars, path traversal `../`, SQL/query) | Payload neutralized or rejected at trust boundary | `security` | `tests/security/test_<feat>_security.py::test_injection_rejected` | [ ] Fails as expected | [ ] Passes |
| TC-08 | **Idempotency, Concurrency & State** | Duplicate/replayed invocation with identical input/key | Idempotent outcome; no duplicate records or corrupted state | `integration` | `tests/integration/test_<feat>_idempotency.py::test_replay_safe` | [ ] Fails as expected | [ ] Passes |
| TC-09 | **Idempotency, Concurrency & State** | Parallel workers racing on shared resource / lock | Serialized cleanly or optimistic conflict raised; zero data loss | `stress` | `tests/stress/test_<feat>_concurrency.py::test_parallel_contention` | [ ] Fails as expected | [ ] Passes |
| TC-10 | **Dependency & Fault Injection** | Downstream timeout, connection refused, partial/corrupt I/O (via fake) | Retries bounded if idempotent; surfaces typed error; no leaked handles | `integration` / `torture` | `tests/torture/test_<feat>_faults.py::test_downstream_failure_recovery` | [ ] Fails as expected | [ ] Passes |
| TC-11 | **Cross-Platform Driver Parity** | Windows (ConPTY/Named Pipe/CRLF), macOS (POSIX/APFS), Linux (POSIX/XDG) | Identical contract behavior across Windows, macOS, and Linux | `unit` / `integration` | `tests/integration/test_<feat>_drivers.py::test_tri_os_driver_contract` | [ ] Fails as expected | [ ] Passes |
| TC-12 | **Operational & Regression** | Latency/memory ceiling and structured telemetry/error logs | Completes within budget (`< N ms`); emits expected diagnostic fields | `perf` / `smoke` | `tests/perf/test_<feat>_budget.py::test_latency_and_telemetry` | [ ] Fails as expected | [ ] Passes |

---

### 2. Post-Build Suite Integration Checklist

- [ ] **RED verified before coding:** All planned test cases (`TC-01`..`TC-11`) were written and executed before implementation, failing for the expected reason.
- [ ] **Auto-discovered by test runner:** Every new test file lives under `tests/<tier>/` (or has tier markers) and appears in `scripts/verify.sh --list`.
- [ ] **Fast gate (`--quick`) passes:** `scripts/verify.sh --quick` executes new `smoke` and `unit` tests in `< 10s`.
- [ ] **Full tiered suite passes post-build:** `scripts/verify.sh` executes `smoke`, `unit`, `integration`, `system`, `perf`, `stress`, `torture`, and `security` stages with 0 failures and 0 silent skips.
- [ ] **Coverage & branch audit complete:** New code achieves `>= 90%` line and `>= 85%` branch coverage (`test-coverage`), with zero unprobed error branches (`hunting-silent-failures`).
