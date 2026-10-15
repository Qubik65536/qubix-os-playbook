# Qubix OS Playbook

An Ansible framework for deploying Qubix branding and desktop defaults onto existing Linux installations. The first target is **CachyOS with Niri**. Qubix reproduces its managed configuration, not the complete operating system.

**Status: MVP candidate ready for disposable-VM testing.** Branding, a separate Qubix Niri session, Noctalia shell/wallpaper, rounded #56728b appearance, shell defaults, SDDM branding, both GRUB and Limine, and Plymouth with both dracut and mkinitcpio are implemented. Static checks and isolated fixtures pass. The first desktop candidate's installation, syntax, preservation, zero-change reapplication, restoration and nested rendering pass. The Noctalia redesign passes native parser and isolated rendering/preservation checks; its primary-session migration is tracked separately. Main-session, authentication, native image generation and reboot recovery remain VM acceptance gates. See [actual evidence](docs/project/status.md).

Get started:

- [User getting-started guide](docs/user/getting-started.md): prepare the target, deploy and test the desktop, then opt into login/boot/splash tests.
- [Human developer getting-started guide](docs/development/getting-started.md): set up tools, understand the code and run fixtures.
- [SSH access and target information](docs/user/collecting-target-info.md): share connection details so the agent can inspect your test machine.

After controller setup, a remote inventory with a `qubix_targets` group and the guide’s `config/local.yml`:

```bash
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --tags installed --ask-become-pass
```

Add --ask-pass with password SSH. The guide includes explicit read privilege for private /boot metadata. The default profile deploys the desktop only. Choose **Qubix Niri** at login or start it from a free TTY. Native Niri, personal dotfiles, distribution identity, boot entries and kernel arguments remain preserved. Login/boot/splash are opt-in; explicit boot paths/version/image mappings are required. Candidate commits are local and have not been pushed.

- [Scope and acceptance](docs/project/scope.md), [roadmap](docs/project/roadmap.md), [backlog](docs/project/backlog.md)
- [Architecture](docs/architecture/overview.md), [configuration](docs/architecture/configuration.md), [candidate boundaries](docs/architecture/mvp-candidate.md)
- [Desktop appearance and shortcuts](docs/architecture/desktop-design.md)
- [Native desktop test results](docs/project/desktop-test-results.md)
- [Verification checklist](docs/user/verification.md), [restoration](docs/user/restoration.md), [troubleshooting](docs/user/troubleshooting.md)
- [Contributing](CONTRIBUTING.md), [agent instructions](AGENTS.md), [testing](docs/development/testing.md)

MVP acceptance requires both loaders and both generators to pass independent VM tests; the first working desktop milestone does not depend on boot customization. Fedora Workstation and KDE are post-MVP.

Visual identity originates in [Qubix OS BlueBuild](https://github.com/Qubik65536/qubix-os-bluebuild). Imported artwork retains [attribution](NOTICE), [checksums](assets/branding/manifest.yml), and Apache-2.0 notices. Image-generation infrastructure is not reused. See [reference review](docs/architecture/reference.md).
