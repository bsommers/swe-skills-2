# Evidence: where each skill came from

Skills were distilled from the standards, specs, audits, changelogs, fix-commit histories, and QA reports of 20 repositories (grouped below by domain). Incidents are generalized in the skills; this file records the source so claims can be re-checked. Repository names are the local project names.

## Source repositories

| Domain | Repos | What they contributed |
|---|---|---|
| Autonomous AI | `seed-brain-gh`, `ai-model-learning`, `eval`, `product-owner`, `agent-manager-fe` | constitution of tenets/standards (spec-first, evidence-before-assertion, complexity budgets, determinism, portability, changelog sync); a self-improving agent loop with guardrails and measured token/timeout failures; a multi-agent audit skill; a grounded PRD pipeline; a driver-pattern terminal manager |
| Cybersecurity | `synth`, `oscal-xdr`, `security-skills` | benchmark corpus with a 51-issue audit and remediation plan, governance (holdouts, canaries, CIs); a pitfalls doc for compliance knowledge graphs; security scan/evaluate/remediate skill design |
| Systems programming | `flowscope` | closed-taint-state engine; forensic false-positive elimination (62 FPs → 5 causes); doc-sync rules; spec-folder workflow |
| Ontologies & semantics | `OntoLogic`, `ontological-firewall`, `morphisms-bfo-ext-domains` | compiler with frontend → ModelIR → emitters; security hardening of emitters; replay playbook; semantic boundary validation |
| Infrastructure | `airflow` | 11-stage pipeline, package shadowing, connection leak, data-dir bug, checkpoint notes |
| Software engineering | `feed-brain-gh`, `uitoolbox`, `gemini-chat-exporter` | context-isolated ingestion pipeline; a plugin-contract UI library with a QA pass that found silent bugs; a browser extension with DOM-cascade scraping and hardening |
| Hardware / media | `floppy-music`, `greener-noise` | small CLI/GUI tools: a line-oriented song DSL, CLI+GUI parity, input validation |

## Skill → evidence

| Skill | Primary evidence |
|---|---|
| `using-swe-skills`, `right-sizing-process` | tiered standards across repos; contrast between one-file tools (`greener-noise`, `floppy-music`) and multi-repo systems |
| `eng` | no external source; a typed entry point added after a review of a sibling `/swe` router found the same routing table repeated in five places that had drifted apart. It keeps one source of truth (`using-swe-skills`) and lints its shortcut table |
| `release` | ported from the older standalone `swe-skills` suite's release skill (SemVer bump, changelog, annotated tag, confirm before push) |
| `writing-intent-briefs` | `product-owner` (`[UNKNOWN]`/`[DECISION NEEDED]`, zero fabrication, Socratic refine); intent-brief and go-ahead specification standards |
| `planning-with-contracts` | spec-driven development standards (spec-first contracts before implementation); `ai-model-learning` plans (global constraints, measured motivation, TDD tasks); `flowscope` numbered spec folders |
| `token-finops` | no external source; split out of `sizing-limits-from-measurement` to hold the per-model $/MTok rate table in one place instead of two, after the same table was found duplicated (and drifted from actual provider pricing) in both skills |
| `sizing-limits-from-measurement` | `ai-model-learning` REASONING_AND_TOKENS + GUARDRAILS (12k tokens all reasoning; 131k same failure at ~450 s; server context fixed at 32k) |
| `choosing-tools-and-substrates` | polyglot substrate standards (modern toolchains, Astral `uv` primacy); `synth` stdlib-only tooling contract; `oscal-xdr` stack rationale |
| `designing-layered-pipelines` | `OntoLogic` and `feed-brain-gh` architecture; `airflow` thin DAGs; `agent-manager-fe` duplicate protocol types fixed by re-export; layered architectural tiering |
| `designing-plugin-contracts` | `agent-manager-fe` ADRs (driver contract, discovery/reattach, mock/live socket); `uitoolbox` ChartPlugin contract |
| `designing-testable-seams` | `ai-model-learning` constructor-injection rule, typed exceptions, best-effort side paths, narrowed except fix |
| `evolving-schemas-and-contracts` | `oscal-xdr` PITFALLS; `ai-model-learning` optional `lesson` field, `TokenUsage` invariant |
| `defending-architecture-decisions` | dual-axis architectural decision defense standard; `agent-manager-fe` ADR format |
| `code-architecture-review` | `feed-brain-gh` AST and graph mapping; `uitoolbox` modular architecture review; Graphify structural knowledge graph workflow |
| `api-contract-audit` | `oscal-xdr` schema drift audit; `agent-manager-fe` DTO / API protocol synchronization; OpenAPI and Protobuf contract checks |
| `refactor-execute` | `flowscope` spec-driven refactor execution; Fowler refactoring catalogs with green-test gating and rollback protection |
| `managing-complexity-budgets` | engineering complexity budget standards (250 LOC per-file budget, dual-gate static analysis) |
| `designing-data-pipelines` | `airflow` fix history (Neo4j connection leak, data-dir env var, `oscal_airflow` rename, diverse top-10) and `oscal-xdr` pitfalls |
| `building-unattended-agent-loops` | `ai-model-learning` guardrails, progress-detection plan (284k-token trial), sandbox constraints |
| `grounding-ai-outputs` | `oscal-xdr` (no LLM in audit path); `product-owner` grounding; `synth` blinded export and canaries |
| `scaffolding-new-projects` | `clif2OntoLogic` bootstrap (upstream repos cloned into ignored `input/`, plan saved in-repo); recurring empty-dir and unrun-quickstart issues |
| `building-small-cli-tools` | `greener-noise` (CLI+GUI parity, validation), `floppy-music` (DSL, `--list`), `OntoLogic` (clean exit codes) |
| `building-code-generators` | `OntoLogic` fixes (topological class sort, OWL well-formedness, Cypher escaping, MERGE parent, per-class Java files); prototypical template isolation standard (isolated template files, zero script-embedded heredocs) |
| `parsing-untrusted-text-robustly` | `gemini-chat-exporter` (selector cascade, nested-list duplication, table pipes); anchor-parser fence immunity; Mermaid label fix; `uitoolbox` date bugs |
| `hardening-trust-boundaries` | `OntoLogic` shell-injection and Cypher-escape fixes; `ai-model-learning` Dockerfile allowlist and "speed bump, not a sandbox"; `synth` sanitizer secondary-injection fixes; extension SECURITY doc |
| `engineering-for-determinism` | deterministic generation standards (SHA pinning, seeded generators); `synth` regeneration/SHA pins; `airflow` seeded generators and Python-version seed-type bug |
| `nix-environments` | `OntoLogic` and multi-substrate compiler toolchains; hermetic dev shells with `flake.nix` wrapping native toolchains while preserving unprivileged portability via `uv`/`cargo` fallback |
| `layered-verification-gates` | multi-tier verification standards; `airflow` skip behavior; `agent-manager-fe` coverage report; constraint-weakening patterns |
| `hunting-silent-failures` | `uitoolbox` QA review (four P0 silent bugs) |
| `debugging-across-layers` | `ai-model-learning` hidden context ceiling; `airflow` shadowing and checkpoint with missing data; port-conflict fix |
| `clustering-failures-by-root-cause` | `flowscope` improvement plan 003; `synth` no-degradation ratchets |
| `building-trustworthy-benchmarks` | `synth` audit plan and governance docs; `eval` benchmark-audit prompts and statistical guide |
| `making-verifiable-claims` | `eval` Toulmin claims and statistics guides; verifiable claims standard (evidence before assertion) |
| `test-coverage` | `floppy-music` and `greener-noise` bats test harness; `synth` multi-ecosystem coverage matrix; bats-core/kcov trap debugging and static reachability analysis |
| `dependency-audit` | `synth` and `security-skills` package CVE vulnerability scanning, CVSS scoring triage, and outdated dependency audits |
| `orchestrating-subagents` | `synth` model-selection guidance; multi-tier subagent verification protocols; `eval` four-agent partitioning; a two-agent incident in this repo where a second agent staged files in a shared checkout and they were swept into the other agent's amend |
| `running-multi-lens-audits` | `eval` benchmark-audit skill; `synth` 51-issue audit |
| `supervising-autonomous-sessions` | bounded autonomous operation rules (variable-gear autonomy, halt-after-3-retries, boundary isolation, evidence rule) |
| `handing-off-sessions` | `airflow` Phase 4.1 checkpoint; `ai-model-learning` full-system rebuild spec; session journaling and incidental tooling standards; `uitoolbox` REBUILD |
| `compacting-context-safely` | `ai-model-learning` measured token failures; `airflow` checkpoint notes; recurring loss of user corrections and repeated dead ends after context compaction |
| `writing-agent-context-files` | `airflow` CLAUDE.md (commands/architecture/pitfalls), `synth` and `flowscope` context files, `.cursorrules`/`AGENTS.md`/`GEMINI.md` in the same repos |
| `writing-user-guides` | `gemini-chat-exporter` and `uitoolbox` user documentation under `docs/`; `scaffolding-new-projects` docs layout; incidents of orphaned documentation subdirectories unreferenced from root READMEs, or missing root READMEs |
| `keeping-docs-in-sync` | living documentation and changelog synchronization standards; `flowscope` doc-sync checklist; `synth` coherence invariant and stale counts |
| `keeping-repos-portable` | repository portability standards (relative pathing, non-root fallbacks); `seed-brain-gh` relative-path fixes; `agent-manager-fe` port fix; `synth` bash 3.2 compatibility |
| `drafting-issue-reports` | `running-multi-lens-audits` issue-file format (51 audit findings filed as problem + proposed fix); user request for a reviewable, unfiled issue script with labels, summary, description, relevance and suggested fix |
| `github-issues-script` | `running-multi-lens-audits` 51-finding issue filing; batch GitHub issue generation with coordinates, impact, and heredoc escaping |
| `writing-pull-requests` | `committing-and-releasing-cleanly` PR-description rule; GitHub closing-keyword docs (one keyword per issue); `gh pr create --help` (2.88: `--dry-run` may still push); ~400-line default from the SmartBear/Cisco code-review study (defect-finding falls off beyond 200–400 lines per review) |
| `pr-review` | `committing-and-releasing-cleanly` review standard; `feed-brain-gh` multi-lens PR review workflow with `gh pr review` |
| `committing-and-releasing-cleanly` | commit and release hygiene standards; `flowscope` dual-remote sync; existing release skills |
| `adaptive-model-routing` | multi-tier model router benchmarks and subagent dispatch; token conservation benchmarks across pro, flash, flash_lite tiers |

## Provenance notes

- The engineering standards cited above were distilled into their transferable, substrate-agnostic core: numeric complexity budgets, dual-gate static checks, evidence-before-assertion, and portability lints.
- A few third-party skill libraries were present in the source ecosystem (general process skills). They were used only to avoid duplication; no text was copied.
- Numbers quoted inside skills (e.g. 62 → 5 causes, 51 issues, 284k tokens) come from the source repos' own docs and are examples, not universal thresholds.
