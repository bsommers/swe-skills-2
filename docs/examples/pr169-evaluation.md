# Evaluation: pr-review router on an external PR

Target: a public PR from a fork (35 files, +3634/-129, five commits; a loopback web studio, MCP resources, TUI pixel rendering). Static review only: the diff was read, nothing was built, run or posted. Output: `pr169-review.md` (verdict `changes_requested`, 16 findings, 9 blocking, 4 questions; validator `OK`). Baseline for comparison: an earlier maintainer-written review of the same PR.

## Caught by both
CSP gap for previewed HTML and the Studio iframe; access token echoed in replies and status text; bundled scope with split proposal; gate not run and stale base; serial accept loop; duplicate CSPRNG helper and `unsafe` without `SAFETY`; Studio save ignoring revisions; ignored persist errors; `localhost` host allowance; missing tests; opt-in and theme-aware pixel graphics; the same open questions.

## Caught by the skills only
- MCP resources list and read every context key with no size cap (the earlier review only asked whether this was scoped).
- Commit `af77acc` uses a symbol first added by a later commit, so history is not bisectable and the MCP piece cannot ship before the artifacts piece. Found from per-commit file lists.
- Concrete, ordered sub-PR boundaries with path globs and dependencies, plus a machine-checkable acceptance check per finding.
- Explicit negative results with coverage: no manifest, lockfile or workflow change; no client-side network code; Markdown rendering escapes before formatting; pin coordinates are digit-only; HTTP parser rejects smuggling shapes.

## Missed by the skills (the earlier review had them)
- The `:web external` argv and browser-history exposure: the opener lives on the base branch, not in the diff. Mitigation: router now says to read base-branch files for behavior the diff only references.
- Windows FFI detail (link behavior, signature check against vendor docs) and the platform `Unsupported` runtime path. Not covered by a checklist item; left as a reviewer judgement.
- The claim that the branch diverges from main by a large unrelated diff was not reproduced: the 35 files are all on-topic and the base is 4 commits behind. Reported as `HYG-stale-base` only.

## False positives and noise
Candidates dismissed after reading the call site: `style="left:${p.x}%"` (digits only by regex), `unsafe set_var` in tests (test-only, justified), `fs::remove_file` (name validated), literal `127.0.0.1` URLs, `/dev/urandom` read (correct). Recipes produced about 40 raw hits for 16 findings; the reading step is what removes noise, so it stays mandatory.

## Skill edits made as a result, then re-run
1. `auditing-egress-and-telemetry`: severity contradicted the router (open `connect-src` was medium there, high in `reviewing-code-security`); now high in both.
2. `auditing-privilege-and-writes`: added hand-rolled HTTP parser checks (with "record sound parsers as positives"), list/read APIs exposing a whole shared store, and terminal graphics enabled by env guessing.
3. `reviewing-pr-hygiene`: added base-staleness and per-commit file-list commands, a note on detecting non-buildable commits, and a hygiene severity line.
4. `pr-review`: read base-branch files, not a PR checkout, when the diff references behavior defined elsewhere.

Re-run with the edited skills: same 16 findings, same verdict; the parser check added a positive note to the reply. Limits: one PR, one reviewer, and the baseline review was written by the same maintainer context, so recall numbers are indicative, not a benchmark.
