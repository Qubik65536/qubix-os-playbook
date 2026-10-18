# Desktop secret storage

Status: Implemented; native unlock, migration/API and file/recovery tests pass; real login pending. Focused task: opt into KDE KWallet on CachyOS Niri/greetd,
replacing GNOME Keyring as the Secret Service provider without deleting stored secrets.

## Contract and acceptance

`qubix.keyring.enabled: true` explicitly authorizes optional KWallet hooks in the
existing greetd PAM file. All other authentication rules remain byte-preserved;
unsupported managers, redirected files, unknown keyring hooks and missing native
prerequisites fail before deployment writes. Disabled (the default) preserves PAM.
Use the separate package preparation playbook before deployment; bootstrap never installs
packages. Require the measured split KWallet implementation (`ksecretd`, `kwalletd6`,
`pam_kwallet5.so`, `pam_kwallet_init`). Password login unlocks a password-matched,
Blowfish `kdewallet`; fingerprint/autologin cannot supply a decryption password.

Manage system defaults and additive provider selection through the shared first-baseline
resource engine. Preserve personal configuration and encrypted GNOME/KDE stores. Never
export secrets to plaintext files or logs. Existing secrets require a separately tested
migration before live provider replacement. Retain GNOME Keyring when required by another
installed package; never bypass package dependency checks or remove the desktop metapackage.

Acceptance: schema rejection, supported/unsupported PAM fixtures, check mode,
installation, installed verification, unchanged reapplication and recovery checks.
On the target test isolated native KWallet unlock and Secret Service store/read/delete,
then migration with values compared in memory and old encrypted files retained. Verify
KDE API access and live provider ownership separately. A real password logout/login remains
an operator gate; never restart the display manager or terminate the desktop for testing.

## Managed interfaces

Preparation installs `kwallet`, `kwallet-pam` and `kwalletmanager` using native Pacman,
without repository refresh, system upgrade or display-manager changes. Package hooks may
create Snapper snapshots. Deployment requires the split KWallet binaries and uses:

- `/etc/pam.d/greetd`: optional `pam_kwallet5.so` authentication capture after
  `system-local-login`, plus optional session `auto_start force_run kwalletd=/usr/bin/ksecretd`.
  `force_run` avoids relying on a graphical environment before greetd starts the desktop.
- `/usr/local/share/dbus-1/services/org.freedesktop.secrets.service`: higher-priority
  system provider default pointing at `ksecretd`; distribution service files stay intact.
- `/etc/xdg/autostart/qubix-kwallet-pam.desktop`: the native `pam_kwallet_init`
  environment handshake for Niri; no password is stored in the desktop file or environment.
- Backed-up GNOME secrets/PKCS11 autostart defaults with `Hidden=true`, and service/socket
  condition drop-ins requiring absent `/etc/qubix/allow-gnome-keyring`. An existing marker
  refuses activation. Personal autostart/D-Bus/systemd overrides retain precedence and must
  be reviewed during actual session acceptance.

Deployment never stops an existing provider: live migration is a separate operator operation.
Native `ksecretd` uses the login-derived password hash for a new encrypted Blowfish `kdewallet`;
existing KDE wallets require their own password compatibility check. KDE application access
is through `kwalletd6`, which proxies the Secret Service. This implementation does not manage
SSH agents, account passwords, fingerprint policy, personal wallet settings or PKCS11 keys.
Disabling the component preserves installed resources; use explicit restoration to reverse it.
The shared recovery engine admits only the recorded keyring `/etc/pam.d/greetd` exception;
all other PAM paths remain refused. Recovery does not migrate newly created KDE secrets back.

Sources: [KWallet architecture](https://github.com/KDE/kwallet/blob/v6.31.0/README.md),
[native PAM integration](https://github.com/KDE/kwallet-pam/blob/master/pam_kwallet.c)
and [native environment handshake](https://github.com/KDE/kwallet-pam/blob/master/pam_kwallet_init).

Niri startup additionally runs native `/usr/lib/pam_kwallet_init` directly through
`spawn-at-startup`, because the measured target launches Niri without an active systemd
XDG autostart target. Full Niri deployment always renders a guarded native hook: it is a no-op when the native
helper is absent or PAM has no wallet socket. This preserves unlocking across later
Niri-only deployments even if the keyring component is not selected. A keyring-only
deployment adds/removes only that exact line in an existing Qubix-owned configuration,
retaining its Niri component baseline and parser validation. Personal Niri files are never
edited. The desktop entry remains available to sessions using systemd XDG autostart.
