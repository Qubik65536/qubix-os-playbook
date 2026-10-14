# Niri desktop and appearance

Status: **Planned**. Niri is the first complete desktop component; boot themes are independent.

Provide a readable system default, a reusable Qubix colour include, and wallpaper/startup integration suited to discovered applications. Responsibilities include optional bindings/rules and companion application defaults. Niri itself supplies no wallpaper service, notification daemon, launcher, or status bar.

Support initially targets CachyOS Niri. Dependencies: branding assets, a working Niri executable, and measured companions. `niri.enabled` selects this component; `niri.user_config: preserve` is the only bootstrap policy. Existing personal files are always Preserved. Existing `/etc/niri/config.kdl` also needs backup and a reviewed activation policy; do not silently replace a distribution's complete defaults.

Install and validate a candidate before activation. Use `/etc/niri/` where appropriate and validate with `niri validate` against the selected file. Personal configuration can override the system file entirely, so report whether the current session is actually using Qubix defaults. Future personal adoption must be explicitly selected and backed up.

Verification levels: installed files; parser success; companion commands available; actual graphical session with wallpaper, launcher, notifications, bar, terminal, and keybindings functioning. The first two levels alone do not satisfy the desktop milestone.

Restoration removes additive Qubix fragments and restores prior default content/metadata using a manifest. No Niri deployment or restoration procedure is operational yet. Next implementation must use an actual CachyOS target report to select companions and supported directives.
