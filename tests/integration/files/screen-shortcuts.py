# Native SSH acceptance helper: moves only its own temporary window.
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import time

session = dict(line.split('=', 1) for line in subprocess.check_output(
    ['systemctl', '--user', 'show-environment'], text=True).splitlines() if '=' in line)
env = dict(os.environ, **session)
socket = Path(env['NIRI_SOCKET'])
assert socket.is_socket()
pid = int(re.search(r'\.(\d+)\.sock$', str(socket))[1])
assert Path(f'/proc/{pid}/comm').read_text().strip() == 'niri'
assert b'/etc/niri/qubix/config.kdl' in Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
config = Path('/etc/niri/qubix/config.kdl').read_text()
shortcuts = json.loads(Path('/usr/share/qubix/noctalia/plugins/shortcuts/bindings.json').read_text())

def run(*args):
    return subprocess.check_output(args, env=env, text=True, timeout=10)

def query(name):
    return json.loads(run('niri', 'msg', '-j', name))

def action(*args):
    run('niri', 'msg', 'action', *args)
    time.sleep(0.15)

def binding(key, expected, *arguments):
    lines = [line for line in config.splitlines() if line.strip().startswith(key + ' ')]
    assert len(lines) == 1, 'Missing or duplicate installed binding: ' + key
    line = lines[0]
    configured = shlex.split(re.search(r'\{\s*(.+?);\s*\}', line)[1])
    assert configured == [expected, *arguments], line
    title = re.search(r'hotkey-overlay-title="([^"]+)"', line)[1]
    assert [key, title] in shortcuts
    action(*configured)

paths = [Path.home() / p for p in ('.config/niri/config.kdl', '.config/noctalia/config.toml',
         '.local/state/qubix/noctalia/settings.toml', '.config/wezterm/wezterm.lua')]

def hashes():
    return [hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in paths]

before_hashes = hashes()
before_windows = {w['id']: w['workspace_id'] for w in query('windows')}
before_focus = query('focused-window')
before_output = query('focused-output')['name']
before_outputs = query('outputs')
boot = Path('/proc/sys/kernel/random/boot_id').read_text()
assert set(before_outputs) == {'eDP-1', 'HDMI-A-1'}, 'This acceptance target needs both screens'
assert before_outputs['HDMI-A-1']['logical']['x'] >= before_outputs['eDP-1']['logical']['width']
run('niri', 'validate', '--config', '/etc/niri/qubix/config.kdl')
process = None
window_id = None
panel_opened = False
try:
    action('load-config-file')
    action('focus-monitor', 'eDP-1')
    process = subprocess.Popen(['wezterm', '--skip-config', 'start', '--always-new-process',
        '--class=qubix-screen-shortcuts-test', '--', '/bin/sleep', '90'], env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        owned = [w for w in query('windows') if w.get('app_id') == 'qubix-screen-shortcuts-test']
        if owned:
            assert len(owned) == 1
            window_id = owned[0]['id']
            break
        time.sleep(0.1)
    assert window_id is not None, 'Test terminal did not appear'
    action('focus-window', '--id', str(window_id))
    for right, left in [('Right', 'Left'), ('L', 'H')]:
        action('move-column-to-last')
        binding('Mod+' + right, 'focus-column-or-monitor-right')
        assert query('focused-output')['name'] == 'HDMI-A-1'
        action('focus-window', '--id', str(window_id))
        binding('Mod+Alt+' + right, 'move-window-to-monitor-right')
        window = next(w for w in query('windows') if w['id'] == window_id)
        assert next(w for w in query('workspaces') if w['id'] == window['workspace_id'])['output'] == 'HDMI-A-1'
        action('focus-window', '--id', str(window_id))
        action('move-column-to-first')
        binding('Mod+' + left, 'focus-column-or-monitor-left')
        assert query('focused-output')['name'] == 'eDP-1'
        action('focus-window', '--id', str(window_id))
        binding('Mod+Alt+' + left, 'move-window-to-monitor-left')
        window = next(w for w in query('windows') if w['id'] == window_id)
        assert next(w for w in query('workspaces') if w['id'] == window['workspace_id'])['output'] == 'eDP-1'
        action('focus-window', '--id', str(window_id))
    for key, direction in [('Up', 'up'), ('Down', 'down'), ('K', 'up'), ('J', 'down')]:
        binding('Mod+' + key, 'focus-window-or-monitor-' + direction)
        assert query('focused-output')['name'] == 'eDP-1'
        binding('Mod+Alt+' + key, 'move-window-to-monitor-' + direction)
    for key, movement in [('Left', 'move-column-left'), ('H', 'move-column-left'),
                          ('Right', 'move-column-right'), ('L', 'move-column-right'),
                          ('Up', 'move-window-up'), ('K', 'move-window-up'),
                          ('Down', 'move-window-down'), ('J', 'move-window-down')]:
        binding('Mod+Shift+' + key, movement)
    widths = []
    for key, delta in [('Left', '-5%'), ('H', '-5%'), ('Right', '+5%'), ('L', '+5%')]:
        action('set-column-width', '50%')
        before = query('focused-window')['layout']['tile_size'][0]
        binding('Mod+Ctrl+' + key, 'set-column-width', delta)
        after = query('focused-window')['layout']['tile_size'][0]
        assert after < before if delta.startswith('-') else after > before
        widths.append([key, before, after])
    for key, delta in [('Up', '-5%'), ('K', '-5%'), ('Down', '+5%'), ('J', '+5%')]:
        binding('Mod+Ctrl+' + key, 'set-window-height', delta)
        action('reset-window-height')

    shell = '/usr/share/qubix/bin/qubix-noctalia'
    panel_result = 'already open; preserved operator panel'
    if not json.loads(run(shell, 'msg', 'status'))['panelOpen']:
        run(shell, 'msg', 'panel-open', 'qubix/shortcuts:cheatsheet', 'resize')
        panel_opened = True
        for _ in range(50):
            if json.loads(run(shell, 'msg', 'status')).get('activePanelId') == 'qubix/shortcuts:cheatsheet':
                break
            time.sleep(0.1)
        else:
            raise AssertionError('Installed shortcut panel did not open')
        run(shell, 'msg', 'plugin', 'qubix/shortcuts:cheatsheet', 'all', 'search', 'Super')
        panel_result = 'open/filter/close'

finally:
    if panel_opened:
        run('/usr/share/qubix/bin/qubix-noctalia', 'msg', 'panel-close', 'qubix/shortcuts:cheatsheet')
    if window_id is not None:
        action('close-window', '--id', str(window_id))
    if process is not None:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=5)
    if before_focus and before_focus['id'] in {w['id'] for w in query('windows')}:
        action('focus-window', '--id', str(before_focus['id']))
    else:
        action('focus-monitor', before_output)
if panel_opened:
    assert not json.loads(run('/usr/share/qubix/bin/qubix-noctalia', 'msg', 'status'))['panelOpen']
assert query('focused-output')['name'] == before_output
if before_focus:
    assert query('focused-window')['id'] == before_focus['id']
assert hashes() == before_hashes
assert query('outputs') == before_outputs
assert {w['id']: w['workspace_id'] for w in query('windows')} == before_windows
assert Path(f'/proc/{pid}/comm').read_text().strip() == 'niri'
assert Path('/proc/sys/kernel/random/boot_id').read_text() == boot
print(json.dumps({'status': 'passed', 'bindings': 32, 'resize_widths': widths, 'focus': 'internal/external roundtrip',
    'window': 'internal/external roundtrip', 'up_down': 'no-neighbor no-op',
    'personal_configs_outputs_original_windows_compositor_boot': 'preserved', 'test_window': 'removed', 'installed_panel': panel_result}))
