# Get started: test Qubix on CachyOS Niri

Status: **Implemented MVP candidate; desktop file lifecycle and nested rendering Tested on CachyOS; primary-session/full VM acceptance pending**. This guide is for someone deploying and trying the desktop. Start with a disposable CachyOS Niri VM and a snapshot. You can test the desktop before touching login, bootloader or splash settings.

## 1. Prepare your controller and VM

Use the existing repository checkout on your Mac or Linux controller. The candidate commits are local: cloning GitHub does not include them until they are published. Ansible transfers files over SSH, so the VM does not need a repository checkout.

On the controller, use Python 3.12 or newer (the validated environment uses 3.13):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
./bootstrap.sh --help
```

On the VM, keep its existing Niri installation and display manager.

Preview the selected desktop transaction before installation, especially on a physical machine:

```bash
pacman -Sp --needed --print-format '%n %v' noctalia foot jq starship
```

Native CachyOS Snapper/Limine package hooks can create snapshots and refresh menu entries. Those effects occurred in the [recorded native desktop test](../project/desktop-test-results.md); they are package preparation effects, independently of Qubix boot branding. Review the actual transaction and keep normal hooks enabled.

Install the selected desktop companions and SSH prerequisites yourself:

```bash
sudo pacman -S --needed python openssh noctalia foot jq starship
noctalia --version
sudo systemctl enable --now sshd
ip -brief address
whoami
```

These are manual VM preparation commands; the playbook does not install packages or enable services. Use an ordinary account with sudo access. Enable SSH only on your test network and retain the hypervisor console. Verify the SSH host key when connecting. Do not share passwords or private keys.

Create an ignored controller inventory at `inventory/target.local.ini`, substituting your VM values:

```ini
[qubix_targets]
qubix-vm ansible_host=192.168.64.10 ansible_user=YOUR_VM_USER ansible_port=22
```

Test `ssh YOUR_VM_USER@192.168.64.10`. With password-only SSH, add `--ask-pass` to Ansible commands and enter the password interactively; the pinned controller uses native SSH askpass. Keep the password out of inventory. SSH keys are convenient for repeated tests. Keep one VM in this inventory while testing boot changes.

## 2. Inspect without deploying

```bash
./bootstrap.sh verify -i inventory/target.local.ini
```

The report must show CachyOS, Linux/systemd, Pacman and Niri. It lists measured companion binaries and manager activity. Bootloader and image generator stay `unresolved` until you confirm them. Package presence is insufficient proof of the firmware's active loader.

If /boot metadata is private, repeat inspection with explicit read-only privilege:

```bash
./bootstrap.sh verify -i inventory/target.local.ini -e '{"qubix_discovery_privileged": true}' --ask-become-pass
```

Keep that typed extra variable on later commands when boot paths need sudo. This permits metadata reads only; deployment still requires its selected component settings.

If help is needed, use [collecting target information](collecting-target-info.md). That guide explains how to identify active paths and what to send back.

## 3. Preview and deploy the desktop

The `cachyos-niri` profile enables branding, Niri and shell defaults. Login, bootloader and Plymouth are disabled. You may save explicit overrides in ignored `config/local.yml`:

```yaml
# Explicit metadata read privilege for stock CachyOS private /boot.
qubix_discovery_privileged: true
qubix:
  profile: cachyos-niri
  branding:
    enabled: true
  niri:
    enabled: true
    user_config: preserve
  shell:
    enabled: true
    change_default_shell: false
  login:
    enabled: false
  bootloader:
    enabled: false
  plymouth:
    enabled: false
```

The discovery flag is an operational override, default false; it permits metadata reads and does not enable boot/splash components. The commands below use password SSH. Omit --ask-pass when using keys. SSH pipelining reduces round trips and was used in the native test.

Run from the controller:

```bash
export ANSIBLE_PIPELINING=true
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-pass --ask-become-pass
./bootstrap.sh deploy -i inventory/target.local.ini -e @config/local.yml --ask-pass --ask-become-pass
./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --tags installed --ask-pass --ask-become-pass
```

Missing prerequisites stop deployment before component writes. The native Niri, Foot and Noctalia parsers validate candidate files before activation. Standalone Noctalia >=5.2.0 and <6.0.0 is required; legacy Quickshell/v4 does not satisfy this profile. A parser failure may leave earlier inert files installed; backups support recovery. Check mode performs no backup/state writes and cannot validate files it has not installed.

Existing personal dotfiles and `/etc/niri/config.kdl` remain intact. The additional session uses `/etc/niri/qubix/config.kdl` explicitly, so it does not inherit your personal Niri configuration. Qubix installs named resources, not a replacement operating system.

## 4. Try the Qubix session

The 32 px dark-module bar shows a bounded active application title, CPU load, used RAM, CPU temperature when available, optional active media and the usual session controls. Unsupported sensor readings show --. On narrow outputs Noctalia may omit earlier modules that do not fit; simplify the widget list in its settings if needed.

Qubix supplies 100% scaling at session start and whenever a screen is newly connected or reconnected. Niri's preferred resolution and refresh rate remain unchanged. You can adjust an already-connected screen through Noctalia for the current session; the helper does not continuously reset it. This default belongs to the Qubix session and does not rewrite personal/native output files. The helper's --once mode is used only for explicit activation in an already-running session.

After deployment, log out when convenient and select **Qubix Niri** in a login manager that offers Wayland session selection. Keep native Niri available as a fallback.

The standard playbook preserves the native session entry. If you separately authorize its retirement, restore its backup before removing/restoring the Qubix session files; see the [operator-directed retirement and recovery procedure](../project/live-test-plan.md#operator-authorized-native-session-retirement-and-reboot). The Niri compositor package is still required by Qubix.

If your existing manager, such as a fixed-command greetd setup, does not expose a session picker, log out, open a free VM TTY, sign in as your ordinary user and run:

```bash
niri --session --config /etc/niri/qubix/config.kdl
```

Run this from a free TTY, not inside an existing graphical session. In a temporary nested preview the Mod key is Alt; the main session uses Super. Qubix does not rewrite greetd's session command.

| Key | Action |
|---|---|
| Super+T or Super+Return | Foot terminal |
| Super+Space or Super+D | Noctalia launcher |
| Super+V | Clipboard history |
| Super+Comma | Noctalia settings |
| Super+N | Notification centre |
| Super+W or Super+Q | Close focused window |
| Super+H/J/K/L | Navigate windows/columns |
| Super+Ctrl+Left/Right or H/L | Resize column width |
| Super+Ctrl+Up/Down or K/J | Resize window height |
| Super+Ctrl+R | Reset automatic window height |
| Super+Tab or Super+O | Overview |
| Alt+Tab | Noctalia window switcher |
| Super+Shift+S | Screenshot |
| Super+Shift+/ | Searchable shortcut cheatsheet |
| Super+F1 | Compact shortcut overlay |
| Super+Shift+E | Exit session |

The compact top bar groups each component in its own rounded module. The dock is disabled; use Super+Space, Super+O or Alt+Tab for application access. Click its keyboard button or press Super+Shift+/ for the shortcut cheatsheet. Search by action or key, scroll through the categories, and close with Escape, Close or an outside click. The list follows Qubix's managed bindings; personal Niri overrides are not included. Follow the [README regeneration guide](../../README.md#regenerate-the-shortcut-cheatsheet) after changing the repository's bindings.

For power controls, press **Super+X**, click the bar power button, or choose the pinned **Power options** entry in the launcher. Hold **1** Lock, **2** Log out, **3** Lock & Suspend, **4** Reboot or **5** Shut down for **three seconds**; releasing early cancels. Clicking a button starts a **five-second countdown**; clicking it again cancels. Escape, Cancel or closing the menu cancels too. The menu shows progress and the remaining seconds. Lock actions are unavailable when Noctalia locking is disabled.

The Control Center's built-in power entry opens the separate native menu: its supplied five-second countdown uses tap-to-arm and a second activation confirms immediately, without release-to-cancel. Native per-row GUI overrides apply there and remain preserved. Searching **reboot**, **shutdown**, **sleep**, **lock** or **logout**, or typing **/session**, returns direct native actions that execute when selected. Those results and the dedicated Super+Alt+L lock shortcut do not use the guarded menu. See the [power confirmation contract](../architecture/desktop-design.md#power-action-countdown).

Resize shortcuts use 5% steps. Tiled windows in one column share its width; height changes are easiest to see with two windows stacked in the column. The reset shortcut returns the focused window to automatic height.

Check wallpaper, bar, notifications, launcher, terminal and keyboard navigation visually. A successful file install is not graphical verification. Review session logs if companions fail. Native user services may start a second bar or notification service; collect their status before changing anything. When upgrading the classic Qubix session, log out and select it again: reloading KDL alone does not replace existing Waybar/Mako/Swaybg processes.

Noctalia provides the shell's Polkit agent; test GUI privilege prompts and lock/unlock manually. Its Qubix defaults use rounded windows/panels and the #56728b accent. The complete [appearance and shortcut contract](../architecture/desktop-design.md) explains shell ownership. GUI changes are stored in the Qubix-only user state namespace and override managed defaults; native Noctalia settings remain preserved. Noctalia app-theme templates are disabled. Foot starts a login shell. Bash receives additive system defaults; existing user Starship configuration takes precedence and personal initialization runs normally. For Zsh, optional adoption is a manual decision: after backing up your own `.zshrc`, you can add `source /usr/share/qubix/shell/qubix.zsh`. The playbook never edits it or runs `chsh`.

Fish remains your existing shell when it is the account default; automatic Fish prompt integration is not implemented. To explicitly try the Qubix Starship prompt in one Fish terminal after deployment, without editing dotfiles:

```fish
set -gx STARSHIP_CONFIG /etc/qubix/starship.toml
starship init fish | source
```

This changes that terminal's prompt; closing it returns to your normal startup configuration. Existing personal prompt configuration remains available. For persistent manual adoption, back it up and review [Starship's Fish setup](https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship) first.

Run deployment again with the same revision and configuration. Expect zero managed configuration changes. Record the recap and actual session behaviour using the [acceptance checklist](verification.md).

## 5. Optional login branding

This candidate supports an **already-active SDDM** with an installed compatible Breeze theme. It does not replace managers. Leave login disabled on greetd/GDM/LightDM targets.

Change only the login section of your existing configuration:

```yaml
  login:
    enabled: true
    backend: sddm
    theme_source: breeze
```

Repeat preview, deploy and installed verification, including `--ask-become-pass` for private login settings. On the VM, if available, preview with `sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/qubix` (some installations name it `sddm-greeter`). Preview requires a graphical display and does not prove authentication.

Take a fresh snapshot, then reboot the VM yourself to test the effective theme, authentication, native Niri and Qubix Niri. Deployment does not restart SDDM or interrupt your session.

## 6. Test the existing bootloader

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

Paths and version above are examples, not detected values. Supported confirmed majors are 8–12. Confirm the loader actually running in firmware, including its version; updating an installed package does not necessarily update the EFI executable. Only branding and terminal foreground/background directives change.

Preview/deploy with `--ask-become-pass`, then installed verification with `--tags installed --ask-become-pass`. Reboot the VM yourself. Confirm theme, original entries, kernel arguments and successful boot. Repeat deployment and test restoration independently for each adapter.

## 7. Optional Plymouth and initramfs

Plymouth is independent of the loader. Keep it disabled until the active generator, existing image paths and kernel mapping are known. The current boot must already contain `splash`; Qubix never inserts kernel arguments. An installed two-step plugin is required. UKIs, signing changes and complex mkinitcpio configurations are unsupported.

For dracut, merge this section with your **actual** version and paths:

```yaml
  plymouth:
    enabled: true
    initramfs_backend: dracut
    confirm_active: true
    force_rebuild: false
    images:
      - path: /boot/initramfs-linux-cachyos.img
        kernel: REPLACE_WITH_INSTALLED_KERNEL_VERSION
        kernel_image: /boot/vmlinuz-linux-cachyos
    presets: []
```

`kernel` is the directory name under `/usr/lib/modules` matching that kernel image, not the package name. `uname -r` identifies only the currently running kernel. Include every image you intend to modify.

For mkinitcpio, change `initramfs_backend` to `mkinitcpio` and provide selected existing preset names, for example `presets: [linux-cachyos]`. Explicit `images` must exactly cover **all** outputs from those presets, including fallback images if present. Map each output to its correct kernel and kernel image. Qubix inserts only the Plymouth hook and runs `--nopost -p PRESET` so post hooks cannot rewrite entries.

Preview/deploy/installed-verify with sudo prompting as above. Actual deployment rebuilds the confirmed images, after backups, and checks theme/plugin/daemon resources in each archive. Unchanged inputs skip regeneration; an incomplete rebuild remains pending. `force_rebuild: true` is an explicit repair option; return it to false afterward.

Reboot and observe the splash. If encryption is in use, verify that the existing unlock path and Plymouth prompt still work; Qubix does not configure encryption. Test each generator independently. Archive contents alone cannot prove a visible or functioning splash.

## 8. Restore and report results

The supported restore returns the first pre-Qubix state of recorded files/images, not the whole OS:

```bash
./bootstrap.sh restore -i inventory/target.local.ini -e @config/local.yml --check --diff --ask-pass --ask-become-pass
./bootstrap.sh restore -i inventory/target.local.ini -e @config/local.yml --ask-pass --ask-become-pass
```

Review [restoration](restoration.md) first. Drift requires deliberate consent; changed kernels prohibit stale image restoration, and changed preserved boot entries/settings prohibit stale activation restoration even after reapplication or force. A VM snapshot is the reliable fallback for boot failure.

File restoration keeps prerequisite packages, protected baselines and empty/unlisted directories. The native desktop test removed all 17 named resources and verified preservation. See the [actual results and limits](../project/desktop-test-results.md).

Inspect both `/var/lib/qubix/deployment.json` and `deployment-pending.json` as root: the first is the last completed file deployment; a pending failed attempt can coexist with it. Neither asserts graphical or reboot success.

Send the revision, configuration (without credentials), target report, command outcomes and checklist evidence. Desktop/login/GRUB/Limine/dracut/mkinitcpio acceptance are separate results. The candidate becomes an accepted MVP only when all required VM tests pass.
