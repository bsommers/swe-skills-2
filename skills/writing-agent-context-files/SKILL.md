---
name: writing-agent-context-files
description: Use when creating or updating CLAUDE.md, AGENTS.md, GEMINI.md, .cursor/rules, or other instruction files that AI coding agents read; when agents keep repeating a mistake in a repo; or when supporting several agent tools in one repository.
---

# Writing Agent Context Files

## Overview

A context file is the briefing a cold agent reads at the start of every session. It should let them run the tests, find where a change belongs, and avoid the known traps — in about 30 seconds. **Put in what can't be derived from the code; keep it short and true.**

## Contents, in order

1. **What this is** — 2–3 sentences, plus in/out of scope.
2. **Commands** — exact, copy-pastable: install, run, test (all / one file / one test), lint, build. Mark which need services.
3. **Architecture map** — 8–15 lines: layers, key modules, data flow, where new code goes.
4. **Invariants & contracts** — rules that must not break ("gold files are generated, never edited"; "tools are stdlib-only").
5. **Pitfalls & quirks** — the things that already bit someone: shadowed package, tests that skip without a service, generated-vs-tracked data, numeric-prefixed modules.
6. **Style** — only conventions a linter can't enforce.
7. **Verification before commit** — the gate commands.
8. **Living vs historical docs** — which files to trust.

## Leave out

Anything derivable by reading code · tutorials · aspirational rules nobody follows · absolute paths · secrets · long histories · duplicated docs.

## Multiple agent tools, one truth

| File | Read by | Approach |
|---|---|---|
| `AGENTS.md` | many agents (Antigravity, Codex, Cursor, others) | **canonical** |
| `CLAUDE.md` | Claude Code | short: `See AGENTS.md`, plus Claude-only notes |
| `GEMINI.md` | Gemini/Antigravity | pointer to `AGENTS.md` |
| `.cursor/rules/*.mdc` | Cursor | thin `alwaysApply` rule pointing at `AGENTS.md`; workflows live in skills |

Generate or symlink the pointers so they cannot drift. Keep each file under ~200 lines.

## Keep it alive

- When an agent trips on something twice, add a line under Pitfalls.
- When a command or count changes, update the file in the same commit (`keeping-docs-in-sync`).
- Test it: hand it to a fresh agent and ask it to run the tests and locate where feature X would go.

## Subagent and output guidance (if wanted)

State desired verbosity explicitly and once: e.g. "subagents reply with status, changed paths, verify output, blockers — no narration."

## Common mistakes

- A 600-line file the agent skims and misses the one crucial rule.
- Rules phrased as wishes ("try to keep functions small") rather than checks.
- Three divergent copies for three tools.
- Listing commands that no longer work.
