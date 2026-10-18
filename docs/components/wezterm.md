# WezTerm home configuration and transparency

Status: **Home migration and scene transparency correction Implemented and Tested** (2026-10-18).
Acceptance: one canonical repository Lua; install Lua and both palettes into the
measured non-root connection account's `~/.config/wezterm`; back up changed regular
files before replacement; validate native configuration, ownership and idempotency;
prove the compositor background is visible in a private nested comparison. Preserve
all other dotfiles, existing apps, session settings and boot identity.

The single canonical Lua is `roles/qubix_niri/files/wezterm/wezterm.lua`. Original
source digests remain in [provenance](../../assets/wezterm/provenance.json); commit
`e9323c1` preserves the original Lua in Git without a second working-tree copy.
Oxocarbon Dark, Krypton/IBM Plex fallbacks, 0.75 background opacity, RESIZE decorations,
simple/hidden single-tab bar and effective Alt behavior remain as supplied. The
macOS blur setting is guarded; Linux blur is not added. Palettes resolve under
`wezterm.home_dir .. '/.config/wezterm/colors'` rather than `/etc/qubix`.

Enabled Niri deploys three files to the measured account: `wezterm.lua`,
`colors/KAMSuperuser.toml` and `colors/oxocarbon-dark.toml`. This explicit user request
supersedes the previous preserve-only policy for these exact paths. Ordinary Ansible
copy backups retain changed originals beside their destination before replacement.
Other files and existing directory modes remain preserved; symlinked/nonstandard
configuration objects fail preflight before deployment writes. Recovery uses these
named timestamped backups; generic system-file restoration does not restore the home
files automatically. Fresh managed files can be deliberately removed by the owner.

Preflight requires a non-root connection account and the measured home directory.
Deployment runs the home copy as that account, after the native validator is installed.
Direct `wezterm`, the application launcher and shortcuts all use native configuration
discovery. The compatibility wrapper passes through arguments and does not force an
`/etc` configuration. Native explicit flags, `WEZTERM_CONFIG_FILE` and nonstandard XDG
roots retain their documented precedence. Earlier `/etc/qubix/wezterm` resources remain
inert with their historical recovery receipts; they are no longer reconciled.

Niri's focus-ring background can mask translucent client surfaces. A rule scoped to
`org.wezfurlong.wezterm` sets `draw-border-with-background false`, retaining WezTerm's
own 0.75 background opacity and opaque text. See the [upstream rule](https://github.com/niri-wm/niri/wiki/Configuration:-Window-Rules#draw-border-with-background).
Acceptance uses a nested compositor and contrasting synthetic scene backgrounds;
capture the composed output, not only the terminal surface. The previous background
fill is the negative control. Personal content must not appear in captures.

Monaspace NF already ships enabled. Missing IBM Plex faces use native fallback; this
component does not install extra font packages. Native validation uses `ls-fonts` plus
error diagnostics, because CLI exit status alone can hide fallback. Installation,
parser checks, actual scene transparency and physical input remain separate gates.
Existing windows are preserved; native GUI reuse can require a new process to load the
home config immediately. Package-only preparation does not deploy these files.

Earlier [supplied-default evidence](../project/wezterm-test-results.md) records the
superseded system-config layout and window-surface captures; it does not establish
scene transparency for this correction.

The [corrected native evidence and controlled scene captures](../project/wezterm-home-test-results.md)
verify native home loading, backups, refusal, reapplication, live rule reload and actual
background-dependent pixels with the original solid-fill negative control.
