---
name: grounding-ai-outputs
description: Use when an LLM's output feeds a decision of record (compliance, audit, security mapping, requirements, status), when synthesizing specs from notes, or when a model might invent details the source never contained.
---

# Grounding AI Outputs

## Overview

Generative models are excellent proposers and unreliable arbiters. **Keep deterministic logic in the decision path; let the model propose offline; require a human or a rule to accept.** And never let it fill gaps with plausible fiction.

## Rules

1. **Deterministic decisions in audit paths.** Mapping alerts to controls, scoring, and pass/fail come from a static, versioned table or rule engine — same input, same answer, traceable.
2. **LLM proposals are drafts.** Model-suggested mappings/classifications enter a candidate file, get human validation, then join the registry.
3. **Zero fabrication.** If a detail wasn't stated or cannot be deduced (protocol, SLA, data volume, tech), write `[UNKNOWN: …]` or `[DECISION NEEDED: …]`. Those markers become the next interview.
4. **Cite the ground.** Claims about code cite `file:line`; claims about behavior cite a command and its output; claims about a spec quote it.
5. **Validate structure.** Model output that feeds a pipeline passes a schema check; on failure, fall back deterministically or retry within a bound.
6. **Separate the judge from the author.** Verification by a fresh-context reviewer or a different model beats self-review.
7. **Prevent leakage when evaluating models.** Strip answer markers and comments from prompts, use canary strings and private holdouts (`building-trustworthy-benchmarks`).
8. **Record what the model did.** Keep prompt, model id, and parameters with any generated artifact you rely on.

## Example marker use

```
The service authenticates users via [UNKNOWN: auth protocol not stated].
Data retention is [DECISION NEEDED: 30d vs 90d — recommend 90d for audit].
```

## Audit checklist for a generated document

- Every concrete number, name, and technology traces to the input or a cited source.
- No unresolved placeholders slipped into the "final" version.
- Every diagram element appears in the text and vice versa.

## Common mistakes

- "Reasonable defaults" quietly presented as requirements.
- Using the model to grade its own answer.
- Letting a model-picked mapping into a compliance report unreviewed.
- Removing `[UNKNOWN]` tags to make a document look finished.
