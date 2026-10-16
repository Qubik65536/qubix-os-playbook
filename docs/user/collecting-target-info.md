# Share SSH access and collect target information

Status: **Read-only collector Implemented; supported-host output needs the VM**. A connection endpoint is sufficient to begin read-only inspection; system details can be collected afterward. No boot or image generation command is needed to inspect the environment.

## Connection details

Send this template with your actual values:

```text
Host/IP or configured SSH alias:
SSH username:
SSH port: 22
Authentication: existing SSH agent, or local private-key file path
Sudo: passwordless, password required, or unavailable
Machine: disposable VM or physical machine
Snapshot/backup and console access: available or unavailable
```

The address must be reachable from the controller running this repository. In the target, `whoami` gives the account and `ip -brief address` lists addresses. NAT may need a forwarded SSH port; mention any required VPN or jump host. A configured SSH alias can supply those settings instead.

Use an existing local key or SSH agent; send only its local path or alias, never the private-key contents, passphrase or sudo password. The pinned Ansible controller supports password authentication with --ask-pass; enter passwords at the prompt rather than saving them in inventory. SSH keys remain convenient for repeated runs. No new key or personal SSH configuration is needed when working key access already exists.

An optional block in `~/.ssh/config` makes repeated connections easier. Keep any existing
OrbStack `Include` at the top. Replace the address/account below; include the IP in the `Host`
patterns when Ansible's inventory connects directly to that IP:

```sshconfig
Host qubix YOUR_TARGET_IP
    HostName YOUR_TARGET_IP
    User YOUR_LINUX_USER
    IdentityFile ~/.ssh/id_ed25519_qubix
    ControlMaster auto
    ControlPersist 8h
    ControlPath ~/.ssh/qubix-%C
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

If an inventory already pins a host key and a shared `ControlPath`, retain those exact settings
in this block instead of the generic path. Set `chmod 600 ~/.ssh/config`, then `ssh -MNf qubix`
to establish a reusable connection with your password. For persistent key access, generate a key
with `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_qubix` and append only its `.pub` contents to
the target account's `~/.ssh/authorized_keys` through your authenticated connection. Keep that
remote directory mode 0700 and file mode 0600. A multiplexed password login expires; it does not
install a key by itself. Use your chosen alias in place of `qubix` in these commands.

From this Mac, first confirm ordinary SSH login, completing host-key verification and any key-unlock prompt yourself:

```bash
ssh -p PORT USER@HOST
```

If the connection times out before authentication, collect these on the target console:

```bash
ip -brief address
systemctl is-active sshd
ss -ltn '( sport = :22 )'
```

Report the actual SSH port and, for a VM, its network mode. Bridged networking or a reachable forwarded NAT port is needed when connecting from another machine. Review the target firewall's SSH rule rather than disabling the firewall. If sshd is unavailable or inactive, use the manual SSH preparation in the [user guide](getting-started.md).

If needed, obtain the target's public host-key fingerprint from its console using `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`, then compare it with the SSH prompt. If that key type is absent, use the existing host public key. Do not disable host-key checking.

You can alternatively provide an existing local Ansible inventory path; its group must be `qubix_targets`. Host-specific inventory and credentials stay out of Git. See the [user guide](getting-started.md) for an ignored inventory example.

Once access is available, the agent can run the collector and Ansible inspection. Reports below are optional if the agent can connect. Initial work is read-only inspection and validation. After inspection, prepare a target-specific deployment plan for review. Boot-critical tests require an explicitly authorized disposable VM with recovery access, following the [project safety rules](../../AGENTS.md).

## Read-only report

From the controller checkout, run the collector on the VM without installing the repository there:

```bash
mkdir -p .cache
ssh USER@HOST 'bash -s' < scripts/collect-target-info.sh > .cache/target-report.txt
./bootstrap.sh verify -i inventory/target.local.ini > .cache/target-verify.txt 2>&1
```

Create `.cache` first if it does not exist. For a custom port use `ssh -p PORT`. You can also copy the collector to the VM and run `bash collect-target-info.sh`.

The collector reads OS/version, network address, running kernel, package versions, Niri, manager activity, user services, EFI/loader status where readable, module directories, kernel file metadata and mkinitcpio configuration/presets. It never invokes sudo, changes services, sources configuration, installs packages or generates images. Missing tools and permission errors stay visible. Review the report for private network identifiers, UUIDs and custom paths before sharing; do not share backup image contents or personal dotfiles.

## Confirm the boot chain separately

`bootctl status` can identify the running loader on some EFI systems. `efibootmgr -v` identifies the current EFI entry/executable, but not necessarily its configuration. Hypervisor firmware settings and the visible boot menu provide additional evidence. On BIOS systems, firmware/installation records and boot-menu version may be needed.

Find the configuration that the running loader actually reads. Check mounts with `findmnt /boot`, `findmnt /efi` and `findmnt /boot/efi` as applicable. Candidate paths appear in the Ansible report; their existence alone does not prove they are active. If several loaders/configurations are present, leave bootloader branding disabled and send the ambiguity.

For GRUB, inspect the confirmed generated file for its existing `custom.cfg` source hook. For Limine, report the menu/EFI loader version and active configuration. Send relevant entries and paths only after redacting private details. Qubix requires explicit `config_path` and `confirm_active` and does not select by distribution.

## Confirm the image generator and mapping

Tool installation alone does not prove image ownership. Review the installed kernel package hooks, existing preset/configuration, current boot entry's image path and installation choices. Do not regenerate anything to find out.

For every image to change, provide:

| Information | How to identify it |
|---|---|
| Initramfs path | Read the active boot entry and installed preset; verify the file exists |
| Kernel version | Matching `/usr/lib/modules/VERSION` directory and `file /boot/vmlinuz-NAME` output |
| Kernel image path | Kernel path from that same boot entry/preset |
| Generator | Existing kernel maintenance hook/preset evidence, not just installed binary |
| mkinitcpio preset names | Names of `/etc/mkinitcpio.d/*.preset` without the suffix |
| All preset outputs | Literal `default_image`, `fallback_image` or other image declarations |
| Existing splash argument | `cat /proc/cmdline` contains the token `splash` |
| UKI/encryption/signing | Installation choices plus entry/preset evidence; report whether present |

`uname -r` is only the running kernel; it does not describe all installed images. If file metadata does not establish a match, stop and send the evidence. A `.efi` UKI or signed-image pipeline is outside this candidate's Plymouth support.

You may manually use sudo to read protected configuration on your VM after reviewing the path, for example `sudo sed -n '1,220p' /boot/limine.conf` or a selected preset. Do not execute/source those files. Avoid broad dumps of unrelated secrets.

## Desktop and login evidence

Collect manager unit activity from the report. For SDDM, confirm `/usr/share/sddm/themes/breeze` exists. On greetd, retain its current configuration; desktop tests can use a free TTY without replacing the manager.

In the graphical session, collect `systemctl --user list-units --type=service --state=running` and application failures if there are duplicate panels/notifications. SSH desktop environment hints may be absent. Tell us whether wallpaper, bar, launcher, terminal, notifications and authentication prompts work visually.

Start by sending connection details; send reports only if direct inspection is unavailable. Active loader/generator confirmation is needed only before their opt-in tests.
