# How-To Guides & Operational Recipes

Practical, copy-pasteable recipes for applying `swe-skills` across common software engineering workflows.

---

## Recipe 1: Sizing and Planning a Feature

When starting any new task, use `/eng` to automatically route to the minimal necessary skills without context bloat:

```text
/eng implement rate limiting on the POST /v1/auth/tokens endpoint
```

1. **Task Sizing:** The router evaluates the radius:
   - Affects 2 files (`src/routes/auth.py`, `src/services/limiter.py`).
   - Sized as **App** scale (modular change requiring verification commands).
2. **Skill Activation:** The router activates `planning-with-contracts` and `designing-testable-seams`.
3. **Plan Output:** The agent generates `docs/plans/rate-limiting.md` defining:
   - Module boundaries and exact method signatures.
   - Verification commands: `pytest tests/test_limiter.py -q`.
   - Threat mitigations: IP spoofing behind reverse proxies.
4. **Phase Eviction:** Before writing code, the agent notes that planning is complete, evicts planning skill text, and proceeds with implementation.

---

## Recipe 2: Subagent Log Isolation (Shielding Main Context)

When executing iterative test or build cycles with high log verbosity, delegate to an ephemeral subagent to avoid poisoning the primary orchestrator context:

```json
// Tool call from Primary Session (running on pro / Sonnet):
{
  "tool": "invoke_subagent",
  "parameters": {
    "Role": "Test Runner",
    "Model": "flash",
    "Prompt": "Run `cargo test -q` in the repo root. If failures occur, fix compilation errors in `src/limiter.rs` without modifying public contracts. Return ONLY the pass/fail status and the resulting diff in <=10 lines."
  }
}
```

- **What Happens:**
  - The worker subagent absorbs dozens of `Compiling <crate>` lines and multiple test retry runs inside its own isolated context window.
  - The primary session never sees the noisy logs.
  - The subagent returns:
    ```text
    Status: ALL PASSED (42 passed, 0 warnings in 1.4s)
    Modified: src/limiter.rs (+4, -1)
    Diff: [compact diff]
    ```

---

## Recipe 3: Safe Multi-File Refactoring

To refactor code across modules without behavioral regression:

1. **Establish Green Baseline:**
   ```bash
   pytest -q  # Record exact passing count (e.g. 148 passed)
   ```
2. **Review Structural Graph:**
   Load `code-architecture-review` to inspect dependency couplings and circular imports.
3. **Execute in Atomic Slices (`refactor-execute`):**
   - Refactor one module at a time.
   - Re-run `pytest -q` after every atomic slice.
   - If tests fail, revert immediately (`git checkout -- <file>`) rather than stacking speculative fixes.
4. **Enforce Gate:** Run `layered-verification-gates` with zero warnings before committing.

---

## Recipe 4: Reviewing a PR Diff

Before merging changes, run an adversarial, multi-lens review:

```bash
# Capture branch diff against main
git diff origin/main...HEAD > /tmp/pr.diff

# Invoke review skill
/eng pr-review /tmp/pr.diff
```

The review evaluates five distinct axes:
1. **Contract Invariance:** Did public function signatures or API endpoints break?
2. **Error Handling:** Are there swallowed exceptions (`except: pass`) or missing timeout boundaries?
3. **Test Integrity:** Were tests deleted, assertions weakened, or `@ts-ignore` / `# noqa` tags added?
4. **Security & Secrets:** Are unsanitized strings passed to shell/SQL? Are secrets exposed?
5. **Token/Log Hygiene:** Do test commands use quiet flags (`-q`)?

---

## Recipe 5: Emergency Context Compaction & Resumption

When context utilization approaches 70% or session steps cross 50:

1. **Reach a Stable Point:** Pause active edits; run verification (`pytest -q` or `cargo test -q`).
2. **Write Checkpoint File:** Create `docs/CHECKPOINT.md`:
   ```markdown
   # Checkpoint: Rate Limiting Implementation
   - **Goal:** Implement token bucket rate limiter for auth routes.
   - **Current State:** `src/limiter.rs` created; unit tests passing (`cargo test -q`).
   - **Next Command:** Integrate limiter middleware into `src/server.rs`.
   - **Uncommitted Changes:** `git status` shows modified `src/limiter.rs`.
   ```
3. **Reset Context:**
   - **Claude Code:** Run `/compact keep: goal, uncommitted diffs, and docs/CHECKPOINT.md`.
   - **Antigravity (`agy`):** Exit session (`/exit` or New Chat) and resume:
     ```text
     Resume from docs/CHECKPOINT.md. Verify its state claims before taking any action.
     ```
4. **Continuity Verification:** The `SessionStart` hook re-reads `docs/CHECKPOINT.md` and checks `git status` before generating any code.

---

## CI/CD Pipeline Integration

Sample GitHub Actions workflow (`.github/workflows/verify-skills.yml`) to validate skill integrity:

```yaml
name: Verify Skills & Gates

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Lint Skill Word Limits & Frontmatter
        run: python3 scripts/lint-skills.py --words

      - name: Run Hook Unit Tests
        run: python3 -m unittest discover tests

      - name: Verify Router Accuracy
        run: python3 scripts/eval-router.py --self-test
```

---

## Troubleshooting Matrix

| Problem | Root Cause | Solution |
|---|---|---|
| `/compact` exits with code 2 in Claude Code | `precompact` hook blocked compaction because no checkpoint file was touched in the last 20 minutes. | Write or update `docs/CHECKPOINT.md` with current state, then re-run `/compact`. |
| Antigravity warns of `invalid hook` | `hooks.json` schema mismatch. | Re-run `python3 scripts/hooks/install-hooks.py --agy` to regenerate valid flat handler configurations. |
| Tool runs produce thousands of tokens of compile progress | Missing quiet flags in build/test commands. | Always append quiet flags: `cargo test -q`, `cargo build -q`, `pytest -q`, `npm test -s`. |
| Git commit fails with `absolute path` error | A skill or test file contains hardcoded machine paths (e.g. `~username/...`). | Replace absolute machine paths with repo-relative paths (`./` or `$REPO_ROOT`). |
| System prompt token overhead is high (>2,500 tokens) | All 54 skills are mounted in user skill directory. | Run `scripts/install.sh --claude --profile core` to mount only the 8 essential core skills. |
