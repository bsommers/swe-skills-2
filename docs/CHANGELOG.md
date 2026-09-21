# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `skills/eng/SKILL.md`: `/eng` typed entry point. A skill name loads that skill, a shortcut word loads its target, and anything else goes to `using-swe-skills`. Routing stays in one place.
- `scripts/lint-skills.py`: checks the `/eng` shortcut table (targets exist, no duplicates, no shadowing of skill names).
- `tests/test_eng_shortcuts.py`: negative tests for those checks.
- `docs/TESTING.md`: three `eng` scenarios.

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
