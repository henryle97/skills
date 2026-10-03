#!/usr/bin/env bash
# Set the same version in every plugin manifest.
#   scripts/bump-version.sh <x.y.z>
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
version="${1:-}"
if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "usage: $0 <x.y.z>" >&2
  exit 1
fi

for manifest in .claude-plugin/plugin.json .codex-plugin/plugin.json; do
  tmp="$(mktemp)"
  jq --arg v "$version" '.version = $v' "$REPO/$manifest" >"$tmp"
  mv "$tmp" "$REPO/$manifest"
  echo "$manifest -> $version"
done
