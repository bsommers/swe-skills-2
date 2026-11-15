---
name: planning-grade-a-uplift
description: Use when asked what it would take to make a project grade A or A+ for its goals, to find gaps between a repository and its stated goals, or to propose additional milestones that would help those goals.
---

# Planning Grade-A Uplift

## Overview

"A+" is meaningless until it is defined against the project's own goals. Define it as a rubric of **measurable criteria**, grade each dimension with evidence, then turn every gap into a work item with a verify command.

## Procedure

1. **State the goals** in one to five sentences from the README, purpose doc and roadmap. If they conflict or are absent, that is the first finding.
2. **Pick dimensions** that serve those goals. Defaults: goal fit, correctness, test depth, docs accuracy, portability, security, release and operations, maintainability, contributor experience. Drop what doesn't apply.
3. **Define A+ per dimension** as an observable condition, e.g. "gate runs in under 60 s with zero skips on Linux and macOS", not "good tests". Use `references/rubric.md` for the grade scale.
4. **Grade with evidence.** Each grade cites a command output, file, or measurement. No evidence means grade `?`, not a guess.
5. **List gaps** as work items:
   ```
   | id | gap | dimension | acceptance | verify command | effort S/M/L | depends on |
   ```
6. **Group into milestones** by dependency and value: M0 safety and correctness, M1 verification and docs truth, M2 portability and contributor experience, M3 growth. Each milestone has exit criteria a script can check.
7. **Propose extra milestones** the goals deserve but nobody asked for (`references/rubric.md` has a prompt list). Mark them `proposed`, and say which goal each serves.
8. **Order by risk reduced per effort**, and name what to stop doing.

## Rules

- Every work item has acceptance and a verify command; if you can't write one, the item is a question, not a task.
- Separate `fix`, `guard` (prevent recurrence) and `grow` (new capability) items.
- Don't inflate: a project can be an honest B+ and still meet its goals. State which grade the goals actually need.
- Cost the plan: effort per milestone and the one item to do first.

## Common mistakes

- Generic checklists unconnected to the goals.
- Grades without evidence.
- A plan that only adds work and never removes or merges anything.
- Milestones with no exit criteria.
