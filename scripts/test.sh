#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_dir"
if [[ -d .venv/bin ]]; then export PATH="$repo_dir/.venv/bin:$PATH"; fi
export ANSIBLE_CONFIG="$repo_dir/ansible.cfg"
export ANSIBLE_HOME="$repo_dir/.cache/ansible"
mkdir -p .cache/tests
bash tests/shell/defaults.sh
bash tests/shell/bootstrap.sh
bash tests/shell/noctalia.sh

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

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/branding.yml "$@" >".cache/tests/branding-$mode.log" 2>&1; then
    cat ".cache/tests/branding-$mode.log"
    exit 1
  fi
  printf 'Branding tests passed (%s mode, isolated filesystem).\n' "$mode"
done

if ! ansible-playbook tests/playbooks/recovery.yml >.cache/tests/recovery.log 2>&1; then
  cat .cache/tests/recovery.log
  exit 1
fi
printf '%s\n' 'Backup/restore fixtures passed.'

if ! ansible-playbook tests/playbooks/desktop.yml >.cache/tests/desktop.log 2>&1; then
  cat .cache/tests/desktop.log
  exit 1
fi
printf '%s\n' 'Desktop definition and prerequisite fixtures passed; run native grammar tests separately.'

if ! ansible-playbook tests/playbooks/login.yml >.cache/tests/login.log 2>&1; then
  cat .cache/tests/login.log
  exit 1
fi
printf '%s\n' 'SDDM clone and unsupported-manager fixtures passed.'

if ! ansible-playbook tests/playbooks/bootloader.yml >.cache/tests/bootloader.log 2>&1; then
  cat .cache/tests/bootloader.log
  exit 1
fi
printf '%s\n' 'Independent GRUB/Limine preservation and reapplication fixtures passed; actual boot pending VM.'

if ! ansible-playbook tests/playbooks/plymouth.yml >.cache/tests/plymouth.log 2>&1; then
  cat .cache/tests/plymouth.log
  exit 1
fi
if ! ansible-playbook tests/playbooks/plymouth-preview.yml --check >.cache/tests/plymouth-preview.log 2>&1; then
  cat .cache/tests/plymouth-preview.log
  exit 1
fi
printf '%s\n' 'Both initramfs dispatch, idempotency, kernel-restore guard and no-write preview fixtures passed.'
