# Noctalia Greeter test results

Status: **Implemented; native rendering, installation and reapplication Tested; next-boot
selection verified; actual login acceptance pending**. Contract:
[login appearance](../components/login.md). Operator procedures:
[greeter](../user/login.md) and [fingerprint enrollment](../user/fingerprint.md).

## Source and environment

The reviewed release is Noctalia Greeter v1.6.0, upstream commit
`44337ecba043749c29de6f3d563315b91987a908`. The target is the previously configured CachyOS
Niri desktop, with Noctalia 5.3.0-1.1, Greeter 1.6.0-1 and greetd 0.10.3-2.1.
SDDM remains active. The native package supplies the `greeter` account and 0750 state directory.
The theme uses the playbook's existing Noctalia palette and desktop cube wallpaper.

## Package preparation

The separate `playbooks/prepare-login.yml` check-mode preview passes 46 tasks with zero changes.
Actual installation passes 47 tasks/one package-transaction change. It installs seven packages:
greetd, greetd-agreety, noctalia-greeter, libliftoff, wayland-protocols, xcb-util-errors and wlroots0.20.
No database refresh or system upgrade is requested. The package-created state directory already
exists, so the fallback tmpfiles initializer is skipped. Native package installation supplies
greetd's PAM file. The cached Greeter package's `.INSTALL` confirms its post-install hook invokes
the upstream setup script. Comparing the new greetd file with the cached native greetd package
finds exactly one added `session required pam_systemd.so` line; the authentication portion is
unchanged. No Qubix task edits PAM or enables fingerprint authentication. All pre-existing PAM
files remain unchanged. The preparation task itself does not directly invoke the setup script.
Identical package preparation subsequently passes 45 tasks with zero changes.

The before/after protected audit finds only `/boot/limine.conf` changed among the earlier
76 tracked resources, from native snapshot hooks. Every earlier recovery manifest, receipt and
original backup is unchanged. This is package preparation evidence, not a new boot-theme activation.

## Fixture evidence

The final disposable-root fixture passes 512 tasks in normal mode and 381 tasks in global check mode,
with sixteen expected refusals in each. The temporary setup/cleanup changes
are isolated fixture operations. It exercises shared-palette rendering, retained session/input/
output/auth/per-output-wallpaper settings, original file restoration, unchanged resource copies,
measured version boundaries, manager activity, legacy/overridden configuration sources,
noncanonical/malformed TOML and redirected configs.
No native authentication or service command runs in these fixtures.

The expanded schema/discovery fixture passes 609 tasks with zero changes (34 profile, eleven
host, seven identity cases and normalization). The original SDDM fixture passes 58 tasks with two
expected refusals. `./scripts/validate.sh` passes static checks, syntax/lint and repository links.

## Native comparison

The native comparison passes 87 tasks/four temporary changes. It runs the actual packaged client
under Niri 26.04 in a temporary 1272×688/100% output, with synthetic `preview` identity, private
runtime/state, a non-activating private D-Bus session and a nonexistent greetd socket. The primary
Niri process and four personal/GUI configuration hashes remain unchanged; no test process remains.
The greeter logs contain no unknown configuration keys, invalid TOML or incomplete-palette warning.

Source: Qubix implementation `b08727c` (based on `e526a2c`); upstream Greeter release/revision above.
The reference uses built-in appearance.
The customized candidate uses the same sixteen Qubix palette roles as the desktop, its existing
cube wallpaper, dark mode and 1.35 corner-radius scale. The initial Noctalia wordmark is hidden.
The unavailable-login warning is intentional in both captures: the preview cannot authenticate.
No personal account, avatar, application window or enrolled fingerprint appears.

![Native Noctalia Greeter 1.6.0 reference preview](../assets/login/reference-noctalia-greeter-1.6.0.png)

Reference: unmodified built-in Noctalia scheme and wordmark, synthetic user, native UI client under
nested Niri; this is a preview, not the active login screen.

![Customized Qubix Greeter preview](../assets/login/qubix-noctalia-greeter-1.6.0.png)

Customized: shared steel-blue surfaces and cube wallpaper, preserved original wallpaper colours,
hidden native wordmark and matching rounded panel. Same environment and synthetic user as reference.

Native UI rendering is separate from greetd's DRM/VT compositor, actual password authentication
and reboot acceptance. No fingerprint enrollment or Qubix PAM authentication change occurs;
the native package's new-session integration is recorded above.

## Installation and next-boot selection

Clean `b08727c` with the same login/desktop selections and both boot components disabled passes:

| Check | Actual evidence |
|---|---|
| Deployment preview | 411 tasks/two proposed files |
| File installation | 518 tasks/eight changes: two resources and their recovery/deployment state |
| Installed verification | 87 tasks/zero changes; exact bytes/modes and native Niri/Noctalia parsers |
| Identical reapplication | 516 tasks/zero changes |
| Final configuration-source guards and installed verification | 90 tasks/zero changes |

The native greeter account can read/parse the root-owned 0644 theme file and read its wallpaper;
its existing 0750 state-directory ownership stays `greeter`. The final audit confirms all 76
protected paths and all 189 earlier recovery files unchanged from the post-package baseline.
Only four recovery files for the two newly owned resources are added; those remain unchanged
after reapplication. Source is recorded clean at `b08727c`, file verification succeeds and no
deployment-pending marker remains. Limine still reports `interface_branding: Qubix OS`.

After reviewing the installed candidate, the operator explicitly selects **Noctalia for next boot**,
overriding the repository's manager-replacement restriction for this transition. A separate
guarded native operation passes 20 tasks/six changes. It retains exact original greetd bytes and
metadata at `/var/lib/qubix/login-transition-b08727c/`, replaces only the agreety launcher with
`/usr/bin/noctalia-greeter-session`, disables SDDM's future startup and enables greetd's alias.
The rest of greetd's native configuration, including terminal/account/PAM selection, is unchanged.
The operation performs no service restart or reboot. SDDM remains active/disabled; greetd is
inactive/enabled, and `display-manager.service` selects greetd for the next boot. Niri PID 1082
and the boot ID remain unchanged. The [guide](../user/login.md) records exact selection recovery.
An independent read-only audit verifies the original backup hash, exact one-line launcher
replacement, native package session integration and final service/alias state.

This does not establish physical password input, greetd's DRM/VT renderer, a working PAM
conversation, Niri return from greetd, fingerprint login or reboot acceptance. Next: save work,
reboot when ready, verify password login into Qubix Niri, then enroll/verify fingerprints locally.
