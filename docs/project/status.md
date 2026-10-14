# Project status

Updated: 2026-10-14. Stage: **Implemented MVP candidate, ready for operator VM testing**. Full MVP acceptance remains In Progress; SSH is connected to a physical CachyOS ThinkPad after service/firewall setup and host-key confirmation. Desktop deployment, installed verification, zero-change reapplication and isolated nested rendering pass. Native desktop restoration passes; primary-session/VM acceptance remains pending.

| Capability | Status | Actual evidence |
|---|---|---|
| Architecture/ADRs/conventions | Implemented | Documentation committed before source; local links/configuration agreement pass |
| Tools and CI | Tested locally; CI Implemented | Locked tools; shared scripts pass; no GitHub execution because commits were not pushed |
| Profile/identity/discovery | Tested in fixtures | 25 profile + 11 host + 7 identity cases; independent manager activity; normal/check zero changes |
| Live CachyOS inspection | Tested on physical target | CachyOS/Linux/systemd; explicit privileged metadata for private /boot; 38 tasks, zero changes/failures |
| Branding | Tested in fixtures and native deployment | Exact installed resources, zero-change reapplication, original-file preservation |
| Niri/wallpaper/companions | Native syntax/files/nested rendering Tested | Niri/Foot/Fuzzel controls pass; wallpaper/bar/terminal/launcher/notifications/IPC navigation render; primary session pending |
| Shell | Native Bash/Starship and controller fixtures Tested | Temporary-home native startup/TOML/prompt pass; default Fish and personal files preserved |
| SDDM | Implemented | UI clone, actual INI lines, standalone/ambiguous/unsupported activity fixtures; authentication pending |
| GRUB and Limine | Implemented | Independent preservation/reapplication/private-mode/absent-hook/stale-restore fixtures; native checker, boot/restore pending |
| Plymouth/dracut/mkinitcpio | Implemented | Simulated dispatch/rebuild skip/archive failure, kernel restore and no-write preview; native generation/splash pending |
| Backup/restore/state | Fixtures and native desktop absence lifecycle Tested | Original-byte/mode/drift faults in fixtures; 17 private live baselines remain intact through restore; boot/image recovery pending |

## Commands and outcomes

- `./scripts/validate.sh`: passes YAML lint, production Ansible lint, all public/fixture syntax checks, ShellCheck, Markdown/local-link/configuration/asset checks and diff whitespace.
- `./scripts/test.sh`: passed the complete framework normal/check (zero changes), branding normal/check, recovery, desktop, SDDM, loader and image-generator/check-mode fixtures. Subsequent focused boot file-lifecycle/private-mode, login, splash and compact-wrapper guard fixtures also pass.
- `bash scripts/collect-target-info.sh --help`: exit 0. Actual macOS invocation: expected exit 2; Linux collector completed with permission failures labelled, followed by successful privileged metadata discovery.
- `./bootstrap.sh verify`: actual macOS rejection, exit 2 and zero changes; expected guard, not supported-host acceptance.

Fake generators/inspectors and archive listings prove dispatch/guards, not native initramfs generation. Desktop tests render definitions, not a compositor. Native Niri validation now passes on CachyOS; Foot/Fuzzel validation, actual file deployment and isolated nested rendering pass; primary-session acceptance remains pending. Controller fixtures write only disposable roots under `.cache/tests/`. The native grammar test creates/removes its own user-owned temporary directory; its eight changes are temporary setup/cleanup.

SSH initially timed out because target sshd was inactive and UFW lacked an allow rule. The operator enabled access and confirmed the ED25519 fingerprint. Password authentication works; no credentials are saved in inventory or Git. The target reports no virtualization and runs Niri 26.04, Noctalia 5.2.1/Alacritty, SDDM 0.21.0, Limine 12.9.3 and mkinitcpio 42.2. Bootctl identifies the current Limine loader; read-only inspection itself changed no boot configuration. Later approved package hooks refreshed Limine snapshot entries.

Native `tests/integration/niri.yml` passes: 62 tasks, eight temporary setup/cleanup changes, zero failures. Corrected validation uses `niri validate --config`; the installed CLI rejected the old option order. Niri, Foot and Fuzzel accept their production candidates and reject invalid controls. This establishes syntax only, not visual or companion startup behaviour.

## Limits and next gate

Native nested rendering is Tested; no primary-session, authentication or reboot success is claimed. [Compatibility](../architecture/compatibility.md) limits login to active SDDM/Breeze; fixed-command greetd desktop testing uses a free TTY. Boot selection is explicit. Plymouth supports existing plain images and literal mkinitcpio settings, not UKIs/signing.

Backups record bytes, UID/GID/mode and absence, not ACLs/xattrs or complete system state. Restore is per resource; changed kernels block stale images. Check mode cannot validate uninstalled files or regenerated archives. Concurrent deployment is unsupported.

The operator authorized desktop-only preparation, including native Snapper/Limine package hooks. Pacman installed Foot 1.28.0, Fuzzel 1.15.0, Waybar 0.15.0, Mako 1.11.0, Swaybg 1.2.2 and Starship 1.26.0 plus 17 dependencies. The preview passed (280 tasks, 17 proposed changes, zero failures). Native package hooks changed limine.conf; the other 75 audited resources and default Fish shell were preserved. Desktop deployment (373 tasks, 58 changes), installed verification (58 tasks, zero changes) and same-revision reapplication (352 tasks, zero changes) pass. All 76 audited native/personal resources match the post-package baseline. Native restore passes (249 tasks, 18 changes); all 17 resources are removed, original hashes/default Fish shell and baseline hashes remain intact, and pending state clears. The [native results](desktop-test-results.md) provide the authoritative command/acceptance record. Next operator gate: select the tested Qubix Niri main session after successful desktop deployment. Breeze is absent. Then independently test login, both loaders and both generators. See [T01](backlog.md) and [operator guide](../user/getting-started.md).

## Repeatable native desktop evidence

The optional tests/integration/desktop.yml workflow passes: 64 tasks, five temporary setup/test/evidence/cleanup changes, zero failures. It runs the production configuration in a nested window on a private D-Bus session, with temporary HOME/config/cache paths. Native wallpaper/bar layers, two Foot windows, Fuzzel rendering, Mako notification receipt and IPC focus navigation pass. Screenshots were inspected; the original Niri service PID and session endpoints remain unchanged. Evidence is retained only under ignored .cache/native-desktop/ on the controller. Physical keys, login, portals, Polkit and lock/unlock remain acceptance items.

Boot recovery fixtures now also prove that native entries/hook changes survive rejected restoration after reapplication, with force false and true. The expanded boot suite passes 724 tasks (five expected rescued refusals); shared recovery passes 229 tasks (two expected rescued refusals). Native boot/recovery remains unverified.
