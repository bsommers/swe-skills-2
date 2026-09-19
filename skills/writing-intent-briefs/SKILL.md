---
name: writing-intent-briefs
description: Use when a request is vague, when requirements come from meeting notes or a rough idea, before planning or coding starts, or when you are tempted to fill in details the user never stated.
---

# Writing Intent Briefs

## Overview

Bound the work before building it. A brief turns a spark into: what problem, for whom, what "done" measures, what is **out**, and what is still unknown. **Never invent specifics** the user did not give or that cannot be deduced — mark them and ask.

## The brief (fits on one screen)

```markdown
# Intent: <name>
**Problem / who it's for:** <1–2 sentences, named persona>
**Outcome & success criteria:** <measurable: "converts 1 MB CSV in < 1 s", not "fast">
**In scope:** …
**Out of scope:** … (explicit non-goals stop scope creep)
**Constraints:** <stack, deadlines, compatibility, budgets>
**Assumptions:** <things I inferred, each flaggable>
**[UNKNOWN: …]** <facts not provided: auth method, SLA, data volume>
**[DECISION NEEDED: …]** <choices only the user can make, with options + your recommendation>
```

## Procedure

1. Restate the request in your own words; note every unstated detail you would need.
2. Fill the brief from what was actually said. Everything else becomes an `[UNKNOWN]` or `[DECISION NEEDED]` — do not paper over it.
3. Ask **one question at a time**, highest-impact unknown first. Offer a recommended answer so the user can say "yes".
4. Stop asking when remaining unknowns are cheap to change later; record them and proceed on stated assumptions.
5. Get an explicit go-ahead ("approved — build it") before multi-file changes or anything unattended. After go-ahead, work hands-off within the scope, and log blockers rather than expanding scope.

## Scale

- **Tool:** three lines in chat: goal, one success check, one non-goal.
- **App/System:** brief saved as `docs/intent/YYYY-MM-DD-<slug>.md` (or `.planning/`), linked from the plan.

## Placeholders are an agenda

Every `[UNKNOWN]` is a future question. A later refinement pass resolves them one by one, updating the brief. An audit pass can then check "no unresolved placeholders remain before build".

## Common mistakes

- Turning "a login" into OAuth + SSO + RBAC because that's typical. Ask, or mark `[DECISION NEEDED]`.
- Success criteria that can't be checked ("intuitive", "scalable"). Give a number or a demo.
- Non-goals left implicit. The first scope-creep argument is the sign.
- Asking five questions at once; users answer the easy one and skip the rest.
