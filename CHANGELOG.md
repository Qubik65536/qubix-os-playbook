# Changelog

Changes are grouped by release. Bootstrap has no release tag.

## Unreleased

- Added 100% output-scale defaults at Qubix session startup/new connection, preserving existing-output session adjustments and native monitor files; lifecycle fixtures pass.

- Corrected the undersized bar logo with launcher-only 2x scaling and made separate module outlines more visible; native before/after previews, live reload, installed verification and zero-change reapplication pass.

- Added pinned launcher power controls and global session-action search; refined the bar using Ryoku showroom inspiration and disabled the dock/bottom reservation. Native preview, primary-session reload, installed verification and zero-change reapplication pass.

- Documented cheatsheet regeneration in README and added labelled window-resize shortcuts with complete generated-binding coverage and native sizing checks.

- Separated Noctalia bar widgets into rounded capsules on a transparent surface; native preview and preservation checks pass.
- Added a searchable Noctalia shortcut panel with category cards/keycaps, generated from managed Niri bindings; open it from the bar or Super+Shift+/.

- Adopted a Noctalia 5 desktop profile with #56728b accents, rounded windows/bar/dock and DMS/macOS-inspired shortcuts.
- Added measured Noctalia version guards, native TOML validation and palette/terminal colour consistency checks.
- Isolated Qubix shell state/data and Noctalia dark-mode writes while preserving application settings.
- Updated the native preview for production candidates, direct SDDM launches, Noctalia IPC and native configuration preservation.

- Established project scope, architecture, safety requirements, and development workflow.
- Added local Ansible controller configuration and locked development dependencies.
- Added strict profile resolution, CachyOS Niri discovery, read-only verification/preflight and a minimal Bash entrypoint.
- Added supported/unsupported host, identity, schema, merge, and ambiguity fixture coverage.
- Added matching local/CI YAML, Ansible, ShellCheck, Markdown, configuration-consistency and fixture validation.
- Added focused Issue and PR templates.
- Added licensed shared artwork, safe named-file deployment, checksum/metadata verification and explicit installed-branding verification.
- Tested branding preview, idempotency, repair, corruption/missing diagnostics, symlink rejection and unrelated-file preservation in temporary filesystems.
- Graphical login/session, native image generation and reboot acceptance remain pending VM testing.

- Added first-baseline file backups, applied checksums, drift-safe restoration and revision-state tasks.
- Added an isolated Qubix Niri session, detected companion prerequisites, wallpaper and Bash/terminal defaults.
- Added SDDM native-UI cloning, supported background overrides and checked theme-selection precedence.
- Added opt-in GRUB custom-hook and Limine 8–12 appearance adapters with active-path confirmation and backups.
- Added a Qubix Plymouth script theme, dracut/mkinitcpio integration, conditional verified regeneration and kernel-aware image recovery.
- Added auditable pending/failure state alongside last verified deployment revision.
- Fixed standalone SDDM detection, conflicting-manager rejection and redirected factory theme preflight.
- Added optional measured CachyOS Polkit agent startup to the separate Qubix Niri session.
- Fixed Starship default selection to preserve existing user configuration precedence.
- Added a read-only VM information collector and target evidence guide.
- Extended each bootloader fixture through real baseline installation, reapplication and exact restoration.
- Fixed rejection of compact deployment tag arguments to keep component selection in YAML.
- Preserved existing activation-file modes and allowed privileged read-only checks for private login/boot/splash configuration.
- Added desktop-first user onboarding, human-developer onboarding and an explicit native MVP acceptance checklist.
- Made user/developer onboarding links prominent and documented the SSH access handoff for live inspection.
- Added pre-authentication SSH timeout diagnostics and clarified password authentication with the pinned controller.
- Added explicit privileged metadata discovery for private boot directories.
- Corrected Niri validator option order and added a reusable native temporary-file grammar test, passing on Niri 26.04.
- Prepared a physical desktop test proposal with explicit package-hook and deployment scope for operator review.
- Added native Fuzzel pre-activation validation and repeatable Foot/Fuzzel production/invalid-control grammar tests.
- Added an optional native Ansible desktop smoke workflow with isolated session, screenshot/log evidence and cleanup.
- Fixed stale GRUB/Limine activation restoration after preserved content changes and reapplication; force cannot bypass the guard.
- Recorded native desktop package preparation, installation, zero-change reapplication, nested rendering, preservation and original-absence restoration; updated operator/developer onboarding and README links.
