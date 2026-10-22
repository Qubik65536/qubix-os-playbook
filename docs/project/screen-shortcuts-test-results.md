# Screen shortcut acceptance

Date: 2026-10-22. Source: parent `c310162` plus this change's managed KDL and
native regression. Environment: operator-selected CachyOS SSH target, Niri 26.04
(`8ed0da4`), existing Qubix session. The internal eDP-1 screen is 1920×1080 at
(0, 0); external HDMI-A-1 is 2560×1440 at (1920, 0), both at 100% scale.
No output configuration is changed. Contract: [screen navigation](../architecture/desktop-design.md#screen-navigation).

The default bindings focus screens with Super+Alt+arrows and move only the focused
window with Super+Alt+Shift+arrows. Labels are derived into the existing shortcut
panel. No new prerequisites, profile keys, connector mappings or ownership changes.

| Gate | Actual evidence |
|---|---|
| Controller | Desktop fixture normal/check: 86 tasks, zero changes each, eight expected rescued refusal cases; generated data covers all KDL bindings without duplicate keys. |
| Static | `./scripts/validate.sh` passes. Existing ignored local-YAML document-start and offline collection warnings remain. |
| Before installation | Native regression fails on the absent screen binding; its temporary terminal is removed and focus restored through `finally`. |
| Preview | 102 tasks, two proposed changes: only eight KDL bindings and their generated JSON labels. |
| File installation | Focused Ansible deployment passes 110 tasks/four changes: managed config/shortcut data and their recovery receipts. Existing original baselines are retained. |
| Parser | Installed Niri validates the candidate before atomic config installation; the regression validates the installed KDL again. |
| Session | Native regression passes three tasks/zero Ansible changes. Reloads the existing Qubix compositor; all eight configured actions and matching JSON labels pass. |
| Movement | Real internal/external focus and test-window roundtrips pass. Up/Down focus/move are no-ops with no neighbor above/below this horizontal layout. |
| Preservation | Original window IDs/workspace assignments, focus, personal Niri/Noctalia/WezTerm hashes, output descriptions, Niri PID and boot ID remain unchanged across the native regression. Test terminal exits. |
| Reapplication | Identical focused deployment passes 110 tasks/zero changes. |
| Boot | No boot files, rebuild, service transition or reboot; boot acceptance is outside this change. |

The focused developer deployment uses the ordinary profile/discovery/Niri roles,
then `qubix_files` with task-scoped sudo for exactly
`/etc/niri/qubix/config.kdl` and
`/usr/share/qubix/noctalia/plugins/shortcuts/bindings.json`. Other rendered
resources are not reconciled. Local logs are ignored `.cache/screen-shortcuts-*`.
User deployment continues to follow the [local-machine procedure](../user/deployment.md).

Repeat native acceptance only on the explicitly selected developer target with
both named screens in the layout above:

```bash
.venv/bin/ansible-playbook tests/integration/screen-shortcuts.yml \
  -i inventory/target.local.ini
```

This script exercises the actions extracted from the installed bindings over IPC,
using a temporary WezTerm window; it does not synthesize physical keyboard events.
Physical key input, vertically stacked output transfers and unplug/replug behavior
remain operator checks. Next: press the new keys on both
screens and confirm the updated list after reopening Super+Shift+/.
