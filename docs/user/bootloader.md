# Configure the existing bootloader

Run the playbook locally on the authorized disposable VM, using
`-i inventory/local.ini -e @config/local.yml`; see [deployment](deployment.md).
Bootloader and Plymouth default enabled but require measured machine-specific inputs.

Both adapters are implemented and mandatory for MVP acceptance. Test them on separate disposable VM installations with their respective loaders already installed. Do not switch loaders just for a theme. Keep a snapshot and console access.

Read [target information](collecting-target-info.md) and [bootloader requirements](../components/bootloader.md) before selection. Merge **one** section below into the same `qubix` mapping; preserve your desktop settings.

For confirmed active GRUB:

```yaml
  bootloader:
    enabled: true
    backend: grub
    config_path: /boot/grub/grub.cfg
    confirm_active: true
```

Use your actual active path; `/boot/grub2/grub.cfg` is also supported. The active generated configuration must already source `custom.cfg`. Qubix adds a checked appearance block to that hook and installs its theme. It does not run `grub-install` or `grub-mkconfig` or replace menu entries.

For confirmed active Limine:

```yaml
  bootloader:
    enabled: true
    backend: limine
    config_path: /boot/limine.conf
    confirm_active: true
    limine_version: 10
```

Paths and version above are examples, not detected values. Supported confirmed majors are 8–12. Confirm the loader actually running in firmware, including its version; updating an installed package does not necessarily update the EFI executable. Only the supported bounded appearance settings change; boot payloads remain preserved.

Preview/deploy with `--ask-become-pass`, then installed verification with `--tags installed --ask-become-pass`. Reboot the VM yourself. Confirm theme, original entries, kernel arguments and successful boot. Repeat deployment and test restoration independently for each adapter.

For initramfs mappings, active Limine cache bindings and splash activation, follow
the [Plymouth guide](plymouth.md). Test the two generators independently.
