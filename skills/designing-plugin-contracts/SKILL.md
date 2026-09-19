---
name: designing-plugin-contracts
description: Use when a host must work with several interchangeable implementations (drivers, adapters, renderers, backends, providers), when adding "just one more" implementation forces changes to the host, or when needing offline/mock modes that match live behavior.
---

# Designing Plugin Contracts

## Overview

The host depends on a **small contract**, never on implementations. Adding an implementation is *write one adapter, register once* — with zero changes to the host. Keep the contract to a handful of operations and events.

## Shape of a good contract

| Example | Contract |
|---|---|
| Terminal session drivers | `write(data)`, `resize(cols, rows)`, `close()`; callbacks `onData`, `onExit`, `onError` |
| Chart plugin | `dataAdapter(raw) → normalized`, `themeAdapter(theme) → lib theme`, `Renderer(props)` |
| Storage / provider | `get`, `put`, `list`, and a typed error set |

## Rules

1. **2–5 members.** If the contract keeps growing per implementation, the abstraction is wrong; split it or push variation into config.
2. **Normalize events and errors at the boundary.** Map each backend's native lifecycle (SSH timeout vs process exit) onto the contract's events so the host has one code path.
3. **Register once.** A single `register(plugin)` call; the host looks plugins up by key. No `if type == "x"` in the host.
4. **Lazy attach.** Create expensive resources on first use, not at discovery, so idle entries cost nothing.
5. **Degrade gracefully.** If an optional runtime is absent (a binary not on PATH), report an empty/unavailable state instead of crashing the host.
6. **Same interface for mock and live.** Provide a mock implementation with the identical contract for offline development and tests; auto-select when the live backend is unreachable.
7. **Contract tests.** Write one suite that runs against *every* implementation; a new one passes it before it ships.
8. **Discovery + reattach.** If sessions can outlive the host, rediscover them at startup and reattach idempotently (create-or-attach semantics).

## Example (TypeScript)

```ts
interface SessionDriver {
  write(data: string): void;
  resize(cols: number, rows: number): void;
  close(): void;
  onData(cb: (chunk: string) => void): void;
  onExit(cb: (code: number) => void): void;
  onError(cb: (err: Error) => void): void;
}
// host: registry.get(kind).create(opts) — no branching on kind
```

## Common mistakes

- Leaking implementation types (a PTY handle, an ORM entity) through the contract.
- A "base class" with optional methods only some plugins implement.
- Mock and live diverging until tests pass against a fiction.
- Contract changes that are breaking, with no version.
