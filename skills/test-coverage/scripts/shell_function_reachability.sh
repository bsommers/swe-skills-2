#!/usr/bin/env bash
# shell_function_reachability.sh — Static test-reachability analysis for
# Bash/shell codebases.
#
# Instrumented line coverage (kcov) is genuinely unreliable for Bash
# projects tested with bats-core: bats rewrites each .bats file into a
# temp script before execution, and kcov's DEBUG-trap-based bash tracer
# frequently mis-attributes (or entirely drops) coverage for files pulled
# in via `source` once bats' own temp-script rewriting is in the mix —
# this was verified empirically, not assumed (see references/
# BASH_COVERAGE_NOTES.md). Use kcov when it works cleanly for a given
# project, but treat THIS script as the reliable floor-level signal:
# "is every defined function referenced by at least one test?" It answers
# a coarser question than line coverage, but it never gives a false
# positive from a broken instrumentation chain and needs no extra tooling
# beyond grep — it works identically in CI and locally.
#
# Usage:
#   shell_function_reachability.sh <lib_dir> [<lib_dir> ...] -- <test_dir> [<test_dir> ...]
#
# Example (run from a repo root):
#   shell_function_reachability.sh lib cvm -- tests/unit tests/integration
#
# Exit status: 0 always (this is a reporting tool, not a gate — wire the
# printed "UNREACHED" count into your own CI threshold if you want a gate).

set -euo pipefail

usage() {
    echo "Usage: $0 <lib_dir_or_file> [...] -- <test_dir_or_file> [...]" >&2
    exit 1
}

lib_paths=()
test_paths=()
seen_separator=false
for arg in "$@"; do
    if [[ "$arg" == "--" ]]; then
        seen_separator=true
        continue
    fi
    if [[ "$seen_separator" == "false" ]]; then
        lib_paths+=("$arg")
    else
        test_paths+=("$arg")
    fi
done

[[ ${#lib_paths[@]} -eq 0 || ${#test_paths[@]} -eq 0 ]] && usage

# Collect candidate shell files under each lib path (file or directory).
lib_files=()
for p in "${lib_paths[@]}"; do
    if [[ -f "$p" ]]; then
        lib_files+=("$p")
    elif [[ -d "$p" ]]; then
        while IFS= read -r f; do
            lib_files+=("$f")
        done < <(find "$p" -type f \( -name "*.sh" -o -perm -u+x \) 2>/dev/null | grep -v '\.bats$' || true)
    fi
done

test_files=()
for p in "${test_paths[@]}"; do
    if [[ -f "$p" ]]; then
        test_files+=("$p")
    elif [[ -d "$p" ]]; then
        while IFS= read -r f; do
            test_files+=("$f")
        done < <(find "$p" -type f \( -name "*.bats" -o -name "*.sh" \) 2>/dev/null || true)
    fi
done

if [[ ${#lib_files[@]} -eq 0 ]]; then
    echo "No library shell files found under: ${lib_paths[*]}" >&2
    exit 1
fi
if [[ ${#test_files[@]} -eq 0 ]]; then
    echo "No test files found under: ${test_paths[*]}" >&2
    exit 1
fi

# Extract "name() {" / "function name {" style definitions per file.
declare -a fn_names=()
declare -a fn_files=()
# NOTE: intentionally uses [[:space:]] rather than \s — \s/\S/\d are
# GNU/PCRE extensions that BSD sed/grep (macOS, *BSD) silently mistreat as
# a literal "s"/"S"/"d" character instead of a whitespace class, which
# would corrupt every extracted name starting with those letters
# (show_help -> how_help) rather than erroring loudly. Verified by hand
# against this exact failure mode — keep it portable.
for f in "${lib_files[@]}"; do
    while IFS= read -r line; do
        name="$(sed -E 's/^[[:space:]]*(function[[:space:]]+)?([A-Za-z_][A-Za-z0-9_]*)[[:space:]]*\(\).*/\2/; s/^[[:space:]]*function[[:space:]]+([A-Za-z_][A-Za-z0-9_]*).*/\1/' <<<"$line")"
        [[ -z "$name" ]] && continue
        fn_names+=("$name")
        fn_files+=("$f")
    done < <(grep -E '^[[:space:]]*(function[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*[[:space:]]*\(\)[[:space:]]*\{?[[:space:]]*$|^[[:space:]]*function[[:space:]]+[A-Za-z_][A-Za-z0-9_]*[[:space:]]*\{?[[:space:]]*$' "$f" || true)
done

if [[ ${#fn_names[@]} -eq 0 ]]; then
    echo "No function definitions found in: ${lib_paths[*]}" >&2
    exit 1
fi

# Build one big haystack of test-file contents to grep against (fast: one
# read instead of N greps per function).
test_corpus="$(cat "${test_files[@]}" 2>/dev/null || true)"

unreached=()
reached_count=0
total=${#fn_names[@]}

for i in "${!fn_names[@]}"; do
    name="${fn_names[$i]}"
    src="${fn_files[$i]}"
    # A function is "reached" if its name appears anywhere in the test
    # corpus OTHER than as its own definition line in a lib file (which
    # it never will, since test_corpus only contains test files) — i.e.
    # any direct call, or reference inside a `run <name>` bats invocation.
    if grep -Fqw -- "$name" <<<"$test_corpus"; then
        reached_count=$((reached_count + 1))
    else
        unreached+=("$name|$src")
    fi
done

echo "=== Shell Function Test-Reachability Report ==="
echo "Library files scanned : ${#lib_files[@]}"
echo "Functions defined     : $total"
echo "Referenced in tests   : $reached_count"
echo "UNREACHED (0 refs)    : ${#unreached[@]}"
echo ""

if [[ ${#unreached[@]} -gt 0 ]]; then
    echo "--- Functions with no reference anywhere in the test suite ---"
    for entry in "${unreached[@]}"; do
        IFS='|' read -r name src <<<"$entry"
        printf '  %-40s %s\n' "$name" "$src"
    done
    echo ""
    echo "Note: a name match only proves the function is REFERENCED by a test"
    echo "(e.g. via 'run some_function' or a direct call) — it does not by"
    echo "itself prove every branch inside it executes, or that external-tool"
    echo "calls inside it (docker, ssh, VBoxManage, ...) are exercised rather"
    echo "than mocked away. Treat this as the floor, not the ceiling."
    echo ""
    echo "Also read the reverse false-negative case: a function invoked only"
    echo "indirectly, through a black-box CLI call in a test (e.g. 'run"
    echo "./mytool --help' exercising show_help() from inside the compiled"
    echo "entrypoint), won't match here since its name never appears as text"
    echo "in the test file. Spot-check a few UNREACHED entries against the"
    echo "test suite before trusting the count outright."
fi
