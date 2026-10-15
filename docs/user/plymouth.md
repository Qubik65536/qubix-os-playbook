# Boot, reboot and poweroff splash

Status: circular theme Implemented; native preview and image generation have separate acceptance gates. See [current evidence](../project/status.md). Plymouth supplies the splash after the bootloader and during shutdown; changing it does not theme the Limine or GRUB menu.

The Qubix theme keeps the logo and QUBIX OS title visible, animates a blue-gray circular loader and uses Starting, Restarting or Shutting down captions. Native Plymouth services select the mode. Password/question/message callbacks remain available; password display receives only the bullet count. The playbook preserves kernel arguments, encryption configuration, boot entries and native service units.

## Preview without activation

On a target with a running Niri session, Plymouth/script/X11 plugins, bubblewrap, Xwayland, ImageMagick and Python already installed:

```bash
.venv/bin/ansible-playbook -i inventory/target.local.ini tests/integration/plymouth.yml -e @config/local.yml --ask-pass --ask-become-pass
```

This explicitly opens a temporary preview window. It runs the actual parser and theme in private user/mount/PID/network namespaces, with a private daemon socket, pseudoterminal and X11 server. Host files are read-only; no DRM or physical virtual-terminal devices are exposed. Evidence is fetched to ignored `.cache/native-plymouth/`; temporary processes/files are removed. Missing prerequisites fail. This test neither selects the host theme nor generates an image. It does not establish an actual boot, encryption unlock or poweroff result.

## Configure activation on a disposable VM

Take a VM snapshot and retain console/live-media access. Inspect the selected native generator, `/etc/mkinitcpio.d/*.preset` or dracut image outputs, installed module directories, current kernel files and active command line. An existing `splash` argument and native script plugin are required. Do not guess an image path from the distribution or use `uname -r` as the version of every installed kernel.

Add a `plymouth` section to your existing ignored configuration. Set `enabled: true`, `confirm_active: true` and the measured `initramfs_backend`. Each `images` entry requires the existing `path`, installed module-directory `kernel` and associated unchanged `kernel_image`. Mkinitcpio also requires exact native `presets`; every selected output must be covered. See the [reviewed target mapping](../project/plymouth-test-plan.md) for a concrete example, which must be re-inspected before reuse.

Preview, review the predicted selection/integration changes, then activate only on an authorized target:

```bash
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/plymouth.local.yml --check --diff --ask-pass --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/plymouth.local.yml --ask-pass --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @config/plymouth.local.yml --tags installed --ask-pass --ask-become-pass
```

Check mode does not rebuild, back up images or prove the resulting archives. Activation snapshots affected resources and images before rebuilding. Mkinitcpio uses `--nopost -p` for selected presets; the preserved snapshot-hook append remains active without rerunning Limine post hooks. Dracut uses the explicit images and kernels. Native archive checks require the logo, theme/script, daemon, script/label plugins and fonts. A failed check leaves pending state visible.

Reapply the identical configuration before reboot: unchanged inputs should skip regeneration. Keep `force_rebuild: false` except for an intentional repair. Observe startup, logout/reboot and poweroff separately; shutdown branding depends on the native Plymouth services and available graphics. For encrypted roots, test the real unlock prompt with console access. Record parser, preview, archive and physical observations separately.

## Recover

Use the [restoration guide](restoration.md). Backups are per-resource rather than a complete rollback; changed kernels block restoring stale images. The standard restore command restores **all** recorded components. If the native Niri login entry was retired, restore that entry before removing the Qubix session. Recover a failed VM from its snapshot first. Physical activation needs the explicit exception and recovery plan described in the [target plan](../project/plymouth-test-plan.md).
