# Evidence: where each skill came from

Skills were distilled from the standards, specs, audits, changelogs, fix-commit histories, and QA reports of 20 repositories (grouped below by domain). Incidents are generalized in the skills; this file records the source so claims can be re-checked. Repository names are the local project names.

## Source repositories

| Domain | Repos | What they contributed |
|---|---|---|
| Autonomous AI | `factory_instructions`, `central_skills`, `seed-brain-gh`, `ai-model-learning`, `eval`, `product-owner`, `agent-manager-fe` | constitution of tenets/standards (spec-first, evidence-before-assertion, complexity budgets, determinism, portability, changelog sync); a self-improving agent loop with guardrails and measured token/timeout failures; a multi-agent audit skill; a grounded PRD pipeline; a driver-pattern terminal manager |
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
| `writing-intent-briefs` | `product-owner` (`[UNKNOWN]`/`[DECISION NEEDED]`, zero fabrication, Socratic refine); factory intent/go-ahead standard |
| `planning-with-contracts` | factory standard 01; `ai-model-learning` plans (global constraints, measured motivation, TDD tasks); `flowscope` numbered spec folders |
| `sizing-limits-from-measurement` | `ai-model-learning` REASONING_AND_TOKENS + GUARDRAILS (12k tokens all reasoning; 131k same failure at ~450 s; server context fixed at 32k) |
| `choosing-tools-and-substrates` | factory standards 34 and 49 (polyglot substrates, `uv`); `synth` stdlib-only tooling contract; `oscal-xdr` stack rationale |
| `designing-layered-pipelines` | `OntoLogic` and `feed-brain-gh` architecture; `airflow` thin DAGs; `agent-manager-fe` duplicate protocol types fixed by re-export; lattice tiering (factory standard 19) |
| `designing-plugin-contracts` | `agent-manager-fe` ADRs (driver contract, discovery/reattach, mock/live socket); `uitoolbox` ChartPlugin contract |
| `designing-testable-seams` | `ai-model-learning` constructor-injection rule, typed exceptions, best-effort side paths, narrowed except fix |
| `evolving-schemas-and-contracts` | `oscal-xdr` PITFALLS; `ai-model-learning` optional `lesson` field, `TokenUsage` invariant |
| `defending-architecture-decisions` | factory standard 35 (dual-axis defense); `agent-manager-fe` ADR format |
| `managing-complexity-budgets` | factory standards 31/36/38/39 (budget table, dual-gate introspection) |
| `designing-data-pipelines` | `airflow` fix history (Neo4j connection leak, data-dir env var, `oscal_airflow` rename, diverse top-10) and `oscal-xdr` pitfalls |
| `building-unattended-agent-loops` | `ai-model-learning` guardrails, progress-detection plan (284k-token trial), sandbox constraints |
| `grounding-ai-outputs` | `oscal-xdr` (no LLM in audit path); `product-owner` grounding; `synth` blinded export and canaries |
| `scaffolding-new-projects` | `clif2OntoLogic` bootstrap (upstream repos cloned into ignored `input/`, plan saved in-repo); recurring empty-dir and unrun-quickstart issues |
| `building-small-cli-tools` | `greener-noise` (CLI+GUI parity, validation), `floppy-music` (DSL, `--list`), `OntoLogic` (clean exit codes) |
| `building-code-generators` | `OntoLogic` fixes (topological class sort, OWL well-formedness, Cypher escaping, MERGE parent, per-class Java files); factory PTIA standard |
| `parsing-untrusted-text-robustly` | `gemini-chat-exporter` (selector cascade, nested-list duplication, table pipes); factory anchor-parser fence immunity; Mermaid label fix; `uitoolbox` date bugs |
| `hardening-trust-boundaries` | `OntoLogic` shell-injection and Cypher-escape fixes; `ai-model-learning` Dockerfile allowlist and "speed bump, not a sandbox"; `synth` sanitizer secondary-injection fixes; extension SECURITY doc |
| `engineering-for-determinism` | factory standard 39; `synth` regeneration/SHA pins; `airflow` seeded generators and Python-version seed-type bug |
| `layered-verification-gates` | factory standards 03/04; `airflow` skip behavior; `agent-manager-fe` coverage report; constraint-weakening patterns |
| `hunting-silent-failures` | `uitoolbox` QA review (four P0 silent bugs) |
| `debugging-across-layers` | `ai-model-learning` hidden context ceiling; `airflow` shadowing and checkpoint with missing data; port-conflict fix |
| `clustering-failures-by-root-cause` | `flowscope` improvement plan 003; `synth` no-degradation ratchets |
| `building-trustworthy-benchmarks` | `synth` audit plan and governance docs; `eval` benchmark-audit prompts and statistical guide |
| `making-verifiable-claims` | `eval` Toulmin claims and statistics guides; factory standard 41 |
| `orchestrating-subagents` | `synth` model-selection guidance; factory multi-tier verification; `eval` four-agent partitioning; a two-agent incident in this repo where a second agent staged files in a shared checkout and they were swept into the other agent's amend |
| `running-multi-lens-audits` | `eval` benchmark-audit skill; `synth` 51-issue audit |
| `supervising-autonomous-sessions` | factory variable-gear autonomy, halt-after-3-retries, boundary isolation, evidence rule |
| `handing-off-sessions` | `airflow` Phase 4.1 checkpoint; `ai-model-learning` full-system rebuild spec; factory incidental-tooling and journaling standards; `uitoolbox` REBUILD |
| `compacting-context-safely` | `ai-model-learning` measured token failures; `airflow` checkpoint notes; recurring loss of user corrections and repeated dead ends after context compaction |
| `writing-agent-context-files` | `airflow` CLAUDE.md (commands/architecture/pitfalls), `synth` and `flowscope` context files, `.cursorrules`/`AGENTS.md`/`GEMINI.md` in the same repos |
| `keeping-docs-in-sync` | factory standards 44/45; `flowscope` doc-sync checklist; `synth` coherence invariant and stale counts |
| `keeping-repos-portable` | factory standard 22; `seed-brain-gh` relative-path fixes; `agent-manager-fe` port fix; `synth` bash 3.2 compatibility |
| `drafting-issue-reports` | `running-multi-lens-audits` issue-file format (51 audit findings filed as problem + proposed fix); user request for a reviewable, unfiled issue script with labels, summary, description, relevance and suggested fix |
| `writing-pull-requests` | `committing-and-releasing-cleanly` PR-description rule; GitHub closing-keyword docs (one keyword per issue); `gh pr create --help` (2.88: `--dry-run` may still push); ~400-line default from the SmartBear/Cisco code-review study (defect-finding falls off beyond 200–400 lines per review) |
| `committing-and-releasing-cleanly` | factory standard 03; `flowscope` dual-remote sync; existing release skills |

## Provenance notes

- The factory standards are strongly opinionated and partly project-specific (lattice tiers, DarkOS tooling). Only the transferable core was kept: the numeric budgets, dual-gate idea, evidence rule, and portability lint.
- A few third-party skill libraries were present in the source ecosystem (general process skills). They were used only to avoid duplication; no text was copied.
- Numbers quoted inside skills (e.g. 62 → 5 causes, 51 issues, 284k tokens) come from the source repos' own docs and are examples, not universal thresholds.
