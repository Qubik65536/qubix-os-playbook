# Installation prerequisites

Status: Implemented candidate; native integration pending.

Follow the [user getting-started guide](getting-started.md). Use existing CachyOS Niri; the project installs neither Linux nor an ISO. A Mac/Linux controller needs Python 3.12+ and locked tools. The target needs Python, exact CachyOS identity, Linux/systemd, Pacman and Niri.

Ansible transfers repository assets over SSH. Use the existing checkout: unpublished candidate commits are not in a GitHub clone. Default inventory selects localhost; always provide your VM inventory from a Mac. Keep host-key checking enabled.

Prepare Foot/Fuzzel/Waybar/Mako/Swaybg manually. Deployment does not install packages, replace managers/loaders or change the default shell. See [compatibility](../architecture/compatibility.md) for optional prerequisites.

Inspect with `./bootstrap.sh verify -i inventory/target.local.ini`. Default inspection uses ordinary readable facts without escalation. Installed boot/splash checks may need sudo. Read [configuration](configuration.md), [deployment](deployment.md) and [recovery](restoration.md).
