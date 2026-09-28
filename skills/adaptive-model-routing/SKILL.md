---
name: adaptive-model-routing
description: Use when selecting or switching models dynamically during a session to conserve tokens, choosing model tiers for subtasks, configuring lifecycle hooks for model gating, or dispatching subagents with matched reasoning density.
---

# Adaptive Model Routing

Dynamically route tasks to the most cost-effective model tier during execution. Use premium reasoning models only for high-density architectural or verification decisions; delegate high-volume execution to faster, lower-cost tiers to conserve tokens.

## Model Tier Matrix

| Tier | Antigravity Target | Claude / OSS Target | Typical Workloads | Token Cost Profile |
|---|---|---|---|---|
| **Lite** | `flash_lite` | Haiku / 8B | Read surveys, grep filtering, boilerplate generation, formatting, lint fixes | Lowest (~10x savings) |
| **Standard** | `flash` | Sonnet / Medium | Modular feature implementation, unit tests, schema edits, doc updates | Balanced baseline |
| **Deep Reasoning** | `pro` | Opus / High Thinking | Spec design, system architecture, security audits, multi-file refactors, edge-case diff review | Premium (~5-10x cost) |

Pair with `token-finops` for budget forecasting and `orchestrating-subagents` for subagent process boundaries.

## Complexity & Density Signals

Evaluate the incoming task before emitting code or spawning subagents:

```
Task Density = (File Impact Radius) × (Logical Ambiguity) × (Safety Criticality)
```

### Route to Lite / Standard (`flash_lite` / `flash`)
- **Deterministic transforms:** Writing standard CRUD endpoints, mechanical migrations, or repetitive test boilerplate.
- **Localized edits:** Modifying 1–2 files where interfaces are already fixed by a contract.
- **Informational scans:** Finding usages, listing directory contents, inspecting logs.
- **Remediation loops:** Fixing syntax errors or formatting warnings where compiler/linter errors provide exact coordinates.

### Route to Deep Reasoning (`pro`)
- **Cross-module architecture:** Redesigning subsystem boundaries, public API contracts, or core state managers.
- **Ambiguous root-cause debugging:** Failures spanning multiple asynchronous layers or network boundaries.
- **Diff verification & adversarial review:** Auditing complex pull requests for concurrency bugs, memory leaks, or regressions.
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
| **Phase 1: Research & Spec** | `pro` (High Thinking) | Catches breaking structural flaws before code generation begins. |
| **Phase 2: Atomic Planning** | `pro` (High Thinking) | Slices implementation into bounded, verifiable execution steps. |
| **Phase 3: Execution** | `flash` / `flash_lite` | Deterministic muscle work: follows locked plans without wasting reasoning budget. |
| **Phase 4: Verification & Diff Review** | `pro` (High Thinking) | Senior reviewer pass: catches edge cases, regressions, and type drifts. |

## Common Mistakes

- **Defaulting to premium everywhere:** Running full-session `pro` or `opus` for mechanical refactors, inflating token burn 5–10x.
- **Using lite models for architectural planning:** Producing brittle plans with hidden circular dependencies, causing costly rework during execution.
- **Unbounded subagent contexts:** Re-injecting large conversational histories into subagents rather than isolated task briefs.
- **Manual mid-session toggling:** Forgetting to switch models back down after completing a high-reasoning review step.
