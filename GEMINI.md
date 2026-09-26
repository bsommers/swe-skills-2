# GEMINI.md

See [AGENTS.md](AGENTS.md) for repository guidance (layout, commands, authoring rules).

Antigravity specifics:
- Skills are discovered from `skills/<name>/SKILL.md` via the root `plugin.json`. Validate with `agy plugin validate .`.
- Antigravity has no todo tool; track multi-step work in a task artifact.
- Context management: Antigravity has no `/compact` command. When a session exceeds ~50 steps or finishes a major phase, follow `compacting-context-safely`, write or refresh `docs/CHECKPOINT.md`, and advise the user to start a fresh session (`/exit` or New Chat) to resume from the checkpoint.
