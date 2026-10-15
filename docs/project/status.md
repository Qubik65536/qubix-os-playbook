# Project status

Updated: 2026-10-15. Stage: **MVP candidate; acceptance In Progress**.
The physical CachyOS Niri desktop is deployed and returns after reboot at 100% scale with the slim
information bar. The native-style Plymouth and active Limine image adapter are deployed from clean 87e824b.
Exact active-image/font checks, installed verification and zero-change reapplication pass. A normal-kernel
reboot returns the desktop; the operator reports that the refined screens work but need higher contrast,
smaller menu text, no decorative captions and a cube background matching the desktop. That correction
is Implemented and native-preview Tested; activation and subjective visual acceptance remain open.
The first Plymouth activation failed visual acceptance and is not counted as a successful boot theme.

The [midnight/Krypton refinement](../architecture/boot-design.md) is now Implemented for Plymouth in
source: a 154 KB renamed subset with embedded OFL, gradient background, original vector ring and
outlined wordmark. Native Pango all-mode animation/prompt rendering and a separate forced-FreeType
boot/prompt control pass with exact final font resolution, preservation and cleanup (50 tasks);
the two-generator fixture passes 409 tasks with five expected refusals. Re-exporting all 38 PNGs
with Inkscape 1.4.3 gives identical checksums. The refinement is activated; see the deployment evidence below.
Limine's matching CP437 font, midnight cube wallpaper and separate heading/help/selection palette are
also Implemented. The exact 15-key graphical-baseline upgrade, preservation, reapplication, restoration
and eight refusal cases pass 726 tasks; the independent global check-mode control passes 21 tasks
without metadata writes. Native no-write preview passes 1197 tasks/40 proposed changes, followed by
an audit of unchanged protected files, 75 baselines and no pending markers. Image/cache lifecycle
regressions pass 771 tasks; bindings pass 368 normal/220 check-mode tasks, and loader/recovery checks
pass 752/232 tasks. These fixture results remain separate from native reboot and console evidence.

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
| Limine | Graphical fixture passes 301 tasks with four expected refusals; protected entry/argument/snapshot bytes verified; operator confirms the deployed menu appearance after reboot |
| Plymouth | Native two-step preview passes 48 tasks and all three modes; mkinitcpio/source/active-image checks pass; operator confirms normal-kernel startup and reboot appearance; poweroff/LTS/recovery remain open |
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

The first reapplication loses connectivity after 1337 successful tasks/zero changes; a resumed run
also encounters a brief LAN failure after 758 tasks/zero changes. Neither interrupted run counts as
completed idempotency. After reconnection, a clean detached checkout of the same e7e652a source and
the identical configuration passes 1490 tasks with zero changes, unreachable hosts or failures.
Both generator invocations are skipped. Installed verification again passes 284 tasks/zero changes.
The pending marker clears normally; all 75 private baseline hashes and tracked resources match the
reconnection audit. Native hourly Snapper cleanup refreshed limine.conf.old to the current config
before this run; all 18 other native boot/cache/EFI resources and the active config remain unchanged.
Temporary sleep inhibitors expire or are stopped; no persistent power policy changes are made.

The guarded reboot request validates all four source/staged images, both pins, all theme assets,
the verified clean revision, cleared pending markers and original recovery baselines before execution.
A one-time 15-second boot-menu request is accepted. The new boot ID is
68011c7a-65dc-41c9-8da8-cf8253bd82d1, running unchanged 7.2.9-2-cachyos via Limine 12.9.3 and the
native CachyOS.linux-cachyos entry. SSH/SDDM and Plymouth start/quit services succeed; the previous
boot records a successful Plymouth reboot-screen service. Qubix Niri/Noctalia return with wallpaper
and bar layers, no dock layer, and eDP-1 at 1920x1080/100% scale. The temporary target inhibitor is gone.
All protected files and 75 baseline hashes match the preboot audit; among the 19 native boot resources,
only loader/random-seed changes across boot. Pending state remains absent. The operator answers yes
for Limine, startup and reboot visuals, then requests more distinctive colours and Monaspace Krypton.
Automatic deployment state remains files-verified; this explicit console evidence is recorded here.

## Krypton deployment and reboot

Clean 87e824b deployment passes 1645 tasks/102 changes/zero failures. Installed verification passes
298 tasks with zero changes; identical reapplication passes 1572 tasks with zero changes and skips
font-cache refresh and both image rebuilds. Exact extraction of all four source/active images verifies
38 runtime assets and all three packaged copies of the final subset; both BLAKE2b pins match.
The 15-to-21-key recovery metadata upgrade preserves original bytes and unrelated fields. All 74
other earlier manifests and 32 original baseline hashes remain intact; there are 81 private manifests.
Protected Limine content outside the appearance block and two owned module references is unchanged.

The guarded 14:29 EDT reboot returns with boot ID d160a3aa-3c19-4935-b59c-fe45c539c4c4,
unchanged 7.2.9-2-cachyos and command line, Limine 12.9.3/native CachyOS entry, successful SSH/SDDM
and Plymouth start/quit services, and a successful prior reboot-screen service. Qubix Niri/Noctalia
return at 1920x1080/100% with bar/wallpaper layers and no dock. All 81 manifests, 76 tracked resources,
seven owned boot assets, root fonts and original recovery bytes match the preboot audit; only the
native loader/random-seed rotates. Pending markers and the temporary inhibitor are absent.
The operator reports “Works, needs visual adjustment”; contrast, captions, menu size and wallpaper
are now explicit follow-up requirements rather than accepted design results.

The contrast correction passes the 726-task Limine lifecycle/refusal fixture and the 50-task native
Plymouth preview: three animation modes, synthetic prompts under Pango and forced FreeType, exact
font selection, host preservation and zero leftover preview processes. The captures were inspected;
deployment and console acceptance of the correction remain pending.

## Limits and next gate

- Complete the requested contrast/caption/menu-size correction and obtain console feedback; retain native prompt behavior.
- Obtain separate poweroff and LTS observations; reboot-screen acceptance does not prove poweroff.
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
