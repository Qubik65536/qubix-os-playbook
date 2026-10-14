# Deployment

Status: Implemented MVP candidate. Native desktop installation, syntax, zero-change reapplication, absence recovery and nested rendering pass; primary-session/login/boot acceptance remains pending. See [actual results](../project/desktop-test-results.md).

After controller setup and target prerequisites, use:

```bash
./bootstrap.sh verify
./bootstrap.sh deploy --check --diff --ask-become-pass
./bootstrap.sh deploy --ask-become-pass
./bootstrap.sh verify --tags installed
```

Add `-i inventory.ini` and `-e @config/local.yml` as appropriate. Private /boot requires the explicit typed discovery privilege override and sudo prompting; password SSH also needs --ask-pass. The [operator guide](getting-started.md) provides the tested remote procedure. The profile enables branding, Qubix Niri and shell defaults; login/boot/Plymouth remain disabled until selected and validated. Missing companion binaries fail before deployment writes. Configuration is the component selection interface: deployment/restore tags are rejected by the wrapper, avoiding accidental skipped checks or activation. Verification tags remain supported.

Deployment builds all enabled component definitions first, then installs named files with protected first-baseline backups, atomic file validation, checksum verification and receipts. Source revision, dirty state and effective configuration digest are recorded only after verification. A failed validation/rebuild may leave earlier resources installed; pending diagnostics coexist with last-success state. Use baselines or the VM snapshot for recovery. Concurrent deployments are unsupported.

Qubix installs an additional session rather than replacing native Niri or personal configuration. Choose **Qubix Niri** at login to test it. No display-manager restart or current-session change occurs during deployment. Shell defaults do not change the login shell.

Check mode does not write backups/receipts or claim installed content. If a parent is absent, copy preview is deferred and proposed resources are listed. It is an approximation, not a transaction plan. See [Niri](../components/niri.md) and [restoration](restoration.md).

The [getting-started guide](getting-started.md) provides remote examples and explicit SDDM/GRUB/Limine/dracut/mkinitcpio opt-ins. Native generation runs only on configured targets; no disk/loader installer or entry regeneration runs. Installed boot/splash checks may need --ask-become-pass for private resources.
