# Roadmap

| Phase | Deliverable | Gate |
|---|---|---|
| 0 Documentation | Scope, architecture, ADRs, conventions and local planning | Reviewed and committed before source |
| 1 Foundation | Tooling, profile, discovery, read-only validation and CI | Executable inspection; unsupported hosts fail safely |
| 2 CachyOS Niri desktop | Artwork, Niri, wallpaper/companions, shell/terminal | Working VM session; preservation and idempotency |
| 3 Login/system branding | Supported login theme and additive system appearance | Login/session verified; identity/authentication preserved |
| 4 Bootloader | **Both GRUB and Limine** | Separate boot, preservation, backup and recovery tests |
| 5 Plymouth | Theme + dracut + mkinitcpio | Resources, reboots and restoration for both generators |
| 6 Stabilization | End-to-end, reapplication, restoration, revision tracking, release readiness | All MVP scope criteria with evidence |
| 7 Expansion | Fedora Workstation, KDE, then justified targets | Stable CachyOS Niri MVP first |

The first desktop milestone does not depend on phases 4–5. Track actual completion in [status](status.md) and actionable work in [backlog](backlog.md).
