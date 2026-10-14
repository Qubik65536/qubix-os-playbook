# Plymouth and initramfs

Status: **Planned**. Independent of bootloader selection.

Install a Qubix-named splash theme and select it through supported Plymouth configuration. `plymouth.enabled` defaults false. `initramfs_backend` is `auto`, `dracut`, or `mkinitcpio`; ambiguity must fail rather than guess. Dependencies: installed Plymouth, branding, active image generator evidence, backup/recovery support.

Internal ordinary Ansible task files provide dracut additive configuration or minimal mkinitcpio hook changes. Preserve unrelated configuration and ordering constraints. Regenerate only appropriate affected images on changed inputs. Do not copy the reference's complete spinner override or image-generation module.

Acceptance separately for each generator: source/theme validation, expected resources in generated images, unchanged unrelated settings, idempotent reapplication, rebooted VM splash, and restoration to the prior splash. Recovery includes original configuration/theme selection and necessary image rebuild. No theme activation, image rebuild, or restoration command is currently operational.
