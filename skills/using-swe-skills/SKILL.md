---
name: using-swe-skills
description: Use when starting any software task — building a tool, feature or system, planning or architecting, debugging, reviewing, or shipping — to decide which swe-skills apply and how much process the task deserves.
---

# Using swe-skills

Load the **one to three** skills that match the task, never all of them. When a process skill (brainstorming, TDD, debugging, code review) also applies, it sets the *how*; these skills add the domain judgment. The `eng` skill (`/eng <task>`) is a typed shortcut into this router.

## 1. Size the task

| Scale | Signals | Process |
|---|---|---|
| **Tool** | one purpose, one user, ≤ a day | 3-line intent, stdlib, one happy + one failure test |
| **App** | several modules, state or UI, days | intent brief, tasks with verify commands, layers |
| **System** | many services/agents/repos, unattended, others depend on it | contracts, ADRs, budgets, audits, checkpoints |

Unsure? `right-sizing-process`.

## 2. Pick skills

| When you… | Load |
|---|---|
| get a fuzzy request | `writing-intent-briefs` |
| write a plan or spec | `planning-with-contracts` |
| set a timeout, token cap, batch or pool size | `sizing-limits-from-measurement` |
| pick a language, library, runtime | `choosing-tools-and-substrates` |
| structure a multi-stage system | `designing-layered-pipelines` |
| support swappable backends/drivers | `designing-plugin-contracts` |
| call APIs, DBs, HTTP, clock, LLMs; testable seams | `designing-testable-seams` |
| define or change data shapes | `evolving-schemas-and-contracts` |
| make a costly-to-reverse decision | `defending-architecture-decisions` |
| grow a big file or function | `managing-complexity-budgets` |
| build ETL, DAGs, graph loads | `designing-data-pipelines` |
| build an unattended LLM/agent loop | `building-unattended-agent-loops` |
| feed LLM output into a decision | `grounding-ai-outputs` |
| start a new repo | `scaffolding-new-projects` |
| write a CLI or script | `building-small-cli-tools` |
| emit code/config from a model | `building-code-generators` |
| parse or scrape text/HTML | `parsing-untrusted-text-robustly` |
| touch shell, SQL, paths, secrets, sandboxes | `hardening-trust-boundaries` |
| see flaky or churning output | `engineering-for-determinism` |
| decide what "done" means | `layered-verification-gates` |
| suspect untested code hides bugs | `hunting-silent-failures` |
| hit a failure that ignores fixes | `debugging-across-layers` |
| face dozens of failures | `clustering-failures-by-root-cause` |
| build or trust a benchmark | `building-trustworthy-benchmarks` |
| report a number or status | `making-verifiable-claims` |
| delegate to subagents | `orchestrating-subagents` |
| audit in depth | `running-multi-lens-audits` |
| run unattended for hours | `supervising-autonomous-sessions` |
| pause, resume, hand off | `handing-off-sessions` |
| context filling up; compact or clear | `compacting-context-safely` |
| write CLAUDE.md/AGENTS.md/rules | `writing-agent-context-files` |
| author user guides in docs/ | `writing-user-guides` |
| change documented behavior | `keeping-docs-in-sync` |
| hardcode paths or env assumptions | `keeping-repos-portable` |
| audit architecture & code with Graphify/AST | `code-architecture-review` |
| review a PR, branch diff, or staged changes | `pr-review` |
| execute refactoring plan safely with green tests | `refactor-execute` |
| audit OpenAPI/GraphQL/DTO schema drift | `api-contract-audit` |
| audit packages for CVE vulnerabilities and licenses | `dependency-audit` |
| measure test coverage and close testing gaps | `test-coverage` |
| generate reviewable batch issue creation script | `github-issues-script` |
| forecast, track, and budget tokens / USD spend | `token-finops` |
| write up bugs or findings as issues | `drafting-issue-reports` |
| turn issues or a branch into a PR | `writing-pull-requests` |
| commit, push, tag, release | `committing-and-releasing-cleanly` |
| calculate SemVer, tag, and publish releases | `release` |

## Rules

- Announce the skills you loaded, and why, in one line.
- If a step costs more than the risk it removes at this scale, say so and skip it.
- Default to **git and GitHub** (`gh` CLI) for version control, issues, and PRs, unless the project uses something else.
- User instructions and project context files override this library.
