# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-09-22

### Added
- `skills/writing-user-guides/SKILL.md`: Guidance for authoring user guides in a `docs/` subdirectory with table of contents, getting started, examples, reference, and bidirectional links to root `README.md`.
- `skills/code-architecture-review/`: Structural architecture analysis via Graphify/AST with 5-section improvement plan generation.
- `skills/api-contract-audit/`: Schema drift and nullability audit for OpenAPI, GraphQL, Protobuf, and DTO contracts.
- `skills/refactor-execute/`: Safe, step-by-step refactoring engine with green-test gates, Fowler recipes, and rollback logging.
- `skills/test-coverage/`: Multi-ecosystem coverage measurement, risk-based gap analysis (P0/P1/P2), and shell test-quality checks.
- `skills/dependency-audit/`: Package vulnerability (CVE) scanning, CVSS score triage, and outdated dependency auditing.
- `skills/pr-review/`: Multi-lens PR and git diff review engine with GitHub CLI (`gh pr review`) integration.
- `skills/github-issues-script/`: Standalone batch issue creator (`scripts/create_issues.sh`) with `--dry-run`, coordinates, and heredoc escaping.
- `scripts/setup_repo_protections.sh`: Configurator for repository rulesets and branch protection gates.

### Changed
- `skills/using-swe-skills/SKILL.md`: Registered all 8 new skills across lifecycle groups.
- `skills/eng/SKILL.md`: Added shortcuts `arch`, `schema`, `refactor`, `cov`, `deps`, `diff`, and `tickets`.
- `README.md`: Updated catalog to 48 skills across entry, planning, architecture, AI systems, build, verify, and sustain groups.
- `skills/code-architecture-review/`, `skills/test-coverage/`, `skills/github-issues-script/`, `skills/release/`: Extracted reference materials into companion `references/` files to strictly satisfy wordcount budgets without losing detail.
- `docs/EVIDENCE.md`: Documented evidence sources for all 48 skills.
- `docs/TESTING.md`: Added pressure test scenarios for all skills (51 scenarios verified).

## [0.4.0] - 2026-09-21

### Added
- `skills/release/SKILL.md` & `skills/release/scripts/release.sh`: Automated Semantic Versioning (SemVer) release tool that analyzes commits, calculates bumps, updates changelogs, tags, and pushes to remote.

## [0.3.0] - 2026-09-21

### Added
- `skills/eng/SKILL.md`: `/eng` typed entry point. A skill name loads that skill, a shortcut word loads its target, and anything else goes to `using-swe-skills`. Routing stays in one place.
- `scripts/lint-skills.py`: checks the `/eng` shortcut table (targets exist, no duplicates, no shadowing of skill names).
- `tests/test_eng_shortcuts.py`: negative tests for those checks.
- `docs/TESTING.md`: three `eng` scenarios (not yet run with fresh agents).

### Changed
- `skills/using-swe-skills/SKILL.md`: mentions `eng` as a typed shortcut into the router.
- `README.md`: 39 skills; documents `/eng` and why it is not named `swe`.

### Fixed
- `skills/compacting-context-safely/SKILL.md`: differentiate Claude `/compact` from agy fresh sessions.

## [0.2.0] - 2026-09-19

### Added
- `scripts/eval-router.py`: Automated benchmark evaluation suite verifying router accuracy against 10 diverse tasks in `docs/TESTING.md` (10/10, 100% accuracy).
- `scripts/run-scenarios.py`: CLI scenario runner validating all 39 pressure testing scenarios against skill manifests.
- `scripts/hooks/git_pre_commit.py`: Git pre-commit hook enforcing secret detection, absolute path prohibition, version parity, and skill linter gates.
- `scripts/hooks/install-hooks.py`: Added `--git` flag to install the pre-commit hook into `.git/hooks/pre-commit`.
- Core reference templates:
  - `skills/planning-with-contracts/references/plan-template.md`
  - `skills/handing-off-sessions/references/checkpoint-template.md`
  - `skills/scaffolding-new-projects/references/scaffold-manifest.json`
- Comprehensive unit test suites in `tests/test_eval_router.py`, `tests/test_git_pre_commit.py`, and `tests/test_run_scenarios.py` (33 total unit tests passing).

### Changed
- `skills/planning-with-contracts/SKILL.md`: Referenced companion plan template.
- `skills/handing-off-sessions/SKILL.md`: Referenced companion checkpoint template.
- `skills/scaffolding-new-projects/SKILL.md`: Referenced companion scaffold manifest.
- `docs/HOOKS.md`: Documented git pre-commit hook installation and behavior.
- `docs/TESTING.md`: Recorded initial automated router benchmark run.

## [0.1.0] - 2026-09-19

### Added
- Initial release of 38 software engineering, planning, and architecture skills.
- Multi-platform plugin support for Antigravity (`plugin.json`), Claude Code (`.claude-plugin/`), and Cursor (`.cursor-plugin/`).
- Context guard hooks for `compacting-context-safely` (`scripts/hooks/context_guard.py`).
- Skill linter (`scripts/lint-skills.py`) and installation preview (`scripts/install.sh`).
