# Boot visual design

Status: **Implemented and deployed from clean 87e824b; normal-kernel reboot works;
contrast/layout correction Implemented and native-preview Tested, activation pending**.
This refines the operator-confirmed Limine/native two-step design from e7e652a.
Menu, startup and reboot branding already work on the authorized target; the operator now
requests a more distinctive palette and GitHub Monaspace Krypton. This document defines that change
before implementation. Boot entries, kernel arguments, native cache/history and EFI binaries remain
Preserved under the existing [boot contract](boot.md).

## Visual direction

Use a shared near-black blue background, steel-blue #56728b accents and near-white foreground.
The first midnight revision boots successfully, but the operator finds both screens low contrast,
the menu text too large and decorative captions unnecessary. Correct those issues by reusing the
desktop's detailed cube wallpaper, darkening the menu surface and brightening text/help. Keep only
the native Qubix OS heading; omit wallpaper slogans and Plymouth's PLAYBOOK caption/underline.
Render the existing 8x20 menu font at 1x1 instead of 2x2. Limine selects entries using reverse video,
so its normal foreground/background pair must remain strongly contrasting; the bright background
setting alone does not define the selected row. See the [native renderer](https://github.com/Limine-Bootloader/Limine/blob/v12.x/common/menu.c).
Plymouth keeps the native two-step renderer, small circular animation and standard password/keyboard controls;
replace its generic white/black treatment with the same dark blue palette, tinted spinner and a
compact, near-white Krypton wordmark with a brighter shaded cube. Use a darker gradient and brighter
ring consistently for boot/reboot/poweroff;
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

For Plymouth, derive a static, renamed TTF subset covering the shipped labels, available CP437 and
extended Latin/combining marks rather than every Monaspace family/weight. Preserve native host fonts
and document coverage. The installed freetype renderer uses its packaged Plymouth.ttf directly;
early-boot text outside the subset is unvalidated and has no promised font fallback. Install the subset
only for the enabled splash component.
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
   For the contrast correction, inspect the desktop-derived wallpaper, caption-free wordmark and
   native animation/prompt previews; verify reduced menu scale and preserved configuration in fixtures.
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
