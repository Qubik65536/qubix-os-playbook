# Physical-target desktop test proposal

Status: In Progress; the operator explicitly authorized the package transaction, its native hook effects, desktop-only deployment and tests. Package preparation, native parsers, installation/verification, zero-change reapplication, nested rendering and original-absence recovery pass. See [actual results](desktop-test-results.md). Main-session acceptance remains open. This plan excludes login, bootloader and Plymouth activation; boot acceptance uses disposable VMs.

## Observed prerequisites

The target is a physical CachyOS ThinkPad running Niri 26.04 with Noctalia 5.2.1/Alacritty, active SDDM, Limine 12.9.3 and mkinitcpio 42.2. The classic Qubix companions were initially missing and are now installed. Native Niri accepts the production KDL; the invalid-file control fails as intended. Existing dotfiles and native system configuration remain preserved.

## Authorized package preparation

Install foot, fuzzel, waybar, mako, swaybg and starship with native Pacman. The current read-only resolution includes 17 dependencies (23 packages total); no kernel, loader or initramfs package is selected. Recheck the transaction immediately before execution.

The machine has native snap-pac pre/post hooks on every transaction and Limine snapshot integration. Normal package installation may create snapshots and refresh snapshot-related menu entries. Do not disable existing hooks to conceal these effects. The operator approval includes these native effects. The completed transaction changed limine.conf; the other 75 audited resources and default Fish shell remain unchanged. Kernel/initramfs files retain their original hashes. No explicit Qubix boot activation or image generation was run.

## Authorized deployment

Enable only branding, niri and shell. Install five attributed branding files, wallpaper, /etc/niri/qubix defaults, five /etc/qubix companion configurations, an additional Qubix Niri session, Bash/Zsh fragments and Starship defaults: 17 named resources plus protected backup/receipt/revision state. Native/personal Niri files, Noctalia/Alacritty and default shell remain preserved.

Preview first, then apply/verify the selected profile. Do not restart the display manager or interrupt the current session. The operator chooses Qubix Niri after logout when convenient. Record observed wallpaper/bar/launcher/notifications/terminal/navigation, original-file hashes, second-run zero managed changes and restoration. GUI privilege prompts remain an acceptance item: the optional KDE authentication agent is absent and must not be assumed available.

## Remaining independent work

Breeze is absent; the current login adapter cannot be selected on this target without further preparation or a validated adapter for an installed factory theme. Do not replace SDDM or install a desktop environment just to obtain a theme. GRUB is absent; both bootloaders and both image generators still need disposable-VM acceptance. No physical-machine loader theme, image rebuild or reboot is included here.

## Operator-authorized native-session retirement and reboot

Status: Native-entry backup/removal, reboot return and Qubix primary-session startup Tested. After the bar/shortcut deployment, the operator explicitly requested reboot and allowed removal of CachyOS's default Niri. This authorizes a target-specific exception to native session-entry preservation; it does not change the default playbook policy.

Keep the installed Niri compositor and native personal configuration: Qubix's session uses that compositor directly. On this inspected target the niri package owns /usr/share/wayland-sessions/niri.desktop, there is no separate cachyos-niri-settings package, and qubix-niri.desktop is now the only available session entry. Validate the installed Qubix KDL/Noctalia/plugin and inspect all configured session directories before retirement.

Back up the exact native desktop entry under the private /var/lib/qubix/retired-sessions/ directory before removing its login entry. Refuse redirected paths or a differing existing backup, and verify the backup before removal. Leave the display manager, its authentication configuration and personal dotfiles intact. This is an operator-directed host operation outside normal deploy/restore reconciliation; no package uninstall, loader change or initramfs generation is required. A package upgrade may recreate the native session entry.

Recovery from a TTY or SSH, before restoring/removing the Qubix session:

```bash
sudo install -o root -g root -m 0644 /var/lib/qubix/retired-sessions/niri.desktop /usr/share/wayland-sessions/niri.desktop
```

Reboot only after confirming Qubix remains the available session and its native validators pass. After reboot, check changed boot ID, returning SSH/SDDM and the selected primary session's configuration/layers. Physical keys, lock/unlock, portals and GUI authentication remain separate acceptance items. See the [recorded result](desktop-test-results.md#native-session-retirement-and-primary-startup).
