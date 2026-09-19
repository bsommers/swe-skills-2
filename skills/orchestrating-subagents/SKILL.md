---
name: orchestrating-subagents
description: Use when delegating work to subagents or parallel agents, choosing which model tier to use for a task, structuring reviews by fresh-context agents, when subagent output is too verbose or conflicts with other agents' edits, or when more than one agent may commit to the same repository.
---

# Orchestrating Subagents

## Overview

Subagents buy parallelism and fresh context; they cost tokens and can conflict. Delegate **well-specified, independent, bounded** work; keep judgment and integration with yourself.

## When to delegate

| Delegate | Keep |
|---|---|
| Mechanical/templated edits, file surveys, test writing to a spec | architecture decisions, ambiguous trade-offs |
| Independent investigations with no shared files | integration and conflict resolution |
| Fresh-eyes review of a plan or diff | deciding what the findings mean |
| Parallel audits by different *lens* | final claims to the user |

## Rules

1. **Match model to task.** Cheap/fast tier for mechanical, well-specified, read-heavy work; strongest tier for architecture, ambiguity, or high-risk multi-step reasoning. Escalate on failure, not by default.
2. **Full task text, not a pointer.** Give: goal, exact files, interfaces, acceptance criteria, the verification command, and constraints. A subagent starts with nothing.
3. **Terse output contract.** Ask for: status, what changed (paths), verification result, blockers. No narration, no restating the prompt.
4. **Parallel only when independent.** Different files, no shared state, no ordering. Otherwise sequence them.
5. **One writer per file, one agent per checkout.** Assign file ownership; integrate diffs yourself. Agents that may commit in parallel each get their own `git worktree add ../<repo>-<task> -b <branch>` (or clone). A shared checkout means a shared index, so one agent's `commit` or `--amend` sweeps up files another agent staged. Merge the branches back yourself.
6. **Bound the slice.** One task, one component; flush context between tasks so stale assumptions don't leak.
7. **Review in two passes:** spec compliance first, then code quality.
8. **Layered verification:** executor self-check → independent reviewer (fresh context) → security/test auditor → second model (optional) → human. Reviewers get the *spec and diff*, not the executor's reasoning.
9. **Never delegate understanding.** Don't write "based on your findings, fix it"; state what to do.
10. **Respect boundaries.** A subagent working in one repo does not write to sibling repos without explicit human approval.
11. **Verify claimed results.** A subagent's "done" is a claim; check the diff and run the tests.

## Dispatch template

```
Task: <one sentence>
Context: <2–4 lines: why, where it fits>
Files: <paths to read / modify>
Contract: <signatures / schemas to honor>
Acceptance: <observable criteria>
Verify: <exact command + expected output>
Report: status · files changed · verify output · blockers (≤10 lines)
```

## Common mistakes

- Same expensive model for everything.
- Two agents editing one file.
- Two agents committing in one checkout, including an agent from another project told to "also add this here".
- Vague "improve X" tasks that produce sprawling diffs.
- Accepting "all tests pass" without seeing the output.
- Using subagent review as a rubber stamp by including the executor's justification.
