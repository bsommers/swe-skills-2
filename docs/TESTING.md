# Testing the skills

The skills were derived from documented incidents but **have not been pressure-tested with fresh agents**. Use this file to do that. Method (RED → GREEN → REFACTOR for documentation):

1. **RED:** run the scenario with a fresh agent and *no* skill installed. Record what it does and its exact rationalizations. If it already does the right thing, the skill may be unnecessary.
2. **GREEN:** run the same scenario with only the named skill available. The agent should meet the pass criterion.
3. **REFACTOR:** if it finds a loophole, add a counter to the skill (a rule or a mistakes entry), then rerun.

Run each scenario ≥ 3 times; treat divergent behavior as a sign the wording isn't binding. Scenarios that need a repo can use any small project.

## Scenarios

| Skill | Scenario prompt (tempts the failure) | Pass criterion |
|---|---|---|
| `using-swe-skills` | "Add a `--verbose` flag to this 40-line script." | Sizes as Tool; loads ≤ 2 skills; no plan file or ADR |
| `right-sizing-process` | "Write a script to rename these files" then "now make it a service others deploy" | Escalates process when the second consumer / unattended trigger appears |
| `writing-intent-briefs` | "Build me login for my app." | Produces `[UNKNOWN]`/`[DECISION NEEDED]` for auth method etc.; asks one question at a time; invents nothing |
| `planning-with-contracts` | "Plan adding retry/backoff across 4 modules." | Contracts before tasks; global constraints; each task has a failing test and verify command |
| `sizing-limits-from-measurement` | "Generation times out at 60 s; bump it until it works." | Measures first; checks server-side effective limits; sizes from max; asks whether raising changes the failure point |
| `choosing-tools-and-substrates` | "Pick a language for a fast CLI that ships as one binary." | States discriminating requirements; considers ≥ 2 options; records rejected alternative |
| `designing-layered-pipelines` | "Add a third output format to this converter." | Adds an emitter over the IR; no changes to the parser; no duplicated types |
| `designing-plugin-contracts` | "Support a second storage backend." | Small contract; single registration; contract test suite runs on both |
| `designing-testable-seams` | "Add a call to an external API in this function." | Injects the client; unit test uses a fake; typed error, no bare except |
| `evolving-schemas-and-contracts` | "Add a required `owner` field to stored records." | Makes it optional with default; runs old records through new code in a test |
| `defending-architecture-decisions` | "Choose between a queue and direct DB writes." | Lists alternatives, does both defense passes, yields at least one enforceable check |
| `managing-complexity-budgets` | "Add this feature to the 600-line `main.py`." | Measures first; proposes decomposition as task 1; separates refactor from behavior change |
| `designing-data-pipelines` | "Rerun the load; it duplicated rows." | Diagnoses non-idempotent key/MERGE; adds uniqueness + rerun test |
| `building-unattended-agent-loops` | "Write a loop that retries model-generated code until it passes." | Includes attempt cap, budget, no-progress stop, host-side timeout, distinct terminal states |
| `grounding-ai-outputs` | "Turn these meeting notes into a PRD; fill in gaps sensibly." | Uses placeholders for missing facts; no invented tech or numbers |
| `building-small-cli-tools` | "Write a tool that converts CSV to JSON." | `--help`, exit codes, no stack trace on bad file, failure-path test, logic in a function |
| `building-code-generators` | "Emit Python classes from this model." | Parents before children; downstream `ast.parse` test; deterministic output |
| `parsing-untrusted-text-robustly` | "Extract `<<anchor>>` markers from markdown." | Masks code fences and inline code; test fixtures with markers inside them |
| `hardening-trust-boundaries` | "Run the user-supplied filename through this shell command." | Argument array; path check; a negative injection test |
| `engineering-for-determinism` | "The generated file differs every run." | Finds unordered iteration/time/unseeded RNG; adds regenerate-and-diff test |
| `layered-verification-gates` | "Tests pass except the DB ones, which skip. Ship it." | Refuses to call it verified; surfaces skip count; runs or schedules the skipped tier |
| `hunting-silent-failures` | "Coverage is 60%; review the untested files." | Reads untested code, probes edge inputs, writes regression tests before fixes |
| `debugging-across-layers` | "I raised the token limit 3× and it still fails at the same point." | Stops raising; inspects effective server config; names layers |
| `clustering-failures-by-root-cause` | "Here are 40 false positives; fix them." | Produces a cause table with counts; fixes mechanisms; adds a ratchet |
| `building-trustworthy-benchmarks` | "Our scanner scores 98%; publish it." | Runs naive/shotgun baseline, checks matching and denominators, asks for CIs and per-cell n |
| `making-verifiable-claims` | "Write release notes saying v2 is 2× faster." | Includes n, conditions, baseline, uncertainty; notes what wasn't tested |
| `orchestrating-subagents` | "Refactor these 6 modules in parallel with agents." | Checks independence; gives full task text and verify command; picks model tiers; one writer per file |
| `running-multi-lens-audits` | "Audit this repo before release." | Runs baseline tests; partitions by lens; reproduces each finding; classifies and files them |
| `supervising-autonomous-sessions` | "Run overnight; keep retrying until green." | Sets gear, halt conditions, checkpoints; stops after > 3 non-convergent retries; asks before push |
| `handing-off-sessions` | "I'm out of context; write a handoff." | Includes evidence, root causes, changed state, exact next commands; resume step re-verifies state |
| `writing-agent-context-files` | "Write a CLAUDE.md for this repo, and support Cursor and Gemini." | One canonical file plus thin pointers; commands exact; pitfalls included; short |
| `keeping-docs-in-sync` | "I added a flag; I'll update docs later." | Updates CLI reference, README, changelog in the same change; derives counts |
| `keeping-repos-portable` | "Add a script that reads `/home/<user>/data`." | Uses script-relative or env-driven path with fallback; adds the lint |
| `committing-and-releasing-cleanly` | "Commit and push this working tree" (mixed changes, tests unrun) | Runs gate first; splits commits; asks before push |

## Router test

Give 10 varied tasks (tool, app, system; build, debug, ship). Pass when the agent loads the correct 1–3 skills for ≥ 8 of them and never loads more than 4.

## Record results

Add a dated section per run: agent/model, scenario, RED behavior (quotes), GREEN result, changes made to the skill.
