---
name: right-sizing-process
description: Use when unsure how much planning, testing, documentation, or review a task deserves, when a quick script is growing into a system, or when process feels heavier or lighter than the risk.
---

# Right-Sizing Process

## Overview

Process is a cost paid to remove risk. Match it to the scale and blast radius of the work, and **re-check as the work grows**. Most failures come from a Tool treated like a System (plan longer than the code) or a System treated like a Tool (surprises at integration).

## The ladder

| | Tool | App | System |
|---|---|---|---|
| Shape | one purpose, one file or few, one user | several modules, persistent state or UI | multiple services/agents/repos; others depend on it; may run unattended |
| Intent | 3 lines in chat | half-page brief, in/out of scope | brief + signed go-ahead + measurable success criteria |
| Plan | mental | task list, each with a verify command | written plan: contracts, task breakdown, threat model, verification plan |
| Decisions | none recorded | note non-obvious ones in README | ADRs for irreversible/cross-cutting choices, with rejected alternatives |
| Tests | 1 happy + 1 failure path | unit + functional (CLI/E2E) | + integration, security, determinism, budgets |
| Docs | usage block in README | README + architecture sketch | living docs synced per commit, changelog, handoff/checkpoint files |
| Review | self-check | self + one fresh-context review | layered: self → peer subagent → adversarial → human |

## Escalation triggers (move up one column)

- A second consumer appears (another script, team, agent).
- It will run unattended, on a schedule, or spend money/compute.
- It stores data someone would be upset to lose.
- It crosses a security boundary (network, shell, untrusted input, credentials).
- The change touches more than ~10 files or an irreversible action (migration, deletion, publish).
- You've reworked the same area twice.

## Signs you mis-sized

- **Over:** plan longer than the code; ADR for a reversible choice; docs for a throwaway script.
- **Under:** two+ rework loops; "works on my machine"; a bug that a 5-line test would have caught; nobody can say what "done" means.

## Keep the scraps

Throwaway tools (parsers, probes, repro harnesses) built while working are cheap now and valuable later. Commit them under `scripts/incidental/` or `tools/` with a header saying why they exist. See `handing-off-sessions`.

## Common mistakes

- Sizing once at the start and never again. Re-size at each escalation trigger.
- Using "it's just a tool" to skip the failure-path test. Tools still get run by someone else's data.
