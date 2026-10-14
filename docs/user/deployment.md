# Deployment

Status: **Implemented preflight only**. No customization resources are installed by this revision.

From the repository root after [controller setup](../development/environment.md):

```bash
./bootstrap.sh verify
./bootstrap.sh deploy --check --diff
./bootstrap.sh deploy
```

Use `-i inventory.ini` for a remote `qubix_targets` group and `-e @config/local.yml` for overrides. Both playbooks validate the schema and measured host compatibility. `deploy` explicitly reports inspection-only status. Enabled Planned components fail, and unsupported targets are rejected.

No privilege escalation is used. Read-only package, version and systemd probes run even in check mode. Temporary Ansible module transport/cache files are used; target configuration is not modified. Check/diff is an approximation, not a complete transaction plan.

The eventual [lifecycle](../architecture/deployment.md) includes backup, component deployment, verification and revision state. A desktop milestone does not depend on boot work. No bootstrap procedure rebuilds initramfs or activates boot themes.
