#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_dir"
if [[ -d .venv/bin ]]; then export PATH="$repo_dir/.venv/bin:$PATH"; fi
export ANSIBLE_CONFIG="$repo_dir/ansible.cfg"
export ANSIBLE_HOME="$repo_dir/.cache/ansible"

yamllint .
ansible-lint --offline playbooks roles tests/playbooks tests/integration tests/tasks
for playbook in playbooks/*.yml tests/playbooks/*.yml tests/integration/*.yml; do
  ansible-playbook "$playbook" --syntax-check
done
shellcheck bootstrap.sh scripts/*.sh roles/qubix_shell/files/qubix.sh tests/shell/*.sh
shellcheck roles/qubix_niri/files/wezterm/validate.sh
shellcheck --shell=bash roles/qubix_niri/templates/wezterm.sh.j2
shellcheck --shell=bash roles/qubix_niri/templates/noctalia.sh.j2
shellcheck --shell=bash roles/qubix_niri/templates/output-defaults.sh.j2
shellcheck --shell=bash roles/qubix_niri/templates/fcitx5.sh.j2
python3 -m py_compile tests/integration/files/*.py tests/static/*.py scripts/*.py
python3 tests/static/check_repository.py
node --test tests/javascript/*.test.mjs
for source in roles/qubix_niri/files/fingerprint/*.js; do
  node --input-type=module --check < "$source"
done
git diff --check
printf '%s\n' 'Static validation passed.'
