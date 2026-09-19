---
name: building-small-cli-tools
description: Use when writing a command-line tool, script, or small utility (converters, generators, exporters, helpers), or adding a GUI or file format on top of one, for reliable behavior and easy sharing.
---

# Building Small CLI Tools

## Overview

Small tools get run by other people on inputs you didn't imagine. A little discipline — help text, exit codes, validation, a failure test — makes them trustworthy at almost no cost.

## Checklist

1. **One purpose.** Name it by what it does. Put core logic in a function; `main()` only parses args and calls it.
2. **Stdlib first.** Third-party deps only for a real reason; state install in the README.
3. **`--help` is the manual.** Every flag documented, with defaults and an example.
4. **Config order:** flag > environment variable > default. Print the effective config in verbose mode.
5. **Exit codes:** `0` success; `1` invalid input or runtime failure with a **one-line diagnostic and no stack trace**; `2` usage errors. Unknown subcommand/target → clean nonzero exit.
6. **Streams:** data to stdout, logs/errors to stderr, so it pipes.
7. **Validate inputs** with bounds and friendly messages ("low-freq must be < high-freq") before doing work.
8. **Side effects are opt-in/out:** `--dry-run`, `--no-play`, `--out DIR`; never overwrite silently.
9. **Deterministic output** (sorted, seeded) so tests and diffs work.
10. **Paths:** resolve relative to the script/repo, not the cwd; `#!/usr/bin/env python3`.
11. **GUI is a thin shell** over the same function the CLI calls; never fork the logic.
12. **Small file format? Make errors line-aware** ("line 12: unknown note 'H9'") and give a `--list`/`--check` that parses without side effects.
13. **Tests via subprocess:** exit 0 on valid input, exit 1 with a diagnostic on invalid, expected output file exists.
14. **README:** install, one example run, options table, format spec if any.

## Skeleton

```python
#!/usr/bin/env python3
"""csv2json: convert CSV to pretty JSON."""
import argparse, csv, json, sys

def convert(rows, indent=2):
    return json.dumps(list(rows), indent=indent, sort_keys=True)

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path"); p.add_argument("--indent", type=int, default=2)
    a = p.parse_args(argv)
    if a.indent < 0:
        print("error: --indent must be >= 0", file=sys.stderr); return 1
    try:
        with open(a.path, newline="") as f:
            print(convert(csv.DictReader(f), a.indent))
    except OSError as e:
        print(f"error: {e}", file=sys.stderr); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Common mistakes

- Uncaught exceptions as the error UX.
- Logic inside the GUI callback.
- Parsing arguments by hand until quoting breaks.
- Relative paths that only work from one directory.
- Adding features before the failure-path test exists.
