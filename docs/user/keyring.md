# KWallet on Qubix Niri

The shipped CachyOS Niri profile selects KWallet with `qubix.keyring.enabled: true`. It provides the
Secret Service for libsecret applications and the KDE Wallet API for KDE software.
Only existing greetd on CachyOS Niri is supported. Login appearance can stay disabled.
See the [component contract](../components/keyring.md) and [test evidence](../project/keyring-test-results.md).

## Preparation and deployment

Install native prerequisites separately, using the normal [local setup](installation.md):

```bash
ANSIBLE_HOME="$PWD/.cache/ansible" .venv/bin/ansible-playbook playbooks/prepare-keyring.yml \
  -i inventory/local.ini --check --ask-become-pass
```

Review the transaction, then remove `--check`. Native package hooks can create snapshots.
Keep `gnome-keyring` installed if `pacman -Qi gnome-keyring` lists a required dependent;
never force removal or remove a desktop metapackage simply to replace secret storage.

Existing GNOME secrets must be migrated before selecting the replacement provider. Keep the
encrypted originals under `~/.local/share/keyrings/` and any existing KDE stores. Do not
export plaintext passwords or replace stores with empty files. The measured target's three
entries were transferred and compared in memory; this playbook does not automate migrations
for other accounts or assume their wallet passwords. An existing nonempty/locked wallet or
multiple collections needs individual review. PKCS11 keys and SSH-agent functions are separate.

Add this to the existing deployment overrides:

```yaml
qubix:
  keyring:
    enabled: true
```

Run normal `deploy --check --diff`, `deploy` and `verify --tags installed` with that override.
The option explicitly authorizes the bounded greetd PAM changes described in the contract;
other authentication rules remain unchanged and original defaults are backed up.
No provider, display manager or graphical session is restarted by deployment.
Save work, log out and log in with the account password to activate and verify login unlocking.
The encrypted `kdewallet` password must match the account password; fingerprint or autologin
cannot decrypt it. Changing the account password may require updating the wallet password
separately in KWallet Manager. Personal provider/autostart settings may override system defaults.

## Verification and recovery

Inspect the actual owner with `busctl --user status org.freedesktop.secrets`; its executable
must be `ksecretd`. `kwalletd6` supplies KDE API compatibility. A store/read/delete test using
a disposable value is available in `tests/integration/files/kwallet-probe.py`; it requires
an already-unlocked wallet and must not be used to trigger an unattended password dialog.
The root-only `kwallet-native.py --isolated` helper tests native PAM in a private bus/data
root, temporarily adds/removes its own test PAM service and initializes a native salt on first
use. Feed credentials through stdin securely, never shell arguments or committed configuration.
Its explicit `--live` mode initializes the actual wallet and is reserved for reviewed migration.

`keyring.enabled: false` stops reconciliation; it does not undo activation. Generic restoration
restores all recorded Qubix defaults, including exact original PAM/provider/autostart bytes and
absences, with normal drift checks. Review [restoration](restoration.md) before using it.
Retain both encrypted stores: new KDE entries are not copied back automatically. Activate the
restored provider at a later logout/login; changing files alone does not change the current owner.
