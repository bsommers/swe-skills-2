---
name: defending-architecture-decisions
description: Use when making an architectural or technology decision that is costly to reverse, choosing between competing designs, writing an ADR or RFC, or noticing that one option seems so obvious that alternatives were never listed.
---

# Defending Architecture Decisions

## Overview

Decide, then **attack your own decision** on two axes before committing: will it run rock-solid, and would a hostile critic accept it? Each defense either produces an invariant/negative test or changes the decision. Record it briefly as an ADR.

## When to write one

Irreversible or expensive-to-reverse; crosses module/team boundaries; picks a technology; sets a data model; or surprises a reasonable reader. **Skip** for reversible, local choices.

## ADR template (5–15 lines of body)

```markdown
# ADR-007: Session drivers behind one contract
**Status:** Accepted | Superseded by ADR-012 · **Date:** 2026-09-19
## Context      what forces the choice (constraints, numbers)
## Decision     what we chose, in one paragraph
## Consequences pros / cons / what gets harder
## Defense
### Stability   failure modes (dependency down, disk full, crash mid-write, race);
                the invariant preventing an invalid state; rollback/recovery path
### Critic      strongest objection; alternatives considered and *why rejected*;
                acknowledged costs; what evidence would make us revisit
## Enforced by  the test/lint/assertion that guards the invariant
```

## Procedure

1. List 2–3 real alternatives (including "do nothing"). One-line reason each was rejected.
2. **Stability pass:** for each dependency, ask "what if it's slow, absent, wrong, or duplicated?" Ask what happens on crash between step k and k+1.
3. **Critic pass:** write the harshest good-faith objection, then answer it or change the decision.
4. Convert each surviving defense into a check: a test, a schema constraint, a lint, or an assertion.
5. Save as `docs/adr/NNN-title.md`. ADRs are **append-only**: supersede, don't rewrite.

## Novel ideas

When you spot an optimization or better approach mid-task that is out of scope, write it as a proposed ADR/note and surface it to the human rather than silently building it.

## Common mistakes

- Justification that only lists benefits.
- "Alternatives considered: none."
- A defense with no resulting test — it will rot into folklore.
- Rewriting history in old ADRs so they match what happened.
- ADRs for trivia, which trains everyone to ignore them.
