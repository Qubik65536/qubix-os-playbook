# Shell and terminal defaults

Status: Implemented candidate. Shell selection/personal files are Preserved; startup behaviour needs target verification.

The shell role supplies `/etc/profile.d/qubix.sh`, `/usr/share/qubix/shell/qubix.zsh` and `/etc/qubix/starship.toml`. Foot integration lives in the [Niri component](niri.md). Dependencies are Bash and an optional installed Starship; a plain prompt is the fallback. Configuration uses `shell.enabled`; `change_default_shell` must remain false.

The system fragment sets the Qubix Starship configuration only when neither an explicit `STARSHIP_CONFIG` nor an existing user `starship.toml` under `XDG_CONFIG_HOME` (default `~/.config`) takes precedence. Interactive Bash initializes the measured Starship executable; personal shell initialization may override defaults. Zsh adoption requires manually sourcing the supplied fragment. There is no chsh, user-file write or automatic Zsh adoption.

Native Bash syntax validation precedes installation. A controller fixture checks explicit configuration, existing-user configuration and fallback selection without modifying personal files. Target acceptance requires Foot/login-shell startup, actual prompt, preserved personal configuration and idempotency. Restoration returns only named file baselines through the shared engine. A restored system fragment cannot reverse a user's separately adopted `.zshrc` line; remove that line manually if desired.
