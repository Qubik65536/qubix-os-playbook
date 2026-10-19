# Get started as a user

Qubix customizes an existing **CachyOS Niri** installation. Run the playbook
**directly on the machine you want to customize**, signed in as your normal desktop
user with sudo access. That machine runs Ansible and receives the customization.
Do not run the whole playbook as root. User deployment requires no SSH service,
remote controller or remote inventory.

Status: **MVP candidate**. Read [features](../features.md) and
[current evidence and limitations](../project/status.md) before applying it.
Boot work uses an explicitly authorized disposable VM with a snapshot and console
access. A successful file deployment does not establish login or boot acceptance.

1. [Install prerequisites](installation.md) on the CachyOS Niri machine and download
   the playbook package there.
2. [Deploy locally](deployment.md): prepare packages and assets, review configuration,
   inspect, preview, deploy and verify using `inventory/local.ini`.
3. [Use the desktop](desktop.md): choose Qubix Niri and learn the shortcuts, output
   scaling, terminal and power controls.
4. Follow the component guides when preparing [login](login.md),
   [KWallet](keyring.md), [fingerprints](fingerprint.md), the
   [bootloader](bootloader.md) and [Plymouth](plymouth.md).
5. Keep [verification](verification.md), [recovery](restoration.md) and
   [local diagnostics](collecting-target-info.md) available.

The full profile selects every implemented component. Missing prerequisites stop
preflight; deployment does not silently omit them or automatically run preparation.
The [deployment guide's defaults summary](deployment.md#enabled-by-default) links to
all effective values. Use its explicit desktop-only trial overrides if preparing in stages.

Developers changing the playbook or testing through SSH should start with
[developer onboarding](../development/getting-started.md) and
[SSH VM testing](../development/ssh-testing.md).
