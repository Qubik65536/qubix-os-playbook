// Native GJS test. Both D-Bus addresses must be the same disposable session bus.
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
if (!GLib.getenv('DBUS_SESSION_BUS_ADDRESS') ||
    GLib.getenv('DBUS_SYSTEM_BUS_ADDRESS') !== GLib.getenv('DBUS_SESSION_BUS_ADDRESS'))
    throw new Error('Refusing to test outside the explicit private bus');
const {Fprintd} = await import(GLib.filename_to_uri(`${ARGV[0]}/fprintd.js`, null));
const {Enrollment} = await import(GLib.filename_to_uri(`${ARGV[0]}/controller.js`, null));
const service = 'net.reactivated.Fprint';
const path = '/net/reactivated/Fprint/Device/0';
const bus = Gio.bus_get_sync(Gio.BusType.SESSION, null);
const calls = [];
let saved = [];
const check = (value, message) => { if (!value) throw new Error(message); };
const manager = Gio.DBusExportedObject.wrapJSObject(`<node><interface name="${service}.Manager">
    <method name="GetDefaultDevice"><arg type="o" direction="out"/></method></interface></node>`,
{GetDefaultDevice() { return path; }});
const xml = `<node><interface name="${service}.Device">
    <property name="name" type="s" access="read"/>
    <property name="num-enroll-stages" type="i" access="read"/>
    <property name="scan-type" type="s" access="read"/>
    <method name="ListEnrolledFingers"><arg type="s" direction="in"/><arg type="as" direction="out"/></method>
    <method name="Claim"><arg type="s" direction="in"/></method>
    <method name="Release"/>
    <method name="EnrollStart"><arg type="s" direction="in"/></method><method name="EnrollStop"/>
    <method name="VerifyStart"><arg type="s" direction="in"/></method><method name="VerifyStop"/>
    <signal name="EnrollStatus"><arg type="s"/><arg type="b"/></signal>
    <signal name="VerifyStatus"><arg type="s"/><arg type="b"/></signal>
    </interface></node>`;
const device = Gio.DBusExportedObject.wrapJSObject(xml, {
    get name() { return 'Simulated reader'; },
    get ['num-enroll-stages']() { return 4; },
    get ['scan-type']() { return 'press'; },
    ListEnrolledFingers(user) { check(user === GLib.get_user_name(), 'Unexpected target account'); return saved; },
    Claim(user) { check(user === '', 'Claim must use the current account'); calls.push('claim'); },
    Release() { calls.push('release'); },
    EnrollStart(finger) { calls.push(`enroll:${finger}`); },
    EnrollStop() { calls.push('enroll-stop'); },
    VerifyStart(finger) { calls.push(`verify:${finger}`); },
    VerifyStop() { calls.push('verify-stop'); },
});
manager.export(bus, '/net/reactivated/Fprint/Manager');
device.export(bus, path);
bus.call_sync('org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus', 'RequestName',
    new GLib.Variant('(su)', [service, 0]), null, Gio.DBusCallFlags.NONE, 5000, null);
const controller = new Enrollment(new Fprintd());
try {
    await controller.connect();
    check(controller.state.name === 'Simulated reader' && controller.state.stages === 4,
        'Gio property unpacking failed');
    check(!calls.length, 'Opening started a biometric operation');
    await controller.start();
    device.emit_signal('EnrollStatus', new GLib.Variant('(sb)', ['enroll-stage-passed', false]));
    await new Promise(resolve => GLib.timeout_add(GLib.PRIORITY_DEFAULT, 50, () => { resolve(); return GLib.SOURCE_REMOVE; }));
    check(controller.state.completed === 1, 'Real D-Bus enrollment signal was not received');
    saved = [controller.state.finger];
    device.emit_signal('EnrollStatus', new GLib.Variant('(sb)', ['enroll-completed', true]));
    for (let i = 0; i < 100 && controller.busy; i++)
        await new Promise(resolve => GLib.timeout_add(GLib.PRIORITY_DEFAULT, 10, () => { resolve(); return GLib.SOURCE_REMOVE; }));
    check(controller.state.phase === 'success', `Enrollment failed: ${controller.state.message}`);
    check(calls.slice(-2).join(',') === 'enroll-stop,release', 'Stop/Release ordering failed');
    await controller.start('verify');
    device.emit_signal('VerifyStatus', new GLib.Variant('(sb)', ['verify-match', true]));
    for (let i = 0; i < 100 && controller.busy; i++)
        await new Promise(resolve => GLib.timeout_add(GLib.PRIORITY_DEFAULT, 10, () => { resolve(); return GLib.SOURCE_REMOVE; }));
    check(controller.state.phase === 'success' && !controller.busy, 'Verify signal did not complete');
    check(calls.slice(-2).join(',') === 'verify-stop,release', 'Verify cleanup failed');
    await controller.start('verify');
    await controller.cancel();
    check(!controller.busy && !controller.claimed, 'Cancel retained the claim');
    await controller.start('verify');
    bus.call_sync('org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus', 'ReleaseName',
        new GLib.Variant('(s)', [service]), null, Gio.DBusCallFlags.NONE, 5000, null);
    for (let i = 0; i < 100 && controller.busy; i++)
        await new Promise(resolve => GLib.timeout_add(GLib.PRIORITY_DEFAULT, 10, () => { resolve(); return GLib.SOURCE_REMOVE; }));
    check(!controller.busy && !controller.claimed && controller.state.phase === 'error',
        'Service disappearance retained a pending scan/claim');
    print(JSON.stringify({private_bus: true, native_adapter: true, property_unpacking: true,
        enrollment_and_verification_signals: true, cancel_cleanup: true, service_loss_cleanup: true,
        physical_operations: 0}));
} finally {
    await controller.close();
    manager.unexport(); device.unexport();
    bus.close_sync(null);
}
