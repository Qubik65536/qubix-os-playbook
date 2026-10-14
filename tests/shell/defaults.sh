#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$repo_dir/.cache/tests"
fixture_dir="$(mktemp -d "$repo_dir/.cache/tests/qubix-shell.XXXXXX")"
cleanup() { rm -rf -- "$fixture_dir"; }
trap cleanup EXIT

# Override only XDG configuration in a disposable root; never change HOME.
XDG_CONFIG_HOME="$fixture_dir" STARSHIP_CONFIG=/my/chosen/config.toml bash --noprofile --norc -c '
  . "$1"
  test "$STARSHIP_CONFIG" = /my/chosen/config.toml
' bash "$repo_dir/roles/qubix_shell/files/qubix.sh"

printf '%s\n' '[character]' > "$fixture_dir/starship.toml"
XDG_CONFIG_HOME="$fixture_dir" STARSHIP_CONFIG='' bash --noprofile --norc -c '
  . "$1"
  test -z "$STARSHIP_CONFIG"
' bash "$repo_dir/roles/qubix_shell/files/qubix.sh"

mkdir "$fixture_dir/empty"
XDG_CONFIG_HOME="$fixture_dir/empty" STARSHIP_CONFIG='' bash --noprofile --norc -c '
  . "$1"
  test "$STARSHIP_CONFIG" = /etc/qubix/starship.toml
' bash "$repo_dir/roles/qubix_shell/files/qubix.sh"
printf '%s\n' 'Shell defaults respect explicit and existing user Starship configuration.'
