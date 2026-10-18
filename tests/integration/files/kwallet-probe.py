"""Disposable live KDE API roundtrip; never read existing entries or print secrets."""
import uuid

import gi

gi.require_version('Gio', '2.0')
from gi.repository import Gio, GLib

connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
application = 'qubix-validation-' + uuid.uuid4().hex
folder = application


def call(method, signature, values):
    return connection.call_sync(
        'org.kde.kwalletd6', '/modules/kwalletd6', 'org.kde.KWallet', method,
        GLib.Variant(signature, values), None, Gio.DBusCallFlags.NONE, 10000, None,
    ).unpack()[0]


locked = connection.call_sync(
    'org.freedesktop.secrets', '/org/freedesktop/secrets/collection/kdewallet',
    'org.freedesktop.DBus.Properties', 'Get',
    GLib.Variant('(ss)', ('org.freedesktop.Secret.Collection', 'Locked')),
    None, Gio.DBusCallFlags.NONE, 10000, None,
).get_child_value(0).get_variant().get_boolean()
assert not locked, 'Unlock the existing wallet before running a noninteractive probe'

handle = call('open', '(sxs)', ('kdewallet', 0, application))
assert handle > 0
try:
    assert call('createFolder', '(iss)', (handle, folder, application))
    assert call('writePassword', '(issss)', (handle, folder, 'probe', 'temporary-value', application)) == 0
    assert call('readPassword', '(isss)', (handle, folder, 'probe', application)) == 'temporary-value'
    assert call('removeEntry', '(isss)', (handle, folder, 'probe', application)) == 0
    assert call('removeFolder', '(iss)', (handle, folder, application))
    print('KDE Wallet API open/store/read/delete/cleanup: PASS')
finally:
    call('close', '(ibs)', (handle, False, application))
