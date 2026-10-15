# Physical-target Plymouth test plan

Status: **Corrective deployment, exact active-image checks and completed zero-change reapplication Tested; normal-kernel menu/startup/reboot appearance confirmed by the operator**. The first scripted attempt failed visual acceptance. The operator approved physical-target Plymouth activation on 2026-10-15 after reviewing the native preview, no-write target preview and exact backup/two-image plan. This extends the earlier [desktop authorization](live-test-plan.md) for this machine only. Root [AGENTS.md](../../AGENTS.md) requires: “Boot work uses explicitly authorized disposable VMs.” Other boot work retains that rule; do not infer further exceptions from this approval.

## Inspected mapping

Read-only inspection on 2026-10-15 finds Plymouth 26.134.222-4, mkinitcpio 42.2, the native cachyos theme, an existing splash argument and native Plymouth poweroff/reboot units. The first attempt proposed no bootloader change; the corrective deployment below also manages Limine appearance and explicit module aliases. Recheck installed kernels, presets and hashes immediately before activation; package updates can invalidate this mapping.

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

## Corrective deployment

Following the failed visual result, the operator requested Limine branding, working startup branding
and a native-looking shutdown, then instructed continuation. This corrective test extends the
approved physical-target work to the confirmed Limine 12 config, Qubix boot wallpaper and exact
module aliases/checksums. It preserves native cache/history, entry identities, kernel paths/args,
EFI loaders and firmware enrollment. No Limine installer/updater or package hook is executed.

Read-only reinspection confirms the same boot ID/kernel, 3.58 GiB free on the vfat /boot ESP,
32 private first baselines and 19 preserved native boot/cache/EFI files. The controller DHCP address
changed; the operator added the replacement restricted SSH firewall rule. The isolated two-step
preview passes 48 tasks, all three animation modes, native password rendering, negative module
control, unchanged host configuration/daemon and zero remaining processes. Its black fallback
background and small spinner/bottom wordmark were inspected; firmware-background and physical
appearance still require observation.

Bind each source mapping to /boot/<machine-id>/linux-cachyos/initramfs and its vmlinuz, with the
corresponding linux-cachyos-lts pair. Verify actual pins and kernel equality before writes.
Stage verified copies under /boot/qubix/plymouth/, then atomically update only bound module values.
Keep snapshot entries/cache/EFI hashes unchanged. Activate graphical Limine appearance separately
in the same confirmed config. Reapply, inspect actual staged archives and pin checks, then reboot.
Restore the retained config before deleting stages; reject native cache/kernel drift even under force.
The [component contract](../components/plymouth.md#active-limine-image-repair) defines that boundary.

The corrective no-write preview passes 1077 tasks with 43 proposed changes and zero failures.
A protected audit afterward finds no changes to the 76 native/personal files, 19 native boot/cache/EFI
resources or 32 existing baseline hashes; no pending state remains. Controller validation passes:
767-task two-image nested-entry lifecycle with two expected stale-pin refusals, 368-task binding/
enrollment/FAT suite with five refusals, 220-task check-mode suite with four refusals, 301-task
graphical fixture with four refusals and 966-task legacy-loader/recovery regression with seven refusals.
Corrective native deployment and console observation remain pending at this checkpoint.

## Recorded results

Clean source 2645034 was used throughout. The no-write target preview passes 459 tasks with seven proposed changes. Actual deployment passes 616 tasks with 28 changes; identical reapplication passes 571 tasks with zero changes and skips both generator invocations. Login/bootloader branding remains disabled. The ignored config/local.yml now retains the approved Plymouth mappings for future runs.

Native archive listing and extraction confirm Theme=qubix, exact installed logo/theme/script bytes, script/label plugins and a 621572-byte packaged font in both images. Original image backup hashes match the pre-deployment originals and associated kernels remain unchanged. Private baseline count rises from 25 to 32; every earlier baseline hash is preserved. Of 76 audited native/personal files, only the approved Plymouth selection and two initramfs images change; Limine, kernel files, main hook configuration, snapshot append, default Fish shell and personal files are preserved. Root-owned backups remain private. No recovery or alternate-kernel boot result is implied.

The guarded reboot returns SSH/SDDM and the Qubix session; Plymouth start/quit services report success. The operator observes the old CachyOS startup splash and rejects the scripted shutdown appearance. Read-only inspection proves the active Limine entries reference /boot/<machine-id>/linux-cachyos/initramfs and its LTS counterpart, with BLAKE2b checksums. Those cached images were outside the first mapping. Source-image archive checks were insufficient. The [corrective contract](../components/plymouth.md#active-limine-image-repair) requires staged active-image binding and a native-style theme before another acceptance attempt.

## Corrective activation results

Clean e7e652a deployment passes 1542 tasks with 145 changes and zero failures. Installed verification
passes 284 tasks with zero changes. Both exact mkinitcpio --nopost presets run; source images are
staged at content-addressed Qubix paths and only the two confirmed module references/pins switch.
Graphical Limine wallpaper/palette and the native two-step definition are installed with FAT modes.

Extraction of all four source/staged images confirms Theme=qubix, all 38 runtime manifest checksums,
native two-step/label plugins and packaged fonts. Both active BLAKE2b pins match. An independent byte
comparison confirms protected config content unchanged. All 19 native boot/cache/history/EFI files
and all 32 earlier baseline hashes remain unchanged; 75 baseline manifests are root-owned/private.
Of 76 tracked native/personal resources, only the two source images and limine.conf change.

The identical reapplication completes 1337 successful tasks with zero changes, then the machine
becomes unreachable (one unreachable, zero component failures). It does not establish completed
idempotency. The transient deployment-attempt marker was observed during reapplication; do not clear
it manually or treat the prior files-verified manifest as completion of the interrupted run.
No controlled reboot was requested after e7e652a. Ping/IPv4/IPv6 SSH fail; the known hostname still
resolves to the original address. The operator was asked to wake/reconnect the target and report any
manual shutdown/reboot observations. Complete same-source reapplication, verify pending state clears,
then execute the prepared guarded reboot/console test. LTS, independent generator/loader and recovery
gates remain separate.

## Reconnected validation and reboot

On 2026-10-15 the operator wakes the target. SSH reconnects with the pinned host key and confirms the
same boot ID/kernel. A second run loses the LAN briefly after 758 tasks/zero changes. The next full
run uses bounded SSH reconnection retries and a clean detached e7e652a checkout, with the identical
inventory/configuration: 1490 successful tasks, zero changes, zero unreachable hosts and zero failures.
Both mkinitcpio commands are skipped. Installed verification passes 284 tasks with zero changes.
The attempt marker clears normally and all 75 private baseline hashes remain unchanged.

Native hourly Snapper cleanup has refreshed limine.conf.old to the current configuration; its service
journal records the writes. All 18 other native boot/cache/EFI hashes, active configuration bytes,
source image hashes and protected personal/native resources match the reconnect audit. Qubix's
original private recovery baseline is unaffected. Temporary controller/target sleep inhibitors are
used for validation; saved power policy is unchanged.

The guarded reboot checks all four exact source/staged image hashes, both BLAKE2b pins, all 38 runtime
assets, clean e7e652a/configuration state, absent pending markers and the 32 original baseline hashes.
It stops the temporary target inhibitor and requests reboot with a one-time 15-second boot menu.
The request is accepted at 13:11 EDT. The target returns with new boot ID
68011c7a-65dc-41c9-8da8-cf8253bd82d1, unchanged 7.2.9-2-cachyos and command line, and Limine 12.9.3
reporting the native CachyOS.linux-cachyos entry. SSH/SDDM, Plymouth start/quit and the prior reboot-screen
service succeed. Qubix Niri/Noctalia return with bar/wallpaper layers, no dock layer and eDP-1 at
1920x1080/100% scale. The temporary target inhibitor is absent. Protected files and all 75 baseline
hashes remain unchanged; only loader/random-seed changes among the audited native boot resources.
Pending state stays absent. The operator confirms all three requested menu/startup/reboot visuals,
then asks for a more distinctive palette and Monaspace Krypton typography. Independent LTS, poweroff,
dracut, GRUB, real encryption input and recovery acceptance remain open.

## Reviewed midnight and Krypton refinement

After confirming the corrected menu/startup/reboot visuals, the operator requests a more distinctive
text/background palette and GitHub Monaspace Krypton, including a subset where useful. The
[design contract](../architecture/boot-design.md) defines the shared midnight/steel-blue/ice-blue
composition, complete CP437 menu font and renamed, OFL-attributed 154 KB native prompt subset.
Plymouth keeps its native two-step controls and small ring; all three modes now use the theme's blue
gradient instead of firmware background. Early freetype text has the documented subset coverage;
real encrypted-root/localized prompt acceptance remains separate.

The isolated native preview passes all three animations, exact subset selection, a synthetic native
prompt, negative module control, host preservation and cleanup. The target no-write preview passes
1197 tasks with 40 proposed changes and zero failures. A subsequent audit confirms unchanged protected
resources, all 75 private baseline hashes, absent pending markers and 3.47 GiB free on /boot.
The standalone-font copyright/OFL embedding follow-up is metadata-only and receives a final native
font/render check before activation. Existing desktop/profile/kernel/image mappings remain unchanged.
That final preview passes 50 tasks: Pango boot/reboot/shutdown, the negative module control, and
separate forced-FreeType boot/password rendering. Both resolve final font SHA256
fe5d940039391c7b2d842a5221d190a39ddfc09c2e2799de61a104a8fb022b22, preserve host selection/session
and leave zero preview processes. The captured FreeType prompt is visually inspected.

Limine's existing exact 15-key graphical recovery contract may gain only the six reviewed font/help
keys after original bytes/hash, current receipt and absence checks. Retain its original bytes and all
other fields, including module aliases. Fonts/licenses gain their own original-absence records.
Rebuild only the same two matching mkinitcpio presets with --nopost, stage verified new images while
retaining earlier stages, verify exact archive/font/pin contents and zero-change reapplication, then
perform the already authorized guarded reboot and record the new console observations separately.

## Krypton activation and contrast follow-up

Clean 87e824b activation passes 1645 tasks/102 changes/zero failures. Installed verification passes
298 tasks/zero changes. All four generated/active images contain the exact 38 runtime assets and
three copies of the final font; both BLAKE2b pins match. Identical reapplication passes 1572 tasks
with zero changes, skipping both generators and font-cache refresh. The ownership extension changes
only the reviewed Limine key list; all earlier original recovery bytes remain intact.

The guarded 14:29 EDT reboot returns with boot ID d160a3aa-3c19-4935-b59c-fe45c539c4c4,
unchanged normal kernel/arguments, Limine 12.9.3/native entry, successful Plymouth start/quit and
previous reboot-screen services. Qubix returns at 100% scale with bar/wallpaper and no dock. All
81 private manifests, 76 tracked resources, seven owned boot assets and root fonts match the
preboot audit. Only the native loader/random-seed rotates; pending markers and temporary inhibitor
are absent. The operator reports working screens but rejects their contrast/layout.

The requested correction brightens foregrounds/cube/ring over darker blue surfaces, removes both
decorative captions and reduces menu scaling to 1x1. The menu wallpaper reuses the canonical desktop
cube. Font files, recovery ownership and activation/image mappings are unchanged. Repeat native
preview, no-write review, exact-image verification and reapplication before the authorized reboot;
record visual acceptance separately. Independent poweroff/LTS/GRUB/dracut/recovery gates stay open.
