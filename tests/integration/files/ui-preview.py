"""Native test helper: fake identity, no greetd/system bus, temporary nested compositor."""
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time


def run(args, **kwargs):
    return subprocess.check_output(args, text=True, timeout=10, **kwargs)


def wait_for(predicate, label):
    for _ in range(1200):
        value = predicate()
        if value:
            return value
        time.sleep(0.1)
    raise AssertionError(label)


root = Path(sys.argv[1])
assert root.parent == Path('/tmp') and root.name.startswith('qubix-ui-preview.')
assert root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.getuid()

if len(sys.argv) > 2:
    assert os.environ['NIRI_SOCKET'] != (root / 'parent-socket').read_text()
    wait_for(lambda: (root / 'sized').exists(), 'Nested output was not resized')
    env = dict(os.environ, USER='preview', LOGNAME='preview', GDK_BACKEND='wayland',
               GSETTINGS_BACKEND='memory', GIO_USE_VFS='local')
    env['GREETD_SOCK'] = str(root / 'no-greetd-socket')
    env['DBUS_SYSTEM_BUS_ADDRESS'] = 'unix:path=' + str(root / 'no-system-bus')
    env['NOCTALIA_GREETER_LOG'] = 'stderr'
    env['NOCTALIA_GREETER_ASSETS_DIR'] = '/usr/share/noctalia-greeter/assets'
    env['NOCTALIA_ASSETS_DIR'] = '/usr/share/noctalia/assets'
    env['NOCTALIA_CONFIG_HOME'] = str(root / 'config')
    env['NOCTALIA_STATE_HOME'] = str(root / 'state')
    env['NOCTALIA_DATA_HOME'] = str(root / 'data')
    state_settings = root / 'state/noctalia/settings.toml'
    state_settings.parent.mkdir(parents=True, exist_ok=True)
    state_settings.write_text('[shell]\npolkit_agent = false\nclipboard_enabled = false\noffline_mode = true\n'
                              '[lockscreen]\nenabled = false\n')
    (root / 'passwd').write_text('root:x:0:0:root:/root:/usr/bin/bash\n'
        f'preview:x:{os.getuid()}:{os.getgid()}:Qubix Preview:{root}/home:/usr/bin/bash\n')
    (root / 'group').write_text(f'preview:x:{os.getgid()}:\n')
    binaries = json.loads((root / 'binaries.json').read_text())
    sandbox = ['/usr/bin/bwrap', '--die-with-parent', '--unshare-pid', '--unshare-net', '--unshare-ipc',
        '--unshare-uts', '--hostname', 'qubix-preview', '--ro-bind', '/', '/', '--dev-bind', '/dev', '/dev',
        '--proc', '/proc', '--bind', str(root), str(root),
        '--ro-bind', str(root / 'passwd'), '/etc/passwd', '--ro-bind', str(root / 'group'), '/etc/group']
    shots = {}
    def screenshot(name, shell=False):
        if shell:
            run(['/usr/bin/noctalia', 'msg', 'notification-clear-active'], env=env)
        time.sleep(1.5)
        target = root / (name + '.png')
        run(['/usr/bin/niri', 'msg', 'action', 'screenshot-screen', '--path', str(target), '--show-pointer', 'false'])
        wait_for(target.is_file, 'Missing screenshot ' + name)
        shots[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    def stop(process):
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    selection = json.loads((root / 'selection.json').read_text())
    assert selection and set(selection) <= {'fingerprint', 'greeter', 'shell'}
    for kind in selection:
        for variant in ('reference', 'qubix'):
            name = kind + '-' + variant
            case_env = dict(env)
            if kind == 'fingerprint':
                args = ['/usr/bin/gjs', '-m', str(root / 'fingerprint/main.js'),
                        '--reference-preview' if variant == 'reference' else '--preview']
            elif kind == 'greeter':
                state = root / name
                state.mkdir(mode=0o700)
                config = root / ('before.toml' if variant == 'reference' else 'candidate.toml')
                (state / 'greeter.toml').write_bytes(config.read_bytes())
                case_env['NOCTALIA_GREETER_STATE_DIR'] = str(state)
                args = ['/usr/bin/noctalia-greeter' if variant == 'reference' else binaries['greeter'],
                        '--user', 'preview']
            else:
                args = ['/usr/bin/noctalia' if variant == 'reference' else binaries['noctalia']]
            with (root / (name + '.log')).open('w') as log:
                process = subprocess.Popen(sandbox + args, env=case_env, stdout=log, stderr=log)
                try:
                    if kind == 'shell':
                        def ready():
                            if process.poll() is not None:
                                raise AssertionError((root / (name + '.log')).read_text())
                            try:
                                return run(['/usr/bin/noctalia', 'msg', 'color-scheme-get'], env=case_env).strip() == 'custom Qubix'
                            except subprocess.CalledProcessError:
                                return False
                        wait_for(ready, 'Noctalia private IPC did not become ready')
                        for panel in ('launcher', 'control-center'):
                            result = run(['/usr/bin/noctalia', 'msg', 'panel-toggle', panel], env=case_env)
                            assert not result.lower().startswith('error'), result
                            screenshot(panel + '-' + variant, shell=True)
                            run(['/usr/bin/noctalia', 'msg', 'panel-toggle', panel], env=case_env)
                    else:
                        wait_for(lambda: process.poll() is not None or
                            json.loads(run(['/usr/bin/niri', 'msg', '--json', 'windows'])), 'Missing ' + name + ' window')
                        assert process.poll() is None, (root / (name + '.log')).read_text()
                        if kind == 'greeter':
                            run(['/usr/bin/niri', 'msg', 'action', 'fullscreen-window'])
                        screenshot(name)
                    assert process.poll() is None, (root / (name + '.log')).read_text()
                    text = (root / (name + '.log')).read_text()
                    assert not re.search(r'JS ERROR|unknown .*key|invalid TOML|incomplete.*palette', text, re.I), text
                finally:
                    stop(process)
                    wait_for(lambda: not json.loads(run(['/usr/bin/niri', 'msg', '--json', 'windows'])), 'Previous window remained')
    comparisons = [kind for kind in selection if kind != 'shell']
    if 'shell' in selection:
        comparisons += ['launcher', 'control-center']
    for kind in comparisons:
        assert shots[kind + '-reference'] != shots[kind + '-qubix'], 'Identical comparison: ' + kind
    (root / 'inner-result.json').write_text(json.dumps({'rendered': True, 'screenshots': shots,
        'biometric_operations': 0, 'fingerprint_preview': 'simulated, no system bus'}))
    sys.exit(0)

session = dict(line.split('=', 1) for line in run(
    ['/usr/bin/systemctl', '--user', 'show-environment']).splitlines() if '=' in line)
parent = {key: session[key] for key in ('NIRI_SOCKET', 'WAYLAND_DISPLAY', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS')}
match = re.search(r'\.(\d+)\.sock$', parent['NIRI_SOCKET'])
assert match and Path(parent['NIRI_SOCKET']).is_socket()
main_pid = int(match[1])
assert (Path('/proc') / str(main_pid) / 'comm').read_text().strip() == 'niri'
(root / 'parent-socket').write_text(parent['NIRI_SOCKET'])
protected = [Path.home() / relative for relative in (
    '.config/niri/config.kdl', '.config/noctalia/config.toml', '.config/dconf/user',
    '.local/state/qubix/noctalia/settings.toml')]


def hashes():
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in protected}


before = hashes()
env = dict(os.environ, **parent)
env.pop('NIRI_SOCKET', None)
env['WAYLAND_DISPLAY'] = str(Path(parent['XDG_RUNTIME_DIR']) / parent['WAYLAND_DISPLAY'])
env['XDG_RUNTIME_DIR'] = str(root / 'runtime')
(root / 'runtime').mkdir(mode=0o700)
env['DBUS_SYSTEM_BUS_ADDRESS'] = 'unix:path=' + str(root / 'no-system-bus')
for key, relative in [('HOME', 'home'), ('XDG_CONFIG_HOME', 'config'), ('XDG_STATE_HOME', 'state'),
                      ('XDG_CACHE_HOME', 'cache'), ('XDG_DATA_HOME', 'data')]:
    env[key] = str(root / relative)
    (root / relative).mkdir(mode=0o700, exist_ok=True)
(root / 'config.kdl').write_text(
    'input {\n    keyboard { xkb { layout "us"; }; };\n}\n'
    'hotkey-overlay { skip-at-startup; }\n')
(root / 'bus.conf').write_text(
    '<busconfig><type>session</type><listen>unix:tmpdir=/tmp</listen>'
    '<policy context="default"><allow send_destination="*"/>'
    '<allow receive_sender="*"/><allow own="*"/></policy></busconfig>')
result = {}
with (root / 'nested.log').open('w') as log:
    process = subprocess.Popen([
        '/usr/bin/dbus-run-session', '--config-file', str(root / 'bus.conf'), '--',
        '/usr/bin/niri', '--config', str(root / 'config.kdl'),
        '--', '/usr/bin/python3', str(root / 'preview.py'), str(root), 'inner'],
        env=env, stdout=log, stderr=log, start_new_session=True)
    try:
        def owned_window():
            windows = json.loads(run(['/usr/bin/niri', 'msg', '--json', 'windows'], env=dict(env, **parent)))
            return next((w for w in windows if w.get('pid') and os.getpgid(w['pid']) == process.pid), None)
        window = wait_for(owned_window, 'Private nested Niri window did not appear')
        for action in [('move-window-to-floating',), ('set-window-width', '1280'), ('set-window-height', '900')]:
            run(['/usr/bin/niri', 'msg', 'action', action[0], '--id', str(window['id']), *action[1:]],
                env=dict(env, **parent))
        (root / 'sized').touch()
        wait_for(lambda: (root / 'inner-result.json').is_file() or process.poll() is not None,
                 'Native preview did not finish')
        assert (root / 'inner-result.json').is_file(), (root / 'nested.log').read_text()
        result = json.loads((root / 'inner-result.json').read_text())
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        remaining = []
        for entry in Path('/proc').iterdir():
            if entry.name.isdecimal():
                try:
                    variables = (entry / 'environ').read_bytes().split(b'\0')
                    if os.getpgid(int(entry.name)) == process.pid or (
                        ('HOME=' + env['HOME']).encode() in variables):
                        remaining.append(int(entry.name))
                except (ProcessLookupError, FileNotFoundError, PermissionError):
                    pass
        for pid in remaining:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        def active_group():
            active = []
            for pid in remaining:
                try:
                    if (Path('/proc') / str(pid) / 'stat').read_text().split()[2] != 'Z':
                        active.append(pid)
                except FileNotFoundError:
                    pass
            return active
        wait_for(lambda: not active_group(), 'Preview processes remain after cleanup')
        assert hashes() == before, 'Personal desktop settings changed'
        assert (Path('/proc') / str(main_pid) / 'comm').read_text().strip() == 'niri'
        result.update(cleanup_remaining=0, personal_settings_preserved=True, primary_niri_preserved=True,
                      authentication_tested=False, boot_tested=False)
(root / 'result.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result))
