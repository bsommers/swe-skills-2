Thank you, @example-contrib, for adding the `--json` output mode to the exporter. The flag is useful for scripting and the fixtures are easy to follow.

**What is good**
- Output goes through the existing `Writer` trait, so both formats share one code path.
- The new tests cover empty input and unicode names.

**Changes requested**

1. **`COR-export-json-trailing-comma`: invalid JSON for one-row exports** (high, blocking) at `src/export/json.rs:41`
   - Why: the writer emits `,` after every row, so a single-row export ends `[{"a":1},]`.
   - How to fix: join rows with `,` between items only.
   - How we will verify: `cargo test export_json_single_row` passes and `python3 -m json.tool` accepts the output.
2. **`HYG-bundled-ci-change`: unrelated CI edit** (medium, non-blocking) at `.github/workflows/ci.yml`
   - Why: the workflow change is independent of the exporter.
   - How to fix: move it to its own PR.
   - How we will verify: the diff no longer touches `.github/`.

**Questions**
- `Q-export-schema-version`: should the JSON carry a schema version field? Either answer is fine; we want the choice documented.

**Next steps**
1. Fix item 1 and push; item 2 can go to a separate PR.
2. Comment here and we will re-check each ID against the new head.

Thanks again; happy to help if anything is unclear.

```json pr-review/v1
{
  "schema": "pr-review/v1",
  "pr": {"repo": "example-org/example-repo", "number": 42},
  "head_sha": "0123456789abcdef0123456789abcdef01234567",
  "verdict": "changes_requested",
  "summary": "Useful --json exporter; one blocking correctness bug and one bundled CI change.",
  "skills_run": ["pr-review", "reviewing-pr-hygiene"],
  "findings": [
    {
      "id": "COR-export-json-trailing-comma",
      "category": "correctness",
      "severity": "high",
      "file": "src/export/json.rs",
      "line": 41,
      "evidence": "Writer appends ',' after every row; one-row output is [{\"a\":1},]",
      "required_change": "Emit separators between rows only.",
      "acceptance_check": "cargo test export_json_single_row passes; python3 -m json.tool accepts the output",
      "blocking": true,
      "confidence": "high"
    },
    {
      "id": "HYG-bundled-ci-change",
      "category": "hygiene",
      "severity": "medium",
      "file": ".github/workflows/ci.yml",
      "line": null,
      "evidence": "Workflow edit is unrelated to the exporter change.",
      "required_change": "Move the CI change to a separate PR.",
      "acceptance_check": "git diff --stat BASE...HEAD shows no .github/ paths",
      "blocking": false
    }
  ],
  "questions": [
    {"id": "Q-export-schema-version", "text": "Should the JSON include a schema version field?"}
  ]
}
```
