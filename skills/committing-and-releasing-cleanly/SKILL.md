---
name: committing-and-releasing-cleanly
description: Use when about to commit, push, open a PR, tag a version, or cut a release; when a working tree mixes unrelated changes; or when unsure whether an action is safe to run without asking.
---

# Committing and Releasing Cleanly

## Overview

Commits are the unit of review and rollback. Keep them **atomic, verified, and explained**; treat anything outward-facing (push, tag, publish) as needing explicit permission. If the project has its own release skill or checklist, follow that over this.

## Commit

1. **Verify first:** the full local gate is green (`layered-verification-gates`); docs and changelog updated (`keeping-docs-in-sync`).
2. **One logical change per commit.** Separate refactors from behavior changes; split a mixed tree into clean commits (stage by hunk).
3. **Conventional messages:** `type(scope): subject`, types `feat fix test refactor docs ci chore`. Subject in imperative mood, ≤ 72 chars; body explains **why**, and what was verified.
4. **Never commit** secrets, absolute paths, build output, or unexplained hash-pin changes.
5. **Never bypass hooks** or checks to get a commit through.

## Branch and PR

- Default to git with GitHub as the remote; use `gh` for PRs, checks (`gh pr checks`), and releases.
- Work on `feature/…`, `fix/…`, `refactor/…`; `main` stays green.
- Push once, after local verification, to conserve CI minutes; avoid WIP pushes.
- PR description: summary, why, how verified (commands + results), risks, follow-ups. For grouping issues into PRs and the full template, load `writing-pull-requests`.
- Squash or merge per project convention; delete merged branches.

## Release

1. Pre-release gate: full suite, clean-clone run, security scan, docs check.
2. Choose the semver bump from the change list: breaking → major, feature → minor, fix → patch.
3. Update changelog and version; tag; publish (`gh release create <tag> --notes-file <changelog-excerpt>`).
4. Multiple remotes (authoritative + org mirror): sync **both** with the project's sync script and verify.

## Ask before you act

Confirm first, unless durably authorized, for: push, force-push, tag/publish, deleting branches or data, amending shared history, touching other repos, running anything that spends money. Approval for one push isn't approval for the next.

## Quick recovery

Wrong commit not yet pushed → `git reset --soft HEAD~1` and redo. Already pushed → new commit that fixes forward; don't rewrite shared history without agreement.

## Common mistakes

- "wip" commits pushed to CI.
- Message says "fix stuff".
- Version bumped without changelog.
- Force-pushing over a teammate's work.
- Releasing from a dirty tree.
