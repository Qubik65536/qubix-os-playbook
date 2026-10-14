# Deployment

Status: **Planned procedure**. No deployment commands are operational yet.

The intended order is inspect, validate profile/capabilities, preview, prepare needed backups, deploy selected components, verify, then record state. See [lifecycle](../architecture/deployment.md). A desktop deployment must not depend on boot work.

Ansible check/diff will be supported where practical; it is not a complete transaction plan. Read-only probes may run in check mode. Do not interpret skipped writes as installed resources or successful graphical integration.

Use a disposable CachyOS Niri VM first. Any later privileged deployment is an explicit operator action. No procedure in bootstrap should rebuild the development host's initramfs or activate boot themes.
