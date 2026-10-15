# Boot, reboot and poweroff splash

Status: native-style theme Implemented; native preview, mkinitcpio generation, corrected deployment and exact active-image verification Tested; the operator confirms normal-kernel startup/reboot appearance. Independent poweroff/LTS/recovery checks remain open. The first physical
activation used verified generator outputs but missed Limine's active cached images; startup still
showed CachyOS, and the operator rejected the earlier scripted shutdown layout. See
[current evidence](../project/plymouth-test-plan.md). Plymouth supplies the splash after the bootloader
and during shutdown; it is independent of Limine/GRUB menu appearance.

The current candidate uses Plymouth's native two-step renderer: firmware/black background, a small
white spinner and a bottom Qubix cube/wordmark. Native prompts remain available. The playbook preserves
kernel arguments, encryption settings, boot entries and service units.

## Preview without activation

On a target with a running Niri session, Plymouth/two-step/X11 plugins, bubblewrap, Xwayland, ImageMagick and Python already installed:

```bash
.venv/bin/ansible-playbook -i inventory/target.local.ini tests/integration/plymouth.yml -e @config/local.yml --ask-pass --ask-become-pass
```

This explicitly opens a temporary preview window. It runs the native module and theme in private user/mount/PID/network namespaces, with a private daemon socket, pseudoterminal and X11 server. Host files are read-only; no DRM or physical virtual-terminal devices are exposed. Evidence is fetched to ignored `.cache/native-plymouth/`; temporary processes/files are removed. Missing prerequisites fail. This test neither selects the host theme nor generates an image. It does not establish an actual boot, encryption unlock or poweroff result.

## Configure activation on a disposable VM

Take a VM snapshot and retain console/live-media access. Inspect the selected native generator, `/etc/mkinitcpio.d/*.preset` or dracut image outputs, installed module directories, current kernel files and active command line. An existing `splash` argument and native two-step plugin are required. Do not guess an image path from the distribution or use `uname -r` as the version of every installed kernel.

Add a `plymouth` section to your existing ignored configuration. Set `enabled: true`, `confirm_active: true` and the measured `initramfs_backend`. Each `images` entry requires the existing `path`, installed module-directory `kernel` and associated unchanged `kernel_image`. Mkinitcpio also requires exact native `presets`; every selected output must be covered. See the [reviewed target mapping](../project/plymouth-test-plan.md) for a concrete example, which must be re-inspected before reuse.

For the supported CachyOS Limine 12 cache layout, also confirm the booted loader with
`bootctl status`, inspect `sudo cat /boot/limine.conf`, and locate the primary entry's `path` and
`module_path`. A `boot():/machine-id/...` URI refers to `/boot/machine-id/...` on the confirmed ESP.
The suffix after `#` is a BLAKE2b checksum, not part of the filename. Use `sudo b2sum /boot/...`
and `sudo sha256sum` on source/cached kernels to check the exact pins and kernel equality.
Snapshot/history paths are separate recovery entries and must not be selected as primary bindings.

Retain the existing desktop selections and add the measured metadata, for example:

```yaml
qubix:
  bootloader:
    enabled: false  # Appearance is independently selectable.
    backend: limine
    config_path: /boot/limine.conf
    confirm_active: true
    limine_version: 12
  plymouth:
    enabled: true
    initramfs_backend: mkinitcpio
    confirm_active: true
    force_rebuild: false
    presets: [linux-cachyos]
    images:
      - path: /boot/initramfs-linux-cachyos.img
        kernel: REPLACE_WITH_INSTALLED_MODULE_VERSION
        kernel_image: /boot/vmlinuz-linux-cachyos
        limine_image: /boot/REPLACE_MACHINE_ID/linux-cachyos/initramfs
        limine_kernel_image: /boot/REPLACE_MACHINE_ID/linux-cachyos/vmlinuz
```

Replace every placeholder with inspected values and include every selected preset output. Set
bootloader.enabled true separately to select the graphical menu. Cached Limine integration requires
both cache fields for every image and a confirmed `/boot/limine.conf`; unbound/ambiguous/enrolled
layouts fail before writes. Other loader layouts need their own adapter, not guessed paths.
Qubix preserves native cache/history/EFI files, stages content-addressed copies under
`/boot/qubix/plymouth/`, and atomically switches only the bound module references and native pins.
FAT permissions follow the existing mount; mount options remain unchanged. Retain the original
native cache paths in the two binding fields after deployment: the active module then points to
an automatically verified Qubix stage, not a replacement value for limine_image. Reinspect mappings
and review recovery baselines after native kernel/cache updates; stale pins are rejected.

CachyOS's native Snapper integration may refresh `limine.conf.old` during hourly cleanup, even
when the active configuration bytes stay unchanged. That rolling copy is not Qubix's original
recovery baseline. Retain the private manifests/originals under `/var/lib/qubix/backup/`; compare
active module paths, pins and kernel/cache hashes when checking for drift. Do not disable native
snapshot integration just to keep the rolling copy unchanged.

Preview, review the predicted selection/integration changes, then activate only on an authorized target:

```bash
./bootstrap.sh deploy -i inventory/target.local.ini -e @.cache/plymouth.local.yml --check --diff --ask-pass --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @.cache/plymouth.local.yml --ask-pass --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @.cache/plymouth.local.yml --tags installed --ask-pass --ask-become-pass
```

Prepare that override in the ignored .cache directory, keeping the rest of your desktop selections. After approval/testing, retain the same mappings in ignored config/local.yml for normal future deployment commands. Check mode does not rebuild, back up images or prove the resulting archives. Activation snapshots affected resources and images before rebuilding. Mkinitcpio uses `--nopost -p` for selected presets; the preserved snapshot-hook append remains active without rerunning Limine post hooks. Dracut uses the explicit images and kernels. Native archive checks inspect generator outputs and actual Limine-referenced staged images; they require the watermark, spinner/input assets, definition, daemon, two-step/label plugins and fonts. A failed check leaves pending state visible.

Reapply the identical configuration before reboot: unchanged inputs should skip regeneration. Keep `force_rebuild: false` except for an intentional repair. Observe startup, logout/reboot and poweroff separately; shutdown branding depends on the native Plymouth services and available graphics. For encrypted roots, test the real unlock prompt with console access. Record module, preview, archive and physical observations separately.

## Recover

Use the [restoration guide](restoration.md). Backups are per-resource rather than a complete rollback; changed kernels block restoring stale images. Limine configuration is restored before staged images are deleted; changed native cache/kernel hashes or unrelated entry drift block restoring stale pins even under force. The standard restore command restores **all** recorded components. If the native Niri login entry was retired, restore that entry before removing the Qubix session. Recover a failed VM from its snapshot first. Physical activation needs the explicit exception and recovery plan described in the [target plan](../project/plymouth-test-plan.md).
