# Compatibility and discovery

Status: **Planned**; no host combination is integration-tested yet.

| Target | Bootstrap contract | MVP validation |
|---|---|---|
| CachyOS + Niri | Linux, exact `ID=cachyos`, executable Pacman/Niri | Disposable VM graphical session |
| GRUB | Report installed/configuration evidence only | Independent boot + preservation + recovery |
| Limine | Report installed/configuration evidence only | Independent boot + preservation + recovery |
| dracut | Report installed executable only | Plymouth resources, reboot + recovery |
| mkinitcpio | Report installed executable only | Plymouth resources, reboot + recovery |
| Fedora/KDE | Explicitly unsupported | Post-MVP |

Discovery returns OS identity/version, executable and installed package evidence, desktop/session hints, display-manager link and activity, boot configuration candidates, and initramfs candidates. Session hints can be absent over SSH or privilege escalation; never use them as the only proof of Niri availability. Ambiguous active bootloader/initramfs selection stays unresolved.

Companion availability is measured before choosing startup, wallpaper, notifications, launcher, and terminal commands. The reviewed CachyOS settings use Noctalia through Quickshell; the BlueBuild reference uses DMS. Neither choice is imposed without inspecting an actual target. Supporting evidence includes terminal, launcher, bar, notification, wallpaper, and desktop-shell binaries plus relevant configuration directories.

Permission or probe errors fail with context. Unsupported hosts are rejected without writes. Version compatibility is recorded as **unverified** until real VM evidence exists; package presence alone does not establish support for a feature directive.
