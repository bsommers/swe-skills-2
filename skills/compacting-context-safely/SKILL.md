---
name: compacting-context-safely
description: Use when an agent's context window is filling up, auto-compaction is near, responses are slowing or forgetting earlier decisions, the task is switching to unrelated work, or before running /compact, /clear, or starting a fresh session mid-task.
---

# Compacting Context Safely

## Overview

Compaction and clearing are lossy: unwritten conversation state is lost. **Write it down, verify on disk, then shrink.**

- **Context replay multiplier:** Every tool turn (run, retry, background check) retransmits cumulative session history as input tokens. High turn counts on deep context multiply spend.
- **Claude Code:** Supports `/compact` (in-place) and `/clear`.
- **Antigravity (`agy`):** Has **no `/compact`**. Shrinking context requires starting a fresh session from a checkpoint.

## Decide: keep, trim, compact, or clear

| Situation | Action |
|---|---|
| Room left; work flowing (<12 turns / <25 steps since checkpoint) | Keep going |
| Periodic cadence (`>=12` turns or `>=25` steps with no fresh `<20m` checkpoint) | **Refresh `docs/CHECKPOINT.md`** at next stable boundary (`references/cadence-and-hooks.md`) |
| Phase/milestone/commit/release just completed | **Refresh `docs/CHECKPOINT.md`** and suggest `/compact` (Claude) or fresh session (`agy`) |
| Bloat from big outputs, searches | **Trim upstream** first (primary defense in `agy`) |
| Same goal, history spent (`>=70%` window in Claude) | **Checkpoint, then `/compact`** with focus instructions |
| Same goal, history spent (`>=50` steps in `agy`) | **Checkpoint and start fresh session** |
| Pausing work >15–30 min (cold prompt cache) | **Checkpoint, then `/compact` or `/exit`** (prevents 12.5x cold-cache rebuild penalty on resume) |
| Unrelated next task, or polluted context | **Clear** (Claude) or fresh session (`agy`) after checkpointing |
| Mid-edit, tests red, change unverified | **Not yet:** reach a stable point, or record unstable state |

## Regular Cadence & Hooks (`context_guard.py`)

Do not wait until the context window is 90% full. Enforce a **dual trigger** (automated hooks + natural boundary self-checks; details in `references/cadence-and-hooks.md`):

1. **Ensure hooks are installed:** Run `python3 scripts/hooks/context_guard.py report` to check token/turn usage, checkpoint freshness, `recommendation:` (`OK`, `CHECKPOINT_DUE`, `COMPACT_OR_RESET_NOW`), and `hooks:` status. If hooks are `missing`, proactively suggest installing them (`scripts/hooks/install-hooks.py --claude --agy --git`).
2. **Hook-fired periodic cadence:** `context_guard.py` nudges every `12` assistant turns (Claude `SWE_SKILLS_CHECKPOINT_CADENCE_TURNS`) or `25` steps (`agy` `SWE_SKILLS_CHECKPOINT_CADENCE_STEPS`) when no checkpoint was updated in `<20 min`, plus full compaction/reset nudges at `70%` window / `50` steps / `30 min` idle.
3. **Natural boundary self-check:** Always refresh `docs/CHECKPOINT.md` and suggest compacting/resetting after completing a plan phase, commit, or `/release`, when switching domains (Planning → Build → Review), or after recording 2+ dead ends.

## Pausing work & prompt cache TTL (5-minute cliff)

Anthropic's prompt cache has a **5-minute TTL**. Turns `<5 min` apart read cache at `0.1x` base rate; idle `>5 min` expires the cache and rebuilds at `1.25x` (**12.5x jump**).

- **Short pause (<5 min):** Leave session open; cache stays warm.
- **Long break (>15–30 min) or overnight:** Write a checkpoint (`handing-off-sessions`), stop background watchers/subagents, and run `/compact` or `/exit`. Never leave deep sessions idling with active background tasks.

## Trim upstream (cheapest)

- Delegate wide searches, log reading, and build/test loops to an ephemeral subagent (`orchestrating-subagents`).
- Suppress routine progress with quiet flags (`cargo test -q`, `pytest -q`, `npm test -s`), cutting tool-output tokens by ~90%.
- Read line ranges; don't re-read files in context. Cap output (`| tail -50`).

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
  - **Compact:** `/compact keep: goal, user decisions, files changed, failing test X, next step; checkpoint at docs/CHECKPOINT.md`.
  - **Clear:** Run `/clear` with checkpoint on disk; `SessionStart` auto-injects the checkpoint, or resume with `"Read <checkpoint> and verify its state claims."`
  - **5-Step Chain (`Checkpoint -> Compact -> Handoff -> /clear -> Resume`):**
    1. Write `docs/CHECKPOINT.md` (unlocks `PreCompact`).
    2. Run `/compact keep: <focus notes>; checkpoint at docs/CHECKPOINT.md`.
    3. Write synthesis/journal notes to `docs/HANDOFF.md` (or refresh `docs/CHECKPOINT.md` with `**Status:** IN PROGRESS — needs resume`).
    4. Run `/clear` (or `scripts/chain-session.sh`) — `SessionStart` injects the checkpoint/handoff into the fresh session.
- **Antigravity (`agy`):**
  - **Never suggest `/compact`** (command does not exist in `agy`).
  - Write `docs/CHECKPOINT.md` (and `docs/HANDOFF.md`), then:
    - **Interactive:** Exit (`/exit` or `Ctrl+D`) or open New Chat (`SessionStart` auto-injects the checkpoint),
    - **In-session subagent:** Spawn `self` (`invoke_subagent` with `TypeName: "self"`, `"Resume from docs/CHECKPOINT.md. Verify state claims before continuing."`), or
    - **CLI loop:** Run `scripts/chain-session.sh --agy`.
- If unable to reset directly, give the **exact command for the harness**.

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
