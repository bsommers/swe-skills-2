---
name: compacting-context-safely
description: Use when an agent's context window is filling up, auto-compaction is near, responses are slowing or forgetting earlier decisions, the task is switching to unrelated work, or before running /compact, /clear, or starting a fresh session mid-task.
---

# Compacting Context Safely

## Overview

Compaction and clearing are lossy: whatever lives **only** in the conversation (a user's correction, a failed approach, a half-edited file) is gone. **Write it down, verify it's on disk, then shrink.**

## Decide: keep, trim, compact, or clear

| Situation | Action |
|---|---|
| Room left; work flowing | Keep going |
| Bloat from big outputs, re-reads, broad searches | **Trim upstream** first |
| Same goal, history mostly spent | **Compact** with focus instructions |
| Unrelated next task, or context polluted by dead ends | **Clear** after checkpointing |
| Mid-edit, tests red, change unverified | **Not yet:** reach a stable point, or record the unstable state explicitly |

## Trim upstream (cheapest)

- Delegate wide searches and log reading to a subagent that returns conclusions (`orchestrating-subagents`).
- Read line ranges; don't re-read files already in context.
- Cap output (`| tail -50`, `-q`); send big logs to a file and grep it.

## Pre-flight (before any compact or clear)

1. **Reach a stable point** and record the baseline check's result.
2. **Write a checkpoint file** (`handing-off-sessions` format), plus:
   - **Goal** in the user's words; **decisions and corrections verbatim** (easiest to lose, costliest to repeat).
   - **Dead ends** and why they failed.
   - **Working-tree state:** branch, uncommitted files, stashes, worktrees; **background processes** and ports.
   - **Authorizations** given and their scope; re-confirm outward-facing ones after a reset.
   - **Exact next command.**
3. **Protect uncommitted work:** commit only if the user's workflow allows; never stash or reset to "clean up."
4. **Re-read the checkpoint** as a zero-context reader: could you resume from it alone?
5. **Persist lasting lessons** to memory or the context file (`writing-agent-context-files`).

## Run it

- **Compact** with focus instructions naming what must survive, e.g. `/compact keep: goal, user decisions, files changed, failing test X, next step; checkpoint at docs/plans/checkpoint.md`.
- **Clear** only with the checkpoint on disk; resume with "Read `<checkpoint>` and verify its state claims."
- If the agent can't trigger it, it prepares the checkpoint and **gives the user the exact command**.
- Don't rely on noticing. Where the harness has hooks, wire the reminder, the pre-compaction checkpoint check and the post-reset injection there.

## After: verify continuity

1. Re-read the checkpoint; check branch, `git status`, and files against it.
2. Rerun the baseline check; it must match.
3. Restate goal and next step in one line. If a user decision is missing or unclear, **ask**; don't reconstruct it.

## Common mistakes

- Compacting mid-debug and then re-trying an approach that already failed.
- Trusting the auto-summary instead of a file you wrote and checked.
- Losing a user correction, then repeating the mistake it corrected.
- Treating pre-reset approval to push or delete as still valid.
- Clearing with a background job running, orphaning it.
- Compacting every few turns "to be safe."
