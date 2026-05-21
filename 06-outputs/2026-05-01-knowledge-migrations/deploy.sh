#!/bin/bash
# Deploy .claude/ knowledge layers to project folders
# Run from anywhere: bash ~/path/to/deploy.sh

STAGING=~/"Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro/06-outputs/2026-05-01-knowledge-migrations"
PROJECTS=~/.gemini/antigravity/projects

deploy() {
  local name=$1
  local src="$STAGING/$name/.claude"
  local dst="$PROJECTS/$name/.claude"
  echo "→ $name"
  cp -r "$src/." "$dst/"
  echo "  ✓ Done ($dst)"
}

deploy smart-volume-radar
deploy proposal-generator
deploy website
deploy cms

echo ""
echo "All done. Verify with:"
echo "  ls ~/.gemini/antigravity/projects/smart-volume-radar/.claude/"
echo "  ls ~/.gemini/antigravity/projects/proposal-generator/.claude/"
echo "  ls ~/.gemini/antigravity/projects/website/.claude/"
echo "  ls ~/.gemini/antigravity/projects/cms/.claude/"
