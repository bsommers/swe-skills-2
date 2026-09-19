# CLAUDE.md

See [AGENTS.md](AGENTS.md) for repository guidance (layout, commands, authoring rules).

Claude Code specifics:
- Skills load from `skills/<name>/SKILL.md`; this repo is also a Claude Code plugin (`.claude-plugin/plugin.json`) and a one-plugin marketplace (`.claude-plugin/marketplace.json`).
- After editing a skill, run `python3 scripts/lint-skills.py --words` before committing.
