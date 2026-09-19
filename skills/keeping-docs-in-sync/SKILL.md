---
name: keeping-docs-in-sync
description: Use when a change alters commands, flags, behavior, capabilities, counts, or architecture that documentation describes; before committing feature work; or when docs contain numbers or examples that may have drifted.
---

# Keeping Docs in Sync

## Overview

Docs drift silently and then mislead agents and humans alike. Make sync **part of the change**: same commit, checked by a script, with numbers derived rather than typed.

## Rules

1. **Same commit.** A feature isn't complete until affected docs are updated in that commit or milestone.
2. **Checklist by change type:**

   | You changed | Update |
   |---|---|
   | CLI flag/subcommand | CLI reference, README quickstart, changelog, shell completions/editor config |
   | Behavior | how-to, architecture note, changelog |
   | Module boundary | architecture diagram, agent context file (`writing-agent-context-files`) |
   | Capability added/removed | capabilities registry (human + machine) |
   | Test/count/corpus size | wherever it's quoted — or remove the number |
3. **Derive counts.** Generate test totals, capability counts, and coverage from commands, or write "as of `<commit/date>`". Hand-typed numbers rot first.
4. **Changelog per commit,** reverse-chronological: Added / Changed / Fixed, plus the verification you ran (command → result).
5. **Machine + human views** of anything both audiences use: `CAPABILITIES.md` and a `capabilities.json` with entrypoints, commands, and test commands; validate the schema in a script.
6. **Mark history as history.** Build logs, old specs, and phase notes get a banner "historical — see docs/…". Living docs are few and current.
7. **Relative links only.** No absolute paths (see `keeping-repos-portable`).
8. **Diagrams and text agree.** Every node in a diagram exists in the prose and code; sanitize labels so Mermaid renders (parentheses, colons, and quotes in edge labels break it).
9. **Docs coherence check** in the gate script: greps for stale terms, verifies links resolve, compares quoted counts to real ones.

## Docs check sketch

```bash
# fail on broken relative links, absolute paths, and count drift
python scripts/check_docs.py   # links resolve · no /home/ or /Users/ · quoted counts == computed
```

## Doc types worth having

README (what/why/quickstart) · HOW_TO (tasks) · ARCHITECTURE (structure, flows) · PURPOSE (problem, non-goals) · CHANGELOG · reference (CLI/API) · ADRs · agent context file.

## Common mistakes

- "Docs later" — later never has the context.
- Updating the README but not the CLI reference.
- Copy-pasted command output that's now stale.
- Ten overlapping docs with unclear authority.
- Claiming coverage or grades the last scan didn't show.
