# Deployment

Status: **Implemented additive artwork deployment; fixture-tested**. Live CachyOS deployment remains unverified. No desktop, login, bootloader or splash activation is performed.

From the root after [controller setup](../development/environment.md), inspect without escalation:

```bash
./bootstrap.sh verify
```

Preview and deploy to a supported CachyOS Niri target (local commands shown):

```bash
./bootstrap.sh deploy --check --diff --ask-become-pass
./bootstrap.sh deploy --ask-become-pass
./bootstrap.sh verify --tags branding
```

Add `-i inventory.ini` for remote `qubix_targets` and `-e @config/local.yml` for overrides. `--ask-become-pass` requests the target's privilege-escalation password; omit it only if escalation is already configured. The wrapper never installs dependencies. Real deployment is an operator action; bootstrap validation runs only disposable fixtures.

Schema and supported-host preflight run unprivileged with `always` tags. Only the selected branding installation block uses escalation. It copies five named Managed files and verifies bytes/modes/ownership. Standalone verification is read-only. Enabling any other component fails before writes. Disabling branding yields preflight only. Use `--tags branding` to select branding; never skip `always` preflight.

Read-only package/version/systemd probes run in check mode. On a fresh namespace, directory changes are previewed, file-copy preview is deferred until the directory exists, and proposed filenames are reported. Post-install verification is skipped during preview; no appearance success is claimed. Check/diff is an approximation, not a complete transaction plan.

The eventual [lifecycle](../architecture/deployment.md) includes backups and revision state, which remain Planned. Artwork availability is not graphical activation. The desktop milestone remains independent of boot work.
