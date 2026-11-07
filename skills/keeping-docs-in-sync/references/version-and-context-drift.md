# Version strings and agent-file drift

## Current-version strings
They hide in README badges, doc headers, man pages, API examples, and packaging metadata (for example a Nix flake version).

- Derive from the manifest, or add a grep gate that compares each occurrence to it.
- Separate **current-version** mentions (update) from **historical** ones (changelog entries, "added in vX": leave alone). A blind find-and-replace corrupts history.

## Agent context files
File counts and module paths drift. One incident: a stated path to a security helper was wrong, so agents followed it to a nonexistent module. Verify every path and count in a context file with a script, not by eye (`writing-agent-context-files`).

## Stale-on-merge
A doc-sync PR based on an older release can be stale by the time it merges. Rebase and re-run the drift gate on the merged result before landing.
