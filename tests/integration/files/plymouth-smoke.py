# Test-only native Plymouth parser/rendering; never contacts the host splash daemon.
import ctypes
import hashlib
import json
import os
import pathlib
import pty
import signal
import subprocess
import sys
import threading
import time


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, timeout=10, check=True, **kwargs)


def parse(path):
    library = ctypes.CDLL('/usr/lib/plymouth/script.so', mode=os.RTLD_LAZY | os.RTLD_LOCAL)
    library.script_parse_file.argtypes = [ctypes.c_char_p]
    library.script_parse_file.restype = ctypes.c_void_p
    library.script_parse_op_free.argtypes = [ctypes.c_void_p]
    library.script_parse_op_free.restype = None
    tree = library.script_parse_file(os.fsencode(path))
    assert tree, 'Native parser returned no syntax tree'
    library.script_parse_op_free(tree)


def inside(root):
    assert os.getuid() == 0 and not pathlib.Path('/dev/dri').exists()
    assert pathlib.Path('/etc/plymouth/plymouthd.conf').read_text().strip() == '[Daemon]\nTheme=qubix\nShowDelay=0'
    valid = run([sys.executable, __file__, '--parse', str(root / 'theme/qubix.script')])
    assert not valid.stderr.strip(), 'Native parser rejected the production theme: ' + valid.stderr
    (root / 'invalid.script').write_text('if (')
    invalid = run([sys.executable, __file__, '--parse', str(root / 'invalid.script')])
    assert 'Parser error' in invalid.stderr, 'Native parser missed the invalid control'
    result = {'native_parser': True, 'negative_parser': True, 'modes': {}}
    xlog = (root / 'xwayland.log').open('w')
    xserver = subprocess.Popen(['/usr/bin/Xwayland', ':98', '-geometry', '800x600', '-nolisten', 'tcp', '-ac', '-nocursor'], stdout=xlog, stderr=xlog)
    try:
        for attempt in range(50):
            if pathlib.Path('/tmp/.X11-unix/X98').exists():
                break
            assert xserver.poll() is None, 'Private Xwayland exited'
            time.sleep(0.1)
        else:
            raise AssertionError('Private Xwayland was not ready')
        for mode in ('boot', 'shutdown', 'reboot'):
            log = (root / (mode + '.log')).open('w')
            master, slave = pty.openpty()
            terminal = os.ttyname(slave)
            assert terminal.startswith('/dev/pts/'), terminal
            def drain_terminal():
                # Native early tracing uses this private tty before --debug-file is active.
                with (root / (mode + '-tty.log')).open('wb') as transcript:
                    while True:
                        try:
                            data = os.read(master, 4096)
                        except OSError:
                            break
                        if not data:
                            break
                        transcript.write(data)
            reader = threading.Thread(target=drain_terminal, daemon=True)
            reader.start()
            daemon = subprocess.Popen([
                '/usr/bin/plymouthd', '--no-daemon', '--no-boot-log', '--graphical-boot',
                '--tty=' + terminal, '--mode=' + mode, '--pid-file=' + str(root / (mode + '.pid')),
                '--debug', '--debug-file=' + str(root / (mode + '-debug.log')),
                '--kernel-command-line=quiet splash plymouth.ignore-serial-consoles',
            ], stdout=log, stderr=log)
            prompt = None
            try:
                for attempt in range(50):
                    ping = subprocess.run(['/usr/bin/plymouth', '--ping'], capture_output=True, timeout=2)
                    if ping.returncode == 0:
                        break
                    assert daemon.poll() is None, 'Isolated Plymouth exited before ping'
                    time.sleep(0.1)
                else:
                    raise AssertionError('Isolated Plymouth was not ready')
                run(['/usr/bin/plymouth', 'show-splash'])
                time.sleep(0.8)
                assert '/usr/lib/plymouth/script.so' in pathlib.Path('/proc', str(daemon.pid), 'maps').read_text(), 'Native script plugin is not mapped'
                first = root / (mode + '.png')
                second = root / (mode + '-motion.png')
                run(['/usr/bin/magick', 'import', '-window', 'root', str(first)])
                time.sleep(0.23)
                run(['/usr/bin/magick', 'import', '-window', 'root', str(second)])
                compared = subprocess.run(['/usr/bin/magick', 'compare', '-metric', 'AE', str(first), str(second), 'null:'], capture_output=True, text=True, timeout=10)
                difference = float(compared.stderr.split()[0])
                assert compared.returncode == 1 and difference > 0, 'Loading circle did not animate'
                result['modes'][mode] = {'animation_pixels_changed': difference}
                if mode == 'boot':
                    prompt = subprocess.Popen(['/usr/bin/plymouth', 'ask-for-password', '--prompt=Qubix preview password'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(0.4)
                    run(['/usr/bin/magick', 'import', '-window', 'root', str(root / 'password-prompt.png')])
                    result['password_prompt_requested'] = True
            finally:
                if prompt is not None and prompt.poll() is None:
                    prompt.terminate()
                    prompt.wait(timeout=3)
                try:
                    subprocess.run(['/usr/bin/plymouth', 'quit'], capture_output=True, timeout=15)
                except subprocess.TimeoutExpired:
                    pass
                try:
                    daemon.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    daemon.kill()
                    daemon.wait(timeout=3)
                os.close(slave)
                reader.join(timeout=2)
                os.close(master)
            assert daemon.returncode == 0, 'Private splash daemon did not exit cleanly'
            text = (root / (mode + '-debug.log')).read_text()
            assert "Loading boot splash theme '/usr/share/plymouth/themes//qubix/qubix.plymouth'" in text and 'parsing script file' in text, 'Production theme was not loaded'
            assert not any(error in text.lower() for error in ('script error', 'parse error', 'parser error')), text[-1500:]
        result['status'] = 'passed'
        (root / 'result.json').write_text(json.dumps(result, indent=2))
    finally:
        xserver.terminate()
        xserver.wait(timeout=3)


def outside(root):
    assert root.parent == pathlib.Path('/tmp') and root.name.startswith('qubix-plymouth-preview.')
    assert root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.getuid()
    session = dict(line.split('=', 1) for line in run(['systemctl', '--user', 'show-environment']).stdout.splitlines() if '=' in line)
    display = pathlib.Path(session['XDG_RUNTIME_DIR']) / session['WAYLAND_DISPLAY']
    assert display.is_socket()
    preserved = [pathlib.Path('/etc/plymouth/plymouthd.conf'), pathlib.Path.home() / '.config/niri/config.kdl', pathlib.Path.home() / '.config/dconf/user']
    def hashes():
        return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None for p in preserved}
    before = hashes()
    host_daemons = subprocess.run(['pgrep', '-x', 'plymouthd'], capture_output=True, text=True).stdout
    before_socket = pathlib.Path(session['NIRI_SOCKET'])
    assert before_socket.is_socket()
    (root / 'home').mkdir()
    token = str(root)
    env = dict(os.environ, QUBIX_PLYMOUTH_PREVIEW_TOKEN=token)
    command = [
        '/usr/bin/bwrap', '--unshare-all', '--uid', '0', '--gid', '0', '--die-with-parent', '--new-session',
        '--ro-bind', '/', '/', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--tmpfs', '/run',
        '--bind', str(root), '/tmp/qubix-preview',
        '--dir', '/run/user/0', '--ro-bind', str(display), '/run/user/0/wayland-preview',
        '--tmpfs', '/usr/share/plymouth/themes', '--ro-bind', str(root / 'theme'), '/usr/share/plymouth/themes/qubix',
        '--ro-bind', str(root / 'plymouthd.conf'), '/etc/plymouth/plymouthd.conf',
        '--setenv', 'XDG_RUNTIME_DIR', '/run/user/0', '--setenv', 'WAYLAND_DISPLAY', 'wayland-preview',
        '--setenv', 'DISPLAY', ':98', '--setenv', 'HOME', '/tmp/qubix-preview/home',
        '--setenv', 'XWAYLAND_NO_GLAMOR', '1',
        '/usr/bin/python3', '/tmp/qubix-preview/smoke.py', '--inside', '/tmp/qubix-preview',
    ]
    log = (root / 'preview.log').open('w')
    process = subprocess.Popen(command, env=env, stdout=log, stderr=log, start_new_session=True)
    try:
        process.wait(timeout=65)
        assert process.returncode == 0, (root / 'preview.log').read_text()[-2500:]
        result = json.loads((root / 'result.json').read_text())
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        remaining = []
        marker = ('QUBIX_PLYMOUTH_PREVIEW_TOKEN=' + token).encode()
        for p in pathlib.Path('/proc').iterdir():
            if not p.name.isdigit():
                continue
            try:
                if p.stat().st_uid == os.getuid() and marker in (p / 'environ').read_bytes().split(b'\0'):
                    remaining.append(int(p.name))
            except (PermissionError, FileNotFoundError, ProcessLookupError):
                pass
        for pid in remaining:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        assert not remaining, 'Isolated preview processes remained: ' + str(remaining)
    assert before == hashes() and before_socket.is_socket(), 'Host configuration/session changed'
    assert host_daemons == subprocess.run(['pgrep', '-x', 'plymouthd'], capture_output=True, text=True).stdout
    result.update({'host_configuration_preserved': True, 'host_plymouth_preserved': True, 'cleanup_remaining': 0})
    (root / 'result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if sys.argv[1] == '--parse':
    parse(pathlib.Path(sys.argv[2]))
elif sys.argv[1] == '--inside':
    inside(pathlib.Path(sys.argv[2]))
else:
    outside(pathlib.Path(sys.argv[1]))
