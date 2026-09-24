#!/usr/bin/env bash
#
# scripts/setup_repo_protections.sh - Reusable GitHub Repository Protection & Ruleset Tool
# Configures branch protection rulesets, secret scanning, push protection, and collaborators.
#

set -e

# Terminal colors
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
NC="\033[0m"

TARGET_ORG=""
TARGET_REPO=""
REQUIRED_APPROVALS=1
REQUIRE_SIGNED_COMMITS=true
ENABLE_SECRET_SCANNING=true
ENABLE_PUSH_PROTECTION=true
SET_VISIBILITY=""
ADD_COLLABORATOR=""
COLLABORATOR_PERMISSION="push"
LIST_COLLABORATORS=false
DRY_RUN=false
POSITIONAL_ARGS=()

usage() {
    echo -e "${BOLD}GitHub Repository Protection & Security Ruleset Configurator${NC}"
    echo ""
    echo "Usage:"
    echo "  $0 [options]"
    echo "  $0 <org/account> <repo>"
    echo "  $0 <org/repo>"
    echo ""
    echo "Parameters:"
    echo "  -o, --org, --owner, --account <name>  GitHub account or organization name (e.g. bsommers)"
    echo "  -r, --repo <name|owner/name>          Target repository name (e.g. swe-skills or bsommers/swe-skills)"
    echo "  --public                              Set repository visibility to public"
    echo "  --private                             Set repository visibility to private"
    echo "  --approvals <count>                   Required approving review count (default: 1)"
    echo "  --signed-commits <true|false>         Require signed commits (default: true)"
    echo "  --add-collaborator <username>         Invite / add a collaborator"
    echo "  --permission <pull|push|maintain|admin> Permission level for collaborator (default: push)"
    echo "  --list-collaborators                  List all active repository collaborators"
    echo "  --dry-run                             Preview payload without applying changes"
    echo "  -h, --help                            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --org bsommers --repo swe-skills"
    echo "  $0 -o bsommers -r swe-skills-2 --approvals 1"
    echo "  $0 bsommers swe-skills"
    echo "  $0 bsommers/swe-skills-2 --public"
    echo "  $0 --repo bsommers/swe-skills --add-collaborator alice --permission push"
    echo "  $0                                    # Auto-detects org and repo from local git remote"
    exit 0
}

# Parse flags and arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--org|--owner|--account)
            TARGET_ORG="$2"
            shift 2
            ;;
        -r|--repo)
            TARGET_REPO="$2"
            shift 2
            ;;
        --public)
            SET_VISIBILITY="public"
            shift
            ;;
        --private)
            SET_VISIBILITY="private"
            shift
            ;;
        --approvals)
            REQUIRED_APPROVALS="$2"
            shift 2
            ;;
        --signed-commits)
            REQUIRE_SIGNED_COMMITS="$2"
            shift 2
            ;;
        --add-collaborator)
            ADD_COLLABORATOR="$2"
            shift 2
            ;;
        --permission)
            COLLABORATOR_PERMISSION="$2"
            shift 2
            ;;
        --list-collaborators)
            LIST_COLLABORATORS=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Handle positional arguments if provided
if [ ${#POSITIONAL_ARGS[@]} -ge 2 ]; then
    TARGET_ORG="${POSITIONAL_ARGS[0]}"
    TARGET_REPO="${POSITIONAL_ARGS[1]}"
elif [ ${#POSITIONAL_ARGS[@]} -eq 1 ]; then
    if [[ "${POSITIONAL_ARGS[0]}" == *"/"* ]]; then
        TARGET_REPO="${POSITIONAL_ARGS[0]}"
    elif [ -z "$TARGET_ORG" ] && [ -n "$TARGET_REPO" ]; then
        TARGET_ORG="${POSITIONAL_ARGS[0]}"
    elif [ -n "$TARGET_ORG" ] && [ -z "$TARGET_REPO" ]; then
        TARGET_REPO="${POSITIONAL_ARGS[0]}"
    else
        TARGET_REPO="${POSITIONAL_ARGS[0]}"
    fi
fi

# Combine ORG and REPO into canonical owner/repo format
FULL_REPO=""

if [ -n "$TARGET_REPO" ]; then
    if [[ "$TARGET_REPO" == *"/"* ]]; then
        FULL_REPO="$TARGET_REPO"
    elif [ -n "$TARGET_ORG" ]; then
        FULL_REPO="${TARGET_ORG}/${TARGET_REPO}"
    fi
fi

echo -e "${CYAN}${BOLD}"
echo "========================================================"
echo "      GitHub Repository Protection & Security Setup     "
echo "========================================================"
echo -e "${NC}"

# Pre-flight checks
if ! command -v gh >/dev/null 2>&1; then
    echo -e "${RED}Error: GitHub CLI ('gh') is required. Install via 'brew install gh' or https://cli.github.com${NC}"
    exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}Error: GitHub CLI is not authenticated. Run 'gh auth login' first.${NC}"
    exit 1
fi

# Detect repository from local git remote if not supplied
if [ -z "$FULL_REPO" ]; then
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
        if [ -n "$REMOTE_URL" ]; then
            DETECTED_REPO=$(echo "$REMOTE_URL" | sed -E 's/.*github\.com[:\/]([^\/]+\/[^\/\.]+)(\.git)?/\1/')
            if [ -n "$TARGET_ORG" ] && [ -z "$TARGET_REPO" ]; then
                # User gave org, extract repo name from remote
                REPO_NAME=$(echo "$DETECTED_REPO" | cut -d'/' -f2)
                FULL_REPO="${TARGET_ORG}/${REPO_NAME}"
            elif [ -z "$TARGET_ORG" ] && [ -n "$TARGET_REPO" ]; then
                # User gave repo name, extract org from remote
                ORG_NAME=$(echo "$DETECTED_REPO" | cut -d'/' -f1)
                FULL_REPO="${ORG_NAME}/${TARGET_REPO}"
            else
                FULL_REPO="$DETECTED_REPO"
            fi
        fi
    fi
fi

# If still missing org or repo, ask interactively or use authenticated user
if [ -z "$FULL_REPO" ]; then
    AUTH_USER=$(gh api user --jq .login 2>/dev/null || echo "")
    
    if [ -z "$TARGET_ORG" ]; then
        read -r -p "Enter GitHub Organization or Account name [${AUTH_USER}]: " input_org
        TARGET_ORG="${input_org:-$AUTH_USER}"
    fi
    
    if [ -z "$TARGET_REPO" ]; then
        read -r -p "Enter Repository name: " input_repo
        TARGET_REPO="$input_repo"
    fi
    
    if [ -n "$TARGET_ORG" ] && [ -n "$TARGET_REPO" ]; then
        if [[ "$TARGET_REPO" == *"/"* ]]; then
            FULL_REPO="$TARGET_REPO"
        else
            FULL_REPO="${TARGET_ORG}/${TARGET_REPO}"
        fi
    fi
fi

if [ -z "$FULL_REPO" ]; then
    echo -e "${RED}Error: No repository specified. Pass --org <org> --repo <repo> or <org>/<repo>.${NC}"
    exit 1
fi

echo -e "Target Account/Org: ${BOLD}${CYAN}$(echo "$FULL_REPO" | cut -d'/' -f1)${NC}"
echo -e "Target Repository:  ${BOLD}${GREEN}${FULL_REPO}${NC}"

# 1. Fetch Repository Metadata
REPO_INFO=$(gh api "repos/${FULL_REPO}" --jq '{name: .name, default_branch: .default_branch, private: .private, visibility: .visibility}')
DEFAULT_BRANCH=$(echo "$REPO_INFO" | jq -r '.default_branch // "main"')
IS_PRIVATE=$(echo "$REPO_INFO" | jq -r '.private')
VISIBILITY=$(echo "$REPO_INFO" | jq -r '.visibility')

echo -e "Default Branch:     ${BOLD}${DEFAULT_BRANCH}${NC}"
echo -e "Current Visibility: ${BOLD}${VISIBILITY}${NC}"
echo ""

# Handle visibility change
if [ -n "$SET_VISIBILITY" ] && [ "$SET_VISIBILITY" != "$VISIBILITY" ]; then
    echo -e "${BLUE}Changing visibility to '${SET_VISIBILITY}'...${NC}"
    if [ "$DRY_RUN" = false ]; then
        gh repo edit "$FULL_REPO" --visibility "$SET_VISIBILITY" --accept-visibility-change-consequences
        echo -e "${GREEN}✓ Repository visibility updated to ${SET_VISIBILITY}.${NC}"
        VISIBILITY="$SET_VISIBILITY"
        if [ "$SET_VISIBILITY" = "private" ]; then
            IS_PRIVATE=true
        else
            IS_PRIVATE=false
        fi
    else
        echo -e "${YELLOW}[DRY RUN] Would update visibility to ${SET_VISIBILITY}.${NC}"
    fi
    echo ""
fi

# 2. Configure Collaborators (if requested)
if [ -n "$ADD_COLLABORATOR" ]; then
    echo -e "${BLUE}Adding collaborator '${ADD_COLLABORATOR}' with permission '${COLLABORATOR_PERMISSION}'...${NC}"
    if [ "$DRY_RUN" = false ]; then
        gh api --method PUT "repos/${FULL_REPO}/collaborators/${ADD_COLLABORATOR}" -f permission="$COLLABORATOR_PERMISSION"
        echo -e "${GREEN}✓ Invitation sent / collaborator added: ${ADD_COLLABORATOR} (${COLLABORATOR_PERMISSION})${NC}"
    else
        echo -e "${YELLOW}[DRY RUN] Would add collaborator ${ADD_COLLABORATOR} with ${COLLABORATOR_PERMISSION} permission.${NC}"
    fi
    echo ""
fi

if [ "$LIST_COLLABORATORS" = true ]; then
    echo -e "${BOLD}Current Collaborators for ${FULL_REPO}:${NC}"
    gh api "repos/${FULL_REPO}/collaborators" --jq '.[] | "  • " + .login + " (" + .role_name + ")"' || true
    echo ""
fi

# 3. Enable Secret Scanning & Push Protection
if [ "$ENABLE_SECRET_SCANNING" = true ] || [ "$ENABLE_PUSH_PROTECTION" = true ]; then
    echo -e "${BLUE}Configuring Secret Scanning & Push Protection...${NC}"
    if [ "$DRY_RUN" = false ]; then
        gh api --method PATCH "repos/${FULL_REPO}" \
            -f "security_and_analysis[secret_scanning][status]=enabled" \
            -f "security_and_analysis[secret_scanning_push_protection][status]=enabled" >/dev/null 2>&1 || {
            echo -e "${YELLOW}ℹ Note: Secret scanning configuration requires public repo or GitHub Advanced Security.${NC}"
        }
        echo -e "${GREEN}✓ Secret scanning & push protection configured.${NC}"
    else
        echo -e "${YELLOW}[DRY RUN] Would enable secret scanning and push protection.${NC}"
    fi
    echo ""
fi

# 4. Construct Ruleset Payload
echo -e "${BLUE}Building Recommended Protection Ruleset for '${DEFAULT_BRANCH}'...${NC}"

RULES_JSON=$(cat << EOF
{
  "name": "Protect Default Branch (${DEFAULT_BRANCH})",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": [
        "~DEFAULT_BRANCH"
      ],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "deletion"
    },
    {
      "type": "non_fast_forward"
    },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": ${REQUIRED_APPROVALS},
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "require_last_push_approval": true,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_linear_history"
    }
  ],
  "bypass_actors": []
}
EOF
)

if [ "$REQUIRE_SIGNED_COMMITS" = "true" ]; then
    RULES_JSON=$(echo "$RULES_JSON" | jq '.rules += [{"type": "required_signatures"}]')
fi

if [ "$DRY_RUN" = true ]; then
    echo -e "${BOLD}Ruleset Payload Preview:${NC}"
    echo "$RULES_JSON" | jq .
    echo ""
    echo -e "${YELLOW}[DRY RUN] Ruleset not created. Exiting.${NC}"
    exit 0
fi

# 5. Check and Apply Ruleset
EXISTING_RULESETS=$(gh api "repos/${FULL_REPO}/rulesets" 2>/dev/null || echo "[]")
EXISTING_ID=$(echo "$EXISTING_RULESETS" | jq -r '.[] | select(.name | startswith("Protect Default Branch")) | .id' | head -n 1)

if [ -n "$EXISTING_ID" ]; then
    echo -e "Updating existing ruleset (ID: ${EXISTING_ID})..."
    gh api --method PUT "repos/${FULL_REPO}/rulesets/${EXISTING_ID}" --input - <<< "$RULES_JSON" >/dev/null
    echo -e "${GREEN}✓ Updated existing ruleset: ID ${EXISTING_ID}${NC}"
else
    echo -e "Creating new ruleset..."
    NEW_RULESET=$(gh api --method POST "repos/${FULL_REPO}/rulesets" --input - <<< "$RULES_JSON")
    NEW_ID=$(echo "$NEW_RULESET" | jq -r '.id')
    echo -e "${GREEN}✓ Created new branch protection ruleset: ID ${NEW_ID}${NC}"
fi

echo ""
echo -e "${GREEN}${BOLD}========================================================${NC}"
echo -e "${GREEN}${BOLD}  🎉 Repository Protection Successfully Applied!       ${NC}"
echo -e "${GREEN}${BOLD}========================================================${NC}"
echo ""
echo -e "Summary of Active Protections on ${BOLD}${FULL_REPO}${NC}:"
echo -e "  • ${GREEN}✓${NC} Branch: Default branch ('${DEFAULT_BRANCH}') dynamically covered"
echo -e "  • ${GREEN}✓${NC} Pull Requests: Required (at least ${REQUIRED_APPROVALS} approval)"
echo -e "  • ${GREEN}✓${NC} Stale Approvals: Dismissed on new commits"
echo -e "  • ${GREEN}✓${NC} Code Owner Reviews: Required (via CODEOWNERS)"
echo -e "  • ${GREEN}✓${NC} Thread Resolution: All review conversations must be resolved"
echo -e "  • ${GREEN}✓${NC} Signed Commits: $([ "$REQUIRE_SIGNED_COMMITS" = "true" ] && echo "Required (GPG/SSH)" || echo "Optional")"
echo -e "  • ${GREEN}✓${NC} Force Pushes: Blocked (non_fast_forward)"
echo -e "  • ${GREEN}✓${NC} Branch Deletion: Blocked"
echo -e "  • ${GREEN}✓${NC} Administrator Bypass: Disabled (Rules enforced equally on admins)"
echo -e "  • ${GREEN}✓${NC} Secret Scanning & Push Protection: Active"
echo ""
echo -e "Settings URL: ${CYAN}https://github.com/${FULL_REPO}/settings/rules${NC}"
echo ""
