"""Native input comparison on a private bus; no physical key injection or live writes."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from gi.repository import Gio, GLib

root = Path(sys.argv[1])
assert root.parent == Path('/tmp') and root.name.startswith('qubix-input-options.')
assert root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.getuid()
BUS = 'org.fcitx.Fcitx5'
IC = 'org.fcitx.Fcitx.InputContext1'
CTRL = 'org.fcitx.Fcitx.Controller1'
context = GLib.MainContext.default()


def pump(duration):
    deadline = time.monotonic() + duration
    while time.monotonic() < deadline:
        while context.pending():
            context.iteration(False)
        time.sleep(0.01)


def run_case(name, engine, schema=None):
    case = root / name
    config = case / 'config'
    data = case / 'data'
    config.mkdir(parents=True)
    data.mkdir()
    (config / 'profile').write_text(
        f'[Groups/0]\nName=Comparison\nDefault Layout=us\nDefaultIM={engine}\n'
        f'[Groups/0/Items/0]\nName=keyboard-us\n[Groups/0/Items/1]\nName={engine}\n'
        '[GroupOrder]\n0=Comparison\n')
    if schema:
        rime = data / 'rime'
        if schema == 'rime_ice':
            shutil.copytree(next((root / 'ice').glob('rime-ice-*')), rime)
        else:
            rime.mkdir()
        (rime / 'default.custom.yaml').write_text(
            f'patch:\n  schema_list:\n    - schema: {schema}\n  menu/page_size: 5\n')
    env = dict(os.environ, FCITX_CONFIG_HOME=str(config), FCITX_DATA_HOME=str(data),
               XDG_CACHE_HOME=str(case / 'cache'), DBUS_SYSTEM_BUS_ADDRESS='unix:path=' + str(root / 'no-system-bus'))
    env.pop('DISPLAY', None)
    env.pop('WAYLAND_DISPLAY', None)
    with (case / 'fcitx.log').open('w') as log:
        process = subprocess.Popen(['/usr/share/qubix/bin/qubix-fcitx5', '--disable=wayland,xim,xcb'],
                                   env=env, stdout=log, stderr=log)
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)

            def call(path, interface, method, parameters=None):
                return bus.call_sync(BUS, path, interface, method, parameters, None,
                                     Gio.DBusCallFlags.NONE, 10000, None).unpack()

            for _ in range(100):
                try:
                    group = call('/controller', CTRL, 'InputMethodGroupInfo',
                                 GLib.Variant('(s)', ('Comparison',)))
                    assert engine in [entry[0] for entry in group[1]], group
                    break
                except GLib.Error:
                    assert process.poll() is None, (case / 'fcitx.log').read_text()
                    time.sleep(0.1)
            else:
                raise AssertionError('Input daemon startup failed')
            path, _ = call('/org/freedesktop/portal/inputmethod', 'org.fcitx.Fcitx.InputMethod1',
                           'CreateInputContext', GLib.Variant('(a(ss))', ([('program', 'qubix-comparison')],)))
            updates, commits = [], []
            bus.signal_subscribe(BUS, IC, 'UpdateClientSideUI', path, None, Gio.DBusSignalFlags.NONE,
                                 lambda *args: updates.append(args[5].unpack()))
            bus.signal_subscribe(BUS, IC, 'CommitString', path, None, Gio.DBusSignalFlags.NONE,
                                 lambda *args: commits.append(args[5].unpack()[0]))
            call(path, IC, 'SetCapability', GLib.Variant('(t)', ((1 << 39) | (1 << 1) | (1 << 4),)))
            call(path, IC, 'FocusIn')
            call('/controller', CTRL, 'SetCurrentIM', GLib.Variant('(s)', (engine,)))

            def key(value):
                return call(path, IC, 'ProcessKeyEvent', GLib.Variant('(uuubu)', (value, 0, 0, False, 0)))[0]

            # Rime compiles schema dictionaries on its first run; poll only our private context.
            for _ in range(120):
                key(ord('n'))
                pump(0.1)
                if any(update[4] for update in updates):
                    key(0xff1b)
                    break
                key(0xff1b)
                time.sleep(0.5)
            else:
                raise AssertionError('No candidates after private schema deployment: ' + (case / 'fcitx.log').read_text()[-4000:])
            samples = []
            for phrase in ('nihao', 'hanyu', 'jisuanji', 'kaifazhe', 'rengongzhineng', 'shurufa', 'weixin', 'github'):
                key(0xff1b)
                updates.clear()
                commits.clear()
                for letter in phrase:
                    key(ord(letter))
                pump(0.3)
                candidates = next((update[4] for update in reversed(updates) if update[4]), [])
                assert candidates, (name, phrase, updates)
                key(32)
                pump(0.1)
                samples.append({'input': phrase, 'candidates': [pair[1] for pair in candidates], 'commit': ''.join(commits)})
            assert samples[0]['commit'] == '你好', samples[0]
            assert samples[1]['commit'] == '汉语', samples[1]
            call(path, IC, 'DestroyIC')
            return {'name': name, 'engine': engine, 'schema': schema, 'samples': samples}
        finally:
            process.terminate()
            process.wait(timeout=10)


protected = [Path.home() / p for p in ('.config/fcitx5/config', '.config/fcitx5/profile',
             '.local/share/fcitx5/rime/default.custom.yaml', '.config/niri/config.kdl')]

def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in protected}

before = hashes()
pids = subprocess.check_output(['pgrep', '-x', 'niri'], text=True).split()
results = [run_case('pinyin', 'pinyin'), run_case('luna', 'rime', 'luna_pinyin_simp'),
           run_case('ice', 'rime', 'rime_ice')]
assert before == hashes(), 'Personal input/desktop configuration changed'
assert pids == subprocess.check_output(['pgrep', '-x', 'niri'], text=True).split()
(root / 'comparison.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(json.dumps(results, ensure_ascii=False))
