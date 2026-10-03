#!/usr/bin/env bash
# Create skills/<name>/ from template/.
#   scripts/new-skill.sh <name> [--user-invoked]
# --user-invoked marks the skill as callable only by the human, in both
# Claude (disable-model-invocation) and Codex (allow_implicit_invocation).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
name="${1:-}"
user_invoked=false
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ] || { [ "$#" -eq 2 ] && [ "$2" != "--user-invoked" ]; }; then
  echo "usage: $0 <name> [--user-invoked]" >&2
  exit 1
fi
[ "${2:-}" = "--user-invoked" ] && user_invoked=true

if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || [ "${#name}" -gt 64 ]; then
  echo "usage: $0 <name> [--user-invoked]  (name: lowercase a-z0-9 joined by '-', max 64)" >&2
  exit 1
fi
dest="$REPO/skills/$name"
if [ -e "$dest" ]; then
  echo "error: $dest already exists" >&2
  exit 1
fi

cp -r "$REPO/template" "$dest"
title="$(echo "$name" | sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g')"
sed -i "s/^name: skill-name$/name: $name/; s/^# Skill Name$/# $title/" "$dest/SKILL.md"
sed -i "s/\"Skill Name\"/\"$title\"/" "$dest/agents/openai.yaml"

if $user_invoked; then
  sed -i '/^description:/a disable-model-invocation: true' "$dest/SKILL.md"
  printf 'policy:\n  allow_implicit_invocation: false\n' >>"$dest/agents/openai.yaml"
fi

echo "created $dest"
echo "next: fill in SKILL.md, agents/openai.yaml and evals/basic/, then run scripts/validate.py"
