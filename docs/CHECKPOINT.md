# Checkpoint — 52 Skills Suite, Installers & Onboarding Skill — 2026-10-24

**Status:** COMPLETE (Verified & Synced)  
**Branch:** `main`  
**Working Tree:** Clean  

---

## 1. Goal & Context
Maintain and verify the 52-skill `swe-skills` engineering library across Claude Code, Antigravity (`agy`), and Cursor, including `building-installers-and-onboarding`, adaptive model routing, Nix environment templates, 7-chapter user manual, context-guard hooks, and synchronized local installations.

---

## 2. Done (With Evidence)
- **Suite Expansion (52 Skills)**:
  - `skills/building-installers-and-onboarding/SKILL.md`: Added multi-target installer standard (`--local`, `--global`, `--prefix`), idempotent `<tool> init` / `doctor` setup, progressive `Next steps:` CLI breadcrumbs, and companion templates (`references/installer-template.sh`, `references/onboarding-cli-patterns.md`).
  - `skills/adaptive-model-routing/SKILL.md`: Added test-time compute heuristics, Flash-High guidance, lifecycle hook (`scripts/hooks/model_router.py`), subagent templates (`templates/subagents/`), and OpenGSD profile (`templates/opengsd/adaptive-model-profile.json`).
  - `skills/nix-environments/SKILL.md`: Added Nix flake/shell reproducibility guidance and `templates/nix/` (`flake.nix`, `shell.nix`, `envrc`).
  - `skills/token-finops/SKILL.md`: Frontier model rate table ($/MTok), token budgeting, provider caching rules, and `/eng finops` shortcut.
- **Documentation & Licensing**:
  - `docs/usermanual/`: Added 7-chapter user manual, SVG vector banner (`docs/assets/logo.svg`), terminal ASCII banner (`docs/assets/banner.txt`), and `scripts/banner.sh`.
  - `docs/EVIDENCE.md`: Decoupled external references for clean standalone provenance.
  - `LICENSE`: Updated repository and plugin manifests to `Apache-2.0`.
- **Hooks & Context Guards**:
  - `scripts/hooks/context_guard.py`: Added `agy` `PreInvocation` context-guard support and tailored `/compact` recommendations.
  - `scripts/hooks/model_router.py`: Added heuristic model-tier routing hook with 18 unit tests.
- **Multi-Platform Deployment & Distribution**:
  - Symlinks synchronized in `~/.claude/skills`, `~/.cursor/skills`, and `~/.agents/skills` (all 52 skills active via `scripts/install.sh --all`).
- **Test & Lint Verification**:
  - `python3 scripts/lint-skills.py --words` → 52 skills, 25,299 words total, 0 errors (1 soft warn on `token-finops` at 1,002 words).
  - `python3 -m unittest discover tests` → 55 tests passing.
  - `python3 scripts/eval-router.py --self-test` → Accuracy 10/10 (100.0%) PASS.
  - `python3 scripts/run-scenarios.py --dry-run` → all 55 scenarios map to valid, existing skills.

---

## 3. Failed / Blocked
- None. All validations green.

---

## 4. State That May Have Changed
- Local symlinks in `~/.cursor/skills`, `~/.agents/skills`, and `~/.claude/skills` point to `~/src/swe-skills-2/skills/` (all 52 skills linked).
- Antigravity plugin `swe-skills` active with 52 skills and 1 hook.

---

## 5. Next Steps
1. Verify repository state:
   ```bash
   git status -sb && python3 -m unittest discover tests && python3 scripts/lint-skills.py --words
   ```
2. Optional maintenance: extract reference tables from `skills/token-finops/SKILL.md` (1,002 words) into `skills/token-finops/references/` to clear the `> 900` word warning.
3. Downstream project onboarding: integrate `templates/AGENTS.snippet.md` into target repositories.
4. Dogfood newly integrated skills (`adaptive-model-routing`, `nix-environments`, `token-finops`, `code-architecture-review`, `test-coverage`) on active codebases.
