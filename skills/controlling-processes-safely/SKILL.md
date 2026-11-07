---
name: controlling-processes-safely
description: Use when code reads a PID from a pid or lock file, sends signals to a daemon or child process, implements stop/restart/status for a background service, or decides whether a process is still running.
---

# Controlling Processes Safely

## Overview

A PID in a file is untrusted data, and "a process with that PID exists" does not mean "my daemon". After a crash and PID reuse, a naive stop command can kill an unrelated process, or everything the user owns.

## Rules

1. **Validate the PID range before `kill(2)`.** Reject `<= 0` (0 signals the process group, -1 signals every process you own), reject 1 (init), reject values that overflow `pid_t`.
2. **Liveness is not identity.** `kill(pid, 0)` succeeding after a stale lockfile may hit a stranger.
3. **Prove ownership via the lock.** Try a non-blocking exclusive `flock` on the lockfile:
   - You can take it: the lock is stale. Clean up, report "not running", send **no** signal.
   - It is held (would block): the daemon is alive and owns it; proceed.
   - Unexpected error: refuse to signal.
4. **The lock must live on the inode the daemon writes.** Write the PID by in-place truncate+write on the locked file. Atomic rename replaces the inode, so the flock check then inspects a different file and lies.
5. **Report honestly:** distinct outcomes for not-running, stale-cleaned, signaled, refused.

## Tests

Use a real unrelated child process (for example `sleep`) whose PID is planted in a stale lockfile; assert stop reports not-running and the child **survives**. Also cover 0, -1, 1, and an overflowing value.

## Common mistakes

- Trusting `kill -0` as proof of ownership.
- Parsing the PID into a signed type and passing it straight to `kill`.
- Writing the pid file via temp-file-and-rename while also using it as the flock target.
- Falling through to "send the signal anyway" on an unexpected lock error.
- Testing only with mocks, never with a real bystander process.

Related: `hardening-trust-boundaries`, `building-unattended-agent-loops` (daemon lifecycle).
