---
name: code-architecture-review
description: Use when conducting a comprehensive code and architecture review of any repository using graph-based structural analysis (Graphify/AST) and producing a detailed, actionable improvement plan.
---

# Code & Architecture Review Skill

An exhaustive, agent-optimized framework for analyzing software architecture, component cohesion, inter-module coupling, code quality, and engineering trade-offs across any codebase.

---

## Agent Detection & Mode Tuning

Detect the active runtime environment (Antigravity `agy`, Claude Code, Cursor, or POSIX CLI). See `references/AGENT_TUNING.md` for tool selection and output conventions.

---

## Workflow Overview

```mermaid
flowchart TD
    Start(["Start Review"]) --> Step1["Step 1: Graphify & Codebase Mapping"]
    Step1 --> PromptInstall{"Graphify Available?"}
    PromptInstall -- No --> AskUser["Ask User: Install Graphify or use Native AST Fallback?"]
    AskUser -- Install --> InstallGraphify["Run installation (pip / npm / gsd-tools)"] --> RunGraphify["Build Graph (.planning/graphs / graphify-out)"]
    AskUser -- Fallback --> NativeScan["Run Deep Native AST & Directory Walk"]
    PromptInstall -- Yes --> RunGraphify
    RunGraphify --> Step2["Step 2: Major Component & Boundary Mapping"]
    NativeScan --> Step2
    Step2 --> Step3["Step 3: Intra-Component Deep Dive (Within-Component)"]
    Step3 --> Step4["Step 4: Inter-Component Interaction & Dependency Review"]
    Step4 --> Step5["Step 5: Architectural Pattern & Quality Evaluation"]
    Step5 --> Step6["Step 6: Generate & Save Improvement Plan in Repo"]
    Step6 --> Step7["Step 7: Security Review Recommendations & Next Actions"]
    Step7 --> End(["Complete Review"])
```

---

## Step 1: Codebase Mapping & Graphify Gate

Knowledge graphs and structural call graphs capture topological dependencies and blast radius.

### 1.1 Check for Graphify / Tooling
Run `scripts/check_graphify.sh` or check CLI availability:
```bash
command -v graphify >/dev/null 2>&1 || command -v gsd-tools >/dev/null 2>&1
```

### 1.2 User Interaction Gate
If graphify is not installed, ask the user before installing:
- **Option 1 (Install):** `uv tool install graphify-cli` or `npx -y @opengsd/gsd-core@latest --local`. Run `graphify update .`.
- **Option 2 (Native Fallback):** Map repository layout, entry points, module boundaries, package manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`), and import hierarchies via file tools and `rg`.

---

## Step 2: Major Component & Domain Mapping

Identify and catalog top-level building blocks:
1. **System Entry Points:** HTTP/REST/GraphQL APIs, CLI entrypoints, background workers, event consumers.
2. **Domain & Business Core:** Services, domain models, rule validators, state machines.
3. **Data Access & Storage:** ORM schemas, query builders, repository abstractions, caching layers.
4. **External Integrations:** Third-party SDKs, cloud provider clients, message queues, file storage.
5. **Cross-Cutting Concerns:** Auth, telemetry/logging, error middleware, config management.

Render a Mermaid component diagram showing the top-level topology.

---

## Step 3: Intra-Component Deep Dive (Within-Component Review)

Evaluate individual modules in isolation against design principles (see `references/ARCHITECTURE_PATTERNS.md`):
1. **Cohesion & SRP:** Single reason to change; flag God objects, mega-functions (>100 lines), grab-bag utils.
2. **Type Safety & Contracts:** Strict types vs. `any`/`dict`; validate boundary inputs (Zod, Pydantic).
3. **Error Handling:** Caught and re-thrown with context; never swallow silently (`catch (e) {}`).
4. **State & Concurrency:** No mutable global state; thread-safe concurrency.
5. **Testability & Determinism:** Testable without live network/database; inject dependencies.

---

## Step 4: Inter-Component & Cross-Module Review

Analyze module boundaries and dependencies:
1. **Coupling Direction:** Inward toward domain logic; detect circular dependencies (`A -> B -> A`).
2. **Interface Abstraction:** Callers depend on interfaces; no leaky storage entities in API/UI layers.
3. **Data Flow & Communication:** Synchronous vs. asynchronous; check for N+1 queries.
4. **Shared State & Side Effects:** Clear resource ownership and lifecycle management.

---

## Step 5: Architectural Pattern & Quality Evaluation

Benchmark against architectural dimensions (details in `references/ARCHITECTURE_PATTERNS.md`):
- **Layering & Boundaries:** Presentation, application, domain, persistence separation.
- **Extensibility (OCP):** Open for extension, closed for modification (no sprawling switch-cases).
- **Scalability & Performance:** Asymptotic complexity, batching, caching, query indexing.
- **Maintainability Index:** Cognitive complexity, DRY adherence, consistent naming.

---

## Step 6: Generate & Save Improvement Plan in Repo

Always write the comprehensive review and actionable roadmap into the repository.

### Default Destination Paths
- **Primary**: `docs/ARCHITECTURE_REVIEW.md` (or `ARCHITECTURE_REVIEW.md` at root if `docs/` is absent)
- **GSD/Planning Projects**: `.planning/reviews/ARCHITECTURE_REVIEW_PLAN.md`

### Required Structure of the Improvement Plan

Fill in `templates/IMPROVEMENT_PLAN_TEMPLATE.md` with the following 5 sections:
1. **Code Architecture:** High-level paradigm, Mermaid current system diagram, target state blueprint, architectural debt.
2. **Code Module & Component Review:** Module scorecard, intra-module findings (hotspots, SRP smells, type/error handling).
3. **Code Inter-Module Review:** Relationship graph, coupling/cohesion analysis, dependency circularity, boundary encapsulation.
4. **Recommended Improvements (Prioritized Roadmap):** P0 critical fixes, P1 refactoring, P2 polish, P3 future-proofing, with concrete Before/After examples.
5. **Security & Robustness Recommendations:** Attack surface, secrets handling, dependency risks, next-step scans (`/security-scan`).

---

## Step 7: Security Review Suggestion & Next Action Guidance

Conclude every review with actionable next steps:
1. Offer to execute **Phase P0 / P1** refactoring immediately (see `refactor-execute`).
2. Suggest running a dedicated security scan (`/security-scan` or `dependency-audit`).
3. Offer to decompose the improvement plan into actionable implementation tasks (`/plan`).

For agent-specific flags, artifact generation, and slash command integration, see `references/AGENT_TUNING.md`.

---

## Review Anti-Patterns to Avoid

1. **Do NOT produce superficial style critiques**: Focus on structure, architecture, design patterns, separation of concerns, and system durability—not just formatting or lint trivialities.
2. **Do NOT skip the user confirmation for tooling**: Always ask before running network/package installations (`pip`, `npm`).
3. **Do NOT leave the plan purely theoretical**: Provide concrete code snippets illustrating the recommended pattern transitions (e.g. converting a switch-statement monolith into a strategy or factory pattern).
4. **Do NOT overwrite existing architecture documents without checking**: Save to `docs/ARCHITECTURE_REVIEW.md` or a new versioned file if one already exists.
