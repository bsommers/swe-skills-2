# Chapter 1: Getting Started

[← Back to User Manual](README.md) · [Next: Skills Catalog →](02-skills-catalog.md)

This chapter guides you through installing, configuring, and verifying **`swe-skills`** across supported AI coding agent environments.

---

## Prerequisites & System Requirements

- **Operating System:** Linux, macOS, or Windows (via WSL2).
- **Runtimes:**
  - Python 3.10+ (standard library only; no third-party package dependencies required for core tools).
  - Git 2.25+.
  - Bash 4.0+.
- **Host Agent Frameworks (one or more):**
  - **Claude Code:** Supports user skills (`~/.claude/skills/`), project skills, and lifecycle hooks (`UserPromptSubmit`, `PreCompact`, `SessionStart`).
  - **Antigravity (`agy`):** Supports plugin registration, skill discovery, and lifecycle hooks (`PreInvocation`, `SessionStart`).
  - **Cursor:** Supports global and project-level agent skills (`~/.cursor/skills/`) and rules (`.cursor/rules/`).
  - **Cross-Runtime Agents:** Codex, Copilot CLI, Gemini CLI reading `~/.agents/skills/`.

---

## Global Installation Across Runtimes

The repository includes a unified shell installer [`scripts/install.sh`](../../scripts/install.sh) that installs skills into all supported global directories in a single command.

### 1. Clone the Repository

```bash
git clone https://github.com/bsommers/swe-skills-2.git ~/src/swe-skills-2
cd ~/src/swe-skills-2
```

### 2. Preview Installation (Dry Run)

```bash
scripts/install.sh --dry-run --all
```

### 3. Execute Installation

```bash
scripts/install.sh --all --force
```

By default, the installer creates symlinks so that updates pulled from git immediately take effect in all agent environments without reinstallation.

---

## Claude Code Setup

Claude Code discovers skills placed in `~/.claude/skills/<skill-name>/SKILL.md`.

### Method A: Via `install.sh` (Recommended)

```bash
scripts/install.sh --claude
```

### Method B: Via Claude Plugin Marketplace

You can register the local marketplace directly inside Claude Code:

```text
/plugin marketplace add ~/src/swe-skills-2
/plugin install swe-skills@swe-skills-marketplace
```

### Installing Context-Guard Hooks

Claude Code hooks monitor context token usage and guard manual `/compact` operations:

```bash
python3 scripts/hooks/install-hooks.py --claude
```

This merges `UserPromptSubmit`, `PreCompact`, and `SessionStart` hooks into your `~/.claude/settings.json`, creating an automated `.bak` backup first.

---

## Antigravity (`agy`) Setup

Antigravity loads plugins via its CLI.

### 1. Validate Plugin Manifest

```bash
agy plugin validate .
```

Expected output:
```text
  [ok]    .
          ✔ skills      : 50 processed
          ✔ hooks       : 1 processed
```

### 2. Install Plugin

```bash
agy plugin install .
```

### 3. Context-Guard Hooks for Antigravity

Antigravity supports `PreInvocation` and `SessionStart` hooks defined in a root `hooks.json`:

```bash
python3 scripts/hooks/install-hooks.py --agy
agy plugin uninstall swe-skills && agy plugin install .
```

Check active registration:

```bash
agy plugin list
```

Verify that `"components": ["skills", "hooks"]` appears under `swe-skills`.

---

## Cursor Setup

Cursor discovers skills placed in `~/.cursor/skills/<skill-name>/SKILL.md`.

```bash
scripts/install.sh --cursor
```

To enable Cursor's agent to prioritize the swe-skills router across any project, configure project rules as shown below.

---

## Project-Level Setup

To install skills directly into a specific target project repository without relying on user-level directories:

```bash
scripts/install.sh --project /path/to/my-project
```

This populates:
- `/path/to/my-project/.claude/skills/`
- `/path/to/my-project/.cursor/skills/`
- `/path/to/my-project/.cursor/rules/swe-skills.mdc`
- `/path/to/my-project/.agents/skills/`

### Adding Context to `AGENTS.md`

Add the snippet in [`templates/AGENTS.snippet.md`](../../templates/AGENTS.snippet.md) into the target project's `AGENTS.md`:

```markdown
<!-- swe-skills-start -->
## Engineering Skills Library

Engineering skills from `swe-skills` are available in this project.
Start non-trivial tasks with `/eng <task description>` or reference skills directly:
- Frame & plan: `planning-with-contracts`, `sizing-limits-from-measurement`
- Architecture: `designing-testable-seams`, `designing-layered-pipelines`
- Verification: `hunting-silent-failures`, `layered-verification-gates`
- Release & Git: `committing-and-releasing-cleanly`, `release`
<!-- swe-skills-end -->
```

---

## Two-Minute First Verification

Once installed, verify that your host agent recognizes the skills:

1. **Start your agent:**
   ```bash
   claude
   # or
   agy
   ```

2. **Run the `/eng` router command:**
   ```text
   /eng help
   ```
   The agent should output the core skills table categorizing Frame, Architecture, AI, Build, Verify, and Ops.

3. **Test natural-language routing:**
   ```text
   /eng I need to design a 3-stage data processing pipeline for JSON events
   ```
   The agent will invoke `using-swe-skills` and load `designing-layered-pipelines` and `evolving-schemas-and-contracts`.
