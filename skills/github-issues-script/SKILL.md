---
name: github-issues-script
description: Use when converting a list of findings, review items, architectural gaps, or bug reports into a structured, reviewable batch script (using gh issue create) with exact file coordinates, impact analysis, and proper labels.
---

# GitHub Issues Script Generator Skill

An agent skill to transform code review findings, architectural debt, security vulnerabilities, or task backlogs into a standalone, human-reviewable executable script (e.g. `scripts/create_issues.sh`) that automates creating production-quality GitHub issues via the GitHub CLI (`gh`).

---

## Agent Detection & Mode Tuning

| Agent / Environment | Recommended Workflow |
| :--- | :--- |
| **Antigravity (`agy`)** | Parse findings from memory or workspace artifacts (`docs/ARCHITECTURE_REVIEW.md`, `docs/IMPROVEMENT_PLAN.md`), write the output script with `write_to_file`, and display an interactive preview artifact. |
| **Claude Code** | Parse `$ARGUMENTS` (e.g. `/github-issues-script docs/IMPROVEMENT_PLAN.md` or from chat context), generate the script in `scripts/create_issues.sh`, and offer to execute a dry-run. |
| **Cursor** | Generate the script in the repository, allowing users to inspect it in the editor and run from Cursor's integrated terminal. |
| **Universal AI Agents** | Standardized POSIX shell generation utilizing robust heredocs to prevent escaping issues. |

---

## Issue Quality & Anatomy Best Practices

Every generated issue must adhere to industry-standard GitHub issue formatting:

```markdown
### 📋 Summary & Nature of Issue
Concise description of the problem, architectural smell, bug, or technical debt.

### 📍 Coordinates & Location
- **File:** [`src/core/auth/session.ts`](file:///absolute/path/or/relative/path)
- **Lines:** `L45-L89`
- **Git Permalink / Target Component:** `Core Auth Module (SessionStore)`

### ⚠️ Why It's a Problem (Impact & Risk)
- **Root Cause:** Explanation of why the code is structured poorly or failing.
- **Blast Radius:** Modules or user flows affected.
- **Technical / Security Impact:** Performance degradation, memory leaks, security vulnerability, or maintenance blocker.

### 🛠️ Recommended Remediation
Step-by-step actionable guide or code transformation to resolve the issue:
```language
// ❌ Before
...
// ✅ Recommended Fix
...
```

### 🔗 References & Assets
- Documentation, ADR links, or related issues.
```

---

## Workflow Steps

```mermaid
flowchart TD
    Start(["Input: Findings / Improvement Plan / Backlog"]) --> Parse["1. Parse & Categorize Issues (Type, Severity, Labels)"]
    Parse --> ResolveCoords["2. Resolve Exact File Coordinates & Links"]
    ResolveCoords --> CraftMarkdown["3. Draft Issue Bodies adhering to Best Practices"]
    CraftMarkdown --> BuildScript["4. Assemble Standalone Batch Script (create_issues.sh)"]
    BuildScript --> ReviewPrompt["5. Present Script & Markdown for User Review"]
    ReviewPrompt --> ManualRun(["User Reviews and Manually Executes Script"])
```

---

## Step 1: Ingest & Categorize Findings

Ingest findings from:
1. An existing improvement plan (e.g. `docs/ARCHITECTURE_REVIEW.md`, `.planning/reviews/`, `BACKLOG.md`)
2. Output from `/code-architecture-review`, `/security-scan`, or test suite
3. Direct user prompt / conversational instructions

For each finding, extract:
- **Title**: Prefixed with a standardized type tag:
  - `[Arch]` - Architectural refactoring / decoupling
  - `[Bug]` - Logic error / runtime defect
  - `[Perf]` - Performance / bottleneck / memory leak
  - `[Security]` - Vulnerability / authorization / validation flaw
  - `[Debt]` - Code smell / typing / maintainability cleanup
  - `[Docs]` - Documentation / specification gap
- **Priority**: `P0` (Critical), `P1` (High), `P2` (Medium), `P3` (Low / Polish)
- **Labels**: e.g., `["architecture", "refactor", "priority:p1"]`
- **Milestone / Project** (Optional)

---

## Step 2: Resolve File Coordinates & Links

Ensure every issue contains exact, verifiable file coordinates:
- Check that the target file exists in the repository.
- Pinpoint specific line ranges (e.g. `src/services/order.ts#L45-L62`).
- Include GitHub-compatible markdown links or relative repository paths.

---

## Step 3: Generate the Standalone Batch Script

Write the batch script to `scripts/create_issues.sh` (or custom path requested by the user).

### Script Requirements:
1. **Safety First**: Must support `--dry-run` to preview all issues without creating them.
2. **Pre-flight Checks**:
   - Verifies `gh` CLI is installed (`command -v gh`).
   - Verifies GitHub authentication (`gh auth status`).
   - Detects the current repository or accepts `--repo owner/name`.
3. **Escaping Integrity**: Uses quoted EOF heredocs (`cat << 'EOF'`) to completely eliminate shell variable expansion and backtick corruption.
4. **Interactive Mode**: Prompts user before each issue or allows batch mode (`--yes` / `--all`).

---

## Reference Template for `scripts/create_issues.sh`

```bash
#!/usr/bin/env bash
#
# scripts/create_issues.sh - Batch GitHub Issue Creator
# Generated by swe-skills github-issues-script
#

set -e

DRY_RUN=false
INTERACTIVE=true
TARGET_REPO=""

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --dry-run      Print issue titles and bodies without creating them"
    echo "  --all, -y      Create all issues automatically without per-issue confirmation"
    echo "  --repo <owner/repo> Override target GitHub repository"
    echo "  -h, --help     Show this help message"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --all|-y) INTERACTIVE=false; shift ;;
        --repo) TARGET_REPO="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

# Pre-flight check
if ! command -v gh >/dev/null 2>&1; then
    echo "Error: GitHub CLI ('gh') is not installed. Install via: brew install gh (macOS) or see https://cli.github.com"
    exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
    echo "Error: GitHub CLI is not authenticated. Please run: gh auth login"
    exit 1
fi

REPO_FLAG=""
if [ -n "$TARGET_REPO" ]; then
    REPO_FLAG="--repo $TARGET_REPO"
fi

create_issue() {
    local title="$1"
    local labels="$2"
    local body="$3"

    echo "========================================================"
    echo "Title:  $title"
    echo "Labels: $labels"
    echo "========================================================"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "$body\n"
        echo "[DRY RUN] Skipped creation."
        echo ""
        return 0
    fi

    if [ "$INTERACTIVE" = true ]; then
        read -r -p "Create this issue? [y/N/q]: " choice
        case "$choice" in
            y|Y) ;;
            q|Q) echo "Aborted."; exit 0 ;;
            *) echo "Skipping issue."; echo ""; return 0 ;;
        esac
    fi

    # Create issue via gh CLI
    gh issue create $REPO_FLAG --title "$title" --label "$labels" --body "$body"
    echo "✓ Issue created."
    echo ""
}

echo "Starting GitHub Issue creation pipeline..."
echo ""

# ------------------------------------------------------------------------------
# Issue Definitions
# ------------------------------------------------------------------------------

# --- ISSUE 1 ---
TITLE_1="[Arch] Decouple Domain Services from Raw Database Client"
LABELS_1="architecture,refactor,priority:p1"
read -r -d '' BODY_1 << 'EOF' || true
### 📋 Summary & Nature of Issue
Domain services currently import database client implementations directly, preventing isolated unit testing and violating the Dependency Inversion Principle.

### 📍 Coordinates & Location
- **File:** `src/services/order.ts`
- **Lines:** `L24-L58`
- **Component:** `OrderProcessingService`

### ⚠️ Why It's a Problem
- **Tight Coupling:** The domain service cannot run in tests without a live PostgreSQL instance.
- **Leaky Database Types:** ORM queries are intermingled with business discount logic.

### 🛠️ Recommended Remediation
Introduce a repository interface (`IOrderRepository`) and inject it into `OrderService` constructor:

```typescript
export interface IOrderRepository {
  getOrder(id: string): Promise<Order>;
  saveOrder(order: Order): Promise<void>;
}
```

### 🔗 References
- Clean Architecture / Ports & Adapters guide
EOF
create_issue "$TITLE_1" "$LABELS_1" "$BODY_1"

echo "All issue tasks processed!"
```

---

## Anti-Patterns to Avoid

1. **Vague Titles**: Never create issues titled `"Fix bug"` or `"Refactor code"`. Always use component-scoped, descriptive titles.
2. **Missing Coordinates**: Never omit exact file paths or line numbers. Reviewers and contributors must know immediately where to look.
3. **No Dry Run**: Never generate a script that executes network mutations without giving the user a chance to inspect or run `--dry-run`.
4. **Shell Quoting Vulnerabilities**: Never use double-quoted strings for multi-line markdown containing code blocks (`$`, backticks, double quotes). Always use quoted heredocs (`<< 'EOF'`).
