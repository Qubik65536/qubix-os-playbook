# Troubleshooting

Status: Candidate diagnostics Implemented; [status](../project/status.md) defines actual support.

| Symptom | Next step |
|---|---|
| SSH timeout before authentication | Confirm target address, active sshd, listening port, firewall and VM network mode; password has not been tested |
| Restricted-sandbox RPC failure | Permit non-destructive Ansible IPC; retain target guards |
| Unsupported host | Use CachyOS Niri; the Mac controller is not a target |
| Missing companion | Prepare the named prerequisite manually, inspect again |
| Invalid option/type | Compare schema; use YAML booleans |
| Native parser rejects candidate | Retain version/output and report; do not bypass validation |
| Appearance unchanged | Confirm the running Qubix profile and saved GUI overrides; compare the actual bar with the current desktop design |
| No session picker | Use a free TTY; fixed-command greetd is preserved |
| Duplicate companions/agent | Collect running user units/processes before changing startup |
| Login rejected | Require unambiguously active SDDM and compatible regular Breeze tree |
| Boot/generator unresolved | Confirm active chain/config/version/mappings before opt-in |
| Limine still looks like CachyOS | Confirm the selected config/version and enabled component; Limine 12 supports Qubix wallpaper/palette, while older supported versions use text/colour settings |
| UKI/complex preset/HOOKS override rejected | Unsupported candidate setup; leave splash disabled and report |
| Archive resource failure | Retain pending marker; inspect native generation before repair/retry |
| Restore drift refusal | Review baseline/local edit before explicit force |
| Changed-kernel image refusal | Snapshot or reviewed native current-kernel recovery; force cannot bypass |
| Probe permission failure under /boot | Use explicit typed qubix_discovery_privileged=true with --ask-become-pass for read-only metadata; failure does not establish absence |

Report revision, options, target versions, command, pending state and redacted output using the [collection guide](collecting-target-info.md). Never include passwords/private keys/backup images or repair appearance by replacing entries, PAM, encryption or dotfiles.

Noctalia reads Qubix defaults from /etc/qubix/noctalia/config.toml when launched through the Qubix profile. GUI preferences under your XDG state root's qubix/noctalia/settings.toml override those defaults and survive deployment. Inspect only the relevant bar/widget settings before changing them; do not delete the whole preference file. A successful config-reload or parser check proves neither the visual distinction nor the logo's legibility. The [desktop design](../architecture/desktop-design.md#bar-visibility-and-logo-correction) records the measured launcher image scale and native screenshot comparison.

The [bootloader contract](../components/bootloader.md) lists exactly what Limine currently manages. Version 12 uses its own supported wallpaper/palette controls; a GRUB theme.txt cannot be reused as a Limine theme.

## Remote validation interrupted

Wake the target and recheck its address, SSH service and firewall using the
[connection guide](collecting-target-info.md). DHCP changes can invalidate a restricted controller
allow rule. Preserve protected pending markers: they distinguish an incomplete attempt from the
last verified deployment. Reconnect and rerun the same source/configuration, then complete installed
verification and unchanged reapplication before reboot. A successful earlier deployment does not
turn a later unreachable run into a completed idempotency test. Keep the test machine awake during
long file/backup checks; do not disable unrelated power settings or remove recovery state to bypass them.
