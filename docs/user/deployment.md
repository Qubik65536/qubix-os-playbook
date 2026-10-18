# Deploy Qubix OS Playbook

Status: **Implemented MVP candidate**. Use an existing CachyOS Niri installation,
initially a disposable VM with a snapshot and console access. Ansible runs on a
Mac/Linux controller and copies resources over SSH; the target needs no checkout.
Installation, parser validation, graphical session acceptance and boot acceptance
are separate checks. See [actual evidence and open gates](../project/status.md).

## Obtain the playbook

Download `qubix-os-playbook-COMMIT.tar.gz` and `SHA256SUMS` from a GitHub prerelease,
or download/unzip the artifact from a successful **Validate** Actions run. Use the
project repository's own release/run. Keep only the selected archive and checksum
in a new directory. GitHub's automatically generated “Source code” downloads are
not the tested package; use the named playbook asset.

In that directory on the controller:

```bash
shasum -a 256 -c SHA256SUMS
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
controller dependencies, credentials and your machine's configuration. Preparation
therefore requires network access. Keep the archive unchanged: deployment records its
exported commit and `dirty: null`, since Git-free sources cannot prove a clean tree.

## Prepare and configure the target

Follow [getting started, sections 1–3](getting-started.md) for native desktop/SSH
prerequisites, a non-root sudo account, and host-key verification. Create your own
`inventory/target.local.ini` with exactly the intended VM:

```ini
[qubix_targets]
qubix-vm ansible_host=192.168.64.10 ansible_user=YOUR_VM_USER ansible_port=22
```

Always pass this inventory: the repository's fallback inventory selects localhost.
Store overrides in `config/local.yml`; never put passwords in inventory or commit
local files. Full defaults require each preparation step below:

| Requirement | Procedure |
|---|---|
| Native Noctalia/Niri companions and SSH | [Target setup](getting-started.md#1-prepare-your-controller-and-vm) |
| Paru, Homebrew, WezTerm; dependency-safe Alacritty/Foot removal | Preview then run `playbooks/prepare-packages.yml` against the inventory, with sudo prompting |
| Pinned 210-face Monaspace NF source | `.venv/bin/ansible-playbook playbooks/prepare-fonts.yml` on the controller |
| Noctalia Greeter packages and existing greetd launcher | [Login preparation/cutover](login.md); `playbooks/prepare-login.yml` does not switch the active manager |
| Exact supported caption/compact builds, GJS/GTK/fprintd | `playbooks/prepare-ui.yml`; follow the [login guide](login.md) for version/native checks |
| KWallet packages and reviewed existing-secret migration | `playbooks/prepare-keyring.yml` and the [keyring guide](keyring.md) |
| Active bootloader and generator/image mappings | [Boot examples](getting-started.md#6-test-the-existing-bootloader) and [Plymouth guide](plymouth.md); confirm measured paths, kernels and active loader |

Remote preparation playbooks use `.venv/bin/ansible-playbook -i
inventory/target.local.ini -e @config/local.yml playbooks/prepare-NAME.yml
--ask-become-pass` (one shell command). Review each guide before running it.
Package transactions may invoke native snapshot/boot hooks and are outside file
restoration. `deploy` never invokes preparation, migrates secrets or switches managers.

For a first desktop-only trial, copy the complete explicit opt-out configuration in
[getting started, section 3](getting-started.md#3-preview-and-deploy-the-desktop).
It disables login, keyring, fingerprint/private presentation and boot work pending
preparation; these are deliberate overrides of the shipped defaults.

## Enabled by default

The authoritative [28-input defaults reference](../architecture/configuration.md#every-effective-default)
is checked against `config/defaults.yml` plus `config/profiles/cachyos-niri.yml`.
With no overrides, every implemented component is selected:

| Enabled selection | Included behavior |
|---|---|
| Fonts + Krypton UI | All 210 official Monaspace NF faces; Fontconfig/GTK/Qubix UI preferences |
| Branding | Attributed original-colour cube/logo, wallpaper and shared palette |
| Qubix Niri/Noctalia | Separate session, bar/launcher/notifications, 100% output scale, shortcuts and guarded power menu |
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
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --tags installed --ask-become-pass
```

Add `--ask-pass` for password SSH. For private boot metadata, set the YAML boolean
`qubix_discovery_privileged: true` outside `qubix` as shown in the getting-started
example; this permits read-only privileged probes and confirms no boot selection.
Use YAML component selections; the wrapper rejects deploy/restore tags.

Check mode is an approximation and cannot validate files it has not installed.
Deployment backs up named resources, installs and validates files, then records
revision/configuration receipts. A failure may leave earlier resources installed;
inspect pending diagnostics and use [restoration](restoration.md). Concurrent
package updates/deployments are unsupported.

Repeat the same deployment to check idempotency. When convenient, log out and select
**Qubix Niri**, preserving native Niri as fallback. No manager restart/current-session
switch happens during deployment. Check the terminal, launcher, shortcuts, lock and
login separately using the [verification checklist](verification.md). File receipts
never assert graphical/boot success. Only reboot an authorized test VM after reviewing
its boot mappings and recovery plan; test each loader/generator combination separately.

## Recover

Review [restoration and its limits](restoration.md), then preview:

```bash
./bootstrap.sh restore -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh restore -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
```

Restoration uses protected first baselines, not whole-system rollback. Packages and
secret migration are separate. Recover WezTerm account files using their timestamped
home-file backups; generic system restoration does not reverse these copies. Keep the
VM snapshot for boot failures. Report commit, sanitized configuration, file/parser
results, session observations and boot observations separately.
