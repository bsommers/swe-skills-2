# Portable prompt: whole-repo review

Paste into any harness (Claude Code, agy, opencode, pi, Cursor) that does not load skills. Replace `<GOAL>`.

```
Review this repository against its goals: <GOAL>.
Read-only until I approve the plan. Check `git status` first; other agents may be editing.

1. Baseline: find and run the repo's test/lint gate. Record pass, fail, skipped.
2. Fan out independent lenses (correctness, security, tests, docs/plans alignment,
   portability, goal fit, operations). Use parallel subagents if you have them, with the
   cheapest model that preserves quality; strongest model for architecture and security.
   No subagents: run the lenses one at a time, writing each result to
   docs/reviews/<date>/results/NN-lens.md before the next.
3. Run your highest-effort code review on the repo or current diff. Reproduce each finding.
4. Compare README, agent instruction files, docs/, plans and manifests with the code and
   each other. List every disagreement and write a plan that brings them into conformance.
5. State what would make this an A+ project for its goals: rubric, current grade per
   dimension, gaps, work items with acceptance and verify commands, and milestones.
   Add any extra milestones that would help the goals.
6. Write docs/reviews/<date>/REVIEW.md. Ask before filing issues, pushing or editing.
```
