# Restoration and recovery

Status: **Planned**. There is no automated restore command yet.

Future default activation requires backups of content/metadata, original absence, target path, and source revision. Recovery reverses Qubix-owned changes, preserves unowned content, and refuses unsafe conflicts. This is resource-level restoration, not whole-system rollback.

Additive artwork can be removed by deleting only the documented Qubix-owned files. Reapply a previous Git revision to return managed artwork to that revision. Detailed filenames and procedures will accompany the branding implementation.

Boot adapters require a known bootable fallback and tested live-media recovery before activation. Revert original appearance settings and rebuild only required generated output with the original platform tools. Exact GRUB, Limine, dracut, and mkinitcpio recovery steps must be documented and tested separately before MVP completion.
