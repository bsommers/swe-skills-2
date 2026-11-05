---
name: designing-uniform-surfaces
description: Use when designing or planning a feature, tool, or service that people or programs will use through more than one interface (UI, keyboard, mouse, CLI, REST/RPC API, MCP, scripts), when a capability exists on one surface but not another, or when writing a plan or spec that adds user-facing functionality.
---

# Designing Uniform Surfaces

## Overview

Every capability is defined **once** as a command in a single core, then exposed on **every surface** that exists in the product. Surfaces are thin adapters; none owns behavior. Uniform by default, opt out explicitly.

## Surfaces checklist (starting points, extend per product)

| Surface | Exposes the capability as |
|---|---|
| Core command | One named operation with typed input/output (e.g. an `Action`/command object) |
| CLI / REPL | Subcommand or colon/slash command, with help and completion |
| API (HTTP/RPC) | Method returning structured data, same validation and gating |
| MCP | Tool or resource mapped to the same operation |
| Keyboard | A key sequence in each mode (GUI and terminal), declared in one binding table |
| Pointer | Click/drag/wheel path in each rendering mode |
| Discovery | Command palette entry, help text, docs, completion |
| Automation | Scripts/playbooks/events can invoke and observe it |

## Default behavior

1. **Ask or inject.** When designing or planning a capability, list which surfaces the product has. Either ask the user which to skip, or write all of them into the plan as tasks. Silence means "all".
2. **Core first.** Define the command and its result type before any adapter. Adapters only translate input and render output.
3. **One path to state.** Every surface calls the same dispatcher, so validation, permissions, logging and undo behave identically.
4. **Parity test.** One table-driven test drives each surface and asserts the same resulting state/output. A new command without all surface entries fails the test.
5. **Exceptions are written down.** Skip a surface only with a reason in an exclusion table (e.g. "needs free-form text: no menu entry"). Unlisted gaps are bugs.
6. **Gate once.** Dangerous or config-writing commands are gated in the core, so remote surfaces cannot bypass what the UI enforces.
7. **Structured output.** Return data, not just a status line, so APIs, MCP and scripts can read results.

## Plan injection

Add to each capability's task list: core command, parse/CLI form, API/MCP exposure, key binding per mode, pointer path, palette/help/docs, parity test. Success criteria name the path for each surface.

## Common mistakes

- UI-only features that scripts and agents cannot reach.
- A key binding that works in one rendering mode only.
- Each surface re-implementing validation, so behavior drifts.
- API added later by copy-pasting UI logic.
- Parity "documented" but not tested.
- Treating the exclusion list as optional.

See `planning-with-contracts`, `designing-plugin-contracts`, `evolving-schemas-and-contracts`.
