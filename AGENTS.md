# AGENTS.md — swe-skills

Guidance for agents editing **this repository** (not for copying into other projects; see `templates/AGENTS.snippet.md` for that).

## What this is

A library of engineering skills (`skills/<name>/SKILL.md`) for Claude Code, Antigravity (`agy`), and Cursor. `skills/` is the single source of truth; manifests and templates only point at it.

## Commands

```bash
python3 scripts/lint-skills.py --words   # validate all skills; must print OK
agy plugin validate .                    # validate the Antigravity plugin (read-only)
scripts/install.sh --dry-run --all       # preview installation
```

## Layout

- `skills/<name>/SKILL.md` — one skill per directory; directory name equals frontmatter `name`.
- `plugin.json`, `.claude-plugin/`, `.cursor-plugin/` — per-tool manifests. Keep versions equal.
- `docs/EVIDENCE.md` — provenance; update when a skill's source material changes.
- `docs/TESTING.md` — pressure scenarios; update when adding a skill.

## Authoring rules

1. Frontmatter has only `name` and `description`. Description starts with `Use when`, third person, ≤ 1024 chars (prefer ≤ 500), states **triggers only**, never the process.
2. Body target ≤ 500 words; heavy reference goes in a `references/` file inside the skill.
3. Guidance form follows the failure it addresses: discipline gaps get rules plus a mistakes list; wrong-shaped output gets a positive recipe or template.
4. Cross-reference other skills as `` `skill-name` `` (lint checks they exist). No `@file` force-loading.
5. No absolute machine paths, no project-private names or secrets in skill text. Concrete incidents are generalized.
6. Adding a skill also means: add it to `using-swe-skills`, README table, `docs/EVIDENCE.md`, and `docs/TESTING.md`.

## Before committing

Lint passes, `agy plugin validate .` passes, manifests' versions match, and changes to a skill are reflected in `docs/TESTING.md` if the behavior it guards changed.
