#!/usr/bin/env bash
# Install Carta git hooks and merge configuration into this repo's .git.
#
# Installs:
#   - pre-commit hook  → regenerates INDEX.yaml when content files are staged
#   - post-merge hook  → regenerates INDEX.yaml after a merge from upstream
#   - post-rewrite hook → regenerates INDEX.yaml after a rebase
#   - merge.ours.driver git config → enables `INDEX.yaml merge=ours` from
#     .gitattributes (the post-merge hook then rebuilds from source)
#
# Idempotent — re-running is safe. Existing non-symlink hooks are backed
# up with a .backup.<timestamp> suffix rather than overwritten.
#
# If your repo already uses the pre-commit framework (pre-commit.com),
# don't use this script — integrate via .pre-commit-config.yaml instead.

set -eu

repo_root="$(git rev-parse --show-toplevel)"

install_hook() {
  local name="$1"
  local hook_src="$repo_root/tools/hooks/$name"
  local hook_dst="$repo_root/.git/hooks/$name"

  if [ ! -f "$hook_src" ]; then
    echo "✗ $hook_src not found — are you in the Carta repo?" >&2
    exit 1
  fi

  chmod +x "$hook_src"

  # If a pre-commit-framework symlink is present for pre-commit, warn and stop.
  if [ "$name" = "pre-commit" ] && [ -L "$hook_dst" ]; then
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
    echo "Backed up existing $name hook to $backup"
  fi

  ln -sf "$hook_src" "$hook_dst"
  echo "✓ Installed $name hook: $hook_dst → $hook_src"
}

install_hook pre-commit
install_hook post-merge
install_hook post-rewrite

# Register the `ours` merge driver in this repo's git config. Without this,
# the `INDEX.yaml merge=ours` line in .gitattributes is silently ignored.
git config merge.ours.driver true
echo "✓ Registered merge.ours.driver in repo git config"

echo
echo "Done. INDEX.yaml will:"
echo "  - regenerate on commits that touch content files (pre-commit)"
echo "  - regenerate after upstream merges (post-merge + .gitattributes merge=ours)"
echo "  - regenerate after rebases (post-rewrite)"
echo
echo "Keep \`python tools/build_index.py --check\` in CI as the freshness gate"
echo "that catches a clone whose hooks didn't fire."
