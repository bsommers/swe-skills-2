---
name: using-swe-skills
description: Use when starting any software task — building a tool, feature or system, planning or architecting, debugging, reviewing, or shipping — to decide which swe-skills apply and how much process the task deserves.
---

# Using swe-skills

## Overview

A library of engineering skills distilled from real projects: what broke, what was measured, what held up. Load **one to three** skills that match the task. Loading all of them wastes context and dilutes each.

These skills complement general process skills (brainstorming, TDD, systematic debugging, code review) if your agent has them. Where both apply, run the process skill for the *how*, and this library for the domain judgment.

## Step 1: Size the task

Load `right-sizing-process` if unsure. Rough ladder:

| Scale | Signals | Process |
|---|---|---|
| **Tool** | One purpose, one user, ≤ a day | Intent in 3 lines, stdlib, one happy + one failure test |
| **App** | Several modules, state or UI, days | Intent brief, task list with verify commands, layered structure |
| **System** | Multiple services/agents/repos, unattended, others depend on it | Written plan with contracts, ADRs, budgets, audits, checkpoints |

## Step 2: Map intent to skill

| You are about to… | Load |
|---|---|
| Start something fuzzy | `writing-intent-briefs` |
| Write a plan or spec | `planning-with-contracts` |
| Set a timeout, token cap, batch size, pool size | `sizing-limits-from-measurement` |
| Pick a language, library or runtime | `choosing-tools-and-substrates` |
| Structure a multi-stage system | `designing-layered-pipelines`, `designing-plugin-contracts` |
| Make code testable / handle errors | `designing-testable-seams` |
| Define data shapes or evolve a schema | `evolving-schemas-and-contracts` |
| Make a decision you can't cheaply undo | `defending-architecture-decisions` |
| Notice files or functions getting big | `managing-complexity-budgets` |
| Build ETL, DAGs, graph loads | `designing-data-pipelines` |
| Build an LLM/agent loop that runs unattended | `building-unattended-agent-loops`, `grounding-ai-outputs` |
| Write a CLI or script | `building-small-cli-tools` |
| Emit code/config from a model | `building-code-generators` |
| Parse or scrape text/HTML/markup | `parsing-untrusted-text-robustly` |
| Touch shell, SQL/Cypher, files, secrets, sandboxes | `hardening-trust-boundaries` |
| See flaky or non-reproducible results | `engineering-for-determinism` |
| Decide what "done" and "green" mean | `layered-verification-gates` |
| Suspect untested code hides bugs | `hunting-silent-failures` |
| Face a failure that ignores your fixes | `debugging-across-layers` |
| Face dozens of failures/false positives | `clustering-failures-by-root-cause` |
| Build or trust an eval / benchmark | `building-trustworthy-benchmarks` |
| Report a number, status, or comparison | `making-verifiable-claims` |
| Delegate to subagents | `orchestrating-subagents` |
| Audit a codebase in depth | `running-multi-lens-audits` |
| Run lights-out for long stretches | `supervising-autonomous-sessions` |
| Pause, resume, or transfer work | `handing-off-sessions` |
| Write CLAUDE.md / AGENTS.md / rules | `writing-agent-context-files` |
| Change behavior that docs describe | `keeping-docs-in-sync` |
| Script paths, envs, cross-machine use | `keeping-repos-portable` |
| Commit, push, tag, release | `committing-and-releasing-cleanly` |

## Rules of use

- Announce which skill you loaded and why, in one line.
- Skills are guidance, not ceremony. If a step costs more than the risk it removes at this scale, say so and skip it.
- User instructions and project context files override this library.
