# Chapter 7: Troubleshooting & FAQ

[← Back to User Manual](README.md) · [← Previous: CLI & Script Reference](06-reference-and-cli.md)

This chapter addresses common operational questions, error symptoms, and diagnostics across supported environments.

---

## Agent Over-Discovery / Loading Too Many Skills

### Symptom
An agent loads 5 or more skills at the start of a conversation, consuming excessive context tokens before answering the user prompt.

### Cause
The agent attempted to match every mentioned concept rather than routing through [`using-swe-skills`](../../skills/using-swe-skills/SKILL.md), or prompt instructions lacked scoping boundaries.

### Remedy
1. Instruct the agent to start with `/eng` or `using-swe-skills`:
   ```text
   /eng [your task]
   ```
2. In custom prompt instructions or agent context files, enforce a 3-skill loading ceiling:
   ```markdown
   Load at most 1–3 swe-skills per task. When unsure, load `using-swe-skills` first.
   ```

---

## Compaction Blocked or Stalled

### Symptom
Claude Code aborts a `/compact` command with:
```text
[context guard] Compaction blocked: no fresh checkpoint found in docs/plans/*checkpoint*.md or docs/CHECKPOINT.md.
```

### Cause
The `PreCompact` hook intercepted a manual `/compact` call, but no checkpoint file was touched within `SWE_SKILLS_CHECKPOINT_FRESH_MINUTES` (default 20 minutes).

### Remedy
1. Ask the agent to write a checkpoint:
   ```text
   Write a checkpoint to docs/CHECKPOINT.md following compacting-context-safely.
   ```
2. Once the checkpoint is written, re-run `/compact`.
3. To temporarily bypass blocking (e.g. in emergency recovery):
   ```bash
   export SWE_SKILLS_CONTEXT_GUARD_BLOCK=0
   ```

---

## Antigravity Plugin Not Registering Hooks

### Symptom
Antigravity executes skills properly, but `PreInvocation` or `SessionStart` hooks do not trigger.

### Cause
Antigravity caches plugin component manifests. Installing over an existing import updates files on disk, but does not re-register component types if `hooks.json` was added after initial installation.

### Remedy
Re-import the plugin:
```bash
python3 scripts/hooks/install-hooks.py --agy
agy plugin uninstall swe-skills
agy plugin install .
```
Verify registration with `agy plugin list`:
```json
{
  "name": "swe-skills",
  "components": ["skills", "hooks"]
}
```

---

## Pre-Commit Hook Rejections

### Symptom
`git commit` fails with:
```text
PRE-COMMIT VERIFICATION FAILED:
  - Absolute home directory path found in docs/MY_DOC.md: /root/...
```

### Cause
[`scripts/hooks/git_pre_commit.py`](../../scripts/hooks/git_pre_commit.py) enforces repository portability. Hardcoded user home directories break when cloned by other developers or CI runners.

### Remedy
1. Replace absolute machine paths with relative paths (`docs/...`, `scripts/...`) or home placeholders (`~` or `$HOME`).
2. If the commit failed due to manifest version mismatch:
   Check `plugin.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `.claude-plugin/marketplace.json`. Ensure all `version` fields match identically.

---

## Symlinks vs Standalone Copies

### Question
Should I install with symlinks (default) or standalone copies (`--copy`)?

### Answer
- **Use Symlinks (Default):** For local development environments where you want `git pull` in `swe-skills-2` to update your agent tools immediately across Claude Code, Cursor, and Antigravity.
- **Use Copies (`--copy`):** For remote development containers, air-gapped systems, or when deploying to shared servers where the source clone may not remain permanently mounted.

```bash
# Standalone copy mode:
scripts/install.sh --all --copy --force
```

---

## Frequently Asked Questions

### Q: Why is this repository called `swe-skills-2` instead of `swe-skills`?
**A:** `swe-skills-2` is a ground-up architectural rewrite featuring discovery-only frontmatter (≤1024 chars), strict word budgets (≤500 words), modular user manuals, and multi-runtime hook integrations. It co-exists cleanly alongside legacy v1 installations without command namespace collisions (using `/eng` instead of `/swe`).

### Q: Can I use `swe-skills` with models other than Claude 3.7 or Claude 3.5 Sonnet?
**A:** Yes. All skills are tested across frontier LLMs (Claude Opus/Sonnet, Gemini 1.5/2.0 Pro/Flash, OpenAI GPT-4o, and DeepSeek-R1). Frontmatter triggers are designed for standard semantic matching engines.

### Q: How do I test the skills without breaking my working tree?
**A:** Use isolated git worktrees or branches. Refer to [`orchestrating-subagents`](../../skills/orchestrating-subagents/SKILL.md) for step-by-step guidance on setting up isolated parallel worktrees.
