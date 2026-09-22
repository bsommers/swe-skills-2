# Agent Detection & Tuning Guide for Code Architecture Review

## Agent Detection & Mode Tuning

Identify the active runtime environment to use the optimal tools and output mechanisms:

| Agent / Environment | Primary Capabilities & Output Mechanism |
| :--- | :--- |
| **Antigravity (`agy`)** | Use native file & search tools (`view_file`, `grep_search`, `find_by_name`). Create interactive user artifacts with `write_to_file` (with `ArtifactMetadata`). Support subagent delegation (`research`, `self`) for large repos. Render Mermaid diagrams natively. |
| **Claude Code** | Use `Read`, `Grep`, `Glob`, and inline `Bash`. Utilize `$ARGUMENTS` parsing if invoked via slash command `/code-architecture-review`. Stream output concisely. |
| **Cursor (Composer / Agent)** | Reference codebase indexing (`@codebase`, `@workspace`), execute terminal commands via terminal tool, generate clean markdown plans suitable for Composer multi-file editing. |
| **Universal / CLI Agents** | Use standard POSIX file inspection, ripgrep (`rg`), AST extractors, and markdown files stored in the repository root or `.planning/` directory. |

---

## Agent-Specific Tuning & Integration

### For Claude Code
- Parse `$ARGUMENTS` to support scoped reviews:
  - `/code-architecture-review` (Full repo scan)
  - `/code-architecture-review src/components` (Subsystem scoped review)
- Leverage sub-commands or parallel reads for fast AST traversal.
- Commit the review report cleanly if requested by the user.

### For Antigravity (`agy`)
- Utilize `write_to_file` with `ArtifactMetadata` for interactive review inspection.
- Embed interactive Mermaid graphs directly in output artifacts.
- Suggest built-in slash commands in chat:
  - *"You can use `/plan` to convert this improvement plan into a structured milestone roadmap."*
  - *"You can run `/security-scan` to perform an in-depth OWASP & CVE audit."*
- If the repository is very large, invoke a `research` subagent to concurrently survey subsystem directories.

### For Cursor
- Guide the user to reference `@docs/ARCHITECTURE_REVIEW.md` in Composer when initiating refactoring.
- Provide targeted file edit instructions matching Cursor's multi-file inline diff engine.
- Generate `.cursor/rules/architecture-rules.mdc` if the user wants to enforce the newly defined architectural boundaries continuously during development.
