# Bootloader component

Status: **Planned**. **GRUB and Limine are both required for MVP** and have separate acceptance tests.

Manage theme resources and supported appearance directives only. `bootloader.enabled` defaults false; `backend` is `auto`, `grub`, or `limine`. Dependencies include branding, active boot-chain evidence, installed-version support, backups, and a recoverable VM. Explicit backend selection still requires validation of the active configuration path.

GRUB uses its theming mechanism with minimal activation changes. Limine uses only directives its installed version supports. Preserve boot entries, kernel arguments, encryption and hardware parameters. Never install or switch bootloaders for appearance. See [boot architecture](../architecture/boot.md) for selection and safety requirements.

Verification includes syntax where available, generated output inspection, unchanged entry/argument evidence, reapplication, and independent VM boot. Restoration reverses activation and returns exact prior configuration before rebuilding necessary output. Document paths and live-media instructions per adapter before accepting the change. No executable adapter exists yet.
