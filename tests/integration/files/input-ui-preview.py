"""Native Fcitx UI exploration in an isolated nested Niri compositor."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time


def run(args, **kwargs):
    return subprocess.check_output(args, text=True, timeout=10, **kwargs)


def wait_for(predicate, label):
    for _ in range(600):
        value = predicate()
        if value:
            return value
        time.sleep(0.1)
    raise AssertionError(label)


root = Path(sys.argv[1])
assert root.parent == Path('/tmp') and root.name.startswith('qubix-input-options.')
assert root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.getuid()

if len(sys.argv) > 2:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gdk, Gio, GLib, Gtk

    assert os.environ['NIRI_SOCKET'] != (root / 'parent-socket').read_text()
    wait_for(lambda: (root / 'sized').exists(), 'Nested output not resized')
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    main_context = GLib.MainContext.default()

    def pump(duration):
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            while main_context.pending():
                main_context.iteration(False)
            time.sleep(0.01)

    css = Gtk.CssProvider()
    css.load_from_data(b'window { background: #101820; } label { color: #cfdae2; font: 16px sans; } '
                       b'entry { background: #283745; color: #f2f5f8; font: 20px sans; padding: 14px; border: 1px solid #56728b; }')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    # GTK's client-side renderer reads standard XDG paths, not FCITX_CONFIG_HOME.
    gtk_conf = Path(os.environ['XDG_CONFIG_HOME']) / 'fcitx5/conf'
    gtk_conf.mkdir(parents=True, exist_ok=True)
    gtk_theme = Path(os.environ['XDG_DATA_HOME']) / 'fcitx5/themes/qubix-preview'
    if not gtk_theme.exists():
        shutil.copytree(root / 'theme', gtk_theme)
    shots = []
    for name, case_name, title, vertical in [
            ('native-pinyin', 'pinyin', 'Current Pinyin - native reference', None),
            ('rime-ice-native', 'ice', 'Rime Ice - native Fcitx UI', None),
            ('rime-ice-horizontal', 'ice', 'Rime Ice - dark horizontal candidates', False),
            ('rime-ice-vertical', 'ice', 'Rime Ice - dark vertical candidates', True)]:
        case = root / case_name
        config = case / 'config'
        data = case / 'data'
        conf = config / 'conf'
        conf.mkdir(exist_ok=True)
        classic = conf / 'classicui.conf'
        if vertical is None:
            classic.write_text('Font=Sans 10\nTheme=default\nVertical Candidate List=False\n')
        else:
            classic.write_text(f'Vertical Candidate List={str(vertical)}\nFont=Noto Sans CJK SC 14\n'
                               'Theme=qubix-preview\nUseDarkTheme=False\nPerScreenDPI=True\n')
            theme = data / 'themes/qubix-preview'
            if not theme.exists():
                shutil.copytree(root / 'theme', theme)
        (gtk_conf / 'classicui.conf').write_text(classic.read_text())
        pump(0.5)
        env = dict(os.environ, FCITX_CONFIG_HOME=str(config), FCITX_DATA_HOME=str(data),
                   GTK_IM_MODULE='fcitx', GSETTINGS_BACKEND='memory')
        env.pop('DISPLAY', None)
        log = (root / (name + '.log')).open('w')
        process = subprocess.Popen(['/usr/share/qubix/bin/qubix-fcitx5', '--disable=xim,xcb'],
                                   env=env, stdout=log, stderr=log)
        window = None
        try:
            def controller(method, parameters=None):
                return bus.call_sync('org.fcitx.Fcitx5', '/controller', 'org.fcitx.Fcitx.Controller1',
                                     method, parameters, None, Gio.DBusCallFlags.NONE, 5000, None).unpack()
            for _ in range(100):
                try:
                    controller('InputMethodGroups')
                    break
                except GLib.Error:
                    pump(0.1)
            else:
                raise AssertionError('Fcitx preview startup failed')
            os.environ['FCITX_CONFIG_HOME'] = str(config)
            os.environ['FCITX_DATA_HOME'] = str(data)
            os.environ['GTK_IM_MODULE'] = 'fcitx'
            window = Gtk.Window(title=title)
            window.set_default_size(900, 420)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
            box.set_border_width(44)
            window.add(box)
            box.pack_start(Gtk.Label(label=title), False, False, 0)
            box.pack_start(Gtk.Label(label='Synthetic test field - no personal content'), False, False, 0)
            entry = Gtk.Entry()
            box.pack_start(entry, False, False, 0)
            window.show_all()
            entry.grab_focus()
            pump(1.0)
            controller('SetCurrentIM', GLib.Variant('(s)', ('pinyin' if case_name == 'pinyin' else 'rime',)))
            if case_name == 'ice':
                def rime_ready():
                    try:
                        return bus.call_sync('org.fcitx.Fcitx5', '/rime', 'org.fcitx.Fcitx.Rime1',
                                             'GetCurrentSchema', None, None, Gio.DBusCallFlags.NONE,
                                             5000, None).unpack()[0] == 'rime_ice'
                    except GLib.Error:
                        return False
                wait_for(rime_ready, 'Rime Ice schema was not ready')
            pump(0.5)
            display = entry.get_display()
            keymap = Gdk.Keymap.get_for_display(display)

            def key(keyval):
                event = Gdk.Event.new(Gdk.EventType.KEY_PRESS)
                event.window = entry.get_window()
                event.send_event = True
                event.time = Gdk.CURRENT_TIME
                event.state = Gdk.ModifierType(0)
                event.keyval = keyval
                success, keys = keymap.get_entries_for_keyval(keyval)
                event.hardware_keycode = keys[0].keycode if success else 0
                event.group = keys[0].group if success else 0
                event.set_device(display.get_default_seat().get_keyboard())
                entry.event(event)
                pump(0.15)

            for letter in 'nihao':
                key(ord(letter))
            pump(1.5)
            popups = [widget for widget in Gtk.Window.list_toplevels()
                      if widget.get_window_type() == Gtk.WindowType.POPUP and widget.get_visible()]
            assert len(popups) == 1, [(w.get_name(), w.get_visible()) for w in Gtk.Window.list_toplevels()]
            popup_size = [popups[0].get_allocated_width(), popups[0].get_allocated_height()]
            if vertical is False:
                assert popup_size[0] > popup_size[1] >= 40, popup_size
            elif vertical is True:
                assert popup_size[1] > popup_size[0] and popup_size[1] >= 150, popup_size
            else:
                assert popup_size[1] < 40, popup_size
            target = root / (name + '.png')
            target.unlink(missing_ok=True)
            run(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(target), '--show-pointer', 'false'])
            wait_for(target.is_file, 'Screenshot was not written')
            key(32)
            pump(0.3)
            assert entry.get_text() == '你好', (name, entry.get_text())
            shots.append({'name': name, 'commit': entry.get_text(), 'popup_size': popup_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        finally:
            if window:
                window.destroy()
                pump(0.2)
            process.terminate()
            process.wait(timeout=10)
            log.close()
            pump(0.3)
    (root / 'inner-result.json').write_text(json.dumps({'screenshots': shots, 'native_gtk_commit': True}))
    sys.exit(0)

session = dict(line.split('=', 1) for line in run(
    ['/usr/bin/systemctl', '--user', 'show-environment']).splitlines() if '=' in line)
parent = {key: session[key] for key in ('NIRI_SOCKET', 'WAYLAND_DISPLAY', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS')}
match = re.search(r'\.(\d+)\.sock$', parent['NIRI_SOCKET'])
assert match and Path(parent['NIRI_SOCKET']).is_socket()
main_pid = int(match[1])
assert (Path('/proc') / str(main_pid) / 'comm').read_text().strip() == 'niri'
(root / 'parent-socket').write_text(parent['NIRI_SOCKET'])
protected = [Path.home() / relative for relative in (
    '.config/niri/config.kdl', '.config/noctalia/config.toml', '.config/dconf/user',
    '.local/state/qubix/noctalia/settings.toml', '.config/fcitx5/config', '.config/fcitx5/profile')]


def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in protected}


before = hashes()
env = dict(os.environ, **parent)
env.pop('NIRI_SOCKET', None)
env['WAYLAND_DISPLAY'] = str(Path(parent['XDG_RUNTIME_DIR']) / parent['WAYLAND_DISPLAY'])
env['XDG_RUNTIME_DIR'] = str(root / 'runtime')
(root / 'runtime').mkdir(mode=0o700, exist_ok=True)
(root / 'sized').unlink(missing_ok=True)
(root / 'inner-result.json').unlink(missing_ok=True)
env['DBUS_SYSTEM_BUS_ADDRESS'] = 'unix:path=' + str(root / 'no-system-bus')
for key, relative in [('HOME', 'home'), ('XDG_CONFIG_HOME', 'config'), ('XDG_STATE_HOME', 'state'),
                      ('XDG_CACHE_HOME', 'cache'), ('XDG_DATA_HOME', 'data')]:
    env[key] = str(root / relative)
    (root / relative).mkdir(mode=0o700, exist_ok=True)
(root / 'config.kdl').write_text(
    'input {\n    keyboard { xkb { layout "us"; }; };\n}\n'
    'hotkey-overlay { skip-at-startup; }\n'
    'layout { default-column-width { proportion 1.0; }; }\n')
(root / 'bus.conf').write_text(
    '<busconfig><type>session</type><listen>unix:tmpdir=/tmp</listen>'
    '<policy context="default"><allow send_destination="*"/>'
    '<allow receive_sender="*"/><allow own="*"/></policy></busconfig>')
result = {}
with (root / 'nested.log').open('w') as log:
    process = subprocess.Popen([
        '/usr/bin/dbus-run-session', '--config-file', str(root / 'bus.conf'), '--',
        '/usr/bin/niri', '--config', str(root / 'config.kdl')],
        env=env, stdout=log, stderr=log, start_new_session=True)
    try:
        def owned_window():
            windows = json.loads(run(['/usr/bin/niri', 'msg', '--json', 'windows'], env=dict(env, **parent)))
            return next((w for w in windows if w.get('pid') and os.getpgid(w['pid']) == process.pid), None)
        window = wait_for(owned_window, 'Private nested Niri window did not appear')
        for action in [('move-window-to-floating',), ('set-window-width', '900'), ('set-window-height', '520')]:
            run(['/usr/bin/niri', 'msg', 'action', action[0], '--id', str(window['id']), *action[1:]],
                env=dict(env, **parent))
        nested_socket = wait_for(lambda: next((root / 'runtime').glob('niri.*.sock'), None),
                                 'Nested IPC socket missing')
        nested_display = wait_for(lambda: next((root / 'runtime').glob('wayland-[0-9]'), None),
                                  'Nested Wayland socket missing')
        client_env = dict(env, NIRI_SOCKET=str(nested_socket), WAYLAND_DISPLAY=str(nested_display))
        client_env.pop('DBUS_SESSION_BUS_ADDRESS', None)
        client = subprocess.Popen(['/usr/bin/dbus-run-session', '--config-file', str(root / 'bus.conf'),
                                   '--', '/usr/bin/python3', str(root / 'preview.py'), str(root), 'inner'],
                                  env=client_env, stdout=log, stderr=log)
        (root / 'sized').touch()
        wait_for(lambda: (root / 'inner-result.json').is_file() or client.poll() is not None,
                 'Native preview did not finish')
        assert (root / 'inner-result.json').is_file(), (root / 'nested.log').read_text()
        result = json.loads((root / 'inner-result.json').read_text())
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        remaining = []
        for entry in Path('/proc').iterdir():
            if entry.name.isdecimal():
                try:
                    variables = (entry / 'environ').read_bytes().split(b'\0')
                    if os.getpgid(int(entry.name)) == process.pid or (
                        ('HOME=' + env['HOME']).encode() in variables):
                        remaining.append(int(entry.name))
                except (ProcessLookupError, FileNotFoundError, PermissionError):
                    pass
        for pid in remaining:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        def active_group():
            active = []
            for pid in remaining:
                try:
                    if (Path('/proc') / str(pid) / 'stat').read_text().split()[2] != 'Z':
                        active.append(pid)
                except FileNotFoundError:
                    pass
            return active
        wait_for(lambda: not active_group(), 'Preview processes remain after cleanup')
        assert hashes() == before, 'Personal desktop settings changed'
        assert (Path('/proc') / str(main_pid) / 'comm').read_text().strip() == 'niri'
        result.update(cleanup_remaining=0, personal_settings_preserved=True, primary_niri_preserved=True,
                      authentication_tested=False, boot_tested=False)
(root / 'result.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result))
