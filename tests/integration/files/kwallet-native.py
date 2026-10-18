# Native test helper; credentials arrive on stdin and are never printed or persisted.
import ctypes as C
import os
import pathlib
import pwd
import subprocess
import sys
import tempfile
import time

assert os.geteuid() == 0, 'Run through sudo with the ordinary desktop user'
assert '--isolated' in sys.argv or '--live' in sys.argv, 'Choose isolated test or explicitly authorized live initialization'
user = pwd.getpwnam(os.environ['SUDO_USER'])
assert user.pw_uid != 0
password = sys.stdin.buffer.readline().rstrip(b'\n')
assert password
service = pathlib.Path('/etc/pam.d/qubix-kwallet-test')
assert not service.exists()
service.write_text('auth required pam_unix.so\nauth optional pam_kwallet5.so\naccount required pam_unix.so\nsession optional pam_kwallet5.so auto_start force_run kwalletd=/usr/bin/ksecretd\n')
service.chmod(0o644)
class Message(C.Structure):
    _fields_ = [('style', C.c_int), ('message', C.c_char_p)]
class Response(C.Structure):
    _fields_ = [('response', C.c_void_p), ('code', C.c_int)]
Callback = C.CFUNCTYPE(C.c_int, C.c_int, C.POINTER(C.POINTER(Message)), C.POINTER(C.POINTER(Response)), C.c_void_p)
libc = C.CDLL('libc.so.6')
libc.calloc.argtypes = [C.c_size_t, C.c_size_t]
libc.calloc.restype = C.c_void_p
libc.strdup.argtypes = [C.c_char_p]
libc.strdup.restype = C.c_void_p
@Callback
def converse(count, messages, responses, data):
    result = C.cast(libc.calloc(count, C.sizeof(Response)), C.POINTER(Response))
    for i in range(count):
        if messages[i].contents.style == 1:
            result[i].response = libc.strdup(password)
        elif messages[i].contents.style == 2:
            result[i].response = libc.strdup(user.pw_name.encode())
    responses[0] = result
    return 0
class Conversation(C.Structure):
    _fields_ = [('callback', Callback), ('data', C.c_void_p)]
pam = C.CDLL('libpam.so.0')
pam.pam_getenv.argtypes = [C.c_void_p, C.c_char_p]
pam.pam_getenv.restype = C.c_char_p
handle = C.c_void_p()
conversation = Conversation(converse, None)
try:
    assert pam.pam_start(b'qubix-kwallet-test', user.pw_name.encode(), C.byref(conversation), C.byref(handle)) == 0
    assert pam.pam_authenticate(handle, 0) == 0, 'Native password authentication failed'
    assert pam.pam_acct_mgmt(handle, 0) == 0
    saved_output = [os.dup(1), os.dup(2)]
    with open(os.devnull, 'w') as quiet:
        os.dup2(quiet.fileno(), 1)
        os.dup2(quiet.fileno(), 2)
        try:
            assert pam.pam_open_session(handle, 0) == 0
        finally:
            for descriptor, saved in zip((1, 2), saved_output):
                os.dup2(saved, descriptor)
                os.close(saved)
    socket = pam.pam_getenv(handle, b'PAM_KWALLET5_LOGIN')
    assert socket, 'Native PAM did not create its unlock socket'
    print('Native PAM authentication/account/session and unlock socket: PASS', flush=True)
finally:
    service.unlink()
os.setgroups([])
os.setgid(user.pw_gid)
os.setuid(user.pw_uid)
os.environ.update(HOME=user.pw_dir, USER=user.pw_name, LOGNAME=user.pw_name, XDG_RUNTIME_DIR=f'/run/user/{user.pw_uid}', PAM_KWALLET5_LOGIN=socket.decode())
# Supply the real desktop environment through the native handshake helper.
for line in subprocess.check_output(['systemctl', '--user', 'show-environment'], text=True).splitlines():
    key, _, value = line.partition('=')
    os.environ[key] = value
os.environ['DBUS_SESSION_BUS_ADDRESS'] = f'unix:path=/run/user/{user.pw_uid}/bus'
if '--isolated' in sys.argv:
    temporary = tempfile.TemporaryDirectory(prefix='qubix-kwallet-')
    os.environ.update(XDG_DATA_HOME=temporary.name + '/data', XDG_CONFIG_HOME=temporary.name + '/config', QT_QPA_PLATFORM='offscreen')
    address, bus_pid = subprocess.check_output(['dbus-daemon', '--session', '--fork', '--print-address', '--print-pid'], text=True).splitlines()
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = address
subprocess.run(['/usr/lib/pam_kwallet_init'], check=True, timeout=15)
print('Native PAM environment handshake: PASS', flush=True)

if '--isolated' in sys.argv:
    try:
        time.sleep(2)
        subprocess.run(['python3', '-c', """
import gi
gi.require_version('Secret', '1')
from gi.repository import Secret
service = Secret.Service.get_sync(Secret.ServiceFlags.OPEN_SESSION | Secret.ServiceFlags.LOAD_COLLECTIONS, None)
collections = service.get_collections()
assert len(collections) == 1 and not collections[0].get_locked(), 'Native PAM did not unlock wallet'
collection = collections[0]
item = Secret.Item.create_sync(collection, None, {'qubix-test': 'native'}, 'Qubix disposable probe', Secret.Value.new('temporary-value', -1, 'text/plain'), Secret.ItemCreateFlags.NONE, None)
item.load_secret_sync(None)
assert item.get_secret().get_text() == 'temporary-value'
assert item.delete_sync(None)
print('Isolated PAM unlock and Secret Service store/read/delete: PASS')
"""], check=True, timeout=20)
    finally:
        result = subprocess.check_output(['busctl', '--address=' + address, 'call', 'org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus', 'GetConnectionUnixProcessID', 's', 'org.kde.secretservicecompat'], text=True)
        os.kill(int(result.split()[1]), 15)
        os.kill(int(bus_pid), 15)
        time.sleep(1)
        temporary.cleanup()
