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

These counts describe the runs at the revisions above; later task additions can change task counts. For the complete repeatable command lines, use the [operator guide](../user/getting-started.md) and [developer test guide](../development/getting-started.md).

## Preservation, recovery and rendering evidence

The audit records SHA-256, presence, UID/GID/mode, symlink destinations and the account's shell. All 76 audited resources match the post-package baseline after deployment, reapplication and restoration. These include native/personal Niri, Noctalia, Alacritty, Fish/other dotfiles, session definitions, distribution identity, PAM, SDDM, generator configuration, kernel/initramfs files and Limine configuration. The native package-hook change is reported separately above.

Seventeen root-owned 0600 baseline manifests in private storage record original absence. Their hashes remain unchanged across reapplication/restoration; pending state clears after success. Live recovery proves removal of newly installed named files. Original-byte restoration, drift and fault handling are also covered by isolated fixtures; live boot/image recovery is still pending. Packages, retained backups and empty/unlisted directories survive file restoration.

The nested workflow uses a private D-Bus session and temporary HOME/config/cache paths, without --session. It checks wallpaper/bar layers, two Foot windows, Fuzzel's rendered layer, a notification received by Mako, and focus movement through Niri IPC. Screenshots were inspected. The original Niri service PID/session endpoints remain unchanged, and the final helper reports zero remaining test processes. Temporary remote artifacts are removed; evidence stays in ignored .cache/native-desktop/ on the controller. Screenshots and logs are not published in Git.

## Remaining acceptance

The operator still needs to select Qubix Niri as the main session and verify physical shortcuts, native default-shell startup, application launching, portals, lock/unlock and GUI privilege prompts. Nested rendering is a development smoke test. Deployment state deliberately keeps graphical_session_verified and boot_verified false.

Breeze and the optional KDE Polkit agent are absent on this machine. Login branding remains disabled. Supported login authentication/restoration, independent GRUB and Limine boots/restoration, and real Plymouth generation/splash/recovery with both dracut and mkinitcpio need disposable VMs. Both loaders and both generators remain mandatory MVP gates; no release acceptance is claimed. See [scope](scope.md) and [backlog](backlog.md).
