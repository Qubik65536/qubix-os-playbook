# Plymouth and initramfs adapters

Status: Implemented candidate. Both generator plans, simulated dispatch/idempotency, check-mode isolation and kernel-aware restoration guards are Tested. Actual archive generation, splash and encryption prompts need VMs.

## Circular boot and poweroff branding

Status: **Implemented; native parser/rendering Tested; image generation and actual power-cycle acceptance pending**. The Qubix logo and title stay visible over the blue-gray background, a native-script circular loading indicator animates, and Plymouth.GetMode() selects Starting/Shutting down/Restarting captions. Normal, message, question and password callbacks remain; password display receives only bullet counts. Native shutdown/reboot services use the same selected theme without replacing service units or touching PAM, loader entries or kernel arguments.

Before activation, test the actual script parser and boot/shutdown/reboot rendering in an unprivileged bubblewrap namespace with a private Xwayland window, private /run and network namespace, read-only host mounts and no DRM/VT devices. The preview must never contact the system Plymouth daemon. Capture only the test window, verify animation, parser rejection of an invalid control, mode captions, prompts, cleanup and preserved host configuration. Image verification must require a native label plugin and packaged font resources because the title, captions and circle use Image.Text. Preview success does not establish initramfs generation or reboot/poweroff acceptance.

The inspected physical target already has Plymouth, a script plugin, splash argument and native poweroff/reboot units. It selects cachyos and has two plain CachyOS/LTS images. Its literal HOOKS+=(sd-btrfs-overlayfs) drop-in remains Preserved. The mkinitcpio adapter supports narrowly parsed literal append arrays, validates the complete hook order and rejects replacements, expansion, operators and duplicate Plymouth hooks. Drop-in hashes participate in the rebuild fingerprint; the files are never managed or executed during discovery. The preservation/refusal fixture passes; native generation remains pending. Do not remove snapshot integration to make deployment pass.

Prepare exact existing kernel/image/preset mappings, a no-write deployment preview, backups and recovery steps before requesting physical-target activation. Actual image regeneration and boot/poweroff observation remain a distinct authorized step.

The native isolated test passes all three animation modes, positive/negative parser controls and a synthetic password prompt, with preserved host selection/session and no leftover processes. Captured mode captions were visually inspected. This is renderer evidence rather than a physical boot result. Follow the [splash guide](../user/plymouth.md) and [reviewed physical-target proposal](../project/plymouth-test-plan.md).

The named script theme manages logo, normal/message/question/password display callbacks and selection in `/etc/plymouth/plymouthd.conf`. Existing ShowDelay and unrelated settings remain preserved. Password callbacks display only a bullet count; the script does not log or store password input. Require an installed script plugin, an existing `splash` kernel argument and explicit generator confirmation. Kernel arguments are never rewritten.

`plymouth.images` maps each existing plain initramfs path to an installed kernel version and its unchanged kernel_image path. The adapter snapshots every affected image before regeneration. Image backups record the associated kernel hash; restoration refuses stale images after a kernel change, even with a drift override. UKI generation/signing is outside current support.

Dracut receives only an additive module drop-in and generates explicit images with `--no-uefi --force image kernel`. Mkinitcpio supports one literal main HOOKS array plus literal append-only drop-ins, inserts Plymouth after systemd/udev and before encryption, and preserves other hook ordering/settings. Competing HOOKS replacements, complex/alternate preset configuration and UKIs fail. Declared images must exactly cover selected preset outputs, including fallback images. `--nopost -p preset` prevents native post hooks from modifying boot entries.

An input fingerprint skips unchanged regeneration. A pending marker survives failure and triggers retry; `force_rebuild: true` permits an explicit repair and should then return to false. Native `lsinitrd` or `lsinitcpio` checks for theme files, daemon, script/label plugins and fonts. Image receipts and success fingerprint are committed only after those checks; kernel hashes must remain unchanged.

Check mode performs no image generation, image backups or success-marker writes. Operator acceptance separately requires dracut and mkinitcpio native generation, a real reboot/splash, encrypted-root input where relevant, unchanged entries/arguments, reapplication and restoration. See [restoration](../user/restoration.md).
