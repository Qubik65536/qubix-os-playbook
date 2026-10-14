# Reference review and reuse

Reviewed 2026-10-13 against [Qubix OS BlueBuild revision `56c57ac`](https://github.com/Qubik65536/qubix-os-bluebuild/tree/56c57acafb9c3305b201a83255c0007cf4b398bd).

Useful designs include separately named Qubix artwork, a slate-blue Niri palette (`#56728B`), a separate theme include, content-validated GRUB assets, and additive shell defaults. The reference separates technical and user documentation and records important design rationale. Its KDE splash layout can inform future KDE work, but no KDE adapter is part of bootstrap.

Reuse candidates are the Qubix logo SVG/PNG and banner. Preserve the repository's Apache-2.0 license, source revision, original paths, and checksums. No artwork is imported during the documentation phase. The branding implementation imports those three assets with [provenance](../../assets/branding/README.md), retained notices and checksums.

Do not copy BlueBuild recipes, image/ISO publishing, Fedora identity rewrites, automatic shell changes, inherited display-manager assumptions, or boot activation scripts wholesale. Those mechanisms have a different deployment and safety boundary.

The [CachyOS Niri settings revision `114bce2`](https://github.com/CachyOS/cachyos-niri-settings/tree/114bce2cc341eeeb8e88e51d6e4437647d6fb047) splits KDL into includes and starts Noctalia via `qs`. This is reference evidence, not a live environment inspection.

[Niri's configuration documentation](https://github.com/niri-wm/niri/wiki/Configuration:-Introduction) specifies user configuration precedence, `/etc/niri/config.kdl` fallback, and `niri validate`. [Ansible check-mode documentation](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html) describes preview limitations. Validate against the installed versions when implementing either integration.
