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

## Arrow and H/J/K/L aliases with larger resizing

Source: parent `5faffe0` plus this change. Same SSH target and output layout as above.
Contract: [additional resize and movement aliases](../architecture/desktop-design.md#additional-resize-and-movement-aliases).
The new Ctrl+Alt directional family supplies both key sets for screen focus/movement,
retaining Alt+L locking and the old arrow bindings. Ctrl+Shift supplies 10% resize
steps alongside the existing 5% controls. All additions ship with enabled Niri;
no new prerequisites or profile inputs are needed.

Controller desktop fixtures pass 86 tasks/zero changes each in normal/check modes,
including generated-data coverage and duplicate-key refusal. Static validation passes.
The expanded native regression fails before installation on missing
`Mod+Ctrl+Alt+Right`, after exercising the old screen roundtrip and cleaning its
own terminal/restoring focus. Pair inspection confirms all 24 arrow/letter action
and label pairs match across tiled navigation/movement, 5%/10% resizing and screen
navigation/movement, with unique keys and the original lock binding intact.

Preview passes 102 tasks/two proposed changes, adding only 24 bindings and JSON
labels, with no removed content. Installation passes 110 tasks/four changes
(the two files and their recovery receipts). Native parser/session acceptance
passes three tasks/zero Ansible changes: all 32 entries agree with installed KDL
and JSON, both arrow/letter screen roundtrips pass, and no-neighbor actions pass.
From a 942-pixel starting column, Left/H produce 751 pixels and Right/L produce
1132 pixels, demonstrating identical measured 10% steps with either key set.
Height actions execute and reset successfully. Original focus, window/workspace
assignments, personal hashes, output geometry, Niri PID and boot ID are preserved;
the test terminal exits. Identical reapplication passes 110 tasks/zero changes.

The expanded helper checks all 32 screen/coarse-resize entries against installed
KDL and JSON, exercises original arrows plus the new arrows/letters, measures
column width changes and exercises height/reset actions on its own terminal.
Height behavior in a stacked column and physical key events remain separate
operator checks. No boot checks or reboot are requested.
