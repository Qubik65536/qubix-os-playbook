# WezTerm defaults from the supplied personal configuration

Status: **Implemented; controller/native installation, parser, rendering, activation and idempotency Tested**. Focused task: vendor the operator-supplied WezTerm Lua and
both colour schemes, make them the Qubix Niri defaults, and validate/deploy/render
on the authorized SSH instance. Acceptance: source provenance and adaptations recorded,
all assets installed with protected baselines, native parser positive/negative controls,
launcher/shortcut integration, personal-config precedence, sanitized native/customized
comparison captures, and zero-change reapplication. No boot/session-manager changes.

The supplied source is `/Users/qubik65536/.config/wezterm` as read on 2026-10-17.
The repository snapshot is independent of that controller path on future deployments.
It includes `wezterm.lua`, `colors/KAMSuperuser.toml` and `colors/oxocarbon-dark.toml`.
Record original checksums alongside the vendored assets. Preserve the selected Oxocarbon
Dark colours, Monaspace Krypton NF / IBM Plex fallback list, 0.75 opacity, RESIZE
window decorations, simple tab bar and hidden single-tab bar. The duplicate left-Alt
assignment is normalized to its effective false value; right Alt remains true.
The macOS-only blur setting is guarded by the target platform; no Linux blur is invented.
The colour directory is explicitly bound to the managed installation for native validation.

The Niri component supplies managed defaults under `/etc/qubix/wezterm`, a terminal
launcher under `/usr/share/qubix/bin`, and an override of the package's desktop entry
in `/usr/local/share/applications` using the same application ID. The package file
remains intact; the ordinary launcher has one effective entry. The file engine permits
only this exact local desktop path for the Niri component, without opening the rest
of `/usr/local` to arbitrary resources. Qubix shortcuts and
TERMINAL select the wrapper. It delegates to native WezTerm unchanged when the caller
supplies explicit CLI configuration/skip flags, `WEZTERM_CONFIG_FILE`, or any existing
native personal configuration candidate (XDG, `.config`, `.wezterm.lua`). Otherwise it
selects the supplied managed config. Existing personal files, preferences and the
account shell are preserved. Restore returns named file baselines; no dotfile adoption.

This is part of enabled `niri.enabled`, with no additional switch. Monaspace NF is
already enabled by the shipped profile. Missing IBM Plex fallback faces use WezTerm's
native font fallback; this task does not install extra font packages. Normal `deploy`
installs the files after package preparation; a package-only preparation does not
activate appearance. An existing WezTerm window retains its selected config; open a
new process to verify the imported defaults. No existing terminal is killed.

See [upstream configuration lookup](https://wezterm.org/config/files.html) for native
precedence. File installation, native parser validation and graphical rendering are
separate evidence gates. Transparency reflects content behind a window; test captures
must use a sanitized backdrop and synthetic content rather than reveal personal windows.

The [SSH evidence and comparison captures](../project/wezterm-test-results.md) record
native positive/negative controls, real Krypton resolution, exact installed bytes/modes,
zero-change reapplication and preserved settings/windows/boot identity. The validator
uses `ls-fonts` with error diagnostics; `show-keys` is not a configuration-load control.
Physical key/launcher input and fallback glyph coverage remain manual acceptance gates.
