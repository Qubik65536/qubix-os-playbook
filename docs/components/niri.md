# Niri desktop and appearance

Status: **Noctalia candidate Implemented; controller ownership/version fixtures, native Niri/Foot/Noctalia grammar and isolated rendering Tested; primary-session migration pending**. Earlier classic-companion deployment/rendering remains recorded in the native results.

The role requires measured Niri, Foot and standalone Noctalia >=5.2.0 and <6.0.0. Discovery reads Noctalia's actual version; binary presence alone is insufficient. Missing tools and unsupported versions fail before component writes. Native Niri/Noctalia/Alacritty settings remain preserved.

The [desktop design](../architecture/desktop-design.md) is authoritative for palette, rounded geometry, shortcuts and migration. Niri manages windows/workspaces; Noctalia supplies bar, dock, launcher, notifications, wallpaper, clipboard, settings and its Polkit agent. Foot supplies the explicitly configured terminal. Qubix does not start Waybar, Fuzzel, Mako, Swaybg or a second authentication agent.

## Managed resources and activation

Eight named resources comprise the desktop: wallpaper, Niri theme/configuration, Foot INI, Noctalia TOML/palette, a minimal profile launcher and the session entry. Noctalia reads managed defaults from /etc/qubix/noctalia/. The launcher sets Noctalia-specific state/data roots beneath the user's XDG roots' qubix/ namespace. Native configuration and ordinary application XDG paths remain intact. Noctalia cache follows XDG_CACHE_HOME; GUI overrides are user-owned and survive Ansible deployment/restoration. App-theme generators are disabled. The profile launcher keeps Noctalia 5.2's automatic GSettings dark-mode write in memory and restores the original backend for applications launched by Noctalia.

Ansible validates Niri with niri validate --config %s, Foot with its --check-config --config %s command, Noctalia with noctalia config validate %s, and the launcher with bash -n. Native tests additionally require Noctalia's production TOML to have no schema warnings, because its CLI can return zero for unknown-section warnings. Palette roles, required terminal colours and cross-component accent consistency are checked locally. The session entry is installed last; parser failures leave earlier inert files recoverable.

Select **Qubix Niri** at login. From a free TTY after logout, niri --session --config /etc/niri/qubix/config.kdl is the alternate entrypoint. The explicit configuration does not inherit personal Niri settings. An existing session can reload its window/shortcut settings, but startup commands do not switch the running companion stack; logout and session selection activate Noctalia.

## Verification, recovery and limits

The native grammar workflow validates production candidates and rejects invalid controls in its private temporary directory. The nested workflow renders these definitions with temporary path substitutions, private D-Bus and test-only state overrides. It measures the main Niri process even when SDDM launches it directly rather than through niri.service, preserving its PID and session endpoints. It does not prove physical shortcuts, authentication, lock/unlock or portal behaviour.

Restore returns the first system-file baselines. Old Qubix classic-companion files remain inert on upgrade and retain their existing backup receipts; restoration includes recorded legacy resources. Packages and user-owned Qubix GUI overrides remain. Switching to the native session restores native shell preferences without overwriting them. Test the Noctalia primary session and second-deploy idempotency before recording full desktop acceptance.
