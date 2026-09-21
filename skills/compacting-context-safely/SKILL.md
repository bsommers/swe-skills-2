---
name: compacting-context-safely
description: Use when an agent's context window is filling up, auto-compaction is near, responses are slowing or forgetting earlier decisions, the task is switching to unrelated work, or before running /compact, /clear, or starting a fresh session mid-task.
---

# Compacting Context Safely

## Overview

Compaction and clearing are lossy: unwritten conversation state is lost. **Write it down, verify on disk, then shrink.**

- **Claude Code:** Supports `/compact` (in-place) and `/clear`.
- **Antigravity (`agy`):** Has **no `/compact`**. Shrinking context requires starting a fresh session from a checkpoint.

## Decide: keep, trim, compact, or clear

| Situation | Action |
|---|---|
| Room left; work flowing | Keep going |
| Bloat from big outputs, searches | **Trim upstream** first (primary defense in `agy`) |
| Same goal, history spent (Claude) | **Compact** with focus instructions |
| Same goal, history spent (`agy`) | **Checkpoint and start fresh session** |
| Unrelated next task, or polluted context | **Clear** (Claude) or fresh session (`agy`) after checkpointing |
| Mid-edit, tests red, change unverified | **Not yet:** reach a stable point, or record unstable state |

## Trim upstream (cheapest)

- Delegate wide searches and log reading to a subagent that returns conclusions (`orchestrating-subagents`).
- Read line ranges; don't re-read files already in context.
- Cap output (`| tail -50`, `-q`); send big logs to a file and grep it.

## Pre-flight (before compact, clear, or session reset)

1. **Reach a stable point** and record baseline check result.
2. **Write a checkpoint file** (`handing-off-sessions` format):
   - **Goal** in user's words; **decisions and corrections verbatim** (costliest to lose).
   - **Dead ends** and why they failed.
   - **Working-tree state:** branch, uncommitted files, stashes, background processes, ports.
   - **Authorizations** given and scope; re-confirm outward-facing ones after reset.
   - **Exact next command.**
3. **Protect uncommitted work:** commit only if allowed; never stash or reset to "clean up."
4. **Re-read checkpoint** as zero-context reader: could you resume from it alone?
5. **Persist lasting lessons** to context file (`writing-agent-context-files`).

## Run it

- **Claude Code:**
  - **Compact:** `/compact keep: goal, user decisions, files changed, failing test X, next step; checkpoint at docs/plans/checkpoint.md`.
  - **Clear:** Run `/clear` with checkpoint on disk; resume with `"Read <checkpoint> and verify its state claims."`
- **Antigravity (`agy`):**
  - **Never suggest `/compact`** (command does not exist in `agy`).
  - Write checkpoint, exit (`/exit` or `Ctrl+D`) or new chat, then resume: `"Resume from <checkpoint>. Verify its state claims before continuing."`
- If unable to trigger reset directly, give the **exact command for the harness**.
- Hooks: Claude guards `PreCompact` and `UserPromptSubmit`; `agy` injects checkpoint on `SessionStart`.

## After: verify continuity

1. Re-read the checkpoint; check branch, `git status`, and files against it.
2. Rerun the baseline check; it must match.
3. Restate goal and next step in one line. If a user decision is missing or unclear, **ask**; don't reconstruct it.

## Common mistakes

- Recommending `/compact` in `agy` where the command does not exist.
- Compacting mid-debug and retrying a failed approach.
- Trusting auto-summaries over verified checkpoint files.
- Losing user corrections, then repeating the mistake.
- Treating pre-reset approvals as still valid.
- Resetting with background jobs running, orphaning them.
- Compacting or resetting every few turns "to be safe."
