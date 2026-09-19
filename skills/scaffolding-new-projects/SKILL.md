---
name: scaffolding-new-projects
description: Use when starting a new repository or project directory, when asked to "scaffold", "bootstrap", or "set up" a repo layout (src/, docs/, tests/, input/, output/, README), or when a new project is about to receive its first code with no structure yet.
---

# Scaffolding New Projects

## Overview

A scaffold is the first contract a repo makes: where inputs come from, where code lives, where results go, and how to check it works. A good scaffold is small, has no fake code, and passes a real check on day one.

## Recipe

1. **Look first.** List the target directory. Never overwrite existing files; add only what's missing and report what you skipped.
2. **Create the standard layout** (see `references/scaffold-manifest.json`; leave out a directory only if it clearly has no use here):

   | Path | Holds | Git |
   |---|---|---|
   | `src/<package>/` | importable code; entry point is thin | tracked |
   | `tests/` | tests plus a small `fixtures/` folder | tracked |
   | `docs/` | architecture, decisions (`docs/adr/`), plans | tracked |
   | `input/` | source data and cloned upstream repos (read-only) | ignored except `README.md` |
   | `output/` | generated artifacts, reproducible from `input/` | ignored except `README.md` |
   | `README.md` | purpose, layout table, quickstart, status | tracked |

3. **Explain each data directory.** `input/README.md` and `output/README.md` say what goes there, where it comes from (URL + pinned commit), and how to regenerate it. Empty directories otherwise disappear from git.
4. **Write a `.gitignore`** that ignores `input/*` and `output/*` but keeps their READMEs, plus language caches and virtualenvs.
5. **Pick the toolchain on purpose** (`choosing-tools-and-substrates`). Write the minimal manifest (`pyproject.toml`, `package.json`, …) with a name, version, and test command. No speculative dependencies.
6. **Add one smoke test that really runs** (e.g., imports the package). Run it. A scaffold that has never been executed isn't done (`layered-verification-gates`).
7. **README skeleton:** one-paragraph purpose, layout table, quickstart commands you actually ran, status line ("scaffold only").
8. **Agent context:** add a short `CLAUDE.md`/`AGENTS.md` only if agents will work here (`writing-agent-context-files`).
9. **Planning home:** if a plan exists, save it in the repo (`docs/` or `.planning/`), not only in chat.
10. **Git:** `git init` on `main` if needed. Commit or create a remote only when asked (`committing-and-releasing-cleanly`).

## Common mistakes

- Placeholder modules full of stub classes that later work has to delete.
- Committing cloned upstream repos or large data under `input/`; record the URL and commit instead.
- Generated files in `output/` that nothing can regenerate.
- A README quickstart nobody ran.
- Absolute machine paths in configs or docs (`keeping-repos-portable`).
