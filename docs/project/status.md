# Project status

Updated: 2026-10-16. Stage: **MVP candidate; acceptance In Progress**.
Compact login, fingerprint setup and QubixOS captions **Implemented; controller/native simulated
adapter/rendering Tested; deployment In Progress**. The [refinement evidence](ui-test-results.md)
contains eight sanitized reference/custom captures. Private pinned UI clients preserve package
binaries, system identity and authentication code; checksum-bound provenance prevents stale reuse
after native updates. The graphical enrollment application uses ordinary GJS/GTK 4 and fprintd,
with explicit start/test/cancel and no PAM/Polkit changes. Display-only Limine naming is separately
bounded to the OS menu title and native generator target. Actual scans/login and renamed-menu
boot appearance remain separate operator gates. The target has returned in greetd/Niri after the
operator's intervening reboot; Qubix has not rebooted or restarted its manager in this task.

Noctalia Greeter **Implemented; fixtures/native rendering/installation/reapplication Tested;
operator-approved next-boot selection verified; physical login pending**. CachyOS
Greeter 1.6.0-1 and greetd 0.10.3-2.1 install alongside active SDDM; the separate package playbook
passes 47 tasks/one package transaction. Native snapshot hooks update Limine; prior recovery bytes
remain intact. The new appearance adapter shares the desktop palette/wallpaper, preserves native
input/output/auth/session/sync configuration and never switches services. The
[greeter guide](../user/login.md), [fingerprint guide](../user/fingerprint.md) and
[test results](login-test-results.md) distinguish preview/file evidence from real login acceptance.
Clean b08727c preview passes 411 tasks/two proposed files; installation 518 tasks/eight changes,
installed verification 87 tasks/zero changes and reapplication 516 tasks/zero changes. Final
configuration-source guards pass 512 normal/381 check-mode tasks with sixteen expected refusals;
native installed verification passes 90 tasks/zero changes. All 76 protected paths and 189 earlier
recovery files remain unchanged. With explicit operator approval, the next-boot selection changes
to greetd while the current SDDM desktop/Niri PID 1082 remain active; no restart/reboot is performed.
Original launcher bytes and enablement metadata are retained for recovery. Native package setup
adds only a session module to newly installed greetd PAM; pre-existing PAM/authentication stays
preserved. Noctalia's system label remains CachyOS; Limine retains the Qubix OS heading.

Power footer/lock-close fix **Implemented; controller/native regression, installation, live footer and
reapplication Tested**. Clean e80b697 restores corner prompts/Cancel and dispatches only after animated
closure. Native no-effect recorder confirms the panel is closed before dispatch (66 tasks/11 temporary
changes). Preview passes 323 tasks/two proposed changes; installation 407 tasks/five changes, installed
verification 63 tasks/zero changes and reapplication 407 tasks/zero changes. A detached Noctalia-only
restart and live screenshot confirm activation, preserving Niri, application windows, GUI settings,
outputs, 76 protected paths and original recovery records. The credential is removed. Native/before/
preview/countdown/live screenshots are committed; physical lock/unlock acceptance remains pending.

Power-layout correction **Implemented; native/live comparison, deployment and reapplication Tested**:
centred content, native 140 px panel height, badge placement and destructive Shut Down styling restored.
Clean 78cc3e1 preview passes 323 tasks/three proposed changes; installation 407 tasks/seven changes,
installed verification 63 tasks/zero changes and reapplication 407 tasks/zero changes. Live guarded/native
five-button captures are inspected after shell-only activation. A timed-out startup is recovered by
detached launch; Niri, GUI settings, outputs, protected files and original recovery records remain
unchanged. Temporary sudo credentials are removed. Physical input acceptance remains pending.

Native-style power-menu refinement **Implemented; controller behavior, native comparison,
installation and zero-change reapplication Tested**. Match the original horizontal icon tiles, number badges
and attached placement, retaining the confirmation behavior below. The native preview passes
63 tasks/eight temporary changes, and the ownership fixture passes 69 tasks with zero changes and
seven expected refusals. Clean f1a28b1 preview proposes two changes; installation passes 407 tasks/five
changes, installed verification 63 tasks/zero changes and reapplication 407 tasks/zero changes.
Live inspection catches cached old geometry after config-reload; a Noctalia-only restart activates
the correct row. Niri/application windows, GUI state, display settings, all 76 protected resources
and all 92 recovery manifests/five original backups remain unchanged. Only two applied receipts
change; no pending markers remain and the temporary sudo credential is removed.
See the [comparison and activation evidence](desktop-test-results.md#native-style-power-menu).

Power confirmation **Implemented; native validation/rendering, deployment and reload Tested**: the
[Qubix power panel](../architecture/desktop-design.md#power-action-countdown) requires a three-second
number-key hold with early-release cancellation, or a cancellable five-second click countdown.
Controller Luau fixtures pass repeat/overlap/mixed-input/lifecycle/locking/stall/dispatch controls;
desktop ownership/version fixtures pass 69 tasks in both normal/check mode, zero changes and seven expected refusals each.
Clean d415856 native preview passes 63 tasks/eight temporary changes; deployment preview passes
323 tasks/six proposed changes. Desktop-only installation passes 410 tasks/16 changes; installed
verification passes 63 tasks/zero changes and identical reapplication passes 407 tasks/zero changes.
Live reload returns ok, with the installed panel visible, unchanged Niri/Noctalia PIDs, GUI state,
100% output scale, all 76 protected resources and all 90 earlier manifests/five original backups.
No pending markers remain; the temporary sudo password file is removed. See the
[deployment evidence](desktop-test-results.md#power-confirmation-deployment).
No real power action or boot check ran. Next: operator checks of early-release and click/Escape
cancellation; the Control Center retains its separate native tap countdown.

Subtle Plymouth wordmark refinement **Implemented; local asset validation Tested**: smaller/lower original-colour logo and
steel-blue lettering with a wider gap; native installation and visual acceptance pending.
Startup fallback repair **Implemented and normal startup Tested**: the operator reported a blank screen followed by the
three-square text fallback on the current revision. SSH through Tailscale confirms Theme=qubix;
simpledrm is ready at 1.38 s, Plymouth starts at 1.57 s and amdgpu is ready at 7.95 s.
Prior archive/service health alone did not establish graphical startup acceptance. The focused
[early graphics repair](../components/plymouth.md#early-graphics-repair) retains separate source,
installation and console gates.
The generator fixture passes 521 tasks/ten expected refusals, schema/discovery 492 tasks/zero
changes, global check-mode control 51 tasks and Limine lifecycle/recovery 771 tasks. Native
activation from clean 0324e27, production installed verification and exact four-image/font/DRM/pin
checks now pass. Reapplication passes 1607 tasks with zero managed changes; its two changes save
local evidence and stop the temporary inhibitor. Both image generators and font-cache refresh
are skipped. All 86 earlier manifests/five original backup files, 21 native boot files, 45
protected configuration/font files and 11 earlier owned boot files remain unchanged; only two
new stages and their absence records are added. Pending markers are absent. The same boot ID,
Niri PID 15607 and Noctalia PID 15697 remain, with eDP-1 at 1920x1080/100% scale. SSH/SDDM are active,
the inhibitor is inactive and native authentication failure records are empty. These are preboot
checks. The operator subsequently confirms the Qubix splash appears and the desktop returns after
the requested normal reboot. No post-reboot SSH preservation audit is claimed for this repair.

The physical CachyOS Niri desktop is deployed and returns after reboot at 100% scale with the slim
information bar. The native-style Plymouth and active Limine image adapter are deployed from clean e3bf16b.
Exact active-image/font checks, installed verification and zero-change reapplication pass. A normal-kernel
reboot returns the desktop. Following feedback on 87e824b, the higher-contrast correction removes
decorative captions, reduces menu text and reuses the desktop cube wallpaper. It is deployed and
native-preview/image/reapplication/reboot Tested; renewed console acceptance remains open.
The first Plymouth activation failed visual acceptance and is not counted as a successful boot theme.
The operator rejects the blue Plymouth logo tint and requests a background. The original-colour logo
and native scaled desktop-cube background correction is deployed from clean e3bf16b;
exact image checks and zero-change reapplication pass. The logo crop matches a canonical render pixel-for-pixel.
All-mode/native Pango/FreeType picture/prompt previews pass 50 tasks with host preservation and
cleanup. Generator fixtures pass 409 tasks/five expected refusals; global check-mode control passes
45 tasks without image generation. Deployment passes 1637 tasks/23 changes, installed verification
passes 300 tasks/zero changes and identical reapplication passes 1591 tasks/zero changes. Both image
rebuilds and font-cache refresh are skipped on reapplication. Renewed console acceptance remains pending.

The guarded 16:38 EDT reboot returns with boot ID 2305848b-690c-49bc-bee1-a5ba893c38a5,
unchanged 7.2.9-2-cachyos/arguments and native Limine 12.9.3 entry. SSH/SDDM and Plymouth start/quit
succeed; Qubix Niri/Noctalia return with bar/wallpaper, no dock and 100% scale. All 86 manifests,
76 tracked resources, 11 owned boot assets and fonts match the preboot audit. Original recovery
bytes/metadata and active configuration remain unchanged; only native loader/random-seed rotates.
Pending markers and the temporary inhibitor are absent. The prior journal records reboot-splash
startup but does not retain a completion message; its appearance still needs console confirmation.

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
| Login | Noctalia Greeter theme/UI/install/reapplication Tested; next-boot greetd selected with consent, current SDDM active; physical authentication/restore pending |
| GRUB | Preservation/dispatch/reapplication/recovery fixtures Tested; independent native boot/restore pending |
| Limine | Refined graphical fixture passes 726 tasks/eight expected refusals; native normal-kernel reboot and protected entry/argument/snapshot bytes verified; earlier appearance confirmed, current contrast acceptance pending |
| Plymouth | Early graphics repair deployed from 0324e27; exact four-image/font/DRM/pin checks, preservation and unchanged reapplication pass; operator confirms repaired startup and desktop return; poweroff/LTS/recovery remain open |
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
clean f626188 deployment passes 1617 tasks/84 changes, installed verification passes 298 tasks/zero
changes, and identical reapplication passes 1572 tasks/zero changes. Both generators and font-cache
refresh are skipped on reapplication. Four-image extraction verifies 38 runtime assets and three exact
font copies per image; both pins match. All 81 earlier manifests and all 19 native boot files remain
unchanged; only two original-absence records for the new stages are added. The preboot audit confirms
83 private manifests, unchanged protected Limine bytes, preserved original recovery bytes and no
pending markers. The first activation attempt stopped at SSH authentication before writes; the
refreshed-connection retry is the completed result above. Renewed console acceptance remains open.

The 15:32 EDT guarded reboot returns with boot ID 8301a46f-e336-47cb-af51-9dbeb679c839,
unchanged normal kernel/arguments and native Limine entry. SSH/SDDM, Plymouth start/quit and the prior
reboot-screen service succeed. Qubix Niri/Noctalia return with bar/wallpaper, no dock and 100% scale.
All 83 manifests, 76 tracked resources, nine owned boot assets and fonts match the preboot audit;
original recovery bytes/metadata and active config are unchanged. Only loader/random-seed rotates
among native boot files. Pending markers and the temporary target inhibitor are absent.

## Limits and next gate

- Obtain console acceptance of the original-colour Plymouth logo/background and current Limine menu; retain native prompt behavior.
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
