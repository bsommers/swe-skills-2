# Triaging external or AI-generated contributor PRs

Check, in order:

1. **Supply chain surface:** did manifests, lockfiles, build scripts, or dependencies change? Treat any such change as the primary review target.
2. **Pinned SHAs:** verify every pinned action SHA against its claimed tag (`hardening-ci-workflows`).
3. **Workflow triggers:** new workflows use `pull_request`, not `pull_request_target`.
4. **Mergeability without touching your tree:** find each PR's merge-base against current main, then
   `git merge-tree --write-tree main <pr-ref>`. Do the same pairwise between PRs in the same batch.
5. **Verify the merged result, not the PR head.** Run the gate on the simulated merge.
6. **Unverified claims:** "tests also fail on main on my machine" must be confirmed against a baseline run.
7. **Merge order:** CI/infra PRs first; prerequisite portability fixes before any CI that depends on them; then the rest.
