#!/usr/bin/env bash
# sync_wiki.sh
# Syncs local wiki.md and all tool subpages to the GitHub Wiki for this repo.
# Usage: ./sync_wiki.sh

set -e

REPO="apro187/HA-Tools"
WIKI_REPO="https://github.com/${REPO}.wiki.git"
TMP_DIR="/tmp/ha-tools-wiki-sync-$$"

# Clone the wiki repo to a temp directory
rm -rf "$TMP_DIR"
git clone "$WIKI_REPO" "$TMP_DIR"

# Copy wiki.md to Home.md (main page)
cp wiki.md "$TMP_DIR/Home.md"

# Copy all tool subpages from wiki/ to the wiki repo (except wiki.md itself)
if [ -d wiki ]; then
  for f in wiki/*.md; do
    base=$(basename "$f")
    # Don't overwrite Home.md
    [ "$base" = "wiki.md" ] && continue
    cp "$f" "$TMP_DIR/$base"
  done
fi

cd "$TMP_DIR"
git add *.md
if git diff --cached --quiet; then
  echo "No changes to push to the wiki."
else
  git commit -m "Update Home.md and tool subpages from local wiki/"
  git push
  echo "Wiki updated successfully!"
fi

# Clean up
tmp_cleanup() { rm -rf "$TMP_DIR"; }
trap tmp_cleanup EXIT
