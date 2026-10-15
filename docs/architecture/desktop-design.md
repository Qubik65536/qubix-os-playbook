# Qubix Niri desktop design

Status: **Noctalia integration Implemented; native grammar and isolated rendering Tested; primary-session startup Tested; interaction/recovery checks pending**. The earlier classic-companion candidate remains documented for recovery history. [ADR-0012](../decisions/ADR-0012.md) records the new direction.

## Composition and ownership

| Surface | First candidate | New design |
|---|---|---|
| Windows, workspaces, shortcuts | Niri KDL | Niri KDL with rounded clipping and revised shortcuts |
| Panel | Waybar JSON/CSS | Noctalia bar |
| Launcher | Fuzzel INI | Noctalia launcher |
| Notifications | Mako | Noctalia notification daemon |
| Wallpaper | Swaybg | Noctalia wallpaper layer with attributed Qubix artwork |
| Terminal | Foot INI | Foot with the Qubix palette |
| Clipboard, settings, window switcher | Not integrated | Noctalia panels and IPC |
| Prompt | Optional Starship | Existing additive Bash/Zsh defaults; Fish remains preserved |

The additional Qubix Niri session keeps its explicit system configuration. Native Niri, Noctalia, Alacritty, Fish, user dotfiles and output/hardware settings remain preserved. Noctalia uses `/etc/qubix/noctalia/` for managed defaults and palettes, with Qubix-only user state and data under the ordinary XDG state/data roots' `qubix/` namespace. GUI changes override supplied shell defaults in that state namespace. They are user-owned and are not reset by deployment or removed by system-file restoration. Other applications keep their ordinary XDG paths.

Noctalia's application theme templates are disabled: palette changes must not rewrite personal GTK/Qt/terminal/browser configurations. Noctalia 5.2.1 also unconditionally writes the GSettings dark-mode preference; the profile launcher uses a transient memory backend for the shell and restores the caller's original backend for applications launched through Noctalia. Native dconf settings remain preserved. No additional Waybar, Mako or Swaybg process is started by the new Qubix configuration. Existing classic companion packages and old Qubix companion files remain available for recorded-baseline recovery; deployment does not remove packages. Noctalia's own Polkit agent supplies GUI authentication prompts; no external agent is started by Qubix. Authentication and lock/unlock require operator testing; PAM remains preserved.

## Appearance

- Primary accent and active Niri focus ring: **#56728b**.
- Base surface: #1b242c; raised surface: #283745; main text: #f2f5f8; secondary text: #cfdae2. Brighter blue-gray secondary colours preserve legibility when an accent alone is too dark for small text.
- Niri window corner radius: **16 px**, with content clipped to geometry; gaps: 12 px.
- Noctalia top bar: a transparent 40 px surface with separate rounded 16 px widget capsules, 8 px edge inset and 12 px end inset. Floating launcher/clipboard/settings surfaces use an increased global corner scale.
- A small rounded bottom dock provides the macOS-inspired application surface. Noctalia controls shell surfaces; ordinary applications retain their own toolkits and decorations.

### Bar and shortcut-panel refinement

Status: **Bar capsules and shortcut panel Implemented; native preview Tested**. Every visible top-bar component has its own rounded capsule on a transparent bar surface, with consistent padding/gaps, subtle outlines and #56728b emphasis. Launcher/workspaces, the clock and system controls retain their existing positions and actions. Empty widgets do not leave decorative capsules behind.

Super+Shift+/ opens a Qubix Noctalia shortcut panel: searchable categories, readable action names, blue-gray keycaps, two columns and scrolling within the available screen. The bar's keyboard button opens the same panel; Super+F1 retains Niri's compact built-in overlay. Escape, a Close button and outside click dismiss the panel.

The presenter is a small local Noctalia plugin using its installed declarative UI runtime, with no new packages, background service or network fetch. Ansible generates its display data from the managed KDL's labelled bindings; the panel must not maintain a second shortcut list or execute listed actions. The role installs plugin files under /usr/share/qubix/noctalia/plugins/ and enables only the local path source in Qubix defaults. Native Noctalia and user GUI overrides remain preserved.

Acceptance: warning-free native TOML/KDL validation, valid plugin manifest/entry paths, matching generated shortcut data, native bar/panel screenshots, successful IPC open/close and search, zero-change reapplication, unchanged native configuration/compositor, and no leftover preview processes. Test the candidate in a nested session before deployment. The currently selected native CachyOS session must remain intact; select Qubix Niri to use these defaults.

## Shortcut contract

`Mod` is Super in the main session and Alt in a nested Niri test. DMS's [published Niri bindings](https://github.com/AvengeMedia/DankMaterialShell/blob/master/core/internal/config/embedded/niri-binds.kdl) inform the core map. Noctalia IPC implements shell actions. These are desktop shortcuts; application copy/paste remains Ctrl+C/V.

| Main-session shortcut | Action |
|---|---|
| Super+Space; Super+D | Launcher |
| Super+T; Super+Return | Foot terminal |
| Super+V | Clipboard history |
| Super+Comma | Noctalia settings |
| Super+N | Notification centre |
| Super+Y | Wallpaper picker |
| Super+Tab; Super+O | Niri overview |
| Alt+Tab | Noctalia window switcher |
| Super+W; Super+Q | Close focused window; W is the macOS-inspired alias |
| Super+H/J/K/L or arrow keys | Navigate tiled windows |
| Super+Shift+H/J/K/L or arrow keys | Move tiled windows |
| Super+Shift+T | Toggle floating |
| Super+Ctrl+W | Toggle tabbed column; relocated from DMS's Super+W |
| Super+Alt+L | Lock through Noctalia |
| Super+X | Session/power menu |
| Super+Shift+E | Niri's confirmed session exit |
| Super+Shift+S; Print | Niri screenshot picker |
| Super+Shift+/; bar keyboard button | Searchable Qubix shortcut panel |
| Super+F1 | Compact Niri shortcut overlay |

Audio, microphone, media and brightness keys call Noctalia's installed IPC commands. Window/workspace sizing and navigation remain Niri actions. No automatic suspension, logout or lock is performed during deployment/testing.

## Acceptance and migration

Require measured Niri, Foot and supported Noctalia before component writes. Validate generated Niri KDL, Foot INI and Noctalia TOML using their installed parsers; check all palette roles and include complete terminal colours, required by the Noctalia 5.2 palette loader. A custom palette name alone does not prove that its colours loaded. Install the session entry last. Existing Qubix baselines remain immutable.

The native nested test must use a distinct Wayland display/private D-Bus session and temporary Qubix state/data/cache. It must support the existing Niri process whether launched by a user service or directly by SDDM. Disable test-only Polkit registration and clipboard persistence, prove shell/bar/wallpaper/launcher/notification/window rendering and IPC, preserve the original compositor and clean up temporary processes. Main-session physical shortcuts, dock interactions, authentication, lock/unlock and portal behaviour require operator verification.

After deploying the new defaults, an existing session can reload Niri appearance and shortcuts, but startup commands do not replace already-running companions. The operator-authorized logout/reboot and selection of Qubix Niri activates the new shell. A file install alone is not visual acceptance.

Primary references: [Noctalia configuration roots](https://docs.noctalia.dev/noctalia/configuration/), [palette roles](https://docs.noctalia.dev/noctalia/theming/palette/), [IPC](https://docs.noctalia.dev/noctalia/ipc/), [Niri rounded window rules](https://github.com/niri-wm/niri/wiki/Configuration:-Window-Rules).
