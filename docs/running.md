# Running, Installation & Configuration

## 1. Prerequisites

- **Operating System:** Linux, macOS, or Windows (WSL2 recommended)
- **Runtime:** Python 3.10+ (standard library only for core hooks; no external pip packages required)
- **Optional Tooling:**
  - [`uv`](https://github.com/astral-sh/uv) (recommended for ultra-fast hook execution)
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

By default, runtimes load the frontmatter descriptions of all installed skills into the initial system prompt, consuming ~2,600 input tokens on every turn. Use `--profile` to install only the skills needed for your workflow:

```bash
# Install core profile (8 skills; drops prompt token overhead by ~85%)
scripts/install.sh --claude --profile core

# Switch to review profile for auditing and testing
scripts/install.sh --claude --profile review
```

| Profile | Skill Count | Estimated Catalog Overhead | Intended Use Case | Included Skills |
|---|:---:|:---:|---|---|
| **`core`** | 8 | ~350 tokens | General development, daily coding | `using-swe-skills`, `planning-with-contracts`, `compacting-context-safely`, `layered-verification-gates`, `committing-and-releasing-cleanly`, `orchestrating-subagents`, `token-finops`, `adaptive-model-routing` |
| **`build`** | 14 | ~650 tokens | Greenfields, scaffolding, CLI tools | `core` + `building-small-cli-tools`, `building-code-generators`, `building-installers-and-onboarding`, `designing-testable-seams`, `engineering-for-determinism`, `scaffolding-new-projects`, `debugging-across-layers` |
| **`review`** | 15 | ~700 tokens | PR audits, security review, QA | `core` + `pr-review`, `code-architecture-review`, `dependency-audit`, `api-contract-audit`, `test-coverage`, `running-multi-lens-audits`, `hunting-silent-failures` |
| **`ship`** | 13 | ~600 tokens | Release cutting, changelogs, docs | `core` + `release`, `writing-pull-requests`, `keeping-docs-in-sync`, `writing-user-guides`, `github-issues-script` |
| **`all`** | 54 | ~2,700 tokens | Full comprehensive library | All 54 skills in `skills/` |

---

## 3. Installing Lifecycle Hooks

To enable automatic context monitoring, `/compact` protection, and adaptive subagent model routing:

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
| `python3 scripts/lint-skills.py --words` | Validates frontmatter, word count limits, cross-references, and naming across all 54 skills. |
| `python3 -m unittest discover tests` | Executes test suite for context guards, model routers, and git hooks. |
| `agy plugin validate .` | Validates plugin manifest (`plugin.json`), hooks schema (`hooks.json`), and skill discovery. |
| `python3 scripts/eval-router.py --self-test` | Evaluates router accuracy against the 10 benchmark scenarios in `docs/TESTING.md`. |
| `python3 scripts/hooks/context_guard.py report` | Outputs context window utilization, active turn stats, and discovered checkpoints. |

---

## 5. Environment Variables

All configuration settings are optional and controlled via environment variables:

| Variable | Default | Purpose |
|---|:---:|---|
| `SWE_SKILLS_CONTEXT_LIMIT` | `200000` | Context window ceiling in tokens. |
| `SWE_SKILLS_CONTEXT_PCT` | `70` | Threshold percentage to trigger first compaction nudge. |
| `SWE_SKILLS_CONTEXT_PCT_STEP` | `10` | Incremental percentage to re-nudge. |
| `SWE_SKILLS_IDLE_MINUTES` | `30` | Idle minutes before cold prompt cache resume nudge. |
| `SWE_SKILLS_AGY_STEP_LIMIT` | `50` | Step count threshold in Antigravity before nudge. |
| `SWE_SKILLS_AGY_BYTES_LIMIT` | `500000` | Transcript byte ceiling in Antigravity before nudge. |
| `SWE_SKILLS_MODEL_ROUTER_ENABLED` | `1` | Set to `0` to disable automatic subagent model routing. |
| `SWE_SKILLS_MODEL_ROUTER_DEFAULT_TIER` | `flash` | Fallback model tier for routine subagents (`flash` / `flash_lite`). |
| `SWE_SKILLS_CONTEXT_GUARD_BLOCK` | `1` | Set to `0` to allow manual `/compact` without a fresh checkpoint. |
| `SWE_SKILLS_CHECKPOINT_FRESH_MINUTES` | `20` | Max age in minutes for a checkpoint to be accepted by `/compact`. |

---

## 6. Exit Codes

| Code | Context | Meaning |
|:---:|---|---|
| `0` | All scripts & hooks | Success / normal execution / pass-through. |
| `1` | `lint-skills.py` / `eval-router.py` | Validation failure, broken cross-reference, or benchmark test failure. |
| `2` | `context_guard.py precompact` | Blocked manual `/compact` because no fresh checkpoint file was verified on disk. |
| `2` | `git_pre_commit.py` | Blocked git commit due to absolute path, unmasked secret, or manifest mismatch. |
