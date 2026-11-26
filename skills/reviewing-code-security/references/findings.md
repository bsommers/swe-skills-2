# Security findings schema

Security findings are the `findings[]` items of `pr-review/v1` (`../../pr-review/references/pr-review-v1.schema.json`), so one block serves the whole review. Standalone audits (no PR) wrap them in the same envelope with `pr.number` of the tracking issue or `1`, or emit the bare array.

| Field | Rule |
|---|---|
| `id` | `<CAT>-<slug>`: `EGR` egress, `SUP` supply-chain, `PRV` privilege, `TRU` trust-boundary, `RES` resource-bounds, `PAR` parsing. Slug names the rule and symbol, not line or order; stable across revisions |
| `category` | `egress`, `supply-chain`, `privilege`, `trust-boundary`, `resource-bounds`, `parsing` |
| `severity` | `critical` `high` `medium` `low` `info` per the rubric in `reviewing-code-security` |
| `file`, `line` | first offending line; `line` null only for repo-wide findings |
| `evidence` | what was seen, quoting at most one short line; never paste a secret, say "token-shaped string" |
| `required_change` | the concrete fix, not "improve security" |
| `acceptance_check` | mechanical re-check: command, test, or `rg` pattern that must return nothing |
| `blocking` | true for `critical`/`high` (validator enforces) and any must-fix |
| `confidence` | `high` verified at call site, `medium` plausible, `low` pattern hit only |
| `cwe` | optional `CWE-n` (for example `CWE-319`, `CWE-532`, `CWE-338`, `CWE-367`, `CWE-22`) |

Example:

```json
{"id": "PRV-preview-token-in-rpc-reply", "category": "privilege", "severity": "high",
 "file": "src/wm/editor_pane.rs", "line": 120,
 "evidence": "status message embeds the full loopback URL including its access token",
 "required_change": "Return a redacted URL by default; expose the full URL only to the opener.",
 "acceptance_check": "rg -n 'format!.*http://127.0.0.1' src/ shows no reply-bound uses of the full URL",
 "blocking": true, "confidence": "high", "cwe": "CWE-532"}
```

Re-check protocol: a follow-up agent runs each `acceptance_check` at the new head and reports per ID resolved, unresolved or changed.
