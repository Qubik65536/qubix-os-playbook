# Boot visual design

Status: **Planned refinement** of the operator-confirmed Limine/native two-step design from
e7e652a. Menu, startup and reboot branding already work on the authorized target; the operator now
requests a more distinctive palette and GitHub Monaspace Krypton. This document defines that change
before implementation. Boot entries, kernel arguments, native cache/history and EFI binaries remain
Preserved under the existing [boot contract](boot.md).

## Visual direction

Use a shared midnight-blue background, muted steel-blue #56728b accents, ice-blue foreground and
subtle cyan highlights. Keep strong foreground/background contrast and a quiet composition.
The menu remains readable over restrained geometric Qubix artwork. Its selected entry should stand
out from secondary help text without hiding native entry names or recovery options. Plymouth keeps
the native two-step renderer, small circular animation and standard password/keyboard controls;
replace its generic white/black treatment with the same dark blue palette, tinted spinner and a
compact Krypton wordmark. Use the theme's gradient background consistently for boot/reboot/poweroff;
this intentionally replaces the firmware-background presentation within Plymouth, not firmware data.

## Typography and assets

Pin [GitHub Next Monaspace](https://github.com/githubnext/monaspace) v1.400 and record upstream
revision, source hashes, SIL OFL 1.1 and generation instructions. Its reserved font names require
renaming modified font software: distribute derivatives as **Qubix Boot Mono**, with explicit
attribution to Monaspace Krypton. This is a derived font name, not a claim to a new type design.

Limine 12 requires a raw 256-glyph CP437 bitmap font, eight pixels wide. Generate the complete
boot character set from Krypton at a measured fixed cell height; preserve box drawing, accented
characters and diagnostic symbols. Render a contact sheet before activation and test the real menu.
No TTF/WOFF file is handed directly to Limine. Supported font/help directives become explicit managed
appearance keys, with additive boot-accessible assets and FAT-aware modes.

For Plymouth, derive a static, renamed TTF subset covering the shipped labels, CP437 and extended
Latin/combining marks rather than every Monaspace family/weight. Retain a native fallback for text
outside that subset; document coverage. Install the subset only for the enabled splash component.
Resolve the exact font before generation, include it in the rebuild fingerprint, and verify the
actual active archives contain the font. Render the wordmark as paths/PNG so it does not depend on
runtime font discovery. Asset-generation tools are optional developer dependencies, not deployment
dependencies. Committed assets, manifests and licenses suffice for normal Ansible deployment.

## Recovery-compatible appearance upgrade

The confirmed target already has a graphical appearance baseline. Adding font/help directives must
not silently expand an older recovery contract. Permit only the exact previously shipped graphical
key set to gain the explicitly listed new font/help keys, and only when first-original bytes/hash,
the current receipt, original absence of those keys and current absence outside the Qubix block all
agree. Preserve original bytes, checksum, identity/mode, module aliases and every unrelated baseline
field. Record only the additional ownership metadata before activation. Check mode validates this
transition without writing it. Text-only/splash-only, missing/tampered baselines, duplicate aliases
and locally edited new directives must still fail safely. Other ownership expansion stays unsupported.

## Acceptance and activation

1. Validate provenance, font names/coverage, bitmap dimensions and deterministic generated checksums.
2. Inspect wordmark, spinner and menu-font contact sheet at their intended sizes.
3. Exercise fresh installation, earlier graphical-baseline upgrade, zero-change reapplication, exact
   restoration and refusal of stale/local edits in disposable filesystem fixtures.
4. Run the real native Plymouth preview in all three modes, including a password-prompt control,
   preserving host selection/daemon and cleaning up preview processes.
5. On the already authorized physical target, review a no-write preview, preserve original recovery
   records and native boot files, rebuild only the two confirmed matching images with --nopost,
   verify exact source/active images and reapplication, then perform the authorized guarded reboot.
6. Record console observations separately from file/parser/archive checks. Keep independent GRUB,
   dracut, LTS, real encryption and recovery acceptance gates open where untested.

The existing [physical test plan](../project/plymouth-test-plan.md) supplies exact image mappings and
the authorization/recovery boundary. The current request authorizes this visual refinement on that
same target; it does not authorize unrelated firmware, authentication or hardware changes.
