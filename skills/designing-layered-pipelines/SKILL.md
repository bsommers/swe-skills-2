---
name: designing-layered-pipelines
description: Use when structuring a system with several stages, inputs, or outputs (compilers, transpilers, ETL, ingest-analyze-report), when logic is leaking into thin wrappers, or when the same types are declared in more than one place.
---

# Designing Layered Pipelines

## Overview

Split into **frontend → normalized IR → pure backends**. N inputs × M outputs becomes N + M pieces. Keep wrappers (CLI, DAG task, HTTP handler) thin and put logic in importable packages, so each stage can be tested and rerun alone.

```
Source ─▶ Parser ─▶ AST ─▶ Validator ─▶ IR ─▶ Emitter A / B / C
(IO edge)                    (pure)          (pure, deterministic)
```

## Rules

1. **Backends see only the IR.** If an emitter needs the raw source, the IR is missing a field — add it to the IR.
2. **Purity in the middle.** Parsing, validation, IR building, and rendering are functions of their inputs. Do IO at the edges (load, write, network).
3. **Imports flow one way.** Assign each module a tier; a module may import only from lower tiers. Enforce with an import-lint test. Back-edges are how cyclic deadlocks and unbuildable orders appear.
4. **One source of truth per shared type.** Re-export a type from its owner; never redeclare it on the other side of a boundary (client/server protocol types drift when duplicated).
5. **Thin wrappers.** A DAG file, CLI `main`, or handler parses arguments, calls a package function, reports the result. Nothing else.
6. **Stage hand-offs are artifacts.** Stages exchange files or records with a schema (JSON, SARIF, tables), so any stage can be rerun from its input without re-running upstream.
7. **Deterministic emission.** Sort, stabilize, and avoid timestamps so outputs diff cleanly (see `engineering-for-determinism`).

## Checks you can actually run

- Can I add a new backend without touching the frontend? (If no, the IR leaks.)
- Can I rerun stage 4 alone from stage 3's output?
- Does any file import "upward"? Does the same struct appear twice?
- Can I test each layer with no network, DB, or filesystem beyond a temp dir?

## Canonical layout

```
app/ or cmd/    CLI entry; option parsing; dispatch only
src/            Types → Parser → Loader → Validator → IR → Emitters/
test/           unit/  property/  integration/
examples/       real inputs used as fixtures by tests
docs/           architecture, how-to, changelog
scripts/        packaging, release, setup
```

## Common mistakes

- Emitters that call each other or reach into the parser.
- "Utility" modules that everything imports and that import everything.
- Business logic inside orchestrator DAG definitions, untestable without the scheduler.
- A validator that mutates the tree it validates.
- Number-prefixed files that aren't importable modules — load them explicitly in tests instead of renaming and losing ordering.
