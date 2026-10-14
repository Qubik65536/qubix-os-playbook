# Qubix OS Playbook

An Ansible framework for deploying Qubix branding and desktop defaults onto existing Linux installations. The first target is **CachyOS with Niri**. Qubix reproduces its managed configuration, not the complete operating system.

**Status: MVP candidate ready for disposable-VM testing.** Branding, a separate Qubix Niri session, wallpaper/companions, shell defaults, SDDM branding, both GRUB and Limine, and Plymouth with both dracut and mkinitcpio are implemented. Static checks and isolated fixtures pass. Native sessions, authentication, image generation, reboots and recovery remain unverified until the VM matrix passes. See [actual evidence](docs/project/status.md).

Start with the [user getting-started guide](docs/user/getting-started.md). Use the [human developer getting-started guide](docs/development/getting-started.md) to understand or change the code. The [target information guide](docs/user/collecting-target-info.md) explains what to collect when the VM finishes installing.

After controller setup and a remote inventory with a `qubix_targets` group:

```bash
./bootstrap.sh verify -i inventory/target.local.ini
./bootstrap.sh deploy -i inventory/target.local.ini --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini --tags installed
```

The default profile deploys the desktop only. Choose **Qubix Niri** at login or start it from a free TTY. Native Niri, personal dotfiles, distribution identity, boot entries and kernel arguments remain preserved. Login/boot/splash are opt-in; explicit boot paths/version/image mappings are required. Candidate commits are local and have not been pushed.

- [Scope and acceptance](docs/project/scope.md), [roadmap](docs/project/roadmap.md), [backlog](docs/project/backlog.md)
- [Architecture](docs/architecture/overview.md), [configuration](docs/architecture/configuration.md), [candidate boundaries](docs/architecture/mvp-candidate.md)
- [Verification checklist](docs/user/verification.md), [restoration](docs/user/restoration.md), [troubleshooting](docs/user/troubleshooting.md)
- [Contributing](CONTRIBUTING.md), [agent instructions](AGENTS.md), [testing](docs/development/testing.md)

MVP acceptance requires both loaders and both generators to pass independent VM tests; the first working desktop milestone does not depend on boot customization. Fedora Workstation and KDE are post-MVP.

Visual identity originates in [Qubix OS BlueBuild](https://github.com/Qubik65536/qubix-os-bluebuild). Imported artwork retains [attribution](NOTICE), [checksums](assets/branding/manifest.yml), and Apache-2.0 notices. Image-generation infrastructure is not reused. See [reference review](docs/architecture/reference.md).
