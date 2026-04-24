#!/usr/bin/env bash
# Install the Carta pre-commit hook into .git/hooks/pre-commit as a symlink.
#
# Idempotent — re-running is safe. If a non-symlink hook already exists, it's
# backed up with a .backup.<timestamp> suffix rather than overwritten.
#
# If your repo already uses the pre-commit framework (pre-commit.com),
# don't use this script — integrate via .pre-commit-config.yaml instead.

set -eu

repo_root="$(git rev-parse --show-toplevel)"
hook_src="$repo_root/tools/hooks/pre-commit"
hook_dst="$repo_root/.git/hooks/pre-commit"

if [ ! -f "$hook_src" ]; then
  echo "✗ $hook_src not found — are you in the Carta repo?" >&2
  exit 1
fi

chmod +x "$hook_src"

# If a pre-commit-framework symlink is present, warn and stop.
if [ -L "$hook_dst" ]; then
  target="$(readlink "$hook_dst")"
  if [[ "$target" == *pre-commit* ]] && [[ "$target" != *carta* ]]; then
    echo "⚠ .git/hooks/pre-commit is already a symlink managed by the pre-commit framework:"
    echo "   $hook_dst → $target"
    echo "   Integrate Carta via .pre-commit-config.yaml instead of this script."
    exit 1
  fi
fi

# Back up any existing non-symlink hook.
if [ -f "$hook_dst" ] && [ ! -L "$hook_dst" ]; then
  backup="$hook_dst.backup.$(date +%s)"
  mv "$hook_dst" "$backup"
  echo "Backed up existing hook to $backup"
fi

ln -sf "$hook_src" "$hook_dst"
echo "✓ Installed pre-commit hook:"
echo "   $hook_dst → $hook_src"
echo
echo "The hook will regenerate INDEX.yaml on any commit that touches content"
echo "files under foundations/, org/, teams/, or projects/."
