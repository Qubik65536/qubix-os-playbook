# Qubix OS Playbook

An Ansible framework for deploying Qubix branding and desktop defaults onto existing Linux installations. The first target is **CachyOS with Niri**. Qubix reproduces its managed configuration, not the complete operating system.

**Status: MVP candidate ready for testing.** Monaspace NF/Krypton defaults, branding, Qubix Niri/Noctalia, shell defaults,
SDDM branding, Noctalia Greeter appearance preparation, both GRUB and Limine, and Plymouth with dracut/mkinitcpio are implemented.
The CachyOS desktop starts at 100% scale; the corrected Limine/native-style Plymouth deployment
and exact boot-image checks pass on the authorized target. Identical-source reapplication passes
with zero changes, and a normal-kernel reboot returns the desktop. The operator confirmed earlier
Limine, startup and reboot branding. The higher-contrast, caption-free update is deployed with smaller
Krypton menu text and the desktop cube wallpaper. Plymouth now keeps the original-colour cube and
adds a scaled desktop-cube background; renewed console acceptance is pending.
Independent loader/generator, authentication and current boot
recovery tests remain acceptance gates. See [actual evidence](docs/project/status.md).

## For users

Start with the [user guide](docs/user/getting-started.md). Run the playbook directly
on the CachyOS Niri machine you want to customize, as your normal desktop account.
The [deployment guide](docs/user/deployment.md) covers downloads, local preparation,
all enabled features and recovery. SSH is reserved for developer testing.

After local setup/preparation and saving the guide's `config/local.yml`:

```bash
./bootstrap.sh verify -i inventory/local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh deploy -i inventory/local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh verify -i inventory/local.ini -e @config/local.yml --tags installed --ask-become-pass
```

The default profile enables fonts/Krypton, branding, Niri/Noctalia/WezTerm, shell,
fingerprint setup, private captions, compact greetd login, KWallet, bootloader
appearance and Plymouth. Packages/builds, existing-manager preparation, reviewed secrets
and explicit boot paths/mappings/confirmations remain prerequisites. The guide includes
deliberate desktop-only opt-outs; see the [complete defaults](docs/architecture/configuration.md).

- [Features](docs/features.md) and [desktop use](docs/user/desktop.md)
- [Login](docs/user/login.md), [fingerprints](docs/user/fingerprint.md) and [KWallet](docs/user/keyring.md)
- [Bootloader](docs/user/bootloader.md), [Plymouth](docs/user/plymouth.md) and [recovery](docs/user/restoration.md)

## For developers

Start with [developer onboarding](docs/development/getting-started.md) for source,
tools, fixtures and contribution rules. Use [SSH VM testing](docs/development/ssh-testing.md)
and [SSH access/evidence collection](docs/development/ssh-access.md) for remote tests.
[Packaging and manual releases](docs/development/releases.md) covers validated artifacts
and manually triggered candidate publication.

## Regenerate the shortcut cheatsheet

Binding edits and regeneration are developer work; follow the
[shortcut development guide](docs/development/shortcuts.md).

## Project documentation

- [Scope and acceptance](docs/project/scope.md), [roadmap](docs/project/roadmap.md), [backlog](docs/project/backlog.md)
- [Architecture](docs/architecture/overview.md), [configuration](docs/architecture/configuration.md), [candidate boundaries](docs/architecture/mvp-candidate.md)
- [Desktop appearance and shortcuts](docs/architecture/desktop-design.md)
- [Native desktop test results](docs/project/desktop-test-results.md)
- [Verification checklist](docs/user/verification.md), [restoration](docs/user/restoration.md), [troubleshooting](docs/user/troubleshooting.md)
- [Contributing](CONTRIBUTING.md), [agent instructions](AGENTS.md), [testing](docs/development/testing.md)

MVP acceptance requires both loaders and both generators to pass independent VM tests; the first working desktop milestone does not depend on boot customization. Fedora Workstation and KDE are post-MVP.

Visual identity originates in [Qubix OS BlueBuild](https://github.com/Qubik65536/qubix-os-bluebuild). Imported artwork retains [attribution](NOTICE), [checksums](assets/branding/manifest.yml), and Apache-2.0 notices. Image-generation infrastructure is not reused. See [reference review](docs/architecture/reference.md).
