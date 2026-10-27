# Super-Permissive Agent Autonomy & Permissions Guide (`Linux` & `macOS`)

> **Reference:** Also available on-demand inside [`skills/supervising-autonomous-sessions/references/agent-autonomy-and-permissions.md`](../skills/supervising-autonomous-sessions/references/agent-autonomy-and-permissions.md).

Drop-in configuration templates for running **Antigravity (`agy` / Antigravity 2.0)**, **Claude Code**, and **OpenGSD** in Gear 3 ("Lights-Out" / zero-prompt autonomous mode), distilled from 770+ real-world session command approvals across `swe-skills`, `bilterm`, `flowscope`, `OntoLogic`, and `maiors`.

---

## 1. Why Agents Still Prompt After Hundreds of "Always Allow" Approvals

1. **Over-Specific Literal Command Approvals**:
   - Clicking *"Always allow"* in a prompt dialog often records the exact argument string (e.g., `"command(cargo clippy -q --all-features --all-targets -- -D warnings)"`).
   - Any flag variation (`--test <suite>` or omitting `--all-features`) misses the literal match and prompts again.
2. **Compound Shell Pipelines (`&&`, `||`, `;`, `|`)**:
   - A compound command such as `shopt -s globstar && awk 'ENDFILE { ... }' src/**/*.rs` evaluates every segment. Missing shell builtins (`shopt`, `awk`, `sed`, `true`, `env`) trigger prompts even when the primary compiler is allowed.
3. **Subagent Inheritance**:
   - Parallel subagents (`invoke_subagent`) evaluate shell commands against the same host permission policy.

---

## 2. Antigravity CLI (`agy`) & Antigravity 2.0 (`~/.gemini/antigravity-cli/settings.json`)

```json
{
  "allowNonWorkspaceAccess": true,
  "toolExecutionPolicy": "always-proceed",
  "artifactReviewMode": "always-proceed",
  "nonWorkspaceFileAccess": "allow",
  "internetAccessPolicy": "allow",
  "permissions": {
    "allow": [
      "command(.*)",
      "command(cargo)",
      "command(rustc)",
      "command(rustup)",
      "command(git)",
      "command(gh)",
      "command(shopt)",
      "command(awk)",
      "command(sed)",
      "command(rg)",
      "command(grep)",
      "command(find)",
      "command(ls)",
      "command(cat)",
      "command(head)",
      "command(tail)",
      "command(sort)",
      "command(wc)",
      "command(diff)",
      "command(sha256sum)",
      "command(shasum)",
      "command(install)",
      "command(cp)",
      "command(mv)",
      "command(rm)",
      "command(mkdir)",
      "command(touch)",
      "command(ln)",
      "command(chmod)",
      "command(tar)",
      "command(curl)",
      "command(jq)",
      "command(python3)",
      "command(python)",
      "command(uv)",
      "command(pytest)",
      "command(ruff)",
      "command(node)",
      "command(npm)",
      "command(npx)",
      "command(nix)",
      "command(just)",
      "command(zig)",
      "command(codegraph)",
      "command(graphify)",
      "command(sips)",
      "command(iconutil)",
      "command(codesign)",
      "command(bash)",
      "command(sh)",
      "command(zsh)",
      "command(env)",
      "command(which)",
      "command(pwd)",
      "command(echo)",
      "command(printf)",
      "command(true)",
      "command(test)",
      "command(set)"
    ],
    "deny": [
      "command(rm -rf /)",
      "command(rm -rf ~)",
      "command(git push --force origin main)",
      "command(git reset --hard origin/main)"
    ]
  }
}
```

---

## 3. Claude Code (`.claude/settings.local.json` or `~/.claude/settings.json`)

```json
{
  "env": {
    "SWE_SKILLS_CHECKPOINT_GLOBS": ".planning/CHECKPOINT.md:.planning/STATE.md:docs/plans/*checkpoint*.md:CHECKPOINT.md"
  },
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": [
      "Bash(*)",
      "Read(*)",
      "Edit(*)",
      "Write(*)",
      "MultiEdit(*)",
      "Glob(*)",
      "Grep(*)",
      "LS(*)",
      "Task(*)",
      "WebFetch(*)",
      "WebSearch(*)",
      "mcp__*"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(git push --force origin main)"
    ]
  }
}
```

---

## 4. OpenGSD Autonomous Workflow (`.planning/config.json`)

```json
{
  "mode": "yolo",
  "parallelization": true,
  "commit_docs": true,
  "workflow": {
    "auto_advance": true,
    "skip_discuss": true,
    "human_verify_mode": "none",
    "use_worktrees": false
  }
}
```

---

## 5. Agent Command Hygiene Rules to Prevent Prompt Fallbacks

1. **Use Native File Tools Over Shell Redirection**: Always use `read_file`, `edit_file`, and `write_file` instead of `cat << 'EOF'` or `sed -i`.
2. **Lead with Allowlisted Binary Names**: Avoid leading with inline shell assignments (`FOO=1 cargo test`); either pass flags or prefix with `env FOO=1` when `command(env)` is allowlisted.
3. **Use Native Timers Over Shell `sleep`**: Use the native `schedule` tool for polling rather than `sleep 30 && gh pr list`.
