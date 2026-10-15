# Physical-target Plymouth activation proposal

Status: **Prepared; activation not authorized or performed**. The existing [desktop authorization](live-test-plan.md) excludes Plymouth/image generation. Root [AGENTS.md](../../AGENTS.md) requires: “Boot work uses explicitly authorized disposable VMs.” This machine is a physical ThinkPad. Request an explicit exception only after the native preview, no-write deployment preview and recovery review pass; do not infer it from desktop/reboot permission.

## Inspected mapping

Read-only inspection on 2026-10-15 finds Plymouth 26.134.222-4, mkinitcpio 42.2, the native cachyos theme, an existing splash argument and native Plymouth poweroff/reboot units. No bootloader change is proposed. Recheck installed kernels, presets and hashes immediately before activation; package updates can invalidate this mapping.

| Preset | Installed kernel/module directory | Existing kernel file | Existing image |
|---|---|---|---|
| linux-cachyos | 7.2.9-2-cachyos | /boot/vmlinuz-linux-cachyos | /boot/initramfs-linux-cachyos.img |
| linux-cachyos-lts | 6.18.55-2-cachyos-lts | /boot/vmlinuz-linux-cachyos-lts | /boot/initramfs-linux-cachyos-lts.img |

Both presets select only their default plain image. No UKI, fallback output, signing or kernel/argument changes are involved. Keep the existing main HOOKS order, which already contains Plymouth, and `/etc/mkinitcpio.conf.d/10-limine-snapper-sync.conf` with HOOKS+=(sd-btrfs-overlayfs).

The ignored override extends the existing desktop configuration with:

```yaml
qubix:
  plymouth:
    enabled: true
    initramfs_backend: mkinitcpio
    confirm_active: true
    force_rebuild: false
    presets: [linux-cachyos, linux-cachyos-lts]
    images:
      - path: /boot/initramfs-linux-cachyos.img
        kernel: 7.2.9-2-cachyos
        kernel_image: /boot/vmlinuz-linux-cachyos
      - path: /boot/initramfs-linux-cachyos-lts.img
        kernel: 6.18.55-2-cachyos-lts
        kernel_image: /boot/vmlinuz-linux-cachyos-lts
```

## Reviewable changes and acceptance

Install the three Qubix theme resources, replace only Theme in the existing Plymouth selection, and preserve unrelated settings. Back up the selection, generator configuration and both original images with kernel hashes in private `/var/lib/qubix/backup/`. The adapter may normalize the literal main HOOKS spacing; native ordering, snapshot drop-in, Limine configuration, kernels and command line must keep their original meaning/bytes as applicable.

Run exactly the two confirmed `mkinitcpio --nopost -p` presets; inspect both generated archives, verify fonts/plugins/theme and unchanged kernels/native files, then reapply without regeneration and run installed verification. Record the splash on reboot and shutdown from the console. A private X11 preview is rendering evidence only. LTS/primary boot and restore need independent observations.

Inspection finds approximately 3.58 GiB free on /boot and 464 GiB free on the root filesystem, sufficient for the approximately 103 MiB of original compressed images plus replacement work space. Recheck space/hashes and verify operator console/live-media recovery access before activation. Keep SSH available. If any precondition changes, stop before image mutation and revise this plan.

Recovery retains the original images only while their matching kernels remain unchanged. Do not upgrade kernels during the test. The [restoration workflow](../user/restoration.md) restores every recorded component; first reinstate the privately retired native Niri session entry if removing Qubix. For splash-only manual recovery, inspect the exact backup manifests and restore only the selection, generator integration and matching images; do not guess hashed filenames or copy stale images. No physical recovery test has passed yet. A disposable VM remains the preferred acceptance environment.
