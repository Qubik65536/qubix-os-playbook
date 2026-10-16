import Gio from 'gi://Gio';
import GLib from 'gi://GLib';

const service = 'net.reactivated.Fprint';
const iface = `${service}.Device`;

export class Fprintd {
    constructor() { this.bus = null; this.path = null; this.subscription = 0; this.ownerWatch = 0; this.closedWatch = 0; }

    async call(path, name, method, args = null, type = null) {
        return new Promise((resolve, reject) => {
            this.bus.call(service, path, name, method, args,
                type ? new GLib.VariantType(type) : null,
                Gio.DBusCallFlags.ALLOW_INTERACTIVE_AUTHORIZATION, 30000, null,
                (bus, result) => {
                    try { resolve(bus.call_finish(result).deepUnpack()); }
                    catch (error) { reject(error); }
                });
        });
    }

    async connect() {
        if (!this.bus || this.bus.is_closed()) {
            const address = Gio.dbus_address_get_for_bus_sync(Gio.BusType.SYSTEM, null);
            this.bus = await new Promise((resolve, reject) => {
                Gio.DBusConnection.new_for_address(address,
                    Gio.DBusConnectionFlags.AUTHENTICATION_CLIENT | Gio.DBusConnectionFlags.MESSAGE_BUS_CONNECTION,
                    null, null, (_source, result) => {
                        try { resolve(Gio.DBusConnection.new_for_address_finish(result)); }
                        catch (error) { reject(error); }
                    });
            });
            this.bus.set_exit_on_close(false);
        }
        [this.path] = await this.call('/net/reactivated/Fprint/Manager', `${service}.Manager`, 'GetDefaultDevice');
        const [props] = await this.call(this.path, 'org.freedesktop.DBus.Properties', 'GetAll',
            new GLib.Variant('(s)', [iface]));
        return {name: props.name?.deepUnpack() ?? 'Fingerprint reader',
            stages: Math.max(0, props['num-enroll-stages']?.deepUnpack() ?? 0),
            scan: props['scan-type']?.deepUnpack() ?? 'press'};
    }

    async list() {
        try {
            const [items] = await this.call(this.path, iface, 'ListEnrolledFingers',
                new GLib.Variant('(s)', [GLib.get_user_name()]));
            return items;
        } catch (error) {
            if (String(error).includes('NoEnrolledPrints')) return [];
            throw error;
        }
    }

    async claim() {
        const device = await this.connect();
        await this.call(this.path, iface, 'Claim', new GLib.Variant('(s)', ['']));
        return device;
    }

    start(kind, finger) {
        return this.call(this.path, iface, kind === 'enroll' ? 'EnrollStart' : 'VerifyStart',
            new GLib.Variant('(s)', [finger]));
    }
    stop(kind) { return this.call(this.path, iface, kind === 'enroll' ? 'EnrollStop' : 'VerifyStop'); }
    release() { return this.call(this.path, iface, 'Release'); }

    subscribe(kind, callback) {
        this.unsubscribe();
        this.subscription = this.bus.signal_subscribe(service, iface,
            kind === 'enroll' ? 'EnrollStatus' : 'VerifyStatus', this.path, null,
            Gio.DBusSignalFlags.NONE, (_bus, _sender, _path, _iface, _signal, args) => callback(...args.deepUnpack()));
        this.ownerWatch = this.bus.signal_subscribe('org.freedesktop.DBus', 'org.freedesktop.DBus',
            'NameOwnerChanged', '/org/freedesktop/DBus', service, Gio.DBusSignalFlags.NONE,
            (_bus, _sender, _path, _iface, _signal, args) => {
                const [, , owner] = args.deepUnpack();
                if (!owner) callback(`${kind}-disconnected`, true);
            });
        this.closedWatch = this.bus.connect('closed', () => callback(`${kind}-disconnected`, true));
    }

    unsubscribe() {
        if (this.subscription && this.bus && !this.bus.is_closed()) this.bus.signal_unsubscribe(this.subscription);
        if (this.ownerWatch && this.bus && !this.bus.is_closed()) this.bus.signal_unsubscribe(this.ownerWatch);
        if (this.closedWatch && this.bus) this.bus.disconnect(this.closedWatch);
        this.subscription = 0;
        this.ownerWatch = 0;
        this.closedWatch = 0;
    }

    async disconnect() {
        this.unsubscribe();
        if (this.bus && !this.bus.is_closed()) {
            await new Promise(resolve => this.bus.close(null, (bus, result) => {
                try { bus.close_finish(result); } catch (_) { /* Already disconnected. */ }
                resolve();
            }));
        }
        this.bus = null;
        this.path = null;
    }
}
