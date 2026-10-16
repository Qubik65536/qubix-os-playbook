#!/usr/bin/python3
# Disposable native-test recorder: never invokes a session action.
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
assert root.parent == Path('/tmp') and root.name.startswith('qubix-native-smoke.')
assert sys.argv[1:] == ['msg', 'session', 'reboot'], 'Only the isolated regression action is accepted'
reply = subprocess.run([str(root / 'qubix-noctalia'), 'msg', 'status'],
                       capture_output=True, text=True, check=True, timeout=8)
status = json.loads(reply.stdout)
assert not status['panelOpen'] and status['activePanelId'] is None, 'Power dispatch preceded panel destruction'
(root / 'power-dispatch.json').write_text(json.dumps({'action': 'reboot', 'status': status}))
