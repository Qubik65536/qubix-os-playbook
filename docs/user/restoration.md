# Restoration and recovery

Status: **Manual managed-artwork removal is documented; automated recovery is Planned**. There is no `restore` playbook or automatic backup/revision-state facility yet.

Branding owns only `/usr/share/qubix/branding/{logo.svg,logo.png,banner.svg,LICENSE,NOTICE}`. It reconciles these files on reapplication. Unlisted files, distribution assets and personal defaults are untouched. To remove branding, first disable `branding.enabled` in operator configuration, then remove only the five owned files:

```bash
sudo rm -- /usr/share/qubix/branding/logo.svg /usr/share/qubix/branding/logo.png /usr/share/qubix/branding/banner.svg /usr/share/qubix/branding/LICENSE /usr/share/qubix/branding/NOTICE
```

Do not recursively delete the namespace: it may contain unrelated files. This manual system-removal procedure is not host-tested; equivalent preservation is tested in disposable fixtures. No application references are activated yet, so removal does not change login, desktop or boot configuration. To recover a prior artwork revision that implements branding, use a separate checkout/worktree at that Git revision and reapply its documented deployment procedure.

Future default activation requires content/metadata backups, original-absence records, target paths, and source revision. Restoration must preserve unowned content and reject conflicts. This is resource-level recovery, not whole-system rollback.

Boot adapters require a known bootable fallback and tested live-media recovery before activation. Exact GRUB, Limine, dracut and mkinitcpio recovery procedures remain Planned and must be independently tested before MVP completion.
