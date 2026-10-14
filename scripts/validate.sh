#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_dir"
if [[ -d .venv/bin ]]; then export PATH="$repo_dir/.venv/bin:$PATH"; fi
export ANSIBLE_CONFIG="$repo_dir/ansible.cfg"
export ANSIBLE_HOME="$repo_dir/.cache/ansible"

yamllint .
ansible-lint --offline playbooks roles tests/playbooks tests/tasks
for playbook in playbooks/*.yml tests/playbooks/*.yml; do
  ansible-playbook "$playbook" --syntax-check
done
shellcheck bootstrap.sh scripts/*.sh
python3 tests/static/check_repository.py
git diff --check
printf '%s\n' 'Static validation passed.'
