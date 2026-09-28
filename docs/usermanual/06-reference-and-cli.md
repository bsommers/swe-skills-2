# Chapter 6: CLI & Script Reference

[← Back to User Manual](README.md) · [← Previous: Authoring Skills](05-authoring-skills.md) · [Next: Troubleshooting & FAQ →](07-troubleshooting-and-faq.md)

This chapter provides comprehensive reference documentation for all CLI utilities, operational scripts, and exit codes in the repository.

---

## `scripts/install.sh`

Unified installer for deploying skills across user-level and project-level directories.

### Usage
```bash
scripts/install.sh [targets] [options]
```

### Targets
- `--claude`: Installs symlinks into `~/.claude/skills/`.
- `--agy`: Runs `agy plugin install` (falls back to `~/.agents/skills/`).
- `--cursor`: Installs symlinks into `~/.cursor/skills/`.
- `--agents`: Installs symlinks into `~/.agents/skills/` (cross-runtime).
- `--all`: Installs into all of the above (default).
- `--project DIR`: Project-level installation into `DIR/.claude/skills`, `DIR/.cursor/skills`, and `DIR/.cursor/rules/swe-skills.mdc`.

### Options
- `--copy`: Copy skill directories instead of creating symlinks.
- `--force`: Overwrite existing files or symlinks with the same name.
- `--uninstall`: Remove skills installed by this script (matching links or marker files).
- `--dry-run`: Preview all filesystem modifications without writing changes.
- `-h, --help`: Display help and exit.

### Exit Codes
- `0`: Success.
- `1`: Invalid project directory.
- `2`: Invalid argument.

---

## `scripts/lint-skills.py`

Static analysis and validation engine for skill authoring compliance.

### Usage
```bash
python3 scripts/lint-skills.py [options]
```

### Options
- `--words`: Print word counts for every skill and total library word count. Warns on skills exceeding 900 words.
- `-h, --help`: Display help.

### Validation Checks Performed
1. **Frontmatter Schema:** Ensures frontmatter contains only `name` and `description`.
2. **Directory Parity:** Confirms directory name matches `name` in frontmatter.
3. **Trigger-Only Check:** Ensures description begins with `"Use when"` and does not exceed 1024 characters.
4. **Cross-Reference Integrity:** Verifies that all `` `skill-name` `` cross-references target existing skills.
5. **Portability:** Verifies that no absolute user paths (`/home/` or `/Users/`) exist in skill documentation.

---

## `scripts/hooks/install-hooks.py`

Opt-in installer for context-guard and git pre-commit hooks.

### Usage
```bash
python3 scripts/hooks/install-hooks.py [targets] [options]
```

### Targets
- `--claude`: Merges hooks into `~/.claude/settings.json` (or project settings).
- `--agy`: Writes `hooks.json` at plugin root and adds `/hooks.json` to `.gitignore`.
- `--git`: Installs `.git/hooks/pre-commit` wrapper script.
- `--project DIR`: Target project directory instead of user home directory (Claude Code).

### Options
- `--uninstall`: Removes hooks installed by this tool while preserving user hooks.
- `--dry-run`: Output target file changes to stdout without modifying disk.

---

## `scripts/hooks/context_guard.py`

Harness lifecycle hook handler for token monitoring, compaction gating, and session continuity.

### Subcommands
- `nudge`: Evaluates token usage from transcript (`UserPromptSubmit`). Outputs nudge JSON when threshold exceeded.
- `preinvocation`: Evaluates step count and transcript size for Antigravity (`PreInvocation`). Outputs `injectSteps` ephemeral message.
- `precompact`: Checks for fresh checkpoint before manual `/compact` (`PreCompact`). Exits `2` to block if missing.
- `sessionstart`: Injects newest checkpoint into fresh session context (`SessionStart`).
- `report`: Prints current context token utilization and newest checkpoint status to stdout.

---

## `scripts/hooks/git_pre_commit.py`

Pre-commit validation gate preventing secrets, machine paths, and manifest divergence.

### Usage
```bash
python3 scripts/hooks/git_pre_commit.py [FILES...]
# If no arguments provided, checks all git staged files
```

### Checks
1. Rejects absolute paths (`/home/...`, `/Users/...`).
2. Rejects private keys and unmasked API tokens.
3. Verifies identical version numbers across all 4 plugin manifests.
4. Runs `scripts/lint-skills.py` to ensure all skills pass linting.

---

## `scripts/eval-router.py`

Evaluation harness measuring accuracy of skill recommendation algorithms.

### Usage
```bash
python3 scripts/eval-router.py [options]
```

### Options
- `--self-test`: Executes built-in golden benchmark cases against the router logic.
- `--benchmark`: Runs comprehensive scenario matrix and reports top-1 and top-3 accuracy.

---

## `scripts/run-scenarios.py`

Pressure-testing validator ensuring all scenarios documented in `docs/TESTING.md` map to real skills.

### Usage
```bash
python3 scripts/run-scenarios.py [--dry-run]
```
- `--dry-run`: Verifies scenario mappings and prints summary table without launching subagents.

---

## `skills/release/scripts/release.sh`

Automated semantic release automation tool.

### Usage
```bash
skills/release/scripts/release.sh [options]
```

### Options
- `--dry-run`: Analyzes commits, calculates bump, and prints preview without writing files.
- `--force-bump <major|minor|patch>`: Overrides automated commit analysis.
