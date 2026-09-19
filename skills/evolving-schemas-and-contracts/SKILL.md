---
name: evolving-schemas-and-contracts
description: Use when defining data shapes for APIs, events, files, or databases, ingesting third-party or vendor data, adding a field to stored records, or renaming/removing something other code depends on.
---

# Evolving Schemas and Contracts

## Overview

Validate at every boundary against a **canonical internal schema**; keep vendor-specific detail in property maps; evolve additively so old data still loads. Treat the derived store as a **projection you can rebuild** from immutable raw history.

## Rules

1. **Validate at the edge.** Parse untrusted input with a schema library (Pydantic, Zod, JSON Schema) at the first line of ingest. Never write raw dynamic keys from unvalidated JSON into a database.
2. **Canonical model, adapters at the rim.** Map each vendor/format into one internal shape (`Finding`, `Observation`). Upstream format changes touch one adapter.
3. **Generic core, specific extras.** Keep stable labels/columns for the core; put vendor-specific fields in a properties map.
4. **Additive evolution.** New fields are optional with defaults (`lesson: str | None = None`) so every existing record deserializes. Removal and rename go through expand → migrate → contract.
5. **Invariants as validators.** Encode checkable truths in the schema (`reasoning + action == completion`), so violation fails at construction.
6. **Reject or quarantine unknowns.** Unrecognized input goes to a dead-letter location with the reason, not silently accepted or dropped.
7. **Parameterize, never concatenate,** values into queries (SQL, Cypher, shell). See `hardening-trust-boundaries`.
8. **Raw is immutable.** Store original payloads append-only; graph/tables are re-runnable projections. Overwriting with upsert loses history and point-in-time answers.
9. **Uniqueness constraints on natural keys** so idempotent loads stay idempotent.
10. **Version the contract** when a break is unavoidable; support N and N-1 during migration.

## Backward-compat check

Before merging a schema change, load a snapshot of *old* records through the *new* code and confirm success. Add that as a test.

## Common mistakes

- Vendor names baked into table/label names.
- Making a new field required, breaking every stored record.
- Free-form JSON blobs with no schema "for flexibility".
- Upserts that destroy the previous state you later need for audits.
- Renaming a column in one deploy.
