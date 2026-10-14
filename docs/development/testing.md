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

The suite exercises 25 profile, 11 host, seven exact-identity cases and evidence normalization, with zero changes. Expected failures are rescued only when the matching diagnostic appears. macOS `./bootstrap.sh verify` rejects the real controller as unsupported with zero changes. In a restricted sandbox Ansible local RPC may require execution approval; fixtures do not deploy to the host.

Basic Markdown checks validate local links, fences, final newlines and whitespace. Consistency checks require schema, profile and authoritative documented defaults to agree and boot/splash to remain opt-in. No privileged deployment belongs in CI.

Meaningful fixture tests must exercise discovery classification, profile merging, invalid profile/options/types, unsupported platforms, missing Niri/Pacman, and unsupported enabled combinations. Tests may inject evidence into classification task files, but production discovery must read the host. Fictional fixture facts cannot establish real host compatibility.

Branding tests create a temporary root under `.cache/tests/`, override destination/ownership to that root/current user, then guarantee cleanup. Normal mode proves exact installed bytes/modes, zero directory/copy changes on reapplication, repair, unowned-file preservation, damaged/missing diagnostics, and namespace/file symlink rejection. Check mode intentionally creates/cleans the fixture root but asserts the proposed branding destination remains absent. Fixture setup/cleanup changes are expected; they do not represent a host deployment. Static checks also verify every imported source checksum against its provenance manifest. No fixtures deploy to `/boot`, a real `/etc`, or personal dotfiles.

Pending native integration matrix: CachyOS Niri session; login; GRUB; Limine; Plymouth+dracut; Plymouth+mkinitcpio; idempotency; preserved configuration; revision tracking; restoration and interrupted deployment. Each boot combination requires a disposable VM reboot and recovery test.

Record exact commands and outcomes in [status](../project/status.md). Broaden tests when failures or changed assumptions justify it. File installation, parsing, graphical verification, and boot acceptance are separate results.

Additional isolated fixtures cover baselines/drift/repeated restore/validator failure/pending state, desktop definitions/optional agent, SDDM cloning/standalone activity/ambiguity, independent GRUB/Limine preservation/private-mode/reapplication/file restoration, both fake generators, incomplete archives, rebuild skipping, kernel-aware restore and no-write splash preview. Shell fixtures verify explicit/user/default Starship precedence without changing HOME or personal files. The [developer guide](getting-started.md) lists focused runs; fake tools never prove native generation or boot success.

Wrapper fixtures reject normal and compact deploy/restore tag options before Ansible invocation. Native private login/boot/splash checks require read-only privilege escalation; existing activation-file modes are retained.

Run native grammar checks explicitly with `ansible-playbook tests/integration/niri.yml -i INVENTORY --ask-pass`; add `-e '{"qubix_discovery_privileged": true}' --ask-become-pass` if boot metadata is private. CI syntax/lint checks this playbook but never runs it against a host. It uses the production render task file, checks invalid controls, validates Niri plus installed Foot/Fuzzel candidates and removes its private temporary files. Missing companions are skipped here, but deployment requires them. It does not prove companion startup or a graphical session.

## Native desktop smoke test

The optional tests/integration/desktop.yml workflow tests an already-deployed desktop inside an existing active Niri service. It requires the installed companions, Python, dbus-run-session, notify-send and makoctl; standard-library Python helpers are test-only. It opens a temporary nested window on a private D-Bus session, without --session or global environment import. Temporary HOME/config/cache paths preserve personal application state. It checks wallpaper/bar layers, two Foot windows, IPC focus navigation, a received Mako notification and Fuzzel rendering, then records screenshots/logs under .cache/native-desktop/ on the controller.

Acceptance requires successful native rendering, unchanged original compositor PID/session endpoints and cleanup of test processes/files. The workflow must fail when the original service/socket is unavailable; it never starts or replaces the main session. Cleanup targets only the temporary compositor process group and its distinct socket. The test does not prove physical key events, login, portals, Polkit, lock/unlock or reboot behaviour. Run it explicitly after desktop deployment; a visible temporary window is expected. Syntax checks alone do not establish these results.
