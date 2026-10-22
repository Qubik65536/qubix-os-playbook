# Use the Qubix desktop

After [local deployment](deployment.md), use these session controls.


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
| Ctrl+Space | Toggle English / Simplified Chinese Pinyin |
| Super+T or Super+Return | WezTerm terminal |
| Super+Space or Super+D | Noctalia launcher |
| Super+V | Clipboard history |
| Super+Comma | Noctalia settings |
| Super+N | Notification centre |
| Super+W or Super+Q | Close focused window |
| Super+arrows or H/J/K/L | Navigate windows/columns |
| Super+Shift+arrows or H/J/K/L | Move windows/columns |
| Super+Ctrl+Left/Right or H/L | Resize column width |
| Super+Ctrl+Up/Down or K/J | Resize window height |
| Super+Ctrl+Shift+Left/Right or H/L | Resize column width in 10% steps |
| Super+Ctrl+Shift+Up/Down or K/J | Resize window height in 10% steps |
| Super+Ctrl+R | Reset automatic window height |
| Super+Ctrl+Alt+arrows or H/J/K/L | Focus the screen in that direction |
| Super+Ctrl+Alt+Shift+arrows or H/J/K/L | Move the focused window to that screen |
| Super+Alt+arrow keys | Focus the screen in that direction |
| Super+Alt+Shift+arrow keys | Move the focused window to that screen |
| Super+Tab or Super+O | Overview |
| Alt+Tab | Noctalia window switcher |
| Super+Shift+S | Screenshot |
| Super+Shift+/ | Searchable shortcut cheatsheet |
| Super+F1 | Compact shortcut overlay |
| Super+Shift+E | Exit session |

The compact top bar groups each component in its own rounded module. The dock is disabled; use Super+Space, Super+O or Alt+Tab for application access. Click its keyboard button or press Super+Shift+/ for the shortcut cheatsheet. Search by action or key, scroll through the categories, and close with Escape, Close or an outside click. The list follows Qubix's managed bindings; personal Niri overrides are not included. Follow the [developer regeneration guide](../development/shortcuts.md) after changing the repository's bindings.

For power controls, press **Super+X**, click the bar power button, or choose the pinned **Power options** entry in the launcher. The compact menu follows Noctalia's horizontal icon-tile layout with number badges beside the bar. Hold **1** Lock, **2** Log out, **3** Lock & Suspend, **4** Reboot or **5** Shut down for **three seconds**; releasing early cancels. Clicking a tile starts a **five-second countdown**; clicking it again cancels. Escape, the lower-right Cancel button or closing the menu cancels too. Shut Down keeps Noctalia’s destructive highlight. The lower-left prompt explains confirmation and cancellation; the selected tile shows progress and remaining seconds. Lock actions are unavailable when Noctalia locking is disabled.

The Control Center's built-in power entry opens the separate native menu: its supplied five-second countdown uses tap-to-arm and a second activation confirms immediately, without release-to-cancel. Native per-row GUI overrides apply there and remain preserved. Searching **reboot**, **shutdown**, **sleep**, **lock** or **logout**, or typing **/session**, returns direct native actions that execute when selected. Those results and the dedicated Super+Alt+L lock shortcut do not use the guarded menu. See the [power confirmation contract](../architecture/desktop-design.md#power-action-countdown).

Screen shortcuts follow your display layout: with the external screen to the right,
Super+Alt+Right focuses it and Super+Alt+Shift+Right moves the focused window there.
Use Left to return to the laptop screen. Up/Down support vertically arranged screens.
With no screen in the requested direction, the action has no effect. Reopen the
shortcut panel after deployment to see the updated list. No extra packages or
connector configuration are required.

The matching H/J/K/L screen controls use Super+Ctrl+Alt (plus Shift to move);
H is left, J down, K up and L right. Super+Alt+L remains the lock shortcut.

Resize shortcuts use 5% steps; add Shift for larger 10% steps with either key set. Tiled windows in one column share its width; height changes are easiest to see with two windows stacked in the column. The reset shortcut returns the focused window to automatic height.

Check wallpaper, bar, notifications, launcher, terminal and keyboard navigation visually. A successful file install is not graphical verification. Review session logs if companions fail. Native user services may start a second bar or notification service; collect their status before changing anything. When upgrading the classic Qubix session, log out and select it again: reloading KDL alone does not replace existing Waybar/Mako/Swaybg processes.

Noctalia provides the shell's Polkit agent; test GUI privilege prompts and lock/unlock manually. Its Qubix defaults use rounded windows/panels and the #56728b accent. The complete [appearance and shortcut contract](../architecture/desktop-design.md) explains shell ownership. GUI changes are stored in the Qubix-only user state namespace and override managed defaults; native Noctalia settings remain preserved. Noctalia app-theme templates are disabled. WezTerm uses the supplied shell configuration. Bash receives additive system defaults; existing user Starship configuration takes precedence and personal initialization runs normally. For Zsh, optional adoption is a manual decision: after backing up your own `.zshrc`, you can add `source /usr/share/qubix/shell/qubix.zsh`. The playbook never edits it or runs `chsh`.

Fish remains your existing shell when it is the account default; automatic Fish prompt integration is not implemented. To explicitly try the Qubix Starship prompt in one Fish terminal after deployment, without editing dotfiles:

```fish
set -gx STARSHIP_CONFIG /etc/qubix/starship.toml
starship init fish | source
```

This changes that terminal's prompt; closing it returns to your normal startup configuration. Existing personal prompt configuration remains available. For persistent manual adoption, back it up and review [Starship's Fish setup](https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship) first.

Run deployment again with the same revision and configuration. Expect zero managed configuration changes. Record the recap and actual session behaviour using the [acceptance checklist](verification.md).

Simplified Chinese Pinyin is included in the Qubix session. After login, focus a text
field, press Ctrl+Space, type `nihao` and press Space to commit `你好`. Press Ctrl+Space
again for English. Super+Space stays assigned to the app launcher; Qubix disables
Fcitx's conflicting default group shortcuts. Saved Fcitx profiles and shortcuts take precedence; add Pinyin to
an existing profile if needed. See [input methods](../components/input-method.md).

Candidates use a dark horizontal panel with larger CJK text. Reopen applications
that were running before the theme upgrade; GTK can cache its input UI settings.
Personal Fcitx UI settings override this default and remain untouched. A fresh
login also reloads the daemon for applications using its candidate renderer.
