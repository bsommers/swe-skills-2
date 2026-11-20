---
name: hunting-cross-pipeline-desync
description: Use when auditing a multi-stage app or tool for bugs where preview, export, wire output, and persistence disagree, when switching documents or modes leaves stale caches, when downstream printers, browsers, or hardware mis-scale output, or when checking behavioral parity against a reference program.
---

# Hunting Cross-Pipeline Desync

## Overview

In multi-stage systems, unit tests on individual modules often pass while the full workflow silently diverges: the UI preview honors a setting that the exporter hardcodes, opening a second document leaks caches from the first, or emitted bytes omit metadata that downstream consumers need. Audit systematically across four axes rather than waiting for field reports.

Use `references/audit-checklist.md` for the consumer-matrix template and domain probe tables.

## 1. Cross-Pipeline Desync & Dual Sources of Truth

1. List every shared domain concept (geometry, margins, units, permissions, pricing, schema defaults, device limits).
2. For each concept, enumerate **every consumer**: UI preview, export/print/render, wire/API/hardware emitter, persistence (save/load), and undo/redo.
3. Trace where each consumer reads its value. Flag any path that hardcodes a literal, duplicates a calculation, or drops a transform.
4. Collapse divergent paths onto one canonical helper or value object, then add a parity test asserting every consumer produces the same geometry, totals, or state for non-default inputs.

## 2. State Lifecycle & Stale-Cache Auditing

1. Enumerate every lifecycle transition: `open A → open B`, `new`, `close`, mode/tab switch, `undo`/`redo`, reconnect, and `reset`.
2. Inventory all parallel mutable state: GPU textures, raster/layout caches, selection handles, undo stacks, derived indices, and open sockets/files.
3. Verify every transition clears or invalidates **all** parallel state in one shared teardown/reset path — never ad-hoc per call site.
4. Test with a stateful sequence: populate A (custom settings, cached assets, active selection), transition to B, and assert zero artifacts from A survive.

## 3. Output & Wire Metadata Fidelity

Inspect emitted bytes and protocol frames the way downstream consumers read them, not just in-memory structs:

- **Physical & visual artifacts:** PNG `pHYs` DPI chunks, JPEG density headers, PDF `MediaBox`/`CropBox`, SVG `viewBox`/physical units, color profiles.
- **Web & API outputs:** `Content-Type`, charset, `Content-Disposition`, pagination/cache headers, timezone/currency units.
- **Binary & hardware wire formats:** framing delimiters, byte order, unit scaling, coordinate-space clamping, and command ordering.

Add tests that parse emitted bytes (e.g., reading the PNG `pHYs` chunk or wire frame) and assert exact metadata and bounds.

## 4. Reference-Program Behavioral Parity

When building a compatible tool or replacement for an established program (design studio, spreadsheet, editor, CLI), audit its domain invariants alongside its feature list:

- **Output hygiene:** hidden guides, grids, and non-print layers never leak into export or execution.
- **Execution order:** domain-required sequencing (e.g., inner cutouts before outer contours, schema migrations before data loads).
- **Space & safety invariants:** physical vs. logical coordinate separation, keepout/margin zones, clamping to valid bounds.
- **Ergonomics:** power-user keyboard shortcuts, modifier drags, and focus/undo semantics matching user muscle memory.

## Common mistakes

- Testing preview, export, and wire emitters only in isolation with default settings (defaults hide hardcoded duplicates).
- Resetting the primary document struct on `open`/`new` while forgetting parallel caches, textures, or selection state.
- Asserting pixel width/height or payload length without inspecting DPI, page-box, or framing metadata.
- Copying a reference tool's UI controls while silently breaking its physical or workflow invariants.

Pairs with `hunting-silent-failures`, `debugging-across-layers`, `designing-uniform-surfaces`, and `layered-verification-gates`.
