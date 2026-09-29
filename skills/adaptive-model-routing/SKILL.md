---
name: adaptive-model-routing
description: Use when selecting or switching models dynamically during a session to conserve tokens, choosing model tiers for subtasks, configuring lifecycle hooks for model gating, or dispatching subagents with matched reasoning density.
---

# Adaptive Model Routing

Dynamically route tasks to the most cost-effective model tier during execution. Use premium reasoning models only for high-density architectural or verification decisions; delegate high-volume execution to faster, lower-cost tiers to conserve tokens.

## Model Tier Matrix

| Tier | Antigravity Target | Claude / OSS Target | Typical Workloads | Cost & Throughput |
|---|---|---|---|---|
| **Lite** | `flash_lite` | Haiku / 8B | Read surveys, grep filtering, boilerplate generation, formatting, lint fixes | Lowest (~10x savings) |
| **Standard** | `flash` (Standard) | Sonnet / Medium | Modular CRUD implementation, boilerplate scaffolding, schema edits, doc updates | Balanced baseline |
| **Fast Reasoning** | `flash` (High Thinking) | Sonnet (Extended) | Algorithmic logic, parser/regex synthesis, TDD unit test cycles, AST refactors | High throughput, test-time compute |
| **Deep Reasoning** | `pro` (High Thinking) | Opus / R1 | System architecture, spec contracts, subtle security audits, multi-file diff review | Premium parametric scale |

Pair with `token-finops` for budget forecasting and `orchestrating-subagents` for subagent process boundaries.

## Test-Time Compute vs. Parametric Capacity

Coding model capability divides into two complementary scaling axes:

1. **Test-Time Compute (`flash` + High Thinking):** Extended reasoning tokens explore branch logic, simulate execution paths, and self-correct before emitting output. Optimal when problem space is algorithmic or bounded and has clear external verification (compiler errors, failing tests, linters). Outperforms or matches larger models on execution throughput at 5–10x lower cost.
2. **Parametric Capacity (`pro`):** Massive pre-trained parameter scale and world knowledge. Essential for unstated requirements, cross-module contract design (ADRs/RFCs), high-stakes security boundaries, or massive multi-file context windows (>200k tokens) where smaller models suffer context dilution.

## Complexity & Density Signals

Evaluate the incoming task before emitting code or spawning subagents:

```
Task Density = (File Impact Radius) × (Logical Ambiguity) × (Safety Criticality)
```

### Route to Lite / Standard (`flash_lite` / `flash`)
- **Deterministic transforms:** Writing standard CRUD endpoints, mechanical migrations, or repetitive boilerplate.
- **Localized edits:** Modifying 1–2 files where interfaces are already fixed by a contract.
- **Informational scans:** Finding usages, listing directory contents, inspecting logs.
- **Remediation loops:** Fixing syntax errors or formatting warnings where compiler/linter errors provide exact coordinates.

### Route to Fast Reasoning (`flash` + High Thinking)
- **Algorithmic implementation:** Complex data structures, parsers, state machines, and mathematical transformations.
- **TDD red-green cycles:** Generating unit tests, edge-case harnesses, and writing code to pass test assertions.
- **Bounded refactoring:** AST transforms and localized optimization where tests immediately verify behavioral invariance.

### Route to Deep Reasoning (`pro`)
- **Cross-module architecture:** Redesigning subsystem boundaries, public API contracts, or core state managers.
- **Ambiguous root-cause debugging:** Failures spanning multiple asynchronous layers, race conditions, or network boundaries.
- **Diff verification & adversarial review:** Auditing pull requests for concurrency hazards, memory leaks, or behavioral regressions.
- **Security-sensitive code:** Auth pipelines, token verification, cryptographic operations, sandboxing boundaries.

## Dynamic Session Strategies

### 1. Dynamic Subagent Delegation (Primary)

Keep the main orchestrator session on a balanced or fast model (`flash`). Delegate heavy reasoning or high-volume execution out-of-band:

```json
{
  "TypeName": "research",
  "Role": "Architecture Reviewer",
  "Model": "pro",
  "Prompt": "Audit src/services/auth.ts and src/middleware/session.ts for race conditions under concurrent token refreshes. Report exact findings in <=10 lines."
}
```

For large code emission runs, dispatch a worker subagent with `Model: "flash"` or `Model: "flash_lite"` to isolate token churn from the primary conversation window.

### 2. Automated Lifecycle Hooks (`PreToolUse`)

Use a lifecycle hook to intercept `invoke_subagent` calls. When high-complexity keywords (`architect`, `optimize`, `audit`, `security`) or high-risk file paths (`auth`, `crypto`, `kernel`) are detected in the subagent prompt or target files, the hook automatically overwrites the `Model` parameter to `pro`:

```json
{
  "decision": "allow",
  "overwrite": {
    "Model": "pro"
  }
}
```

If the task is routine, the hook preserves the lighter tier, preventing accidental token burn.

### 3. OpenGSD / Spec-Driven Development Phase Mapping

In phased workflows, enforce model tiering by lifecycle phase:

| Phase | Recommended Tier | Rationale |
|---|---|---|
| **Phase 1: Research & Spec** | `pro` (High Thinking) | Parametric capacity catches breaking structural flaws before coding. |
| **Phase 2: Atomic Planning** | `pro` (High Thinking) | Evaluates cross-module dependency graphs and contract invariants. |
| **Phase 3: Execution & TDD** | `flash` (High Thinking) | Test-time compute: rapid, verification-guided code and unit test synthesis. |
| **Phase 4: Diff Verification** | `pro` (High Thinking) | Senior reviewer pass: catches edge cases, regressions, and security gaps. |

## Common Mistakes

- **Defaulting to premium everywhere:** Running full-session `pro` or `opus` for mechanical refactors and TDD loops, inflating token burn 5–10x.
- **Underutilizing test-time compute:** Using standard flash without thinking for complex algorithms or unit tests when flash with high thinking solves it faster and cheaper than pro.
- **Using lite models for architectural planning:** Producing brittle plans with hidden circular dependencies, causing costly rework during execution.
- **Unbounded subagent contexts:** Re-injecting large conversational histories into subagents rather than isolated task briefs.
- **Manual mid-session toggling:** Forgetting to switch models back down after completing a high-reasoning review step.
