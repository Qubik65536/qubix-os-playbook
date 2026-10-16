// UI-independent fprintd lifecycle. The adapter owns one D-Bus connection/claim.
export const fingers = ['left-thumb', 'left-index-finger', 'left-middle-finger',
    'left-ring-finger', 'left-little-finger', 'right-thumb', 'right-index-finger',
    'right-middle-finger', 'right-ring-finger', 'right-little-finger'];

const guidance = {
    'enroll-retry-scan': 'That scan was unclear. Lift your finger and try again.',
    'enroll-swipe-too-short': 'Swipe the full length of your finger over the reader.',
    'enroll-finger-not-centered': 'Move your finger to the centre of the reader.',
    'enroll-remove-and-retry': 'Lift your finger completely, then touch the reader again.',
    'verify-retry-scan': 'Try again with a clean, dry finger.',
    'verify-swipe-too-short': 'Swipe the full length of your finger.',
    'verify-finger-not-centered': 'Centre your finger on the reader.',
    'verify-remove-and-retry': 'Lift your finger, then try again.',
};
const failures = {
    'enroll-duplicate': 'This fingerprint is already registered. Choose a different finger.',
    'enroll-data-full': 'The reader is full. Manage existing fingerprints before adding another.',
    'enroll-disconnected': 'The reader disconnected. Reconnect it and try again.',
    'verify-disconnected': 'The reader disconnected. Reconnect it and try again.',
    'verify-no-match': 'No match. You can test again or choose another finger.',
};

export function friendlyError(error) {
    const text = String(error?.message ?? error);
    if (/PermissionDenied|Not Authorized|AccessDenied/.test(text))
        return 'Permission was denied. Open Fingerprint setup in your active local desktop session.';
    if (/AlreadyInUse|ClaimDevice/.test(text))
        return 'The reader is busy. Close other fingerprint tools and try again.';
    if (/NoSuchDevice|No devices|ServiceUnknown/.test(text))
        return 'No supported fingerprint reader was found. Check the fingerprint setup guide.';
    if (/NoEnrolledPrints/.test(text)) return 'No fingerprints are saved for this account.';
    return 'The reader could not complete the request. Try again, or check the fingerprint setup guide.';
}

export class Enrollment {
    constructor(adapter, changed = () => {}) {
        this.adapter = adapter;
        this.changed = changed;
        this.state = {phase: 'loading', message: 'Looking for your fingerprint reader…',
            finger: 'right-index-finger', enrolled: [], stages: 0, completed: 0, name: '', scan: 'press', mode: 'enroll'};
        this.busy = false;
        this.cancelled = false;
        this.closed = false;
        this.operation = null;
        this.claimed = false;
        this.serial = 0;
        this.pending = Promise.resolve();
    }

    emit(values) {
        Object.assign(this.state, values);
        if (!this.closed) this.changed({...this.state, enrolled: [...this.state.enrolled], busy: this.busy});
    }

    async connect() {
        if (this.busy || this.closed) return;
        this.busy = true;
        this.emit({phase: 'loading', message: 'Looking for your fingerprint reader…'});
        this.pending = (async () => {
            try {
                const device = await this.adapter.connect();
                const enrolled = await this.adapter.list();
                this.emit({...device, enrolled, phase: 'ready', message: 'Choose a finger to get started.'});
            } catch (error) {
                this.emit({phase: 'error', message: friendlyError(error)});
            } finally {
                this.busy = false;
                this.emit({});
            }
        })();
        return this.pending;
    }

    select(finger) {
        if (this.busy || !fingers.includes(finger)) return;
        this.emit({finger, completed: 0, phase: 'ready', message: this.state.enrolled.includes(finger)
            ? 'This finger is saved. Test it, or choose another finger to enroll.' : 'Choose Start enrollment when you are ready.'});
    }

    async start(kind = 'enroll') {
        if (this.busy || this.closed || !['enroll', 'verify'].includes(kind)) return;
        const saved = this.state.enrolled.includes(this.state.finger);
        if ((kind === 'enroll' && saved) || (kind === 'verify' && !saved)) return;
        this.busy = true;
        this.cancelled = false;
        const serial = ++this.serial;
        this.emit({phase: 'claiming', mode: kind, completed: 0, message: 'Preparing the reader…'});
        this.pending = (async () => {
            try {
                const device = await this.adapter.claim();
                this.claimed = true;
                if (device) this.emit(device);
                if (this.cancelled) return;
                // Recheck after claiming: another process may have enrolled this finger.
                const enrolled = await this.adapter.list();
                this.emit({enrolled});
                if (this.cancelled) return;
                if (kind === 'enroll' && enrolled.includes(this.state.finger))
                    throw new Error('This finger is already saved');
                this.adapter.subscribe(kind, (status, done) => {
                    if (serial === this.serial && !this.cancelled && this.operation === kind)
                        this.status(kind, status, done);
                });
                this.operation = kind;
                this.emit({phase: kind === 'enroll' ? 'enrolling' : 'verifying',
                    message: this.state.scan === 'swipe' ? 'Swipe your finger over the reader.' : 'Touch the reader, then lift your finger.'});
                await this.adapter.start(kind, this.state.finger);
            } catch (error) {
                if (!this.cancelled) this.emit({phase: 'error', message: friendlyError(error)});
                try { await this.cleanup(); }
                catch (_) { /* The dedicated connection was closed to release the device. */ }
                await this.adapter.disconnect();
                this.busy = false;
                this.emit({});
            } finally {
                if (this.cancelled) {
                    try { await this.cleanup(); }
                    catch (_) { /* A disconnected reader cannot retain this bus claim. */ }
                    this.busy = false;
                    this.emit({phase: 'ready', completed: 0, message: 'Cancelled. A scan that already completed may remain saved.'});
                }
            }
        })();
        return this.pending;
    }

    status(kind, status, done) {
        if (!done) {
            if (status === 'enroll-stage-passed') this.emit({
                completed: Math.min(this.state.completed + 1, Math.max(0, this.state.stages - 1)),
                message: 'Good scan. Lift your finger and touch a slightly different area.'});
            else this.emit({message: guidance[status] ?? 'Follow the reader’s instructions and try again.'});
            return;
        }
        // Fence repeated/stale signals while Stop/Release and confirmation are outstanding.
        ++this.serial;
        this.emit({phase: 'finishing', message: 'Finishing…'});
        this.pending = this.pending.then(async () => {
            try {
                await this.cleanup();
                if (this.cancelled) return;
                if (kind === 'enroll' && status === 'enroll-completed') {
                    const enrolled = await this.adapter.list();
                    if (!enrolled.includes(this.state.finger)) throw new Error('Enrollment was not saved');
                    this.emit({enrolled, phase: 'success', completed: this.state.stages,
                        message: 'Fingerprint saved. Test the reader when you are ready.'});
                } else if (kind === 'verify' && status === 'verify-match') {
                    this.emit({phase: 'success', message: 'Fingerprint recognised. Your reader is ready.'});
                } else this.emit({phase: 'error', message: failures[status]
                    ?? 'The scan could not finish. Try again with a clean, dry finger.'});
            } catch (error) {
                this.emit({phase: 'error', message: friendlyError(error)});
            } finally {
                this.busy = false;
                this.emit({});
            }
        });
    }

    async cleanup() {
        this.adapter.unsubscribe();
        const operation = this.operation;
        this.operation = null;
        let failure;
        if (operation) {
            try { await this.adapter.stop(operation); } catch (error) { failure = error; }
        }
        if (this.claimed) {
            try { await this.adapter.release(); } catch (error) { failure ??= error; }
            this.claimed = false;
        }
        // Closing the dedicated bus connection guarantees fprintd releases a lost claim.
        if (failure) {
            await this.adapter.disconnect();
            throw failure;
        }
    }

    async cancel() {
        if (!this.busy) return;
        this.cancelled = true;
        ++this.serial;
        this.emit({phase: 'cancelling', message: 'Cancelling…'});
        await this.pending;
        // Claim/Start may have been pending. Stop them only after their reply.
        try { await this.cleanup(); }
        catch (error) { this.emit({phase: 'error', message: friendlyError(error)}); }
        this.busy = false;
        try { this.emit({enrolled: await this.adapter.list()}); }
        catch (_) { /* Discovery can be retried if the reader is disconnected. */ }
        this.emit({phase: 'ready', completed: 0, message: 'Cancelled. A scan that already completed may remain saved.'});
    }

    async close() {
        this.closed = true;
        await this.cancel();
        await this.adapter.disconnect();
    }
}
