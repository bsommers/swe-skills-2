# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (CI and community)
- `.github/workflows/ci.yml`: lint, unit tests, and installer dry run on every PR and push to `main`; read-only token, SHA-pinned `actions/checkout`, concurrency cancel, 10-minute timeout.
- `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue forms (bug report, skill feedback, skill proposal), and a PR template with the contribution checklist.
- `scripts/lint-skills.py`: fails when manifest versions (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`, marketplace entry) differ or a manifest is invalid JSON.

### Fixed
- `tests/test_context_guard.py`: the hook-installer dry-run test no longer assumes `uv` is installed (it failed on runners without `uv`).

### Changed
- `scripts/lint-skills.py`: the 900-word body limit is now explicitly soft (warns); bodies over 1035 words (15% over) fail lint. Lint also fails when a skill is missing from the README table, `docs/EVIDENCE.md`, or `docs/TESTING.md`, and accepts `--root DIR`.
- `tests/test_exhaustive_test_design.py`: the lint test allows soft word-count warnings and still fails on errors and any other warning.

### Added
- `tests/test_lint_skills.py`: fixture-tree tests for the soft/hard word limits and documentation-coverage checks.
- `typesafe-ai` rows in `docs/EVIDENCE.md` and `docs/TESTING.md`.

## [0.17.0] - 2026-11-08

### Added
- `skills/using-local-tool-registry/` (`references/local-tools-and-vm-catalog.md`), `scripts/tool-registry.py`, & `docs/tool-registry.seed.json`: Searchable local tool and VM registry indexing 110+ repositories in `~/src` (highlighting `cvm`, `win-devvm`, `gha-vm-runners`, `fedora-vms`, `freebsd-kvm`, `flowscope`, `synth`, `eval`, `gitnexus`, `ontologic`, `cli-anything`) with `update`, `search`, `recommend --phase`, `show`, and `list` commands (`/eng tools`, `/eng vms`, `/eng registry`).
- `skills/running-local-ci/` (`references/local-ci-and-vm-runners.md`): Standing local-first CI rule and execution guide that runs all linters, builds, and test matrices locally (`scripts/verify.sh`, `~/src/gha-vm-runners/local-ci.sh`, `cvm`, `win-devvm`, `gha-vm-runners.sh`) and conserves hosted GitHub Actions CI minutes unless explicitly overridden by the user (`/eng local-ci`, `/eng ci`).
- `skills/rendering-graphic-examples/` & `references/svg-png-pipeline.md`: Deterministic SVG + Hi-DPI PNG visual generation skill for accompanying documentation recipes, architecture guides, and CLI telemetry (`/eng graphics`, `/eng svg`).
- `skills/showcasing-graphics-in-docs/` & `references/futuristic-neon-grid-theme.md`: Visual documentation styling skill featuring the signature futuristic obsidian-black background (`#050811`) with light-blue neon cyber grid (`#00e5ff` / `#38bdf8`), high-contrast HUD panels, and user-theme override support (`/eng showcase`, `/eng neon`).
- `skills/designing-logos-and-icons/` & `references/logo-and-icon-templates.md`: Brand and icon kit skill generating the wide hero banner (`docs/assets/logo.{svg,png}`), square `512x512` plugin icon (`assets/logo.{svg,png}` wired into `plugin.json` `"logo"`, and `docs/assets/icon.{svg,png}`), and `64x64` subsystem neon icons (`docs/assets/icons/icon-*.{svg,png}`) (`/eng logo`, `/eng icons`).
- `skills/building-github-pages-sites/` & `references/github-pages-template.md`: GitHub Pages showcase skill and deterministic generator (`scripts/build-pages.py`) producing `docs/index.html` and `docs/.nojekyll` with live 68-skill search, category filters, SVG/PNG visual gallery, and copy-pasteable recipes (`/eng pages`, `/eng gh-pages`).
- `scripts/render-graphics.py` & `scripts/build-pages.py`: Deterministic generators producing 15 `.svg` + 15 `.png` neon-grid graphics (including `workflow-local-tools-and-ci.{svg,png}`) and the accompanying GitHub Pages portal (`docs/index.html`).
- `tests/test_graphics_and_pages.py`: Automated tests verifying the 6 new skills, `scripts/tool-registry.py`, updated documentation & CI skills, XML/PNG validity of all 30 rendered graphic assets, `plugin.json` logo wiring, and zero broken links across `docs/index.html` and `README.md`.

### Changed
- `skills/writing-user-guides/SKILL.md` & `skills/keeping-docs-in-sync/SKILL.md`: Expanded to govern the complete documentation suite (`README.md`, `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, `docs/how-to.md`, `docs/usermanual/`, rendered graphics, and `docs/index.html`).
- `skills/hardening-ci-workflows/SKILL.md`, `skills/layered-verification-gates/SKILL.md`, `skills/committing-and-releasing-cleanly/SKILL.md`, & `templates/AGENTS.snippet.md`: Integrated the standing local-first CI rule (`running-local-ci`) and local tool/VM discovery (`using-local-tool-registry`) to conserve hosted GitHub Actions minutes.
- Refreshed `README.md`, `docs/README.md`, `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, `docs/how-to.md`, `docs/usermanual/`, `docs/EVIDENCE.md`, `docs/TESTING.md`, and `docs/CHECKPOINT.md` with embedded SVG/PNG visual examples and synchronized all manifests to `0.17.0` (68 skills).

## [0.16.0] - 2026-11-07

### Added
- `skills/driving-browsers-for-qa/` with `references/` (tool choice, `playwright.config.template.ts`, `plan-steps.e2e.template.ts`, `QA-REPORT.template.md`): automating a manual QA plan with Playwright and recorded evidence against a live stack (62 skills total).
- `/eng` shortcuts `qa-drive` and `qa-report`; `scripts/install.sh` adds the skill to the `build` and `review` profiles.

### Changed
- Synchronized all manifests (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`), `README.md`, `docs/running.md`, `docs/usermanual/`, and `docs/CHECKPOINT.md` to `0.16.0` (62 skills).

## [0.15.0] - 2026-11-07

### Added
- `skills/compacting-context-safely/references/cadence-and-hooks.md`: Reference guide for dual-trigger periodic checkpointing and compaction (automated hook cadence + natural task-boundary self-checks).
- `skills/hardening-ci-workflows/`, `skills/bounding-untrusted-resource-use/`, `skills/controlling-processes-safely/`, & `skills/keeping-event-loops-responsive/`: Four new build/security skills covering CI workflow hardening, untrusted allocation bounds, safe PID/process signaling, and non-blocking event-loop waiters (61 skills total).

### Changed
- `scripts/hooks/context_guard.py` & `docs/HOOKS.md`: Added periodic checkpoint cadence reminders every `12` assistant turns in Claude (`SWE_SKILLS_CHECKPOINT_CADENCE_TURNS`) and every `25` steps in Antigravity (`SWE_SKILLS_CHECKPOINT_CADENCE_STEPS`) when no fresh `<20m` checkpoint exists; expanded `context_guard.py report` with `recommendation:` (`OK`, `CHECKPOINT_DUE`, `COMPACT_OR_RESET_NOW`) and `hooks:` installation diagnostics.
- `skills/compacting-context-safely/SKILL.md`, `skills/handing-off-sessions/SKILL.md`, `skills/supervising-autonomous-sessions/SKILL.md`, & `skills/writing-agent-context-files/SKILL.md`: Integrated periodic checkpoint cadence, hook verification (`context_guard.py report`), and phase-transition compaction rules.
- `tests/test_context_guard.py`: Added automated tests for periodic turn/step checkpoint cadence and `report` diagnostics (`74/74` unit tests passing).
- Synchronized all manifests (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`), `README.md`, `docs/running.md`, `docs/usermanual/`, and `docs/CHECKPOINT.md` to `0.15.0` (61 skills).

## [0.14.0] - 2026-11-07

### Added
- `skills/designing-exhaustive-test-cases/` & `references/test-matrix-template.md`: Pre-build exhaustive test case design skill requiring a 6-dimension test matrix (happy path, boundary/equivalence partitions, negative/malformed/adversarial inputs, idempotency/state/concurrency, dependency failure fakes, and operational/regression ratchets) plus tri-OS driver parity (`Windows`, `macOS`, `Linux`), mapped across the 8-tier test hierarchy (`smoke`, `unit`, `integration`, `system`, `perf`, `stress`, `torture`, `security`), written RED-first before build time, and wired permanently into `scripts/verify.sh` for automatic post-build execution.
- `skills/designing-plugin-contracts/references/cross-platform-driver-architecture.md`: Cross-platform driver architecture reference for **Windows, macOS, and Linux** covering ConPTY/Job Objects vs. POSIX PTY/process groups, Named Pipes vs. Unix domain sockets (`< 104` byte macOS `sun_path`), atomic file writes (`MoveFileExW` vs. `rename`), standard OS directories (`%APPDATA%`, `~/Library/Application Support`, `$XDG_CONFIG_HOME`), injected syscall seams for cross-host unit coverage, and tri-OS contract test suites.
- `tests/test_exhaustive_test_design.py`: Automated test suite (`TestExhaustiveTestDesignSkill` and `TestTriOSCoverageAndDriverArchitecture`) verifying `designing-exhaustive-test-cases`, tri-OS driver architecture and test coverage, portable `verify.sh.template` (no Bash 4+ `mapfile` or GNU-only `gensub`), CRLF/LF `shell_function_reachability.sh` execution, router dispatch, `/eng` shortcuts (`tdd`, `testcases`, `driver`, `drivers`), and zero-warning lint compliance.
- `scripts/install.sh`: Added `designing-exhaustive-test-cases` (`core`, `build`, `review`) and `designing-plugin-contracts` (`build`).

### Changed
- `skills/designing-plugin-contracts/SKILL.md`: Expanded plugin/driver contract guidance to mandate **Windows, macOS, and Linux** driver support from day one with OS-agnostic host contracts and tri-OS contract test suites.
- `skills/test-coverage/SKILL.md`, `references/COVERAGE_TOOLS_MATRIX.md`, `templates/COVERAGE_REPORT_TEMPLATE.md`, & `scripts/shell_function_reachability.sh`: Added Windows, macOS, and Linux coverage tool matrix (`cargo llvm-cov`, `llvm-cov`, `pytest-cov`, `vitest`, `coverlet`), OS-gated driver branch auditing, and Windows CRLF/POSIX `find` portability in `shell_function_reachability.sh`.
- `skills/layered-verification-gates/verify.sh.template`: Replaced Bash 4+ `mapfile` and GNU-gawk `gensub` with POSIX/Bash 3.2 equivalents and portable `PYTHON_BIN` detection so `verify.sh` runs cleanly on Windows (Git Bash/MSYS2/WSL), macOS, and Linux.
- `scripts/lint-skills.py` & `scripts/hooks/context_guard.py`: Added Windows path linting (`C:\Users\...`) and native tri-OS state directory resolution (`%LOCALAPPDATA%` on Windows, `~/Library/Caches` on macOS, `$XDG_STATE_HOME` on Linux).
- `skills/planning-with-contracts/SKILL.md` & `references/plan-template.md`: Added mandatory Pre-Build Exhaustive Test Matrix section and post-build `scripts/verify.sh` task verification.
- `skills/using-swe-skills/SKILL.md` & `skills/eng/SKILL.md`: Added routing rule and `/eng` shortcuts (`tdd`, `testcases`, `driver`, `drivers`).
- Expanded skills library from 56 to 57 skills across `README.md`, `docs/running.md`, `docs/usermanual/`, `docs/EVIDENCE.md`, and `docs/TESTING.md`, and synchronized all manifests to `0.14.0`.

## [0.13.0] - 2026-11-05

### Added
- `skills/designing-uniform-surfaces/`: Surface uniformity skill ensuring commands, flags, endpoints, config keys, and sibling modules share consistent naming, argument order, output shapes, and error semantics.
- `scripts/install.sh`: Added `designing-uniform-surfaces` to the `build` installation profile.

### Changed
- `skills/planning-with-contracts/SKILL.md`: Referenced `designing-uniform-surfaces` when specifying sibling commands, flags, or API surfaces.
- `skills/token-finops/SKILL.md`: Tightened model detection and pricing source prose below the 900-word lint threshold (zero lint warnings across all 56 skills).
- Expanded skills library from 55 to 56 skills across `README.md`, `skills/using-swe-skills/`, `docs/running.md`, `docs/usermanual/`, `docs/EVIDENCE.md`, and `docs/TESTING.md`.
- Synchronized all manifests to `0.13.0` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

## [0.12.0] - 2026-11-03

### Added
- `skills/layered-verification-gates/verify.sh.template` & `references/TEST_TIERS_AND_TRIAGE.md`: Token-cheap, composable, hierarchical verification runner (`--quick`, `--tier`, `--only`, `--match`, `--failed`, `--list`, `--status`, `--report`) producing one-line terminal verdicts plus structured reports (`STATUS`, `summary.tsv`, `report.md`, `junit.xml`, and per-stage `fail.txt`/`log` in `target/verify/`), alongside an 8-tier test taxonomy (`smoke`, `unit`, `integration`, `system`, `perf`, `stress`, `torture`, `security`) and failing-test triage playbook.
- `scripts/chain-session.sh` & `docs/AUTONOMY_AND_PERMISSIONS.md`: Deterministic 5-step session chaining (`Checkpoint → Compact → Handoff → Clear → Resume`) and autonomous permission configuration reference across Claude Code, Antigravity, and Cursor.
- `scripts/hooks/git_pre_commit.py`: Pre-commit guard rejecting duplicate `docs/CHANGELOG.md` files so the root `CHANGELOG.md` remains the single canonical changelog.

### Changed
- `skills/scaffolding-new-projects/SKILL.md` & `references/scaffold-manifest.json`: Expanded project scaffolding to create the full hierarchical `tests/{smoke,unit,integration,system,perf,stress,torture,fixtures}/` layout and wire `scripts/verify.sh` on day one.
- `skills/test-coverage/SKILL.md` & `templates/COVERAGE_REPORT_TEMPLATE.md`: Added 8-tier suite completeness auditing, runner composability checks, and root-cause triage & remediation guidance for failing tests.
- `skills/handing-off-sessions/SKILL.md` & `skills/compacting-context-safely/SKILL.md`: Integrated 5-step session chaining (`scripts/chain-session.sh`) across documentation and user manual guides.
- Removed duplicate `docs/CHANGELOG.md` and synchronized all references and manifests to `0.12.0` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

## [0.11.0] - 2026-10-29

### Added
- `skills/building-release-binaries/`: Per-platform release binary skill that picks up after `release` pushes a tag: builds from a worktree of the tag on the host that can link each target, uses consistent archive names, verifies each unpacked archive (architecture, `--version`, dynamic deps, minimum OS), merges `SHA256SUMS` across hosts, and asks before uploading.
- `skills/building-release-binaries/scripts/build-binaries.sh`: Generic Rust build script that reads the binary name and version from `Cargo.toml`, builds the host's native targets, writes `SHA256SUMS`, and optionally uploads (`--upload`, `--create-release`).
- `scripts/install.sh`: Added `building-release-binaries` to the profile that includes `release`.

### Changed
- `skills/release/SKILL.md`: Hands off to `building-release-binaries` once the tag is pushed.
- Expanded skills library from 54 to 55 skills across `README.md`, `skills/using-swe-skills/`, `docs/usermanual/`, `docs/EVIDENCE.md`, and `docs/TESTING.md`.
- Synchronized all manifests to `0.11.0` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

## [0.10.0] - 2026-10-26

### Added
- `skills/security-best-practices/`: Defense-in-depth security engineering skill covering constant-time authentication checks, explicit multi-tenant query isolation (preventing IDOR), AEAD cryptography, strict input allowlist schemas, leak-free error handling, and supply chain CVE auditing.
- `skills/architecture-best-practices/`: Architectural structuring skill enforcing hexagonal dependency inversion (domain core decoupled from I/O and frameworks), versioned DTO contract boundaries, acyclic dependency graphs (DAG), discrete pipeline staging, and resilience patterns (timeouts, circuit breakers).
- `skills/eng/SKILL.md`: Added `/eng security` and `/eng patterns` shortcuts routing directly to the new skills.
- `scripts/install.sh`: Added `architecture-best-practices` to the `build` profile and `security-best-practices` to the `review` profile.

### Changed
- Expanded skills library from 52 to 54 skills across `README.md`, `skills/using-swe-skills/`, `docs/usermanual/`, `docs/EVIDENCE.md`, and `docs/TESTING.md`.
- Synchronized all manifests to `0.10.0` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

## [0.9.0] - 2026-10-25

### Added
- `docs/`: Comprehensive multi-document production documentation hub (`docs/README.md`, `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, `docs/how-to.md`).
- `docs/diagrams/`: Multi-format architectural visual models across three distinct formats:
  - `docs/diagrams/ascii_architecture.txt`: High-resolution terminal-ready ASCII schematic.
  - `docs/diagrams/architecture.mmd`, `docs/diagrams/execution_flow.mmd`, `docs/diagrams/context_lifecycle.mmd`: Standalone Mermaid diagrams.
  - `docs/diagrams/architecture.drawio`, `docs/diagrams/execution_flow.drawio`: Native draw.io XML vector diagrams.
- `scripts/install.sh`: Added `--profile` support (`core`, `build`, `review`, `ship`, `all`) to allow selective installation of skill subsets, reducing static system prompt catalog token overhead by ~85%.

### Changed
- `skills/compacting-context-safely/SKILL.md`: Added context window turn replay multiplier analysis and quiet-flag tool output suppression directives (`cargo test -q`, `pytest -q`, `npm test -s`).
- `skills/orchestrating-subagents/SKILL.md`: Added Rule 12 (**Subagent Log Isolation**) and delegation row for iterative build/test/lint loops to quarantine noisy compiler progress inside ephemeral `flash` subagents, shielding the primary orchestrator session from context bloat.
- `skills/adaptive-model-routing/SKILL.md`: Documented build/test loop routing to `flash` / `flash_lite` worker subagents for log isolation.
- `skills/layered-verification-gates/SKILL.md`: Mandated quiet verification flags by default (`-q`) across all toolchains to preserve turn token budget.
- `skills/using-swe-skills/SKILL.md`: Added Bounded Active Set discipline (max 1–3 skills in memory concurrently) and Phase-Transition Eviction rules.
- Synchronized all manifests to `0.9.0` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

### Fixed
- `scripts/hooks/install-hooks.py`: Corrected Antigravity (`agy_hooks()`) JSON structure to use flat handler lists for `SessionStart` and `PreInvocation` with top-level named hook object, resolving `agy plugin validate .` errors.

## [0.8.0] - 2026-10-25

### Added
- `skills/building-installers-and-onboarding/`: Build-time and post-build remediation skill covering multi-target installers (`--local` user home default, `--global`, and `--prefix` custom path), idempotent `<tool> init` and `doctor` setup commands, progressive in-tool `Next steps:` CLI breadcrumbs, and synchronized user guide workflows.
- `skills/building-installers-and-onboarding/references/installer-template.sh`: Reusable POSIX/Bash installer template supporting `--local`, `--global`, `--prefix`, `--dry-run`, `--force`, `--uninstall`, and `$PATH` verification.
- `skills/building-installers-and-onboarding/references/onboarding-cli-patterns.md`: User journey state machine, `print_next_steps` CLI helper, `<tool> guide` workflow subcommand pattern, and post-build remediation checklist.
- `skills/eng/SKILL.md`: Added `/eng onboard` shortcut routing to `building-installers-and-onboarding`.
- `scripts/hooks/context_guard.py`: Added cold-cache idle resume detection (`SWE_SKILLS_IDLE_MINUTES`, `SWE_SKILLS_IDLE_MIN_TOKENS`) for `nudge` (`UserPromptSubmit`) and `preinvocation` (`PreInvocation`) to warn when the 5-minute prompt cache has expired (`12.5x` cold-cache rebuild penalty) and advise checkpointing + `/compact` or `/clear`.
- `docs/banner.txt` & `scripts/banner.sh`: Added terminal ASCII banner asset, helper script, and vector SVG banner in `README.md`.

### Changed
- `skills/compacting-context-safely/SKILL.md` & `skills/handing-off-sessions/SKILL.md`: Added pause/resume workflow rules around Anthropic's 5-minute prompt cache TTL cliff and stopping background jobs before breaks.
- `skills/writing-user-guides/SKILL.md`: Expanded Getting Started requirements to cover multi-scope installation (`--local`, `--global`, `--prefix`), `<tool> init`, and the immediate `init → verify → first run` sequence.
- `skills/building-small-cli-tools/SKILL.md`: Linked multi-step CLI onboarding and installers to `building-installers-and-onboarding`.
- `skills/using-swe-skills/SKILL.md`, `README.md`, `docs/usermanual/`, `docs/EVIDENCE.md`, `docs/TESTING.md`: Registered `building-installers-and-onboarding` (52 skills total) and documented direct `SKILL.md` loading when skills are pruned from `~/.claude/skills/`.
- Synchronized all manifests to `0.8.0` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

### Fixed
- `scripts/hooks/install-hooks.py`: Updated `uv` hook runner from `uv run` to `uv run --no-project` so hook execution succeeds inside target repositories whose `pyproject.toml` lacks a `[project]` table.

## [0.7.1] - 2026-09-30

### Added
- `docs/usermanual/04-workflows-and-recipes.md`: Added Recipe 7 detailing Adaptive Model Dispatch & Test-Time Compute Optimization with subagent configuration examples for fast reasoning vs. architectural review.
- `templates/opengsd/adaptive-model-profile.json`: Added `tdd_cycle` stage configured with `flash` and high thinking for algorithmic logic, red-green test generation, and bounded refactors.

### Changed
- `skills/adaptive-model-routing/SKILL.md`: Added decision boundary between Test-Time Compute (`flash` + High Thinking) and Parametric Capacity (`pro` + High Thinking), distinguishing bounded algorithmic tasks from large-scale architectural synthesis.
- `docs/EVIDENCE.md`: Decoupled provenance documentation from proprietary Dark Factory and DarkOS citations, replacing them with generalized software engineering standards (spec-driven development, prototypical template isolation, complexity budgets).
- Synchronized all manifests to `0.7.1` (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`).

## [0.7.0] - 2026-09-28

### Added
- `skills/nix-environments/`: Progressive enhancement skill establishing a 3-tier environment hierarchy (Hermetic Nix devShell → Native Host Toolchain → Container/CI fallback) to eliminate host dependency barriers while guaranteeing bit-for-bit system reproducibility.
- `templates/nix/`: Production-ready hybrid templates including `flake.nix` (multi-arch devShell wrapping Python, `uv`, `pkg-config`, `openssl`, and `git`), legacy `shell.nix`, and `envrc` for direnv.
- `skills/eng/SKILL.md`: Added `/eng nix` shortcut routing directly to `nix-environments`.

### Fixed
- Fixed retro DOS ASCII logo alignment to strict 80-column standard width across `README.md` and `docs/usermanual/README.md`, eliminating ragged line wraps in terminal and browser viewports.

### Changed
- `skills/using-swe-skills/SKILL.md`: Registered `nix-environments` in core skill router table.
- Expanded skill catalog to 51 skills across `README.md` and `docs/usermanual/`.

## [0.6.0] - 2026-09-28

### Added
- `skills/adaptive-model-routing/`: Dynamic LLM tier selection and model gating to conserve token consumption across frontier workflows.
- `scripts/hooks/model_router.py`: `PreToolUse` hook for Antigravity intercepting `invoke_subagent` calls to automatically select model tiers (`pro`, `flash`, `flash_lite`).
- `scripts/hooks/install-hooks.py`: Added `--uv` and `--no-uv` runner flags to prioritize Astral `uv` for fast hook execution.
- `docs/usermanual/`: Comprehensive 7-chapter user manual covering Getting Started, Skills Catalog, Hooks & Context Guards, Workflows & Practical Recipes, Authoring Skills, CLI Reference, and Troubleshooting/FAQ.
- ASCII retro DOS style logo banner across `README.md` and `docs/usermanual/README.md`.

### Changed
- `README.md`: Integrated DOS ASCII banner, added User Manual chapter index, and expanded skills catalog to 50 skills.
- `LICENSE`: Updated project license from MIT to Apache-2.0.
- `skills/eng/SKILL.md`: Added `model` shortcut for `adaptive-model-routing`.
- `skills/using-swe-skills/SKILL.md`: Registered `adaptive-model-routing` in general router.

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
