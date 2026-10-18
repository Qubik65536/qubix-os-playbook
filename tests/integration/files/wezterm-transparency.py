"""Native test: compare composed backgrounds in a private nested Niri session."""
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

root = Path(sys.argv[1])
assert root.parent == Path('/tmp') and root.name.startswith('qubix-wezterm-scene-')
assert root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.getuid()
parent = dict(line.split('=', 1) for line in subprocess.check_output(
    ['systemctl', '--user', 'show-environment'], text=True).splitlines() if '=' in line)
parent_env = dict(os.environ, **{k: parent[k] for k in (
    'WAYLAND_DISPLAY', 'NIRI_SOCKET', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS')})
def run(args, env):
    return subprocess.check_output(args, env=env, text=True, stderr=subprocess.PIPE, timeout=20).strip()
def windows(env):
    return json.loads(run(['niri', 'msg', '--json', 'windows'], env))
before = {(w['id'], w.get('pid')) for w in windows(parent_env)}
focus = next((w['id'] for w in windows(parent_env) if w.get('is_focused')), None)
boot = Path('/proc/sys/kernel/random/boot_id').read_text()
private_home = root / 'home'
config_dir = private_home / '.config/wezterm'
config_dir.mkdir(parents=True)
for name in ('wezterm.lua', 'colors/KAMSuperuser.toml', 'colors/oxocarbon-dark.toml'):
    destination = config_dir / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path.home() / '.config/wezterm' / name, destination)
protected = [Path.home() / p for p in ('.config/niri/config.kdl', '.config/dconf/user', '.config/wezterm/wezterm.lua')]
def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in protected}
original_hashes = hashes()
base = (root / 'theme.kdl').read_text()
def config(style, colour):
    theme = base.replace('background-color "#1B242C"', 'background-color "' + colour + '"')
    if style == 'before':
        theme = theme.replace('draw-border-with-background false', 'draw-border-with-background true')
    (root / 'config.kdl').write_text('hotkey-overlay { skip-at-startup; }\n' + theme)
config('before', '#e02040')
env = dict(parent_env, HOME=str(private_home), XDG_CONFIG_HOME=str(private_home / '.config'),
           XDG_CACHE_HOME=str(private_home / '.cache'), XDG_STATE_HOME=str(private_home / '.local/state'),
           XDG_DATA_HOME=str(private_home / '.local/share'))
env.pop('NIRI_SOCKET', None)
env.pop('WEZTERM_CONFIG_FILE', None)
log = (root / 'session.log').open('w')
compositor = subprocess.Popen(['dbus-run-session', '--', 'niri', '--config', str(root / 'config.kdl')],
    env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
terminal = None
try:
    socket = None
    for _ in range(100):
        for candidate in Path(parent['XDG_RUNTIME_DIR']).glob('niri.*.sock'):
            match = re.search(r'\.(\d+)\.sock$', candidate.name)
            try:
                if match and os.getpgid(int(match[1])) == compositor.pid:
                    socket = candidate
                    break
            except ProcessLookupError:
                pass
        if socket:
            break
        assert compositor.poll() is None, (root / 'session.log').read_text()
        time.sleep(0.1)
    assert socket, 'No private compositor socket'
    nested_env = dict(env, NIRI_SOCKET=str(socket), WAYLAND_DISPLAY=socket.name[5:].rsplit('.', 2)[0])
    for _ in range(50):
        owned = [w for w in windows(parent_env) if w.get('pid') and os.getpgid(w['pid']) == compositor.pid]
        if owned:
            for action, size in [('set-window-width', '1000'), ('set-window-height', '700')]:
                run(['niri', 'msg', 'action', 'move-window-to-floating', '--id', str(owned[0]['id'])], parent_env)
                run(['niri', 'msg', 'action', action, '--id', str(owned[0]['id']), size], parent_env)
            break
        time.sleep(0.1)
    terminal = subprocess.Popen(['/usr/bin/wezterm', 'start', '--always-new-process', '--', '/bin/bash', '--noprofile',
        '--norc', '-c', 'printf "Synthetic WezTerm transparency test\\nOpaque text, translucent background\\n"; sleep 180'],
        env=nested_env, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
    for _ in range(100):
        if windows(nested_env):
            break
        assert terminal.poll() is None, (root / 'session.log').read_text()
        time.sleep(0.1)
    assert len(windows(nested_env)) == 1
    captures = []
    for style in ('before', 'after'):
        for label, colour in [('red', '#e02040'), ('blue', '#2040e0')]:
            config(style, colour)
            run(['niri', 'msg', 'action', 'load-config-file'], nested_env)
            time.sleep(0.7)
            path = root / (style + '-' + label + '.png')
            run(['niri', 'msg', 'action', 'screenshot-screen', '--path', str(path), '--show-pointer', 'false'], nested_env)
            for _ in range(50):
                if path.exists() and path.stat().st_size > 1000:
                    break
                time.sleep(0.1)
            assert path.exists()
            captures.append(path.name)
    print(json.dumps({'directory': str(root), 'captures': captures, 'private_scene': True}))
finally:
    for process in (terminal, compositor):
        if process:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
    for _ in range(50):
        if {(w['id'], w.get('pid')) for w in windows(parent_env)} == before:
            break
        time.sleep(0.1)
    if focus is not None:
        run(['niri', 'msg', 'action', 'focus-window', '--id', str(focus)], parent_env)
    assert {(w['id'], w.get('pid')) for w in windows(parent_env)} == before
    assert original_hashes == hashes()
    assert boot == Path('/proc/sys/kernel/random/boot_id').read_text()
