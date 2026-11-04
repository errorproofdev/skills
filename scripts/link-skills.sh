#!/usr/bin/env bash
# Mirror this repo's skills into a local skills directory as symlinks.
#
# Usage: scripts/link-skills.sh <target-dir>
#   e.g. scripts/link-skills.sh ~/.claude/skills
#
# For every plugins/<category>/skills/<name> in the repo, <target-dir>/<name>
# becomes a symlink to it. Anything already at that path that is not the
# correct link is moved to <target-dir>.backup/<timestamp>/<name> first.
# Symlinks in <target-dir> that point into this repo but whose skill no
# longer exists are removed. Entries not owned by this repo are never touched.
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 <target-dir>" >&2
  exit 2
fi

repo="$(cd "$(dirname "$0")/.." && pwd -P)"
target="$1"
[ -d "$target" ] || { echo "error: target directory does not exist: $target" >&2; exit 1; }
target="$(cd "$target" && pwd -P)"
backup="$target.backup/$(date +%Y%m%d-%H%M%S)"

linked=0 unchanged=0 backed_up=0 pruned=0

for src in "$repo"/plugins/*/skills/*/; do
  src="${src%/}"
  name="$(basename "$src")"
  [ -f "$src/SKILL.md" ] || { echo "error: $src has no SKILL.md" >&2; exit 1; }
  dest="$target/$name"
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    unchanged=$((unchanged + 1))
    continue
  fi
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    mkdir -p "$backup"
    mv "$dest" "$backup/$name"
    backed_up=$((backed_up + 1))
  fi
  ln -s "$src" "$dest"
  linked=$((linked + 1))
done

for dest in "$target"/*; do
  [ -L "$dest" ] || continue
  case "$(readlink "$dest")" in
    "$repo"/plugins/*) [ -e "$dest" ] || { rm "$dest"; pruned=$((pruned + 1)); } ;;
  esac
done

echo "target=$target linked=$linked unchanged=$unchanged backed_up=$backed_up pruned=$pruned"
[ "$backed_up" -eq 0 ] || echo "backup=$backup"
