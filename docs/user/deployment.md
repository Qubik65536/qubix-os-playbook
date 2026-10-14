# Deployment

Status: Implemented desktop candidate. File engine recovery is fixture-tested; actual Niri parsing/session verification requires the installing CachyOS VM.

After controller setup and target prerequisites, use:

```bash
./bootstrap.sh verify
./bootstrap.sh deploy --check --diff --ask-become-pass
./bootstrap.sh deploy --ask-become-pass
./bootstrap.sh verify --tags installed
```

Add `-i inventory.ini` and `-e @config/local.yml` as appropriate. The profile enables branding, Qubix Niri and shell defaults; login/boot/Plymouth remain disabled until selected and validated. Missing companion binaries fail before deployment writes. Configuration is the component selection interface: deployment/restore tags are rejected by the wrapper, avoiding accidental skipped checks or activation. Verification tags remain supported.

Deployment builds all enabled component definitions first, then installs named files with protected first-baseline backups, atomic file validation, checksum verification and receipts. Source revision, dirty state and effective configuration digest are recorded only after verification. A failed file validation may leave earlier inert resources installed; use recorded baselines for recovery. Concurrent deployments are unsupported.

Qubix installs an additional session rather than replacing native Niri or personal configuration. Choose **Qubix Niri** at login to test it. No display-manager restart or current-session change occurs during deployment. Shell defaults do not change the login shell.

Check mode does not write backups/receipts or claim installed content. If a parent is absent, copy preview is deferred and proposed resources are listed. It is an approximation, not a transaction plan. See [Niri](../components/niri.md) and [restoration](restoration.md).
