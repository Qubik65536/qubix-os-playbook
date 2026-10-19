# Regenerate the shortcut cheatsheet

1. Edit `roles/qubix_niri/templates/config.kdl.j2` in this checkout. Give each binding a `hotkey-overlay-title="Category / Action"` immediately after its key combination, on the same line. Use **Applications**, **Windows**, **Navigation**, **Session** or **Media** as the category. Bindings with the same category/action are grouped as alternative keys.

   ```kdl
   Mod+T hotkey-overlay-title="Applications / Terminal" { spawn "/usr/share/qubix/bin/qubix-wezterm" "start"; }
   ```

2. Check the generated list with the desktop fixture:

   ```bash
   .venv/bin/ansible-playbook tests/playbooks/desktop.yml
   ```

3. Deploy using the inventory and configuration for the explicitly selected developer test VM:

   ```bash
   ./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
   ```

   Add `--ask-pass` for password SSH. Keep `niri.enabled: true`; use your existing component selections. Deployment regenerates `/usr/share/qubix/noctalia/plugins/shortcuts/bindings.json` from the managed KDL and installs both together.

4. Close and reopen the panel with **Super+Shift+/** or its bar button. It reads the regenerated list each time it opens.

Regeneration happens during deployment. Personal configuration changes and application-specific shortcuts are outside this generated list. The [user guide](../user/getting-started.md) covers deployment/verification, and the [developer guide](getting-started.md) covers native parser and rendering tests.
