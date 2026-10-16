# Compatibility and discovery

Status: **Candidate adapters Implemented; fixtures Tested; native desktop file lifecycle/nested rendering Tested; full acceptance pending**.

| Selection | Supported candidate contract | Pending native acceptance |
|---|---|---|
| CachyOS Niri | Exact ID=cachyos, Linux/systemd/Pacman/Niri; measured Foot/jq and standalone Noctalia >=5.2.0 and <6.0.0 | Main-session keys/default shell/portals/Polkit/lock/unlock |
| Login | Active SDDM/Breeze, or Noctalia Greeter 1.6.x with explicit greetd preparation/existing mode | Native client preview Tested; greetd authentication/DRM/sessions/restore gates separate |
| Optional UI refinements | Private Noctalia 5.3.0/Greeter 1.6.0 with exact source/native/artifact provenance; GJS/GTK 4/fprintd for enrollment | Native simulated UI Tested; physical enrollment/login and compact-greeter boot pending |
| GRUB | Confirmed /boot/grub[2]/grub.cfg sourcing custom.cfg; native checker/tools | Checker/menu/original-entry boot/restore |
| Limine | Confirmed regular limine.conf under /boot or /efi, observed major 8–12 | Menu/original-entry boot/restore |
| dracut | Plymouth/two-step plugin/lsinitrd, existing splash token, confirmed plain images/kernel mapping | Generation/archive/splash/unlock/restore |
| mkinitcpio | Same splash requirements, lsinitcpio, literal main HOOKS plus literal append-only drop-ins, selected literal presets covering all outputs | Generation/hooks/archive Tested physically; splash/unlock/restore pending |
| Fedora/KDE | Unsupported, no adapters | Post-MVP |

UKIs/signing and complex/alternate mkinitcpio outputs are unsupported. Other login combinations
preserve login and reject enabled appearance; the Qubix desktop can use a free TTY.
The [Noctalia Greeter contract](../components/login.md) describes inactive preparation and
already-active greetd appearance; neither switches display managers or modifies PAM. Optional compact
mode selects a private UI client through a backed-up wrapper command; see the
[refinement contract](login-refinement.md).

The Plymouth picture background requires native two-step support for background.png and
ScaleBackgroundImage. Real-host preflight checks both capabilities in the installed plugin before
writes; isolated fixture plugins do not establish native rendering support. Other aspect ratios
may stretch the picture and need separate visual acceptance.

Discovery measures identity/version, binaries/packages, kernel arguments, alias/standalone manager activity, paths and hints. SSH hints can be absent. Tools alone cannot establish firmware selection or image ownership; operator confirmation is required.

The inspected CachyOS installation uses standalone Noctalia 5.2.1; the reference uses DMS. The [new desktop design](desktop-design.md) uses the installed Noctalia shell with Qubix-specific defaults/state and DMS-inspired shortcuts. Noctalia supplies its own Polkit agent. Legacy Quickshell/v4 is unsupported by this profile. Native preferences remain preserved; earlier classic-companion evidence below is historical.

Probe failures stay errors, not absence. Record combinations here only after [VM acceptance](../user/verification.md). Partial native desktop evidence is recorded below; no full MVP combination has passed yet.

## Protected discovery metadata

Current login follow-up (2026-10-16): the target now has Noctalia 5.3.0-1.1, Noctalia Greeter
1.6.0-1 and greetd 0.10.3-2.1. Native client rendering, file installation and zero-change
reapplication pass. The operator's subsequent reboot returns in greetd/Niri. The private compact
client is selected for a future greetd start and QubixOS desktop captions are active; physical
compact-client password/fingerprint login and recovery remain pending. The earlier
5.2.1/login-disabled observation below is historical. See [login evidence](../project/login-test-results.md).

A stock CachyOS target may mount /boot mode 0700. Ordinary discovery must fail permission errors instead of treating inaccessible configuration as absent. An explicit boolean operator variable, qubix_discovery_privileged (default false), permits only candidate-path metadata probes to use sudo. Enabled bootloader/Plymouth components also require this read access during discovery. This never authorizes loader installation, activation or image generation.

Use a typed extra variable with --ask-become-pass for privileged inspection. All other discovery probes remain ordinary user reads. Native acceptance requires zero reported changes and accurate candidate evidence on a real protected /boot target.

Observed physical target: CachyOS with Niri 26.04, Noctalia 5.2.1, Alacritty 0.17.0, SDDM 0.21.0, Limine 12.9.3 and mkinitcpio 42.2. Privileged read-only discovery passes with zero changes. Desktop install/verify/reapplication/absence restoration and isolated nested rendering also pass with Foot 1.28.0, Fuzzel 1.15.0, Waybar 0.15.0, Mako 1.11.0, Swaybg 1.2.2 and Starship 1.26.0. Native Fish/Noctalia/Alacritty configuration remains preserved. Breeze and the optional KDE agent are absent, so login is disabled and GUI privilege prompts remain unverified. Main-session and independent boot acceptance remain open. See [actual test evidence](../project/desktop-test-results.md).
