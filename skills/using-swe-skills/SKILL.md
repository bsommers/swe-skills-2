---
name: using-swe-skills
description: Use when starting any software task — building a tool, feature or system, planning or architecting, debugging, reviewing, or shipping — to decide which swe-skills apply and how much process the task deserves.
---

# Using swe-skills

Load **one to three** skills that match the task, never all of them. Process skills (brainstorming, TDD, debugging, review) set the *how*; these skills add domain judgment. The `eng` skill (`/eng <task>`) is a typed shortcut into this router.

## 1. Size the task

| Scale | Signals | Process |
|---|---|---|
| **Tool** | one purpose, one user, ≤ a day | 3-line intent, stdlib, one happy + one failure test |
| **App** | several modules, state or UI, days | intent brief, tasks with verify commands, layers |
| **System** | many services/agents/repos, unattended | contracts, ADRs, budgets, audits, checkpoints |

Unsure? `right-sizing-process`.

## 2. Pick skills

| When you… | Load |
|---|---|
| get a fuzzy request | `writing-intent-briefs` |
| write a plan or spec | `planning-with-contracts` |
| specify IPC, daemon, or remote connection state machines | `planning-with-contracts` |
| prove a bugfix or regression with red test first | `designing-exhaustive-test-cases` |
| verify cross-platform compilation & #[cfg] coverage | `running-local-ci` |
| plan/build new functionality; pre-build test matrix | `designing-exhaustive-test-cases` |
| set a timeout, token cap, batch or pool size | `sizing-limits-from-measurement` |
| pick a language, library, runtime | `choosing-tools-and-substrates` |
| discover local tools, VM sandboxes (`cvm`, `win-devvm`), or analyzers in `~/src` | `using-local-tool-registry` |
| structure a multi-stage system | `designing-layered-pipelines` |
| support swappable backends/drivers | `designing-plugin-contracts` |
| expose a capability across UI, keys, CLI, API, MCP | `designing-uniform-surfaces` |
| call APIs, DBs, HTTP, clock, LLMs; testable seams | `designing-testable-seams` |
| define or change data shapes | `evolving-schemas-and-contracts` |
| make a costly-to-reverse decision | `defending-architecture-decisions` |
| grow a big file or function | `managing-complexity-budgets` |
| build ETL, DAGs, graph loads | `designing-data-pipelines` |
| build an unattended LLM/agent loop | `building-unattended-agent-loops` |
| feed LLM output into a decision | `grounding-ai-outputs` |
| integrate TypeSafe System One / Jev decision models | `typesafe-ai` |
| start a new repo | `scaffolding-new-projects` |
| write a CLI or script | `building-small-cli-tools` |
| build an installer, `init`, or next-step CLI guide | `building-installers-and-onboarding` |
| emit code/config from a model | `building-code-generators` |
| parse or scrape text/HTML | `parsing-untrusted-text-robustly` |
| touch shell, SQL, paths, secrets, sandboxes | `hardening-trust-boundaries` |
| write/review CI workflows, pin actions, dep gates | `hardening-ci-workflows` |
| run CI locally first and conserve hosted GitHub Actions minutes | `running-local-ci` |
| size or count from untrusted input; capped lists | `bounding-untrusted-resource-use` |
| signal a PID from a pid/lock file; daemon control | `controlling-processes-safely` |
| add a wait/poll handler to a request/serve loop | `keeping-event-loops-responsive` |
| handle auth, sessions, crypto, input, exploits | `security-best-practices` |
| see flaky or churning output | `engineering-for-determinism` |
| decouple business logic, set module boundaries | `architecture-best-practices` |
| configure reproducible dev envs or Nix flakes | `nix-environments` |
| decide what "done" means | `layered-verification-gates` |
| automate browser QA plan with recorded evidence | `driving-browsers-for-qa` |
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
| write/refresh user guides, README, arch, purpose | `writing-user-guides` |
| render SVG/PNG visual diagrams for docs/examples | `rendering-graphic-examples` |
| showcase graphics in docs with neon-grid theme | `showcasing-graphics-in-docs` |
| design project logo, banner, or SVG/PNG icons | `designing-logos-and-icons` |
| build/update a GitHub Pages site in `docs/` | `building-github-pages-sites` |
| change documented behavior | `keeping-docs-in-sync` |
| hardcode paths or env assumptions | `keeping-repos-portable` |
| audit architecture & code with Graphify/AST | `code-architecture-review` |
| review a PR, branch diff, or staged changes | `pr-review` |
| execute refactoring plan safely with green tests | `refactor-execute` |
| audit OpenAPI/GraphQL/DTO schema drift | `api-contract-audit` |
| audit packages for CVEs and licenses | `dependency-audit` |
| measure test coverage and close testing gaps | `test-coverage` |
| generate reviewable batch issue script | `github-issues-script` |
| forecast, track, budget tokens / USD spend | `token-finops` |
| select/switch models dynamically; save tokens | `adaptive-model-routing` |
| write up bugs or findings as issues | `drafting-issue-reports` |
| turn issues or a branch into a PR | `writing-pull-requests` |
| commit, push, tag, release | `committing-and-releasing-cleanly` |
| calculate SemVer, tag, and publish releases | `release` |
| build, package, upload release binaries | `building-release-binaries` |

## Rules

- Announce loaded skills and why in one line.
- **Bounded active set:** Keep at most 1–3 skills in context; every loaded skill replays tokens each turn.
- **Phase-transition eviction:** Between major phases (plan → build → ship), follow `compacting-context-safely` to checkpoint and resume with only active-phase skills.
- If a skill is not in `~/.claude/skills/`, read `skills/<skill-name>/SKILL.md` directly.
- Skip steps that cost more than the risk they remove at this scale.
- Default to **git and GitHub** (`gh` CLI) unless the project uses another host.
- User instructions and project context files override this library.
