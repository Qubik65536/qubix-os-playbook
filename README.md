# Qubix OS Playbook

An Ansible framework for deploying Qubix branding and desktop defaults onto existing Linux installations. The first target is **CachyOS with Niri**. Qubix reproduces its managed configuration, not the complete operating system.

**Status: MVP candidate ready for disposable-VM testing.** Branding, a separate Qubix Niri session, Noctalia shell/wallpaper, rounded #56728b appearance, shell defaults, SDDM branding, both GRUB and Limine, and Plymouth with both dracut and mkinitcpio are implemented. Static checks and isolated fixtures pass. The first desktop candidate's installation, syntax, preservation, zero-change reapplication, restoration and nested rendering pass. The Noctalia redesign passes native parser and isolated rendering/preservation checks; primary-session startup now passes on the authorized target. Main-session interaction, authentication, native image generation and recovery remain acceptance gates. See [actual evidence](docs/project/status.md).

Get started:

- [User getting-started guide](docs/user/getting-started.md): prepare the target, deploy and test the desktop, then opt into login/boot/splash tests.
- [Human developer getting-started guide](docs/development/getting-started.md): set up tools, understand the code and run fixtures.
- [SSH access and target information](docs/user/collecting-target-info.md): share connection details so the agent can inspect your test machine.
- [Boot and poweroff splash guide](docs/user/plymouth.md): preview native-style spinner branding, review image mappings and plan activation/recovery.

After controller setup, a remote inventory with a `qubix_targets` group and the guide’s `config/local.yml`:

```bash
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --tags installed --ask-become-pass
```

Add --ask-pass with password SSH. The guide includes explicit read privilege for private /boot metadata. The default profile deploys the desktop only. Choose **Qubix Niri** at login or start it from a free TTY. Native Niri, personal dotfiles, distribution identity, boot entries and kernel arguments remain preserved. Login/boot/splash are opt-in; explicit boot paths/version/image mappings are required. Candidate commits are local and have not been pushed.

## Regenerate the shortcut cheatsheet

1. Edit `roles/qubix_niri/templates/config.kdl.j2` in this checkout. Give each binding a `hotkey-overlay-title="Category / Action"` immediately after its key combination, on the same line. Use **Applications**, **Windows**, **Navigation**, **Session** or **Media** as the category. Bindings with the same category/action are grouped as alternative keys.

   ```kdl
   Mod+T hotkey-overlay-title="Applications / Terminal" { spawn "/usr/bin/foot" "--config=/etc/qubix/foot.ini"; }
   ```

2. Check the generated list with the desktop fixture:

   ```bash
   .venv/bin/ansible-playbook tests/playbooks/desktop.yml
   ```

3. Deploy using the inventory and configuration from your normal desktop deployment:

   ```bash
   ./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
   ```

   Add `--ask-pass` for password SSH. Keep `niri.enabled: true`; use your existing component selections. Deployment regenerates `/usr/share/qubix/noctalia/plugins/shortcuts/bindings.json` from the managed KDL and installs both together.

4. Close and reopen the panel with **Super+Shift+/** or its bar button. It reads the regenerated list each time it opens.

Regeneration happens during deployment. Personal configuration changes and application-specific shortcuts are outside this generated list. The [user guide](docs/user/getting-started.md) covers deployment/verification, and the [developer guide](docs/development/getting-started.md) covers native parser and rendering tests.

## Project documentation

- [Scope and acceptance](docs/project/scope.md), [roadmap](docs/project/roadmap.md), [backlog](docs/project/backlog.md)
- [Architecture](docs/architecture/overview.md), [configuration](docs/architecture/configuration.md), [candidate boundaries](docs/architecture/mvp-candidate.md)
- [Desktop appearance and shortcuts](docs/architecture/desktop-design.md)
- [Native desktop test results](docs/project/desktop-test-results.md)
- [Verification checklist](docs/user/verification.md), [restoration](docs/user/restoration.md), [troubleshooting](docs/user/troubleshooting.md)
- [Contributing](CONTRIBUTING.md), [agent instructions](AGENTS.md), [testing](docs/development/testing.md)

MVP acceptance requires both loaders and both generators to pass independent VM tests; the first working desktop milestone does not depend on boot customization. Fedora Workstation and KDE are post-MVP.

Visual identity originates in [Qubix OS BlueBuild](https://github.com/Qubik65536/qubix-os-bluebuild). Imported artwork retains [attribution](NOTICE), [checksums](assets/branding/manifest.yml), and Apache-2.0 notices. Image-generation infrastructure is not reused. See [reference review](docs/architecture/reference.md).
