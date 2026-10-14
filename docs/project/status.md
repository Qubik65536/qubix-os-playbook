# Project status

Updated: 2026-10-13. Stage: **Phase 1, controller tooling**.

| Capability | Status | Evidence |
|---|---|---|
| Scope, architecture, decisions and workflow | Implemented | Documentation review; no source implementation |
| Controller tooling | Implemented | Local virtual environment and locked tools; CI remains Planned |
| Discovery/profile/orchestration | Planned | No executable playbooks |
| Branding | Planned | Reuse source inspected; no assets imported |
| Niri/appearance/shell/login | Planned | No graphical target inspected |
| GRUB and Limine | Planned | Both required for MVP; no host boot changes |
| Plymouth/dracut/mkinitcpio | Planned | No image changes |
| Backups/restoration/revision state | Planned | Contracts only |

Controller is macOS. No CachyOS VM is supplied. Reference repositories were inspected; this is not evidence of live target compatibility. Next gate: implement local tooling and read-only foundation. [Backlog](backlog.md) contains task acceptance criteria.
