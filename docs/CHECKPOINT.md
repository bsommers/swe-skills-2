# Checkpoint — 57 Skills Suite, `designing-exhaustive-test-cases` & `v0.14.0` — 2026-11-07

**Status:** COMPLETE & VERIFIED  
**Branch:** `main`  
**Working Tree:** Clean  
**Active Release Tag:** `v0.14.0`  

---

## 1. Goal & Context
Maintain, expand, and verify the 57-skill `swe-skills` engineering library across Claude Code, Antigravity (`agy`), and Cursor. Ensure every planned or built feature has exhaustive pre-build test cases designed before coding (`designing-exhaustive-test-cases`) and wired into the tiered post-build test suite (`layered-verification-gates`, `scripts/verify.sh`).

---

## 2. Done (With Evidence)
- **Added `designing-exhaustive-test-cases` (57th skill) & `references/test-matrix-template.md`**:
  - Mandates a 6-dimension pre-build test matrix (happy path, boundary/equivalence partitions, negative/malformed/adversarial inputs, idempotency/state/concurrency, dependency failure fakes, and operational/regression ratchets) mapped across the 8-tier suite hierarchy (`smoke`, `unit`, `integration`, `system`, `perf`, `stress`, `torture`, `security`), written RED-first before build time, and wired into `scripts/verify.sh` for automatic post-build execution.
- **Updated Planning, Verification, Coverage & Routing Skills**:
  - Updated `skills/planning-with-contracts/SKILL.md` and `references/plan-template.md` to require the Exhaustive Pre-Build Test Matrix and post-build `scripts/verify.sh` verification.
  - Updated `skills/layered-verification-gates/SKILL.md` and `skills/test-coverage/SKILL.md` to enforce pre-build exhaustive test case design and post-build suite integration.
  - Added routing in `skills/using-swe-skills/SKILL.md`, `/eng` shortcuts (`tdd`, `testcases`) in `skills/eng/SKILL.md`, and `core`/`build`/`review` profile entries in `scripts/install.sh`.
- **Added Exhaustive Post-Build Test Suite (`tests/test_exhaustive_test_design.py`) & Tri-OS Support (Windows, macOS, Linux)**:
  - Updated `skills/designing-plugin-contracts/SKILL.md` and added `references/cross-platform-driver-architecture.md` so driver architectures target **Windows, macOS, and Linux** from day one (ConPTY/Job Objects vs. POSIX PTY/process groups, Named Pipes vs. Unix domain sockets, `MoveFileExW` vs. `rename`, `%APPDATA%` vs. `~/Library/Application Support` vs. `$XDG_CONFIG_HOME`, injected syscall seams, and tri-OS contract test suites).
  - Updated `skills/test-coverage/SKILL.md`, `references/COVERAGE_TOOLS_MATRIX.md`, `templates/COVERAGE_REPORT_TEMPLATE.md`, `scripts/shell_function_reachability.sh`, and `skills/layered-verification-gates/verify.sh.template` for full **Windows, macOS, and Linux** portability (eliminating Bash 4+ `mapfile`, GNU-only `gensub`, and CRLF line-ending issues).
  - Added 11 automated tests in `tests/test_exhaustive_test_design.py` verifying skill structure, reference template, tri-OS driver and coverage support, CRLF shell reachability, cross-skill integration, router dispatch, installer/docs synchronization, and zero-warning lint compliance (total suite: 72/72 passing).
- **Synchronized Documentation & Installed Across All Targets**:
  - Updated `README.md`, `CHANGELOG.md`, `docs/EVIDENCE.md`, `docs/TESTING.md`, `docs/running.md`, `docs/usermanual/`, and manifests (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`) to `0.14.0` (57 skills).

---

## 3. Failed / Blocked
- None. All validations pass 100% green.

---

## 4. State That May Have Changed
- Local symlinks in `~/.cursor/skills`, `~/.agents/skills`, and `~/.claude/skills` point to `~/src/swe-skills-2/skills/` (57 skills linked).
- Antigravity plugin `swe-skills` active with 57 skills and 1 hook (`context-guard`).

---

## 5. Next Steps Upon Resuming
1. Verify repository state:
   ```bash
   git status -sb && python3 -m unittest discover tests && python3 scripts/lint-skills.py --words
   ```
