# Running, Installation & Configuration

## 1. Prerequisites

- **Operating System:** Linux, macOS, or Windows (Git Bash / MSYS2 / WSL2 / native Python)
- **Runtime:** Python 3.10+ (standard library only for core hooks; no external pip packages required)
- **Optional Tooling:**
  - [`uv`](https://github.com/astral-sh/uv) (recommended for ultra-fast hook execution)
  - `inkscape`, `rsvg-convert`, or ImageMagick (`magick`) (for rasterizing `.svg` assets to `.png` via `scripts/render-graphics.py`)
  - `git` 2.25+
  - Supported agent harnesses: **Claude Code**, **Antigravity (`agy`)**, or **Cursor**

---

## 2. Installation Targets & Profiles

Use `scripts/install.sh` to install skills globally or on a per-project basis.

### Targets

```bash
# User-level installation (default is symlinks so repository edits reflect instantly)
scripts/install.sh --claude     # Installs to ~/.claude/skills/
scripts/install.sh --agy        # Installs plugin via `agy plugin install .`
scripts/install.sh --cursor     # Installs to ~/.cursor/skills/
scripts/install.sh --agents     # Installs cross-runtime alias ~/.agents/skills/
scripts/install.sh --all        # Installs across all available targets

# Project-level installation
scripts/install.sh --project /path/to/my-repo
```

### Profile-Based Surfacing (Token Conservation)

By default, runtimes load the frontmatter descriptions of all installed skills into the initial system prompt, consuming ~3,200 input tokens on every turn. Use `--profile` to install only the skills needed for your workflow:

```bash
# Install core profile (9 skills; drops prompt token overhead by ~85%)
scripts/install.sh --claude --profile core

# Switch to review profile for auditing and testing
scripts/install.sh --claude --profile review
```

| Profile | Skill Count | Estimated Catalog Overhead | Intended Use Case | Included Skills |
|---|:---:|:---:|---|---|
| **`core`** | 11 | ~480 tokens | General development, daily coding | `using-swe-skills`, `planning-with-contracts`, `designing-exhaustive-test-cases`, `compacting-context-safely`, `layered-verification-gates`, `running-local-ci`, `using-local-tool-registry`, `committing-and-releasing-cleanly`, `orchestrating-subagents`, `token-finops`, `adaptive-model-routing` |
| **`build`** | 22 | ~990 tokens | Greenfields, scaffolding, CLI tools, drivers | `core` + `architecture-best-practices`, `building-small-cli-tools`, `building-code-generators`, `building-installers-and-onboarding`, `designing-plugin-contracts`, `designing-testable-seams`, `designing-uniform-surfaces`, `engineering-for-determinism`, `scaffolding-new-projects`, `debugging-across-layers`, `driving-browsers-for-qa` |
| **`review`** | 20 | ~920 tokens | PR audits, security review, QA | `core` + `security-best-practices`, `pr-review`, `driving-browsers-for-qa`, `code-architecture-review`, `dependency-audit`, `api-contract-audit`, `test-coverage`, `running-multi-lens-audits`, `hunting-silent-failures` |
| **`ship`** | 20 | ~920 tokens | Releases, binaries, docs, graphics & GitHub Pages | `core` + `release`, `building-release-binaries`, `writing-pull-requests`, `keeping-docs-in-sync`, `writing-user-guides`, `rendering-graphic-examples`, `showcasing-graphics-in-docs`, `designing-logos-and-icons`, `building-github-pages-sites`, `github-issues-script` |
| **`all`** | 69 | ~3,200 tokens | Full comprehensive library | All 69 skills in `skills/` |

---

## 3. Installing Lifecycle Hooks

To enable automatic periodic checkpoint cadence reminders, `/compact` protection, and adaptive subagent model routing:

```bash
# Claude Code hooks (merges into ~/.claude/settings.json)
python3 scripts/hooks/install-hooks.py --claude

# Antigravity hooks (writes plugin root hooks.json)
python3 scripts/hooks/install-hooks.py --agy
agy plugin uninstall swe-skills && agy plugin install .

# Git pre-commit hook (protects against secret leaks & linter failures)
python3 scripts/hooks/install-hooks.py --git
```

---

## 4. CLI Utilities Reference

| Command | Purpose |
|---|---|
| `python3 scripts/lint-skills.py --words` | Validates frontmatter, word count limits, cross-references, and naming across all 69 skills. |
| `python3 scripts/tool-registry.py search "<query>"` | Searches or updates (`update`, `recommend`, `show`, `list`) the centralized local tool & VM registry across `~/src`. |
| `python3 scripts/render-graphics.py` | Deterministically generates all 15 `.svg` + 15 `.png` neon-grid logos, icons, and example visuals. |
| `python3 scripts/build-pages.py` | Generates the accompanying GitHub Pages showcase (`docs/index.html` + `docs/.nojekyll`). |
| `python3 -m unittest discover tests` | Executes full automated test suite (hooks, router, exhaustive TDD, tool registry, graphics, and GitHub Pages). |
| `agy plugin validate .` | Validates plugin manifest (`plugin.json`), logo (`assets/logo.svg`), hooks (`hooks.json`), and skill discovery. |
| `python3 scripts/eval-router.py --self-test` | Evaluates router accuracy against the 10 benchmark scenarios in `docs/TESTING.md`. |
| `python3 scripts/hooks/context_guard.py report` | Outputs context utilization, active turn stats, `recommendation:`, `hooks:`, and checkpoint status. |
| `scripts/chain-session.sh [--claude\|--agy]` | Chains fresh CLI sessions automatically from `docs/HANDOFF.md` or `docs/CHECKPOINT.md` until `**Status:** COMPLETE`. |

---

## 5. Environment Variables

All configuration settings are optional and controlled via environment variables:

| Variable | Default | Purpose |
|---|:---:|---|
| `SWE_SKILLS_CONTEXT_LIMIT` | `200000` | Context window ceiling in tokens. |
| `SWE_SKILLS_CONTEXT_PCT` | `70` | Threshold percentage to trigger first capacity compaction nudge. |
| `SWE_SKILLS_CONTEXT_PCT_STEP` | `10` | Incremental percentage to re-nudge. |
| `SWE_SKILLS_CHECKPOINT_CADENCE_TURNS` | `12` | Periodic assistant-turn interval in Claude Code to nudge for a checkpoint when none is fresh (`0` disables). |
| `SWE_SKILLS_CHECKPOINT_CADENCE_STEPS` | `25` | Periodic step interval in Antigravity (`agy`) to nudge for a checkpoint when none is fresh (`0` disables). |
| `SWE_SKILLS_IDLE_MINUTES` | `30` | Idle minutes before cold prompt cache resume nudge. |
| `SWE_SKILLS_AGY_STEP_LIMIT` | `50` | Step count threshold in Antigravity before capacity nudge. |
| `SWE_SKILLS_AGY_BYTES_LIMIT` | `500000` | Transcript byte ceiling in Antigravity before capacity nudge. |
| `SWE_SKILLS_MODEL_ROUTER_ENABLED` | `1` | Set to `0` to disable automatic subagent model routing. |
| `SWE_SKILLS_MODEL_ROUTER_DEFAULT_TIER` | `flash` | Fallback model tier for routine subagents (`flash` / `flash_lite`). |
| `SWE_SKILLS_CONTEXT_GUARD_BLOCK` | `1` | Set to `0` to allow manual `/compact` without a fresh checkpoint. |
| `SWE_SKILLS_CHECKPOINT_FRESH_MINUTES` | `20` | Max age in minutes for a checkpoint to be accepted by `/compact` and cadence checks. |

---

## 6. Exit Codes

| Code | Context | Meaning |
|:---:|---|---|
| `0` | All scripts & hooks | Success / normal execution / pass-through. |
| `1` | `lint-skills.py` / `eval-router.py` | Validation failure, broken cross-reference, or benchmark test failure. |
| `2` | `context_guard.py precompact` | Blocked manual `/compact` because no fresh checkpoint file was verified on disk. |
| `2` | `git_pre_commit.py` | Blocked git commit due to absolute path, unmasked secret, duplicate changelog, or manifest mismatch. |
