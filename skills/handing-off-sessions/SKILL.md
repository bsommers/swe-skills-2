---
name: handing-off-sessions
description: Use when pausing or ending a work session, resuming after a break or context reset, transferring work to another agent or person, or preserving what was learned, including scratch tools and as-built specifications.
---

# Handing Off Sessions

## Overview

Context evaporates; files persist. Leave a record a **zero-context reader** can act on in minutes: what's done (with evidence), what failed (with cause), what changed underneath, and the exact next command.

## Checkpoint file (write before stopping)

```markdown
# Checkpoint — <topic> — 2026-09-19
**Status:** IN PROGRESS — needs resume  (or COMPLETE)
## Done (with evidence)
- Step 1 … `pytest tests/test_x.py` → 12 passed
## Failed / blocked (with root cause)
- Load returned 0 rows. Root cause: input files didn't exist when it ran.
## Bugs fixed this session (so they aren't reintroduced)
- `device_types.py`: `key: value` used where `key = value` was needed …
## State that may have changed
- `data/simulated-sites/` was empty when last checked — regenerate.
## Next steps (exact commands, in order)
1. `python -m generators.site_generator`
2. `pytest -q` → expect N passed
## Open questions
```

## Resuming

1. Read the checkpoint, then **verify its state claims** (files, services, branch, versions). Trust nothing about state.
2. Rerun the baseline test command before continuing.
3. Update the checkpoint as you go.

## Journals

For sessions that discover things, keep a dated journal entry: intent, decisions, surprises/gotchas, hypotheses, dead ends. Dead ends prevent repeat work.

## Preserve incidental tools

Ad-hoc parsers, probes, repro harnesses, generators: keep them (`scripts/incidental/`, `tools/`), with a header:

```
# INCIDENTAL TOOL: <name> · <date>
# Context: <plan/issue/bug id>   Purpose: <why it exists>
# Usage: <exact command>          Archaeology: <assumptions, edge cases it revealed>
```
Include a shebang and `--help`. They record how the problem was actually understood.

## As-built rebuild spec

When a codebase must be reproducible by a fresh agent, write a spec **from the live source, not from memory or the original spec**:

- Purpose and **non-negotiable design properties** (a rebuild that drops these hasn't rebuilt it).
- Stack, versions, external services.
- Module map in dependency order, with signatures and defaults.
- The bugs found and fixed, so the "obvious" implementation isn't repeated.
- Verified numbers (module count, test count, date) and exact commands to confirm a rebuild.
- A *Divergence from the original spec* section.

## Common mistakes

- Handoff that says what was done but not what to run next.
- Copying a stale "status" without re-verifying.
- Deleting scratch tools "for cleanliness".
- A rebuild spec written from the old prompt instead of the code.
