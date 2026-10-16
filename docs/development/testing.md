# Testing strategy

Status: **Implemented local checks and GitHub Actions workflow**. Run `./scripts/validate.sh` for all static checks and `./scripts/test.sh` for normal/check-mode fixtures. The scripts prefer `.venv/bin` and keep controller caches in `.cache/`. GitHub Actions runs the same scripts on Ubuntu/Python 3.13 with locked tools; the remote workflow has not run during bootstrap.

Equivalent individual commands, with the virtual environment active:

```bash
mkdir -p .cache/tests
yamllint .
ANSIBLE_HOME="$PWD/.cache/ansible" ansible-lint --offline playbooks roles tests/playbooks tests/tasks
ansible-playbook playbooks/verify.yml --syntax-check
ansible-playbook playbooks/deploy.yml --syntax-check
ansible-playbook tests/playbooks/framework.yml --syntax-check
shellcheck bootstrap.sh scripts/*.sh
python3 tests/static/check_repository.py
ansible-playbook tests/playbooks/framework.yml
ansible-playbook tests/playbooks/framework.yml --check
ansible-playbook tests/playbooks/branding.yml
ansible-playbook tests/playbooks/branding.yml --check
```

The output-default shell fixture uses real jq with a fake Niri transport to cover startup, new outputs, reconnects, disabled screens, preserved manual scale, explicit once activation and invalid input. No real display is changed by that fixture.

The power-panel fixture runs the actual Luau entry in a no-effect host with mocked input, frame,
UI and dispatch APIs. Run `.venv/bin/python tests/static/check_power.py` using the
[controller-only Luau prerequisite](environment.md); it also runs in `scripts/test.sh` and CI.
It verifies early release for every key, complete holds, repeats, overlapping keys, click countdowns,
mixed input, close/reopen, disabled locking, stalled frames and exactly-once native IPC dispatch.
No real session/power command executes. These fixtures do not prove native event delivery or rendering.

The suite exercises 25 profile, 11 host, seven exact-identity cases and evidence normalization, with zero changes. Expected failures are rescued only when the matching diagnostic appears. macOS `./bootstrap.sh verify` rejects the real controller as unsupported with zero changes. In a restricted sandbox Ansible local RPC may require execution approval; fixtures do not deploy to the host.

Basic Markdown checks validate local links, fences, final newlines and whitespace. Consistency checks require schema, profile and authoritative documented defaults to agree and boot/splash to remain opt-in. No privileged deployment belongs in CI.

Meaningful fixture tests must exercise discovery classification, profile merging, invalid profile/options/types, unsupported platforms, missing Niri/Pacman, and unsupported enabled combinations. Tests may inject evidence into classification task files, but production discovery must read the host. Fictional fixture facts cannot establish real host compatibility.

Branding tests create a temporary root under `.cache/tests/`, override destination/ownership to that root/current user, then guarantee cleanup. Normal mode proves exact installed bytes/modes, zero directory/copy changes on reapplication, repair, unowned-file preservation, damaged/missing diagnostics, and namespace/file symlink rejection. Check mode intentionally creates/cleans the fixture root but asserts the proposed branding destination remains absent. Fixture setup/cleanup changes are expected; they do not represent a host deployment. Static checks also verify every imported source checksum against its provenance manifest. No fixtures deploy to `/boot`, a real `/etc`, or personal dotfiles.

Pending native integration matrix: CachyOS Niri session; login; GRUB; Limine; Plymouth+dracut; Plymouth+mkinitcpio; idempotency; preserved configuration; revision tracking; restoration and interrupted deployment. Each boot combination requires a disposable VM reboot and recovery test.

Record exact commands and outcomes in [status](../project/status.md). Broaden tests when failures or changed assumptions justify it. File installation, parsing, graphical verification, and boot acceptance are separate results.

Additional isolated fixtures cover baselines/drift/repeated restore/validator failure/pending state, desktop definitions/Noctalia version gates, SDDM cloning/standalone activity/ambiguity, independent GRUB/Limine preservation/private-mode/reapplication/file restoration, both fake generators, incomplete archives, rebuild skipping, kernel-aware restore and no-write splash preview. Shell fixtures verify explicit/user/default Starship precedence without changing HOME or personal files. The [developer guide](getting-started.md) lists focused runs; fake tools never prove native generation or boot success.

Wrapper fixtures reject normal and compact deploy/restore tag options before Ansible invocation. Native private login/boot/splash checks require read-only privilege escalation; existing activation-file modes are retained.

Run native grammar checks explicitly with `ansible-playbook tests/integration/niri.yml -i INVENTORY --ask-pass`; add `-e '{"qubix_discovery_privileged": true}' --ask-become-pass` if boot metadata is private. CI syntax/lint checks this playbook but never runs it against a host. It uses the production render task file, checks invalid controls, validates Niri plus installed Foot/Noctalia candidates and removes its private temporary files. Missing companions are skipped here, but deployment requires them. It does not prove companion startup or a graphical session.

## Native desktop smoke test

The optional tests/integration/desktop.yml workflow tests rendered production candidates inside an existing main Niri compositor, supporting direct SDDM and user-service launches. It requires measured Noctalia/Foot/jq, Python, dbus-run-session, notify-send and dbus-send; standard-library Python helpers are test-only. It copies candidates with temporary path substitutions, opens a nested window on a private D-Bus session without --session/global environment import, and keeps HOME/config/state/data/cache temporary. Test-only overrides disable Polkit, clipboard collection, locking and network requests. It checks Noctalia wallpaper/bar layers and dock absence, two distinctly titled Foot windows and focus/title screenshots in a test-owned preview window expanded to the available width, 100% private output scale, IPC focus navigation, width/height changes and automatic height reset using the candidate's actual resize actions, the notification bus owner's process identity, notification rendering, launcher and notification centre IPC, the Power options desktop-entry command opening the session menu, global reboot search and /session results without executing any power action, and the local shortcut panel's manifest, open/search/close behaviour and screenshots. Desktop-file validation runs when the native validator is installed; its availability is recorded. Screenshots/logs stay in ignored .cache/native-desktop/.

Acceptance requires successful native rendering, unchanged original compositor PID/session endpoints and cleanup of test processes/files. The workflow must fail when the main compositor/socket is unavailable; it never starts or replaces the main session. Native Niri/Noctalia/dconf and Qubix-only GUI settings hashes must remain unchanged. Cleanup targets only the temporary compositor process group and its distinct socket. The test does not prove physical key events, login, portals, Polkit, lock/unlock or reboot behaviour. Run it explicitly when evaluating a candidate; a visible temporary window is expected. Installed-resource verification remains a separate bootstrap.sh verify --tags installed command. Syntax checks alone do not establish these results.

The power-menu entry now opens `qubix/power:menu`; native lint checks both local plugin manifests.
The preview opens and captures that panel and the original native session menu as a visual reference,
without activating a power action. Lock entries are disabled/hidden respectively in the private test.
An unprivileged visual-only run may limit `qubix_discovery_evidence_paths` to desktop candidates;
that run does not inspect private boot metadata. Native Control Center
countdowns and physical hold/release cancellation require separate operator checks before acceptance.

## Native splash preview

Run tests/integration/plymouth.yml explicitly using the [splash guide](../user/plymouth.md).
It checks the native two-step plugin against an invalid-module control, captures three animated
modes and a synthetic password prompt. A private bubblewrap namespace, pseudoterminal and Xwayland
server isolate daemon IPC and devices. A reader drains early tty debug output. Verify actual
plugin mappings, clean daemon exits, unchanged host selection/session and zero leftover processes.
The refined preview binds its exact Qubix Boot Mono subset in a private font tree, checks the native
font resolver and records the selected SHA256. It preserves native host fonts and uses a private
fontconfig cache. Pango renders all three modes; a separate namespace substitutes the installed
FreeType label implementation for its boot/password control, matching the packaged early-boot font
path without replacing host plugins. Re-export checksums with Inkscape 1.4.3 match across all 38 PNGs.
Optional font/art tools and regeneration are documented under [boot assets](../../assets/boot/README.md)
and [font assets](../../assets/fonts/README.md); they are not target or ordinary CI dependencies.
Logs/screenshots remain ignored. Review spinner, watermark and prompt captures manually; this test
does not prove native initramfs packaging, firmware graphics, encrypted-root input or actual shutdown.

The Limine image fixtures run with `ansible-playbook tests/playbooks/limine-plymouth.yml` and
`ansible-playbook tests/playbooks/limine-bindings.yml` (also `--check`). They exercise two independently
bound sources, indented native submenu entries, staged bytes/pins, original cache/snapshot
preservation, reapplication, actual referenced archive dispatch, config-first recovery and force
refusal after cached image/kernel drift. Smaller controls cover missing/duplicate/wrong bindings,
no persistent preview state, compatible appearance-baseline alias enrollment and FAT permission
planning. Their fake generators/digest tools inspect only disposable roots; native boot remains
separate. Shared CI invokes these through scripts/test.sh with a 30-minute job timeout.

The graphical fixture also seeds the exact earlier 15-key recovery contract, tests font/help
ownership enrollment, retains unknown original metadata fields and checks exact restoration.
Stale originals/receipts and new directives outside Qubix ownership must fail. Run
`ansible-playbook tests/playbooks/limine-font-preview.yml --check` for the independent global
check-mode no-metadata-write control; invoking a normal playbook task with check_mode alone does
not change Ansible's global ansible_check_mode flag used by orchestration guards.
