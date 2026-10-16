"""Run the actual power panel in a no-effect Luau host on the controller."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
interpreter = os.environ.get('LUAU_BIN') or shutil.which('luau') or str(ROOT / '.cache/luau/luau')
source = (ROOT / 'roles/qubix_niri/files/power/panel.luau').read_text()
fixture = (ROOT / 'tests/luau/power.luau').read_text()
assert fixture.count('-- INCLUDE_PRODUCTION_PANEL') == 1
cache = ROOT / '.cache/tests'
cache.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='power-', dir=cache) as directory:
    script = Path(directory) / 'power.luau'
    script.write_text(fixture.replace('-- INCLUDE_PRODUCTION_PANEL', source))
    subprocess.run([interpreter, str(script)], check=True)
