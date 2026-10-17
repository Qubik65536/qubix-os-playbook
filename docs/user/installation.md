# Installation prerequisites

Status: Implemented candidate; native desktop procedure Tested; main-session and boot acceptance pending.

Follow the [user getting-started guide](getting-started.md). Use existing CachyOS Niri; the project installs neither Linux nor an ISO. A Mac/Linux controller needs Python 3.12+ and locked tools. The target needs Python, exact CachyOS identity, Linux/systemd, Pacman and Niri.

Ansible transfers repository assets over SSH. Use the existing checkout: unpublished candidate commits are not in a GitHub clone. Default inventory selects localhost; always provide your VM inventory from a Mac. Keep host-key checking enabled.

Prepare standalone Noctalia >=5.2.0 and <6.0.0, Foot, jq and optional Starship manually; preview the transaction and account for native Snapper/Limine hooks. Deployment does not install packages, replace managers/loaders or change the default shell. See [compatibility](../architecture/compatibility.md) for optional prerequisites.

Inspect with `./bootstrap.sh verify -i inventory/target.local.ini`. Default inspection uses ordinary readable facts without escalation. Installed boot/splash checks may need sudo. Read [configuration](configuration.md), [deployment](deployment.md) and [recovery](restoration.md).

## Font source preparation

Before the first deployment with fonts enabled, prepare the official pinned source
on the controller (approximately 315 MiB download, 476 MiB extracted):

```bash
.venv/bin/ansible-playbook playbooks/prepare-fonts.yml
```

This separate step only downloads/extracts controller cache files. Normal verify/deploy
uses the prepared cache without downloads and fails if it is absent or damaged.
No font-building tools or extra Python application are installed on the target.
See the [font contract](../components/fonts.md) for installation/selection options.
