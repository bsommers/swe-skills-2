# Chapter 5: Authoring & Extending Skills

[← Back to User Manual](README.md) · [← Previous: Workflows & Recipes](04-workflows-and-recipes.md) · [Next: CLI & Script Reference →](06-reference-and-cli.md)

This chapter provides the specification and quality criteria for contributing new engineering skills to `swe-skills`.

---

## Skill Specification & Frontmatter Standard

Every skill lives in its own directory under `skills/<name>/` and contains a mandatory [`SKILL.md`](../../skills/using-swe-skills/SKILL.md) entry point.

### Directory Structure
```text
skills/<name>/
├── SKILL.md                 # Primary instruction file (required)
├── references/              # Reference tables, matrices, checklists (>500 words)
├── templates/               # Reusable file templates or schemas
└── scripts/                 # Standalone helper scripts
```

### Frontmatter Standard
The YAML frontmatter must contain **only** `name` and `description`:

```yaml
---
name: my-new-skill
description: Use when [specific triggering conditions], when [symptom occurs], or before [sensitive operation].
---
```

#### Authoring Rules for Frontmatter
1. **Triggers Only:** The description must state **when** to activate the skill, never the step-by-step workflow. (Describing the process in the description causes LLMs to attempt execution without loading the full skill).
2. **Third-Person Phrasing:** Always begin with `"Use when..."`.
3. **Character Cap:** Maximum 1024 characters; strongly prefer ≤ 500 characters.
4. **Exact Match:** The `name` field must match the directory name exactly.

---

## Word Budgets and Reference Splitting

- **Core Body Target:** ≤ 500 words.
- **Tone:** Imperative, concise, highly structured rules and mistakes.
- **Reference Splitting:** If deep reference material (such as syntax tables, price sheets, or complex schemas) exceeds the budget, place it inside `skills/<name>/references/<topic>.md`.
- **Cross-References:** Cross-reference other skills using `` `other-skill` ``. The linter automatically verifies that referenced skills exist.

---

## Step-by-Step Guide to Adding a Skill

Adding a skill requires updates across several synchronized documents to ensure discovery, validation, and provenance.

### 1. Create the Skill Directory & Entry Point
```bash
mkdir -p skills/my-new-skill
```
Create `skills/my-new-skill/SKILL.md` following the template below:

```markdown
---
name: my-new-skill
description: Use when encountering X, when debugging Y, or before modifying Z.
---

# My New Skill

## Overview
Brief explanation of failure modes this skill prevents.

## Rules
1. **Rule one title.** Imperative guidance.
2. **Rule two title.** Imperative guidance.

## Mistakes to Avoid
- Anti-pattern 1.
- Anti-pattern 2.
```

### 2. Register in the Router (`using-swe-skills`)
Add a routing row to [`skills/using-swe-skills/SKILL.md`](../../skills/using-swe-skills/SKILL.md) in the relevant category table:
```markdown
| perform action X | `my-new-skill` |
```

### 3. Register `/eng` Shortcut (Optional)
If the skill merits a fast 1-word shortcut, add it to [`skills/eng/SKILL.md`](../../skills/eng/SKILL.md):
```markdown
| `shortcut` | `my-new-skill` |
```

### 4. Document Provenance in `docs/EVIDENCE.md`
Add a row to [`docs/EVIDENCE.md`](../EVIDENCE.md) identifying the historical incidents or projects that justified the skill.

### 5. Add Scenario to `docs/TESTING.md`
Add a pressure scenario to [`docs/TESTING.md`](../TESTING.md) specifying a realistic user prompt and expected agent behaviors.

### 6. Update `README.md`
Increment the skill count (e.g. `Skills (51)`) and list `my-new-skill` under the appropriate functional category in the main table.

---

## Validation Gates & Skill Linter

Before committing any skill, run the automated validation suite locally:

```bash
# 1. Run the skill linter (frontmatter, cross-refs, word caps)
python3 scripts/lint-skills.py --words

# 2. Validate router evaluation suite
python3 scripts/eval-router.py --self-test

# 3. Validate pressure test scenarios
python3 scripts/run-scenarios.py --dry-run

# 4. Validate Antigravity plugin manifest
agy plugin validate .

# 5. Run unit tests
python3 -m unittest discover tests
```

All commands must exit with code 0 (`OK`).

---

## Common Authoring Mistakes

| Anti-Pattern | Why It Fails | Remedy |
|---|---|---|
| **Process in description** | LLM executes from description without loading body. | Describe triggers only ("Use when..."). |
| **Bloated body (> 900 words)** | Consumes excessive context window on every load. | Split details into `references/`. |
| **Absolute machine paths** | Breaks on other machines; rejected by pre-commit. | Use repo-relative paths (`src/...`). |
| **Invented cross-references** | Typos in skill links confuse agents. | Run `lint-skills.py` to check link targets. |
| **Missing provenance** | Unverifiable opinions creep into library. | Document real incidents in `docs/EVIDENCE.md`. |
