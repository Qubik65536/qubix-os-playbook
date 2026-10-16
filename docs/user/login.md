# Noctalia Greeter on CachyOS

Status: **Implemented; installation, native UI preview and unchanged reapplication Tested;
selected for the target's next boot with operator approval; actual login acceptance pending**.
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
refresh Snapper snapshots and Limine's snapshot menu. The preparation task does not directly run
the upstream setup script or start/enable a service. CachyOS's greeter **package post-install hook**
does run that script: on this fresh installation it appends `session required pam_systemd.so`
to the newly installed greetd PAM file. Its authentication rules and all pre-existing PAM files
remain unchanged; this is native package session integration, not fingerprint configuration.

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
The adapter also requires the native greetd unit without launcher flags, drop-ins or environment
overrides and refuses a legacy `greetd.conf` that would shadow the inspected `config.toml`.
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

The configured target's approved transition retains the original greetd file and metadata under
`/var/lib/qubix/login-transition-b08727c/`. To return its **next-boot** selection to the recorded
SDDM setup from a recovery shell:

```bash
sudo systemctl disable greetd.service
sudo install -o root -g root -m 0644 /var/lib/qubix/login-transition-b08727c/config.toml /etc/greetd/config.toml
sudo systemctl enable sddm.service
```

These commands restore future startup selection; they do not stop an active desktop. The current
selection is greetd enabled/SDDM disabled, with SDDM still active until the operator reboots.
The ready local override is `config/login.local.yml`; change `activation` to `existing` after
greetd is actually running. Actual password/fingerprint login still requires console acceptance.

## Names in Noctalia and Limine

The stock Noctalia 5.3 launcher reads its distribution caption from `/etc/os-release` or
`/usr/lib/os-release`; its Control Center Home version caption is hardcoded. The optional Qubix
presentation build below changes just those two captions while preserving native system identity.
The System tab continues to report CachyOS. See the upstream
[detector](https://github.com/noctalia-dev/noctalia/blob/v5.3.0/src/system/distro_info.cpp).

Limine already uses `interface_branding: Qubix OS` in its owned appearance block. Native CachyOS
entry titles normally remain preserved. The explicit display-name task below changes the OS
menu title separately from that heading; entry IDs, snapshots and boot payloads stay preserved.

## Compact greeter and QubixOS captions

The optional [presentation variants](../../assets/ui/README.md) are pinned UI-only builds of
Noctalia 5.3.0 and Greeter 1.6.0. They are installed separately from native package executables.
Use the ordinary controller/inventory setup and an ignored desktop-only configuration:

```yaml
qubix_discovery_privileged: true
qubix:
  niri:
    fingerprint_setup: true
    presentation: qubix
  login:
    enabled: true
    backend: greetd
    theme_source: noctalia
    activation: existing
    compact: true
  bootloader: {enabled: false}
  plymouth: {enabled: false}
```

Only use `existing` once greetd is running; use `prepare` with inactive greetd. Compact mode
requires Noctalia's native wrapper already selected; it does not perform the manager cutover.

```bash
ANSIBLE_HOME="$PWD/.cache/ansible" .venv/bin/ansible-playbook playbooks/prepare-ui.yml \
  -i inventory/target.local.ini -e @config/ui.local.yml --ask-become-pass
ANSIBLE_HOME="$PWD/.cache/ansible" .venv/bin/ansible-playbook tests/integration/ui.yml \
  -i inventory/target.local.ini -e @config/ui.local.yml --ask-become-pass
```

Preparation installs missing build/GJS prerequisites, verifies source/patch checksums and
compiles two clients as the ordinary user. It stages generated artifacts and exact native-binary
provenance; it does not install upstream hooks or change running services. The isolated preview
uses synthetic identity/scans and disconnected authentication, not real biometric enrollment.
Then run the normal `deploy --check --diff`, `deploy` and `verify --tags installed` with this file.

The launcher caption becomes **QubixOS** and Control Center Home shows
**QubixOS (Noctalia v5.3.0)**. Activate the new shell through the existing
[Noctalia-only procedure](../architecture/desktop-design.md#power-action-countdown), preserving
the session environment, Niri, applications and GUI state. `config-reload` alone cannot switch
the running binary. The compact greeter is selected by a backed-up command-only replacement in
`/etc/greetd/config.toml`; the wrapper uses the native compositor/session launcher. A running greetd
retains its launcher until a later service start; no restart or reboot is performed by deployment.

Both selecting wrappers fall back to the updated native client if its binary checksum changes,
including updates within the same upstream version. Redeployment refuses stale provenance.
Review the updated package/source before rebuilding its generated cache; keep the updated native
client available meanwhile. PAM, Polkit, keyboard/display settings and passwords remain preserved.

To leave caption customization, deploy `niri.presentation: native`. To leave compact mode, first
restore the `default_session.command` to `/usr/bin/noctalia-greeter-session`, preserving the rest
of greetd's configuration, then deploy `compact: false`. No running login service is restarted.
Generic restoration retains the original first-baseline semantics described in the recovery guide.

## Requested Limine OS menu title

For the measured `/boot/limine.conf` on this target, the separate bounded task renames just
`/+CachyOS` to `/+QubixOS` and sets native `TARGET_OS_NAME="QubixOS"` in `/etc/default/limine`.
Both native entry and snapshot tools read that target; the machine-ID binding is retained.
Preview before applying:

```bash
ANSIBLE_HOME="$PWD/.cache/ansible" .venv/bin/ansible-playbook playbooks/menu-label.yml \
  -i inventory/target.local.ini -e '{"qubix_discovery_privileged":true,"qubix_menu_confirm":true,"qubix_menu_config":"/boot/limine.conf"}' \
  --check --diff --ask-become-pass
```

Remove `--check` to apply the requested label. The task refuses ambiguous menus, wrong machine-ID
bindings, custom generator targets and enabled/ambiguous EFI config enrollment before any writes;
it never invokes a generator, image rebuild or reboot.
Native kernel-entry names, IDs, paths, hashes, ordering, arguments and snapshot contents are identical.
Before a generic boot restoration, run this same task with `-e qubix_menu_display_name=CachyOS`.
This reverses the display title first so the normal preserved-entry guard still protects boot data;
general restoration then returns original defaults. Native snapshot/kernel changes still require
the existing reviewed recovery procedure rather than overwriting a stale config.
