---
name: writing-user-guides
description: Use when authoring, structuring, or updating user guide documentation for a repository, CLI, library, or service; when documentation belongs in a dedicated subdirectory of docs/; or when connecting a quickstart README to a detailed user guide.
---

# Writing User Guides

## Overview

A README gives a quick orientation, but users need task walkthroughs, reproducible examples, and complete reference docs. Write comprehensive user guides in a dedicated subdirectory of `docs/` (e.g. `docs/user-guide/`), maintain bidirectional navigation with the root `README.md` (creating it if absent), and keep guidance verifiable.

## Core Rules

1. **Subdirectory placement under `docs/`.**
   - Place user guides in a dedicated subdirectory of `docs/` (`docs/user-guide/` or `docs/guide/`).
   - Use `docs/user-guide/README.md` (or `index.md`) as the entry point.
   - For multi-page guides, split chapters into modular files in that subdirectory and link them from the entry document.
2. **Bridge root `README.md` (create if missing).**
   - If the root `README.md` is missing, create a concise one: title, 1–2 sentence purpose, quickstart snippet, and an explicit link to `docs/user-guide/`.
   - If present, add or verify a prominent link under "Documentation" or "User Guide" pointing to `docs/user-guide/README.md`.
   - Always include a relative backlink in the user guide pointing to the root `README.md` (`[← Project README](../../README.md)`).
3. **Required structural sections:**
   - **Table of Contents:** Anchor links to every section or chapter.
   - **Getting Started:** Prerequisites (runtimes, dependencies, accounts), installation, and a two-minute first run command.
   - **Examples:** Copy-pasteable task recipes with real inputs and expected outputs. Cover basic usage and common workflows.
   - **Reference:** Comprehensive CLI flags, config schemas, API endpoints, environment variables, and exit codes.
   - **Troubleshooting & FAQ:** Common errors, diagnostics, and remedies.
4. **Runnable, verified examples.**
   - Test example commands against the current codebase before documenting. Never invent flags or syntax.
   - Use realistic defaults or standard env placeholders (`$API_KEY`), never invalid pseudo-code.
5. **Portable relative links.**
   - Use relative paths across the root `README.md`, `docs/`, and guide files (see `keeping-repos-portable`). Never use absolute machine paths.
6. **Synchronize docs with behavior changes.**
   - Update user guides and README links in the same commit whenever CLI flags, options, or behaviors change (see `keeping-docs-in-sync`).

## Guide Template

```markdown
# [Project Name] User Guide

[← Back to Project README](../../README.md)

## Table of Contents
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Reference](#reference)
- [Troubleshooting & FAQ](#troubleshooting--faq)

## Getting Started
Prerequisites, installation, and first working command.

## Examples
### Basic Usage
Task walkthrough with expected output.

## Reference
CLI flags, config schema, environment variables, exit codes.

## Troubleshooting & FAQ
Error symptoms, causes, and solutions.
```

## Common Mistakes

- **Orphaned guide:** Writing `docs/user-guide/` without a pointer from root `README.md`, or omitting backlinks.
- **Ignoring missing README:** Creating deep docs in `docs/` while leaving repository root without a `README.md`.
- **Bloating root README:** Inverting hierarchy by stuffing full references into root README instead of `docs/`.
- **Missing Table of Contents:** Long pages without navigable anchor links.
- **Untestable examples:** Commands that fail or refer to non-existent flags.
