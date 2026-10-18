#!/usr/bin/env bash
# Read-only evidence collector; run on the disposable CachyOS VM.
set -euo pipefail

case "${1:-}" in
  -h|--help)
    printf '%s\n' 'Usage: bash scripts/collect-target-info.sh'
    printf '%s\n' 'Read-only Linux report. No sudo, installation, service changes or boot writes.'
    exit 0 ;;
  '') ;;
  *) printf '%s\n' 'Unknown argument; use --help.' >&2; exit 2 ;;
esac
if [[ "$(uname -s)" != Linux ]]; then
  printf '%s\n' 'Run this collector on the CachyOS test VM, not the controller.' >&2
  exit 2
fi

probe() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  if command -v "$1" >/dev/null 2>&1; then
    if "$@" 2>&1; then :; else
      printf '%s\n' '[Probe unavailable or failed; retain this diagnostic.]'
    fi
  else
    printf '%s\n' '[Tool not installed.]'
  fi
}

probe uname -a
probe cat /etc/os-release
probe cat /proc/cmdline
probe ip -brief address
probe niri --version
probe pacman -Q paru wezterm niri foot fuzzel waybar mako swaybg starship sddm greetd gdm lightdm grub limine plymouth dracut mkinitcpio
for unit in display-manager sddm greetd gdm lightdm; do
  probe systemctl show "$unit.service" --property=Id,LoadState,ActiveState
done
probe systemctl --user list-units --type=service --state=running --no-pager
probe systemctl --user list-unit-files --no-pager
probe bootctl status --no-pager
probe efibootmgr -v
probe ls -ld /boot /efi /boot/efi /usr/share/sddm/themes/breeze
probe ls -l /usr/lib/modules
probe ls -l /usr/lib/polkit-kde-authentication-agent-1

shopt -s nullglob
for path in /boot/vmlinuz* /etc/mkinitcpio.d/*.preset; do
  if [[ -r "$path" ]]; then
    case "$path" in
      /boot/vmlinuz*) probe file "$path" ;;
      *.preset) probe cat "$path" ;;
    esac
  else
    printf '\n[Not readable as current user: %s]\n' "$path"
  fi
done
if [[ -r /etc/mkinitcpio.conf ]]; then
  probe cat /etc/mkinitcpio.conf
fi
for dir in /etc/mkinitcpio.conf.d /etc/dracut.conf.d /boot/grub /boot/grub2 /boot/limine /efi/EFI/limine /boot/efi/EFI/limine; do
  if [[ -d "$dir" ]]; then probe ls -l "$dir"; fi
done
printf '\n%s\n' 'Share this report after reviewing it for private host/network identifiers.'
printf '%s\n' 'It reports evidence; firmware-selected loader, generator and graphical success still need operator confirmation.'
