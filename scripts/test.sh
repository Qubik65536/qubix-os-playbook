#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_dir"
if [[ -d .venv/bin ]]; then export PATH="$repo_dir/.venv/bin:$PATH"; fi
export ANSIBLE_CONFIG="$repo_dir/ansible.cfg"
export ANSIBLE_HOME="$repo_dir/.cache/ansible"
mkdir -p .cache/tests

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/framework.yml "$@" >".cache/tests/framework-$mode.log" 2>&1; then
    cat ".cache/tests/framework-$mode.log"
    exit 1
  fi
  if ! grep -Eq 'changed=0 .*failed=0 ' ".cache/tests/framework-$mode.log"; then
    cat ".cache/tests/framework-$mode.log"
    exit 1
  fi
  printf 'Framework tests passed (%s mode, zero changes).\n' "$mode"
done
