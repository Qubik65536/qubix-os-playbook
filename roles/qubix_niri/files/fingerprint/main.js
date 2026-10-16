import Gtk from 'gi://Gtk?version=4.0';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Gdk from 'gi://Gdk?version=4.0';
import {Enrollment, fingers} from './controller.js';
import {Fprintd} from './fprintd.js';

const reference = ARGV.includes('--reference-preview');
const preview = reference || ARGV.includes('--preview');
const app = new Gtk.Application({application_id: preview ? 'org.qubix.Fingerprint.Preview' : 'org.qubix.Fingerprint',
    flags: Gio.ApplicationFlags.DEFAULT_FLAGS});
const title = finger => finger.replace('-finger', '').split('-').map(s => s[0].toUpperCase() + s.slice(1)).join(' ');

// An isolated, explicit preview never connects to the system bus or reads account data.
class Preview {
    async connect() { return {name: 'Preview reader · simulated scans', stages: 8, scan: 'press'}; }
    async list() { return []; }
    unsubscribe() {}
    async disconnect() {}
}

app.connect('activate', () => {
    if (app.active_window) { app.active_window.present(); return; }
    const provider = new Gtk.CssProvider();
    provider.load_from_path(`${GLib.path_get_dirname(GLib.filename_from_uri(import.meta.url)[0])}/style.css`);
    if (!reference) Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION);
    const window = new Gtk.ApplicationWindow({application: app, title: preview ? 'Fingerprint setup · Preview' : 'Fingerprint setup',
        default_width: 496, default_height: 530, resizable: false});
    const header = new Gtk.HeaderBar({show_title_buttons: true});
    header.set_title_widget(new Gtk.Label({label: 'QubixOS', css_classes: ['brand']}));
    window.set_titlebar(header);
    const body = new Gtk.Box({orientation: Gtk.Orientation.VERTICAL, spacing: 18,
        margin_start: 28, margin_end: 28, margin_top: 18, margin_bottom: 24});
    window.set_child(body);
    const top = new Gtk.Box({orientation: Gtk.Orientation.HORIZONTAL, spacing: 14});
    top.append(new Gtk.Image({file: `${GLib.path_get_dirname(GLib.filename_from_uri(import.meta.url)[0])}/fingerprint.svg`,
        pixel_size: 38, css_classes: ['accent']}));
    const heading = new Gtk.Box({orientation: Gtk.Orientation.VERTICAL, spacing: 5});
    heading.append(new Gtk.Label({label: 'Fingerprint setup', xalign: 0, css_classes: ['heading']}));
    heading.append(new Gtk.Label({label: 'Add a fingerprint for this account.', xalign: 0, css_classes: ['muted']}));
    top.append(heading);
    body.append(top);
    const device = new Gtk.Label({label: '', xalign: 0, ellipsize: 3, css_classes: ['muted', 'small']});
    body.append(device);
    const choices = new Gtk.Box({orientation: Gtk.Orientation.HORIZONTAL, spacing: 12, homogeneous: true});
    const buttons = new Map();
    for (const side of ['left', 'right']) {
        const column = new Gtk.Box({orientation: Gtk.Orientation.VERTICAL, spacing: 5});
        column.append(new Gtk.Label({label: `${side === 'left' ? 'Left' : 'Right'} hand`, xalign: 0, css_classes: ['section']}));
        for (const finger of fingers.filter(f => f.startsWith(side))) {
            const button = new Gtk.Button({label: title(finger).replace(/^(Left|Right) /, ''), css_classes: ['finger']});
            button.connect('clicked', () => controller.select(finger));
            column.append(button);
            buttons.set(finger, button);
        }
        choices.append(column);
    }
    body.append(choices);
    const card = new Gtk.Box({orientation: Gtk.Orientation.VERTICAL, spacing: 10, css_classes: ['status-card']});
    const selected = new Gtk.Label({xalign: 0, css_classes: ['section']});
    const message = new Gtk.Label({xalign: 0, wrap: true, max_width_chars: 46, lines: 3});
    const progress = new Gtk.ProgressBar({show_text: true});
    card.append(selected); card.append(message); card.append(progress); body.append(card);
    body.append(new Gtk.Label({label: 'Your password remains available. Login setup is separate.',
        xalign: 0, wrap: true, css_classes: ['muted', 'small']}));
    const actions = new Gtk.Box({orientation: Gtk.Orientation.HORIZONTAL, spacing: 10, halign: Gtk.Align.END});
    const cancel = new Gtk.Button({label: 'Close'});
    const primary = new Gtk.Button({label: 'Start enrollment', css_classes: ['primary']});
    actions.append(cancel); actions.append(primary); body.append(actions);
    let state;
    const controller = new Enrollment(preview ? new Preview() : new Fprintd(), value => {
        state = value;
        device.label = value.name;
        selected.label = title(value.finger);
        message.label = value.message;
        for (const [finger, button] of buttons) {
            const enrolled = value.enrolled.includes(finger);
            button.label = title(finger).replace(/^(Left|Right) /, '') + (enrolled ? '  ✓' : '');
            button.sensitive = !value.busy && value.phase !== 'loading';
            if (finger === value.finger) button.add_css_class('selected');
            else button.remove_css_class('selected');
        }
        const saved = value.enrolled.includes(value.finger);
        primary.label = value.phase === 'enrolling' ? 'Enrolling…' : value.phase === 'verifying' ? 'Testing…'
            : value.phase === 'error' && !value.name ? 'Find reader' : saved ? 'Test reader' : 'Start enrollment';
        primary.sensitive = !preview && !value.busy && value.phase !== 'loading';
        cancel.label = value.busy ? 'Cancel' : 'Close';
        cancel.sensitive = !['cancelling', 'finishing'].includes(value.phase);
        progress.visible = value.mode === 'enroll' && ['enrolling', 'success', 'finishing'].includes(value.phase) && value.stages > 0;
        progress.fraction = Math.min(1, value.completed / Math.max(1, value.stages));
        progress.text = `${value.completed} of ${value.stages} scans`;
        if (value.phase === 'error') card.add_css_class('error'); else card.remove_css_class('error');
    });
    primary.connect('clicked', () => {
        if (state.phase === 'error' && !state.name) controller.connect();
        else controller.start(state.enrolled.includes(state.finger) ? 'verify' : 'enroll');
    });
    cancel.connect('clicked', () => { if (state.busy) controller.cancel(); else window.close(); });
    let closing = false;
    window.connect('close-request', () => {
        if (closing) return false;
        closing = true;
        window.sensitive = false;
        controller.close().finally(() => window.destroy());
        return true;
    });
    controller.connect().then(() => {
        if (preview && !closing) {
            controller.busy = true;
            controller.emit({phase: 'enrolling', completed: 3,
                message: 'Good scan. Lift your finger and touch a slightly different area.'});
        }
    });
    window.present();
});
app.run([]);
