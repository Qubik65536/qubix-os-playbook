# Project status

Updated: 2026-10-14. Stage: **Implemented MVP candidate, ready for operator VM testing**. Full MVP acceptance remains In Progress; SSH is connected to a physical CachyOS ThinkPad after service/firewall setup and host-key confirmation. Read-only discovery passes; deployment and VM acceptance remain pending.

| Capability | Status | Actual evidence |
|---|---|---|
| Architecture/ADRs/conventions | Implemented | Documentation committed before source; local links/configuration agreement pass |
| Tools and CI | Tested locally; CI Implemented | Locked tools; shared scripts pass; no GitHub execution because commits were not pushed |
| Profile/identity/discovery | Tested in fixtures | 25 profile + 11 host + 7 identity cases; independent manager activity; normal/check zero changes |
| Live CachyOS inspection | Tested on physical target | CachyOS/Linux/systemd; explicit privileged metadata for private /boot; 38 tasks, zero changes/failures |
| Branding | Tested in fixtures | Provenance/hash checks, isolated preview/install/repair/idempotency/preservation |
| Niri/wallpaper/companions | Implemented | Separate session definitions, missing-tool rejection, optional measured agent; native parsers/session pending |
| Shell | Tested in controller fixtures | Explicit/user/default Starship precedence; native interactive startup pending |
| SDDM | Implemented | UI clone, actual INI lines, standalone/ambiguous/unsupported activity fixtures; authentication pending |
| GRUB and Limine | Implemented | Independent preservation/reapplication/private-mode/file-restore fixtures; native checker, boot/restore pending |
| Plymouth/dracut/mkinitcpio | Implemented | Simulated dispatch/rebuild skip/archive failure, kernel restore and no-write preview; native generation/splash pending |
| Backup/restore/state | Tested in fixtures | Bytes/modes/absence, drift/repeated restore, failed validator and pending/last-success records |

## Commands and outcomes

- `./scripts/validate.sh`: passes YAML lint, production Ansible lint, all public/fixture syntax checks, ShellCheck, Markdown/local-link/configuration/asset checks and diff whitespace.
- `./scripts/test.sh`: passed the complete framework normal/check (zero changes), branding normal/check, recovery, desktop, SDDM, loader and image-generator/check-mode fixtures. Subsequent focused boot file-lifecycle/private-mode, login, splash and compact-wrapper guard fixtures also pass.
- `bash scripts/collect-target-info.sh --help`: exit 0. Actual macOS invocation: expected exit 2, no writes; Linux output pending.
- `./bootstrap.sh verify`: actual macOS rejection, exit 2 and zero changes; expected guard, not supported-host acceptance.

Fake generators/inspectors and archive listings prove dispatch/guards, not native initramfs generation. Desktop tests render definitions, not a compositor. Native validators are wired into deployment but not yet run on CachyOS. Fixtures write only disposable roots under `.cache/tests/`.

SSH initially timed out because target sshd was inactive and UFW lacked an allow rule. The operator enabled access and confirmed the ED25519 fingerprint. Password authentication works; no credentials are saved in inventory or Git. The target reports no virtualization and runs Niri 26.04, Noctalia 5.2.1/Alacritty, SDDM 0.21.0, Limine 12.9.3 and mkinitcpio 42.2. Bootctl identifies the current Limine loader; no boot configuration was changed.

## Limits and next gate

No native graphical or reboot success is claimed. [Compatibility](../architecture/compatibility.md) limits login to active SDDM/Breeze; fixed-command greetd desktop testing uses a free TTY. Boot selection is explicit. Plymouth supports existing plain images and literal mkinitcpio settings, not UKIs/signing.

Backups record bytes, UID/GID/mode and absence, not ACLs/xattrs or complete system state. Restore is per resource; changed kernels block stale images. Check mode cannot validate uninstalled files or regenerated archives. Concurrent deployment is unsupported.

Next: obtain explicit permission for desktop prerequisites/deployment on the physical target, or use a disposable VM. Foot/Fuzzel/Waybar/Mako/Swaybg/Starship and Breeze are absent. Native package hooks include Snapper/Limine integration; inspect those effects before installing prerequisites. Then independently test login, both loaders and both generators. See [T01](backlog.md) and [operator guide](../user/getting-started.md).
