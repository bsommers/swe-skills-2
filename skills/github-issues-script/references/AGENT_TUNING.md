# Agent Detection & Workflow for GitHub Issues Script

Identify the active runtime environment to use the optimal workflow:

| Agent / Environment | Recommended Workflow |
| :--- | :--- |
| **Antigravity (`agy`)** | Parse findings from memory or workspace artifacts (`docs/ARCHITECTURE_REVIEW.md`, `docs/IMPROVEMENT_PLAN.md`), write the output script with `write_to_file`, and display an interactive preview artifact. |
| **Claude Code** | Parse `$ARGUMENTS` (e.g. `/github-issues-script docs/IMPROVEMENT_PLAN.md` or from chat context), generate the script in `scripts/create_issues.sh`, and offer to execute a dry-run. |
| **Cursor** | Generate the script in the repository, allowing users to inspect it in the editor and run from Cursor's integrated terminal. |
| **Universal AI Agents** | Standardized POSIX shell generation utilizing robust heredocs to prevent escaping issues. |
