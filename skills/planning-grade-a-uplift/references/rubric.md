# Grade scale and milestone prompts

## Scale (apply per dimension)

| Grade | Meaning |
|---|---|
| A+ | Meets the goal with evidence; failure modes guarded by automation; a newcomer succeeds unaided |
| A | Meets the goal; evidence exists; one or two manual steps remain |
| B | Works for the author; gaps appear off the happy path or on other platforms |
| C | Partly works; claims exceed evidence |
| D/F | Broken, misleading, or unsafe |
| ? | Not enough evidence to grade |

## Prompts for additional milestones

- Can a stranger install, run and verify it in ten minutes on each supported platform?
- Is every number, count and command in the docs generated or linted?
- Is there a regression suite for each past incident?
- Are claims about quality backed by a benchmark or eval someone else can rerun?
- Is there a release process with provenance (tags, checksums, changelog)?
- Is the supported-platform matrix tested, not asserted?
- Are contributions guided (templates, CONTRIBUTING, good first issues)?
- Is security reporting defined, and are dependencies and CI pinned?
- What is the deprecation and compatibility policy?
- Is there telemetry-free feedback: how do you learn it is failing for users?
