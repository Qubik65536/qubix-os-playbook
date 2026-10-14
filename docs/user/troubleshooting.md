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
| Appearance unchanged | Select Qubix Niri; native/personal Niri files are preserved |
| No session picker | Use a free TTY; fixed-command greetd is preserved |
| Duplicate companions/agent | Collect running user units/processes before changing startup |
| Login rejected | Require unambiguously active SDDM and compatible regular Breeze tree |
| Boot/generator unresolved | Confirm active chain/config/version/mappings before opt-in |
| UKI/complex preset/HOOKS override rejected | Unsupported candidate setup; leave splash disabled and report |
| Archive resource failure | Retain pending marker; inspect native generation before repair/retry |
| Restore drift refusal | Review baseline/local edit before explicit force |
| Changed-kernel image refusal | Snapshot or reviewed native current-kernel recovery; force cannot bypass |
| Probe permission failure under /boot | Use explicit typed qubix_discovery_privileged=true with --ask-become-pass for read-only metadata; failure does not establish absence |

Report revision, options, target versions, command, pending state and redacted output using the [collection guide](collecting-target-info.md). Never include passwords/private keys/backup images or repair appearance by replacing entries, PAM, encryption or dotfiles.
