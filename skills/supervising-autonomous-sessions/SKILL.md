---
name: supervising-autonomous-sessions
description: Use when letting an AI coding session run for long stretches with little supervision, deciding how much autonomy to grant, when a session keeps retrying without progress, or when an agent might touch things outside its task.
---

# Supervising Autonomous Sessions

## Overview

Autonomy is a dial, not a switch. Set it by **reversibility and blast radius**, define when the agent must stop, and keep the human able to see and halt everything.

## Gears

| Gear | Mode | Use when |
|---|---|---|
| 1 Clocked | approval at each step | irreversible actions, unfamiliar code, security-sensitive |
| 2 Checkpointed | runs a phase, pauses for review | multi-file features with clear tests |
| 3 Lights-out | runs freely while making verified progress | well-specified, reversible, well-tested work |

The human can shift gears any time. Prefer lower gears for anything touching shared state, credentials, production, or other repos.

## Preconditions for lights-out

- A brief with scope and a **go-ahead** (`writing-intent-briefs`), a plan with verify commands (`planning-with-contracts`), and a green baseline.
- Work happens on a branch or worktree.
- Budgets set (time, tokens, retries) and a visible status output.

## Halt conditions

Stop and report — do not push through — when:

1. **> 3 consecutive non-convergent retries** (same error signature, or a repair whose diff is essentially the same as the last).
2. A **pre-action check** fails: blast radius bigger than planned, complexity budget crossed, an invariant would break (`managing-complexity-budgets`).
3. The next step is **irreversible or outward-facing** (push, publish, delete, send, spend) and wasn't explicitly authorized.
4. The task would write **outside its boundary** (another repo, global config).
5. A blocker needs a decision only the human can make: log it (`STATE`/checkpoint) and pause.

## While running

- **Evidence with every claim** — command and output.
- **Checkpoint per phase** (`handing-off-sessions`), so a crash resumes instead of restarts.
- **Small commits after green,** local verification before any push (CI minutes are finite).
- **Keep a running blocker/discovery log;** surprises are the most valuable output.
- **No lateral writes.** Cross-repo changes require human approval.

## Common mistakes

- Granting lights-out for work with no tests.
- Counting "different error message, same root cause" as progress.
- Treating an approval for one push as approval for the next.
- Long silent runs with no status surface.
