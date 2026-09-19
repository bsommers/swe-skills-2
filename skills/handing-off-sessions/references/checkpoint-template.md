# Checkpoint — <Topic / Component> — YYYY-MM-DD

**Status:** IN PROGRESS — needs resume <!-- or COMPLETE -->
**Branch:** `<branch-name>` @ `<short-sha>`
**Working Tree:** `<clean / uncommitted files listed>`

## 1. Goal & Context
<!-- In user's words: the high-level objective and constraints. -->
<One to two sentences summarizing the target capability.>

## 2. Done (With Evidence)
<!-- Itemized completed tasks accompanied by exact verification commands and outputs. -->
- Completed contract definition: `src/core/contracts.py` created.
- Verified test pass: `pytest tests/test_contracts.py -q` -> 8 passed in 0.12s.

## 3. Failed / Blocked (With Root Cause)
<!-- Dead ends, blockers, and why specific approaches failed so they are not repeated. -->
- Direct memory mapping failed on socket payloads. Root cause: payload length exceeds buffer size when headers contain extensions. Switched to chunked stream parser.

## 4. State That May Have Changed
<!-- Modified files, generated fixtures, running daemons, background tasks, or ports. -->
- Background server on port 8080 terminated.
- Test database seeded with 50 synthetic fixtures; regenerate with `python3 scripts/seed.py` if schema modified.

## 5. Explicit Authorizations & Scope
<!-- Boundaries and approvals granted by the user. -->
- Permitted: modifying local test harness and script files under `scripts/`.
- Prohibited: pushing to remote or modifying external repository dependencies.

## 6. Next Steps (Exact Commands In Order)
<!-- Executable, ordered commands for a zero-context reader resuming the session. -->
1. Verify state: `git status` and `pytest tests/test_contracts.py -q`
2. Implement chunked buffer parser in `src/core/parser.py`
3. Run verification suite: `pytest -q tests/`
