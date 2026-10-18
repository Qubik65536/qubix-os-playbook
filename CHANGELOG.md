# Changelog

Changes are grouped by release. Bootstrap has no release tag.

## Unreleased

- Add explicit CachyOS package preparation for Paru, Homebrew on Linux and WezTerm.
  Pin/verify the official Brew installer and keep it non-root; preserve personal files
  and existing Brew. Remove Alacritty/Foot only through dependency-safe Pacman removal.
  Require WezTerm for Qubix Niri and launch it from both terminal shortcuts and the
  session terminal environment. Operator-authorized SSH installation/removal, native
  rendering/parser checks, guarded shell activation and zero-change reapplication pass;
  comparison captures are recorded. Fresh Brew bootstrap and physical input remain pending.

- Enable bootloader appearance and Plymouth in the shipped profile too. Keep loader/generator
  confirmations false and machine mappings unresolved; reject unprepared activation before
  writes. Document explicit desktop-only opt-outs and test normal/check-mode safety gates.

- Enable fingerprint setup, Qubix captions, compact existing Noctalia/greetd login and
  KWallet in the shipped CachyOS Niri profile. Explain every effective default, resolution
  order, explicit opt-outs and separate fresh-machine preparation. Require future implemented
  features to ship enabled unless directed otherwise, with documented boot/hardware/personal
  preservation exceptions. Deployment still requires prepared packages/builds, an existing
  supported manager and reviewed secrets; no automatic fresh-machine setup is claimed.

- Add opt-in KWallet Secret Service selection and greetd password-unlock integration,
  native package preparation, backed-up provider/PAM resources and restoration fixtures.
  Preserve personal encrypted stores and unrelated authentication; keep GNOME Keyring
  installed when required by the distribution desktop package. Native migration and
  separate login acceptance are documented in the keyring guide. Native migration and both
  APIs pass; installed verification passes 67 tasks/zero changes and reapplication 209/zero changes.

- Add pinned official GitHub Monaspace NF installation (all 210 faces) with independently
  configurable Krypton UI defaults for Fontconfig, GTK schema defaults and Qubix Noctalia.
  Preserve saved user preferences, application font choices and boot typography. Add offline
  deployment preparation, strict source checks, cache/recovery handling, disposable normal/check
  fixtures and native reference/Krypton comparison screenshots. Clean d38d479 installation,
  107-task installed verification, live shell activation and 4,238-task zero-change reapplication pass.
  User settings, application windows, all 85 protected resources, earlier originals and boot identity
  remain preserved; no boot/image operation runs.

- Add a user/developer feature overview with implementation links and explicit distinctions
  between implemented behavior, test evidence and pending physical acceptance.

- Add an optional GTK 4/GJS fingerprint enrollment window with finger selection, measured progress,
  retry guidance, cancellation, saved-finger protection and explicit verification. Add separately
  installed, checksum-pinned UI-only Noctalia/Greeter builds for QubixOS captions and smaller,
  minimal steel-blue login controls. Preserve native binaries, PAM, system identity and output settings;
  native updates trigger startup fallback and stale-provenance refusal. Add a bounded requested
  Limine OS-title/native-target change, recovery instructions, fixtures and eight native comparisons.
  Physical scans, authentication and future greeter/menu appearance remain separate acceptance gates.
  Reuse the boot adapter's native enrollment-policy check for display-only menu changes, refusing
  enrolled/ambiguous EFI configuration before writing labels or persistent targets.
  Clean fc721e1 installation, installed verification, zero-change reapplication and a session-preserving
  Noctalia-only restart pass. The title-only menu change is installed from 14a0339; physical compact
  greeter/menu appearance and biometric login remain operator gates.

- Added Noctalia Greeter 1.6.x appearance preparation with the shared Qubix palette and cube wallpaper,
  preserved input/output/auth/session/sync settings and drift-safe file recovery. A separate native
  package playbook installs prerequisites alongside SDDM. Added login/cutover and fingerprint guides;
  native distribution identity and boot entries remain preserved. Authentication acceptance is separate.
  Clean b08727c installation, native preview, installed verification and zero-change reapplication pass.
  With operator approval, greetd is selected for the next boot while the SDDM desktop stays active.
  Guard legacy/overridden greetd configuration sources before appearance writes and retain exact
  selection recovery. Existing PAM stays unchanged; native packages integrate their new greetd session.

- Restore lower-left power-menu prompts and lower-right Cancel, and defer confirmed actions until
  the native close animation completes so Lock cannot leave the countdown visible at one second.
  Require committed screenshot comparisons for visual customizations. Clean e80b697 native no-effect
  regression, deployment, live footer and zero-change reapplication pass; physical lock/unlock pending.

- Corrected power-tile content centring and native panel height, removed the extra footer,
  and restored Noctalia’s destructive Shut Down palette in both guarded and native menus.
  Clean 78cc3e1 installation, live five-button comparison and zero-change reapplication pass.

- Restyled the guarded power menu to follow Noctalia's original horizontal icon tiles, number
  badges and bar-attached placement, retaining key holds and cancellable click countdowns.
  Clean f1a28b1 native comparison, installation, installed verification and zero-change reapplication
  pass. A shell-only restart refreshes cached manifest geometry while preserving Niri, apps and preferences.

- Added a guarded Qubix Power options panel: hold keys 1–5 for three seconds (release cancels),
  or click for a cancellable five-second countdown. Clean d415856 native validation/rendering,
  installation, live reload, installed verification and zero-change reapplication pass with
  protected configuration and recovery baselines preserved; physical cancellation acceptance remains open.

- Made the Plymouth bottom wordmark smaller and lower, doubled the logo/text layout gap and
  applied the shared steel-blue accent to lettering while preserving original logo colours.

- Added an explicit native Plymouth early-simpledrm selection and DRM renderer archive checks for
  blank startup/text-fallback diagnosis. Clean 0324e27 activation, exact four-image/font/pin checks,
  preservation and unchanged reapplication pass; the operator confirms the repaired startup splash
  and return to the desktop after a normal reboot.

- Restored Plymouth's original logo colours and added a native scaled desktop-cube background with a pixel-preservation guard. Native all-mode/prompt previews, exact source/active-image checks, zero-change reapplication and normal-kernel boot health pass after clean e3bf16b deployment; renewed console acceptance is pending.

- Increased boot-screen contrast, removed decorative captions, reduced the Limine font to 1x1 and reused the detailed desktop cube wallpaper. Clean f626188 deployment, exact four-image/pin verification, zero-change reapplication and normal-kernel reboot pass; renewed console acceptance is pending.
- Deployed the Krypton refinement from clean 87e824b: four-image/font verification, zero-change reapplication and normal-kernel reboot pass; the operator requests the contrast/layout correction above.

- Added Krypton-derived CP437 text, midnight cube artwork and distinct heading/help/selection colours to Limine 12. Guarded earlier graphical-baseline enrollment preserves original recovery bytes/fields; normal and no-write upgrade fixtures pass.

- Refined Plymouth with a midnight-blue gradient, original ice-blue vector ring and outlined Krypton wordmark. Native all-mode/prompt preview selects the exact renamed subset and preserves the host; the higher-contrast, caption-free refinement is deployed.

- Added reproducible, OFL-attributed Krypton-derived boot font assets: a renamed 154 KB Latin subset and complete 5 KB CP437 bitmap.

- Deployed graphical Limine and native-style Plymouth from clean e7e652a; exact source/active-image assets, pins, installed verification and preservation pass. Identical-source reapplication completes with zero changes. The normal-kernel reboot returns Qubix at 100% scale, and the operator confirms menu/startup/reboot branding.

- Added explicit Limine cache bindings, verified content-addressed image staging, native BLAKE2b pin activation and config-first recovery; native cache/history/EFI files remain preserved.
- Added FAT-aware boot asset permissions and safe refusal of ambiguous image references, stale recovery pins and narrower earlier appearance ownership.

- Replaced the rejected scripted splash with a native two-step spinner, modest Qubix watermark and attributed neutral input assets; archive checks cover all runtime assets.

- Added graphical Limine 12 defaults with Qubix wallpaper, palette and font/margin settings, exact recovery metadata and refusal of shadowed/enrolled configurations; fixtures pass.

- Added branded circular Plymouth animation with boot, reboot and poweroff captions; native isolated parser/rendering/prompt tests pass. Image verification now requires label plugins and fonts; actual boot activation remains separate.

- Preserved literal mkinitcpio hook appends while validating effective Plymouth/encryption order; unsafe mutations and duplicate Plymouth hooks fail in fixtures.

- Added a 32 px information bar inspired by the olive-dusk reference, bounded application titles, CPU/RAM/temperature widgets and optional media; native wide-preview/title checks pass.

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
