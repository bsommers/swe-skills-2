---
name: writing-pull-requests
description: Use when turning one or more issues or a finished branch into a GitHub pull request, when deciding which issues belong in the same PR, when writing a PR title or description, or when a PR should be drafted for human review before it is opened.
---

# Writing Pull Requests

## Overview

A PR is a request for a reviewer's attention. Give them **one coherent change, a description they can verify, and a link to every issue it resolves.** The deliverable is a git branch, a PR body file, and a reviewable `open-pr.sh` that uses the `gh` CLI. Never push or open the PR without the user's go-ahead (`committing-and-releasing-cleanly`).

## Procedure

1. **Load the bundle.** For each issue (numbers, URLs, or a `drafting-issue-reports` script), `gh issue view <n>`. Drop issues that are closed or already fixed on the base branch, and say which you dropped. Drafted issues that aren't filed yet have no numbers: ask to file them first, or leave `Closes #?` placeholders.
2. **Group into PRs.** Issues share a PR only when they touch the same area *and* a reviewer can judge them together. Split out anything risky, unrelated, or a pure refactor. A PR over ~400 changed lines (excluding generated files) should be split. Show the grouping table (PR · issues · reason) before coding when there is more than one PR.
3. **Branch and commit.** One branch per PR (`fix/…`, `feat/…`). One commit per issue where possible, with a conventional message whose body ends `Refs #<n>`.
4. **Verify.** Run the project's gate (`layered-verification-gates`). Record the exact commands and their results; they go in the body verbatim.
5. **Write the body file** from `references/pr-body-template.md` (e.g. `.pr/<branch>.md`). Fill every section; write "None" rather than deleting one.
6. **Write `open-pr.sh`**, which only echoes unless run with `--open`:
   `git push -u origin <branch> && gh pr create --base <default-branch> --title "<title>" --body-file .pr/<branch>.md --label <labels> [--draft]`
7. **Report** the grouping, the title, the path to each body file, and what is unverified. Stop and wait.

## Title

Conventional form, ≤ 72 chars, imperative, and about the change rather than the process: `fix(export): keep last CSV row without trailing newline`. For a bundle, name the shared outcome, not a list: `fix(export): correct row handling in CSV and TSV writers`.

## Linking issues

- Put one closing keyword per issue on its own line: `Closes #12`, then `Closes #15`. `Closes #12, #15` closes only #12.
- Use `Refs #n` for partial fixes. Keywords only close issues when the PR merges into the default branch.
- Copy the label type from the issues (`bug` → `fix`, `enhancement` → `feat`).

## Common mistakes

- Bundling unrelated fixes because they were in the same list.
- "Tested locally" with no command or result.
- A description that narrates the commits instead of saying what changes for the user and why.
- Dropping risk and rollback because "it's small".
- Pushing or opening the PR to "check how it looks". Show the body file instead. `gh pr create --dry-run` is not a preview: it may still push.
- Scope creep: fixes the issues didn't ask for. File them as follow-ups instead.
