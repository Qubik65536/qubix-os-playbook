# Native presenter-only preview; the shared outer helper owns process cleanup.
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

root = Path(sys.argv[1])
result = {'socket': os.environ['NIRI_SOCKET'], 'display': os.environ['WAYLAND_DISPLAY'],
          'bus': os.environ['DBUS_SESSION_BUS_ADDRESS']}
assert result['socket'] != json.loads((root / 'parent.json').read_text())['socket']

def shell(*args):
    output = subprocess.check_output([str(root / 'qubix-noctalia'), 'msg', *args], text=True, timeout=8).strip()
    assert not output.lower().startswith('error:'), output
    return output

def wait_for(predicate, label):
    for _ in range(50):
        if predicate():
            return
        time.sleep(0.1)
    raise AssertionError(label)

def capture(name):
    shell('notification-clear-active')
    time.sleep(0.4)
    subprocess.run(['niri', 'msg', 'action', 'screenshot-screen', '--path', str(root / name),
                    '--show-pointer', 'false'], check=True, capture_output=True, timeout=8)

try:
    for _ in range(60):
        try:
            shell('status')
            break
        except (subprocess.CalledProcessError, AssertionError):
            time.sleep(0.2)
    else:
        raise AssertionError('Private Noctalia did not start')
    shell('panel-open', 'qubix/shortcuts:cheatsheet')
    wait_for(lambda: json.loads(shell('status')).get('activePanelId') == 'qubix/shortcuts:cheatsheet',
             'Shortcut panel did not open')
    capture('shortcuts.png')
    for term in ['resize', 'brightness']:
        shell('plugin', 'qubix/shortcuts:cheatsheet', 'all', 'search', term)
        capture('shortcuts-' + term + '.png')
    shell('panel-close', 'qubix/shortcuts:cheatsheet')
    data_path = root / 'plugins/shortcuts/bindings.json'
    data = json.loads(data_path.read_text())
    data += [['Print', 'Windows / Keycap sizing sample'],
             ['Mod+Ctrl+Alt+Shift+Page_Down', 'Windows / Keycap sizing sample'],
             ['XF86MonBrightnessDown', 'Windows / Keycap sizing sample']]
    data_path.write_text(json.dumps(data))
    shell('panel-open', 'qubix/shortcuts:cheatsheet', 'Keycap sizing sample')
    shell('plugin', 'qubix/shortcuts:cheatsheet', 'all', 'search', 'Keycap sizing sample')
    capture('shortcuts-stress.png')
    shell('panel-close', 'qubix/shortcuts:cheatsheet')
    wait_for(lambda: not json.loads(shell('status'))['panelOpen'], 'Shortcut panel did not close')
    result.update(status='passed', screenshots=4, filtering=True, close_reopen=True,
                  stress='short, long chord and media aliases; private data only')
except Exception as error:
    result.update(status='failed', error=traceback.format_exc())
finally:
    (root / 'result.json').write_text(json.dumps(result))
