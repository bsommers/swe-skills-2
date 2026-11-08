---
name: writing-user-guides
description: Use when authoring, structuring, or refreshing user guide documentation, README, purpose, architecture, running/using, or how-to docs for a repository, CLI, library, or service; when documentation belongs in docs/; or when connecting a quickstart README to a full documentation suite.
---

# Writing User Guides & Documentation Suites

## Overview

A README gives a quick orientation, but users and agents need a complete, synchronized documentation hub: purpose and threat model, architecture and subsystems, running/using configuration, task walkthroughs with rendered graphic examples, and a chapter-by-chapter user manual.

## Core Rules

1. **Maintain the complete documentation suite in `docs/` + root `README.md`.**
   - **Root `README.md`:** Hero banner/logo (`designing-logos-and-icons`), concise purpose, visual showcase preview (`showcasing-graphics-in-docs`), quickstart commands, link to the accompanying GitHub Pages showcase (`building-github-pages-sites`), and navigation table to `docs/`.
   - **`docs/README.md`:** Central navigational index and recommended reading order.
   - **`docs/purpose.md`:** Problem statement, core tenets, threat model, and empirical provenance.
   - **`docs/architecture.md`:** High-level layered architecture, subsystem deep-dives, lifecycle hooks, and visual models (`rendering-graphic-examples`).
   - **`docs/running.md` (Using & Configuration):** Prerequisites, installation targets, profile-based surfacing, CLI reference, environment variables, and exit codes.
   - **`docs/how-to.md`:** Copy-pasteable operational recipes accompanied by rendered SVG/PNG workflow diagrams (`rendering-graphic-examples`).
   - **`docs/usermanual/` (or `docs/user-guide/`):** Multi-chapter reference manual (`01-getting-started.md` through `07-troubleshooting-and-faq.md`) with `README.md` entry point and `[← Back to Project README](../../README.md)` backlink.
2. **Required structural sections across the guide:**
   - **Table of Contents:** Anchor links to every section or chapter.
   - **Getting Started & Bootstrap Workflow:** Prerequisites, multi-scope installation (`--local`, `--global`, `--prefix`), initialization, and `init → verify → first run` (`building-installers-and-onboarding`).
   - **Visual Examples & Recipes:** Task walkthroughs with real inputs, expected outputs, and accompanying SVG/PNG visuals (`rendering-graphic-examples`, `showcasing-graphics-in-docs`).
   - **Reference:** CLI flags, config schemas, environment variables, and exit codes.
   - **Troubleshooting & FAQ:** Common errors, root causes, and remedies.
3. **Runnable, verified examples & portable links.**
   - Test example commands against the codebase before documenting. Never invent flags.
   - Use relative paths across `README.md`, `docs/`, `docs/index.html`, and guide chapters (`keeping-repos-portable`). Never use absolute machine paths.
4. **Synchronize docs, graphics, and GitHub Pages together.**
   - Refresh `README.md`, `docs/purpose.md`, `docs/architecture.md`, `docs/running.md`, `docs/how-to.md`, `docs/usermanual/`, rendered graphics, and `docs/index.html` in the same commit whenever capabilities or counts change (`keeping-docs-in-sync`).

## Guide Template

```markdown
# [Project Name] User Guide

[← Back to Project README](../../README.md)

## Table of Contents
- [Getting Started](#getting-started)
- [Examples & Visual Walkthroughs](#examples--visual-walkthroughs)
- [Reference](#reference)
- [Troubleshooting & FAQ](#troubleshooting--faq)
```

## Common Mistakes

- **Orphaned guide or missing hub links:** Writing `docs/` files without linking them from root `README.md`, `docs/README.md`, and `docs/index.html`.
- **Stale architecture/purpose counts:** Updating `README.md` while leaving old capability counts or outdated diagrams in `docs/purpose.md` or `docs/architecture.md`.
- **Wall of text without visual examples:** Omitting rendered SVG/PNG diagrams (`rendering-graphic-examples`) for complex multi-step workflows.
- **Untestable examples:** Commands that fail or refer to non-existent flags.
