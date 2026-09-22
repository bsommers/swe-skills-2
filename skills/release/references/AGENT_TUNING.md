# Agent Detection & Capabilities for Release Skill

Identify the active runtime environment to use the optimal capabilities and workflows:

| Agent / Environment | Capabilities & Best Practices |
| :--- | :--- |
| **Antigravity (`agy`)** | Run commands via `run_command`, view files via `view_file`, display interactive artifacts for release notes review with `write_to_file`. |
| **Claude Code** | Parse `$ARGUMENTS` (e.g. `/release`, `/release patch`, `/release minor`, `/release major`, `/release --dry-run`), run git commands inline in Bash. |
| **Cursor (Composer / Agent)** | Run terminal commands, update `CHANGELOG.md` in-editor, prompt user before pushing to remote. |
| **Universal AI Agents** | Execute portable shell commands and follow strict SemVer 2.0.0 guidelines. |
