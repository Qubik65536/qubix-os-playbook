# Native test helper only; requires an already-running main Niri compositor.
import json
import hashlib
import os
import pathlib
import re
import signal
import subprocess
import sys
import time

def interrupted(signum, frame):
    raise KeyboardInterrupt('Native smoke test interrupted')

signal.signal(signal.SIGTERM, interrupted)
signal.signal(signal.SIGHUP, interrupted)

root = pathlib.Path(sys.argv[1])
assert root.parent == pathlib.Path('/tmp') and root.name.startswith('qubix-native-smoke.')
assert root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.getuid()
session = dict(line.split('=', 1) for line in subprocess.check_output(['systemctl', '--user', 'show-environment'], text=True).splitlines() if '=' in line)
keys = ['WAYLAND_DISPLAY', 'NIRI_SOCKET', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS']
parent = {k: session[k] for k in keys}
service_pid = subprocess.check_output(['systemctl', '--user', 'show', 'niri.service', '--property=MainPID', '--value'], text=True).strip()
socket_pid = re.search(r'\.(\d+)\.sock$', parent['NIRI_SOCKET'])
assert socket_pid and pathlib.Path(parent['NIRI_SOCKET']).is_socket()
main_pid = int(socket_pid[1])
main_process = pathlib.Path('/proc') / str(main_pid)
assert main_process.stat().st_uid == os.getuid() and (main_process / 'comm').read_text().strip() == 'niri'
assert service_pid in ('0', str(main_pid)), 'The service and selected session disagree'
native_paths = [pathlib.Path.home() / p for p in (
    '.config/niri/config.kdl', '.config/noctalia/config.toml', '.config/dconf/user',
    '.local/state/noctalia/settings.toml')]

def native_hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in native_paths}

before_hashes = native_hashes()
(root / 'parent.json').write_text(json.dumps({'socket': parent['NIRI_SOCKET'], 'display': parent['WAYLAND_DISPLAY']}))
environment = dict(os.environ, **parent)
environment.pop('NIRI_SOCKET', None)
environment['HOME'] = str(root / 'home')
environment['XDG_CONFIG_HOME'] = str(root / 'home/.config')
environment['XDG_CACHE_HOME'] = str(root / 'home/.cache')
environment['XDG_STATE_HOME'] = str(root / 'home/.local/state')
environment['XDG_DATA_HOME'] = str(root / 'home/.local/share')
for directory in ['HOME', 'XDG_CONFIG_HOME', 'XDG_CACHE_HOME', 'XDG_STATE_HOME', 'XDG_DATA_HOME']:
    pathlib.Path(environment[directory]).mkdir(parents=True, exist_ok=True)
test_state = pathlib.Path(environment['XDG_STATE_HOME']) / 'qubix/noctalia'
test_state.mkdir(parents=True, mode=0o700)
(test_state / 'settings.toml').write_text('[shell]\npolkit_agent = false\nclipboard_enabled = false\noffline_mode = true\n[lockscreen]\nenabled = false\n')
log = (root / 'session.log').open('w')
process = subprocess.Popen(['/usr/bin/dbus-run-session', '--', '/usr/bin/niri', '--config', str(root / 'config.kdl'), '--', '/usr/bin/python3', str(root / 'inner.py'), str(root)], env=environment, stdout=log, stderr=log, start_new_session=True)
result = {'status': 'failed', 'error': 'No result from nested compositor'}
try:
    for attempt in range(350):
        if (root / 'result.json').exists():
            result = json.loads((root / 'result.json').read_text())
            break
        if process.poll() is not None:
            break
        time.sleep(0.2)
    else:
        result['error'] = 'Nested test timed out'
    if result.get('socket'):
        assert result['socket'] != parent['NIRI_SOCKET']
        subprocess.run(['/usr/bin/niri', 'msg', 'action', 'quit', '--skip-confirmation'], env=dict(environment, NIRI_SOCKET=result['socket']), capture_output=True, timeout=5, check=False)
finally:
    if process.poll() is None:
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
    # Match this launch's group, socket or private bus; never the original session bus.
    test_bus = result.get('bus', '')
    assert not test_bus or test_bus != parent['DBUS_SESSION_BUS_ADDRESS']

    def test_processes():
        matches = []
        for entry in pathlib.Path('/proc').iterdir():
            if not entry.name.isdecimal() or int(entry.name) == os.getpid():
                continue
            try:
                pid = int(entry.name)
                variables = (entry / 'environ').read_bytes().split(b'\0')
                socket_match = result.get('socket') and ('NIRI_SOCKET=' + result['socket']).encode() in variables
                bus_match = test_bus and ('DBUS_SESSION_BUS_ADDRESS=' + test_bus).encode() in variables
                if os.getpgid(pid) == process.pid or socket_match or bus_match:
                    matches.append(pid)
            except (PermissionError, FileNotFoundError, ProcessLookupError):
                pass
        return matches

    remaining = test_processes()
    for pid in remaining:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    for attempt in range(10):
        if not test_processes():
            break
        time.sleep(0.1)
    for pid in test_processes():
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    time.sleep(0.1)
    result['cleanup_remaining'] = len(test_processes())
    after = dict(line.split('=', 1) for line in subprocess.check_output(['systemctl', '--user', 'show-environment'], text=True).splitlines() if '=' in line)
    after_pid = subprocess.check_output(['systemctl', '--user', 'show', 'niri.service', '--property=MainPID', '--value'], text=True).strip()
    result['native_environment_preserved'] = all(after.get(k) == v for k, v in parent.items())
    result['native_compositor_preserved'] = after_pid == service_pid and main_process.exists() and (main_process / 'comm').read_text().strip() == 'niri'
    result['native_configuration_preserved'] = native_hashes() == before_hashes
    result['cleanup_signalled_remaining'] = len(remaining)
    (root / 'result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
assert result['status'] == 'passed', result.get('error')
assert result['native_environment_preserved'] and result['native_compositor_preserved']
assert result['native_configuration_preserved'], 'Native Niri/Noctalia/dconf settings changed'
assert result['cleanup_remaining'] == 0, 'Temporary test processes remain'
