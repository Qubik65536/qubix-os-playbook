# MVP candidate implementation contract

Status: Implemented candidate; controller fixtures Tested and native acceptance pending. This document defined the contract before implementation. A candidate is ready for operator VM tests; MVP acceptance still requires the graphical/reboot matrix in [scope](../project/scope.md).

## Files, backups and state

Ordinary component roles prepare named file definitions after capability checks. A shared Ansible file role snapshots original content, UID/GID/mode and original absence before mutation, installs files, verifies hashes and records receipts. First baselines survive reapplication. Backups live under `/var/lib/qubix/backup/`, mode 0700; receipts and deployment revision/configuration digest are root-readable. The engine rejects symlinked paths, retains unlisted files and does not claim a cross-component transaction. Restore returns original files or removes originally absent files; local drift requires an explicit force option. Generated boot resources have separate backups and receipts. A failed rebuild remains pending and is retried; successful revision state is written last. Check mode creates no target backup/state and does not rebuild images.

## Desktop

Niri installs an additional **Qubix Niri** session with explicit `/etc/niri/qubix/config.kdl`; native system/user configuration remains untouched. The session explicitly uses measured Foot/jq and standalone Noctalia >=5.2.0 and <6.0.0, or fails with missing dependency/version evidence. Noctalia supplies the shell surfaces with a separate Qubix profile, as defined in the [desktop design](desktop-design.md). Parser validation must precede session activation. Wallpaper uses attributed reference artwork. Foot, bar and notification configuration live in Qubix-named paths. Bash defaults and an optional sourced Zsh fragment preserve personal files and the login shell.

## Login

Initial supported login adapter is an already-active SDDM with an installed compatible source theme. Clone its existing authentication/session UI into a Qubix namespace and customize supported background settings; never modify PAM or switch managers. Validate source resources and effective theme precedence. Other managers fail explicitly when selected. Login activation is independent of desktop installation.

## Bootloader

Both GRUB and Limine ship in the candidate. Modification requires explicit backend, active configuration path and `confirm_active: true`; tools/configuration candidates alone do not prove firmware selection. GRUB requires its active generated configuration to source `custom.cfg`, and uses an isolated appearance block in that hook, preserving entries/arguments. Limine supports documented shared directives for explicitly confirmed major versions 8–12; it changes only global branding/foreground/background directives. Unsupported or ambiguous versions fail before writes. Both preserve boot entries and arguments, back up activation/resources, and have independent preservation/reapplication/restore fixtures. No bootloader installer or disk commands run.

## Plymouth

A Qubix script theme and theme-selection file are separate from loaders. Both dracut and mkinitcpio adapters are required. Operators confirm the active generator and explicitly list image paths/kernel versions; mkinitcpio also names existing presets. Reject UKI/Secure Boot signing changes and ambiguous hook overrides. Insert only the Plymouth hook while preserving existing hook order, and require existing `splash` kernel argument rather than rewriting boot entries. Back up affected images before rebuilding, verify theme resources using the installed archive inspection tool, and persist pending rebuild state for retries/recovery. Restoration returns exact pre-change configuration and images; no unrelated generator settings are owned.

## Validation boundary

Controller fixtures use synthetic facts and temporary filesystem roots, never development-host boot paths. Static checks cover templates/schema; fake command tools test dispatch/failure handling only. Actual `niri validate`, SDDM preview/login, GRUB/Limine reboot, dracut/mkinitcpio generation and recovery require the installing CachyOS VM. The [user guide](../user/getting-started.md) and [human developer guide](../development/getting-started.md) provide prerequisites, commands, evidence collection, recovery and reporting.

Primary references: [Niri](https://github.com/niri-wm/niri/wiki/Getting-Started), [Limine v8 configuration](https://github.com/limine-bootloader/limine/blob/v8.x/CONFIG.md), [SDDM configuration](https://man.archlinux.org/man/sddm.conf.5.en), [mkinitcpio](https://man.archlinux.org/man/mkinitcpio.8.en), [dracut](https://man.archlinux.org/man/dracut.8.en).
