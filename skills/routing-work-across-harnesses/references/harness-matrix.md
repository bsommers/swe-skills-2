# Harness matrix

**Status: written from memory of each tool's documentation; not verified inside this repo.** Confirm a row against the harness's current docs before depending on it, then record the date here. Last verified: never.

| Harness | Project skills | User skills | Subagents | Model per subagent | Instruction file | Notes |
|---|---|---|---|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Agent/Task tool; `.claude/agents/*.md` | `model` arg or agent frontmatter (`haiku`/`sonnet`/`opus`) | `CLAUDE.md` | Native `/code-review <level>`; plugin via `.claude-plugin/` |
| Antigravity (`agy`) | `.agents/skills/` | `~/.agents/skills/` or `agy plugin install` | agent profiles in `templates/agy/agents` | frontmatter `model` (`flash`/`pro`) | `GEMINI.md`, `AGENTS.md` | `agy plugin validate .` |
| opencode | `.opencode/skills/` (also reads `.claude/skills`, `.agents/skills`) | `~/.config/opencode/skills/` | `.opencode/agents/*.md`, mode `subagent` | `model: provider/model` in agent file or `opencode.json` | `AGENTS.md` | Custom commands in `.opencode/command/` |
| pi | `.pi/skills/`, `.agents/skills/` | `~/.pi/agent/skills/` | none built in; run lenses sequentially, or launch `pi -p` per lens from a script | `--model` per process | `AGENTS.md` | Minimal harness; keep prompts self-contained |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | `.cursor/agents/*.md` | frontmatter `model` (`fast`, `inherit`, or an ID) | `.cursor/rules/*.mdc`, `AGENTS.md` | Slash commands in `.cursor/commands/` |

## Tier to model suggestions

Aliases are starting points; set real IDs in harness config. Review them when models change.

| Tier | Claude Code | agy | opencode / pi | Cursor |
|---|---|---|---|---|
| fast | `haiku` | `flash` | cheapest configured model | `fast` |
| standard | `sonnet` | `flash` or `pro` | mid-tier configured model | `inherit` |
| frontier | `opus` (or the strongest available) | `pro` | strongest configured model | strongest selectable |

## Commands

The portable entry is `/eng health` where skills load. Where only prompts are supported, copy `templates/commands/repo-health.md` into the harness's command directory or paste `skills/reviewing-repo-health/references/prompt.md`.
