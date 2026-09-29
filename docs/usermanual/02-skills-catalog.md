# Chapter 2: Skills Catalog & Classification

[← Back to User Manual](README.md) · [← Previous: Getting Started](01-getting-started.md) · [Next: Hooks & Context Guards →](03-hooks-and-context-guards.md)

This chapter provides a structured breakdown of the **51 skills** in `swe-skills`, organized into seven functional domains.

---

## Skill Classification & Design Philosophy

Every skill adheres to strict authoring principles:
- **Discovery-Only Frontmatter:** Descriptions start with `"Use when..."` and state triggers only, never repeating implementation workflows.
- **Strict Word Budgets:** Main body target ≤ 500 words to conserve LLM context. Heavy reference tables live in modular subdirectories.
- **Cross-Referenced Network:** Skills link directly to adjacent skills via `` `skill-name` `` notation.
- **Grounded Provenance:** Real incident origins documented in [`docs/EVIDENCE.md`](../EVIDENCE.md).

---

## 1. Entry & Routing

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`using-swe-skills`](../../skills/using-swe-skills/SKILL.md) | Starting any software task — building a tool, feature or system, planning or architecting, debugging, reviewing, or shipping — to decide which swe-skills apply and how much process the task deserves. | Task classification (Tool, App, System) and minimal 1–3 skill dispatch. |
| [`eng`](../../skills/eng/SKILL.md) | The user types `/eng`, with or without a task, a skill name, or a shortcut word, to start a software task or load one swe-skills skill directly. | Unified slash-command entry point with fast keyword shortcuts. |

---

## 2. Frame & Plan

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`right-sizing-process`](../../skills/right-sizing-process/SKILL.md) | Unsure how much planning, testing, documentation, or review a task deserves, when a quick script is growing into a system, or when process feels heavier or lighter than the risk. | Process tier matrix matching risk to overhead. |
| [`writing-intent-briefs`](../../skills/writing-intent-briefs/SKILL.md) | A request is vague, when requirements come from meeting notes or a rough idea, before planning or coding starts, or when you are tempted to fill in details the user never stated. | 1-page intent brief defining core problems and non-goals. |
| [`planning-with-contracts`](../../skills/planning-with-contracts/SKILL.md) | Writing an implementation plan or spec for a multi-file change, before touching code on anything that spans several modules, or when a plan is being executed by an agent with no prior context. | Interface contracts, module boundaries, and atomic task sequence. |
| [`sizing-limits-from-measurement`](../../skills/sizing-limits-from-measurement/SKILL.md) | Choosing or debugging a timeout, token cap, context window, retry count, batch size, pool size, memory limit or budget, especially when a call fails at the same point no matter how high you raise the limit. | Measured empirical baselines rather than guessed limits. |
| [`token-finops`](../../skills/token-finops/SKILL.md) | Forecasting, budgeting, tracking, and reporting LLM token consumption and dollar costs ($/MTok) across frontier models and autonomous agent workflows. | Cost modeling matrix across frontier and open-weight models. |
| [`choosing-tools-and-substrates`](../../skills/choosing-tools-and-substrates/SKILL.md) | Picking a language, framework, database, library, or runtime for a new component, when adding a dependency, or when a proposed stack seems chosen out of habit rather than fit. | Objective trade-off rubric against maintenance burden. |
| [`adaptive-model-routing`](../../skills/adaptive-model-routing/SKILL.md) | Selecting or switching models dynamically during a session to conserve tokens, choosing model tiers for subtasks, configuring lifecycle hooks for model gating, or dispatching subagents with matched reasoning density. | Dynamic routing rules matching task complexity to model tier (`pro`, `flash`, `flash_lite`). |

---

## 3. Architecture & Modeling

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`designing-layered-pipelines`](../../skills/designing-layered-pipelines/SKILL.md) | Structuring a system with several stages, inputs, or outputs (compilers, transpilers, ETL, ingest-analyze-report), when logic is leaking into thin wrappers, or when the same types are declared in more than one place. | Strict 3-tier pipeline (Source → Intermediate Representation → Emitter). |
| [`designing-plugin-contracts`](../../skills/designing-plugin-contracts/SKILL.md) | A host must work with several interchangeable implementations (drivers, adapters, renderers, backends, providers), when adding "just one more" implementation forces changes to the host, or when needing offline/mock modes that match live behavior. | Stable host SPI / API boundary with plugin capability detection. |
| [`designing-testable-seams`](../../skills/designing-testable-seams/SKILL.md) | Writing code that talks to databases, HTTP, the clock, containers, LLMs, or the filesystem; when tests need live services; or when error handling swallows failures with broad excepts. | Dependency injection seams for zero-IO testing. |
| [`evolving-schemas-and-contracts`](../../skills/evolving-schemas-and-contracts/SKILL.md) | Defining data shapes for APIs, events, files, or databases, ingesting third-party or vendor data, adding a field to stored records, or renaming/removing something other code depends on. | Backward/forward compatible schema evolution policies. |
| [`defending-architecture-decisions`](../../skills/defending-architecture-decisions/SKILL.md) | Making an architectural or technology decision that is costly to reverse, choosing between competing designs, writing an ADR or RFC, or noticing that one option seems so obvious that alternatives were never listed. | Lightweight ADR format analyzing irreversible trade-offs. |
| [`managing-complexity-budgets`](../../skills/managing-complexity-budgets/SKILL.md) | Files or functions are growing large, before adding a feature to an already big module, when an agent's edits keep breaking unrelated things, or when planning where new code should live. | File, line, and cognitive complexity caps with refactoring triggers. |
| [`designing-data-pipelines`](../../skills/designing-data-pipelines/SKILL.md) | Building ETL, scheduled DAG workflows, knowledge-graph or database loads, simulated data generation, or report pipelines; when reruns duplicate data, history gets overwritten, or queries time out. | Idempotent DAG pipelines with deterministic staging and loads. |
| [`code-architecture-review`](../../skills/code-architecture-review/SKILL.md) | Conducting a comprehensive code and architecture review of any repository using graph-based structural analysis (Graphify/AST) and producing a detailed, actionable improvement plan. | Multi-tier architectural assessment and remediation plan. |
| [`api-contract-audit`](../../skills/api-contract-audit/SKILL.md) | Auditing API contracts, OpenAPI/Swagger specifications, GraphQL schemas, Protobufs, and DTOs against backend route implementations to detect schema drift, undocumented endpoints, type mismatches, and breaking contract changes. | Schema-drift scorecard and contract validation matrix. |
| [`refactor-execute`](../../skills/refactor-execute/SKILL.md) | Safely executing architectural refactorings and code improvements step-by-step from an improvement plan or task list with green baseline tests, atomic commits, behavioral invariance, and incremental verification. | Verified behavioral invariance throughout multi-step refactoring. |

---

## 4. AI Systems & Unattended Loops

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`building-unattended-agent-loops`](../../skills/building-unattended-agent-loops/SKILL.md) | Building an LLM or agent system that generates and runs code, retries on failure, or runs for hours or days without supervision, including self-healing loops, daemons, batch runners, and sandboxes. | Hard stop conditions, isolated execution sandboxes, and circuit breakers. |
| [`grounding-ai-outputs`](../../skills/grounding-ai-outputs/SKILL.md) | An LLM's output feeds a decision of record (compliance, audit, security mapping, requirements, status), when synthesizing specs from notes, or when a model might invent details the source never contained. | Verifiable claim extraction with direct source citations. |

---

## 5. Build & Code Generation

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`scaffolding-new-projects`](../../skills/scaffolding-new-projects/SKILL.md) | Starting a new repository or project directory, when asked to "scaffold", "bootstrap", or "set up" a repo layout (src/, docs/, tests/, input/, output/, README), or when a new project is about to receive its first code with no structure yet. | Standardized repo anatomy (`src/`, `docs/`, `tests/`, `scripts/`). |
| [`building-small-cli-tools`](../../skills/building-small-cli-tools/SKILL.md) | Writing a command-line tool, script, or small utility (converters, generators, exporters, helpers), or adding a GUI or file format on top of one, for reliable behavior and easy sharing. | UNIX-philosophy CLI with clean exit codes and pipeable stdout/stderr. |
| [`building-code-generators`](../../skills/building-code-generators/SKILL.md) | Writing emitters, transpilers, scaffolders, or any tool that outputs code, config, schemas, diagrams or queries from a model, especially when generated output must compile, parse, or load in a downstream system. | AST-validated, deterministic emitter architectures. |
| [`parsing-untrusted-text-robustly`](../../skills/parsing-untrusted-text-robustly/SKILL.md) | Parsing or scraping text, HTML/DOM, markdown, logs, or markup you do not control; when a scraper breaks after a site update; when a parser matches things inside code blocks; or when type-guessing gives wrong results. | Robust, defensive grammar parsing with fallback boundaries. |
| [`hardening-trust-boundaries`](../../skills/hardening-trust-boundaries/SKILL.md) | Code passes data into a shell, SQL/Cypher/query language, filesystem path, template, container build, extension permission, or secret store; when running model-written or third-party code; or before shipping anything that handles untrusted input. | Injection-proof parameterization and strict input sanitization. |
| [`engineering-for-determinism`](../../skills/engineering-for-determinism/SKILL.md) | Results differ between runs or machines, tests are flaky, generated files churn in diffs, simulated data must be reproducible, or ground-truth files risk being hand-edited and drifting from their generator. | Bit-for-bit reproducible runs (sorted keys, fixed seeds, UTC timestamps). |
| [`nix-environments`](../../skills/nix-environments/SKILL.md) | Configuring reproducible development environments, hermetic build toolchains, or system-level dependencies with Nix flakes or devShells, especially when a project requires native C libraries or cross-compiler tools alongside language package managers. | 3-tier environment hierarchy (Hermetic Nix → Native Toolchain → Container/CI fallback) with hybrid `flake.nix`. |

---

## 6. Verify, Measure & Quality

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`layered-verification-gates`](../../skills/layered-verification-gates/SKILL.md) | Deciding what "done" or "green" means, before committing, before a phase or release, when tests are skipped or unavailable, or when tempted to weaken a check to get past a gate. | 4-tier verification ladder (Syntax → Types/Lint → Unit/Invariance → End-to-End). |
| [`hunting-silent-failures`](../../skills/hunting-silent-failures/SKILL.md) | Reviewing code with low test coverage, after adding a permissive parser or adapter, when output looks plausible but subtly wrong or empty, or when asked to QA a test suite for real gaps rather than count coverage. | Fault injection and edge-case probing to uncover swallowed exceptions. |
| [`debugging-across-layers`](../../skills/debugging-across-layers/SKILL.md) | A failure persists no matter which setting you change, when behavior differs between environments, when imports or config resolve to the wrong thing, or after resuming work from a checkpoint where state may have changed. | Layer-by-layer diagnostic isolation (transport, config, kernel, runtime). |
| [`clustering-failures-by-root-cause`](../../skills/clustering-failures-by-root-cause/SKILL.md) | Facing many failing tests, false positives, review findings, or bug reports at once, or when improving a metric like precision or recall without regressing another. | Root-cause taxonomy grouping bulk issues into atomic fixes. |
| [`building-trustworthy-benchmarks`](../../skills/building-trustworthy-benchmarks/SKILL.md) | Building or trusting an evaluation suite, benchmark corpus, scorer, or leaderboard; when comparing tools or models; when a score looks too good; or when ground truth labels might be wrong. | Contamination-resistant evaluation sets and scoring harnesses. |
| [`making-verifiable-claims`](../../skills/making-verifiable-claims/SKILL.md) | Reporting status, results, performance, security posture or comparisons ("done", "faster", "secure", "passes"), writing release notes or docs with numbers, or reviewing someone else's claims. | Concrete evidence commands backing every engineering claim. |
| [`test-coverage`](../../skills/test-coverage/SKILL.md) | Auditing a repository's test suite to measure real coverage across languages, identify untested critical paths, evaluate shell test quality, or produce a prioritized gap-closing plan. | Comprehensive coverage audit and high-risk path test strategy. |
| [`dependency-audit`](../../skills/dependency-audit/SKILL.md) | Auditing third-party package dependencies across JS/TS, Python, Rust, Go, Java, and Ruby for known security vulnerabilities (CVEs), outdated packages, license compliance risks, and supply chain threats. | Security and license compliance scorecard with automated audit scripts. |

---

## 7. Collaborate, Sustain & Operations

| Skill | Trigger ("Use when...") | Primary Deliverable |
|---|---|---|
| [`orchestrating-subagents`](../../skills/orchestrating-subagents/SKILL.md) | Delegating work to subagents or parallel agents, choosing which model tier to use for a task, structuring reviews by fresh-context agents, when subagent output is too verbose or conflicts with other agents' edits, or when more than one agent may commit to the same repository. | Isolated worktree allocation and clean multi-agent merge verification. |
| [`running-multi-lens-audits`](../../skills/running-multi-lens-audits/SKILL.md) | Auditing a codebase, test suite, benchmark, or plan in depth before a release, after a big milestone, or when a single reviewer keeps missing whole classes of problems. | Parallel audit lenses (Security, Architecture, Performance, QA). |
| [`supervising-autonomous-sessions`](../../skills/supervising-autonomous-sessions/SKILL.md) | Letting an AI coding session run for long stretches with little supervision, deciding how much autonomy to grant, when a session keeps retrying without progress, or when an agent might touch things outside its task. | Guardrails for unattended execution, stopping rules, and rollback boundaries. |
| [`handing-off-sessions`](../../skills/handing-off-sessions/SKILL.md) | Pausing or ending a work session, resuming after a break or context reset, transferring work to another agent or person, or preserving what was learned, including scratch tools and as-built specifications. | High-fidelity checkpoint artifacts capturing decisions, dead ends, and next command. |
| [`compacting-context-safely`](../../skills/compacting-context-safely/SKILL.md) | An agent's context window is filling up, auto-compaction is near, responses are slowing or forgetting earlier decisions, the task is switching to unrelated work, or before running /compact, /clear, or starting a fresh session mid-task. | Lossless checkpointing before context reset with post-reset verification. |
| [`writing-agent-context-files`](../../skills/writing-agent-context-files/SKILL.md) | Creating or updating CLAUDE.md, AGENTS.md, GEMINI.md, .cursor/rules, or other instruction files that AI coding agents read; when agents keep repeating a mistake in a repo; or when supporting several agent tools in one repository. | Terse, actionable agent instructions tailored per harness. |
| [`writing-user-guides`](../../skills/writing-user-guides/SKILL.md) | Authoring, structuring, or updating user guide documentation for a repository, CLI, library, or service; when documentation belongs in a dedicated subdirectory of docs/; or when connecting a quickstart README to a detailed user guide. | Modular multi-chapter user documentation in `docs/`. |
| [`keeping-docs-in-sync`](../../skills/keeping-docs-in-sync/SKILL.md) | A change alters commands, flags, behavior, capabilities, counts, or architecture that documentation describes; before committing feature work; or when docs contain numbers or examples that may have drifted. | Same-commit documentation synchronization and link validation. |
| [`keeping-repos-portable`](../../skills/keeping-repos-portable/SKILL.md) | Writing scripts, configs, docs links or cross-repo references; when something works only on one machine or from one directory; when adding ports, paths or environment assumptions; or before sharing or containerizing a repo. | Zero hardcoded home paths, POSIX compliance, and directory invariance. |
| [`drafting-issue-reports`](../../skills/drafting-issue-reports/SKILL.md) | Asked to write up bugs, enhancements, or review or audit findings as GitHub issues, when turning a list of problems into a backlog, or when issues should be prepared for human review before anything is filed. | Structured GitHub issues with repro steps, expected behavior, and scope. |
| [`writing-pull-requests`](../../skills/writing-pull-requests/SKILL.md) | Turning one or more issues or a finished branch into a GitHub pull request, when deciding which issues belong in the same PR, when writing a PR title or description, or when a PR should be drafted for human review before it is opened. | Atomic PR briefs linking issues, summarizing changes, and citing verification evidence. |
| [`pr-review`](../../skills/pr-review/SKILL.md) | Reviewing pull requests and git branch diffs against architectural rules, breaking changes, test coverage, error handling, security boundaries, and edge cases to generate actionable line-by-line review comments. | Multi-axis code review comments with exact coordinate citations. |
| [`github-issues-script`](../../skills/github-issues-script/SKILL.md) | Converting a list of findings, review items, architectural gaps, or bug reports into a structured, reviewable batch script (using gh issue create) with exact file coordinates, impact analysis, and proper labels. | Executable shell batch scripts using GitHub CLI (`gh issue create`). |
| [`committing-and-releasing-cleanly`](../../skills/committing-and-releasing-cleanly/SKILL.md) | About to commit, push, tag a version, or cut a release; when a working tree mixes unrelated changes; or when unsure whether an action is safe to run without asking. | Verification-first commits, atomic staging, and explicit human confirmation before push. |
| [`release`](../../skills/release/SKILL.md) | Analyzing changes since last release, calculating SemVer tag bump, generating changelogs, creating annotated git tags, and publishing releases. | Automated semantic version bumps, tag creation, and changelog sync. |
