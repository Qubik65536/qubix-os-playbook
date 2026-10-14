#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd -- "$repo_dir"
export ANSIBLE_CONFIG="$repo_dir/ansible.cfg"

usage() {
  printf '%s\n' 'Usage: ./bootstrap.sh verify|deploy|restore [ansible-playbook arguments]'
  printf '%s\n' 'Default inventory is local. Override with -i inventory.ini; verify never escalates privileges.'
}

case "${1:---help}" in
  verify|deploy|restore) action=$1; shift ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

if [[ "$action" == deploy || "$action" == restore ]]; then
  for argument in "$@"; do
    case "$argument" in
      --tags|--tags=*|-t|--skip-tags|--skip-tags=*)
        printf '%s\n' 'Select deployment components in qubix configuration; tags are reserved for verification.' >&2
        exit 2 ;;
    esac
  done
fi

if [[ -x "$repo_dir/.venv/bin/ansible-playbook" ]]; then
  ansible_bin="$repo_dir/.venv/bin/ansible-playbook"
elif command -v ansible-playbook >/dev/null 2>&1; then
  ansible_bin="$(command -v ansible-playbook)"
else
  printf '%s\n' 'Ansible is missing. Follow docs/development/environment.md.' >&2
  exit 127
fi

exec "$ansible_bin" "$repo_dir/playbooks/$action.yml" "$@"
