# Native test helper only; the deployment engine remains Ansible.
import json
import os
import pathlib
import subprocess
import sys
import time

root = pathlib.Path(sys.argv[1])
native_socket = os.environ['NIRI_SOCKET']
assert native_socket != json.loads((root / 'parent.json').read_text())['socket']
assert os.environ['WAYLAND_DISPLAY'] != json.loads((root / 'parent.json').read_text())['display']

def command(args):
    return subprocess.run(args, capture_output=True, text=True, check=True, timeout=8).stdout

def query(name):
    return json.loads(command(['/usr/bin/niri', 'msg', '--json', name]))

def namespaces(value):
    if isinstance(value, dict):
        return {str(value.get('namespace', ''))}.union(*(namespaces(v) for v in value.values()))
    if isinstance(value, list):
        return set().union(*(namespaces(v) for v in value))
    return set()

result = {'socket': native_socket, 'display': os.environ['WAYLAND_DISPLAY'], 'bus': os.environ['DBUS_SESSION_BUS_ADDRESS']}
children = []
try:
    for attempt in range(50):
        layers = query('layers')
        if {'waybar', 'wallpaper'}.issubset(namespaces(layers)):
            break
        time.sleep(0.2)
    else:
        raise AssertionError('Waybar/Swaybg layers did not appear: ' + str(layers))
    result['initial_layers'] = layers
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'wallpaper.png'), '--show-pointer', 'false'])
    for number in range(2):
        log = (root / ('foot-' + str(number) + '.log')).open('w')
        children.append(subprocess.Popen(['/usr/bin/foot', '--config=/etc/qubix/foot.ini', '--app-id=qubix-native-' + str(number), '--title=Qubix native desktop test', '/bin/bash', '--noprofile', '--norc', '-c', 'printf "Qubix OS Playbook\nNative Foot rendering test\n"; sleep 40'], stdout=log, stderr=log))
    for attempt in range(50):
        windows = query('windows')
        if len([w for w in windows if str(w.get('app_id', '')).startswith('qubix-native-')]) == 2:
            break
        time.sleep(0.2)
    else:
        raise AssertionError('Foot windows did not appear: ' + str(windows))
    before_focus = next(w['id'] for w in windows if w.get('is_focused'))
    command(['/usr/bin/niri', 'msg', 'action', 'focus-column-left'])
    time.sleep(0.4)
    after_focus = next(w['id'] for w in query('windows') if w.get('is_focused'))
    assert before_focus != after_focus, 'IPC navigation did not change focus'
    result['windows'] = windows
    result['focus_changed'] = True
    command(['/usr/bin/notify-send', '--app-name=Qubix-native-test', '--expire-time=0', 'Qubix desktop test', 'Native notification and companion smoke test'])
    notifications = json.loads(command(['/usr/bin/makoctl', 'list', '-j']))
    assert 'Qubix desktop test' in str(notifications), 'Notification not received by isolated Mako'
    result['notifications'] = notifications
    log = (root / 'fuzzel.log').open('w')
    launcher = subprocess.Popen(['/usr/bin/fuzzel', '--config=/etc/qubix/fuzzel.ini', '--namespace=qubix-native-fuzzel', '--no-exit-on-keyboard-focus-loss'], stdout=log, stderr=log)
    children.append(launcher)
    for attempt in range(50):
        layers = query('layers')
        if 'qubix-native-fuzzel' in namespaces(layers):
            break
        assert launcher.poll() is None, 'Fuzzel exited before rendering'
        time.sleep(0.2)
    else:
        raise AssertionError('Fuzzel layer did not appear: ' + str(layers))
    result['final_layers'] = layers
    time.sleep(0.5)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'desktop.png'), '--show-pointer', 'false'])
    result['status'] = 'passed'
except Exception as error:
    result['status'] = 'failed'
    result['error'] = str(error)
finally:
    for child in children:
        if child.poll() is None:
            child.terminate()
    (root / 'result.tmp').write_text(json.dumps(result, indent=2))
    os.replace(root / 'result.tmp', root / 'result.json')
