# Project scope

The reproducibility boundary is **Qubix-managed configuration** on an existing distribution. Preserve native package management, distribution identity, boot entries, kernel arguments, encryption settings, hardware configuration, and personal dotfiles.

## Bootstrap acceptance

Documentation precedes source. Atomic Conventional Commits record the foundation. Ansible provides executable read-only CachyOS discovery, a loadable `cachyos-niri` profile, strict configuration validation, non-destructive verification, and static CI. Unsupported hosts must fail explicitly. Capabilities must be described by their actual verification level. A small additive branding capability may follow validated infrastructure.

## MVP acceptance

A disposable CachyOS Niri VM receives a working graphical Qubix desktop through one documented procedure. It includes shared artwork, wallpaper, detected companion applications, shell and terminal defaults, and supported login branding. Existing personal configurations remain intact unless a separate explicit adoption mechanism is selected.

Both GRUB and Limine must independently pass boot and recovery tests. Plymouth must pass both dracut and mkinitcpio tests. Reapplication must be idempotent, configuration preservation and restoration verified, and deployed revisions traceable. Syntax validation alone does not establish graphical or boot success.

## Non-goals

No distribution, custom ISO, image builder, BlueBuild/bootc replacement, replacement for Pacman/DNF, declarative whole-system manager, general provisioning framework, or kernel/hardware/encryption manager. No Fedora or KDE implementation during bootstrap. No new Python application or custom adapter framework.

## Ownership and safety

[Ownership](../architecture/configuration.md) governs every resource. [Boot safety](../architecture/boot.md) governs privileged boot operations. Development may write repository files and disposable test fixtures; deployment to a real machine is a separate operator action.
