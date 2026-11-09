# Development Guidelines

How to work on **this repository** (the skill library itself). For using the skills in your own projects see [running.md](running.md); for authoring a single skill step by step see [User Manual Chapter 5](usermanual/05-authoring-skills.md). The terse agent-facing version of these rules is [AGENTS.md](../AGENTS.md).

[← Back to Documentation Hub](README.md)

## Table of Contents
- [Repository model](#repository-model)
- [Prerequisites](#prerequisites)
- [Workflow](#workflow)
- [Skill authoring rules](#skill-authoring-rules)
- [Adding a skill: checklist](#adding-a-skill-checklist)
- [Verification gates](#verification-gates)
- [Documentation sync](#documentation-sync)
- [Scripts and tests](#scripts-and-tests)
- [Graphics rendering (cross-platform)](#graphics-rendering-cross-platform)
- [Versioning and releases](#versioning-and-releases)
- [Commits and pull requests](#commits-and-pull-requests)
- [Portability and security](#portability-and-security)

## Repository model

- `skills/<name>/SKILL.md` is the **single source of truth**. Manifests (`plugin.json`, `.claude-plugin/`, `.cursor-plugin/`) and templates only point at it.
- Heavy reference material lives in `skills/<name>/references/`, not in the skill body.
- `scripts/` holds the installer, linter, graphics/pages generators, tool registry, and opt-in hooks (`scripts/hooks/`). They use the Python standard library only.
- `docs/` holds living documentation; `docs/CHECKPOINT.md` and `CHANGELOG.md` are history/state records, not specs.

See [architecture.md](architecture.md) for how the pieces fit together.

## Prerequisites

- Python 3 (standard library only; no `pip install` step).
- Git, and optionally `gh` for issues and PRs.
- Optional: `agy` (Antigravity) to run `agy plugin validate .`.

## Workflow

1. Branch from `main`; do not commit directly to it.
2. Make the change (skill, script, or doc).
3. Run the [verification gates](#verification-gates).
4. Update docs in the same change ([sync checklist](#documentation-sync)).
5. Open a PR; one logical change per PR.

## Skill authoring rules

1. Frontmatter has only `name` and `description`; `name` equals the directory name.
2. `description` starts with `Use when`, is third person, at most 1024 characters (prefer 500), and states **triggers only**, never the process. An agent that reads the process in the description skips the body.
3. Body targets 500 words or fewer. Move long reference into `references/`.
4. Match the form to the failure: discipline gaps get rules plus a mistakes list; wrong-shaped output gets a positive recipe or template.
5. Cross-reference other skills as `` `skill-name` ``; the linter checks they exist. Do not use `@file` force-loading.
6. No absolute machine paths, project-private names, or secrets. Generalize incidents.

## Adding a skill: checklist

1. Create `skills/<name>/SKILL.md` (and `references/` if needed).
2. Add it to the routing table in `skills/using-swe-skills/SKILL.md`; add an `/eng` shortcut in `skills/eng/SKILL.md` only if warranted.
3. Add it to the README skills table and bump the count.
4. Add provenance to [EVIDENCE.md](EVIDENCE.md) and a pressure scenario to [TESTING.md](TESTING.md).
5. Update every doc that quotes the skill count (see below).
6. Run the gates.

## Verification gates

Run before every commit. "Done" means these pass, not that they were skipped.

```bash
python3 scripts/lint-skills.py --words   # must print OK (0 errors)
python3 -m unittest discover tests       # hooks, router, shortcuts, graphics/pages
agy plugin validate .                    # if agy is installed
scripts/install.sh --dry-run --all       # preview install; touches nothing
```

Never weaken a check to get green. If a test is unavailable, say so rather than reporting success.

## Documentation sync

Docs, diagrams and the Pages showcase drift silently. Update them in the same change:

| You changed | Update |
|---|---|
| Skill added/removed | `using-swe-skills`, `eng`, `README.md`, `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, `docs/usermanual/`, `docs/index.html`, `scripts/render-graphics.py` |
| CLI flag or script behavior | `docs/running.md`, `docs/usermanual/06-reference-and-cli.md`, `README.md`, `CHANGELOG.md` |
| Hook behavior | `docs/HOOKS.md`, `docs/usermanual/03-hooks-and-context-guards.md` |
| Architecture or subsystem | `docs/architecture.md`, diagrams in `docs/diagrams/` and `docs/assets/examples/` |
| Counts or versions | every file quoting them; grep before committing |

Regenerate derived artifacts rather than hand-editing:

```bash
python3 scripts/render-graphics.py   # SVG + PNG assets
python3 scripts/build-pages.py       # docs/index.html
```

Use relative links only. Mark old build logs and plans as historical.

## Scripts and tests

| Path | Purpose |
|---|---|
| `scripts/lint-skills.py` | Frontmatter, naming, cross-references, word limits, portability |
| `scripts/install.sh` | Installer for all targets, with profiles |
| `scripts/hooks/` | `context_guard.py`, `model_router.py`, `git_pre_commit.py`, `install-hooks.py` |
| `scripts/tool-registry.py` | Local tool/VM registry |
| `scripts/render-graphics.py`, `build-pages.py` | Deterministic graphics and Pages generation |
| `scripts/eval-router.py`, `run-scenarios.py` | Router evaluation and scenario runs |
| `tests/` | `unittest` suites for hooks, router, shortcuts, graphics/pages, scenarios |

Generators must be deterministic: identical input yields byte-identical output, so diffs stay quiet.

## Graphics rendering (cross-platform)

`scripts/render-graphics.py` writes SVGs, then converts them to PNG with the first converter it finds on `PATH`: `inkscape`, `rsvg-convert`, or `magick`. It aborts with "No SVG-to-PNG converter found" if none is installed.

> **TODO: uniform rendering on Linux, macOS and Windows.** Different converters (and different font stacks) produce byte-different PNGs from the same SVG. Regenerating on one machine rewrites every committed PNG even when no SVG changed, which makes diffs noisy and the PNGs depend on whoever ran the script last. Before relying on PNGs as canonical, pick one pinned converter and font setup that works on all three platforms and document or enforce it (for example a fixed `rsvg-convert` version with bundled fonts, or a container image), and make the script choose it deterministically instead of taking the first match. Until then:

- The SVGs are the source of truth; treat PNGs as derived.
- After regenerating, commit only the PNGs whose SVG actually changed (`git status` shows which) and revert the rest with `git checkout -- <paths>`.
- Record which converter and version produced the committed PNGs in the commit message. The current ones were produced with `rsvg-convert` 2.63.4 (macOS, Homebrew `librsvg`).
- Install a converter with `brew install librsvg` (macOS), `apt install librsvg2-bin` (Debian/Ubuntu), or `choco install inkscape` (Windows).

## Versioning and releases

- Semantic Versioning. Keep the version equal across `plugin.json`, `.claude-plugin/`, and `.cursor-plugin/`.
- Record every user-visible change in `CHANGELOG.md` (Added / Changed / Fixed) with the verification you ran.
- Tag releases only after the gates pass. See the `release` and `committing-and-releasing-cleanly` skills.

## Commits and pull requests

- Conventional-style subjects (`feat(skills): ...`, `fix(...)`, `docs: ...`, `chore(release): ...`) match existing history.
- Do not mix unrelated changes in one commit.
- Confirm before pushing, tagging or any other outward-facing action.
- PR descriptions state what changed, why, and which gates were run.

## Portability and security

- No absolute paths such as home directories; use relative paths and environment variables.
- Never commit secrets. `scripts/hooks/git_pre_commit.py` blocks unmasked secrets, absolute machine paths and duplicate changelogs; install it with `scripts/hooks/install-hooks.py`.
- Treat anything passed to a shell, path, or query as untrusted (`hardening-trust-boundaries`).
