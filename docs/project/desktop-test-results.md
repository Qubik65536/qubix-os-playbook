# Native desktop test results

Date: 2026-10-14. Status: **Desktop file lifecycle and isolated nested rendering Tested; primary-session and full MVP acceptance In Progress.** The operator authorized six desktop packages, their normal native hooks, and branding/Niri/shell deployment and recovery on a physical CachyOS test machine.

## Tested environment

The controller uses macOS, Python 3.13 and pinned Ansible 2.21.5. The target runs CachyOS/Linux/systemd, kernel 7.2.9-2-cachyos, Niri 26.04, native Noctalia 5.2.1/Alacritty 0.17.0 and the existing default Fish shell. SDDM 0.21.0, firmware-identified Limine 12.9.3 and mkinitcpio 42.2 were inspected; their Qubix components stayed disabled.

| Installed desktop package | Tested version |
|---|---|
| Foot | 1.28.0-2.1 |
| Fuzzel | 1.15.0-1.1 |
| Waybar | 0.15.0-3.1 |
| Mako | 1.11.0-1.1 |
| Swaybg | 1.2.2-1.1 |
| Starship | 1.26.0-1 |

Pacman installed these plus 17 dependencies after matching the preview: 23 new packages, 13.48 MiB download. The command was `sudo pacman -S --needed foot fuzzel waybar mako swaybg starship`; no database refresh or system upgrade was requested. Native Snapper/Limine hooks refreshed snapshot menu content in limine.conf. The other 75 audited resources and all kernel/initramfs hashes remained unchanged. Qubix subsequently preserved the post-package Limine configuration.

Initial desktop file lifecycle used revision cf54072. The reusable native smoke workflow was committed as 28cc112; stale boot restoration refusal was committed as 6a10daa. Those test/recovery changes do not change desktop resource bytes. Final deployment records its actual checkout revision, configuration digest and dirty flag in private state.

## Commands and actual outcomes

Controller commands used an ignored inventory/configuration, strict confirmed host-key checking, SSH pipelining and interactive `--ask-pass --ask-become-pass`. Configuration enabled branding/Niri/shell only, preserved user configuration/default shell, and explicitly permitted private /boot metadata reads.

| Operation | Result |
|---|---|
| `bootstrap.sh deploy --check --diff` | 280 tasks; 17 proposed changes; no failures; no baseline/state writes |
| `tests/integration/niri.yml` | 62 tasks; eight temporary setup/cleanup changes; Niri/Foot/Fuzzel accept production definitions and reject invalid controls |
| `bootstrap.sh deploy` | 373 tasks; 58 file/directory/baseline/receipt/state changes; no failures |
| `bootstrap.sh verify --tags installed` | 58 tasks; zero changes/failures; expected hashes/modes and native Niri syntax |
| Same-revision/configuration deployment | 352 tasks; zero changes/failures, including final revision state |
| `tests/integration/desktop.yml` | 64 tasks; five temporary test/evidence/cleanup changes; no failures |
| Native Bash/Starship probe | Interactive initialization, TOML parsing and prompt rendering pass using a temporary home |
| `bootstrap.sh restore --check --diff` | 248 tasks; 17 proposed removals; no failures |
| `bootstrap.sh restore` | 249 tasks; 18 changes; all 17 originally absent resources removed; state records restored |
| Final desktop redeployment from `3bc4851` | 352 tasks; 18 changes; managed resources restored; installed verification passes with 58 tasks and zero changes/failures |
| Reapplication before authorized reboot | 352 tasks; zero changes/failures; installed verification again passes with 58 tasks and zero changes/failures |
| Operator-authorized `sudo systemctl reboot` | Changed boot ID confirms restart; SSH and native SDDM return active; Qubix session entry remains available and installed Niri validation passes |

These counts describe the runs at the revisions above; later task additions can change task counts. For the complete repeatable command lines, use the [operator guide](../user/getting-started.md) and [developer test guide](../development/getting-started.md).

## Preservation, recovery and rendering evidence

The audit records SHA-256, presence, UID/GID/mode, symlink destinations and the account's shell. All 76 audited resources match the post-package baseline after deployment, reapplication and restoration. These include native/personal Niri, Noctalia, Alacritty, Fish/other dotfiles, session definitions, distribution identity, PAM, SDDM, generator configuration, kernel/initramfs files and Limine configuration. The native package-hook change is reported separately above.

Seventeen root-owned 0600 baseline manifests in private storage record original absence. Their hashes remain unchanged across reapplication/restoration; pending state clears after success. Live recovery proves removal of newly installed named files. Original-byte restoration, drift and fault handling are also covered by isolated fixtures; live boot/image recovery is still pending. Packages, retained backups and empty/unlisted directories survive file restoration.

The nested workflow uses a private D-Bus session and temporary HOME/config/cache paths, without --session. It checks wallpaper/bar layers, two Foot windows, Fuzzel's rendered layer, a notification received by Mako, and focus movement through Niri IPC. Screenshots were inspected. The original Niri service PID/session endpoints remain unchanged, and the final helper reports zero remaining test processes. Temporary remote artifacts are removed; evidence stays in ignored .cache/native-desktop/ on the controller. Screenshots and logs are not published in Git.

## Remaining acceptance

After the authorized reboot, no Niri user service was running at the time of inspection. The operator still needs to select Qubix Niri as the main session and verify physical shortcuts, native default-shell startup, application launching, portals, lock/unlock and GUI privilege prompts. SDDM being active does not prove greeter rendering or successful authentication. The restart used the existing boot configuration with Qubix login/bootloader/Plymouth components disabled; it does not establish their acceptance. Nested rendering is a development smoke test. Deployment state deliberately keeps graphical_session_verified and boot_verified false.

Breeze and the optional KDE Polkit agent are absent on this machine. Login branding remains disabled. Supported login authentication/restoration, independent GRUB and Limine boots/restoration, and real Plymouth generation/splash/recovery with both dracut and mkinitcpio need disposable VMs. Both loaders and both generators remain mandatory MVP gates; no release acceptance is claimed. See [scope](scope.md) and [backlog](backlog.md).

## Noctalia redesign

The accepted [desktop design](../architecture/desktop-design.md) replaces the classic companions with the installed standalone Noctalia 5.2.1. It retains Niri and Foot, uses #56728b as the shell/compositor accent, adds clipped 16 px windows, rounded floating bar/panels/dock and DMS/macOS-inspired shortcuts. Native personal settings remain preserved; application theme generation is disabled and Noctalia's automatic GSettings write is transient.

The native grammar workflow passes: 63 tasks, eight private setup/cleanup changes, zero failures. The final candidates are checked before activation. Noctalia reports unknown sections as warnings with exit zero, so the negative control uses an invalid typed setting and the positive control rejects schema warnings.

The revised candidate-rendering workflow passes: 59 tasks, eight private setup/test/evidence/cleanup changes, zero failures. It supports the actual direct SDDM Niri launch. Noctalia bar/dock/wallpaper, two Foot windows, launcher, received notifications and notification centre render; IPC changes focus and confirms the Qubix palette/wallpaper. Screenshots were inspected after correcting the palette's required terminal fields; a selected custom palette name alone had allowed a fallback to built-in colours. The startup hotkey overlay is suppressed.

The original compositor PID/session environment and native Niri/Noctalia/dconf hashes remain unchanged. Cleanup leaves zero test processes. The profile-launcher shell fixture verifies transient GSettings use and restoration of default/explicit backends for application launches. Desktop fixtures pass 58 tasks with zero changes and six expected dependency/version refusals. Framework normal mode passes 459 tasks, zero changes and 26 expected refusals. Static checks pass.

The new desktop was then deployed from clean revision 4dc23f6: 343 tasks, 16 file/directory/baseline/receipt/state changes, zero failures. Same-revision reapplication passes with 338 tasks and zero changes/failures. Installed verification passes with 62 tasks and zero changes/failures, including native Niri/Noctalia parsers.

The post-deployment audit matches all 76 native/personal resources to the post-package baseline, including kernel/initramfs/boot settings and the original Fish shell. All 17 earlier baseline hashes remain intact; three new Noctalia palette/config/launcher baselines bring the private manifest count to 20. Pending state clears; deployment state records the clean source revision and files-verified status, retaining false graphical/boot acceptance flags. Legacy Qubix companion files remain inert and retain their original backup records.

The operator-authorized reboot after this deployment also succeeds: a new boot ID is observed, SSH/native SDDM return active, both installed parsers pass and the Qubix session entry is available. No user desktop process was running at inspection, leaving session selection to the operator. Qubix login/bootloader/Plymouth remained disabled throughout.

These results establish syntax, nested appearance and actual system-file deployment/idempotency. Physical shortcuts, launcher application startup, GUI authentication, lock/unlock and portals need primary-session acceptance after the operator selects the updated session. Restoration of the three new Noctalia resources remains a native recovery acceptance item; the shared first-baseline engine is covered by fixtures and the earlier classic lifecycle.

## Bar and shortcut-panel refinement

Clean source revision 6bb163c adds separate rounded widget capsules and a searchable local Noctalia shortcut panel, opened with the bar keyboard button or Super+Shift+/. Its three managed files contain the manifest, Luau presenter and JSON generated from labelled KDL bindings. Super+F1 retains Niri's compact overlay. No additional packages or services were installed.

| Check | Actual outcome |
|---|---|
| scripts/validate.sh | YAML/Ansible/ShellCheck, all syntax checks and repository consistency pass |
| tests/playbooks/desktop.yml | 62 tasks, zero changes/failures; six expected dependency/version refusals; generated binding data covers labelled KDL |
| tests/integration/desktop.yml | 62 tasks, eight temporary changes, zero failures; manifest lint and panel open/search/close pass |
| bootstrap.sh deploy | 395 tasks, 15 changes, zero failures |
| Same-revision/configuration reapplication | 391 tasks, zero changes/failures |
| bootstrap.sh verify --tags installed | 64 tasks, zero changes/failures; hashes/modes and installed native validators pass |

The native screenshots were inspected: separate floating bar pills, two-column category cards, keycaps, bounded scrolling with a visible footer, and a search that filters 41 grouped actions to the launcher entry. The initial preview caught unbounded content; the final presenter gives the scroll viewport the remaining panel height. Search is exercised through the same callback used by the input. Physical keystrokes and pointer dismissal still require operator testing.

The main native Niri/Noctalia process IDs and preview configuration/session checks remain preserved; cleanup leaves zero test processes. A post-deployment audit matches all 76 native/personal resources and the default Fish shell to the pre-deployment snapshot. All 20 earlier baseline hashes remain intact; the three new private manifests bring the total to 23. State records clean revision 6bb163c, files-verified and no pending attempt, with graphical/boot acceptance flags still false.

During this deployment the active main session was native CachyOS Niri/Noctalia. Saved Qubix GUI preferences contained no bar/theme/plugin overrides. Log out and select **Qubix Niri** to use the refinements; the native session remains available. Primary-session acceptance and native restoration of the newer Noctalia resources remain open. Login, bootloader and Plymouth components remained disabled; no reboot was needed for this deployment. Evidence stays in ignored .cache/native-desktop/ and the local refinement logs/audit.

## Native session retirement and primary startup

The operator then explicitly requested reboot and permitted removal of CachyOS's default Niri. This is a target-specific exception to normal native-entry preservation, outside deploy/restore reconciliation. An inspected, guarded Ansible host operation passed 14 tasks with three changes: private backup directory, exact native-entry backup, and removal of /usr/share/wayland-sessions/niri.desktop. The Niri compositor package 26.04-1.1 remains installed and required by Qubix; personal configuration remains intact.

The native entry is recoverable from /var/lib/qubix/retired-sessions/niri.desktop, root-owned mode 0600 inside a root-owned 0700 directory. Its SHA-256 matches the original entry. All four configured SDDM session directories were inspected; qubix-niri.desktop is the sole remaining entry. The [recovery procedure](live-test-plan.md#operator-authorized-native-session-retirement-and-reboot) restores the native entry before any Qubix file restoration; package upgrades may recreate it.

The requested sudo systemctl reboot completed. A changed boot ID confirms restart, and SSH/SDDM return active under the same pinned SSH host key. Installed Niri and Noctalia validators pass after reboot; the installed shortcut plugin reports zero errors/warnings. The main user session now runs Niri with --session --config /etc/niri/qubix/config.kdl and Noctalia with NOCTALIA_CONFIG_HOME=/etc/qubix. Read-only IPC confirms a visible bar, custom Qubix palette and Noctalia wallpaper/bar/dock layers on eDP-1. This establishes primary-session startup, not complete interaction acceptance.

The 76-resource audit shows exactly one intentional change: removal of the native session entry. The other 75 native/personal resources, default Fish shell and all 23 existing private baseline hashes remain unchanged. The retirement backup is separate from those managed baselines. No pending deployment remains. Login authentication settings, bootloader configuration and initramfs images were not modified.

No autologin was configured. Physical shortcut handling, launcher applications, portals, GUI authentication, lock/unlock and native restoration of the newer Noctalia resources remain acceptance items. Deployment state still retains false graphical/boot acceptance flags. Local evidence is ignored under .cache/native-session-retirement-audit.json and the retirement log.

## Resize, power controls and compact bar

Clean source revision bbea600 deploys the compact #56728b bar, disabled dock/bottom reservation, pinned Power options application and global Session launcher search. It includes the resize bindings from 79175a3 and the [README cheatsheet regeneration guide](../../README.md#regenerate-the-shortcut-cheatsheet) from 4c99994. No additional packages were required.

| Check | Actual outcome |
|---|---|
| scripts/validate.sh | YAML/Ansible/ShellCheck, syntax, Markdown/local links and repository consistency pass |
| tests/playbooks/desktop.yml | 62 tasks, zero changes/failures, six expected dependency/version refusals; every managed binding is represented in generated shortcut data |
| tests/integration/desktop.yml | 62 tasks, eight temporary changes, zero failures; native sizing, power-menu/search and dock-absence checks pass |
| bootstrap.sh deploy | 409 tasks, 10 changes, zero failures |
| Same-revision/configuration reapplication | 408 tasks, zero changes/failures |
| bootstrap.sh verify --tags installed | 64 tasks, zero changes/failures; installed hashes/modes and parsers pass |
| Active-session config-reload | Returns ok; Qubix bar/wallpaper remain visible and no dock layer remains on eDP-1 |

The isolated preview invokes the actual resize actions parsed from the candidate KDL. Column width grows from 438 to 483 logical pixels and also decreases; stacked-window height grows from 386 to 407 and also decreases; automatic height reset succeeds. The screenshot of the filtered cheatsheet includes the four resize actions with arrow/HJKL aliases. The full generated list has 46 grouped actions.

Inspected screenshots show compact separate bar modules without a dock, Power options pinned first in the launcher, a global reboot search result, /session results and the native session menu. The test runs the candidate desktop entry's actual command to open that menu. It never activates a power action; test-only locking is disabled, so action availability differs from production. Native desktop-file validation and warning-free Noctalia TOML validation pass.

The deployed defaults were reloaded in the existing Qubix primary session. Niri PID 931, Noctalia PID 1002 and the boot ID remain unchanged through activation and reapplication; no reboot or session restart was needed. Read-only IPC confirms the custom Qubix palette, visible bar and wallpaper, and dock absence. The installed Niri, Noctalia and Power options entry pass their native validators.

The fresh post-deployment audit matches all 76 native/personal resource snapshots, including the intentionally absent retired native login entry. The default Fish shell, retirement backup and all 23 existing private baseline hashes remain unchanged. The new power entry brings private baseline manifests to 24. State records clean revision bbea600, files-verified and no pending attempt; graphical_session_verified and boot_verified remain false.

Physical shortcut handling, actual launcher application/power actions, portals, GUI authentication, lock/unlock and native recovery of the newer Noctalia resources remain operator acceptance items. Login, bootloader and Plymouth components stayed disabled. Local evidence remains ignored under .cache/native-desktop/, .cache/controls-*.log and .cache/controls-preservation-audit.json.

## Bar visibility and logo correction

Date: 2026-10-15. Clean source ce72276 corrects the undersized launcher image and understated module styling. Inspection found the previous compact settings installed in the running Qubix profile with no bar/widget GUI overrides. Noctalia 5.2's launcher image uses a 16 px base box; transparent artwork margins make the visible cube smaller.

The corrected launcher scale doubles the image box to 32 px while preserving the original attributed PNG. The transparent bar is 40 px high with 36 px modules, 12 px module radii, stronger #56728b outlines, opaque fills and wider separation. Before/after isolated screenshots were inspected and visibly show the larger cube and clearer boundaries. The native test preserves the parent compositor, native/personal settings and Qubix GUI preferences, with zero leftover test processes.

| Check | Actual outcome |
|---|---|
| scripts/validate.sh | All static checks pass |
| tests/playbooks/desktop.yml | 62 tasks, zero changes/failures, six expected refusals |
| tests/integration/desktop.yml | 62 tasks, eight temporary changes, zero failures; warning-free shell validation and rendering pass |
| bootstrap.sh deploy | 408 tasks, three changes, zero failures |
| Same-revision/configuration reapplication | 408 tasks, zero changes/failures |
| bootstrap.sh verify --tags installed | 64 tasks, zero changes/failures |

Active-profile config-reload returns ok and installed settings report the 32 px image box and stronger outline. The visible bar/wallpaper layers remain, the dock remains absent, and Niri PID 931, Noctalia PID 1002 and the boot ID are unchanged. This records live activation separately from the inspected isolated screenshots; complete physical interaction acceptance remains pending.

The final audit matches all 76 native/personal snapshots and all 24 private baseline hashes. The retired native-session backup and default Fish shell also remain unchanged. Deployment state records clean ce72276, files-verified and no pending attempt; graphical/boot acceptance flags remain false.

Read-only Limine inspection still finds the native boot():/limine-splash.png wallpaper and no Qubix marker. Only branding, Niri and shell are selected. The adapter's current heading/two-colour contract does not provide BlueBuild's graphical GRUB layout; richer Limine appearance remains recorded under F08. No boot configuration or initramfs resources changed.

Evidence is ignored under .cache/bar-logo-*.log, .cache/bar-logo-preservation-audit.json, .cache/bar-logo-before/ and .cache/native-desktop/.

## Slim information bar and 100% startup

The 32 px information bar and output-scale helper are deployed from clean 2645034. The controller
fixture passes 68 tasks with seven expected refusals and zero changes; the isolated native desktop
preview passes 62 tasks with eight temporary changes. It shows changing application titles and
CPU/RAM readings, optional media and no dock; unavailable temperature is displayed as --.

Desktop deployment passes 426 tasks with eight changes. Full configuration reapplication after the
separate initial Plymouth activation passes 571 tasks with zero changes. The guarded reboot returns
SSH/SDDM/Qubix with boot ID 802776ba-c8fe-4afa-8f7a-531d794868dc, Niri PID 1004 and Noctalia PID 1078.
Read-only IPC confirms eDP-1 at 1920x1080, scale 1.0, unchanged refresh/transform and a running startup
scale helper. Native monitor files and personal configurations remain preserved. This establishes
startup/scale and running shell layers, while physical interaction and newer-resource recovery remain
operator/VM acceptance. The [separate splash results](plymouth-test-plan.md#recorded-results) document
that boot-theme attempt's failed visual acceptance; it does not invalidate the desktop startup result.

## Power confirmation deployment

Date: 2026-10-16. Clean source d415856 supplies the
[guarded power panel](../architecture/desktop-design.md#power-action-countdown). The operator requested
SSH retry and deployment. After SSH authentication returned, a private controller-only sudo password
file enabled the authorized operation; it was removed after final verification. Only branding and
Niri were selected. Shell, login, bootloader and Plymouth components stayed disabled. No packages
were installed, images regenerated, or reboot/power actions invoked.

| Gate | Actual outcome |
|---|---|
| Native candidate parsing/rendering | 63 tasks, eight temporary test/evidence/cleanup changes, zero failures; both plugin manifests lint cleanly and Noctalia configuration has no schema warnings |
| Deployment preview | 323 tasks, six proposed desktop changes, zero failures; post-preview audit matches the entire pre-preview snapshot |
| File installation | 410 tasks, 16 changes, zero failures; six desktop resources updated/added with recovery receipts |
| Installed verification | 63 tasks, zero changes/failures; exact resource bytes/modes and native parsers pass |
| Same-source/configuration reapplication | 407 tasks, zero changes/failures |
| Primary-session activation | config-reload returns ok; IPC opens/captures/closes the installed panel without activating any entry |

The inspected nested screenshot shows all five options, countdown instructions, a progress track and
Cancel. Lock actions are disabled in that test-only session. The inspected primary screenshot shows
all five enabled, with legible instructions and no clipped controls. Native rendering is separate
from the no-effect controller tests of holds, repeats, early release, overlapping keys, mouse timers,
mixed input, closing/reopening, disabled locking and exactly-once dispatch. Physical input delivery
and cancellation still require operator acceptance; no real lock/logout/suspend/reboot/shutdown
action was used for verification. The Control Center's separate native menu retains tap-based countdowns.

Niri PID 1698, Noctalia PID 1764, boot ID 05705ba7-c596-4c52-9e12-e08050d84367, GUI-state hash and
output settings remain unchanged through reload and reapplication. eDP-1 remains 1920x1080 at scale
1.0; bar/wallpaper remain visible with no dock. The final power panel is closed. The nested test
preserves native configuration/compositor/environment and leaves zero test processes; its remote
temporary directory and the separate primary screenshot directory are removed.

All 76 protected native/personal resources, default Fish shell, retired-session backup, 90 earlier
baseline manifests and five original backup files remain unchanged. Only the four expected applied
receipts change; two new baseline manifests for the plugin files, plus their receipts, bring the total
to 92 baseline manifests.
The final audit matches the post-install snapshot exactly. Pending markers are absent; deployment
state records clean d415856, components branding/niri and files-verified, retaining false graphical
and boot acceptance flags. The source candidate's physical-input and recovery gates remain open.

Evidence remains ignored under .cache/tests/power-*.log, .cache/native-desktop/qubix-test/,
.cache/power-*.json and .cache/power-live.png. Local static validation passes after documenting results.
