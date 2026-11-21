# Antigravity (`agy`) Subagent Templates

Optional subagent profiles for `agy` (Antigravity CLI).

> [!IMPORTANT]
> `agy` agent frontmatter `model:` and `invoke_subagent` `Model` only accept abstract tiers (`inherit`, `flash_lite`, `flash`, `pro`). Concrete `agy models` IDs (e.g. `gemini-4-carbon-high`) are rejected by the agent loader and are only valid for `--model` / `/model` on the main session.

## Profiles

| File | `model` Tier | Policy / Tools | Role |
|---|---|---|---|
| `architect.md` | `pro` | `commandExecutionPolicy: off`, read-only (`read_file`, `search_web`, `send_message`) | Architecture, specs, audits; returns a locked plan for an executor |
| `ops-executor.md` | `flash` | `commandExecutionPolicy: auto`, read/write/run + `search_web` | Executes multi-step implementation, CI, and ops tasks with verification gates |
| `bulk-worker.md` | `flash_lite` | `commandExecutionPolicy: sandbox`, read/write/run | High-throughput localized edits, boilerplate, and test runs |

## Install & Invoke

Copy into a plugin's `agents/` directory, workspace `.agents/agents/`, or global `~/.gemini/config/agents/`:

```bash
mkdir -p .agents/agents
cp templates/agy/agents/*.md .agents/agents/
```

- **As a subagent (`subagent: true`):** The coordinator invokes it via `invoke_subagent` with `TypeName: "architect"` (or `"ops-executor"`, `"bulk-worker"`).
- **As a main session agent:** Set `mainAgent: true` in frontmatter, then run `agy --agent architect` (or `/agents` in TUI). Set the main session model with `agy --model gemini-4-hydrogen-medium` (or `/model`).
