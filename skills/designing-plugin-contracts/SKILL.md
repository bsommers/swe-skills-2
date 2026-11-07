---
name: designing-plugin-contracts
description: Use when a host must work with several interchangeable implementations (drivers, adapters, renderers, backends, providers), when building cross-platform drivers for Windows, macOS, and Linux, when adding "just one more" implementation forces changes to the host, or when needing offline/mock modes that match live behavior.
---

# Designing Plugin & Cross-Platform Driver Contracts

## Overview

The host depends on a **small, OS-agnostic contract**, never on concrete implementations or OS conditionals. Adding a provider or targeting **Windows, macOS, and Linux** from day one is *write one adapter per backend/OS, register once* — with zero `if platform == ...` branching in the host.

## Shape of a Good Contract

| Example | Contract |
|---|---|
| Cross-platform session/PTY drivers (`Windows`, `macOS`, `Linux`, `Mock`) | `spawn(cmd, env, cwd)`, `write(data)`, `resize(cols, rows)`, `close()`; callbacks `onData`, `onExit`, `onError` |
| Chart / UI plugin | `dataAdapter(raw) → normalized`, `themeAdapter(theme) → lib theme`, `Renderer(props)` |
| Storage / provider | `get`, `put`, `list`, and a typed error set |

## Rules

1. **2–5 members.** If the contract keeps growing per implementation, split it or push variation into config.
2. **Build for Windows, macOS, and Linux from day one.** Never scatter `#[cfg(windows)]`, `sys.platform`, or `process.platform` across host logic. Isolate OS primitives behind platform driver implementations (`WindowsDriver`, `MacOSDriver`, `LinuxDriver`, plus `MockDriver`) — see `references/cross-platform-driver-architecture.md`:
   - **Process & PTY:** Windows ConPTY + Job Objects + `PATHEXT` vs. macOS/Linux POSIX `openpty`/`forkpty` + process groups (`-pgid`) + `SIGWINCH`.
   - **IPC & Transport:** Windows Named Pipes (`\\.\pipe\<name>`) or loopback TCP vs. macOS/Linux Unix domain sockets (keep socket paths `< 100` bytes for macOS `sun_path`).
   - **Filesystem & Paths:** Structured `Path`/`PathBuf` (never string-joined `/` or `\`), atomic replace (`MoveFileExW` on Windows vs. `rename` on POSIX), case-sensitivity awareness, and `CRLF`/`LF` normalization (`keeping-repos-portable`).
   - **Standard Directories:** Windows `%APPDATA%`/`%LOCALAPPDATA%`, macOS `~/Library/Application Support` & `~/Library/Caches`, Linux `$XDG_CONFIG_HOME` & `$XDG_STATE_HOME`.
3. **Normalize events and errors at the boundary.** Map each OS/backend's native lifecycle (Windows `CTRL_BREAK_EVENT`/exit code, POSIX `SIGTERM`/`SIGHUP`, SSH timeout) onto the contract's typed events and errors.
4. **Register once & lazy attach.** Single `register(driver)` lookup by key; allocate expensive handles on first use.
5. **Degrade gracefully & support mock/live parity.** Provide an in-memory/mock driver implementing the identical contract for fast cross-OS unit tests (`designing-testable-seams`).
6. **Shared tri-OS contract test suite.** Write one exhaustive contract test suite (`designing-exhaustive-test-cases`) that runs against *every* driver implementation across **Windows, macOS, and Linux** (`test-coverage`).
7. **Discovery + reattach.** Rediscover surviving sessions at startup and reattach idempotently.

## Example (TypeScript)

```ts
export interface SessionDriver {
  write(data: string): void;
  resize(cols: number, rows: number): void;
  close(): Promise<void>;
  onData(cb: (chunk: string) => void): void;
  onExit(cb: (code: number) => void): void;
  onError(cb: (err: Error) => void): void;
}
// Host selects WindowsConPtyDriver | PosixPtyDriver (macOS/Linux) | MockPtyDriver via registry
```

## Common Mistakes

- Leaking OS or implementation handles (raw PTY fd, Windows `HANDLE`, ORM entity) through the contract.
- Assuming POSIX-only paths, signals, or `fork()` in core logic and bolting Windows/macOS support on later.
- Mock and live drivers diverging until tests pass against a fiction.
- Running coverage on Linux only while leaving Windows and macOS driver adapters untested (`test-coverage`).
