---
name: sizing-limits-from-measurement
description: Use when choosing or debugging a timeout, token cap, context window, retry count, batch size, pool size, memory limit or budget, especially when a call fails at the same point no matter how high you raise the limit.
---

# Sizing Limits From Measurement

## Overview

Every limit is a hypothesis about the workload. **Measure the real workload, size from the worst case, make limits loud when hit, and know every layer that can cap you.** A limit set too low often fails *silently and cheaply* — zero output, zero cost, nothing to repair.

---

## Rules

1. **Measure before choosing.** Run the real (or a representative) workload; record peak and tail, not just mean.
2. **Size from the max plus headroom** when too-low fails silently. Use the mean only when too-low fails visibly.
3. **Scale coupled limits together.** A token cap and the timeout that bounds its generation move as a pair; raising one alone just moves the failure.
4. **Enumerate the layers.** Client setting → proxy → server config → runtime → OS/hardware. The *effective* limit is the minimum across all of them.
5. **Invariant failure = hidden ceiling.** If raising your knob 3× changes nothing (same failure, same elapsed time), the cap is below the layer you're tuning. Inspect the actual effective config there (e.g. the server's loaded context size), not your request.
6. **Make every limit configurable** with an env default, and record the chosen value and why next to it.
7. **Say what kind of limit it is.** Enforced *before* spending (hard cap) or accounted *after* (can overshoot by one call). Document which.
8. **Fail loud.** A limit hit must raise a typed error naming the limit and its value, never return empty output.
9. **Bound the outputs you feed back.** Truncate captured logs/tracebacks to the *last* N bytes (signal is at the end).
10. **Standardize on Million Tokens (MTok) for Token FinOps.** Always compute and report token costs in $/MTok:
    $$\text{Cost} = \left(\frac{\text{Input Tokens}}{1{,}000{,}000} \times \text{Input \$/MTok}\right) + \left(\frac{\text{Output Tokens}}{1{,}000{,}000} \times \text{Output \$/MTok}\right)$$

---

## Token FinOps & Frontier Model Rate Matrix ($ / MTok)

| Provider & Family | Model Tier | Input ($/MTok) | Output ($/MTok) | Workload Fit |
| :--- | :--- | :---: | :---: | :--- |
| **Google Gemini** | `gemini-3.7-flash` / `3.8-flash` | **$0.15** | **$0.60** | Fast scaffolding, tool calling, unit tests |
| **Google Gemini** | `gemini-3.8-pro` / `2.5-pro` | **$1.25** | **$5.00** | Deep thinking, architecture, complex refactors |
| **Anthropic Claude** | `claude-3-5-haiku` | **$0.80** | **$4.00** | Lightweight triage, classification, diff checks |
| **Anthropic Claude** | `claude-3-7-sonnet` / `sonnet-5` | **$3.00** | **$15.00** | Primary engineering, multi-file changes, specs |
| **Anthropic Claude** | `claude-3-opus` / `opus-5` | **$15.00** | **$75.00** | Critical safety, formal audits, highest reasoning |
| **OpenAI** | `o3-mini` | **$1.10** | **$4.40** | Focused algorithmic coding and math proofs |
| **OpenAI** | `gpt-4o` | **$2.50** | **$10.00** | General-purpose multimodal tasks |

---

## Symptom → suspect

| Symptom | Suspect |
|---|---|
| Empty/truncated output, `finish_reason=length` | completion cap consumed by hidden reasoning/preamble |
| Timeout with zero tokens produced | timeout shorter than time-to-first-token for this size |
| Same failure & elapsed time across raised caps | server-side context/window fixed below your request |
| Works small, fails at scale | batch/pool/memory sized to the demo |
| Retries succeed randomly | limit near the workload's tail; flakiness = limit too tight |
| Budget "reset" after restart | budget held in memory; persist it (and reset on a calendar boundary deliberately) |
| Forecast 10× higher than single run | multi-stage pipeline estimate applied to single-stage run; scope ledger to active slice |

---

## Example

A reasoning model burned all 12k completion tokens deriving a formula and emitted no code. At 32k it finished. On a harder task, 49k and 131k failed identically at ~450 s — the server had a fixed 32k context window that the request could not override. The fix was the server's config, not a bigger client number.

---

## Common mistakes

- Picking a round number ("60s seems fine") and never measuring.
- Raising a client limit repeatedly without checking what the server is actually running with.
- Sizing from average completions, then failing on the biggest task.
- Budgets checked only after the fact with no note that overshoot is possible.
- Comparing a single-stage task spend against a whole-pipeline multi-agent forecast.
