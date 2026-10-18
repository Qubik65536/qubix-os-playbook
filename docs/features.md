# Implemented features

Qubix OS Playbook customizes an existing **CachyOS Niri** installation with Ansible.
It supplies a coherent desktop, login and boot appearance, plus tools to deploy,
verify and restore the files it owns. It does not build an operating-system image.

This overview is for users deciding what to enable and developers finding the code.
It lists implemented behavior, briefly explains its implementation and links to the
authoritative contracts. Implemented means the code exists; physical login and boot
acceptance are reported separately below.
Evidence is current as of **2026-10-17**; see [project status](project/status.md)
for exact revisions and test results. The shipped profile enables implemented desktop,
compact Noctalia login, fingerprint setup, captions and KWallet; review the
[effective defaults and preparation requirements](architecture/configuration.md).
Boot/splash also default enabled and require explicit machine-specific mappings/confirmations; fresh-machine setup is not automatic.

## Desktop and everyday use

| Feature | What you get and how it works | Code and details |
|---|---|---|
| Monaspace NF and optional Krypton UI | All 210 official GitHub Monaspace NF faces install with attribution and checksums. A separate boolean selects Krypton for generic Fontconfig families, GTK defaults and Qubix Noctalia while preserving saved user/application font choices. | [Font role](../roles/qubix_fonts/tasks/main.yml), [font contract](components/fonts.md), [native comparisons](project/font-test-results.md) |
| Shared Qubix appearance | Original-colour cube logo, wallpaper and a shared steel-blue palette. Ansible installs attributed assets under `/usr/share/qubix`; desktop and login templates reuse them. | [Branding role](../roles/qubix_branding/tasks/main.yml), [branding contract](components/branding.md) |
| Separate Qubix Niri session | Select **Qubix Niri** at login for rounded windows, wallpaper, Foot terminal and Noctalia bar, launcher, notifications and companion integration. System templates provide defaults while preserving native and personal configurations. The output helper initially selects 100% scale without changing resolution or refresh rate. | [Desktop rendering](../roles/qubix_niri/tasks/render.yml), [Niri contract](components/niri.md) |
| Shortcuts and searchable help | Window/workspace navigation, application launchers and resizing, plus **Super+Shift+/** for the shortcut panel. Deployment extracts labelled bindings from the actual Niri configuration into the local Noctalia plugin. | [Bindings](../roles/qubix_niri/templates/config.kdl.j2), [shortcut plugin](../roles/qubix_niri/files/shortcuts), [desktop design](architecture/desktop-design.md) |
| Guarded power menu | **Super+X** opens five native-style action tiles. Hold a number key for three seconds or click for a cancellable five-second countdown. A local Noctalia plugin handles cancellation and dispatches only after the panel closes. | [Power plugin](../roles/qubix_niri/files/power), [behavior contract](architecture/desktop-design.md#power-action-countdown) |
| Shell and terminal defaults | Foot styling and optional Starship prompt defaults. System fragments respect existing user settings; Bash can initialize Starship, and Zsh adoption is manual. The account's default shell stays unchanged. | [Shell role](../roles/qubix_shell/tasks/main.yml), [shell contract](components/shell.md) |
| QubixOS desktop captions | Default launcher footer **QubixOS** and Control Center heading **QubixOS (Noctalia v5.3.0)**. A pinned private Noctalia build changes two captions; native package binaries and CachyOS system identity remain intact. Native updates trigger fallback until the private build is refreshed. | [UI patches and provenance](../assets/ui/README.md), [variant selection](../roles/qubix_niri/tasks/variant.yml), [configuration guide](user/login.md) |

Desktop installation, parser/rendering checks and zero-change reapplication are tested.
Focused live checks also cover the power panel and QubixOS captions. Complete
primary-session and physical lock/unlock acceptance remain separate; see
[desktop evidence](project/desktop-test-results.md) and [UI evidence](project/ui-test-results.md).

## Login and fingerprint setup

| Feature | What you get and how it works | Code and details |
|---|---|---|
| Noctalia Greeter theme | Matching palette and wallpaper, with the default compact card, smaller controls and reduced decoration. Appearance templates preserve native input, output, session and authentication settings; compact mode uses a pinned private Greeter build. Separate preparation installs prerequisites. Ordinary deployment does not switch display-manager services. | [Login role](../roles/qubix_login/tasks/main.yml), [compact adapter](../roles/qubix_login/tasks/compact.yml), [login guide](user/login.md) |
| Existing SDDM/Breeze branding | An alternative adapter for supported installed SDDM/Breeze. It copies the installed theme with authentication QML unchanged and applies appearance settings through a backed-up selection drop-in. | [SDDM adapter](../roles/qubix_login/tasks/sddm.yml), [login contract](components/login.md) |
| Graphical fingerprint enrollment | Open **Fingerprint setup** from **Super+Space**. Select a finger, explicitly start enrollment, follow measured progress/retry guidance, cancel or test the reader. A GTK 4/GJS application talks to fprintd over D-Bus; fprintd owns biometric data and authorization. Existing enrollments are protected. | [Application](../roles/qubix_niri/files/fingerprint), [installation](../roles/qubix_niri/tasks/fingerprint.yml), [fingerprint guide](user/fingerprint.md) |
| KWallet secret storage | Default Secret Service and KDE Wallet API integration with bounded greetd PAM hooks and Niri startup. Existing secrets require reviewed migration; GNOME Keyring remains installed if required by package dependencies. | [Keyring role](../roles/qubix_keyring/tasks/main.yml), [guide](user/keyring.md), [native evidence](project/keyring-test-results.md) |
| Fingerprint login instructions | A manual guide covers reader support, enrollment, native authentication configuration and password fallback. The fingerprint feature does not modify PAM or automatically enable biometric login; the separate KWallet feature has a bounded PAM exception. | [Fingerprint guide](user/fingerprint.md), [refinement contract](architecture/login-refinement.md) |

Noctalia Greeter installation/reapplication and native rendering are tested. The
fingerprint controller has 32 automated cases plus native GJS tests against a simulated
fprintd service. **Real scans, biometric/password login and the compact greeter's
physical appearance still need operator acceptance.** SDDM has fixture coverage;
physical login/restore is pending. [Login evidence](project/login-test-results.md) and
[UI evidence](project/ui-test-results.md) contain the comparisons and limitations.

## Boot menu and splash

| Feature | What you get and how it works | Code and details |
|---|---|---|
| Limine appearance | Cube wallpaper, restrained colours and smaller Krypton-derived menu text on supported graphical Limine versions. The adapter changes bounded appearance settings while preserving entries, snapshots, defaults and kernel arguments. | [Limine adapter](../roles/qubix_bootloader/tasks/limine.yml), [bootloader contract](components/bootloader.md) |
| QubixOS Limine OS label | A separate, explicitly confirmed operation renames the selected CachyOS menu heading to **QubixOS** and sets the native generator's target label. Guards preserve boot payloads, IDs, arguments and snapshot structure. | [Menu-label playbook](../playbooks/menu-label.yml), [label tasks](../roles/qubix_bootloader/tasks/menu_label.yml), [operator guide](user/login.md) |
| GRUB appearance | A Qubix theme and additive configuration for a proven existing GRUB setup. Native syntax validation runs before activation; the adapter does not install a bootloader or regenerate the full menu. | [GRUB adapter](../roles/qubix_bootloader/tasks/grub.yml), [bootloader contract](components/bootloader.md) |
| Plymouth splash | Native two-step animation with the original-colour Qubix logo, cube background, wordmark and spinner, including password-prompt artwork. Templates and assets customize the installed Plymouth plugin. | [Plymouth role](../roles/qubix_plymouth/tasks/main.yml), [Plymouth contract](components/plymouth.md) |
| dracut and mkinitcpio integration | Explicit kernel/image mappings, conditional rebuilds and archive-content checks put the theme into selected initramfs images. Optional native Limine image binding updates only the selected image reference and checksum pins. Recovery guards reject stale kernel/image relationships. | [Plymouth task files](../roles/qubix_plymouth/tasks), [boot design](architecture/boot-design.md), [splash guide](user/plymouth.md) |

Both loader adapters and both image generators have fixture coverage. The authorized
native Limine/Plymouth path has installation, image-content, reapplication and earlier
successful boot evidence. **The newest menu label/visual refinements and independent
GRUB/dracut boot and recovery combinations still require acceptance.** See
[current status](project/status.md); installation alone is not proof of a successful boot.

## Deployment, verification and recovery

| Feature | What you get and how it works | Code and details |
|---|---|---|
| Read-only discovery and strict configuration | Inspect native identity, tools, services and boot evidence before deployment. Typed defaults/profile/operator settings are validated; unsupported enabled combinations and ambiguous boot selections fail before component writes. | [Profile role](../roles/qubix_profile/tasks/main.yml), [discovery role](../roles/qubix_discovery/tasks/main.yml), [configuration](user/configuration.md) |
| Repeatable deployment and installed verification | Ordinary Ansible roles render named resources, validate supported native syntax and verify installed content. `bootstrap.sh` exposes verify/deploy/restore; check mode previews supported operations. Separate preparation playbooks handle narrowly selected prerequisites. | [Deploy playbook](../playbooks/deploy.yml), [installed verification](../playbooks/tasks/verify-installed.yml), [deployment guide](user/deployment.md) |
| Backups, drift checks and restoration | The shared file engine records original bytes, ownership, modes and original absence, then retains applied receipts. Restore detects unexpected edits instead of overwriting them. Revision/configuration digests and pending/failure records distinguish completed installation from interrupted work. | [File engine](../roles/qubix_files/tasks), [state role](../roles/qubix_state/tasks), [restoration guide](user/restoration.md), [ownership contract](architecture/configuration.md) |
| Developer checks and visual evidence | Local lint, syntax/schema/link checks, isolated Ansible fixtures, controller tests and native previews exercise behavior without treating previews as live login/boot proof. Sanitized reference/custom screenshots accompany visual changes. | [Validation script](../scripts/validate.sh), [fixture runner](../scripts/test.sh), [developer guide](development/getting-started.md), [testing guide](development/testing.md) |

General package/system management, Fedora and KDE support are **Planned**, not implemented
features. Full MVP acceptance is **In Progress**. Start with the
[user guide](user/getting-started.md) to try the desktop, or the
[developer guide](development/getting-started.md) to change it; use the
[backlog](project/backlog.md) for remaining work.
