---
name: clustering-failures-by-root-cause
description: Use when facing many failing tests, false positives, review findings, or bug reports at once, or when improving a metric like precision or recall without regressing another.
---

# Clustering Failures by Root Cause

## Overview

Dozens of failures usually come from a handful of mechanisms. **Group by cause, fix the biggest cause at its layer, and lock the gain with a ratchet.** Don't fix instances one at a time.

## Procedure

1. **Collect** every failing case with enough context to see *why* (input, rule/test, output).
2. **Cluster by mechanism,** not by symptom or file. Write a table: cause, count, example, layer.
3. **Rank** by `count × (1 / fix cost)`; note dependencies between fixes.
4. **Fix the mechanism** at the right layer (scope rule, dedupe at emit, split overlapping rules, add a missing guard shape), not each instance.
5. **Ratchet.** Commit baseline metrics; add a test that fails if any metric gets worse (e.g. precision ≥ 0.85, flow fidelity = 100%, per-language recall). "No degradation" is enforced, not hoped for.
6. **Re-cluster after each fix** — clusters merge and new ones surface. Record before/after numbers.

## Forensic table (example: 62 false positives → 5 causes)

| Cause | ≈Count | Layer | Fix |
|---|---|---|---|
| Private helper parameters treated as untrusted roots | 21 | analysis scope | treat only public entrypoints as sources |
| Same physical sink reported per caller | 20 | reporting | dedupe by `(rule, file, sink line)`; merge traces |
| Two rules matching the same call | 15 | rules | split by read vs write semantics |
| Over-broad return-value sink | 5 | rules | require context |
| Unhandled guard shape | 3 | engine | add chained-comparison / suffix-check support |

## Ratchet sketch

```python
BASELINE = json.load(open("metrics.baseline.json"))
def test_no_regression():
    now = evaluate()
    for k, floor in BASELINE.items():
        assert now[k] >= floor - 1e-9, f"{k} regressed: {now[k]} < {floor}"
```
Update the baseline only in a commit that explains the improvement.

## Also works for

Review findings (many nits → few patterns), flaky test triage, lint-error floods, incident retrospectives.

## Common mistakes

- Fixing the loudest instance first and never seeing the pattern.
- Improving precision by silently killing recall (no ratchet on the other axis).
- Counting alerts instead of distinct physical findings.
- Changing the metric definition to look better.
