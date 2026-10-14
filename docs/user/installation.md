# Installation

The controller tooling, inspection workflow, and additive artwork deployment are **Implemented**. A live CachyOS target has not yet been integration-tested. Use an existing CachyOS Niri installation; this project does not install Linux or build an ISO.

Clone the repository, enter its root, and follow [controller setup](../development/environment.md). The default inventory selects localhost. The target needs Python, Linux/systemd, exact CachyOS identity, and executable `/usr/bin/pacman` and `/usr/bin/niri`. No package installation is automatic. Artwork deployment needs target privilege escalation; inspection does not.

For a remote target, create an operator-owned inventory (example; replace the hostname):

```ini
[qubix_targets]
qubix-vm ansible_host=192.0.2.10 ansible_user=operator
```

Then run `./bootstrap.sh verify -i inventory.ini`. Use normal SSH authentication and host-key verification. Do not add `--become` for inspection; the playbooks explicitly disable escalation in preflight. The macOS development host is intentionally unsupported as a target.

Read [configuration](configuration.md), [deployment](deployment.md), and [restoration](restoration.md) before later mutation. Bootloader/Plymouth remain disabled and unimplemented.
