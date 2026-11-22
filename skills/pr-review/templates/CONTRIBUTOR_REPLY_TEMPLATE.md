Thank you, @<author>, for <specific thing the PR does>. <One sentence of genuine, specific appreciation.>

**What is good**
- <specific strength with file or behavior named>

**Changes requested** (each has an ID so a follow-up review can re-check it)

1. **`<ID>`: <short title>** (<severity>, <blocking | non-blocking>) at `<file>:<line>`
   - Why: <one or two sentences of evidence>
   - How to fix: <concrete change>
   - How we will verify: <command, test, or grep that must pass>

**Questions**
- `Q-<slug>`: <question>

**Next steps**
1. <ordered step, for example "split per the proposal below", "rebase onto main">
2. Push to this branch and comment here; we will re-check every ID above against the new head.

Thanks again for the contribution. Happy to help if any item is unclear.

<!-- Machine-readable block: keep last. Schema: references/pr-review-v1.schema.json -->
```json pr-review/v1
{
  "schema": "pr-review/v1",
  "pr": {"repo": "<owner>/<repo>", "number": 0},
  "head_sha": "<sha>",
  "verdict": "changes_requested",
  "summary": "<= 600 chars",
  "skills_run": ["pr-review"],
  "findings": [],
  "questions": []
}
```
