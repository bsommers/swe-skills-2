---
name: building-unattended-agent-loops
description: Use when building an LLM or agent system that generates and runs code, retries on failure, or runs for hours or days without supervision, including self-healing loops, daemons, batch runners, and sandboxes.
---

# Building Unattended Agent Loops

## Overview

An unbounded retry loop burns unlimited compute repeating the same failure. Unattended-safe means **bounded, observable, sandboxed, restart-safe, and honest about why it stopped.**

## Required properties

1. **Bounded everywhere.** Repair-attempt cap per task, token/cost budget per run, wall-clock timeout per execution, output size cap. These are load-bearing, not tunables to remove.
2. **Persisted budgets.** A daemon's daily budget lives on disk so a restart can't reset it; reset on a deliberate calendar boundary.
3. **No-progress detection that costs nothing.** Between attempts, compare code/error text deterministically (e.g. similarity ≥ 0.95). Stop early when a repair is essentially identical to the last. No extra LLM "judge" call on the already-expensive path. Keep the threshold high — a false stop wastes paid attempts.
4. **Distinct terminal states.** `succeeded`, `exhausted` (used every attempt), `no_progress` (stopped early), `infra_error` (model/DB down). Each has a different next action.
5. **Sandbox model-written code.** No network, all capabilities dropped, `no-new-privileges`, pid and memory limits, and a **host-enforced** timeout with force-kill — never trust the script to stop itself.
6. **Typed errors, no bare except.** One flaky call must not kill the process; a persistent failure must surface clearly.
7. **Heartbeat in the inner loop.** A busy daemon inside a long objective must not look stalled.
8. **Best-effort extras.** Distilling a lesson from a failure, scoring, telemetry: one extra call **on the failure path only**, never fatal, `None` on error.
9. **Feed learning forward.** Store a short `lesson` with each failed record; recall it into later prompts.
10. **Nothing important is silently discarded.** Commit or catalog every attempt's code and outcome.
11. **Deterministic fallback.** If the model or vector store is down, still produce a usable (if plain) result instead of crashing.
12. **Scaffolding verbs don't spend compute.** `bootstrap` writes files; `--submit` opts in to running trials.
13. **Kill switch and status.** A human can see what it's doing and stop it.

## Settings worth exposing (with rationale beside each)

`MAX_REPAIR_ATTEMPTS` · `NO_PROGRESS_THRESHOLD` · `EXEC_TIMEOUT` · `LLM_TIMEOUT` (scale with max tokens) · `SOFT_CONTEXT_CAP` (drop oldest recalled memory first; truncation not summarization, since summarizing spends the budget you're protecting) · `RUN_TOKEN_BUDGET` / `DAILY_TOKEN_BUDGET` · `OUTPUT_CAP_BYTES` (keep the *last* N) · `RETRY_ATTEMPTS`.

See `sizing-limits-from-measurement` for choosing values.

## Measured motivation (example)

One trial spent 284k tokens across repairs and still failed; another errored at 66k. Nothing distinguished "close" from "spinning". Non-convergence detection plus a distilled lesson fixed both without adding an LLM call to the success path.

## Common mistakes

- Post-hoc budget accounting described as a hard cap (overshoots by a call).
- Trusting a container's own timeout instead of the host's.
- Unlimited stack traces pasted into repair prompts (cap and keep the tail).
- Speaking of a Dockerfile allowlist as a sandbox. Label speed bumps as speed bumps.
