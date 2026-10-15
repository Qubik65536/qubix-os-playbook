# Native test helper only; the deployment engine remains Ansible.
import json
import configparser
import shlex
import os
import pathlib
import re
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

def shell(*args):
    output = command([str(root / 'qubix-noctalia'), 'msg', *args]).strip()
    assert not output.lower().startswith('error:'), output
    return output

def namespaces(value):
    if isinstance(value, dict):
        return {str(value.get('namespace', ''))}.union(*(namespaces(v) for v in value.values()))
    if isinstance(value, list):
        return set().union(*(namespaces(v) for v in value))
    return set()

def wait_for(predicate, label):
    for attempt in range(50):
        value = predicate()
        if value:
            return value
        time.sleep(0.2)
    raise AssertionError(label + ' did not appear')

def focused_window():
    return next(w for w in query('windows') if w.get('is_focused'))

def configured_resize(key):
    # Exercise the action actually assigned in this rendered candidate.
    line = next(line for line in (root / 'config.kdl').read_text().splitlines()
                if line.lstrip().startswith(key + ' '))
    match = re.search(r'\{\s*(set-column-width|set-window-height|reset-window-height)(?:\s+"([^"]+)")?;\s*\}', line)
    assert match, 'Expected a supported resize action for ' + key
    args = ['/usr/bin/niri', 'msg', 'action', match[1]]
    if match[2] is not None:
        args.append(match[2])
    command(args)

result = {'socket': native_socket, 'display': os.environ['WAYLAND_DISPLAY'], 'bus': os.environ['DBUS_SESSION_BUS_ADDRESS']}
children = []
try:
    validation = command(['/usr/bin/noctalia', 'config', 'validate', str(root / 'config/noctalia/config.toml')])
    assert not re.search(r'(?m)^(WARN|ERROR)', validation), validation
    result['shell_config_validated'] = True
    command([str(root / 'qubix-output-defaults'), '--once'])
    result['outputs'] = query('outputs')
    assert all(output['logical']['scale'] == 1 for output in result['outputs'].values() if output.get('logical'))
    result['output_scale_default'] = 1
    def initial_layers():
        layers = query('layers')
        names = namespaces(layers)
        return layers if 'noctalia-wallpaper' in names and any(n.startswith('noctalia-bar-') for n in names) and 'noctalia-dock' not in names else None
    result['initial_layers'] = wait_for(initial_layers, 'Noctalia bar/wallpaper layers without a dock')
    result['palette'] = shell('color-scheme-get')
    assert result['palette'] == 'custom Qubix', result['palette']
    result['wallpaper'] = shell('wallpaper-get')
    assert result['wallpaper'] == str(root / 'assets/wallpaper.png'), result['wallpaper']
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'wallpaper.png'), '--show-pointer', 'false'])
    for number in range(2):
        log = (root / ('foot-' + str(number) + '.log')).open('w')
        children.append(subprocess.Popen(['/usr/bin/foot', '--config=' + str(root / 'foot.ini'), '--app-id=qubix-native-' + str(number), '--title=Qubix Noctalia desktop test', '/bin/bash', '--noprofile', '--norc', '-c', 'printf "Qubix OS Playbook\\nNoctalia and rounded window test\\n"; sleep 60'], stdout=log, stderr=log))
    def foot_windows():
        windows = query('windows')
        return windows if len([w for w in windows if str(w.get('app_id', '')).startswith('qubix-native-')]) == 2 else None
    windows = wait_for(foot_windows, 'Foot windows')
    before_focus = next(w['id'] for w in windows if w.get('is_focused'))
    command(['/usr/bin/niri', 'msg', 'action', 'focus-column-left'])
    time.sleep(0.4)
    after_focus = next(w['id'] for w in query('windows') if w.get('is_focused'))
    assert before_focus != after_focus, 'IPC navigation did not change focus'
    result['windows'] = windows
    result['focus_changed'] = True
    width_before = focused_window()['layout']['tile_size'][0]
    configured_resize('Mod+Ctrl+Right')
    width_grown = wait_for(lambda: focused_window()['layout']['tile_size'][0]
                           if focused_window()['layout']['tile_size'][0] > width_before + 1 else None,
                           'Column width growth')
    configured_resize('Mod+Ctrl+Left')
    wait_for(lambda: focused_window()['layout']['tile_size'][0] < width_grown - 1, 'Column width reduction')
    full_height = focused_window()['layout']['tile_size'][1]
    command(['/usr/bin/niri', 'msg', 'action', 'consume-or-expel-window-right'])
    wait_for(lambda: focused_window()['layout']['tile_size'][1] < full_height - 10, 'Stacked test windows')
    height_before = focused_window()['layout']['tile_size'][1]
    configured_resize('Mod+Ctrl+Down')
    height_grown = wait_for(lambda: focused_window()['layout']['tile_size'][1]
                            if focused_window()['layout']['tile_size'][1] > height_before + 1 else None,
                            'Window height growth')
    configured_resize('Mod+Ctrl+Up')
    wait_for(lambda: focused_window()['layout']['tile_size'][1] < height_grown - 1, 'Window height reduction')
    configured_resize('Mod+Ctrl+R')
    wait_for(lambda: abs(query('windows')[0]['layout']['tile_size'][1]
                         - query('windows')[1]['layout']['tile_size'][1]) <= 2, 'Automatic window height reset')
    result['resize'] = {'width_before': width_before, 'width_grown': width_grown,
                        'height_before': height_before, 'height_grown': height_grown, 'reset': True}
    owner = command(['/usr/bin/dbus-send', '--session', '--print-reply', '--dest=org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus.GetConnectionUnixProcessID', 'string:org.freedesktop.Notifications'])
    owner_pid = int(re.search(r'uint32 (\d+)', owner)[1])
    assert (pathlib.Path('/proc') / str(owner_pid) / 'comm').read_text().strip() == 'noctalia'
    result['notification_owner'] = 'noctalia'
    command(['/usr/bin/notify-send', '--app-name=Qubix-native-test', '--expire-time=0', 'Qubix desktop test', 'Noctalia notification and rounded shell smoke test'])
    wait_for(lambda: 'noctalia-notification' in namespaces(query('layers')), 'Noctalia notification')
    shell('panel-open', 'launcher')
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'launcher', 'Noctalia launcher')
    result['launcher_status'] = json.loads(shell('status'))
    result['final_layers'] = query('layers')
    time.sleep(0.5)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'desktop.png'), '--show-pointer', 'false'])
    shell('panel-close', 'launcher')
    power_entry = root / 'home/.local/share/applications/qubix-power.desktop'
    validator = pathlib.Path('/usr/bin/desktop-file-validate')
    if validator.is_file():
        command([str(validator), str(power_entry)])
        result['power_entry_native_validation'] = 'passed'
    else:
        result['power_entry_native_validation'] = 'unavailable'
    desktop = configparser.ConfigParser(interpolation=None)
    desktop.read(power_entry)
    power_args = shlex.split(desktop['Desktop Entry']['Exec'])
    assert power_args == [str(root / 'qubix-noctalia'), 'msg', 'panel-toggle', 'session'], power_args
    command(power_args) # Open the configured menu; never execute a power action.
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'session', 'Power options menu')
    time.sleep(0.4)
    result['power_menu_status'] = json.loads(shell('status'))
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'power-menu.png'), '--show-pointer', 'false'])
    shell('panel-close', 'session')
    shell('panel-open', 'launcher', 'reboot')
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'launcher', 'Launcher power search')
    time.sleep(0.4)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'power-search.png'), '--show-pointer', 'false'])
    result['launcher_power_query'] = 'reboot'
    shell('panel-close', 'launcher')
    shell('panel-open', 'launcher', '/session')
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'launcher', 'Launcher session provider')
    time.sleep(0.4)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'power-options.png'), '--show-pointer', 'false'])
    shell('panel-close', 'launcher')
    shell('panel-open', 'control-center', 'notifications')
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'control-center', 'Notification centre')
    result['notifications_status'] = json.loads(shell('status'))
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'notifications.png'), '--show-pointer', 'false'])
    shell('panel-close', 'control-center')
    shell('panel-open', 'qubix/shortcuts:cheatsheet')
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'qubix/shortcuts:cheatsheet', 'Shortcut panel')
    result['shortcuts_status'] = json.loads(shell('status'))
    time.sleep(0.4)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'shortcuts.png'), '--show-pointer', 'false'])
    shell('plugin', 'qubix/shortcuts:cheatsheet', 'all', 'search', 'launcher')
    time.sleep(0.3)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'shortcuts-search.png'), '--show-pointer', 'false'])
    shell('plugin', 'qubix/shortcuts:cheatsheet', 'all', 'search', 'resize')
    time.sleep(0.3)
    command(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / 'resize-shortcuts.png'), '--show-pointer', 'false'])
    shell('panel-close', 'qubix/shortcuts:cheatsheet')
    wait_for(lambda: not json.loads(shell('status')).get('panelOpen'), 'Shortcut panel close')
    result['shortcuts_search_dispatched'] = True
    result['shortcuts_closed'] = True
    assert 'noctalia-dock' not in namespaces(query('layers')), 'Disabled dock still has a surface'
    result['dock_absent'] = True
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
