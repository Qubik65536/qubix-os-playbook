# Deploy Qubix OS Playbook

Status: **Implemented MVP candidate**. Use an existing CachyOS Niri installation,
initially a disposable VM with a snapshot and console access. Run Ansible directly
on that machine, as the normal desktop account with task-scoped sudo. The playbook,
Python environment, caches and configuration all live on the machine being customized.
Installation, parser validation, graphical session acceptance and boot acceptance
are separate checks. See [actual evidence and open gates](../project/status.md).

## Obtain the playbook

Download `qubix-os-playbook-COMMIT.tar.gz` and `SHA256SUMS` from a GitHub prerelease,
or download/unzip the artifact from a successful **Validate** Actions run. Use the
project repository's own release/run. Keep only the selected archive and checksum
in a new directory. GitHub's automatically generated “Source code” downloads are
not the tested package; use the named playbook asset.

In that directory on the CachyOS Niri machine:

```bash
sha256sum -c SHA256SUMS
# Substitute the full commit shown in the downloaded filename.
tar -xzf qubix-os-playbook-COMMIT.tar.gz
cd qubix-os-playbook-COMMIT
cat SOURCE_REVISION
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
./bootstrap.sh --help
```

Python 3.12+ is required (CI uses 3.13). A Git checkout works too. Always run commands
from this root so Ansible finds its configuration. The archive contains all tracked
source/assets/docs, but excludes downloaded fonts, private compiled UI clients,
Python dependencies, credentials and your machine's configuration. Preparation
therefore requires network access. Keep the archive unchanged: deployment records its
exported commit and `dirty: null`, since Git-free sources cannot prove a clean tree.

## Prepare and configure the target

Complete [installation prerequisites](installation.md) on this machine. Use the shipped
`inventory/local.ini`; it selects localhost over local transport. Run as the desktop
account, never `sudo ./bootstrap.sh` or a root Ansible process. Individual privileged
tasks use sudo with `--ask-become-pass`.

Save overrides in `config/local.yml` and keep credentials out of it. Full defaults
require each preparation step below:

| Requirement | Procedure |
|---|---|
| Native Noctalia/Niri companions | [Local prerequisites](installation.md) |
| Paru, Homebrew, WezTerm, Fcitx/Pinyin/CJK fonts; dependency-safe Alacritty/Foot removal | Preview then run `playbooks/prepare-packages.yml` against the inventory, with sudo prompting |
| Pinned 210-face Monaspace NF source | `.venv/bin/ansible-playbook playbooks/prepare-fonts.yml` on this machine |
| Noctalia Greeter packages and existing greetd launcher | [Login preparation/cutover](login.md); `playbooks/prepare-login.yml` does not switch the active manager |
| Exact supported caption/compact builds, GJS/GTK/fprintd | `playbooks/prepare-ui.yml`; follow the [login guide](login.md) for version/native checks |
| Wi-Fi sharing GUI/backend | Prepare `linux-wifi-hotspot`; see [hotspot setup](hotspot.md) |
| KWallet packages and reviewed existing-secret migration | `playbooks/prepare-keyring.yml` and the [keyring guide](keyring.md) |
| Active bootloader and generator/image mappings | [Boot examples](bootloader.md) and [Plymouth guide](plymouth.md); confirm measured paths, kernels and active loader |

Create `config/local.yml` using the trial example below or your reviewed full
configuration before running preparation. Preview and apply package preparation locally:

```bash
.venv/bin/ansible-playbook -i inventory/local.ini -e @config/local.yml playbooks/prepare-packages.yml --check --ask-become-pass
.venv/bin/ansible-playbook -i inventory/local.ini -e @config/local.yml playbooks/prepare-packages.yml --ask-become-pass
```

This installs Paru, Homebrew on Linux, WezTerm and the [Pinyin prerequisites](../components/input-method.md), then removes Alacritty/Foot
with dependency checks. Full-profile login/UI/keyring preparation has separate
commands in the linked component guides; do not skip those prerequisites.
Font preparation is a separate local command:

```bash
.venv/bin/ansible-playbook playbooks/prepare-fonts.yml
```

It downloads about 315 MiB and extracts about 476 MiB into this machine's cache.
Read each guide before preparation: login requires inactive greetd for package setup,
UI builds require the exact supported versions, and KWallet needs reviewed secret migration.
Package hooks may update native snapshots/boot menus; package transactions are outside
file restoration. `deploy` does not invoke preparation or switch managers.

For a first desktop-only trial, save this complete **explicit opt-out** configuration
as `config/local.yml`. It deliberately differs from the shipped full defaults:

```yaml
qubix_discovery_privileged: true
qubix:
  profile: cachyos-niri
  niri:
    fingerprint_setup: false
    presentation: native
  login:
    enabled: false
    compact: false
  keyring:
    enabled: false
  bootloader:
    enabled: false
  plymouth:
    enabled: false
```

This retains fonts/Krypton, branding, Niri/Noctalia/WezTerm and shell defaults.
Prepare the native companions, `prepare-packages.yml` and fonts before this trial.
For full deployment, remove those opt-outs only after satisfying the table above,
then add the measured bootloader/Plymouth mappings from their guides. Missing overrides
retain the enabled profile defaults; never invent boot confirmations or kernel paths.

After preparation, Bash/Zsh can use Brew immediately with
`eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"`; Fish uses
`/home/linuxbrew/.linuxbrew/bin/brew shellenv fish | source`. Persistent shell setup is
your choice; the playbook does not edit shell dotfiles. Existing working Brew is preserved.

## Enabled by default

The authoritative [28-input defaults reference](../architecture/configuration.md#every-effective-default)
is checked against `config/defaults.yml` plus `config/profiles/cachyos-niri.yml`.
With no overrides, every implemented component is selected:

| Enabled selection | Included behavior |
|---|---|
| Fonts + Krypton UI | All 210 official Monaspace NF faces; Fontconfig/GTK/Qubix UI preferences |
| Branding | Attributed original-colour cube/logo, wallpaper and shared palette |
| Qubix Niri/Noctalia | Separate session, bar/launcher/notifications, 100% output scale, shortcuts and guarded power menu |
| Pinyin (part of Niri) | Simplified Chinese via Fcitx 5; Ctrl+Space toggles English/Pinyin; saved personal input profiles take precedence |
| WezTerm (part of Niri) | Terminal shortcuts/launcher, supplied Lua/two palettes, Oxocarbon Dark and 75% opacity; backs up the three managed account files |
| Fingerprint setup | GTK enrollment/test application; enrollment and biometric authentication remain explicit |
| Qubix presentation | Prepared private Noctalia caption build; native distribution identity stays intact |
| Shell defaults | Additive Bash/Starship and optional Zsh integration; existing shell remains selected |
| Compact Noctalia/greetd login | Appearance on the prepared existing launcher, without a service switch |
| KWallet | Secret Service/KDE integration and narrowly measured greetd PAM keyring hooks after reviewed migration |
| Bootloader appearance | Existing GRUB or Limine adapter, after explicit active-loader confirmation |
| Plymouth | Existing dracut or mkinitcpio integration, after explicit image/kernel/preset confirmation |

Enabled means selected for validation, not silently installed despite missing prerequisites.
Boot confirmations default **false**, backends remain `auto`, and paths/image/preset mappings
remain unset. A full default deployment therefore fails until you supply measured inputs.
Boot activation uses explicitly authorized disposable VMs. Account-shell switching is false,
Niri personal-config handling is `preserve`, early graphics is `preserve`, and forced image
rebuilds are false. Personal files remain preserved except the three explicitly managed
WezTerm account files. The separate Limine OS-label command, manager cutover, secret
migration and actual fingerprint enrollment are manual operations, not default deployment steps.
All exceptions and ownership details live in the configuration reference.

## Inspect, preview, deploy and verify

After preparation and configuration:

```bash
./bootstrap.sh verify -i inventory/local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh deploy -i inventory/local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh verify -i inventory/local.ini -e @config/local.yml --tags installed --ask-become-pass
```

For private boot metadata, set the YAML boolean `qubix_discovery_privileged: true`
outside `qubix` as in the trial example. This permits read-only privileged probes;
it confirms no boot selection. No SSH authentication is involved.
Use YAML component selections; the wrapper rejects deploy/restore tags.

Check mode is an approximation and cannot validate files it has not installed.
Deployment backs up named resources, installs and validates files, then records
revision/configuration receipts. A failure may leave earlier resources installed;
inspect pending diagnostics and use [restoration](restoration.md). Concurrent
package updates/deployments are unsupported.

Repeat the same deployment to check idempotency. When convenient, log out and select
**Qubix Niri**, preserving native Niri as fallback. No manager restart/current-session
switch happens during deployment. Follow [desktop usage](desktop.md), then check the terminal, launcher, shortcuts, lock and
login separately using the [verification checklist](verification.md). File receipts
never assert graphical/boot success. Only reboot an authorized test VM after reviewing
its boot mappings and recovery plan; test each loader/generator combination separately.

## Recover

Review [restoration and its limits](restoration.md), then preview:

```bash
./bootstrap.sh restore -i inventory/local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh restore -i inventory/local.ini -e @config/local.yml --ask-become-pass
```

Restoration uses protected first baselines, not whole-system rollback. Packages and
secret migration are separate. Recover WezTerm account files using their timestamped
home-file backups; generic system restoration does not reverse these copies. Keep the
VM snapshot for boot failures. Report commit, sanitized configuration, file/parser
results, session observations and boot observations separately.
