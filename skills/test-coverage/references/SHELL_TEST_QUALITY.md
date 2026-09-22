# Shell Test-Quality Checklist Reference

Apply this whenever the target repository includes Bash or shell code, regardless of coverage tool availability. These are correctness bugs that raw line coverage will not surface even at 100%:

## 1. `set -e` Interaction Check

bats-core does NOT run test bodies under `set -e`, but a real CLI entrypoint sourcing these library files typically does (`set -euo pipefail` at the top). A bare `[[ cond ]] && cmd` or `cmd1 || cmd2` used as a function's or loop's *final* statement silently returns the condition's exit code — under `-e`, this can abort the entire real process the moment the "everything's fine" branch is hit, while the exact same code sails through bats untested (bats doesn't run under `-e`, so this class of bug is invisible to it).

**Verification technique:** Run the suspect function in a real `bash -euo pipefail -c '...; echo REACHED_END'` subshell and assert `REACHED_END` actually prints.

## 2. External-Command Mocking

Every function that shells out to docker/podman/ssh/cloud CLIs/hypervisor managers needs at least one test where that binary is a fake script on `PATH` (`PATH="$fake_bin_dir:$PATH"`) recording its invocation and returning canned output — not just a `command -v docker || skip`. Skipping when the tool's absent means CI (which usually lacks these tools) never runs the logic at all.

## 3. Command-String Injection Check

Anywhere a variable is spliced into a command *string* that's later handed to a shell (`ssh host "$cmd"`, `eval "$x"`) rather than passed as a separate argv element, add a test with shell metacharacters (`; touch pwned`, `` `id` ``) in that variable and assert nothing unintended happens. Contrast with argv-array invocation (`cmd_array+=("$var")`), which is immune by construction and doesn't need this test.

## 4. Dispatch-Table Completeness

Every `case "$mode" in a|b|c) ...; esac` that maps an enum-like value to behavior should have a companion test asserting an unrecognized value fails loudly (`*) die ...`) — not silently falls through and does nothing. A dispatch table with no default case is a silent-no-op waiting to happen the moment a new valid-looking-but-untested value reaches it.
