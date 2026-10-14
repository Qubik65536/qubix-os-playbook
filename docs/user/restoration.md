# Restoration and recovery

Status: **Implemented named-file recovery; isolated fixtures Tested**. The shared file engine snapshots bytes, original absence and UID/GID/mode before mutation. Baselines and applied-checksum receipts are under `/var/lib/qubix/backup/`, readable only by root. New components use this engine; the original bootstrap branding role is being migrated with deployment orchestration.

Run `./bootstrap.sh restore --check --diff --ask-become-pass` to preview and `./bootstrap.sh restore --ask-become-pass` to restore. Add the same remote inventory used for deployment. Restore needs a readable recorded baseline and supported CachyOS host; an empty backup set fails explicitly. It restores the first pre-Qubix state, retains baselines, removes only originally absent recorded files, and leaves unlisted resources/directories alone.

Local drift fails safely. Inspect the target and backup before deliberately passing `-e qubix_files_force_restore=true`. Restoration is per resource; a later conflict can leave earlier resources already restored. Original ACLs/xattrs are not recorded, concurrent deployments are unsupported, and automated boot-image recovery is still being implemented. Snapshot the test VM before deployment.

Branding owns only `/usr/share/qubix/branding/{logo.svg,logo.png,banner.svg,LICENSE,NOTICE}`. It reconciles these files on reapplication. Unlisted files, distribution assets and personal defaults are untouched. To remove branding, first disable `branding.enabled` in operator configuration, then remove only the five owned files:

```bash
sudo rm -- /usr/share/qubix/branding/logo.svg /usr/share/qubix/branding/logo.png /usr/share/qubix/branding/banner.svg /usr/share/qubix/branding/LICENSE /usr/share/qubix/branding/NOTICE
```

Do not recursively delete the namespace: it may contain unrelated files. This manual system-removal procedure is not host-tested; equivalent preservation is tested in disposable fixtures. No application references are activated yet, so removal does not change login, desktop or boot configuration. To recover a prior artwork revision that implements branding, use a separate checkout/worktree at that Git revision and reapply its documented deployment procedure.

Future default activation requires content/metadata backups, original-absence records, target paths, and source revision. Restoration must preserve unowned content and reject conflicts. This is resource-level recovery, not whole-system rollback.

Boot adapters require a known bootable fallback and tested live-media recovery before activation. Exact GRUB, Limine, dracut and mkinitcpio recovery procedures remain Planned and must be independently tested before MVP completion.
