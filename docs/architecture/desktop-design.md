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
| Terminal | Foot INI | WezTerm with supplied Oxocarbon/Krypton defaults and preserved personal overrides |
| Clipboard, settings, window switcher | Not integrated | Noctalia panels and IPC |
| Prompt | Optional Starship | Existing additive Bash/Zsh defaults; Fish remains preserved |

The additional Qubix Niri session keeps its explicit system configuration. Native Niri, Noctalia, Alacritty, Fish, user dotfiles and output/hardware settings remain preserved. Noctalia uses `/etc/qubix/noctalia/` for managed defaults and palettes, with Qubix-only user state and data under the ordinary XDG state/data roots' `qubix/` namespace. GUI changes override supplied shell defaults in that state namespace. They are user-owned and are not reset by deployment or removed by system-file restoration. Other applications keep their ordinary XDG paths.

Noctalia's application theme templates are disabled: palette changes must not rewrite personal GTK/Qt/terminal/browser configurations. Noctalia 5.2.1 also unconditionally writes the GSettings dark-mode preference; the profile launcher uses a transient memory backend for the shell and restores the caller's original backend for applications launched through Noctalia. Native dconf settings remain preserved. No additional Waybar, Mako or Swaybg process is started by the new Qubix configuration. Existing classic companion packages and old Qubix companion files remain available for recorded-baseline recovery; deployment does not remove packages. Noctalia's own Polkit agent supplies GUI authentication prompts; no external agent is started by Qubix. Authentication and lock/unlock require operator testing; PAM remains preserved.

## Appearance

### Slim information bar and display scale

Status: **Scale helper and slim bar Implemented; fixtures, native preview, primary deployment and 100% startup after reboot Tested**. The requested [olive-dusk reference](https://ryoku.dev/showroom/11.webp) uses thin dark modules, shallow rounded corners and a quiet outline. The inspected eDP-1 is 1920x1080 at 1.25 scale: the previous 40 logical px bar occupies about 50 physical px. The new defaults use a 32 px bar at 100% output scale, with 28 px dark modules, 6 px radii/gaps/edge inset and 10 px end insets. Keep #56728b accents and an identifiable 24 px launcher image box. No reference artwork or shell code is imported.

Show a bounded active application icon/title beside the launcher/workspaces/shortcut button, optional native MPRIS media in the centre, and CPU load, used RAM, available CPU temperature, connectivity, volume, battery, notifications, date/time and shell/session controls on the right. Missing sensors and inactive media must use native unavailable/hidden behaviour rather than invented values. Bound title/media widths and inspect narrow and full-width previews.

Niri 26.04 has exact output matching and automatic scale selection rather than a global wildcard scale setting. A small Bash helper uses installed jq and Niri's JSON IPC to apply scale 1.0 once at session start and when an enabled output first appears/reconnects. It observes native workspace/config events, remembers connected outputs and exits with the compositor. Existing-output events must not repeatedly override an operator's session-local scale adjustment. It changes only runtime scale, preserving modes, refresh rates, transforms, position configuration and personal files. Startup plus hotplug handling supplies the requested default for future screens; jq becomes a measured prerequisite. A --once mode permits explicit activation in an already-running session.

Acceptance: native parser/renderer checks; 100% scale on the active panel; isolated startup/hotplug/reconnect and manual-override preservation tests; real application-title changes and hardware readings in screenshots; no dock; preserved native configuration and main compositor; zero-change Ansible reapplication. The default applies in Qubix Niri, leaving other sessions' configuration intact.

- Primary accent and active Niri focus ring: **#56728b**.
- Base surface: #1b242c; raised surface: #283745; main text: #f2f5f8; secondary text: #cfdae2. Brighter blue-gray secondary colours preserve legibility when an accent alone is too dark for small text.
- Niri window corner radius: **16 px**, with content clipped to geometry; gaps: 12 px.
- Noctalia top bar: a transparent 32 px surface with separate dark 28 px modules, 6 px module radii/edge inset and 10 px end insets. The launcher image is scaled to 24 px; other widgets retain their ordinary content scale. Floating launcher/clipboard/settings surfaces use an increased global corner scale.
- The dock is disabled, including its reserved bottom area. The launcher, Niri overview and window switcher provide application access. Noctalia controls shell surfaces; ordinary applications retain their own toolkits and decorations.

### Bar and shortcut-panel refinement

Status: **Bar capsules and shortcut panel Implemented; native preview Tested**. Every visible top-bar component has its own rounded capsule on a transparent bar surface, with consistent padding/gaps, subtle outlines and #56728b emphasis. Launcher/workspaces, the clock and system controls retain their existing positions and actions. Empty widgets do not leave decorative capsules behind.

Super+Shift+/ opens a Qubix Noctalia shortcut panel: searchable categories, readable action names, blue-gray keycaps, two columns and scrolling within the available screen. The bar's keyboard button opens the same panel; Super+F1 retains Niri's compact built-in overlay. Escape, a Close button and outside click dismiss the panel.

The presenter is a small local Noctalia plugin using its installed declarative UI runtime, with no new packages, background service or network fetch. Ansible generates its display data from the managed KDL's labelled bindings; the panel must not maintain a second shortcut list or execute listed actions. The role installs plugin files under /usr/share/qubix/noctalia/plugins/ and enables only the local path source in Qubix defaults. Native Noctalia and user GUI overrides remain preserved.

Acceptance: warning-free native TOML/KDL validation, valid plugin manifest/entry paths, matching generated shortcut data, native bar/panel screenshots, successful IPC open/close and search, zero-change reapplication, unchanged native configuration/compositor, and no leftover preview processes. Test the candidate in a nested session before deployment. Preserve the active main compositor and personal configuration while testing; use Qubix Niri for these defaults.

### Resize and launcher/layout revision

Status: **Resize bindings and launcher/bar/dock changes Implemented; native preview, deployment, primary reload and zero-change reapplication Tested**. Super+Ctrl+Left/Right (or H/L) adjust column width in 5% steps, Super+Ctrl+Up/Down (or K/J) adjust window height in the same steps, and Super+Ctrl+R resets automatic height. Tiled windows share column width; height controls are most apparent when windows are stacked. Keep labelled bindings in the canonical KDL so regeneration includes these controls.

The profile supplies a pinned **Power options** launcher entry. The [guarded power panel](#power-action-countdown) now handles that entry, Super+X and the bar power button. The native Session provider remains enabled in global launcher search for lock/logout/sleep/reboot/shutdown terms; retain `/session` for its full action list. Selecting a direct action result executes it through Noctalia; the Power options entry opens the guarded menu. The Control Center's native power entry remains available.

The compact modules, restrained borders and spacing observed in the [Ryoku showroom](https://ryoku.dev/showroom), especially the pink-room reference, inform the separate floating components and existing #56728b palette. The visibility correction below defines the current geometry. This is visual inspiration; no Ryoku source, artwork or runtime is imported. The Noctalia dock and its reserved bottom area are disabled; launcher, overview and window switcher provide application access.

Acceptance: generated binding coverage including resize labels, native KDL/TOML validation, observed width/height changes in the isolated test, visible launcher power entry/results without executing power actions, screenshots with no dock layer, preserved main compositor/personal configuration, and zero-change reapplication. Update native fixtures for the resulting production candidates. Deploy and reload the active Qubix shell after these checks; reboot is unnecessary.

### Bar visibility and logo correction

Status: **Implemented; native preview, live reload, installed verification and zero-change reapplication Tested**. Inspection of the primary Qubix session confirms that the compact revision is installed and no user bar/widget overrides mask it. Its height, radius and border changes were too small to establish the intended visual distinction. Noctalia 5.2 renders a launcher image at its 16 px base glyph size; the attributed logo's transparent margins further reduce the visible cube.

The earlier correction used a 40 px bar with 36 px modules, 12 px module radii, 10 px separation/edge inset and 16 px end insets. Outline opacity rises from 30% to 80% with opaque module fills. Only the launcher widget's scale is set to 2.0, yielding a 32 px image box and twice the previous visible artwork dimensions; its horizontal capsule padding is reduced so its button stays compact. Original artwork, palette, individual module boundaries, actions, dock absence and user preferences remain preserved. Before/after native preview screenshots were inspected; the larger cube and stronger outlines are visible, parser checks pass and the parent configuration/compositor remain unchanged.

Acceptance: warning-free native configuration validation, inspected before/after preview screenshots showing a clearly larger cube and distinct module outlines, preserved parent session/configuration, live profile reload and zero-change reapplication. File presence and layer names alone do not establish visual improvement.

### Power-action countdown

Status: **Implemented; controller fixtures, native validation/rendering, installation, reload and zero-change reapplication Tested; physical input pending**. See the [deployment evidence](../project/desktop-test-results.md#power-confirmation-deployment). A local `qubix/power:menu` Noctalia panel supplies the original five
actions: 1 Lock, 2 Log out, 3 Lock & Suspend, 4 Reboot and 5 Shut down. Hold a number for three
seconds to execute; releasing early cancels. Repeated key-down events must never confirm early.
Pressing another number cancels the hold and requires releasing the held keys before retrying.
A button click starts a visible five-second countdown; clicking it again cancels, and selecting
another starts a fresh countdown. Mixing mouse and held-key input cancels the current action.
Escape, Cancel, outside click, panel replacement/close and reopen clear all pending state.

Footer/lock-close correction: **Implemented; controller/native no-effect regression, installation, live footer and zero-change reapplication Tested; physical lock/unlock pending**. Retain the native tile row and destructive Shut Down
styling, adding a lower-left prompt and lower-right Cancel button beneath it (836-by-184 panel).
Prompts describe idle, hold/release, click/repeat-click and cancellation states. After confirmation,
latch the action and request closure; dispatch exactly once from the host's completed-close callback,
not while its close animation is visible. Recheck lock availability before dispatch. Unconfirmed
closure never dispatches. Acceptance: deferred-close controller regression, native/footer screenshots,
installed/live checks and preserved cancellation behavior. Never exercise real power actions in
unattended tests. See the [comparison screenshots and regression evidence](../project/desktop-test-results.md#power-footer-and-completed-close-dispatch).

Native-layout correction: **Implemented; controller fixtures, native/live comparison, installation and zero-change reapplication Tested; physical input pending**. Match Noctalia 5.2's five 152-by-112 logical-pixel
tiles, 12 px gaps, 28 px icons, 8 px icon/label gap and centred content in the original 836-by-140 tile-only panel.
Use symmetric upper/lower badge/progress slots so neither shifts the content centre. The declarative
API lacks native overlay badges; retain the upper-right badge with that bounded approximation.
The footer correction above adds guidance below that unchanged tile row; retain tooltips and countdown labels. Shut Down uses the native error/on_error palette at rest and
during confirmation; the native session action explicitly retains its destructive variant.
Acceptance: inspect guarded/native captures for centred content, equal tile height, the deliberate
footer height difference and highlighted Shut Down; pass existing cancellation fixtures and warning-free native rendering. Record installation,
live activation and physical input separately. The [native session implementation](https://github.com/noctalia-dev/noctalia/blob/v5.2.1/src/shell/session/session_panel.cpp)
and [button palette](https://github.com/noctalia-dev/noctalia/blob/v5.2.1/src/ui/controls/button.cpp)
are the versioned reference. See the [comparison evidence](../project/desktop-test-results.md#native-style-power-menu).

Activation constraint (Noctalia 5.2.1): `config-reload` can refresh Luau content while retaining
registered panel dimensions/placement from the previous manifest. A correct isolated preview and
installed files do not prove live geometry. This manifest upgrade requires a Noctalia-only restart
through the Qubix launcher, retaining the existing session environment and the original caller's
GSettings backend before the launcher reapplies its memory backend. Preserve Niri, application
windows and GUI configuration; expect the shell PID to change. Do not toggle plugins through GUI
settings merely to refresh geometry. Capture the live menu after activation; future session startup
reads the new manifest normally. Launch the shell as a detached process and poll IPC readiness;
a short blocking startup timeout can terminate it before readiness. See the [actual activation evidence](../project/desktop-test-results.md#native-style-power-menu).

Super+X, the bar power button and the pinned Power options entry open this panel. It uses the
existing declarative UI runtime, captured press/release events and frame ticks (plugin API 26),
without a service or new target package. Countdown ticks are bounded so a stalled renderer cannot
skip the hold interval. Only after confirmation does it call the existing Noctalia session IPC
with fixed argument arrays; it never runs a privileged command itself. Lock and Lock & Suspend
are disabled when Noctalia locking is disabled. Native power backend overrides remain effective.
This fixed Qubix menu does not adopt native per-row action customizations; those remain preserved
in the separate native menu. No personal configuration is rewritten.

The Control Center's internal power entry still opens Noctalia's native menu. Supply five-second
native countdown defaults for its five entries, but its keys use native tap-to-arm/second-tap-to-confirm
behavior. Direct launcher action results, IPC and the dedicated lock shortcut keep native execution
paths. State this distinction in the operator guide. Native contracts:
[countdowns](https://github.com/noctalia-dev/noctalia/blob/v5.2.1/docs/user/configuration/shell.mdx#session-panel),
[key capture](https://github.com/noctalia-dev/noctalia/blob/v5.2.1/docs/user/plugins/development/declarative-ui.mdx#handling-keys-directly).

Acceptance: no-effect script fixtures cover early release, full hold, repeat, overlapping keys,
mouse countdown/cancellation, mixed input, close/reopen, disabled locking, stalled ticks and exactly
one native IPC invocation; parsed configuration checks original native actions/shortcuts/countdowns,
plugin paths and Qubix entrypoints. Desktop ownership/version fixtures and static checks pass.
Native plugin lint, warning-free TOML validation, rendering, physical input and installation/reload
are separate gates. Never run a real power action during verification.

## Shortcut contract

`Mod` is Super in the main session and Alt in a nested Niri test. Noctalia IPC implements shell actions. These are desktop shortcuts; application copy/paste remains Ctrl+C/V.

| Main-session shortcut | Action |
|---|---|
| Super+Space; Super+D | Launcher |
| Super+T; Super+Return | WezTerm terminal |
| Super+V | Clipboard history |
| Super+Comma | Noctalia settings |
| Super+N | Notification centre |
| Super+Y | Wallpaper picker |
| Super+Tab; Super+O | Niri overview |
| Alt+Tab | Noctalia window switcher |
| Super+W; Super+Q | Close focused window; W is the macOS-inspired alias |
| Super+H/J/K/L or arrow keys | Navigate tiled windows |
| Super+Shift+H/J/K/L or arrow keys | Move tiled windows |
| Super+Ctrl+Alt+arrows or H/J/K/L; Super+Alt+arrows | Focus the screen in that direction |
| Super+Ctrl+Alt+Shift+arrows or H/J/K/L; Super+Alt+Shift+arrows | Move the focused window to the screen in that direction |
| Super+Shift+T | Toggle floating |
| Super+Ctrl+W | Toggle tabbed column |
| Super+Ctrl+Left/Right or H/L | Decrease/increase column width in 5% steps |
| Super+Ctrl+Up/Down or K/J | Decrease/increase window height in 5% steps |
| Super+Ctrl+Shift+Left/Right or H/L | Decrease/increase column width in 10% steps |
| Super+Ctrl+Shift+Up/Down or K/J | Decrease/increase window height in 10% steps |
| Super+Ctrl+R | Reset automatic window height |
| Super+Alt+L | Lock through Noctalia |
| Super+X | Session/power menu |
| Super+Shift+E | Niri's confirmed session exit |
| Super+Shift+S; Print | Niri screenshot picker |
| Super+Shift+/; bar keyboard button | Searchable Qubix shortcut panel |
| Super+F1 | Compact Niri shortcut overlay |

Audio, microphone, media and brightness keys call Noctalia's installed IPC commands. Window/workspace sizing and navigation remain Niri actions. No automatic suspension, logout or lock is performed during deployment/testing.

### Additional resize and movement aliases

Status: **Implemented; controller/native parser/session and zero-change reapplication Tested**.
Keep existing bindings and add 10% resize steps using
Super+Ctrl+Shift+arrows or H/J/K/L. Add a complete equivalent screen-navigation
family using Super+Ctrl+Alt+arrows or H/J/K/L, with Shift to move the focused
window. The extra Ctrl avoids the existing Super+Alt+L lock binding. The earlier
Super+Alt+arrow screen controls remain aliases. Existing 5% resizing and tiled
focus/movement already support both directional key sets.

Acceptance: no duplicate keys, equivalent actions/labels for each arrow/letter
pair, native KDL validation, actual internal/external roundtrips with both key
sets and observable 10% column resizing on a test-owned window, two-file scoped
deployment and zero-change reapplication. Physical keyboard input and stacked
window height resizing retain their separate operator checks. No new packages,
profile variables, output configuration or personal-file ownership.

### Screen navigation

Status: **Implemented; controller/native horizontal dual-screen interaction Tested;
zero-change reapplication Tested**. Native directional monitor bindings ship in the default
Qubix session and generated shortcut panel. Internal/external screens use their
current logical layout, without connector names, monitor configuration writes or
new prerequisites. Moving affects the focused window rather than its whole column.
With one screen, or no screen in the requested direction, native Niri behavior applies.
Existing tile movement, resizing and Super+Alt+L locking remain available.

Acceptance: controller binding/cheatsheet checks, native candidate parser validation,
test-window internal/external focus and movement roundtrips, native no-neighbor
behavior above/below the horizontal target layout, installed KDL and
cheatsheet agreement, primary-session reload without compositor replacement or
personal-config changes, and zero-change reapplication on the selected SSH target.
Physical keyboard input and vertical transfers remain operator checks.
See [native evidence](../project/screen-shortcuts-test-results.md).

## Acceptance and migration

Require measured Niri, WezTerm, jq and supported Noctalia before component writes. Validate generated Niri KDL and Noctalia TOML using their installed parsers; check all palette roles and include complete terminal colours, required by the Noctalia 5.2 palette loader. A custom palette name alone does not prove that its colours loaded. Install the session entry last. Existing Qubix baselines remain immutable.

The native nested test must use a distinct Wayland display/private D-Bus session and temporary Qubix state/data/cache. It must support the existing Niri process whether launched by a user service or directly by SDDM. Disable test-only Polkit registration and clipboard persistence, prove shell/bar/wallpaper/launcher/power-menu/notification/window rendering and IPC, plus dock absence, preserve the original compositor and clean up temporary processes. Main-session physical shortcuts, application launching, authentication, lock/unlock and portal behaviour require operator verification.

After deploying the new defaults, an existing session can reload Niri appearance and shortcuts, but startup commands do not replace already-running companions. The operator-authorized logout/reboot and selection of Qubix Niri activates the new shell. A file install alone is not visual acceptance.

Primary references: [Noctalia configuration roots](https://docs.noctalia.dev/noctalia/configuration/), [palette roles](https://docs.noctalia.dev/noctalia/theming/palette/), [IPC](https://docs.noctalia.dev/noctalia/ipc/), [Niri rounded window rules](https://github.com/niri-wm/niri/wiki/Configuration:-Window-Rules).
