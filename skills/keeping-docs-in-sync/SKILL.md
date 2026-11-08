---
name: keeping-docs-in-sync
description: Use when a change alters commands, flags, behavior, capabilities, counts, or architecture that documentation describes; before committing feature work; or when docs, rendered graphics, or GitHub Pages contain numbers or examples that may have drifted.
---

# Keeping Docs in Sync

## Overview

Docs, visual diagrams, and showcase pages drift silently and then mislead agents and humans alike. Make sync **part of the change**: same commit, checked by a script, with numbers and graphics derived rather than hand-typed.

## Rules

1. **Same commit.** A feature isn't complete until affected docs, rendered graphics, and showcase pages are updated in that commit or milestone.
2. **Checklist by change type:**

   | You changed | Update |
   |---|---|
   | CLI flag/subcommand | `docs/running.md`, CLI reference, `README.md` quickstart, `CHANGELOG.md` |
   | Behavior or workflow | `docs/how-to.md`, `docs/architecture.md`, `docs/purpose.md`, `CHANGELOG.md` |
   | Module boundary or subsystem | `docs/architecture.md`, rendered SVG/PNG diagrams (`rendering-graphic-examples`), agent context file (`writing-agent-context-files`) |
   | Skill / capability added or removed | `using-swe-skills`, `eng`, `README.md`, `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, `docs/usermanual/`, `docs/index.html` (`building-github-pages-sites`), `scripts/render-graphics.py` |
   | Test/count/corpus size | Every file quoting the count — or regenerate from the source of truth |
3. **Derive counts & re-render visuals.** Generate capability counts, test totals, and SVG/PNG visual badges (`rendering-graphic-examples`, `showcasing-graphics-in-docs`, `designing-logos-and-icons`) from scripts so banners and diagrams never lag behind the codebase.
4. **Changelog per commit,** reverse-chronological: Added / Changed / Fixed, plus the verification you ran (command → result).
5. **Machine + human views** of anything both audiences use: manifests (`plugin.json`), `README.md`, `docs/usermanual/`, and `docs/index.html`; validate consistency in tests.
6. **Mark history as history.** Build logs, old specs, and phase notes get a banner "historical — see docs/…". Living docs are few and current.
7. **Relative links only.** Verify all relative links in `README.md`, `docs/*.md`, and `docs/index.html` resolve on disk (`keeping-repos-portable`).
8. **Diagrams and text agree.** Every node or count in a Mermaid, draw.io, or SVG/PNG diagram exists in the prose and code.
9. **Docs coherence check** in the test suite: checks skill counts, version parity across manifests and docs, valid SVG/PNG assets, and zero broken links.

## Version strings and context files

Current-version strings drift across badges, headers, manifests, `README.md`, and GitHub Pages: derive from `plugin.json` or test-gate them, and leave historical changelog mentions alone. Details: `references/version-and-context-drift.md`.

## Doc types worth having

`README.md` (hero, showcase, quickstart) · `docs/purpose.md` (problem, threat model) · `docs/architecture.md` (subsystems, flows) · `docs/running.md` (install, profiles, CLI, env) · `docs/how-to.md` (recipes + graphic examples) · `docs/usermanual/` (7-chapter guide) · `docs/index.html` (GitHub Pages showcase) · `CHANGELOG.md`.

## Common mistakes

- "Docs later" — later never has the context.
- Updating `README.md` while `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, or `docs/index.html` still quote stale skill counts or versions.
- Forgetting to re-run `scripts/render-graphics.py` when counts or architecture tiers change.
- Claiming coverage or grades the last scan didn't show.
