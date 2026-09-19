---
name: planning-with-contracts
description: Use when writing an implementation plan or spec for a multi-file change, before touching code on anything that spans several modules, or when a plan is being executed by an agent with no prior context.
---

# Planning With Contracts

## Overview

A plan is a contract between intent and code. Write **interfaces and constraints first**, then tasks that each end green. A plan should let a zero-context agent execute without asking what "done" means.

## Plan skeleton

1. **Goal** — 2–3 sentences: the deliverable, not the activity.
2. **Motivation (measured)** — numbers or observed failures that justify the work ("trial 2 spent 284k tokens and still failed"). No number → say so.
3. **Current → proposed architecture** — a small diagram; only what changes.
4. **Contracts** — exact types/signatures/schemas each task produces or consumes. Write these before tasks; they are the seams.
5. **Global constraints** — invariants the whole change must preserve: "batch and daemon modes stay byte-identical", "no new dependencies", "all N existing tests pass", "everything new is best-effort and must not take down a run".
6. **Tasks** — numbered, dependency-ordered. Each has: files touched, interface produced/consumed, **failing test first**, verify command, and ends committable.
7. **Threat & failure model** — what can go wrong (bad input, dependency down, half-written state) and the mitigation or accepted risk.
8. **Verification plan** — exact commands and the expected output/count.

## Task template

```markdown
### Task 3: <verb phrase>
**Files:** modify `a.py`, test `tests/test_a.py`
**Produces:** `NoProgressError(AgentFrameworkError)` with `.record`
- [ ] Write failing test (state the expected failure message)
- [ ] Implement minimal change
- [ ] Verify: `pytest tests/test_a.py -q` → all pass
```

## Review the plan before executing

Run an adversarial pass (yourself in fresh context, or a subagent): edge cases, races, backward compatibility, performance cliffs, dependency cycles. Fix the plan, not the code, at this stage. Check no task depends on a later one and no step says "handle appropriately".

## Larger features: spec folder

`spec.md` (what/why) · `plan.md` · `research.md` (options tried, decisions) · `data-model.md` · `contracts/` · `tasks.md` · `quickstart.md` (how to see it work) · `checklists/`. One folder per feature, numbered.

## Keep an as-built record

Original specs go stale the day code diverges. Keep the plan as history and maintain a separate as-built description when it matters (see `handing-off-sessions`).

## Common mistakes

- Tasks phrased as activities ("improve error handling") rather than outputs.
- Contracts invented mid-implementation, so tasks disagree on shapes.
- No global constraints, so a refactor quietly changes a public entry point.
- Verification says "run tests" without the command or expected count.
