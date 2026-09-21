# swe-skills

Software engineering, planning, and architecture skills for AI-assisted coding sessions — from a one-file tool to a multi-service system. Works with **Claude Code**, **Antigravity (`agy`)**, and **Cursor** (and anything reading `~/.agents/skills`).

Every skill is distilled from real projects: bugs that were found, limits that were measured, audits that were run, and rules that held up across ~20 repositories (compilers, pipelines, benchmarks, agent frameworks, browser extensions, UI libraries). Provenance is in [docs/EVIDENCE.md](docs/EVIDENCE.md).

## How it's meant to be used

Start with **`using-swe-skills`**. It sizes the task (tool / app / system) and routes to the one to three skills that apply. Loading everything at once wastes context, so each skill is short (≈300–500 words) and has a discovery-only description.

Or type **`/eng`**, a shortcut into the same router:

```text
/eng add retry logic across the four API modules   # free text -> using-swe-skills picks the skills
/eng hunting-silent-failures src/parser            # a skill name -> loads that skill
/eng release                                       # a shortcut word -> committing-and-releasing-cleanly (still asks before push)
/eng help                                          # the router's skill table
```

The shortcut words live in one table, in [`skills/eng/SKILL.md`](skills/eng/SKILL.md), and the linter checks it. Only the first word is matched, exactly; anything else is free text.

The name is deliberately not `swe`: the older `swe-skills` suite already has a `swe` router, and `eng` lets the two install side by side instead of one replacing the other.

## Skills (39)

| Group | Skills |
|---|---|
| **Entry** | `using-swe-skills` · `eng` |
| **Frame & plan** | `right-sizing-process` · `writing-intent-briefs` · `planning-with-contracts` · `sizing-limits-from-measurement` · `choosing-tools-and-substrates` |
| **Architecture** | `designing-layered-pipelines` · `designing-plugin-contracts` · `designing-testable-seams` · `evolving-schemas-and-contracts` · `defending-architecture-decisions` · `managing-complexity-budgets` · `designing-data-pipelines` |
| **AI systems** | `building-unattended-agent-loops` · `grounding-ai-outputs` |
| **Build** | `scaffolding-new-projects` · `building-small-cli-tools` · `building-code-generators` · `parsing-untrusted-text-robustly` · `hardening-trust-boundaries` · `engineering-for-determinism` |
| **Verify & measure** | `layered-verification-gates` · `hunting-silent-failures` · `debugging-across-layers` · `clustering-failures-by-root-cause` · `building-trustworthy-benchmarks` · `making-verifiable-claims` |
| **Collaborate & sustain** | `orchestrating-subagents` · `running-multi-lens-audits` · `supervising-autonomous-sessions` · `handing-off-sessions` · `compacting-context-safely` · `writing-agent-context-files` · `keeping-docs-in-sync` · `keeping-repos-portable` · `drafting-issue-reports` · `writing-pull-requests` · `committing-and-releasing-cleanly` |

These complement general process skills (brainstorming, TDD, systematic debugging, code review) rather than replace them.

## Install

```bash
git clone <this repo> ~/src/swe-skills-2 && cd ~/src/swe-skills-2
scripts/install.sh --dry-run          # preview
scripts/install.sh --all              # symlinks into all user-level locations
```

| Tool | What gets installed | Manual equivalent |
|---|---|---|
| **Claude Code** | `~/.claude/skills/<skill>` symlinks | or `/plugin marketplace add ~/src/swe-skills-2` then `/plugin install swe-skills@swe-skills-marketplace` |
| **Antigravity (`agy`)** | `agy plugin install <repo>` (falls back to `~/.agents/skills`) | `agy plugin validate .` then `agy plugin install .` |
| **Cursor** | `~/.cursor/skills/<skill>` (Cursor Agent Skills) | project-level: `scripts/install.sh --project <dir>` also adds `.cursor/rules/swe-skills.mdc` |
| **Others** (Codex, Copilot CLI, Gemini CLI) | `~/.agents/skills/<skill>` | `scripts/install.sh --agents` |

Per project: `scripts/install.sh --project /path/to/repo` installs into `.claude/skills`, `.agents/skills`, `.cursor/skills` and adds the thin Cursor rule. Use `--copy` for standalone copies, `--uninstall` to remove, `--force` to replace same-named entries.

Add [`templates/AGENTS.snippet.md`](templates/AGENTS.snippet.md) to a project's `AGENTS.md` so every agent knows the library exists.

### Optional: context-guard hooks

A skill only helps if it loads in time, and an agent judges its own context use poorly. Opt-in hooks
nudge it to checkpoint around 70% full, block a `/compact` that has no fresh checkpoint, and feed the
checkpoint back after `/compact` or `/clear`:

```bash
scripts/hooks/install-hooks.py --claude --dry-run   # preview; --agy for Antigravity
```

Nothing fires until installed. See [docs/HOOKS.md](docs/HOOKS.md) for events, settings and limits.

## Repository layout

```
skills/<name>/SKILL.md        the skills (single source of truth)
plugin.json                   Antigravity plugin manifest
.claude-plugin/               Claude Code plugin + marketplace manifests
.cursor-plugin/               Cursor plugin manifest
templates/                    Cursor always-on rule; AGENTS.md snippet
scripts/lint-skills.py        validates frontmatter, naming, cross-references, portability
scripts/install.sh            installer for all targets
scripts/hooks/                opt-in context-guard hooks + their installer
tests/                        tests for the hook scripts
docs/EVIDENCE.md              which repos/incidents each skill came from
docs/TESTING.md               pressure scenarios for validating each skill
docs/HOOKS.md                 how to turn the context-guard hooks on
```

## Develop

```bash
python3 scripts/lint-skills.py --words   # must print OK
python3 -m unittest discover tests       # hook, router-eval and /eng shortcut tests
```

Authoring rules: description starts with "Use when…" and states triggers only (never the workflow); third person; ≤ 1024 chars; body targets ≤ 500 words; one skill per directory, name equals directory; the router must list every skill; `/eng` shortcuts must name existing skills. See [AGENTS.md](AGENTS.md).

## Status

v0.1.0. Skills are evidence-derived but **not yet pressure-tested with fresh agents**; [docs/TESTING.md](docs/TESTING.md) lists the scenarios to run.

## License

MIT
