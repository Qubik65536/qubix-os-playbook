# Boot visual design

Status: **Implemented and deployed from clean 87e824b; normal-kernel reboot works;
contrast/layout correction deployed from clean f626188 and native-preview/image/reapplication/reboot Tested;
renewed console acceptance pending**.
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
compact, near-white Krypton wordmark with the original, unmodified Qubix cube colours. Never tint,
recolour or filter the logo; contrast adjustments apply to text, backgrounds and supporting accents.
Use a blue-charcoal picture background, fallback gradient and brighter ring consistently for boot/reboot/poweroff;
this intentionally replaces the firmware-background presentation within Plymouth, not firmware data.

### Original-colour logo and picture background correction

Status: **Implemented and deployed from clean e3bf16b; native preview, image checks, zero-change
reapplication and normal-kernel boot health Tested; renewed console acceptance pending**,
following operator feedback on f626188. Its blue logo tint is rejected.
Render the canonical logo.svg directly, retaining its original colours and shading. Keep the
near-white caption-free wordmark and spinner. Add a subtle desktop-cube picture on a blue-charcoal
background using native two-step's background.png and ScaleBackgroundImage support; keep its central
prompt area quiet. Retain a blue-charcoal gradient as the fallback. Scaling follows the native
renderer rather than a custom splash script; non-16:9 outputs may stretch the picture and require
separate visual acceptance. Confirm background rendering in native Pango/FreeType previews, compare
the rendered logo crop against the canonical logo, and verify the picture in actual boot archives.
Kernel mappings, Limine appearance, first recovery bytes and native prompt behaviour stay unchanged.

### Subtle bottom wordmark refinement

Status: **Implemented; local asset validation Tested; native activation pending**. Reduce the logo from 72 to 54 px and lettering from 25 to 19 px,
increase the layout gap from 6 to 12 px, and move native watermark vertical alignment
from .93 to .96. Use the shared steel-blue #56728b accent for lettering only.
Acceptance: regenerate the outlined asset deterministically, preserve the canonical logo
pixels at its new size, validate manifest/configuration and inspect a composition preview.
Two Inkscape exports reproduce identical committed assets; canonical logo pixels and static
validation pass. The 1920x1080 composition is inspected. The existing generator fixture
passes 521 tasks with ten expected refusals.
Native rendering, installation/image verification and console appearance are separate gates;
retain existing background, spinner, prompts and early-simpledrm selection.

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
