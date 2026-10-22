# Simplified Chinese Pinyin

Status: **Implemented; native installation/parser/engine/primary daemon and zero-change reapplication Tested; physical application typing and next-login startup pending**. Focused task: make zh-Hans Pinyin available alongside
English in Qubix Niri. Acceptance: native packages and engine are measured before
component writes; English/Pinyin defaults load in real Fcitx; `nihao`/`hanyu` commit `你好`/`汉语`;
personal input configuration remains unchanged; installation reapplication has zero
changes. Parser, isolated input, primary session and physical typing are separate gates.

Niri includes Fcitx 5 by default, without a separate feature switch. Explicit package
preparation installs `fcitx5`, `fcitx5-chinese-addons`, `fcitx5-gtk`, `fcitx5-qt` and
`noto-fonts-cjk`. Deployment only validates prerequisites; it never installs packages.
The managed `/etc/qubix/fcitx5/profile` defaults to the US keyboard with Pinyin as the
input method activated by Fcitx's native Ctrl+Space shortcut. The managed
`/etc/qubix/fcitx5/config` clears Fcitx's built-in Super+Space and
Shift+Super+Space group-switch shortcuts, reserving Super+Space for Niri's launcher.
Personal global Fcitx configuration retains precedence, just like personal profiles. Pinyin uses its native
Simplified Chinese output; no Traditional Chinese conversion is enabled by Qubix.

The session starts `/usr/share/qubix/bin/qubix-fcitx5`. This launcher prepends the
managed directory to Fcitx's configuration search path only for that process.
Personal `~/.config/fcitx5` (or `FCITX_CONFIG_HOME`) retains priority, including saved
engine selections, learned words and shortcuts. Existing profiles must add Pinyin
through Fcitx configuration if absent; deployment never overwrites them. No locale,
keyboard layout, personal dotfile, global XDG search path or native session is changed.
Fcitx may save its selected defaults into its own user configuration at runtime.

Qubix Niri sets GTK_IM_MODULE/QT_IM_MODULE to `fcitx` and XMODIFIERS to `@im=fcitx`
for applications launched by the session. Existing applications need reopening;
logout/login activates startup and the complete session environment. Deployment does
not restart the compositor or terminate applications. Another running input framework
must be resolved by the operator before starting Fcitx; never replace it automatically.

Managed system resources use the ordinary baseline/receipt engine and restoration.
Package installation and Fcitx's own user data are outside file restoration.
Use Ctrl+Space to toggle English/Pinyin, type `nihao` and press Space to commit `你好`.
Application-specific Electron/Chromium IME flags remain application settings.

Upstream references: [Fcitx setup](https://fcitx-im.org/wiki/Setup_Fcitx_5),
[Wayland integration](https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland/en) and
[Fcitx search paths](https://github.com/fcitx/fcitx5/blob/master/src/lib/fcitx-utils/standardpath.cpp).

See [native test evidence and remaining gates](../project/pinyin-test-results.md).

Shortcut correction acceptance: the native global configuration reports empty forward/
backward group shortcuts, retains Ctrl+Space, and still converts Simplified Chinese.
The primary daemon must reload those settings without a compositor restart; identical
file reapplication must report zero changes. Physical launcher/input acceptance is separate.

[Rime and candidate UI options](../architecture/input-method-options.md) now have native
engine/GTK preview evidence. Rime Ice adoption and production UI integration remain
Planned; ordinary deployment still uses the Pinyin defaults described above.
