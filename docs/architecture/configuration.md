# Configuration contract

Status: **Implemented and fixture-tested schema**. `qubix` is the operator input; resolved configuration is an internal fact. Only profile `cachyos-niri` is initially allowed.

```yaml
qubix:
  profile: cachyos-niri
  fonts:
    enabled: true
    krypton_ui: true
  branding:
    enabled: true
  niri:
    enabled: true
    user_config: preserve
    fingerprint_setup: true
    presentation: qubix
  shell:
    enabled: true
    change_default_shell: false
  login:
    enabled: true
    backend: greetd
    theme_source: noctalia
    activation: existing
    compact: true
  hotspot:
    enabled: true
  keyring:
    enabled: true
  bootloader:
    enabled: true
    backend: auto
    config_path: ''
    confirm_active: false
    limine_version: 0
  plymouth:
    enabled: true
    initramfs_backend: auto
    confirm_active: false
    force_rebuild: false
    early_graphics: preserve
    images: []
    presets: []
```

Resolution order is `config/defaults.yml` (complete schema fallbacks), then
`config/profiles/cachyos-niri.yml` (the shipped feature selections), then the operator
`qubix` mapping (recursive overrides). The YAML above is the effective configuration
with no overrides; the false values in the fallback file alone are not the shipped behavior.

The current profile enables fonts/Krypton, branding, Qubix Niri, fingerprint setup,
Qubix captions, shell defaults, compact Noctalia/greetd appearance, KWallet, bootloader
appearance and Plymouth integration. Its [desktop design](desktop-design.md) uses measured standalone Noctalia with separate Qubix defaults and GUI state; desktop shell selection is fixed for this initial profile. All candidate components have implementations; unsupported selections still fail explicitly. Bootloader and Plymouth are enabled and require explicit target confirmation and authorization. No fallback from a mistyped profile or backend.

Booleans must be YAML booleans, not strings. Each nested mapping allows only documented keys. `user_config` initially accepts only `preserve`; an adoption interface requires its own consent and recovery design. `change_default_shell` must be false during bootstrap. Login backend allows `auto`, `sddm`, `greetd`, `gdm`, `lightdm`; bootloader allows `auto`, `grub`, `limine`; initramfs allows `auto`, `dracut`, `mkinitcpio`. Allowing a value in the schema does not implement an adapter.

## Every effective default

| Input under `qubix` | Default | Effect |
|---|---|---|
| `profile` | `cachyos-niri` | Only supported deployment profile; other distributions/desktops fail validation. |
| `fonts.enabled` | `true` | Install all 210 pinned official Monaspace NF faces after controller preparation. |
| `fonts.krypton_ui` | `true` | Prefer Krypton for generic UI/monospace defaults and Qubix shell text; saved choices win. |
| `branding.enabled` | `true` | Install shared original-colour Qubix artwork and attribution. |
| `niri.enabled` | `true` | Install the Qubix Niri/Noctalia session, supplied WezTerm appearance, terminal integration and Simplified Chinese Pinyin with dark horizontal candidate defaults. |
| `niri.user_config` | `preserve` | Keep native/personal Niri files; no automatic dotfile adoption. |
| `niri.fingerprint_setup` | `true` | Install the enrollment application; never enroll a finger or enable fingerprint PAM automatically. |
| `niri.presentation` | `qubix` | Select prepared, version-pinned Qubix caption builds; retain native system identity. |
| `shell.enabled` | `true` | Install additive shell/terminal defaults while preserving personal configuration. |
| `shell.change_default_shell` | `false` | Keep the account shell; automatic switching is unsupported. |
| `login.enabled` | `true` | Install appearance on the supported existing manager after all prerequisites pass. |
| `login.backend` | `greetd` | Require existing greetd; never replace another manager automatically. |
| `login.theme_source` | `noctalia` | Use the native Noctalia Greeter appearance interface and shared palette/wallpaper. |
| `login.activation` | `existing` | Require the active supported launcher; inactive preparation is a separate explicit selection. |
| `login.compact` | `true` | Select the prepared compact private greeter client through its backed-up wrapper. |
| `hotspot.enabled` | `true` | Add the native Share Wi-Fi launcher after separate package preparation; starting/sharing requires runtime adapter support and user action. |
| `keyring.enabled` | `true` | Select KWallet, replace only measured greetd keyring hooks and suppress GNOME Keyring startup. |
| `bootloader.enabled` | `true` | Select boot appearance; require confirmed target configuration before writes. |
| `bootloader.backend` | `auto` | Unresolved placeholder; activation needs explicit `grub` or `limine`. |
| `bootloader.config_path` | `''` | No guessed active configuration path. |
| `bootloader.confirm_active` | `false` | No default confirmation of the loader running in firmware. |
| `bootloader.limine_version` | `0` | Unknown major; Limine activation requires the observed supported major. |
| `plymouth.enabled` | `true` | Select splash integration; require confirmed image/generator mappings before writes. |
| `plymouth.initramfs_backend` | `auto` | Unresolved placeholder; activation needs explicit `dracut` or `mkinitcpio`. |
| `plymouth.confirm_active` | `false` | No default confirmation of active initramfs selection. |
| `plymouth.force_rebuild` | `false` | Rebuild only when required; no forced repeat generation. |
| `plymouth.early_graphics` | `preserve` | Keep existing early graphics; no default framebuffer/hardware selection. |
| `plymouth.images` | `[]` | No image/kernel/active-cache mappings are assumed. |
| `plymouth.presets` | `[]` | No mkinitcpio presets selected; dracut does not use this list. |

`qubix_discovery_privileged` is an operational input outside `qubix`, default false.
True authorizes read-only privileged metadata probes; it does not enable a component or
confirm any boot selection. Enabled boot components also require privileged metadata reads,
so full-profile inspection may need `--ask-become-pass`. Credentials, inventory and personal
machine mappings never ship.

## Default feature policy and final-deployment preparation

Status: Implemented; boot-default refusal/opt-out fixtures Tested in normal/check mode. Focused acceptance: both components resolve
enabled without overrides, explicit false overrides work, and unresolved boot inputs fail
both adapters before filesystem writes in normal/check mode.

Focused task: promote implemented desktop/login/storage capabilities into the shipped
CachyOS Niri profile and explain every effective input. Acceptance: profile resolution
and explicit opt-outs pass fixtures; the complete reference matches the resolved profile;
unsupported combinations still fail before writes; preparation and exceptions are documented.
This prepares defaults for final deployment; it does not establish new physical login or boot evidence.

New implemented features must be enabled by default in the supported profile unless the
user directs otherwise. Add their prerequisites and acceptance tests when introducing them.
An absent prerequisite causes an actionable preflight failure, rather than silently dropping
an enabled feature. Record exceptions here with their specific reason. Planned/unsupported
implementations cannot be enabled to claim readiness. A default selection does not install
packages, build presentation binaries, migrate personal secrets, select a manager or reboot.

The shipped target is a prepared CachyOS Niri system with the measured Noctalia/greetd
launcher already selected. Before ordinary deployment, prepare the pinned fonts, native UI
packages/private builds and KWallet packages, review existing secret migration, and establish
the supported greetd configuration through the separately authorized manager procedure.
An SDDM or unprepared machine must use explicit overrides or complete that preparation;
the profile never infers permission to switch its manager. Fresh-machine setup is not
automated by `deploy`; preparation playbooks are separate commands and manager/secret
transitions retain their operator steps. See [preparation](../user/getting-started.md).

Explicit target selections and preserved defaults:

- `bootloader.enabled` and `plymouth.enabled` now default true as explicitly requested.
  Selection still requires confirmed active loader/generator paths, versions and image/kernel
  mappings before writes. The disposable-VM authorization policy remains in effect; enabling
  a profile flag does not confirm a specific machine. Explicitly set either flag false to opt out.
  GRUB, Limine, dracut and mkinitcpio remain mandatory MVP work.
- Boot/splash `confirm_active` remains false; `backend: auto`, empty paths/images/presets and
  `limine_version: 0` are unresolved placeholders, never authorization or guessed hardware values.
- `plymouth.early_graphics: preserve` retains existing hardware behavior. Selecting `simpledrm`
  requires the measured supported environment and explicit boot configuration.
- `plymouth.force_rebuild: false` avoids rebuilding unchanged images; true is a deliberate repair override.
- `niri.user_config: preserve` and `shell.change_default_shell: false` protect personal setup.
  Automatic adoption/default-shell replacement is unsupported.
- `login.activation: existing` requires the selected active manager. Preparation and manager cutover
  are explicit operations; enabling login appearance never switches services.

## Ownership

| Policy | Meaning | Examples |
|---|---|---|
| Managed | Qubix reconciles content in a Qubix namespace | `/usr/share/qubix/branding/` |
| Default | Operator selects supplied defaults; explicit Qubix session does not inherit personal Niri settings | `/etc/niri/qubix/` defaults and terminal defaults |
| Preserved | Detect and report without modifying | Dotfiles, boot entries, kernel arguments, encryption, `/usr/lib/os-release` |

Existing non-Qubix system defaults require backup and an explicit activation policy before replacement. Additive fragments are preferred. A file's presence does not prove the application loaded it.

Login supports already-active SDDM with `theme_source: breeze`, `activation: existing` and
validated background/type options. Its native authentication QML is copied unchanged.
Noctalia Greeter uses explicit `backend: greetd`, `theme_source: noctalia` and
`activation: prepare|existing`. Preparation requires greetd inactive and stages its appearance;
existing requires only greetd active and the measured native wrapper already selected.
Both preserve PAM, services and session startup. See the authoritative
[login component contract](../components/login.md) and [operator guide](../user/login.md).

`niri.fingerprint_setup: true` installs the optional GTK 4/GJS enrollment application;
installed `gjs`, `gtk4` and `fprintd` are required before writes. `niri.presentation: qubix`
selects a prepared private Noctalia 5.3.0 UI build for display captions. `native` keeps the
distribution binary. `login.compact: true` requires Noctalia Greeter 1.6.0, a prepared private
UI build and an already-selected Noctalia launcher, then backs up/replaces only that launcher
command with a wrapper around the native compositor. All three options are enabled by the shipped profile; explicitly select false/native to opt out.
See the [presentation/enrollment contract](login-refinement.md); preparation, file installation,
session activation and actual authentication are separate gates.

Boot activation requires `backend: grub|limine`, confirmed `config_path` and `confirm_active: true`. Limine additionally requires the observed booted major `limine_version` (8–12). Auto/unknown configurations fail before writes. Native configs and boot entries remain preserved except minimal supported appearance changes.

Plymouth needs a confirmed generator, explicit images (path, kernel version and kernel_image), and mkinitcpio preset names. All selected preset outputs must be mapped. force_rebuild is an explicit repair override, normally false. Plain initramfs images are supported; UKI signing and encrypted/hardware/kernel arguments remain outside ownership.

`plymouth.early_graphics` accepts `preserve` (default) or `simpledrm`. The latter explicitly selects
the existing firmware framebuffer through native Plymouth configuration on a supported daemon;
it does not alter kernel arguments or GPU modules. See the [early graphics contract](../components/plymouth.md#early-graphics-repair).

Active-image binding: each image may additionally declare both limine_image and limine_kernel_image for the existing native cache pair. These require the confirmed Limine config/backend and exact file/reference/kernel validation. Verified generated images are staged at content-addressed Qubix paths before updating only the bound module aliases/checksums; native cache/snapshot images remain preserved. See the [component contract](../components/plymouth.md#active-limine-image-repair). Without a valid active-image binding, cached Limine startup branding must fail explicitly.

`fonts.enabled` installs the pinned official Monaspace NF desktop families.
`fonts.krypton_ui` selects Krypton UI defaults independently and requires fonts enabled.
Both default true in this profile. Set only `krypton_ui: false` to keep the fonts and
remove the alias preference on reapplication. See the authoritative [font contract](../components/fonts.md)
for preparation, preserved application/user choices, cache handling and activation limits.

`keyring.enabled: true` selects KWallet on an existing greetd system and is the shipped profile default.
This is the narrow exception to preserved PAM: only measured optional keyring hooks in
`/etc/pam.d/greetd` are replaced, after native package preparation and operator secret migration.
All other authentication and personal stores stay preserved. Disabled does not undo an earlier
activation; use backed-up restoration. See the [keyring contract](../components/keyring.md).

The standard CachyOS package preparation now installs Paru, Homebrew on Linux and
WezTerm and removes the two stock terminals, Alacritty and Foot, with dependency
checks. This explicit preparation command has no additional feature toggle; Niri
requires WezTerm by default. Bootstrap/deploy continue to validate prepared packages
without running package transactions. Personal terminal settings remain Preserved.
See the [package and terminal contract](../components/package-management.md).

Enabled Niri now includes the supplied [WezTerm appearance defaults](../components/wezterm.md):
managed Lua/palettes and a personal-config-aware launcher/desktop entry. They ship by
default without a separate switch; native explicit config retains precedence; the three requested account files are managed with backups.
The package desktop file stays Preserved; its same-ID local default override uses
protected baselines. No account dotfiles are installed or adopted.

The 2026-10-18 user-directed exception manages only `~/.config/wezterm/wezterm.lua`
and its two supplied palettes in the measured non-root connection account. Changed
regular files receive timestamped Ansible backups before replacement; symlinks fail
preflight. All other personal files remain Preserved. Direct native WezTerm loading
now replaces the earlier system-config fallback wrapper. See the [home configuration
and transparency contract](../components/wezterm.md). Generic system restoration does
not reverse these account copies; recover using the retained home-file backups.

The user-facing [deployment defaults summary](../user/deployment.md#enabled-by-default)
links to the exhaustive table above. Packaging changes no effective feature defaults;
package caches, private builds and machine inputs still require separate preparation.

User preparation and deployment run locally on the machine being customized, using
`inventory/local.ini` as the ordinary desktop account. In that mode the Ansible
controller and target are the same machine: font/UI preparation caches stay there,
Homebrew belongs to that account, and its WezTerm files receive the documented backups.
SSH is reserved for developer testing; see the [deployment transport policy](deployment.md#user-deployment-and-developer-transport).

`hotspot.enabled` adds the [native Wi-Fi sharing launcher](../components/hotspot.md).
Prepare `linux-wifi-hotspot` separately; no service or hotspot starts during deployment.
Hardware/driver/channel support is checked by the native application when starting.

Enabled Niri includes [zh-Hans Pinyin](../components/input-method.md) by default,
without another toggle. Separate package preparation supplies Fcitx 5, Chinese addons,
GTK/Qt modules and CJK fonts. Managed defaults retain personal Fcitx precedence;
existing profiles are deliberately preserved and may need Pinyin added manually.
This preservation exception prevents replacing saved engines, dictionaries and shortcuts.

Pinyin's managed global Fcitx defaults disable its Super+Space and Shift+Super+Space
group-switch bindings to avoid the Niri launcher conflict; Ctrl+Space remains the input
toggle. Existing personal global input settings retain precedence and are never rewritten.

The Niri candidate UI is default-enabled alongside Pinyin. Its shared Fcitx Default
lives at `/etc/xdg/fcitx5/conf/classicui.conf`, with Managed theme assets in
`/usr/share/fcitx5/themes/qubix/`, because GTK client rendering uses standard XDG
paths. This affects Fcitx in other sessions without personal UI settings; native
session configuration itself stays preserved. Personal UI overrides are preserved.
See the [input ownership and acceptance contract](../components/input-method.md).

Enabled Niri includes the [screen-navigation shortcuts](desktop-design.md#simple-directional-controls-and-adaptive-keycaps)
by default, without a separate toggle or additional prerequisites. They use native
monitor actions and preserve output layout and personal configuration.

Enabled Niri uses the distribution's `niri-session` launcher with the explicit
Qubix `NIRI_CONFIG`, including its native graphical-session lifecycle by default.
This needs no new profile input or resource. Native service units, portal selection,
Slack settings and audio-device choices remain Preserved. See the
[session lifecycle contract](../components/niri.md#native-session-lifecycle-and-huddles-repair).

The operator-selected ThinkPad has a measured Slack GPU rendering failure. Its
new account-only Slack launcher uses `--disable-gpu` after successful Huddle
acceptance. This application-specific exception is not a global profile default:
other hardware has not demonstrated the failure, and disabling GPU acceleration
can increase CPU work. Native Slack resources and saved preferences stay preserved.
See [evidence and recovery](../project/huddle-test-results.md).

The default Niri directional controls use at most two modifiers: Super for
window/screen focus, Shift to move tiles, Ctrl to resize and Alt to send a window
to another screen. Both arrows and H/J/K/L work; Super+Escape locks. These replace
the earlier high-modifier aliases. The generated cheatsheet uses intrinsic keycap
sizes and wrapping, without new prerequisites or profile inputs. See the
[shortcut contract](desktop-design.md#simple-directional-controls-and-adaptive-keycaps).
