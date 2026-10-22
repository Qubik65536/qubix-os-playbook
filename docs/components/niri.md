# Niri desktop and appearance

Status: **Noctalia candidate Implemented; controller ownership/version fixtures, native Niri/Noctalia grammar (historical Foot checks) and isolated rendering Tested; primary-session startup Tested; interaction/recovery checks pending**. Earlier classic-companion deployment/rendering remains recorded in the native results.

The role requires measured Niri, WezTerm, jq and standalone Noctalia >=5.2.0 and <6.0.0. Discovery reads Noctalia's actual version; binary presence alone is insufficient. Missing tools and unsupported versions fail before component writes. Native Niri/Noctalia and personal terminal settings remain preserved.

The [slim information bar and scale policy](../architecture/desktop-design.md#slim-information-bar-and-display-scale) adds installed jq as a prerequisite and an Implemented session-bound scale helper; controller lifecycle fixtures, isolated native scale checks and primary reboot startup at 100% are Tested. See the [desktop evidence](../project/desktop-test-results.md#slim-information-bar-and-100-startup). Output scale becomes a Qubix Default of 100% at session start/new connection; other output settings and personal configuration remain Preserved. An operator may adjust an already-connected screen for the current session. The helper does not change refresh rates, resolutions or persistent native monitor files.

The [desktop design](../architecture/desktop-design.md) is authoritative for palette, rounded geometry, shortcuts and migration. Niri manages windows/workspaces; Noctalia supplies bar, launcher, notifications, wallpaper, clipboard, settings and its Polkit agent. The Qubix dock is disabled. WezTerm supplies the explicitly configured terminal. Qubix does not start Waybar, Fuzzel, Mako, Swaybg or a second authentication agent.

Optional `presentation: qubix` requires the prepared exact Noctalia 5.3.0 client and bound native/source
provenance. Optional `fingerprint_setup: true` requires installed GJS, GTK 4 and fprintd and adds
the graphical enrollment application. The private client/license add two resources; the application,
icon and searchable entry add six. Both follow the [refinement contract](../architecture/login-refinement.md).

## Managed resources and activation

Twenty-four system resources and three account configuration files comprise the desktop: wallpaper, Niri theme/configuration, Noctalia TOML/palette, a minimal profile launcher, Fcitx profile/global defaults/launcher, shared candidate UI defaults and three theme assets, an output-scale helper, a Power options application entry, the session entry, three shortcut-plugin files (manifest, presenter and generated data) two power-plugin files (manifest and panel), and three system integration resources and three home files for [WezTerm](wezterm.md). Noctalia reads managed defaults from /etc/qubix/noctalia/. The launcher sets Noctalia-specific state/data roots beneath the user's XDG roots' qubix/ namespace. Native configuration and ordinary application XDG paths remain intact. Noctalia cache follows XDG_CACHE_HOME; GUI overrides are user-owned and survive Ansible deployment/restoration. App-theme generators are disabled. The profile launcher keeps Noctalia 5.2's automatic GSettings dark-mode write in memory and restores the original backend for applications launched by Noctalia.

Ansible validates Niri with niri validate --config %s, Noctalia with noctalia config validate %s, and the launcher with bash -n. Native tests additionally require Noctalia's production TOML to have no schema warnings, because its CLI can return zero for unknown-section warnings. Palette roles, required terminal colours and cross-component accent consistency are checked locally. The session entry is installed last; parser failures leave earlier inert files recoverable.

Each visible bar widget has its own compact rounded module; the dock reserves no bottom area. The launcher pins Power options (Noctalia application ID qubix-power) to open the [guarded power panel](../architecture/desktop-design.md#power-action-countdown), also reached from Super+X and the bar power button. It requires holding keys 1–5 and offers cancellable click countdowns. The Control Center retains the native menu with countdown defaults. The global Session provider searches enabled native actions; /session lists them, and direct selection executes through Noctalia's native runner. The desktop entry only opens the guarded menu. User GUI overrides remain preserved. The keyboard button and Super+Shift+/ open a searchable two-column shortcut panel; Super+F1 keeps Niri's compact fallback. Super+Ctrl+arrows (with H/J/K/L aliases) resize column width/window height in 5% steps; Super+Ctrl+R resets height. Its managed local Noctalia plugin uses the existing declarative UI runtime and presents labels generated from KDL bindings. It does not execute shortcuts, fetch plugins or alter personal configuration. Native tests lint both plugin manifests/entry paths, open/filter/close the shortcut panel and capture screenshots; controller fixtures verify generated bindings and power confirmation behavior without executing actions.

Select **Qubix Niri** at login. From a free TTY after logout, niri --session --config /etc/niri/qubix/config.kdl is the alternate entrypoint. The explicit configuration does not inherit personal Niri settings. An existing session can reload its window/shortcut settings, but startup commands do not switch the running companion stack; logout and session selection activate Noctalia.

Noctalia 5.2.1 can retain old plugin geometry after config-reload. Manifest size/placement upgrades
use the [shell-only activation procedure and preservation constraints](../architecture/desktop-design.md#power-action-countdown);
inspect the live panel rather than treating installed bytes or successful reload as visual acceptance.

## Verification, recovery and limits

The native grammar workflow validates production candidates and rejects invalid controls in its private temporary directory. The nested workflow renders these definitions with temporary path substitutions, private D-Bus and test-only state overrides. It measures the main Niri process even when SDDM launches it directly rather than through niri.service, preserving its PID and session endpoints. It does not prove physical shortcuts, authentication, lock/unlock or portal behaviour.

Restore returns the first system-file baselines. Old Qubix classic-companion files remain inert on upgrade and retain their existing backup receipts; restoration includes recorded legacy resources. Packages and user-owned Qubix GUI overrides remain. When its entry is retained, switching to the native session restores native shell preferences without overwriting them. An operator-directed native-entry retirement is outside normal deployment/restoration; restore that entry first using the [documented private backup](../project/live-test-plan.md#operator-authorized-native-session-retirement-and-reboot). Qubix requires the compositor package; personal configuration stays intact. Test the Noctalia primary session and second-deploy idempotency before recording full desktop acceptance.

The profile's configurable [Krypton typography](fonts.md) supplies `shell.font_family`
through the managed Noctalia defaults. User GUI font choices remain preserved; WezTerm uses the supplied Krypton/IBM Plex defaults unless personal settings take precedence. Only the explicitly managed `~/.config/wezterm` files change, with backups.

The current WezTerm migration is Implemented with controller checks and [native
installation/rendering/activation evidence](../project/package-management-test-results.md).
Physical shortcut input remains pending; historical Foot results are kept separately. Run the
[CachyOS preparation step](package-management.md) before deploying this revision.
No Foot configuration is installed by new deployments. Both terminal bindings use
`qubix-wezterm start`; the session terminal environment selects the managed wrapper.

Niri also starts [Simplified Chinese Pinyin](input-method.md) with native Fcitx 5
and GTK/Qt/XWayland integration. English/Pinyin and dark horizontal candidate defaults are additive; saved personal
input profiles retain precedence. Prepare the five native packages before deployment.
