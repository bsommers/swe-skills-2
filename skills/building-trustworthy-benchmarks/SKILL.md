---
name: building-trustworthy-benchmarks
description: Use when building or trusting an evaluation suite, benchmark corpus, scorer, or leaderboard; when comparing tools or models; when a score looks too good; or when ground truth labels might be wrong.
---

# Building Trustworthy Benchmarks

## Overview

A benchmark is a measuring instrument; its errors become everyone's conclusions. Audit **three parts separately**: the ground truth, the evaluator, and the statistics. Assume any number is wrong until each part is verified.

## Ground truth

- **Generated, not hand-edited,** from markers in the samples; regenerate and diff (`engineering-for-determinism`).
- **Marker on the exact sink line;** test `marker_line + 1 == sink_line`.
- **Every sample compiles/parses** with its real toolchain. Broken samples make scanners "miss" for the wrong reason.
- **Negative twins** with structural parity to positives (e.g. > 70% similar) and *verified safe* — no secondary flaw in the "sanitizer".
- **Taxonomy audit:** don't conflate neighbors (path traversal vs upload, command vs argument injection); record accepted aliases explicitly.
- **Synthetic and safe:** placeholder secrets, reserved example domains.

## Evaluator

- **Normalize locations** (relative, absolute, `file://`, base-URI ids) before matching.
- **Optimal matching** (min-distance bipartite), never greedy first-fit; **small tolerance** (±1 line).
- **Right denominators:** count distinct samples/physical findings, not raw alerts; don't double-penalize exact vs alias rule ids.
- **Gameability test:** a shotgun tool that flags everything must NOT score full marks. Include true negatives.
- **Fuzz the evaluator** itself with edge inputs (hex offsets, missing fields, empty results).

## Statistics

- Report **k/n, point estimate, and a confidence interval** (Wilson / Clopper-Pearson).
- Compute `n` per stratum (language × category × shape). **Flag any claim with n ≤ 4.**
- Use **MCC / Youden's J** with imbalanced negatives; not F1 alone.
- Multi-trial agent runs: **unbiased pass@k** per finding; report variance and cost.
- Account for clustering (templated samples aren't independent); state effective n.

## Contamination and governance

- **Private holdout** (~20%) with a published SHA-256 commitment; rotate on a schedule.
- **Canary tokens** in private cases to detect memorization.
- **Blinded export** strips answer markers and giveaway comments but keeps line numbers.
- **Pre-register declared capabilities;** report full-corpus and declared-only results.
- **Reproducibility manifest** with versions, corpus hash, options, commit.

## Common mistakes

- Trusting a high score before running a naive baseline.
- Counting alerts as findings.
- Ground truth edited by hand "just this once".
- Publishing recall for a cell of 3 samples.
- Ignoring whether the LLM under test has seen the answer markers.

Multi-lens audit procedure: `running-multi-lens-audits`. Reporting: `making-verifiable-claims`.
