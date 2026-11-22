<!-- Example output of the pr-review router on a real external-contributor PR (static review of the diff only; nothing was built or run; not posted anywhere). -->
Thank you for this contribution. The loopback Studio shows real care: random path token with constant-time compare, Host and Origin checks, request size caps, `no-store` and `Referrer-Policy` headers, `/api/*` disabled for raw previews, and private (0600) persistence through `secure_fs`.

**What is good**
- No new dependencies, no workflow or manifest changes, and no outbound network calls from the application itself.
- The five commits are cleanly named and mostly map to separable topics.
- The Studio page escapes HTML before rendering Markdown, and review-pin coordinates are digit-only, so no script injection path was found there.
- The hand-written HTTP parser rejects `Transfer-Encoding`, duplicate `Content-Length`, and oversized heads and bodies, so no request-smuggling path was found.
- Unit and integration tests accompany the HTTP parser and the artifact model.

**Lenses run:** hygiene, egress and telemetry, privilege and writes, core correctness. **Skipped:** dependency audit (no manifest or lockfile change), CI hardening (no workflow change). Static review of the diff at the head SHA below; nothing from the PR was built or executed.

**Changes requested** (each ID is re-checked automatically on the next push)

1. **`EGR-studio-iframe-open-network`: Studio preview iframe can reach the network** (high, blocking) at `src/editor/studio_web.rs:541`
   - Why: `sandbox="allow-scripts"` isolates the origin but not the network. Artifact content is writable by other agents over the context bus, so a script in an artifact can `fetch` or beacon its content anywhere.
   - How to fix: set a CSP on the `srcdoc` (`<meta http-equiv="Content-Security-Policy" ...>` inside the document, or `csp` attribute): `default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'`. Make network access an explicit opt-in.
   - How we will verify: a test asserts the served page and iframe document carry `connect-src 'none'`.
2. **`EGR-raw-preview-csp-open-network`: raw HTML/SVG preview has no network restriction** (high, blocking) at `src/editor/preview.rs:579`
   - Why: the header is only `Content-Security-Policy: sandbox allow-scripts`.
   - How to fix: `sandbox allow-scripts; default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'`. Consider `frame-ancestors 'none'` and `Cross-Origin-Resource-Policy: same-origin` on the Studio page.
   - How we will verify: a header test for both responses; `rg -n "Content-Security-Policy" src/editor/preview.rs` shows `connect-src 'none'`.
3. **`PRV-preview-url-token-in-replies`: access token is placed in replies and status text** (high, blocking) at `src/wm/editor_pane.rs:314` (also `:377`)
   - Why: the full `http://127.0.0.1:PORT/<token>/` URL appears in RPC/MCP reply fields and editor messages, so it can reach logs, agent transcripts and recordings. On a shared machine any local user can reach loopback, so the token is the only barrier.
   - How to fix: return and display a redacted URL by default; give the full URL only to the component that opens it. Optionally exchange a one-time `?t=` for an HttpOnly cookie and redirect to a token-free path.
   - How we will verify: tests assert reply `url` fields and messages do not contain the token; `rg -n "format!.*\{url\}" src/wm/editor_pane.rs` shows no reply-bound full URLs.
4. **`PRV-mcp-resources-expose-all-keys`: MCP resources list and read every ContextBus key** (medium, blocking) at `src/api/mcp_resources.rs:61`
   - Why: `list(None)` and `get(ctx_key)` expose all keys with full values and no size cap, not only `artifact:` entries.
   - How to fix: restrict to the `artifact:` prefix (or document and gate the rest), cap returned size, and keep it read-only.
   - How we will verify: a test that a non-artifact key is absent from `resources/list` and rejected by `resources/read`, and an oversized value is truncated or refused.
5. **`RES-preview-serve-loop-serial`: one slow connection stalls the server** (medium, blocking) at `src/editor/preview.rs:634`
   - Why: connections are handled inline; each idle speculative connection can hold the loop up to the 2 s deadline, stalling the 1.2 s Studio polling. `Drop` only sets a flag and never joins.
   - How to fix: serve each connection on a bounded short-lived worker, or shrink the per-connection deadline; join with a bounded wait on `Drop` or document the detach.
   - How we will verify: a test where a stalled client does not block a second request.
6. **`COR-studio-save-clobbers-concurrent-edit`: Studio save ignores revisions** (medium, blocking) at `src/editor/preview.rs:436`
   - Why: `bus.set(key, text, None)` overwrites a newer agent edit silently.
   - How to fix: send the last-seen revision from the page, pass it as the expected revision, and return a conflict the UI shows.
   - How we will verify: a test saving with a stale revision returns a conflict and leaves the newer text.
7. **`HYG-bundled-features`: five independent changes in one PR** (medium, blocking)
   - Why: 35 files, about 3.6k added lines: GUI resize fix, framed texture fix, MCP resources, artifacts plus Studio plus preview server, TUI pixel rendering. Security-sensitive code is mixed with unrelated display fixes.
   - How to fix: split as in `split_proposal` below; the existing commit boundaries are a good guide.
   - How we will verify: each sub-PR touches only its listed paths.
8. **`HYG-gate-evidence-incomplete`: project gate not run** (medium, blocking)
   - Why: the description says `scripts/verify.sh` was not run (macOS only, targeted clippy and tests instead) and lists "Merge preconditions: None". Linux and Windows results are not stated.
   - How to fix: run the full gate on the rebased head, or name each skipped stage and why, and include Linux evidence.
   - How we will verify: the description cites the gate output for the new head SHA.
9. **`CMP-tui-pixel-default-on-unthemed`: pixel graphics on by default, ignoring the pane theme** (medium, blocking) at `src/ui/tui_media_gfx.rs:34`
   - Why: Kitty or iTerm2 output is enabled from environment variables alone, which is unreliable over ssh and tmux. The pixel path adds no theme mapping, while main maps page lightness through `themed_pixel`, so users who rely on theme-following lose it.
   - How to fix: default to half-block; enable pixels via config or `BILTERM_BROWSER_GFX`; apply the theme remap to pixel frames.
   - How we will verify: a unit test that default detection returns half-block without an override, and a test that pixel frames pass through the theme mapping.
10. **`PRV-bcrypt-unsafe-no-safety-comment`: `unsafe` FFI block lacks a safety justification** (medium, non-blocking) at `src/editor/preview.rs:72`
    - Why: the signature looks correct, but the invariants are not stated and the Windows path is unverified.
    - How to fix: add `// SAFETY:` naming the buffer, length and flags invariants; confirm windows-msvc x64 and ARM64 builds.
    - How we will verify: `rg -n -B2 "unsafe \{" src/editor/preview.rs` shows a `SAFETY` comment.
11. **`ARC-duplicate-token-generator`: second CSPRNG token function** (low, non-blocking) at `src/editor/preview.rs:52`
    - Why: duplicates `generate_http_token` in `src/api/http.rs`.
    - How to fix: move one implementation into `secure_fs` and use it from both; check the token before binding the listener.
    - How we will verify: `rg -n "fn generate_.*token" src/` returns one definition.
12. **`COR-persist-errors-ignored`: persistence failures are silent** (low, non-blocking) at `src/editor/preview.rs:385`
    - Why: `let _ = write_private_file(...)` hides failed saves.
    - How to fix: surface the error to the UI or log it.
    - How we will verify: a test with an unwritable directory reports an error.
13. **`PRV-host-allows-localhost`: Host allow-list accepts the name `localhost`** (low, non-blocking) at `src/editor/preview.rs:202`
    - Why: with the token this is acceptable; literal `127.0.0.1` and `[::1]` are tighter against rebinding.
    - How to fix: accept only literal loopback addresses.
    - How we will verify: a test that `Host: localhost:PORT` is refused.
14. **`TST-missing-csp-and-stall-tests`: no tests for CSP headers or stalled clients** (low, non-blocking)
    - Why: the new defenses in items 1, 2 and 5 need regression tests.
    - How to fix: add them with those fixes.
    - How we will verify: the named tests exist and pass in the gate.
15. **`HYG-mcp-commit-not-self-contained`: commit does not build on its own** (low, non-blocking) at `src/api/mcp_resources.rs:62`
    - Why: commit `af77acc` uses `crate::editor::artifact::ARTIFACT_KEY_PREFIX`, which first appears in `4fb23ed`, so history is not bisectable and the MCP piece cannot be a standalone PR yet.
    - How to fix: order it after the artifacts PR, as in the proposal.
    - How we will verify: `git rebase --exec "cargo check --lib" BASE` passes for every commit.
16. **`HYG-stale-base`: branch is behind main** (low, non-blocking)
    - Why: the PR base is 4 commits behind current main.
    - How to fix: rebase onto main and re-run the gate.
    - How we will verify: `mergeStateStatus` is clean and the head is rebased.

**Questions**
- `Q-tui-pixel-multiplexers`: has the pixel path been tried under tmux, over ssh, and on WezTerm, and what happens to a stale image if the terminal ignores the delete sequence?
- `Q-mcp-resources-scope`: is exposing non-artifact ContextBus keys intended, and are values meant to be size-capped?
- `Q-windows-bcrypt-run`: has the `BCryptGenRandom` path been built and run on Windows (x64 and ARM64)?
- `Q-gate-linux`: can the full `scripts/verify.sh` be run on Linux, or which stages cannot run on your machine?

**Next steps**
1. Split into the sub-PRs proposed in the block below; start with the two display fixes, which are independent.
2. Address items 1 to 6 in the Studio PR before anything else; they are the blocking security and correctness items.
3. Rebase, run the gate, and cite its output for the new head SHA.
4. Comment here when ready; we will re-run each acceptance check by ID.

Thank you again. This is a large and ambitious feature, and we would be glad to review it in smaller pieces.

```json pr-review/v1
{
  "schema": "pr-review/v1",
  "pr": {"repo": "bsommers/bilterm", "number": 169},
  "head_sha": "dfe685fc16a3c0e4cca6ab040c2d225eb38fc52d",
  "verdict": "changes_requested",
  "summary": "Well-built loopback Studio, but bundles five features; preview content can reach the network, the access token is echoed in replies, MCP exposes all bus keys, and the gate was not run.",
  "skills_run": ["pr-review", "reviewing-pr-hygiene", "reviewing-code-security", "auditing-egress-and-telemetry", "auditing-privilege-and-writes"],
  "split_proposal": [
    {"title": "fix(gui): resize guard and framed browser texture alignment", "paths": ["src/ui/gui_font/linux_x11.rs", "src/ui/gui_macos.rs", "src/ui/gui_window.rs", "src/ui/renderer.rs"]},
    {"title": "feat(editor): shared artifacts and editor integration", "paths": ["src/editor/artifact.rs", "src/editor/mod.rs", "src/wm/editor_pane.rs", "src/wm/editor_menu.rs", "src/cli/editor_cmd.rs", "src/api/rpc*.rs", "tests/editor_surface_parity.rs"]},
    {"title": "feat(editor): loopback Artifact Studio and preview server", "paths": ["src/editor/preview.rs", "src/editor/studio_web.rs"], "depends_on": ["feat(editor): shared artifacts and editor integration"]},
    {"title": "feat(api): scoped ContextBus artifact resources over MCP", "paths": ["src/api/mcp_resources.rs", "src/api/mcp.rs"], "depends_on": ["feat(editor): shared artifacts and editor integration"]},
    {"title": "feat(ui): opt-in TUI pixel rendering with theme mapping", "paths": ["src/ui/tui_media_gfx.rs", "src/ui/mod.rs", "src/app.rs", "src/colon_command/execute_media.rs", "tests/browser_gui_surface.rs"]}
  ],
  "findings": [
    {"id": "EGR-studio-iframe-open-network", "category": "egress", "severity": "high", "file": "src/editor/studio_web.rs", "line": 541, "evidence": "iframe sandbox=\"allow-scripts\" with srcdoc set from artifact HTML; no CSP, so connect-src is unrestricted", "required_change": "Apply a CSP with connect-src 'none' to the srcdoc document; make network access opt-in.", "acceptance_check": "test asserts the iframe document carries connect-src 'none'", "blocking": true, "confidence": "high", "cwe": "CWE-1021"},
    {"id": "EGR-raw-preview-csp-open-network", "category": "egress", "severity": "high", "file": "src/editor/preview.rs", "line": 579, "evidence": "raw HTML/SVG served with only 'Content-Security-Policy: sandbox allow-scripts'", "required_change": "Add default-src 'none'; script-src and style-src 'unsafe-inline'; img-src data:; connect-src 'none' while keeping sandbox.", "acceptance_check": "header test passes; rg -n \"connect-src 'none'\" src/editor/preview.rs matches", "blocking": true, "confidence": "high", "cwe": "CWE-693"},
    {"id": "PRV-preview-url-token-in-replies", "category": "privilege", "severity": "high", "file": "src/wm/editor_pane.rs", "line": 314, "evidence": "full loopback URL with access token is placed in RPC reply url fields and status messages (also line 377)", "required_change": "Redact the token in replies and messages by default; expose the full URL only to the opener.", "acceptance_check": "tests assert reply url fields and messages do not contain the token", "blocking": true, "confidence": "high", "cwe": "CWE-532"},
    {"id": "PRV-mcp-resources-expose-all-keys", "category": "privilege", "severity": "medium", "file": "src/api/mcp_resources.rs", "line": 61, "evidence": "context_bus().list(None) and get(ctx_key) expose every key and full value, no size cap", "required_change": "Limit to the artifact: prefix, cap value size, keep read-only.", "acceptance_check": "test: non-artifact key absent from resources/list and refused by resources/read; oversized value refused", "blocking": true, "confidence": "high", "cwe": "CWE-200"},
    {"id": "RES-preview-serve-loop-serial", "category": "resource-bounds", "severity": "medium", "file": "src/editor/preview.rs", "line": 634, "evidence": "serve_loop handles each accepted connection inline with a 2 s request deadline; Drop sets a flag without joining", "required_change": "Serve connections on bounded worker threads or shorten the deadline; bounded join on Drop.", "acceptance_check": "test: a stalled client does not block a second request", "blocking": true, "confidence": "high", "cwe": "CWE-400"},
    {"id": "COR-studio-save-clobbers-concurrent-edit", "category": "correctness", "severity": "medium", "file": "src/editor/preview.rs", "line": 436, "evidence": "bus.set(key, text, None) passes no expected revision", "required_change": "Send last-seen revision from the page, pass it as expected, return a conflict the UI shows.", "acceptance_check": "test: save with stale revision returns conflict and keeps newer text", "blocking": true, "confidence": "high"},
    {"id": "HYG-bundled-features", "category": "hygiene", "severity": "medium", "file": null, "line": null, "evidence": "35 files, +3634/-129, five independent topics in five commits, security-sensitive server mixed with display fixes", "required_change": "Split into the sub-PRs in split_proposal.", "acceptance_check": "each sub-PR touches only its listed paths", "blocking": true, "confidence": "high"},
    {"id": "HYG-gate-evidence-incomplete", "category": "hygiene", "severity": "medium", "file": null, "line": null, "evidence": "PR body states scripts/verify.sh was not run, macOS only, with Merge preconditions: None", "required_change": "Run the full gate on the rebased head, or name each skipped stage with a reason; include Linux evidence.", "acceptance_check": "description cites gate output for the new head SHA", "blocking": true, "confidence": "high"},
    {"id": "CMP-tui-pixel-default-on-unthemed", "category": "compat", "severity": "medium", "file": "src/ui/tui_media_gfx.rs", "line": 34, "evidence": "detect_from_env enables Kitty/iTerm2 from env vars by default; no theme mapping in the pixel path, while main applies themed_pixel", "required_change": "Default to half-block; opt in via config or BILTERM_BROWSER_GFX; apply the theme remap to pixel frames.", "acceptance_check": "unit tests: default detection is half-block; pixel frames pass through the theme mapping", "blocking": true, "confidence": "medium"},
    {"id": "PRV-bcrypt-unsafe-no-safety-comment", "category": "privilege", "severity": "medium", "file": "src/editor/preview.rs", "line": 72, "evidence": "unsafe FFI call to BCryptGenRandom without a SAFETY justification; Windows build unverified", "required_change": "Add a SAFETY comment stating buffer, length and flag invariants; confirm windows-msvc x64 and ARM64 builds.", "acceptance_check": "rg -n -B2 'unsafe \\{' src/editor/preview.rs shows a SAFETY comment", "blocking": false, "confidence": "high"},
    {"id": "ARC-duplicate-token-generator", "category": "architecture", "severity": "low", "file": "src/editor/preview.rs", "line": 52, "evidence": "generate_preview_token duplicates generate_http_token in src/api/http.rs", "required_change": "Share one implementation via secure_fs; check the token before binding the listener.", "acceptance_check": "rg -n 'fn generate_.*token' src/ returns one definition", "blocking": false, "confidence": "high"},
    {"id": "COR-persist-errors-ignored", "category": "correctness", "severity": "low", "file": "src/editor/preview.rs", "line": 385, "evidence": "let _ = write_private_file(...) discards persistence errors", "required_change": "Report or log the failure.", "acceptance_check": "test: unwritable directory yields an error report", "blocking": false, "confidence": "high"},
    {"id": "PRV-host-allows-localhost", "category": "privilege", "severity": "low", "file": "src/editor/preview.rs", "line": 202, "evidence": "is_loopback_host accepts the name localhost", "required_change": "Accept only literal loopback addresses.", "acceptance_check": "test: Host: localhost:PORT is refused", "blocking": false, "confidence": "high"},
    {"id": "TST-missing-csp-and-stall-tests", "category": "tests", "severity": "low", "file": null, "line": null, "evidence": "no tests cover CSP headers or a stalled client", "required_change": "Add tests with the fixes for items 1, 2 and 5.", "acceptance_check": "the named tests exist and pass in the gate", "blocking": false, "confidence": "high"},
    {"id": "HYG-mcp-commit-not-self-contained", "category": "hygiene", "severity": "low", "file": "src/api/mcp_resources.rs", "line": 62, "evidence": "commit af77acc references crate::editor::artifact::ARTIFACT_KEY_PREFIX introduced in 4fb23ed; absent on main", "required_change": "Order the MCP change after the artifacts PR.", "acceptance_check": "git rebase --exec 'cargo check --lib' BASE passes for every commit", "blocking": false, "confidence": "medium"},
    {"id": "HYG-stale-base", "category": "hygiene", "severity": "low", "file": null, "line": null, "evidence": "PR base is 4 commits behind current main", "required_change": "Rebase onto main and re-run the gate.", "acceptance_check": "mergeStateStatus is clean after rebase", "blocking": false, "confidence": "high"}
  ],
  "questions": [
    {"id": "Q-tui-pixel-multiplexers", "text": "Has the pixel path been tried under tmux, over ssh and on WezTerm, and what happens to a stale image if the terminal ignores the delete sequence?"},
    {"id": "Q-mcp-resources-scope", "text": "Is exposing non-artifact ContextBus keys intended, and should values be size-capped?"},
    {"id": "Q-windows-bcrypt-run", "text": "Has the BCryptGenRandom path been built and run on Windows x64 and ARM64?"},
    {"id": "Q-gate-linux", "text": "Can the full scripts/verify.sh run on Linux, or which stages cannot run on your machine?"}
  ]
}
```
