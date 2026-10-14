# Project status

Updated: 2026-10-13. Stage: **MVP candidate implementation In Progress**.

| Capability | Status | Evidence |
|---|---|---|
| Scope, architecture, ten ADRs, roadmap and workflows | Implemented | Documentation committed before source; local links/consistency pass |
| Controller tooling | Tested | Python 3.13.14; Ansible 2.21.5; ansible-lint 26.10.1; yamllint 1.38.0; ShellCheck 0.11.0 |
| Profile/identity/discovery contracts | Tested | 25 profile + 11 host + 7 identity cases and normalization; normal/check mode; zero changes |
| Live inspection | Implemented | Real macOS rejection with zero changes; supported CachyOS collection still unverified |
| CI workflow | Implemented | Same local scripts pass; GitHub execution pending because no commits were pushed |
| Branding installation and file verification | Tested | Licensed assets; isolated filesystem; preview/idempotency/repair/preservation; missing/corrupt/symlink rejection |
| Niri/appearance/shell | Implemented | Definitions and missing-companion fixtures pass; native parser/session pending VM |
| Login | Implemented | Native Breeze clone and unsupported-manager fixtures; VM login pending |
| GRUB and Limine | Implemented | Independent preservation/idempotency and unsupported-version fixtures; reboot acceptance pending |
| Plymouth/dracut/mkinitcpio | Planned | Opt-in; no image changes |
| Backups/restoration/revision state | Implemented | Baselines, receipts, conflict/restore fixtures; deployment revision recorded last |

## Actual validation

`./scripts/validate.sh`: YAML lint, production Ansible lint, all entry/test playbook syntax checks, ShellCheck, Markdown/local-link checks, schema/profile/documented-default agreement and source asset hashes pass.

`./scripts/test.sh`: framework fixtures pass in normal/check mode with zero changes; branding fixtures pass both modes. Branding tests deliberately create/mutate/remove only temporary fixtures and assert a second install changes no files/directories. A preview leaves the branding namespace absent. Tests assert unowned content survives both reapplication and rejected symlink writes.

`./bootstrap.sh verify`: on the real macOS controller, expected unsupported-host rejection (exit 2), zero changes. It does not claim supported-host or graphical verification.

## Limits and next milestone

No live CachyOS VM was supplied. Supported-host collection, system artwork deployment, Niri parsing/session behaviour, login, boot and recovery remain **unverified on a real target**. Artwork installation alone cannot activate Qubix appearance. Check mode defers file copies if the namespace does not exist; it cannot verify unwritten content. Restricted sandbox requires approved execution for Ansible local IPC.

Next: collect a live disposable CachyOS Niri report, design minimal validated Niri/companion defaults, and add backup-aware activation. See [F03/F06](backlog.md). First desktop milestone requires observed wallpaper, launcher, bar/notifications, terminal, preservation and idempotency; boot work remains independent.

The next implementation follows [candidate contracts](../architecture/mvp-candidate.md). A VM is installing; complete other implementation/fixture work first, then collect live target evidence.
