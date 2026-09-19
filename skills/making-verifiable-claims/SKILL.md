---
name: making-verifiable-claims
description: Use when reporting status, results, performance, security posture or comparisons ("done", "faster", "secure", "passes"), writing release notes or docs with numbers, or reviewing someone else's claims.
---

# Making Verifiable Claims

## Overview

A claim without evidence is an opinion; a claim without boundaries is usually false. Structure every non-trivial claim the way a skeptical reviewer would test it, and prefer *"not measured"* over a confident guess.

## The claim, structurally (Toulmin)

| Part | Question | Example |
|---|---|---|
| **Claim** | what exactly am I asserting? | "v2 cuts p95 latency 40%" |
| **Grounds** | what data supports it? | "n=30 runs, table 2, commit abc123" |
| **Warrant** | why does the data imply the claim? | "same hardware, same input, paired runs" |
| **Qualifier** | under what conditions? | "4-core node, warm cache, corpus v3" |
| **Rebuttal** | when does it *not* hold? | "single-threaded loads, cold start" |

## Report template

> **X** = *value* (k/n, 95% CI a–b) on *corpus/version* at *commit*, measured with *command*. Not tested: *…*.

## Rules

1. **Status claims need logs.** "Tests pass" = paste the command and summary line. "Fixed" = show the failing case now passing.
2. **Numbers carry n and uncertainty.** Counts as k/n; intervals for rates; effect size, not just p-value.
3. **Significance is checked, not asserted.** p ≥ 0.05 → don't write "significantly". Small effect size → say so.
4. **Compare fairly.** Same inputs, same machine, warm-up handled, baseline included, several runs. Series with coefficient of variation > 5% are noisy; say so.
5. **Distinguish measured, inferred, and assumed.** Label each.
6. **State the boundaries** (hardware, versions, data) and what you did *not* test.
7. **Retract cleanly.** If a claim is wrong, fix it where it was published (README, changelog) and say what changed.
8. **Derive, don't type, counts** in docs (test totals, capability counts) or date-stamp them (`keeping-docs-in-sync`).
9. **Humility.** No "robust", "secure", "production-ready" without the test or scan that supports the word.

## Quick check before sending

- Could a reader reproduce this number from what I wrote?
- Is there a stronger claim than the evidence supports? Dial it back.
- Did I say what would falsify it?

## Common mistakes

- Best-run vs baseline-average comparisons.
- Precision quoted without recall (or vice versa).
- "Grade A" with no scan output attached.
- Claims that survive only because no one reran them.
