"""Exercise real Fcitx on a private bus/home; never send keys to desktop clients."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from gi.repository import Gio, GLib

BUS_NAME = "org.fcitx.Fcitx5"
IM_IFACE = "org.fcitx.Fcitx.InputMethod1"
IC_IFACE = "org.fcitx.Fcitx.InputContext1"


def probe(root, personal=False):
    config = root / "config"
    config.mkdir(exist_ok=True)
    if personal:
        (config / "profile").write_text(
            "[Groups/0]\nName=Personal\nDefault Layout=us\nDefaultIM=keyboard-us\n"
            "[Groups/0/Items/0]\nName=keyboard-us\nLayout=\n[GroupOrder]\n0=Personal\n"
        )
    original = (config / "profile").read_bytes() if personal else None
    env = dict(os.environ, FCITX_CONFIG_HOME=str(config),
               FCITX_DATA_HOME=str(root / "data"), XDG_CACHE_HOME=str(root / "cache"))
    # No connection to the user's compositor or X server in this backend test.
    for key in ("DISPLAY", "WAYLAND_DISPLAY"):
        env.pop(key, None)
    with (root / "fcitx.log").open("w") as log:
        process = subprocess.Popen(["/usr/share/qubix/bin/qubix-fcitx5", "--disable=wayland,xim,xcb"],
                                   env=env, stdout=log, stderr=log)
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

            def call(path, interface, method, parameters=None):
                destination = "org.freedesktop.DBus" if interface == "org.freedesktop.DBus" else BUS_NAME
                return bus.call_sync(destination, path, interface, method, parameters,
                                     None, Gio.DBusCallFlags.NONE, 5000, None).unpack()

            for _ in range(100):
                try:
                    result = call("/org/freedesktop/DBus", "org.freedesktop.DBus", "NameHasOwner",
                                  GLib.Variant("(s)", (BUS_NAME,)))
                    if result[0]:
                        break
                except GLib.Error:
                    pass
                assert process.poll() is None, (root / "fcitx.log").read_text()
                time.sleep(0.1)
            else:
                raise AssertionError("Fcitx did not acquire its private bus name")
            global_config, _ = call("/controller", "org.fcitx.Fcitx.Controller1", "GetConfig",
                                    GLib.Variant("(s)", ("fcitx://config/global",)))
            hotkeys = global_config["Hotkey"]
            assert not hotkeys["EnumerateGroupForwardKeys"], hotkeys
            assert not hotkeys["EnumerateGroupBackwardKeys"], hotkeys
            assert "Control+space" in hotkeys["TriggerKeys"].values(), hotkeys
            # Separate client connection remains alive through context creation and all events.
            path, _ = call("/org/freedesktop/portal/inputmethod", IM_IFACE, "CreateInputContext",
                           GLib.Variant("(a(ss))", ([("program", "qubix-pinyin-test")],)))
            commits = []
            bus.signal_subscribe(BUS_NAME, IC_IFACE, "CommitString", path, None,
                                 Gio.DBusSignalFlags.NONE,
                                 lambda *args: commits.append(args[5].unpack()[0]))
            call(path, IC_IFACE, "FocusIn")

            def key(value, state=0):
                return call(path, IC_IFACE, "ProcessKeyEvent",
                            GLib.Variant("(uuubu)", (value, 0, state, False, 0)))[0]

            key(32, 4)  # Native Ctrl+Space trigger, no compositor input injection.
            time.sleep(1)
            handled = []
            context = GLib.MainContext.default()
            for phrase in ("nihao", "hanyu"):
                handled.extend(key(ord(letter)) for letter in phrase)
                key(32)
                deadline = time.monotonic() + 1
                while time.monotonic() < deadline:
                    while context.pending():
                        context.iteration(False)
                    time.sleep(0.01)
            call(path, IC_IFACE, "DestroyIC")
            if personal:
                assert not commits and not any(handled), (commits, handled)
                assert (config / "profile").read_bytes() == original
            else:
                assert all(handled) and commits == ["你好", "汉语"], (commits, handled)
            return {"personal_precedence": personal, "commits": commits, "handled": handled,
                    "group_shortcuts": [hotkeys["EnumerateGroupForwardKeys"],
                                        hotkeys["EnumerateGroupBackwardKeys"]]}
        finally:
            process.terminate()
            process.wait(timeout=10)


with tempfile.TemporaryDirectory(prefix="qubix-pinyin-") as directory:
    root = Path(directory)
    results = [probe(root), probe(root, personal=True)]
    print(json.dumps(results, ensure_ascii=False))
