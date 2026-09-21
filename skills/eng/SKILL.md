---
name: eng
description: Use when the user types /eng, with or without a task, a skill name, or a shortcut word, to start a software task or load one swe-skills skill directly.
---

# /eng

A typed shortcut into the library. `using-swe-skills` owns routing; this skill only saves typing and adds the shortcut table below.

## Dispatch

Read the first word of the arguments.

1. **A skill name** (any skill in this library, e.g. `/eng hunting-silent-failures parser`): load that skill and treat the rest as the task.
2. **A shortcut** from the table: load the skill it names and treat the rest as the task.
3. **Anything else**, including free text: load `using-swe-skills` with all the arguments as the task. It sizes the task and picks one to three skills.
4. **No arguments, `help` or `list`**: load `using-swe-skills`, show its skill table, and ask what the user is working on.

Only the first word is matched, and only exactly. "review the auth module" runs the `review` shortcut on "the auth module"; "the review is late" is free text.

## Shortcuts

| Word | Skill |
|---|---|
| `review` | `running-multi-lens-audits` |
| `coverage` | `hunting-silent-failures` |
| `commit` | `committing-and-releasing-cleanly` |
| `pr` | `writing-pull-requests` |
| `issues` | `drafting-issue-reports` |
| `plan` | `planning-with-contracts` |
| `debug` | `debugging-across-layers` |
| `size` | `right-sizing-process` |
| `handoff` | `handing-off-sessions` |
| `compact` | `compacting-context-safely` |

## Rules

- A shortcut never waives the target skill's confirmations. `/eng commit` still asks before any push or tag.
- Say which skill loaded and why, in one line.
- Do not restate or extend the router's table here. Add new routes to `using-swe-skills`; add a shortcut only for a word people will type.
