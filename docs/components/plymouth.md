# Plymouth and initramfs adapters

Status: **Corrective implementation deployed and normal-kernel startup/reboot appearance confirmed;
Krypton/midnight refinement Implemented and native-preview Tested, activation pending**. Native
two-step rendering, mkinitcpio generation, exact source/active-image contents, installed verification
and completed zero-change reapplication pass for e7e652a.
The first scripted attempt failed visual acceptance; see [recorded results](../project/plymouth-test-plan.md).
Dracut, encrypted-root input and recovery retain independent acceptance gates.

## Active Limine image repair

Status: **Implemented; two-image lifecycle/refusal/recovery fixtures and target no-write preview Tested**. CachyOS Limine entries load extensionless cached initramfs files and verify BLAKE2b digests, rather than loading the generator's /boot/initramfs-*.img outputs. Before writes, bind each source image explicitly with optional limine_image and limine_kernel_image fields. Both must identify existing regular files on the confirmed /boot ESP, the cached kernel must equal the declared source kernel, and exactly one primary module/kernel pair must match in the selected Limine configuration. Require a confirmed Limine backend/configuration; reject missing/ambiguous bindings and unsupported enrollment instead of reporting activation success.

After generation, stage verified image copies under a Qubix-owned, content-addressed /boot/qubix/plymouth/ path. Preserve native cache and snapshot images. Atomically update only explicitly bound module_path values and their native BLAKE2b digests after the staged files are ready. Entry identities, kernel paths/hashes, arguments, snapshot entries and EFI binaries remain Preserved. Capture original config and stage-file absence baselines; keep image kernel-hash guards. Record owned module aliases in config recovery metadata so restoration can distinguish these expected pointer changes from native entry drift. Reapplication must reuse the same files and skip regeneration; installed verification must inspect the actual referenced images and hashes.

Recovery must restore the retained Limine configuration before deleting any staged image. Verify
the original native cache and cached kernel against their recorded hashes first; force cannot bypass
stale pins or unrelated entry drift. Earlier appearance-only baselines may gain alias metadata only
when their intact original configuration contains the exact original image/kernel pins; original
bytes and all first-baseline fields remain unchanged. Old content-addressed stages remain available
until restoration; automatic garbage collection is outside this repair.

## Native splash style revision

Status: **Implemented; isolated native preview Tested**. The refined theme uses the native
`two-step` layout: a midnight-blue gradient, an original 32 px ice-blue spinner at 70% height and
a shaded Qubix cube/Krypton wordmark near the bottom. All three modes use this gradient rather than
the firmware-background presentation, without altering firmware data. Native password/question/message controls remain.
There is no large central title or routine startup/shutdown caption. The original CachyOS theme
remains Preserved. The attributed [asset manifest](../../assets/plymouth/manifest.yml) pins neutral
input files and adapted definition to their GPL-3.0 source revision; Qubix artwork
retains Apache-2.0 attribution. The [asset guide](../../assets/plymouth/README.md) explains regeneration.

Install only the attributed 154 KB Qubix Boot Mono subset and OFL in /usr/share/fonts/qubix/ when
Plymouth is enabled. Include their hashes in the rebuild fingerprint. Before a required rebuild,
refresh only this font directory and require the native plymouth-font-file helper to select the
exact subset path/checksum. Unchanged reapplication skips both cache refresh and generation;
installed verification resolves the font without writing caches. Native mkinitcpio packages the
selected file as /usr/share/fonts/Plymouth.ttf. The subset's Latin coverage is explicit; early native
freetype rendering of other scripts is unvalidated. Existing host fonts remain preserved.

The earlier script design passed isolated rendering but failed operator acceptance; it is replaced
in source and on the target by the native definition. Obsolete script/logo files from that
installation are inert when `ModuleName=two-step` is selected and remain in recovery records.

The private native preview tests module loading against an invalid-module control, actual animation
in boot/shutdown/reboot and a synthetic password prompt. It uses an unprivileged bubblewrap namespace,
private Xwayland/daemon/socket/TTY, read-only host mounts and no DRM/VT devices. It captures only the
test window, checks preservation and cleans up processes. Preview does not establish physical boot,
encrypted-root input acceptance. It binds the exact candidate subset in its private font tree and
verifies native resolution; no host font is installed during preview. See the [splash guide](../user/plymouth.md).
The refined preview also forces the installed FreeType label module within the private mount
namespace, renders its boot/password control and verifies the packaged font without changing host
plugins. Pango tests all three modes; the separate FreeType result covers early-boot text behavior.

The role changes only Theme in `/etc/plymouth/plymouthd.conf`, retaining ShowDelay and unrelated
settings. It requires the installed two-step plugin, an existing splash argument and explicit
generator confirmation. Native shutdown/reboot services supply the mode; services, encryption
settings and kernel arguments are never rewritten. Archive checks require every runtime theme
asset, daemon, native two-step/label plugins and fonts before recording success.

`plymouth.images` maps each existing plain initramfs path to an installed kernel version and its unchanged kernel_image path. The adapter snapshots every affected image before regeneration. Image backups record the associated kernel hash; restoration refuses stale images after a kernel change, even with a drift override. UKI generation/signing is outside current support.

Dracut receives only an additive module drop-in and generates explicit images with `--no-uefi --force image kernel`. Mkinitcpio supports one literal main HOOKS array plus literal append-only drop-ins, inserts Plymouth after systemd/udev and before encryption, and preserves other hook ordering/settings. Competing HOOKS replacements, complex/alternate preset configuration and UKIs fail. Declared images must exactly cover selected preset outputs, including fallback images. `--nopost -p preset` prevents native post hooks from modifying boot entries.

An input fingerprint skips unchanged regeneration. A pending marker survives failure and triggers retry; `force_rebuild: true` permits an explicit repair and should then return to false. Native `lsinitrd` or `lsinitcpio` checks for theme files, daemon, two-step/label plugins and fonts. Image receipts and success fingerprint are committed only after those checks; kernel hashes must remain unchanged.

Check mode performs no image generation, image backups or success-marker writes. Operator acceptance separately requires dracut and mkinitcpio native generation, a real reboot/splash, encrypted-root input where relevant, unchanged entries/arguments, reapplication and restoration. See [restoration](../user/restoration.md).
