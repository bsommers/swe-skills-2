---
name: engineering-for-determinism
description: Use when results differ between runs or machines, tests are flaky, generated files churn in diffs, simulated data must be reproducible, or ground-truth files risk being hand-edited and drifting from their generator.
---

# Engineering for Determinism

## Overview

Given the same inputs, seeds, and toolchain, output should be **bit-for-bit identical**. Non-determinism turns every debugging session into archaeology and lets agents chase phantom regressions. Treat flakiness as a bug with a cause, not weather.

## Rules

1. **Seed every RNG, per entity.** Derive the seed from a stable id so each site/record is reproducible independent of generation order. Use a seed type the runtime accepts (an integer or string — newer interpreters reject some object types).
2. **Stable ordering.** Sort dict/set/file-listing iteration before emitting. Locale-independent sorts.
3. **No ambient time or randomness in outputs.** Inject a clock; omit timestamps from generated artifacts or put them in a separate manifest.
4. **Pin the toolchain.** Lockfiles, exact language/compiler versions, container image digests; hermetic builds that don't read ambient host state.
5. **Generated means generated.** Files produced by a generator (gold labels, schemas, bindings) are **never hand-edited**. Change the generator or its input, regenerate.
6. **Regeneration check.** A test that regenerates everything and asserts zero diff (bit-for-bit) across all corpora/artifacts.
7. **Hash pins for contracts.** When a test pins a file's SHA-256, updating it must be an intentional, reviewed change alongside the reason.
8. **Clean-clone test.** Run the suite in a fresh checkout/container so missing files, untracked outputs, and ambient env show up. Tests must pass with optional outputs absent.
9. **Run-twice-compare.** For any pipeline: run twice in different directories; diff outputs.
10. **Reproducibility manifest.** Record tool versions, corpus hash, options, and commit alongside results.

## Diagnose flakiness

| Cause | Tell | Fix |
|---|---|---|
| Unordered iteration | diff reorders lines | sort |
| Unseeded RNG / time | values differ per run | seed / inject |
| Shared temp or port | fails in parallel | unique temp dirs, ephemeral ports |
| Test order coupling | passes alone, fails in suite | isolate state |
| Ambient env | passes on your machine | hermetic env, clean clone |
| Hidden network | slow/failing offline | fake it |

## Common mistakes

- "Fixing" flaky tests with retries.
- Seeding once globally so adding one entity reshuffles all others.
- Updating a hash pin to make CI green without reading the diff.
- Committing generated output that isn't reproducible.
