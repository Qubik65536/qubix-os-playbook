# Developer testing over SSH

SSH is a **developer testing transport**. Users run the playbook directly on their
CachyOS Niri machine; see [user onboarding](../user/getting-started.md). This guide
lets a Mac/Linux development controller exercise the same playbooks against an
explicitly authorized test VM. The controller holds source, Python tools, prepared
font cache and overrides; the VM receives resources over SSH and needs no checkout.

## Prepare the controller and test VM

Complete [developer setup](getting-started.md) and [tool prerequisites](environment.md).
Use a disposable CachyOS Niri VM, take a snapshot and keep hypervisor console access.
Prepare its native desktop prerequisites using [installation](../user/installation.md),
running those package commands at the VM console. Do not switch managers/loaders for branding.

At the VM console, prepare developer access explicitly:

```bash
sudo pacman -S --needed openssh
sudo systemctl enable --now sshd
ip -brief address
whoami
```

Enable SSH only on the test network. Native package hooks may refresh snapshots and
boot menus. Verify the host key before connecting; never disable host-key checking.
Create ignored `inventory/target.local.ini` on the controller:

```ini
[qubix_targets]
qubix-vm ansible_host=192.168.64.10 ansible_user=YOUR_VM_USER ansible_port=22
```

Replace the address/account. Test `ssh YOUR_VM_USER@192.168.64.10`. Keep passwords
out of inventory. Keys are convenient; password SSH uses `--ask-pass` on Ansible
commands. `--ask-become-pass` supplies the separate target sudo password.
See [developer access and evidence collection](ssh-access.md) for ports, aliases,
network failures and sanitized reports. Keep one VM per boot-test inventory.

## Inspect and prepare

Copy the [user deployment trial overrides](../user/deployment.md#prepare-and-configure-the-target)
into ignored controller `config/local.yml`, or provide a fully reviewed target-specific
configuration. Every remote command must pass the test inventory; the repository's
fallback is localhost, which must never receive a VM deployment by mistake.

```bash
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
.venv/bin/ansible-playbook -i inventory/target.local.ini -e @config/local.yml playbooks/prepare-packages.yml --check --ask-become-pass
.venv/bin/ansible-playbook -i inventory/target.local.ini -e @config/local.yml playbooks/prepare-packages.yml --ask-become-pass
.venv/bin/ansible-playbook playbooks/prepare-fonts.yml
```

For private /boot metadata set `qubix_discovery_privileged: true` outside `qubix`.
This permits privileged read-only inspection; it confirms no boot selection.
Full defaults also need login/UI/keyring preparation and explicit loader/generator
mappings; follow the component guides, replacing `inventory/local.ini` with the
remote test inventory in their Ansible commands. `prepare-fonts.yml` always prepares
source on the controller running Ansible. Package preparation installs Paru/Brew/WezTerm
and removes Alacritty/Foot; file restoration does not undo package transactions.

## Preview, apply and verify

```bash
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --tags installed --ask-become-pass
```

Add `--ask-pass` if required. Optional `ANSIBLE_PIPELINING=true` reduces round trips.
Repeat the exact source/configuration to measure idempotency. Check mode is an
approximation; file/grammar checks do not establish session, authentication or boot success.
Use the [native fixtures and limits](testing.md) and [acceptance checklist](../user/verification.md).
Do not infer physical interaction from SSH process/service observations. Keep native/personal
checksums, package versions, screenshots and source revision with each result.

Restore only after reviewing [recovery](../user/restoration.md):

```bash
./bootstrap.sh restore -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-become-pass
./bootstrap.sh restore -i inventory/target.local.ini -e @config/local.yml --ask-become-pass
```

## Interrupted remote tests

Wake the VM and recheck its address, sshd, firewall and network mode using the access
guide. DHCP changes may invalidate a controller allow rule. Keep pending markers and
the last-success receipt; reconnect and rerun the same source/configuration, then
complete installed verification and zero-change reapplication before reboot. An
unreachable run does not count as completed idempotency.

For brief network failures, `ANSIBLE_SSH_RETRIES=6` permits bounded connection retries;
it does not retry failed component validation or make deployment transactional.
Keep the VM awake during long checks without disabling unrelated power policy.
Record interruption and recovery evidence in project status; a remote test is not
evidence that the user-local deployment path has passed native acceptance.
