# Supplied WezTerm configuration

The operator explicitly supplied their `~/.config/wezterm` on 2026-10-17 for inclusion
in Qubix OS Playbook. `source/` retains the original palette files byte-for-byte; the original Lua is
recoverable from commit `e9323c1` rather than duplicated in the working tree.
[provenance.json](provenance.json) binds their SHA-256 digests. Deployment reads the
repository snapshot and never depends on the original controller home directory.

The two TOML files retain their own upstream origin URLs. Their shipped copies add
only a final newline. The single canonical Lua under `roles/qubix_niri/files/wezterm` uses the account
configuration colour directory,
guards macOS blur, and drops the superseded left-Alt=true assignment and unused
commented scheme choices. Oxocarbon Dark, Krypton/IBM Plex fallbacks, transparency
and effective Alt behavior remain as supplied. No theme/logo colours are transformed.

See the [component contract](../../docs/components/wezterm.md) for ownership,
configuration precedence, prerequisites, validation and activation.
