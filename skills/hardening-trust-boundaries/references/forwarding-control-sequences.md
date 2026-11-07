# Forwarding untrusted control sequences to a privileged sink

Case: a terminal emulator or multiplexer passes an escape sequence from untrusted program output (for example an OSC clipboard-write) on to the host terminal or OS. The sink is privileged; the source is not.

## Rules

1. **Bound each sequence by its own terminator.** Searching the whole remaining buffer for a terminator lets unrelated escape bytes that follow an earlier terminator ride along raw.
2. **An unexpected embedded ESC aborts the sequence.** Drop it; do not forward.
3. **Allowlist the exact grammar**: permitted selection characters, base64 alphabet only, a size cap. A prefix check ("starts with the right opener") is not validation.
4. **Drop read/query forms.** A query lets untrusted output ask the host to send the clipboard back, which is exfiltration.
5. **Re-emit from parsed parts**, never the original bytes.
6. **Make test doubles as strict as production.** A laxer mock lets tests pass against behavior the real path rejects.
7. **Pin chunk-split behavior** with a test: the same sequence split across reads must give the same result.

## Tests

Valid write forwarded; smuggled second sequence stripped; embedded ESC aborts; query form dropped; oversize dropped; split across chunks identical.
