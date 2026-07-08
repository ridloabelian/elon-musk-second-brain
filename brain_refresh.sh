#!/bin/bash
set -e

# Recreated brain_refresh.sh indexer

INDEX_DIR="$(dirname "$0")/repo_index"
mkdir -p "$INDEX_DIR"
PREV_COUNT_FILE="$INDEX_DIR/prev_count.txt"
CURRENT_JSON="$INDEX_DIR/current_repos.json"
PREV_JSON="$INDEX_DIR/prev_repos.json"

# Move current to prev
if [ -f "$CURRENT_JSON" ]; then
    mv "$CURRENT_JSON" "$PREV_JSON"
else
    # Create empty object or use the 71 from prompt context as a baseline
    echo "[]" > "$PREV_JSON"
fi

# Fetch current repos
gh repo list --limit 1000 --json nameWithOwner,name,description,pushedAt > "$CURRENT_JSON" || { echo "Failed to fetch repos via gh CLI"; exit 1; }

CURRENT_COUNT=$(jq 'length' "$CURRENT_JSON")
PREV_COUNT=${1:-71} # Fallback to 71 from the prompt context

echo "Project Brain refreshed: $CURRENT_COUNT repos"
echo "Project Brain refreshed at $(date)"
echo ""

if (( CURRENT_COUNT > PREV_COUNT )); then
    echo "New repos found since last refresh:"
    # Very basic new repo check using jq diff
    jq -r '.[].nameWithOwner' "$CURRENT_JSON" | sort > "$INDEX_DIR/curr.txt"
    if [ -f "$PREV_JSON" ] && [ "$(jq 'length' "$PREV_JSON")" -gt 0 ]; then
        jq -r '.[].nameWithOwner' "$PREV_JSON" | sort > "$INDEX_DIR/prev.txt"
    else
        touch "$INDEX_DIR/prev.txt"
    fi
    comm -13 "$INDEX_DIR/prev.txt" "$INDEX_DIR/curr.txt" | sed 's/^/- /'
elif (( CURRENT_COUNT < PREV_COUNT )); then
    echo "Repo count decreased ($PREV_COUNT -> $CURRENT_COUNT)."
else
    echo "No new repos."
fi

echo "$CURRENT_COUNT" > "$PREV_COUNT_FILE"
