# Login appearance

## Noctalia Greeter preparation and existing greetd

Status: **Implemented; fixtures, native UI rendering, installation and reapplication Tested;
operator-approved next-boot selection verified; actual login pending**.
Focused task: install the CachyOS `noctalia-greeter` package alongside
the current manager, supply the existing Qubix desktop palette/wallpaper, and document fingerprint
enrollment and a separately reviewed manager cutover. The existing SDDM adapter remains supported.

Contract (documented before implementation):

- `login.backend: greetd`, `theme_source: noctalia`, `activation: prepare` prepares the native
  `/var/lib/noctalia-greeter/greeter.toml` and an additive greetd configuration example. It must
  reject an active greetd, so preparation cannot silently reconfigure an existing login screen.
- `activation: existing` (the default) accepts only an already-active greetd whose existing
  configuration launches `/usr/bin/noctalia-greeter-session`. It manages appearance alone.
  Standard appearance mode does not edit `/etc/greetd/config.toml`, PAM, services, accounts or native session files.
  Explicit `compact: true` additionally selects the private UI client through the narrow,
  backed-up wrapper change in the [refinement contract](../architecture/login-refinement.md).
- Support is measured Noctalia Greeter 1.6.x, using the released declarative appearance interface.
  Require the installed wrapper/compositor, a real package-created state directory and Qubix
  branding/Niri resources. Reject unsupported combinations and redirects before resource writes.
  The supported native greetd unit has no launcher flags, drop-ins or environment overrides;
  `/etc/greetd/greetd.conf` must be absent because it takes precedence over `config.toml`.
- Managed appearance uses all sixteen roles from the same Qubix palette as Noctalia, the existing
  cube wallpaper, dark mode and matching corner radii. Preserve mutable `sync.toml`, keyboard,
  monitor, user, authentication and session settings in an existing greeter configuration.
- Package installation is an explicit, separate preparation playbook; bootstrap never installs
  packages or switches display managers. Native package hooks can refresh Snapper/Limine menus;
  record those effects separately from Qubix appearance writes.
  CachyOS's Greeter package hook also integrates `pam_systemd` into newly installed greetd PAM;
  preserve pre-existing PAM files and do not template authentication policy in Qubix.
- The shared first-baseline engine owns only the exact greeter configuration path under `/var/lib`;
  it backs up existing bytes and metadata, records original absence and supports drift-safe recovery.
- Fingerprint setup includes operator documentation and the optional GTK enrollment application;
  service-specific PAM review, password fallback and restoration remain operator steps. No automatic PAM modification.
- Native Noctalia has no caption override. The optional private presentation build changes only
  launcher/Home captions; os-release and the System tab retain CachyOS identity. The separately
  requested Limine OS-title change preserves IDs, snapshots and kernel arguments. Both are defined
  in the [refinement contract](../architecture/login-refinement.md).

Acceptance: focused normal/check-mode fixtures cover preparation, existing-manager gating,
palette agreement, malformed/unsupported inputs, redirects, preservation, file installation,
zero-change reapplication and original restoration. Static checks pass. Native evidence must
separately record package/file installation, TOML parsing, reference/custom preview screenshots,
preservation and cleanup. A real greetd password login, Niri return, fingerprint login and reboot
remain separate operator/VM gates; preparing files never claims authentication acceptance.

## SDDM

Status: Implemented candidate; cloned-UI and unsupported-manager fixtures Tested; native preview/login needs VM.

`login.enabled` remains opt-in. `backend: auto` accepts only measured already-active SDDM; `theme_source: breeze` requires an installed non-symlinked Breeze tree with supported background/type options. The source authentication QML and resources are cloned unchanged into `/usr/share/sddm/themes/qubix/`. Qubix changes only the supported background override and Current theme selection. Existing source theme, PAM, manager and session startup remain preserved.

A backed-up drop-in activates the clone; if `/etc/sddm.conf` already sets Current with higher precedence, only that one setting is minimally replaced with backup. Ambiguous Current declarations or incompatible source themes fail. Discovery probes both the manager alias and individual SDDM/greetd/GDM/LightDM units. Standalone active SDDM is accepted; conflicting active managers fail safely. No service restart is performed. On the VM, preview `sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/qubix` where available, then verify actual login into both native and Qubix sessions. File-copy success does not establish a working login. Restore uses the shared first-baseline engine.
