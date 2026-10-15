#!/usr/bin/env bash
# Exercise the actual profile launcher with exec intercepted before Noctalia starts.
# Cases intentionally isolate variables and invoke exec indirectly through the sourced launcher.
# shellcheck disable=SC1090,SC2030,SC2031,SC2329
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
profile="$repo_dir/roles/qubix_niri/templates/noctalia.sh.j2"
if bash "$profile" --application; then
  printf '%s\n' 'Empty application invocation unexpectedly succeeded.' >&2
  exit 1
fi

(
  unset GSETTINGS_BACKEND
  exec() {
    [[ "$GSETTINGS_BACKEND" == memory ]]
    [[ "$NOCTALIA_CONFIG_HOME" == /etc/qubix ]]
    [[ "$NOCTALIA_STATE_HOME" == "$XDG_STATE_HOME/qubix" ]]
    [[ "$NOCTALIA_DATA_HOME" == "$XDG_DATA_HOME/qubix" ]]
    [[ "$XDG_CONFIG_HOME" == /preserved/config ]]
    [[ "$QUBIX_NATIVE_GSETTINGS_BACKEND_SET" == 0 ]]
    [[ "$1" == /usr/bin/noctalia ]]
    exit 0
  }
  export XDG_CONFIG_HOME=/preserved/config
  export XDG_STATE_HOME=/preserved/state
  export XDG_DATA_HOME=/preserved/data
  source "$profile"
)

(
  export GSETTINGS_BACKEND=memory
  export QUBIX_NATIVE_GSETTINGS_BACKEND_SET=0
  exec() {
    [[ "${GSETTINGS_BACKEND+x}" != x ]]
    [[ "$1" == app && "$2" == 'argument with spaces' ]]
    exit 0
  }
  set -- --application app 'argument with spaces'
  source "$profile"
)

(
  export GSETTINGS_BACKEND=memory
  export QUBIX_NATIVE_GSETTINGS_BACKEND_SET=1
  export QUBIX_NATIVE_GSETTINGS_BACKEND=keyfile
  exec() {
    [[ "$GSETTINGS_BACKEND" == keyfile ]]
    [[ "$1" == app ]]
    exit 0
  }
  set -- --application app
  source "$profile"
)

printf '%s\n' 'Noctalia profile and application environment preservation passed.'
