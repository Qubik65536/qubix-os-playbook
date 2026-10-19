# Restoration and recovery

Status: Named-file/image recovery Implemented; isolated fixtures and native desktop absence recovery Tested; VM boot recovery pending.

Snapshot the VM and retain console access before login/boot changes. Private `/var/lib/qubix/backup/` stores first pre-Qubix bytes, UID/GID/mode, absence and applied-checksum receipts. Baselines survive reapplication. ACLs/xattrs and whole-system state are not captured.

## Normal restoration

Run from the local playbook root as the same desktop account used for deployment:

```bash
./bootstrap.sh restore -i inventory/local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh restore -i inventory/local.ini -e @config/local.yml --ask-become-pass
```

Use the same local overrides for private /boot discovery. Restore handles **all recorded baselines**, independently of enabled components. Original files/images return; originally absent files are removed. Unlisted files/directories, retained backups and prerequisite packages remain. Empty directories created by deployment are not removed. Disabling a component alone does not uninstall it. Empty baseline sets fail explicitly.

Local drift/unreceipted partial changes stop restore. Inspect the target/receipt/original before intentionally adding `-e qubix_files_force_restore=true`. Restoration is per resource; a later failure may leave earlier resources restored. Concurrent deployment is unsupported.

Boot activation recovery refuses changed preserved entries/settings even if Qubix was reapplied afterward. Use reviewed native recovery or a VM snapshot when native package hooks have changed the menu; force cannot bypass this protection.

Image backups include associated kernel hashes. Changed kernels prohibit stale image restoration, even with force. Use the VM snapshot or reviewed current-kernel native recovery. Successful restoration clears image-input/pending markers; backups remain, and subsequent deployment rebuilds required images.

## Failed deployment or reboot

Read `deployment-pending.json` beside `deployment.json` under `/var/lib/qubix/` as root. Pending state describes an unfinished/failed attempt; deployment.json may describe an older success. `plymouth-pending` triggers retry after an incomplete rebuild. Resolve the actual failure; do not clear markers to manufacture success.

If the VM cannot boot, revert its snapshot first. Manual live-media recovery requires mounting the correct root and boot/EFI filesystems, inspecting JSON manifests for exact targets and original backup names, and restoring only affected activation/integration resources. Never guess hashed filenames.

GRUB recovery restores its original custom hook; Limine restores the original active configuration. No loader installation/disk operation needs reversal. Plymouth recovery restores selection/generator integration and compatible original images. After kernel changes use reviewed native generation for current outputs instead of stale images. These live-media steps require independent VM validation before release.

Choose native Niri when a restored Qubix session entry is removed. Remove any manually adopted Zsh source line yourself; the playbook never edits personal dotfiles. Test original login, entries, splash and sessions using the [checklist](verification.md). Resource restoration is not a transaction or whole-system rollback.

Limine image staging restores the retained config before deleting Qubix boot images. Original
native cache and cached-kernel hashes must still match the recovery record, even under force.
An intact earlier appearance-only baseline can gain explicit module-alias ownership without
replacing its original bytes. A native package update that changes pinned files requires reviewed
native recovery; copying an old config onto new cached images would invalidate its checksums.
