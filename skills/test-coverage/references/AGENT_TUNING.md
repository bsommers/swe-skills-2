# Agent Detection & Tuning for Test Coverage

Identify the active runtime environment to use the optimal tools and output mechanisms:

| Agent / Environment | Primary Capabilities & Output Mechanism |
| :--- | :--- |
| **Claude Code** | Use `Read`, `Grep`, `Glob`, `Bash`. Invoke via `/test-coverage`, parse `$ARGUMENTS` for a scoped path. Run coverage tools inline; stream progress concisely. |
| **Antigravity (`agy`)** | Use native file/search tools. Run coverage commands via `run_command`. Render the coverage summary as an interactive artifact with `write_to_file`. |
| **Cursor (Composer / Agent)** | Run terminal commands for the detected tool, reference `@<coverage-report-path>` in Composer for follow-up work. |
| **Universal / CLI Agents** | Use POSIX tools; fall back to `references/COVERAGE_TOOLS_MATRIX.md` and the reachability script when no coverage tool is installed and network/package installation isn't available or approved. |
