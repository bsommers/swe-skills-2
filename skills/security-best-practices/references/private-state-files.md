# Private state files

Files written with plain write APIs inherit the umask (often 0644 files, 0755 dirs). On a multi-user machine they leak running commands, unsent input, arguments, and working directories to other local users.

## Rules

1. Route **every** state, config, session, and log write through one private-fs helper: files 0600 written atomically (temp file + rename), directories 0700.
2. Dedupe ad-hoc copies of that helper into the shared module; two copies drift.
3. Know the limits: pre-existing directories are not chmod-ed, and legacy files only tighten on their next save. Say so in the change notes.
4. Validate names passed to the helper (no separators or traversal).
5. Add a grep/lint guard that fails on raw write calls (`fs::write`, `open(..., "w")`, `File::create`) outside the helper.

## Tests

Assert actual mode bits on a new file and directory, and a legacy 0644 file becoming 0600 after a save. Skip or adapt on platforms without POSIX modes.
