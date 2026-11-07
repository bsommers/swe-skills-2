---
name: keeping-event-loops-responsive
description: Use when adding a wait, sleep, poll, or "wait until X" request handler to a single-threaded or single-owner request/serve loop (RPC, socket, MCP, or IPC server), when a server hangs until a wait times out, or when adding an input filter/debounce/dedup (e.g. dropping key auto-repeat) ahead of a router that may forward the input.
---

# Keeping Event Loops Responsive

## Overview

If a handler sleeps or polls inside a single-owner loop, every other client is blocked, including the client that would deliver the awaited event. The wait can only succeed if the event already happened: a self-deadlock that surfaces as a timeout.

## Rules

1. **Park the waiter, don't block.** Store request id, reply channel, and deadline; return to the loop.
2. **Re-check parked waiters** after each handled request, and on a periodic tick that runs **only while waiters exist** (no idle wakeups).
3. **Bound parked waiters.** On overflow, answer immediately rather than queueing.
4. **Drop waiters whose client disconnected.**
5. **Keep response shapes byte-identical** to the old blocking version, including the timeout reply.
6. **Purely sequential transports** (stdio, scripted playbooks) cannot deliver anything during the wait. Check once and answer immediately. Document this as a behavior change.

## Filter only what you consume

Place an input filter, debounce, or dedup where the consumer is known, or gate it on "will this layer consume the event?". A filter that runs before routing also swallows events that are merely passing through to a child (e.g. dropping key auto-repeat for a toggle chord also kills a held key forwarded raw to an editor: one keypress, then nothing). Test both paths: consumed (press, then repeat, filtered) and passthrough (press, then repeat, forwarded bytes match).

## Tests (over a real socket)

- A reply or event sent mid-wait completes the parked wait.
- An unrelated request is answered while a wait is pending.
- Timeout response shape is unchanged.
- Disconnect during a wait leaks nothing; waiter cap answers immediately.

## Common mistakes

- Moving the sleep into a helper thread that still holds the state lock.
- A timer tick that runs forever, even with nothing parked.
- Testing only with a mock clock and an in-process call, so the deadlock never reproduces.
- Changing the timeout payload while "refactoring".
- Filtering auto-repeat/duplicates before routing, so keys this layer never handles are dropped too.

Related: `designing-testable-seams`, `debugging-across-layers` (a timeout that ignores tuning is often a deadlock), `sizing-limits-from-measurement`.
