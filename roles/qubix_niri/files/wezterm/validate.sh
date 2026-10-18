#!/usr/bin/env bash
# WezTerm CLI can report configuration errors while returning zero and using defaults.
set -euo pipefail
if (( $# != 1 )); then exit 2; fi
qubix_diagnostics=$(mktemp)
trap 'rm -f -- "$qubix_diagnostics"' EXIT
if ! WEZTERM_LOG=error /usr/bin/wezterm --config-file "$1" ls-fonts > /dev/null 2> "$qubix_diagnostics"; then
  cat "$qubix_diagnostics" >&2
  exit 1
fi
if [[ -s "$qubix_diagnostics" ]]; then
  cat "$qubix_diagnostics" >&2
  exit 1
fi
