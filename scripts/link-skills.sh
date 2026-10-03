#!/usr/bin/env bash
# Symlink every skill in skills/ into each harness's user skill folder, so a
# `git pull` (or a local edit) is live everywhere without reinstalling.
#   scripts/link-skills.sh [--antigravity] [--unlink]
#   ~/.claude/skills  Claude Code
#   ~/.agents/skills  Codex, Gemini CLI, Cursor, Copilot, OpenCode, Amp, ...
#   ~/.gemini/antigravity-cli/skills  Antigravity CLI (with --antigravity)
# Don't also install this repo as a plugin on the same machine: Codex would
# list every skill twice.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")
unlink=false
for arg in "$@"; do
  case "$arg" in
    --antigravity) DESTS+=("$HOME/.gemini/antigravity-cli/skills") ;;
    --unlink) unlink=true ;;
    *) echo "usage: $0 [--antigravity] [--unlink]" >&2; exit 1 ;;
  esac
done

for dest in "${DESTS[@]}"; do
  # Writing into a destination that resolves into this repo would pollute skills/.
  if [ -L "$dest" ]; then
    case "$(readlink -f "$dest")" in
      "$REPO" | "$REPO"/*) echo "error: $dest is a symlink into this repo; remove it and re-run" >&2; exit 1 ;;
    esac
  fi
  mkdir -p "$dest"

  for src in "$REPO"/skills/*/; do
    [ -f "$src/SKILL.md" ] || continue
    src="${src%/}"
    name="$(basename "$src")"
    target="$dest/$name"

    if $unlink; then
      if [ -L "$target" ] && [ "$(readlink -f "$target")" = "$src" ]; then
        rm "$target"
        echo "unlinked $target"
      fi
      continue
    fi

    # Never clobber a real folder or a link to someone else's skill.
    if { [ -e "$target" ] || [ -L "$target" ]; } && { [ ! -L "$target" ] || [ "$(readlink -f "$target")" != "$src" ]; }; then
      echo "skip $target: exists and is not ours (remove it to link this repo's $name)" >&2
      continue
    fi
    ln -sfn "$src" "$target"
    echo "linked $target -> $src"
  done

  # Drop links to skills that were renamed or removed from this repo.
  for link in "$dest"/*; do
    [ -L "$link" ] || continue
    case "$(readlink "$link")" in
      "$REPO"/skills/*) [ -e "$link" ] || { rm "$link"; echo "removed stale $link"; } ;;
    esac
  done
done
