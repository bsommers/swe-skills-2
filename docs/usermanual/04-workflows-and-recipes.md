# Chapter 4: Workflows & Practical Recipes

[← Back to User Manual](README.md) · [← Previous: Hooks & Context Guards](03-hooks-and-context-guards.md) · [Next: Authoring Skills →](05-authoring-skills.md)

This chapter provides step-by-step, copy-pasteable engineering recipes demonstrating how to combine `swe-skills` during everyday development tasks.

---

## Recipe 1: Scaffolding a New Project with Contracts

When starting a new project from scratch, prevent architecture drift before writing implementation code.

### Skills Used
- [`scaffolding-new-projects`](../../skills/scaffolding-new-projects/SKILL.md)
- [`planning-with-contracts`](../../skills/planning-with-contracts/SKILL.md)
- [`choosing-tools-and-substrates`](../../skills/choosing-tools-and-substrates/SKILL.md)

### Walkthrough

1. **Trigger via `/eng`:**
   ```text
   /eng scaffold a CLI tool in Python for converting CSV logs to Parquet format
   ```

2. **Agent actions:**
   - Evaluates substrates using [`choosing-tools-and-substrates`](../../skills/choosing-tools-and-substrates/SKILL.md) (standard library `argparse` + `pyarrow`).
   - Creates standard anatomy using [`scaffolding-new-projects`](../../skills/scaffolding-new-projects/SKILL.md):
     ```text
     my-project/
     ├── src/my_tool/
     ├── tests/
     ├── docs/
     ├── scripts/
     ├── README.md
     └── pyproject.toml
     ```
   - Writes contract in `docs/CONTRACTS.md` defining expected input schemas, exit codes, and error formats before writing `src/`.

3. **Verification:**
   ```bash
   python3 -m unittest discover tests
   ```

---

## Recipe 2: Hunting Silent Failures in Unfamiliar Code

When inheriting low-coverage code or diagnosing an issue where tests pass but production behavior is erratic.

### Skills Used
- [`hunting-silent-failures`](../../skills/hunting-silent-failures/SKILL.md)
- [`debugging-across-layers`](../../skills/debugging-across-layers/SKILL.md)
- [`test-coverage`](../../skills/test-coverage/SKILL.md)

### Walkthrough

1. **Trigger via `/eng`:**
   ```text
   /eng hunting-silent-failures src/data_pipeline/
   ```

2. **Agent actions:**
   - Audits all exception handlers in `src/data_pipeline/` for broad `except Exception: pass` or `except: return None`.
   - Replaces broad handlers with typed exceptions and structured logging.
   - Injects edge-case faults: empty inputs, malformed unicode, truncated JSON streams.
   - Measures actual branch execution via [`test-coverage`](../../skills/test-coverage/SKILL.md).

3. **Verification:**
   Run negative test assertions ensuring errors propagate cleanly rather than failing silently.

---

## Recipe 3: Executing Safe Architectural Refactoring

When restructuring a critical module or splitting a large monolith while maintaining strict behavioral invariance.

### Skills Used
- [`code-architecture-review`](../../skills/code-architecture-review/SKILL.md)
- [`refactor-execute`](../../skills/refactor-execute/SKILL.md)
- [`designing-testable-seams`](../../skills/designing-testable-seams/SKILL.md)

### Walkthrough

1. **Baseline Phase:**
   Run the full existing test suite to ensure 100% green state before modifying any files:
   ```bash
   pytest tests/
   ```

2. **Trigger via `/eng`:**
   ```text
   /eng refactor src/core/engine.py to decouple storage backend using testable seams
   ```

3. **Incremental Execution:**
   - [`refactor-execute`](../../skills/refactor-execute/SKILL.md) establishes an invariant test harness.
   - Introduces the storage interface protocol.
   - Migrates callers one by one in atomic commits.
   - Runs verification after every single file edit.

4. **Rollback Safety:**
   If any intermediate step breaks a test, the change is reverted immediately rather than patched forward blindly.

---

## Recipe 4: Multi-Lens Pre-Release Auditing

Before cutting a major release or merging a massive pull request.

### Skills Used
- [`running-multi-lens-audits`](../../skills/running-multi-lens-audits/SKILL.md)
- [`dependency-audit`](../../skills/dependency-audit/SKILL.md)
- [`api-contract-audit`](../../skills/api-contract-audit/SKILL.md)
- [`making-verifiable-claims`](../../skills/making-verifiable-claims/SKILL.md)

### Walkthrough

1. **Trigger via `/eng`:**
   ```text
   /eng audit repository across security, dependencies, and API contract lenses
   ```

2. **Parallel Audit Passes:**
   - **Lens 1 (Security & Dependencies):** Scans package manifests with [`dependency-audit`](../../skills/dependency-audit/SKILL.md) for CVEs, license compliance, and malicious supply chain patterns.
   - **Lens 2 (Contract Parity):** Runs [`api-contract-audit`](../../skills/api-contract-audit/SKILL.md) comparing OpenAPI routes to route handlers.
   - **Lens 3 (Claims & Verification):** Verifies all claims in `README.md` against real terminal outputs using [`making-verifiable-claims`](../../skills/making-verifiable-claims/SKILL.md).

3. **Output:**
   Generates a consolidated report in `docs/AUDIT_REPORT.md` with high/medium/low severity findings.

---

## Recipe 5: Context Compaction and Clean Session Handoffs

When an agent session spans multiple hours and context approaches capacity.

### Skills Used
- [`compacting-context-safely`](../../skills/compacting-context-safely/SKILL.md)
- [`handing-off-sessions`](../../skills/handing-off-sessions/SKILL.md)

### Walkthrough

1. **Context Guard Fires:**
   The `nudge` or `preinvocation` hook notifies the agent:
   ```text
   [context guard] Context usage is at 74% (148,000 / 200,000 tokens).
   Load `compacting-context-safely` and write a checkpoint.
   ```

2. **Creating the Checkpoint:**
   The agent writes `docs/CHECKPOINT.md`:
   - Exact user decisions made during the session.
   - Dead ends explored and discarded (to prevent repeating them).
   - Modified uncommitted files and git status.
   - Background tasks or subprocesses.
   - Exact next command to run.

3. **Executing Compaction:**
   - **Claude Code:** User or agent runs `/compact`. The `PreCompact` hook validates `docs/CHECKPOINT.md` and permits compaction. `SessionStart` immediately re-injects the checkpoint into the fresh window.
   - **Antigravity (`agy`):** Agent instructs the user to start a fresh chat (`/exit` or New Chat). The `SessionStart` hook reloads `docs/CHECKPOINT.md` on startup.

---

## Recipe 6: Automated SemVer Versioning and Release

When code changes are tested, documented, and ready for deployment.

### Skills Used
- [`committing-and-releasing-cleanly`](../../skills/committing-and-releasing-cleanly/SKILL.md)
- [`release`](../../skills/release/SKILL.md)
- [`keeping-docs-in-sync`](../../skills/keeping-docs-in-sync/SKILL.md)

### Walkthrough

1. **Run Verification Gate:**
   ```bash
   python3 -m unittest discover tests
   python3 scripts/lint-skills.py --words
   agy plugin validate .
   ```

2. **Trigger Release via `/eng`:**
   ```text
   /eng release
   ```

3. **Release Execution:**
   - Analyzes git commits since the last annotated tag (`vX.Y.Z`).
   - Calculates semantic bump (`patch`, `minor`, or `major`).
   - Synchronizes `docs/CHANGELOG.md` with reverse-chronological entry.
   - Prompts human for explicit approval before pushing tag to remote:
     ```text
     Proposed release: v0.5.1 -> v0.6.0 (minor)
     Proceed with tag creation and push? [y/N]
     ```

---

## Recipe 7: Adaptive Model Dispatch & Test-Time Compute Optimization

When balancing reasoning quality against token expenditure and API latency across complex multi-step workflows.

### Skills Used
- [`adaptive-model-routing`](../../skills/adaptive-model-routing/SKILL.md)
- [`token-finops`](../../skills/token-finops/SKILL.md)
- [`orchestrating-subagents`](../../skills/orchestrating-subagents/SKILL.md)

### Walkthrough

1. **Classify Workloads Along Scaling Axes:**
   - **Test-Time Compute (`flash` + High Thinking):** Bounded algorithmic problems with external verification (compilers, linters, unit test suites). Extended reasoning tokens simulate execution branches and self-correct at ~5–10x lower token cost.
   - **Parametric Scale (`pro` + High Thinking):** Unstated requirements, cross-module architecture (ADRs/RFCs), massive context windows (>200k tokens), and deep security audits.

2. **Trigger via `/eng`:**
   ```text
   /eng model dispatch subagents to implement parser logic and audit session security
   ```

3. **Subagent Execution Dispatch:**
   - **Algorithmic Worker (`flash` + High Thinking):**
     ```json
     {
       "TypeName": "self",
       "Role": "Parser Implementer",
       "Model": "flash",
       "Prompt": "Implement AST tokenizer in src/parser/tokens.ts with test-driven unit tests. Run pytest until green."
     }
     ```
   - **Security Reviewer (`pro` + High Thinking):**
     ```json
     {
       "TypeName": "research",
       "Role": "Security Auditor",
       "Model": "pro",
       "Prompt": "Audit src/auth/session.ts across all token refresh flows for concurrency race conditions and replay attacks."
     }
     ```

4. **Measurement & Verification:**
   Track token consumption and savings using [`token-finops`](../../skills/token-finops/SKILL.md) to verify cost efficiency targets.
