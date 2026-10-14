# Testing strategy

Status: **Implemented local static and Ansible fixture checks; CI is Planned**. From the root with the virtual environment active:

```bash
yamllint .
ANSIBLE_HOME="$PWD/.cache/ansible" ansible-lint --offline playbooks roles tests/playbooks tests/tasks
ansible-playbook playbooks/verify.yml --syntax-check
ansible-playbook playbooks/deploy.yml --syntax-check
ansible-playbook tests/playbooks/framework.yml --syntax-check
shellcheck bootstrap.sh
ansible-playbook tests/playbooks/framework.yml
```

The suite exercises 22 profile, 11 host, seven exact-identity cases and evidence normalization, with zero changes. Expected failures are rescued only when the matching diagnostic appears. macOS `./bootstrap.sh verify` rejects the real controller as unsupported with zero changes. In a restricted sandbox Ansible local RPC may require execution approval; fixtures do not deploy to the host.

Basic Markdown/link and configuration consistency automation will accompany CI. No privileged deployment belongs in CI.

Meaningful fixture tests must exercise discovery classification, profile merging, invalid profile/options/types, unsupported platforms, missing Niri/Pacman, and planned enabled components. Tests may inject evidence into classification task files, but production discovery must read the host. Fictional fixture facts cannot establish real host compatibility.

Additive branding tests use a temporary filesystem, exact source/installed checksums, repeated application with zero changes, check-mode no-write evidence, and damaged/missing asset rejection. No fixtures point to `/boot`, a real `/etc`, or personal dotfiles.

Future integration matrix: CachyOS Niri session; login; GRUB; Limine; Plymouth+dracut; Plymouth+mkinitcpio; idempotency; preserved configuration; revision tracking; restoration and interrupted deployment. Each boot combination requires a disposable VM reboot and recovery test.

Record exact commands and outcomes in [status](../project/status.md). Broaden tests when failures or changed assumptions justify it. File installation, parsing, graphical verification, and boot acceptance are separate results.
