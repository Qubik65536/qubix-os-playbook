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

Meaningful fixture tests must exercise discovery classification, profile merging, invalid profile/options/types, unsupported platforms, missing Niri/Pacman, and planned enabled components. Tests may inject evidence into classification task files, but production discovery must read the host. Fictional fixture facts cannot establish real host compatibility.

Branding tests create a temporary root under `.cache/tests/`, override destination/ownership to that root/current user, then guarantee cleanup. Normal mode proves exact installed bytes/modes, zero directory/copy changes on reapplication, repair, unowned-file preservation, damaged/missing diagnostics, and namespace/file symlink rejection. Check mode intentionally creates/cleans the fixture root but asserts the proposed branding destination remains absent. Fixture setup/cleanup changes are expected; they do not represent a host deployment. Static checks also verify every imported source checksum against its provenance manifest. No fixtures deploy to `/boot`, a real `/etc`, or personal dotfiles.

Future integration matrix: CachyOS Niri session; login; GRUB; Limine; Plymouth+dracut; Plymouth+mkinitcpio; idempotency; preserved configuration; revision tracking; restoration and interrupted deployment. Each boot combination requires a disposable VM reboot and recovery test.

Record exact commands and outcomes in [status](../project/status.md). Broaden tests when failures or changed assumptions justify it. File installation, parsing, graphical verification, and boot acceptance are separate results.
