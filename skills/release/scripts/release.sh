#!/usr/bin/env bash
#
# release.sh - Automated Semantic Versioning (SemVer) release tool
# Analyzes changes, calculates SemVer bumps, updates CHANGELOG.md, tags, and pushes to remote.
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

DRY_RUN=false
ASSUME_YES=false
MANUAL_BUMP=""
CUSTOM_VERSION=""

usage() {
    echo -e "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --patch           Force PATCH bump (e.g. 0.1.0 -> 0.1.1)"
    echo "  --minor           Force MINOR bump (e.g. 0.1.0 -> 0.2.0)"
    echo "  --major           Force MAJOR bump (e.g. 0.1.0 -> 1.0.0)"
    echo "  --version <vX.Y.Z> Specify exact version tag"
    echo "  --dry-run         Preview changes, version bump, and release notes without committing or tagging"
    echo "  -y, --yes         Push without asking (default: ask on a terminal, skip the push otherwise)"
    echo "  -h, --help        Show this help message"
    echo ""
    exit 0
}

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --patch) MANUAL_BUMP="patch"; shift ;;
        --minor) MANUAL_BUMP="minor"; shift ;;
        --major) MANUAL_BUMP="major"; shift ;;
        --version) CUSTOM_VERSION="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        -y|--yes) ASSUME_YES=true; shift ;;
        -h|--help) usage ;;
        *) echo -e "${RED}Unknown argument: $1${NC}"; usage ;;
    esac
done

echo -e "${CYAN}${BOLD}"
echo "========================================================"
echo "           SWE-Skills Release & Tagging Tool            "
echo "========================================================"
echo -e "${NC}"

# Check if inside a git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo -e "${RED}Error: Not inside a Git repository.${NC}"
    exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "Current Branch: ${BOLD}${CURRENT_BRANCH}${NC}"

# Find latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -z "$LATEST_TAG" ]; then
    echo -e "Latest Tag: ${YELLOW}(None found - initial release)${NC}"
    COMMIT_RANGE="HEAD"
    PREV_VER="0.0.0"
else
    echo -e "Latest Tag: ${GREEN}${LATEST_TAG}${NC}"
    COMMIT_RANGE="${LATEST_TAG}..HEAD"
    # Strip leading 'v'
    PREV_VER="${LATEST_TAG#v}"
fi

# Get commits in range
COMMITS=$(git log "$COMMIT_RANGE" --oneline --no-merges 2>/dev/null || echo "")

if [ -z "$COMMITS" ] && [ -n "$LATEST_TAG" ]; then
    echo -e "${YELLOW}No new commits found since ${LATEST_TAG}. Nothing to release.${NC}"
    exit 0
fi

echo ""
echo -e "${BOLD}Commits to be included in this release:${NC}"
if [ -n "$COMMITS" ]; then
    echo "$COMMITS" | sed 's/^/  • /'
else
    echo "  • (Initial repository commits)"
fi
echo ""

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$PREV_VER"
MAJOR=${MAJOR:-0}
MINOR=${MINOR:-0}
PATCH=${PATCH:-0}

# Determine bump type
BUMP_TYPE="patch"

if [ -n "$CUSTOM_VERSION" ]; then
    NEXT_TAG="$CUSTOM_VERSION"
    [[ "$NEXT_TAG" != v* ]] && NEXT_TAG="v${NEXT_TAG}"
else
    if [ -n "$MANUAL_BUMP" ]; then
        BUMP_TYPE="$MANUAL_BUMP"
    else
        # Auto-detect bump based on commit messages
        has_breaking=false
        has_feat=false

        while IFS= read -r line; do
            if echo "$line" | grep -qiE "(BREAKING CHANGE|feat!|fix!|refactor!)"; then
                has_breaking=true
            elif echo "$line" | grep -qiE "^[a-f0-9]+ feat(\(.*\))?:"; then
                has_feat=true
            fi
        done <<< "$COMMITS"

        if [ "$has_breaking" = true ]; then
            if [ "$MAJOR" -eq 0 ]; then
                BUMP_TYPE="minor" # in 0.x.x breaking usually bumps minor
            else
                BUMP_TYPE="major"
            fi
        elif [ "$has_feat" = true ]; then
            BUMP_TYPE="minor"
        else
            BUMP_TYPE="patch"
        fi

        # If initial release with no prior tags and features present, default to v0.1.0
        if [ -z "$LATEST_TAG" ]; then
            BUMP_TYPE="initial"
        fi
    fi

    case "$BUMP_TYPE" in
        major)
            NEXT_MAJOR=$((MAJOR + 1))
            NEXT_TAG="v${NEXT_MAJOR}.0.0"
            ;;
        minor)
            NEXT_MINOR=$((MINOR + 1))
            NEXT_TAG="v${MAJOR}.${NEXT_MINOR}.0"
            ;;
        initial)
            NEXT_TAG="v0.1.0"
            ;;
        patch|*)
            NEXT_PATCH=$((PATCH + 1))
            NEXT_TAG="v${MAJOR}.${MINOR}.${NEXT_PATCH}"
            ;;
    esac
fi

echo -e "Calculated Release Tag: ${BOLD}${GREEN}${NEXT_TAG}${NC} (Bump type: ${CYAN}${BUMP_TYPE}${NC})"
echo ""

# Generate Changelog entries
TODAY=$(date +"%Y-%m-%d")

RELEASE_NOTES="## [${NEXT_TAG}] - ${TODAY}\n\n"

# Extract feature lines
FEAT_LINES=$(echo "$COMMITS" | grep -iE "^[a-f0-9]+ feat" | sed -E 's/^[a-f0-9]+ feat(\([^\)]+\))?:[[:space:]]*/- /' || echo "")
FIX_LINES=$(echo "$COMMITS" | grep -iE "^[a-f0-9]+ fix" | sed -E 's/^[a-f0-9]+ fix(\([^\)]+\))?:[[:space:]]*/- /' || echo "")
CHORE_LINES=$(echo "$COMMITS" | grep -iE "^[a-f0-9]+ (chore|docs|refactor|test)" | sed -E 's/^[a-f0-9]+ [a-z]+(\([^\)]+\))?:[[:space:]]*/- /' || echo "")

if [ -n "$FEAT_LINES" ]; then
    RELEASE_NOTES="${RELEASE_NOTES}### Added\n${FEAT_LINES}\n\n"
fi
if [ -n "$FIX_LINES" ]; then
    RELEASE_NOTES="${RELEASE_NOTES}### Fixed\n${FIX_LINES}\n\n"
fi
if [ -n "$CHORE_LINES" ]; then
    RELEASE_NOTES="${RELEASE_NOTES}### Changed / Maintenance\n${CHORE_LINES}\n\n"
fi
if [ -z "$FEAT_LINES" ] && [ -z "$FIX_LINES" ] && [ -z "$CHORE_LINES" ]; then
    ALL_LINES=$(echo "$COMMITS" | sed -E 's/^[a-f0-9]+[[:space:]]*/- /')
    RELEASE_NOTES="${RELEASE_NOTES}### Changes\n${ALL_LINES}\n\n"
fi

echo -e "${BOLD}Release Notes Preview:${NC}"
echo -e "$RELEASE_NOTES"

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] No changes were committed, tagged, or pushed.${NC}"
    exit 0
fi

# Update CHANGELOG.md
CHANGELOG_FILE="CHANGELOG.md"
if [ ! -f "$CHANGELOG_FILE" ]; then
    echo "# Changelog" > "$CHANGELOG_FILE"
    echo "" >> "$CHANGELOG_FILE"
    echo "All notable changes to this project will be documented in this file." >> "$CHANGELOG_FILE"
    echo "" >> "$CHANGELOG_FILE"
fi

# Prepend new release under header
TMP_CHANGELOG=$(mktemp)
awk -v notes="$RELEASE_NOTES" '
    NR==1 { print; next }
    NR==2 { print; next }
    NR==3 { print; next }
    NR==4 { print notes; print; next }
    { print }
' "$CHANGELOG_FILE" > "$TMP_CHANGELOG" 2>/dev/null || {
    # Fallback if less than 4 lines
    echo -e "$RELEASE_NOTES" >> "$CHANGELOG_FILE"
    cp "$CHANGELOG_FILE" "$TMP_CHANGELOG"
}
mv "$TMP_CHANGELOG" "$CHANGELOG_FILE"

echo -e "${GREEN}✓ Updated ${CHANGELOG_FILE}${NC}"

# Stage changes & commit
git add "$CHANGELOG_FILE"
git commit -m "chore(release): prepare ${NEXT_TAG}" || true

# Create annotated tag
TAG_MSG="Release ${NEXT_TAG}

$(echo -e "$RELEASE_NOTES" | sed 's/^## .*//')"

git tag -a "$NEXT_TAG" -m "$TAG_MSG"
echo -e "${GREEN}✓ Created annotated git tag: ${BOLD}${NEXT_TAG}${NC}"

# Check for remote and push
REMOTE_NAME=$(git remote | head -n 1 || echo "")

if [ -n "$REMOTE_NAME" ]; then
    echo ""
    DO_PUSH="$ASSUME_YES"
    if [ "$DO_PUSH" != true ] && [ -t 0 ]; then
        read -r -p "Push '${CURRENT_BRANCH}' and tag '${NEXT_TAG}' to remote '${REMOTE_NAME}'? [y/N] " REPLY
        if [[ "$REPLY" =~ ^[Yy]$ ]]; then DO_PUSH=true; fi
    fi
    if [ "$DO_PUSH" = true ]; then
        echo -e "${BLUE}Pushing branch and tag to remote '${REMOTE_NAME}'...${NC}"
        git push "$REMOTE_NAME" "$CURRENT_BRANCH"
        git push "$REMOTE_NAME" "$NEXT_TAG"
        echo -e "${GREEN}✓ Successfully pushed release ${NEXT_TAG} to remote '${REMOTE_NAME}'!${NC}"
    else
        echo -e "${YELLOW}ℹ Not pushed. Release ${NEXT_TAG} exists locally. To publish it:${NC}"
        echo -e "    git push ${REMOTE_NAME} ${CURRENT_BRANCH} && git push ${REMOTE_NAME} ${NEXT_TAG}"
    fi
else
    echo ""
    echo -e "${YELLOW}ℹ Note: No git remote is currently configured.${NC}"
    echo -e "  To push your release to a remote repository later:"
    echo -e "    1. git remote add origin <repo-url>"
    echo -e "    2. git push -u origin ${CURRENT_BRANCH} --tags"
fi

echo ""
echo -e "${GREEN}${BOLD}🎉 Release ${NEXT_TAG} completed successfully!${NC}"
