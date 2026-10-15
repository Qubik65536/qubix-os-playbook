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

The active main session is native CachyOS Niri/Noctalia. Saved Qubix GUI preferences contain no bar/theme/plugin overrides. Log out and select **Qubix Niri** to use the refinements; the native session remains available. Primary-session acceptance and native restoration of the newer Noctalia resources remain open. Login, bootloader and Plymouth components remained disabled; no reboot was needed for this deployment. Evidence stays in ignored .cache/native-desktop/ and the local refinement logs/audit.
