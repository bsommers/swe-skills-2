# Contributor reply format

One comment, human first, machine block last. Validate before posting:
`python3 skills/pr-review/scripts/validate_pr_review.py reply.md` (path relative to the library root; stdlib only). Schema: `pr-review-v1.schema.json`. Template: `../templates/CONTRIBUTOR_REPLY_TEMPLATE.md`. Sample: `sample-reply.md`.

## Tone

Open with specific thanks, name what is good, then request changes as numbered items. Each item states the evidence, the exact fix, and the check that proves it. Neutral and kind; no sarcasm, no "obviously". Never imply bad faith; report facts ("this request is sent to a third-party host") not motives.

## Stable ID rules (so a follow-up agent can re-check)

1. Finding id = `<CAT>-<slug>`: `CAT` is 2-5 capitals from the category (`HYG`, `EGR`, `PRV`, `SUP`, `TRU`, `RES`, `PAR`, `COR`, `TST`, `ARC`, `DOC`, `CMP`, `OTH`); `slug` is 3-61 chars of lowercase kebab naming the rule and the symbol or module (`EGR-preview-csp-open-connect`).
2. Derive the slug from what is wrong, never from line numbers or order. Renumbering breaks re-checks.
3. IDs are unique per review, never reused for a different problem, and kept when the line moves. A new problem gets a new ID.
4. Re-review: for each previous ID, re-run its `acceptance_check` against the new `head_sha`; report resolved IDs in prose and drop them from `findings`, keep unresolved ones with the same ID and updated evidence.
5. Question ids are `Q-<slug>` on the same rules.

## Field rules

- `blocking: true` for every `critical` or `high` finding, and for any finding that must change before merge. `info` and most `low` are non-blocking.
- `file`/`line` are null only for PR-level findings (hygiene, description).
- `evidence` quotes or names what you saw (a short snippet is fine). Never paste secrets seen in the diff; say "a token-shaped string at file:line".
- `acceptance_check` must be mechanical where possible: a command, test name, or grep that returns nothing. If only a human can judge, say what they should look at.
- Verdicts: `approve` (no blocking), `changes_requested` (>=1 blocking), `needs_info` (cannot judge without answers; >=1 question), `reject` (unsalvageable or out of scope; explain, stay kind).
- Optional `split_proposal[]`: `{title, paths[], depends_on[]}` for each proposed sub-PR.
- The validator enforces the schema plus these consistency rules.
