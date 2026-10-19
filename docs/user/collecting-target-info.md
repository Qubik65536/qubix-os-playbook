# Collect information on this machine

Run these commands directly on the CachyOS Niri machine as your ordinary account,
from the extracted playbook/checkout root:

```bash
mkdir -p .cache
bash scripts/collect-target-info.sh > .cache/target-report.txt
./bootstrap.sh verify -i inventory/local.ini -e @config/local.yml --ask-become-pass > .cache/target-verify.txt 2>&1
```

Create `config/local.yml` using the [deployment guide](deployment.md) first. The
collector never invokes sudo, changes services, installs packages or generates images.
Permission errors remain visible. For private boot metadata, the verification command
requires the explicit YAML boolean `qubix_discovery_privileged: true` outside `qubix`.
Review output for network identifiers, UUIDs, account names and private paths before
sharing. Never share credentials, personal secrets, dotfiles or backup image contents.
Report the source revision, sanitized options, exact command and failure output.
Developer connection/access setup lives in the [SSH testing guide](../development/ssh-testing.md).

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

In the graphical session, collect `systemctl --user list-units --type=service --state=running` and application failures if there are duplicate panels/notifications. Tell us whether wallpaper, bar, launcher, terminal, notifications and authentication prompts work visually.
