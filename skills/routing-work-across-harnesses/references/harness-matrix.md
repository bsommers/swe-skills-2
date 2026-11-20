# Harness matrix

**Status: checked against official docs on 2026-11-15** (sources at the bottom). Cells marked *unverified* could not be confirmed. Re-check when a harness ships a major release. `install.sh --agy` uses `agy plugin install`, else falls back to the CLI skills dir. Last verified: 2026-11-15.

| Harness | Project skills | User skills | Subagents | Model per subagent | Instruction file | Notes |
|---|---|---|---|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Agent/Task tool; `.claude/agents/*.md` | `model` arg or agent frontmatter (`haiku`/`sonnet`/`opus`/`fable`), full IDs, or `inherit`; `CLAUDE_CODE_SUBAGENT_MODEL` overrides | `CLAUDE.md` | Native `/code-review <level>`; plugin via `.claude-plugin/` |
| Antigravity (`agy`) | `.agents/skills/` | `~/.gemini/config/skills/` (app), `~/.gemini/antigravity-cli/skills/` (CLI; the CLI does not read `~/.agents/skills/`), or `agy plugin install` | `.agents/agents/<name>.md`; global `~/.gemini/config/agents/`; plugin `agents/` (repo templates: `templates/agy/agents`) | frontmatter `model`: `inherit` (default), `flash`, `pro` | `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md` | `agy plugin validate .` |
| opencode | `.opencode/skills/` (also reads `.claude/skills`, `.agents/skills`) | `~/.config/opencode/skills/` | `.opencode/agents/*.md`, mode `subagent` | `model: provider/model` in agent file or `opencode.json` | `AGENTS.md` | Custom commands in `.opencode/commands/` (singular `command/` is legacy). Model may carry a `#variant` suffix |
| pi | `.pi/skills/`, `.agents/skills/` | `~/.pi/agent/skills/` | none built in; run lenses sequentially, or launch `pi -p` per lens from a script | `--model` per process (`provider/id`, optional `:thinking`) | `AGENTS.md`, `CLAUDE.md` | Minimal harness; keep prompts self-contained. `.pi/skills` and `~/.pi/agent/skills` *unverified* (only `.agents/skills` and `~/.agents/skills` confirmed); prompts in `~/.pi/agent/prompts/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | `.cursor/agents/*.md` | frontmatter `model`: `inherit` (default) or a model ID; a `fast` alias is *not documented* | `.cursor/rules/*.mdc`, `AGENTS.md` | Slash commands in `.cursor/commands/` |

## Tier to model suggestions

Aliases are starting points; set real IDs in harness config. Review them when models change.

| Tier | Claude Code | agy | opencode / pi | Cursor |
|---|---|---|---|---|
| fast | `haiku` | `flash` | cheapest configured model | cheapest model ID you have |
| standard | `sonnet` | `flash` or `pro` | mid-tier configured model | `inherit` |
| frontier | `opus` (or the strongest available) | `pro` | strongest configured model | strongest selectable |

## Commands

The portable entry is `/eng health` where skills load. Where only prompts are supported, copy `templates/commands/repo-health.md` into the harness's command directory or paste `skills/reviewing-repo-health/references/prompt.md`.

## Sources (2026-11-15)

code.claude.com/docs/en/skills, /sub-agents; antigravity.google/docs/subagents.md, /plugins.md, /rules; codelabs.developers.google.com/getting-started-with-antigravity-skills; opencode.ai/docs/skills, /agents, /commands; github.com/badlogic/pi-mono (packages/coding-agent/docs); cursor.com/docs/context/skills, /subagents, /rules.
