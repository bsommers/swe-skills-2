---
name: designing-data-pipelines
description: Use when building ETL, scheduled DAG workflows, knowledge-graph or database loads, simulated data generation, or report pipelines; when reruns duplicate data, history gets overwritten, or queries time out.
---

# Designing Data Pipelines

## Overview

Numbered stages, thin orchestrators, file/record hand-offs, **idempotent loads**, immutable raw history. Design so a rerun for any date or subset gives the same result and never duplicates.

## Rules

1. **Stages are numbered and single-purpose** (collect → validate → normalize → enrich → load → analyze → report). Orchestrator files are wrappers over importable packages.
2. **Hand off files with schemas** under a configurable data dir. Honor the same env var (`DATA_DIR`) in *every* path — a hardcoded path in one stage is the classic bug.
3. **Idempotent load.** Use upsert/MERGE keyed on natural keys with uniqueness constraints. Rerunning must not duplicate. When linking, MERGE the parent node before the child relationship.
4. **Batch writes** (`UNWIND`/bulk insert) in micro-batches; put a queue between bursty producers and a serialized writer to avoid lock contention/timeouts.
5. **Immutable raw, replayable projection.** Keep raw payloads append-only; keep state changes as events when history matters; the graph/tables are rebuildable.
6. **Parameterized queries only.** Bound traversal depth (`*1..3`); never run unbounded cartesian aggregates on request paths.
7. **Precompute aggregates** asynchronously and cache; dashboards read the cache.
8. **Resource lifecycles.** Open connections in context managers; a driver created per call and never closed leaks until the DB refuses.
9. **Simulation is seeded** per entity so any site/record is reproducible (`engineering-for-determinism`).
10. **Don't shadow dependencies.** A local package named like a third-party one (`airflow`) breaks imports; name it distinctly.
11. **Reports must be honest about sampling.** Dedupe rows (one per entity in a "top 10"), drop unnamed categories, state n.
12. **Say what's tracked vs generated.** A committed data snapshot of 10 while generators define 100 confuses everyone; document it.

## Testing

- Load DAG modules by path when filenames aren't importable (numeric prefixes).
- Tests needing the DB or scheduler skip **loudly** with the reason; also provide a containerized run that covers them.
- Add an end-to-end script that runs every stage on a tiny dataset.

## Pitfalls → prevention

| Pitfall | Prevention |
|---|---|
| Write-lock contention under bursts | queue + micro-batch |
| Vendor schema rigidity | canonical schema + adapters (`evolving-schemas-and-contracts`) |
| Traversal explosion | depth limits, indexes, uniqueness constraints |
| Lost temporal history | raw append-only + event ledger |
| Wrong data dir in one stage | single settings module, env-driven |
