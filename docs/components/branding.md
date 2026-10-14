# Shared branding

Status: **Planned**. First useful mutation after validated discovery.

Own only explicitly listed assets under `/usr/share/qubix/branding/`. Reuse canonical Qubix logo/banner assets with source/license/checksum attribution. Preserve distribution logos and identity files. Target support initially requires CachyOS Niri, although artwork itself is platform-independent. No package or graphical-session dependency is needed to install inert artwork.

`branding.enabled` selects installation. Deploy fixed asset filenames and modes with Ansible copy tasks. Reapplication must report no change when bytes/metadata match. Preview must report proposed writes. Verification compares exact checksums and file type; installation success establishes asset availability only.

Restoration initially consists of removing only the explicitly listed Qubix-owned files, preserving unknown files in that namespace. Prior revisions of managed artwork are recovered by checking out the previous Git revision and reapplying; automatic backup/restore is a later state component. Do not claim a recovery playbook exists until it is implemented.

Acceptance: provenance is complete, a disposable filesystem confirms checksums, second application has zero changes, damaged assets fail verification, and unrelated files survive.
