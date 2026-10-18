# KWallet acceptance evidence

Date: 2026-10-17. Status: Implemented; native unlock/migration/API, file installation and recovery Tested;
real greetd password login pending.
Source: this change based on `70e5870`; final implementation is recorded by its commit.
Environment: existing physical CachyOS Niri desktop, active greetd; native KWallet
6.31.0-1.1, kwallet-pam 6.8.0-1.1 and kwalletmanager 26.08.2-1.1.
Authoritative responsibilities and acceptance: [keyring contract](../components/keyring.md).

## Native installation and session evidence

Native Pacman installs 38 new packages (153.68 MiB), including KWallet, PAM and its manager.
No distribution upgrade, display-manager switch, reboot or initramfs operation runs.
Package hooks create native Snapper snapshot 24. GNOME Keyring remains required by
`cachyos-niri-noctalia`; its package is retained instead of breaking that dependency.

The disposable native PAM service authenticates the ordinary account through `pam_unix`,
opens the native KWallet session hook and checks its socket. The native `pam_kwallet_init`
handshake starts `ksecretd` on a private D-Bus with temporary configuration/data. The encrypted
wallet opens automatically and a disposable Secret Service value is stored, read and deleted.
The reusable helper repeats successfully with generalized user handling and daemon cleanup.
This establishes native module behavior, not an actual greetd logout/login.

Three existing GNOME Login entries are transferred in memory. Labels, attributes and every
secret byte compare equal; the original encrypted `login.keyring` checksum is unchanged.
One binary value's invalid legacy text content type is corrected to `application/octet-stream`;
its bytes remain exact. Initial guarded attempts reveal the content type issue and a stale
libsecret item cache; neither attempt is counted as migration success. The original provider
is restored between retries; final verification uses direct D-Bus reads and passes.
No secret values, labels or application metadata are recorded in this document or logs.

The live Secret Service owner is `ksecretd`, PID 8419 at verification, with default alias
pointing at `/org/freedesktop/secrets/collection/kdewallet`. Its collection is unlocked.
A separate KDE API test opens `kdewallet` through `kwalletd6`, stores/reads/deletes a disposable
password and removes the test folder. Both API roundtrips pass. GNOME daemon processes are absent.
Niri PID 1151 remains active; no display-manager restart, logout or reboot is performed.

## Deployment, fixtures and remaining gates

PAM/schema/Niri fixtures pass 131 tasks with five disposable setup/cleanup changes and nine
expected refusals in normal and check mode. Coverage includes custom/required keyring hooks,
unknown/duplicate includes, missing final newline, malformed schema, unsupported manager,
missing prerequisites and byte-identical Niri/PAM reapplication.

The disposable file lifecycle passes 376 tasks/39 fixture changes, including exact installation,
verification, reapplication with zero managed changes and restoration of all seven system-default
resources. Planning authorization is cleared before recovery, proving independent original-PAM
restoration. Original provider absence is restored. Niri grammar is tested separately on the target.

| Gate | Actual evidence |
|---|---|
| Package preparation | Native installation above; playbook check passes 42 tasks/zero changes |
| Final file installation | Deployment passes 209 tasks/two final startup-file/receipt changes; eight resource definitions verified |
| Parser | Native `niri validate --config /etc/niri/qubix/config.kdl` passes the final guarded startup line |
| Installed verification | Production `verify --tags installed` passes 67 tasks/zero changes |
| Reapplication | Identical-source production deployment passes 209 tasks/zero changes |
| Session | Native isolated PAM unlock, live Secret Service and KDE API probes pass; provider stays unlocked, GNOME processes absent |
| Boot | No reboot, bootloader activation or image rebuild performed |

`./scripts/validate.sh` passes YAML, Ansible lint/syntax, ShellCheck, Python compilation,
repository/link/schema checks, 32 JavaScript tests and whitespace checks. The existing generic
schema/discovery fixture passes 827 tasks/zero changes, with 38 expected refusals.
An explicit GNOME startup test was rejected by automatic approval review because it could reclaim
Secret Service. The safer inspection verifies effective condition drop-ins, their absent marker,
D-Bus provider selection and generated autostart unit without starting GNOME. The measured XDG
autostart target is inactive, so the independently installed Niri startup hook is essential.

Actual greetd password logout/login, absence of an unlock dialog on that login and future
KDE application behavior remain operator gates. No boot acceptance is claimed. Encrypted
GNOME originals and all package dependencies remain available for recovery.
