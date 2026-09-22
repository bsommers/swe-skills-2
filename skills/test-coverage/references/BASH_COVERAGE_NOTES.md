# Bash/Shell Coverage: What Actually Works

Verified empirically (macOS ARM64, kcov 43, bats-core 1.14.0) — not assumed from docs. Re-verify against your own tool versions; kcov's bash instrumentation is trap-based and version-sensitive.

## kcov works cleanly on a direct script invocation

```bash
kcov --exclude-pattern=/opt/homebrew,/usr/lib,/System out/ ./mytool --some-flag
```

This produces accurate per-file, per-line coverage for `mytool` and everything it `source`s. Use this for coverage of direct CLI invocations (smoke tests, `--help`, one-shot commands).

## kcov + bats-core has two real failure modes

1. **`--include-path` breaks child-process attach.** With `--include-path=<repo>` set, kcov frequently fails to follow bats' nested fork/exec chain (`bats-exec-suite` → `bats-exec-file` → per-test bash subshell) far enough to instrument anything — you get a coverage report with 0 covered lines and no error. Fix: use `--exclude-pattern` to keep bats' own install directory out of the report instead of `--include-path` to allow-list your repo. `--exclude-pattern` filters at the instrumentation layer in a way that doesn't disturb the attach chain the same way; `--include-path` does.

2. **bats' own DEBUG trap collides with kcov's.** Without `--exclude-pattern` covering bats' install directory (e.g. `/opt/homebrew/Cellar/bats-core/*` on a Homebrew install, or wherever `bats-core`'s `lib/bats-core/*.bash` lives), kcov attempts to line-trace bats' own internal trap-handling scripts. Both kcov and bats-core hook the `DEBUG` trap for their own purposes; tracing bats' trap-handling code with kcov's trap-based tracer causes runaway recursive output (each trap firing re-triggers the other), and the run can hang or produce gigabytes of log noise. **Always exclude the bats install path.**

3. **Even with both fixed, per-file attribution through `source` is unreliable.** After applying both fixes above, the run completes and produces real coverage data — but it may attribute ALL covered lines to bats' own generated temp script (e.g. `/tmp/bats-run-XXXX/1-mytest.bats.src`) rather than correctly split across the `source`d library files a test pulls in. This means you can get a real, non-zero coverage number that is nonetheless useless for per-file gap analysis.

## Practical recommendation

- Use kcov for a rough, best-effort **aggregate** percentage and for genuinely useful coverage of direct CLI-invocation-style tests (bypassing bats entirely, e.g. a small non-bats smoke-test script).
- Use `scripts/shell_function_reachability.sh` (in this skill) as the **reliable, deterministic** signal for "what's completely untested" — a static function-definition-vs-test-corpus cross-reference. It can't measure branch coverage inside a function, but it never lies about whether a function is referenced *anywhere* in the test suite, and it has zero tooling dependencies or version sensitivity.
- Report both numbers side by side in your coverage report; don't present kcov's number alone as if it were trustworthy per-file data for a bats-tested project.

## The flags that worked here, for reference

```bash
kcov --exclude-pattern=/opt/homebrew,/usr/lib,/System /tmp/out bats tests/unit/some_test.bats
```

No `--include-path`. `--include-pattern` (report-filtering only, doesn't touch the attach chain) is safe to combine with this if you want to narrow the *report* to specific paths after the fact.
