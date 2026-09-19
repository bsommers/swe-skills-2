# Implementation Plan: <Feature / Change Name>

## 1. Goal
<!-- 2–3 sentences: the deliverable, not the activity. -->
Add <capability> to <component> so that <user/caller benefit>.

## 2. Motivation (Measured)
<!-- Numbers, error rates, or observed failures that justify the work. -->
- Observed: <failure description, token count, latency, or test failure>
- Expected: <target metric, clean pass, or bounded resource consumption>

## 3. Architecture Changes
<!-- A concise before/after description or minimal diagram. -->
```
Current:   Input -> ComponentA -> Output
Proposed:  Input -> ComponentA -> IntermediaryIR -> ComponentB -> Output
```

## 4. Contracts & Schemas
<!-- Exact types, signatures, or schemas produced and consumed across seams. -->
```python
class ProcessingContract:
    id: str
    payload: dict
    timestamp: float

def process_entry(entry: ProcessingContract) -> bool:
    """Processes entry deterministically without side effects."""
```

## 5. Global Constraints
<!-- Invariants the entire change must preserve. -->
- No new external runtime dependencies.
- Existing public API contracts and CLI flags remain backwards compatible.
- All test suites pass with zero warnings.
- Graceful degradation: errors in auxiliary reporting must not crash main execution.

## 6. Tasks
<!-- Numbered, dependency-ordered. Failing test first, minimal edit, verify command. -->

### Task 1: <Contract definition and unit test harness>
**Files:** `src/models.py`, `tests/test_models.py`
**Produces:** Core data models and validation functions
- [ ] Write failing test in `tests/test_models.py` (expected: model validation failure on missing fields)
- [ ] Implement minimal model definitions in `src/models.py`
- [ ] Verify: `pytest tests/test_models.py -q`

### Task 2: <Component integration and implementation>
**Files:** `src/engine.py`, `tests/test_engine.py`
**Produces:** Integrated pipeline stage honoring contracts
- [ ] Write failing test in `tests/test_engine.py`
- [ ] Implement pipeline transformation
- [ ] Verify: `pytest tests/test_engine.py -q`

## 7. Threat & Failure Model
<!-- What can go wrong and how it is mitigated or accepted. -->
| Threat / Edge Case | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Malformed input data | High | Med | Validate against contract upfront; return clean nonzero status. |
| Timeout on large payloads | Med | High | Enforce deadline on client side and process in bounded chunks. |

## 8. Verification Plan
<!-- Exact terminal commands and expected counts/outputs. -->
```bash
pytest -q tests/
ruff check .
python3 -m mypy .
```
