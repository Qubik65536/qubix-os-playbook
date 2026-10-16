# Noctalia Greeter on CachyOS

Status: **Implemented; package installation and native UI preview Tested; login acceptance pending**.
The [login contract](../components/login.md)
defines support and ownership. The greeter uses greetd; it is a different login manager from SDDM.
Preparation keeps SDDM active. Bootstrap never switches display managers.

## Install prerequisites and theme

After the usual [controller setup](installation.md), inspect the package transaction:

```bash
ANSIBLE_HOME="$PWD/.cache/ansible" .venv/bin/ansible-playbook playbooks/prepare-login.yml \
  -i inventory/target.local.ini -e '{"qubix_discovery_privileged":true}' --check --ask-become-pass
```

Remove `--check` to install. The separate preparation playbook installs missing `greetd` and
`noctalia-greeter` packages with native Pacman and initializes absent state using the package's
tmpfiles rule. It does not refresh repositories or upgrade the whole system; use the normal
CachyOS upgrade procedure first if your system/repositories are stale. Native package hooks may
refresh Snapper snapshots and Limine's snapshot menu. The playbook never runs the upstream
setup script, which may adjust PAM, or starts/enables a service. Package-provided PAM files are
installed with greetd; existing authentication files remain preserved.

Use a separate ignored configuration file based on the desktop profile. Keep bootloader and
Plymouth disabled for this login-only change:

```yaml
qubix_discovery_privileged: true
qubix:
  profile: cachyos-niri
  login:
    enabled: true
    backend: greetd
    theme_source: noctalia
    activation: prepare
  bootloader:
    enabled: false
  plymouth:
    enabled: false
```

Run the usual `bootstrap.sh deploy --check --diff`, `deploy` and `verify --tags installed` with
that file, your inventory and sudo authentication. The existing branding/Niri/shell selections
remain enabled by the profile. Only select `activation: prepare` while greetd is inactive.
The theme uses the shared Qubix steel-blue palette and cube wallpaper, dark panels and matching
corner radii. It preserves input, display, user, session, auth and mutable `sync.toml` settings.
The initial unused Noctalia wordmark is hidden; the original-colour cube is in the wallpaper.

The owned file is `/var/lib/noctalia-greeter/greeter.toml`. Its directory remains owned by the
native greeter account; the administrator configuration is installed root-owned/readable at 0644.
The first original bytes/metadata are retained by the shared recovery engine. Noncanonical
appearance tables, redirected paths and unreviewed versions are refused before writes.
GUI Sync writes lower-priority `sync.toml`; Qubix's declared palette/wallpaper continue to win.

## Preview and review

Run the optional native comparison on an already-running Niri desktop:

```bash
ANSIBLE_HOME="$PWD/.cache/ansible" .venv/bin/ansible-playbook tests/integration/login.yml \
  -i inventory/target.local.ini -e @config/login.local.yml --ask-become-pass
```

This displays a temporary nested window. It uses the real greeter binary with fake user data,
a private D-Bus session, isolated state, disabled system-bus access and no authentication service.
It captures reference/Qubix screenshots under `.cache/native-login/`, checks personal settings and
the original Niri process, and cleans up. A login-service-unavailable indication is expected.
This preview tests the native UI client under Niri; it does not test the bundled compositor's
DRM/VT path, a real greetd conversation, password input or login. See the
[comparison evidence](../project/login-test-results.md).

## Separately reviewed login-manager cutover

The repository prohibits replacing a display manager for branding. A real cutover needs an explicit
operator exception after reviewing the prepared theme, console recovery and native configuration.
Do not stop SDDM while relying on its current graphical session. Keep an independent root-capable
TTY/SSH shell, record whether SDDM and its alias were enabled, and take a VM snapshot where possible.

Inspect and back up `/etc/greetd/config.toml` with its original ownership/mode. Merge only the
`[default_session]` example in `/usr/share/qubix/login/greetd-default-session.toml`; retain the native
terminal, `[general]`, initial session and other settings. Confirm the example's `greeter` account
matches the package-created state directory's owner. Use the full wrapper path
`/usr/bin/noctalia-greeter-session`, not the UI executable. Inspect `noctalia-greeter sessions` and
select **Qubix Niri** at the first login. Do not invent a native session command or enable autologin.

Once explicitly authorized, a maintenance cutover can disable the recorded old manager for the
next boot and enable greetd **without `--now`**, then schedule the reboot after saving work.
Review `systemctl is-enabled sddm greetd` and the `display-manager.service` link to ensure a single
manager is selected. Neither service switch nor reboot is automated by these playbooks.
The upstream [installation guide](https://docs.noctalia.dev/greeter/installation/) explains greetd's
wrapper/account requirements; its immediate-stop commands must not be run inside an unsaved session.

At the console establish password login and the expected Niri session before attempting
[fingerprints](fingerprint.md). Test a wrong password, successful login, logout, another login and
return after reboot. Record this separately from files and preview rendering.

After a successful manual transition, use `activation: existing` for future theme deployments.
That mode requires only greetd active and the exact existing native wrapper command. Preparation
refuses an active greetd; it cannot accidentally reconfigure a running login screen.

For recovery use the independent shell to disable greetd, restore the exact greetd configuration
backup and return the original SDDM enablement/alias. Start the original manager only after any
current graphical work has been closed; do not run both managers. The generic `bootstrap.sh restore`
restores **all recorded Qubix resources**, including this appearance, but it does not undo packages,
native package hooks, manual PAM edits or manual manager selection. See [restoration](restoration.md).

## Names in Noctalia and Limine

The Noctalia 5.3 Control Center's system label is read from `/etc/os-release` or
`/usr/lib/os-release`. Its measured configuration has no supported distribution-label override.
Qubix preserves both files and the native CachyOS identity; this task does not patch the installed
shell or rename your account/hostname. See the upstream
[detector](https://github.com/noctalia-dev/noctalia/blob/v5.3.0/src/system/distro_info.cpp).

Limine already uses `interface_branding: Qubix OS` in its owned appearance block. Native CachyOS
entry titles/IDs, snapshot sections and kernel arguments remain unchanged. The heading is separate
from the native entries; this task does not regenerate or rename them.
