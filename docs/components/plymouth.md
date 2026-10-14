# Plymouth and initramfs adapters

Status: Implemented candidate. Both generator plans, simulated dispatch/idempotency, check-mode isolation and kernel-aware restoration guards are Tested. Actual archive generation, splash and encryption prompts need VMs.

The named script theme manages logo, normal/message/question/password display callbacks and selection in `/etc/plymouth/plymouthd.conf`. Existing ShowDelay and unrelated settings remain preserved. Password callbacks display only a bullet count; the script does not log or store password input. Require an installed script plugin, an existing `splash` kernel argument and explicit generator confirmation. Kernel arguments are never rewritten.

`plymouth.images` maps each existing plain initramfs path to an installed kernel version and its unchanged kernel_image path. The adapter snapshots every affected image before regeneration. Image backups record the associated kernel hash; restoration refuses stale images after a kernel change, even with a drift override. UKI generation/signing is outside current support.

Dracut receives only an additive module drop-in and generates explicit images with `--no-uefi --force image kernel`. Mkinitcpio supports one literal main HOOKS array, inserts Plymouth after systemd/udev and before encryption, and preserves other hook ordering/settings. Competing HOOKS overrides, complex/alternate preset configuration and UKIs fail. Declared images must exactly cover selected preset outputs, including fallback images. `--nopost -p preset` prevents native post hooks from modifying boot entries.

An input fingerprint skips unchanged regeneration. A pending marker survives failure and triggers retry; `force_rebuild: true` permits an explicit repair and should then return to false. Native `lsinitrd` or `lsinitcpio` checks for theme files, daemon and script plugin. Image receipts and success fingerprint are committed only after those checks; kernel hashes must remain unchanged.

Check mode performs no image generation, image backups or success-marker writes. Operator acceptance separately requires dracut and mkinitcpio native generation, a real reboot/splash, encrypted-root input where relevant, unchanged entries/arguments, reapplication and restoration. See [restoration](../user/restoration.md).
