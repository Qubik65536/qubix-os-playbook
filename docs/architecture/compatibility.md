# Compatibility and discovery

Status: **Candidate adapters Implemented; fixtures Tested; live compatibility unverified**.

| Selection | Supported candidate contract | Pending native acceptance |
|---|---|---|
| CachyOS Niri | Exact ID=cachyos, Linux/systemd/Pacman/Niri; measured Foot/Fuzzel/Waybar/Mako/Swaybg | Parsers, companions, session |
| Login | Unambiguously active SDDM, regular compatible Breeze tree | Preview/authentication/sessions/restore |
| GRUB | Confirmed /boot/grub[2]/grub.cfg sourcing custom.cfg; native checker/tools | Checker/menu/original-entry boot/restore |
| Limine | Confirmed regular limine.conf under /boot or /efi, observed major 8–12 | Menu/original-entry boot/restore |
| dracut | Plymouth/script plugin/lsinitrd, existing splash token, confirmed plain images/kernel mapping | Generation/archive/splash/unlock/restore |
| mkinitcpio | Same splash requirements, lsinitcpio, literal main HOOKS/no overrides, selected literal presets covering all outputs | Generation/hooks/archive/splash/unlock/restore |
| Fedora/KDE | Unsupported, no adapters | Post-MVP |

UKIs/signing and complex/alternate mkinitcpio outputs are unsupported. Other managers preserve login and reject enabled branding; the Qubix desktop can use a free TTY.

Discovery measures identity/version, binaries/packages, kernel arguments, alias/standalone manager activity, paths and hints. SSH hints can be absent. Tools alone cannot establish firmware selection or image ownership; operator confirmation is required.

Reviewed CachyOS uses Noctalia/Quickshell and the reference uses DMS. This candidate supplies a separate classic companion session after measuring prerequisites, preserving native configuration. The CachyOS KDE authentication agent starts only if measured. Actual target services/versions still need inspection.

Probe failures stay errors, not absence. Record combinations here only after [VM acceptance](../user/verification.md). No live combination has been verified yet.
