#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_dir"
if [[ -d .venv/bin ]]; then export PATH="$repo_dir/.venv/bin:$PATH"; fi
export ANSIBLE_CONFIG="$repo_dir/ansible.cfg"
export ANSIBLE_HOME="$repo_dir/.cache/ansible"
mkdir -p .cache/tests
python3 tests/static/check_power.py
bash tests/shell/defaults.sh
bash tests/shell/bootstrap.sh
bash tests/shell/wezterm.sh
bash tests/shell/noctalia.sh
bash tests/shell/output-defaults.sh

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/packages.yml "$@" >".cache/tests/packages-$mode.log" 2>&1; then
    cat ".cache/tests/packages-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Package selection fixtures passed without native transactions.'
if ! ansible-playbook tests/playbooks/wezterm-files.yml >.cache/tests/wezterm-files.log 2>&1; then
  cat .cache/tests/wezterm-files.log
  exit 1
fi
printf '%s\n' 'WezTerm local desktop boundary, installation, idempotency and restore passed.'
if ! ansible-playbook tests/playbooks/wezterm-home.yml >.cache/tests/wezterm-home.log 2>&1; then
  cat .cache/tests/wezterm-home.log
  exit 1
fi
printf '%s\n' 'WezTerm account configuration backup and idempotency fixture passed.'

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/default-boot.yml "$@" >".cache/tests/default-boot-$mode.log" 2>&1; then
    cat ".cache/tests/default-boot-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Enabled boot defaults reject unresolved machine configuration before writes.'

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/fonts.yml "$@" >".cache/tests/fonts-$mode.log" 2>&1; then
    cat ".cache/tests/fonts-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Font source, selection and recovery fixtures passed.'

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

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/keyring.yml "$@" >".cache/tests/keyring-$mode.log" 2>&1; then
    cat ".cache/tests/keyring-$mode.log"
    exit 1
  fi
done
if ! ansible-playbook tests/playbooks/keyring-files.yml >.cache/tests/keyring-files.log 2>&1; then
  cat .cache/tests/keyring-files.log
  exit 1
fi
printf '%s\n' 'KWallet PAM preservation/refusal and disposable file recovery fixtures passed.'

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/noctalia-greeter.yml "$@" >".cache/tests/greeter-$mode.log" 2>&1; then
    cat ".cache/tests/greeter-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Noctalia Greeter preparation, preservation, refusal and recovery fixtures passed.'

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/menu-label.yml "$@" >".cache/tests/menu-label-$mode.log" 2>&1; then
    cat ".cache/tests/menu-label-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Display-only Limine label and native-default restoration fixtures passed.'

for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/ui-variants.yml "$@" >".cache/tests/ui-variants-$mode.log" 2>&1; then
    cat ".cache/tests/ui-variants-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Compact launcher and source/native/private binary provenance fixtures passed.'

if ! ansible-playbook tests/playbooks/bootloader.yml >.cache/tests/bootloader.log 2>&1; then
  cat .cache/tests/bootloader.log
  exit 1
fi
printf '%s\n' 'Independent GRUB/Limine preservation and reapplication fixtures passed; actual boot pending VM.'

if ! ansible-playbook tests/playbooks/limine-appearance.yml >.cache/tests/limine-appearance.log 2>&1; then
  cat .cache/tests/limine-appearance.log
  exit 1
fi
printf '%s\n' 'Graphical Limine preservation, recovery and unsafe-input fixtures passed.'

if ! ansible-playbook tests/playbooks/limine-font-preview.yml --check >.cache/tests/limine-font-preview.log 2>&1; then
  cat .cache/tests/limine-font-preview.log
  exit 1
fi
printf '%s\n' 'Graphical font ownership upgrade makes no metadata writes in global check mode.'

if ! ansible-playbook tests/playbooks/plymouth.yml >.cache/tests/plymouth.log 2>&1; then
  cat .cache/tests/plymouth.log
  exit 1
fi
if ! ansible-playbook tests/playbooks/plymouth-preview.yml --check >.cache/tests/plymouth-preview.log 2>&1; then
  cat .cache/tests/plymouth-preview.log
  exit 1
fi
printf '%s\n' 'Both initramfs dispatch, idempotency, kernel-restore guard and no-write preview fixtures passed.'

if ! ansible-playbook tests/playbooks/limine-plymouth.yml >.cache/tests/limine-plymouth.log 2>&1; then
  cat .cache/tests/limine-plymouth.log
  exit 1
fi
for mode in normal check; do
  set --
  if [[ "$mode" == check ]]; then set -- --check; fi
  if ! ansible-playbook tests/playbooks/limine-bindings.yml "$@" >".cache/tests/limine-bindings-$mode.log" 2>&1; then
    cat ".cache/tests/limine-bindings-$mode.log"
    exit 1
  fi
done
printf '%s\n' 'Limine active-image staging, preservation, recovery, refusal and no-write preview fixtures passed.'
