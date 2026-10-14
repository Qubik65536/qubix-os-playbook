#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p "$repo_dir/.cache/tests"
fixture_output="$(mktemp "$repo_dir/.cache/tests/qubix-wrapper.XXXXXX")"
cleanup() { rm -f -- "$fixture_output"; }
trap cleanup EXIT

for action in deploy restore; do
  for argument in -tbranding --tags=branding --skip-tags=branding; do
    if bash "$repo_dir/bootstrap.sh" "$action" "$argument" >"$fixture_output" 2>&1; then
      printf 'Unexpected acceptance: %s %s\n' "$action" "$argument" >&2
      exit 1
    fi
    # Require wrapper rejection before Ansible can inspect or change any host.
    if ! grep -Fq 'tags are reserved for verification' "$fixture_output"; then
      cat "$fixture_output"
      exit 1
    fi
  done
done
printf '%s\n' 'Deployment/restore tag selection rejected before Ansible invocation.'
