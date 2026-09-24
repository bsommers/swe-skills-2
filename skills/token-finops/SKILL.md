---
name: token-finops
description: Use when forecasting, budgeting, tracking, and reporting LLM token consumption and dollar costs ($/MTok) across frontier models and autonomous agent workflows.
---

# Token FinOps

## Overview

Token FinOps provides end-to-end discipline for managing token spend, context depth, and dollar costs in autonomous coding agent workflows. Every agent turn consumes input and output tokens against a commercial rate card. 

**Core Tenet:** Standardize all financial forecasting, budgeting, telemetry, and reporting on **Million Tokens (MTok)** and **USD ($)** derived from explicit model rate cards.

---

## 1. Model Detection & Selection Protocol

Before estimating budgets or executing agent pipelines, determine the active model tier:

1. **Autonomous Detection**:
   - Inspect environment variables (e.g. `ANTHROPIC_MODEL`, `GEMINI_MODEL`, `OPENAI_MODEL`).
   - Read workspace agent rules (e.g. `.agents/rules/model_selection.md`, `CLAUDE.md`, `AGENTS.md`).
   - Check local project configuration (`.climah/rate_card.toml`, `settings.json`).
2. **Interactive Clarification / User Prompting**:
   - If the target model cannot be determined unambiguously, **prompt the user** to select or confirm the active model tier.
   - Example prompt:
     > "Which model tier will drive this task?
     > 1. Gemini 3.8 Flash ($0.15 / $0.60 per MTok) [Recommended for fast iteration]
     > 2. Gemini 3.8 Pro ($1.25 / $5.00 per MTok) [Recommended for deep reasoning]
     > 3. Claude Sonnet 5 ($3.00 / $15.00 per MTok)
     > 4. Claude Opus 5 ($5.00 / $25.00 per MTok)"
3. **Multi-Tier Agent Hierarchies**:
   - In hierarchical systems (e.g. `climah`, subagent swarms), resolve rates **per agent role** (e.g. Architect on Pro/Opus, Builder on Flash/Sonnet, Validator on Haiku/Flash).

---

## 2. Frontier Model Rate Matrix ($ / MTok)

All calculations must use input and output rates per Million Tokens (MTok):

$$\text{Cost (USD)} = \left(\frac{\text{Input Tokens}}{1{,}000{,}000} \times \text{Input Rate}\right) + \left(\frac{\text{Output Tokens}}{1{,}000{,}000} \times \text{Output Rate}\right)$$

| Provider / Family | Model Identifier | Input ($/MTok) | Output ($/MTok) | Context Window | Typical Workload Role |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Google Gemini** | `gemini-3.7-flash` / `gemini-3.8-flash` | **$0.15** | **$0.60** | 1,000,000 | Fast builds, tool execution, unit test generation |
| **Google Gemini** | `gemini-3.8-pro` | **$1.25** | **$5.00** | 2,000,000 | Complex planning, architecture design, formal evaluation |
| **Anthropic Claude** | `claude-sonnet-5` | **$3.00** | **$15.00** | 1,000,000 | Primary code generation, multi-file refactoring, specs |
| **Anthropic Claude** | `claude-opus-5` | **$5.00** | **$25.00** | 1,000,000 | High-stakes security audits, formal verification |
| **Anthropic Claude** | `claude-3-5-haiku` | **$0.80** | **$4.00** | 200,000 | Fast triage, classification, token counting |
| **OpenAI** | `o3-mini` | **$1.10** | **$4.40** | 200,000 | Algorithmic tasks, unit test synthesis |
| **OpenAI** | `gpt-4o` | **$2.50** | **$10.00** | 128,000 | General multimodal tasks, documentation |

---

## 3. The 4-Phase Budgeting & Monitoring Lifecycle

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│   Phase 1: Forecast     │ ──> │  Phase 1.5: Recalibrate │ ──> │   Phase 2: Live Monitor │
│ (Pre-run estimate Y0)   │     │ (Post-discovery delta)  │     │ (Running turn-by-turn)  │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
```

### Phase 1 — Initial Pre-Run Forecast ($Y_0$)
Before reading large file trees or writing code, generate an initial forecast table:
- **Baseline Overhead**: Harness prompt + tool schemas + project rules (~25,000 tokens / 0.025 MTok).
- **File Read Input**: Estimated files to read ($\text{lines} \times 5 \text{ tokens/line}$).
- **Thinking Budget**: Tiered by task complexity:
  - *Trivial*: 1k–2k tokens
  - *Simple*: 2k–4k tokens
  - *Moderate*: 4k–8k tokens
  - *Complex*: 8k–15k tokens
  - *Research/Spike*: 15k–30k+ tokens
- **Output Budget**: Anticipated diff / generated code lines ($\text{lines} \times 5 \text{ tokens/line}$) + conversational prose.

Output the allocated budget in both tokens and USD:
`Allocated budget (Y0): ~52,000 tokens (0.052 MTok | $0.0780 USD @ gemini-3.8-flash)`

### Phase 1.5 — Plan-Informed Recalibration ($Y_1$)
Immediately before issuing the first build or code modification action:
- Replace guessed line counts with exact counts from discovery.
- Sum task estimates from structured plans (e.g. `PLAN.md`, `SPEC.md`).
- Report the delta:
  `[RECALIBRATED BUDGET: Y0 → Y1 (0.052 MTok → 0.068 MTok | $0.0780 → $0.1020 USD, Δ+30%) | basis: 7 files discovered]`

### Phase 2 — Turn-by-Turn Telemetry & Warning Gates
Include a compact status line on every turn:
`[BUDGET STATS: Used: 0.021 MTok ($0.0315) / Alloc: 0.068 MTok ($0.1020) | Context: 18,400 tok | Status: ON-TRACK]`

- **Warning Threshold**: When spend crosses **70% of allocated budget ($Y_1$)**, flag status as `WARNING`.
- **Warning Action**: Pause execution, dump session checkpoint to scratchpad, and recommend compaction (`/compact`) or session reset.

---

## 4. Scoped Forecast Calibration (Sub-pipelines & Levels)

When executing a specific phase, stage, or level rather than a full pipeline:
- **Scope the Initial Ledger**: Do NOT benchmark a single sub-task against the entire multi-phase project budget. Scope the budget ledger to the active slice (e.g. `--level build`).
- **Dual Display**: Always present both the **Active Slice Forecast** (for local stage pacing) and the **Full Pipeline Forecast** (for macro governance).
- **Ignore Static Asset Bloat**: When scanning repository tokens for baseline discovery, filter out binary artifacts, test fixtures, and deep ontology assets.

---

## 5. Summary & Hand-off Reporting

When completing a task, always output a FinOps summary block:

```markdown
### 📊 Token FinOps Execution Summary
- **Model(s) Used**: `gemini-3.8-flash` (Builder) + `gemini-3.8-pro` (Architect)
- **Input Consumption**: 95,617 tokens (0.0956 MTok)
- **Output Generation**: 2,820 tokens (0.0028 MTok)
- **Total Spend**: $0.1336 USD (vs. Stage Forecast: $0.1556 USD, Variance: -14.1%)
- **Budget Health**: ✅ Completed under budget
```
