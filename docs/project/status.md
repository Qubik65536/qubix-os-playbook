# Project status

Updated: 2026-10-15. Stage: **MVP candidate; acceptance In Progress**.
The physical CachyOS Niri desktop is deployed and returns after reboot at 100% scale with the slim
information bar. The corrected native-style Plymouth and active Limine image adapter are fixture
Tested and deployed from clean e7e652a. Exact active-image checks and installed verification pass; reapplication was interrupted by target connectivity loss, and controlled boot observation remains pending.
The first Plymouth activation failed visual acceptance and is not counted as a successful boot theme.

| Capability | Status and actual evidence |
|---|---|
| Architecture, ADRs and conventions | Implemented before source; local links and schema/default agreement pass |
| Tooling/CI | Static checks and fixtures Tested locally; Actions configured, not executed remotely |
| Profile/discovery | Unsupported/schema/identity fixtures and native read-only discovery Tested |
| Branding | Native install, exact resources, original preservation, reapplication and earlier restoration Tested |
| Niri/Noctalia | Native grammar, private rendering, primary startup/reload and 100% output scale Tested; physical interaction/recovery acceptance open |
| Shell/terminal | Native temporary-home Bash/Starship checks pass; personal files and default Fish preserved |
| Login | SDDM clone/activity/ambiguity fixtures Tested; physical target branding disabled; authentication/restore pending |
| GRUB | Preservation/dispatch/reapplication/recovery fixtures Tested; independent native boot/restore pending |
| Limine | Graphical fixture passes 301 tasks with four expected refusals; graphical appearance deployed; protected entry/argument/snapshot bytes verified; physical appearance pending |
| Plymouth | Native two-step preview passes 48 tasks and all three modes; selection, native mkinitcpio generation and exact active-image assets verified; controlled appearance observation pending |
| Image/cache adapters | Two-image nested-entry lifecycle passes 767 tasks with two expected stale-pin refusals; binding/enrollment/FAT fixtures pass 368 tasks with five refusals and check mode 220 tasks with four refusals |
| Recovery/state | Generic and loader regression suite passes 966 tasks with seven expected refusals; native classic desktop recovery Tested; newer desktop/boot recovery pending |

## Current validation

`./scripts/validate.sh` passes YAML, Ansible syntax/lint, ShellCheck, Python helper compilation,
Markdown/local links, manifests/configuration consistency and diff whitespace. Shared scripts/CI
include the image-binding fixtures; the expanded CI timeout is 30 minutes. Fake generators and
inspectors establish dispatch, preservation and recovery contracts, not native boot validity.

The native-style Plymouth preview loads the real two-step plugin, rejects an invalid-module control,
animates boot/reboot/shutdown, renders the native password prompt and leaves zero processes.
Host selection, daemon and desktop configuration remain unchanged. See the
[splash results and reviewed corrective plan](plymouth-test-plan.md).

The exact physical no-write deployment preview passes 1077 tasks with 43 proposed changes and zero
failures. A subsequent protected audit confirms all 76 native/personal resources, 19 native boot/cache/
EFI resources and 32 existing first-baseline hashes unchanged, with no pending deployment state.
No generator or staged-image activation runs in check mode.

Desktop evidence, including the slim information bar, primary reload/startup, absence of the dock,
retired native login entry and preservation, is in [desktop test results](desktop-test-results.md).
README links both [operator](../user/getting-started.md) and
[human developer](../development/getting-started.md) onboarding.

## Corrective deployment results

Clean e7e652a deploys successfully: 1542 tasks, 145 changes, zero failures. Installed verification
passes 284 tasks with zero changes. Native extraction of both generated images and both Limine-
referenced stages verifies all 38 runtime asset checksums, Theme=qubix, two-step/label plugins and fonts.
Both native BLAKE2b pins match; protected Limine bytes, including entry identities/arguments and
snapshot sections, remain unchanged. All 19 native cache/history/EFI resources and all 32 earlier
baseline hashes remain intact. There are now 75 private baseline manifests. Only the two intended
source images and limine.conf change among the 76 tracked native/personal resources.

Identical reapplication reaches 1337 successful tasks with zero changes, then SSH becomes unreachable
(one unreachable, zero component failures). This is an interrupted test, not a completed zero-change
reapplication. The protected transient attempt marker was present during that run and may remain;
the last verified deployment still records clean e7e652a. IPv4/IPv6 SSH and ping fail afterward; the
known local hostname still resolves to the recorded address. The planned controlled reboot has not
been requested. The operator has been asked to wake/reconnect the machine and report any console test.

## Limits and next gate

- Reconnect the test machine, complete same-source reapplication and verify pending state clears.
  Then run the guarded reboot and obtain console observations of Limine/startup/shutdown.
- Test independent GRUB and dracut boots, LTS boot, login authentication, encrypted-root input where
  relevant, physical shortcuts/locking/portals and current desktop/boot restoration in disposable VMs.
- Fixed image/kernel mappings require reinspection after package updates. Stale native pins and
  narrower earlier appearance ownership fail safely; reviewed rebasing remains backlog work.
- Boot components remain opt-in. The operator approved this physical-target Plymouth test and
  subsequently requested Limine/startup/native-style corrections; other boot work retains VM policy.
- Backups preserve bytes, UID/GID/mode and absence, not ACLs/xattrs or whole-system state. Restore is
  per resource; Limine config precedes stage removal. Concurrent deployment/package updates are unsupported.

The first physical splash attempt rebuilt generator outputs but missed Limine's separate pinned cache.
It returned SSH/SDDM/Qubix successfully, but the operator still saw CachyOS startup and rejected the
large scripted shutdown layout. The corrected implementation preserves native cache/history/EFI files,
stages content-addressed images, atomically changes only bound module references/pins and uses the
native small-spinner layout. File/archive verification and physical appearance remain distinct gates.
