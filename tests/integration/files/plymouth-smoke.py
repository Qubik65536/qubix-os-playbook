# Test-only native Plymouth module/rendering; never contacts the host splash daemon.
import configparser
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


def inside(root):
    renderer = os.environ['QUBIX_PREVIEW_FONT_RENDERER']
    prefix = '' if renderer == 'pango' else 'freetype-'
    artifact = lambda name: root / (prefix + name)
    assert os.getuid() == 0 and not pathlib.Path('/dev/dri').exists()
    assert pathlib.Path('/etc/plymouth/plymouthd.conf').read_text().strip() == '[Daemon]\nTheme=qubix\nShowDelay=0'
    definition = root / 'theme/qubix.plymouth'
    candidate = definition.read_text()
    config = configparser.ConfigParser()
    config.read_string(candidate)
    assert config['Plymouth Theme']['ModuleName'] == 'two-step'
    font_path = pathlib.Path('/usr/share/fonts/qubix/QubixBootMono-Regular.ttf')
    selected = run(['/usr/lib/plymouth/plymouth-font-file', 'Qubix Boot Mono 12']).stdout.strip()
    assert selected == str(font_path), 'Native font resolver silently chose a different family: ' + selected
    assert font_path.read_bytes() == pathlib.Path('/usr/share/fonts/Plymouth.ttf').read_bytes()
    result = {'native_module': True, 'negative_module': False, 'modes': {},
              'font_family': 'Qubix Boot Mono', 'font_sha256': hashlib.sha256(font_path.read_bytes()).hexdigest(),
              'font_renderer': renderer}
    if renderer == 'freetype':
        assert pathlib.Path('/usr/lib/plymouth/label-pango.so').read_bytes() == pathlib.Path('/usr/lib/plymouth/label-freetype.so').read_bytes()
    xlog = artifact('xwayland.log').open('w')
    xserver = subprocess.Popen(['/usr/bin/Xwayland', ':98', '-geometry', '800x600', '-nolisten', 'tcp', '-ac', '-nocursor'], stdout=xlog, stderr=xlog)
    try:
        for attempt in range(50):
            if pathlib.Path('/tmp/.X11-unix/X98').exists():
                break
            assert xserver.poll() is None, 'Private Xwayland exited'
            time.sleep(0.1)
        else:
            raise AssertionError('Private Xwayland was not ready')
        for mode in (('invalid', 'boot', 'shutdown', 'reboot') if renderer == 'pango' else ('boot',)):
            definition.write_text(candidate.replace('ModuleName=two-step', 'ModuleName=qubix-invalid-control') if mode == 'invalid' else candidate)
            log = artifact(mode + '.log').open('w')
            master, slave = pty.openpty()
            terminal = os.ttyname(slave)
            assert terminal.startswith('/dev/pts/'), terminal
            def drain_terminal():
                # Native early tracing uses this private tty before --debug-file is active.
                with artifact(mode + '-tty.log').open('wb') as transcript:
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
                '--tty=' + terminal, '--mode=' + ('boot' if mode == 'invalid' else mode), '--pid-file=' + str(artifact(mode + '.pid')),
                '--debug', '--debug-file=' + str(artifact(mode + '-debug.log')),
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
                mapped = '/usr/lib/plymouth/two-step.so' in pathlib.Path('/proc', str(daemon.pid), 'maps').read_text()
                if mode == 'invalid':
                    assert not mapped, 'Invalid module unexpectedly loaded the native spinner'
                    result['negative_module'] = True
                    continue
                assert mapped, 'Native two-step plugin is not mapped'
                if renderer == 'freetype':
                    maps = pathlib.Path('/proc', str(daemon.pid), 'maps').read_text()
                    assert any('/usr/lib/plymouth/label-' + name + '.so' in maps for name in ('pango', 'freetype'))
                first = artifact(mode + '.png')
                second = artifact(mode + '-motion.png')
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
                    run(['/usr/bin/magick', 'import', '-window', 'root', str(artifact('password-prompt.png'))])
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
            text = artifact(mode + '-debug.log').read_text()
            assert "Loading boot splash theme '/usr/share/plymouth/themes//qubix/qubix.plymouth'" in text, 'Production theme was not loaded'
            assert not any(error in text.lower() for error in ('script error', 'parse error', 'parser error')), text[-1500:]
            assert 'Could not load font' not in text, 'Native renderer could not load the packaged subset'
            if renderer == 'freetype':
                assert 'controls/label-pango/plugin.c' not in text, 'Forced preview still used Pango code'
        result['status'] = 'passed'
        artifact('result.json').write_text(json.dumps(result, indent=2))
    finally:
        definition.write_text(candidate)
        xserver.terminate()
        xserver.wait(timeout=3)


def outside(root, renderer='pango'):
    prefix = '' if renderer == 'pango' else 'freetype-'
    artifact = lambda name: root / (prefix + name)
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
    (root / 'home').mkdir(exist_ok=True)
    (root / 'fonts.conf').write_text('''<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig><dir>/usr/share/fonts/qubix</dir><dir>/usr/share/fonts/native</dir>
<cachedir>/tmp/qubix-preview/font-cache</cachedir></fontconfig>''')
    token = str(root)
    env = dict(os.environ, QUBIX_PLYMOUTH_PREVIEW_TOKEN=token)
    command = [
        '/usr/bin/bwrap', '--unshare-all', '--uid', '0', '--gid', '0', '--die-with-parent', '--new-session',
        '--ro-bind', '/', '/', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--tmpfs', '/run',
        '--bind', str(root), '/tmp/qubix-preview',
        '--dir', '/run/user/0', '--ro-bind', str(display), '/run/user/0/wayland-preview',
        '--tmpfs', '/usr/share/plymouth/themes', '--ro-bind', str(root / 'theme'), '/usr/share/plymouth/themes/qubix',
        '--tmpfs', '/usr/share/fonts', '--dir', '/usr/share/fonts/qubix',
        '--ro-bind', '/usr/share/fonts', '/usr/share/fonts/native',
        '--ro-bind', str(root / 'fonts'), '/usr/share/fonts/qubix',
        '--ro-bind', str(root / 'fonts/QubixBootMono-Regular.ttf'), '/usr/share/fonts/Plymouth.ttf',
        '--ro-bind', str(root / 'plymouthd.conf'), '/etc/plymouth/plymouthd.conf',
        '--setenv', 'XDG_RUNTIME_DIR', '/run/user/0', '--setenv', 'WAYLAND_DISPLAY', 'wayland-preview',
        '--setenv', 'DISPLAY', ':98', '--setenv', 'HOME', '/tmp/qubix-preview/home',
        '--setenv', 'XWAYLAND_NO_GLAMOR', '1',
        '--setenv', 'FONTCONFIG_FILE', '/tmp/qubix-preview/fonts.conf',
        '--setenv', 'QUBIX_PREVIEW_FONT_RENDERER', renderer,
    ]
    if renderer == 'freetype':
        # Both implement the native label ABI; substitute only within this mount namespace.
        command += ['--ro-bind', '/usr/lib/plymouth/label-freetype.so', '/usr/lib/plymouth/label-pango.so']
    command += ['/usr/bin/python3', '/tmp/qubix-preview/smoke.py', '--inside', '/tmp/qubix-preview']
    log = artifact('preview.log').open('w')
    process = subprocess.Popen(command, env=env, stdout=log, stderr=log, start_new_session=True)
    try:
        process.wait(timeout=65)
        assert process.returncode == 0, artifact('preview.log').read_text()[-2500:]
        result = json.loads(artifact('result.json').read_text())
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
    artifact('result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if sys.argv[1] == '--inside':
    inside(pathlib.Path(sys.argv[2]))
else:
    outside(pathlib.Path(sys.argv[1]))
    outside(pathlib.Path(sys.argv[1]), 'freetype')
