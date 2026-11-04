#!/usr/bin/env bash
# Copy a local skill into this repo under a category.
#
# Usage: scripts/import-skill.sh <source-dir> <skill> <category>
#   e.g. scripts/import-skill.sh ~/.claude/skills my-skill workflow
#
# Copies <source-dir>/<skill> to plugins/<category>/skills/<skill>, dereferencing
# symlinks and skipping .DS_Store. Run scripts/link-skills.sh afterwards to
# replace the local copy with a symlink to the repo.
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "usage: $0 <source-dir> <skill> <category>" >&2
  exit 2
fi

repo="$(cd "$(dirname "$0")/.." && pwd -P)"
src="$1/$2"
skill="$2"
category="$3"
dest="$repo/plugins/$category/skills/$skill"

[ -d "$repo/plugins/$category" ] || { echo "error: unknown category '$category'; expected one of: $(cd "$repo/plugins" && echo */ | tr -d /)" >&2; exit 1; }
[ -f "$src/SKILL.md" ] || { echo "error: $src/SKILL.md not found" >&2; exit 1; }
existing="$(find "$repo"/plugins/*/skills -mindepth 1 -maxdepth 1 -name "$skill")"
[ -z "$existing" ] || { echo "error: skill already in repo: $existing" >&2; exit 1; }
name="$(sed -n '2,/^---/s/^name:[[:space:]]*//p' "$src/SKILL.md" | tr -d "\"'" | head -n 1)"
[ "$name" = "$skill" ] || { echo "error: SKILL.md name '$name' does not match directory '$skill'" >&2; exit 1; }

mkdir -p "$dest"
rsync -aL --exclude .DS_Store "$src/" "$dest/"
echo "imported=$skill category=$category dest=$dest"
