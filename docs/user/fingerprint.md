# Fingerprint setup on CachyOS

Status: **Guide Implemented; enrollment and real authentication require the operator**.
The playbook preserves PAM and fingerprints. Run enrollment at the laptop in your own logged-in
desktop or TTY, with a working password and a separate recovery shell available.

## Check the reader and enroll

Inspect the native packages and USB device:

```bash
lsusb
pacman -Q fprintd libfprint
```

If missing, install `fprintd` using the normal CachyOS package procedure. fprintd is D-Bus activated;
it normally does not need `systemctl enable`. Check [libfprint's supported devices](https://fprint.freedesktop.org/supported-devices.html)
against the actual USB ID. A supported ID alone does not prove firmware or matching quality.

Enroll and verify as your ordinary account:

```bash
fprintd-enroll -f right-index-finger
fprintd-list "$USER"
fprintd-verify -f right-index-finger
```

Lift and replace your finger until enrollment completes, then verify several times with the sensor
clean and dry. Do not run enrollment as root: the intended identity is your desktop account.
Remote SSH may be refused by Polkit because it is not an active local session; use the local
desktop rather than weakening the policy. For errors inspect `journalctl -b -u fprintd`.
The [fprintd manual](https://man.archlinux.org/man/fprintd.1.en) documents enrollment, verification
and deletion. `fprintd-delete "$USER"` removes that account's enrolled fingerprints when deliberately requested.

## Unlock an existing Noctalia desktop

Noctalia 5.3's [fingerprint authenticator](https://github.com/noctalia-dev/noctalia/blob/v5.3.0/src/auth/fingerprint_authenticator.cpp)
uses fprintd directly through D-Bus. Enrollment and Noctalia's Security → Lock Screen → Fingerprint
setting are the first checks; adding a module to the greetd PAM stack does not configure this path.
Keep the password field available. In the Qubix session use the GUI setting, which belongs to the
Qubix-only user state; the playbook does not replace that state. The supported shell setting is
`[lockscreen] fingerprint = true`.

After saving your work, lock once and verify both a fingerprint unlock and a password unlock.
Then test suspend/resume. Physical interaction is required; an SSH reader listing cannot establish
lock-screen authentication. If the reader remains claimed, close a separate `fprintd-verify`
process before trying again. Do not kill or replace the desktop session as a diagnostic.

## Log in through Noctalia Greeter

First establish a working **password** login through greetd and return to Qubix Niri using the
[greeter guide](login.md). Greeter authentication uses greetd's PAM service, whereas Noctalia's
desktop unlock uses its own fprintd integration. Sudo, TTY, SSH and disk encryption are separate.

Inspect `/etc/greetd/config.toml` for `[general].service` (default `greetd`) and inspect that
service's `/etc/pam.d/` file and its includes. Back up the exact files before editing, retaining
ownership and mode. Use `sudoedit`; never replace a complete PAM stack with a downloaded example
or edit the global `system-auth` file just to enable greeter fingerprints.

A service-specific fingerprint rule commonly uses:

```text
auth sufficient pam_fprintd.so max-tries=1 timeout=10
```

This is an example **to integrate after reviewing the existing policy**, not a complete PAM file.
Its position and `sufficient` control can bypass later auth rules on success. Keep applicable
access, lockout and other required checks effective, and retain the native password, account and
session stacks. Do not append a `required` fingerprint rule that makes both fingerprint and
password mandatory. For an isolated policy, copy the native greetd PAM file to a separately named
service such as `greetd-fingerprint`, review the auth-rule placement there, and point only
`[general].service` to that reviewed service. Leave the greeter-session PAM service and other
applications' services untouched. Restore the original service selection to undo that experiment.

The target's greetd 0.10.3 falls back to the general PAM service when the optional greeter-specific
service file is absent. Keep its greeter account/session policy intact when selecting a dedicated
service; see the [native service selection](https://github.com/kennylevinsen/greetd/blob/0.10.3/greetd/src/server.rs).

In `/var/lib/noctalia-greeter/greeter.toml`, merge these values into the existing `[auth]` table
after choosing the PAM policy:

```toml
[auth]
allow_empty_password = true
request_timeout = 60
```

An empty Enter submission lets the fingerprint PAM conversation begin; it does not grant an
empty-password login by itself. PAM still decides authentication. Keep the greeter timeout longer
than the fingerprint attempt plus password fallback. The playbook preserves these operator settings.

PAM processes fingerprint and password sequentially. While the fingerprint module waits, password
checking waits too; an empty-submit option does not make them parallel. A short bounded fingerprint
timeout helps password fallback. See [pam_fprintd](https://man.archlinux.org/man/pam_fprintd.8.en)
and [Noctalia's limitation and recovery notes](https://docs.noctalia.dev/greeter/troubleshooting/#fingerprint-blocks-password-login).

At the console test a valid fingerprint, an unrecognized finger, timeout followed by a correct
password, a wrong password, cancellation and the selected Niri session. Keep your recovery shell
open until all succeed. To recover, return to the TTY/SSH shell and restore the exact PAM/config
backups; changes take effect on the next authentication conversation. Do not change SSH or sudo
authentication to fix a greeter issue.

Fingerprint login does not unlock an encrypted root filesystem and may not unlock a
password-encrypted keyring. Keep your disk passphrase and account password available.

## Recorded target evidence

On 2026-10-16 the existing target reports fprintd 1.94.5-2.1 and Synaptics `06cb:00bd`;
fprintd exposes one device. An SSH enrollment-list query is refused by Polkit. No enrollment,
fingerprint verification, PAM change or real login is performed by this task. Do the local
enrollment and acceptance checks above before calling fingerprint login Tested.
