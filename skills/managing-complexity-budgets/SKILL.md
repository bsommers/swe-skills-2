---
name: managing-complexity-budgets
description: Use when files or functions are growing large, before adding a feature to an already big module, when an agent's edits keep breaking unrelated things, or when planning where new code should live.
---

# Managing Complexity Budgets

## Overview

Complexity creep is gradual and agent-accelerated. Give the codebase **numeric budgets**, check them at two moments — *before planning* and *before acting* — and decompose when you cross, before adding more.

## Starting budgets (tune per project, write them down)

| Metric | Warn | Limit | Action when crossed |
|---|---|---|---|
| Logical LOC per file | 200 | 250 | split into a package/registry |
| Functions per file | 10 | 15 | extract helpers/subcommands |
| Classes per file | 3 | 5 | one model per file |
| Nesting depth | 3 | 4 | guard clauses, early returns |
| Imports (fan-in coupling) | 15 | 20 | facade or dependency injection |
| Distinct responsibilities | 3 | 5 | separate modules |

Budgets are triggers to *look*, not laws; a 400-line file of one flat table is fine. Record deliberate exceptions.

## Dual gate

1. **Pre-planning:** survey the target area. Measure it. If it's above warn, the plan's first task is to decompose, not to add.
2. **Pre-action:** immediately before editing, recheck size, blast radius (who imports this?) and invariants. If it changed since you planned, stop and replan.

If either gate trips: decompose or escalate. Don't proceed "just this once".

## Decompose safely

1. Add characterization tests around current behavior first.
2. Extract one cohesive unit at a time; keep the old import path working via re-export.
3. Run the tests after every extraction; commit each.
4. Never mix decomposition and behavior change in one commit.

## Measure cheaply

A ~40-line script can count logical lines, functions, max indentation, and imports per file and print offenders. Run it in the test suite or pre-commit. Look for fan-in hubs: modules everything imports.

## Common mistakes

- Refactoring and adding features together, so a regression can't be localized.
- Splitting by file size rather than by responsibility.
- Budgets nobody measures.
- A `utils` module that becomes the new monolith.
- Letting an agent append to the biggest file because it's "where things are".
