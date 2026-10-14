# Native test helper only; requires an already-running main Niri service.
import json
import os
import pathlib
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
main_pid = subprocess.check_output(['systemctl', '--user', 'show', 'niri.service', '--property=MainPID', '--value'], text=True).strip()
assert main_pid != '0' and pathlib.Path(parent['NIRI_SOCKET']).is_socket()
(root / 'parent.json').write_text(json.dumps({'socket': parent['NIRI_SOCKET'], 'display': parent['WAYLAND_DISPLAY']}))
environment = dict(os.environ, **parent)
environment.pop('NIRI_SOCKET', None)
environment['HOME'] = str(root / 'home')
environment['XDG_CONFIG_HOME'] = str(root / 'home/.config')
environment['XDG_CACHE_HOME'] = str(root / 'home/.cache')
environment['XDG_STATE_HOME'] = str(root / 'home/.local/state')
for directory in ['HOME', 'XDG_CONFIG_HOME', 'XDG_CACHE_HOME', 'XDG_STATE_HOME']:
    pathlib.Path(environment[directory]).mkdir(parents=True, exist_ok=True)
log = (root / 'session.log').open('w')
process = subprocess.Popen(['/usr/bin/dbus-run-session', '--', '/usr/bin/niri', '--config', '/etc/niri/qubix/config.kdl', '--', '/usr/bin/python3', str(root / 'inner.py'), str(root)], env=environment, stdout=log, stderr=log, start_new_session=True)
result = {'status': 'failed', 'error': 'No result from nested compositor'}
try:
    for attempt in range(200):
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
    result['native_compositor_preserved'] = after_pid == main_pid
    result['cleanup_signalled_remaining'] = len(remaining)
    (root / 'result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
assert result['status'] == 'passed', result.get('error')
assert result['native_environment_preserved'] and result['native_compositor_preserved']
assert result['cleanup_remaining'] == 0, 'Temporary test processes remain'
