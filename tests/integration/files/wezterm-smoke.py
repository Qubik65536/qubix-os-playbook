import json
import os
from pathlib import Path
import subprocess
import tempfile
import hashlib
import shutil
import time


def run(args):
    return subprocess.run(args, env=session_env, capture_output=True, text=True, check=True, timeout=20).stdout.strip()

session_env = dict(os.environ)
for line in subprocess.check_output(['systemctl', '--user', 'show-environment'], text=True).splitlines():
    if '=' in line:
        key, value = line.split('=', 1)
        if key in ('WAYLAND_DISPLAY', 'NIRI_SOCKET', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS'):
            session_env[key] = value
root = Path(tempfile.mkdtemp(prefix='qubix-terminal-acceptance-'))
for name in ('home', 'config', 'cache', 'state', 'data'):
    (root / name).mkdir(mode=0o700)
private_env = dict(session_env, HOME=str(root / 'home'), XDG_CONFIG_HOME=str(root / 'config'),
                   XDG_CACHE_HOME=str(root / 'cache'), XDG_STATE_HOME=str(root / 'state'), XDG_DATA_HOME=str(root / 'data'))
protected = [Path.home() / name for name in ('.config/wezterm/wezterm.lua', '.wezterm.lua', '.config/dconf/user')]
before_hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None for path in protected}
boot_id = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
private_env.pop('WEZTERM_CONFIG_FILE', None)
windows = json.loads(run(['niri', 'msg', '--json', 'windows']))
before = {(window['id'], window.get('pid')) for window in windows}
focused = next((window['id'] for window in windows if window.get('is_focused')), None)
content = 'printf "Qubix OS Playbook\\nTerminal acceptance test\\n\\nParu + Homebrew + WezTerm\\nPersonal configuration preserved\\n\\n"; printf "\\033[31mRed  \\033[32mGreen  \\033[34mBlue\\033[0m\\n"; sleep 120'
results = {}
try:
    for name in ('reference', 'customized'):
        app_id = 'qubix-terminal-' + name
        if name == 'reference':
            argv = ['/usr/bin/wezterm', '--skip-config', 'start', '--always-new-process', '--class=' + app_id,
                    '--', '/bin/bash', '--noprofile', '--norc', '-c', content]
        else:
            argv = ['/usr/share/qubix/bin/qubix-wezterm', 'start', '--always-new-process', '--class=' + app_id,
                    '--', '/bin/bash', '--noprofile', '--norc', '-c', content]
        with (root / (name + '.log')).open('w') as log:
            process = subprocess.Popen(argv, env=private_env, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                       start_new_session=True)
        window = None
        try:
            for attempt in range(100):
                matches = [w for w in json.loads(run(['niri', 'msg', '--json', 'windows'])) if w.get('app_id') == app_id]
                if matches:
                    window = matches[0]
                    break
                if process.poll() is not None:
                    raise RuntimeError((root / (name + '.log')).read_text())
                time.sleep(0.2)
            assert window, name + ' window did not appear'
            time.sleep(1)
            image = root / (name + '.png')
            run(['niri', 'msg', 'action', 'screenshot-window', '--id', str(window['id']), '--path', str(image)])
            for attempt in range(50):
                if image.is_file() and image.stat().st_size > 1000:
                    break
                time.sleep(0.1)
            assert image.is_file() and image.stat().st_size > 1000
            results[name] = {'app_id': window['app_id'], 'screenshot': str(image)}
        finally:
            if window:
                run(['niri', 'msg', 'action', 'close-window', '--id', str(window['id'])])
            process.wait(timeout=15)
    if focused is not None:
        run(['niri', 'msg', 'action', 'focus-window', '--id', str(focused)])
    after = {(w['id'], w.get('pid')) for w in json.loads(run(['niri', 'msg', '--json', 'windows']))}
    assert before == after, 'Application windows changed'
    results['application_windows_preserved'] = True
    assert before_hashes == {str(path): hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None for path in protected}
    assert boot_id == Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    results['personal_settings_preserved'] = True
    results['boot_id_preserved'] = True
    results['directory'] = str(root)
    print(json.dumps(results))
except Exception:
    shutil.rmtree(root)
    raise
