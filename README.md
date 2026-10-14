# Qubix OS Playbook

An Ansible framework for deploying Qubix branding and desktop defaults onto existing Linux installations. The first target is **CachyOS with Niri**. Qubix manages its own configuration, not the complete operating system.

**Status: bootstrap foundation with additive branding.** Strict profile validation, read-only CachyOS Niri discovery, and shared artwork installation are implemented and fixture-tested. No graphical or boot integration has been verified. Follow [project status](docs/project/status.md) for evidence.

Set up [controller tools](docs/development/environment.md), then run from the repository root:

```bash
./bootstrap.sh verify
./bootstrap.sh deploy --check --diff --ask-become-pass
```

These commands inspect an existing CachyOS Niri host and reject unsupported systems. Deployment installs five named artwork/license files under `/usr/share/qubix/branding/` after preflight; `--check` previews without installing. Other desktop and boot components remain Planned. Use `-i inventory.ini` for a remote `qubix_targets` group and `-e @config/local.yml` for overrides. See [installation](docs/user/installation.md).

The MVP includes a working Niri desktop, login branding, **both GRUB and Limine adapters**, and Plymouth with both dracut and mkinitcpio. Boot work remains opt-in and follows the first desktop milestone. Fedora Workstation and KDE are post-MVP.

- [Scope and acceptance criteria](docs/project/scope.md)
- [Architecture](docs/architecture/overview.md) and [configuration contract](docs/architecture/configuration.md)
- [Roadmap](docs/project/roadmap.md) and [backlog](docs/project/backlog.md)
- [Installation](docs/user/installation.md), [deployment](docs/user/deployment.md), and [recovery](docs/user/restoration.md)
- [Contributing](CONTRIBUTING.md) and [agent instructions](AGENTS.md)

Visual identity originates in [Qubix OS BlueBuild](https://github.com/Qubik65536/qubix-os-bluebuild). Imported artwork retains [attribution](NOTICE), [checksums](assets/branding/manifest.yml), and Apache-2.0 notices. This project does not reuse its image-generation infrastructure or overwrite distribution identity. See [reference review](docs/architecture/reference.md).
