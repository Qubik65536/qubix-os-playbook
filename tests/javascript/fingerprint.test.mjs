import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const source = await readFile(new URL('../../roles/qubix_niri/files/fingerprint/controller.js', import.meta.url));
const {Enrollment, fingers, friendlyError} = await import(`data:text/javascript;base64,${source.toString('base64')}`);
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r; }); return {promise, resolve}; };
class Reader {
    constructor() { this.calls = []; this.saved = []; this.block = null; this.fail = null; }
    async call(name) {
        this.calls.push(name);
        if (this.block?.name === name) await this.block.promise;
        if (this.fail === name) throw new Error('PermissionDenied');
    }
    async connect() { await this.call('connect'); return {name: 'Test reader', stages: 4, scan: 'press'}; }
    async list() { await this.call('list'); return [...this.saved]; }
    claim() { return this.call('claim'); }
    subscribe(kind, callback) { this.calls.push('subscribe'); this.callback = callback; }
    unsubscribe() { this.calls.push('unsubscribe'); }
    start(kind, finger) { this.finger = finger; return this.call(`start-${kind}`); }
    stop(kind) { return this.call(`stop-${kind}`); }
    release() { return this.call('release'); }
    disconnect() { return this.call('disconnect'); }
}
async function fixture() {
    const reader = new Reader(); const state = new Enrollment(reader);
    await state.connect(); reader.calls = []; return {reader, state};
}

test('opening only discovers/lists; all ten fingers are valid and arbitrary input is refused', async () => {
    const {reader, state} = await fixture();
    assert.equal(fingers.length, 10);
    for (const finger of fingers) { state.select(finger); assert.equal(state.state.finger, finger); }
    state.select('unknown'); assert.equal(state.state.finger, fingers.at(-1));
    assert.deepEqual(reader.calls, []);
});

test('success requires completed signal and saved listing; cleanup precedes success', async () => {
    const {reader, state} = await fixture();
    await state.start();
    for (let i = 0; i < 8; i++) reader.callback('enroll-stage-passed', false);
    assert.equal(state.state.completed, 3);
    assert.equal(state.busy, true);
    reader.saved = [state.state.finger];
    reader.callback('enroll-completed', true);
    await state.pending;
    assert.equal(state.state.phase, 'success'); assert.equal(state.state.completed, 4);
    assert.deepEqual(reader.calls.slice(-4), ['unsubscribe', 'stop-enroll', 'release', 'list']);
    await state.start(); assert.equal(reader.calls.filter(c => c === 'start-enroll').length, 1);
    await state.start('verify'); reader.callback('verify-match', true); await state.pending;
    assert.match(state.state.message, /recognised/);
});

test('a completion signal without saved data never claims success', async () => {
    const {reader, state} = await fixture(); await state.start();
    reader.callback('enroll-completed', true); await state.pending;
    assert.equal(state.state.phase, 'error'); assert.equal(state.busy, false);
});

for (const status of ['enroll-retry-scan', 'enroll-swipe-too-short', 'enroll-finger-not-centered', 'enroll-remove-and-retry']) {
    test(`${status} keeps the same scan active without advancing progress`, async () => {
        const {reader, state} = await fixture(); await state.start();
        reader.callback(status, false);
        assert.equal(state.state.phase, 'enrolling'); assert.equal(state.state.completed, 0);
        assert.equal(reader.calls.includes('release'), false);
        await state.cancel();
    });
}
for (const status of ['enroll-failed', 'enroll-duplicate', 'enroll-data-full', 'enroll-disconnected', 'enroll-unknown-error']) {
    test(`${status} releases the reader and offers a retry`, async () => {
        const {reader, state} = await fixture(); await state.start();
        reader.callback(status, true); await state.pending;
        assert.equal(state.state.phase, 'error'); assert.equal(state.busy, false);
        assert.ok(reader.calls.indexOf('stop-enroll') < reader.calls.indexOf('release'));
    });
}
for (const stage of ['claim', 'list', 'start-enroll']) {
    test(`cancel during ${stage} waits for reply and cannot start a later scan`, async () => {
        const {reader, state} = await fixture();
        reader.block = {name: stage, ...deferred()};
        const started = state.start();
        for (let i = 0; i < 10; i++) await Promise.resolve();
        const cancelled = state.cancel(); reader.block.resolve();
        await Promise.all([started, cancelled]);
        assert.equal(state.busy, false); assert.equal(state.state.phase, 'ready');
        if (stage !== 'start-enroll') assert.equal(reader.calls.includes('start-enroll'), false);
        else assert.ok(reader.calls.includes('stop-enroll'));
        assert.ok(reader.calls.includes('release'));
    });
}
test('double-start, busy selection and late signals cannot start/change another operation', async () => {
    const {reader, state} = await fixture(); await state.start();
    const callback = reader.callback; const finger = state.state.finger;
    state.select('left-thumb'); await state.start();
    assert.equal(state.state.finger, finger);
    assert.equal(reader.calls.filter(c => c === 'claim').length, 1);
    await state.cancel(); callback('enroll-completed', true); await state.pending;
    assert.equal(state.state.phase, 'ready');
});
for (const stage of ['claim', 'list', 'start-enroll', 'stop-enroll', 'release']) {
    test(`${stage} failure never leaves the UI busy or a claimed connection alive`, async () => {
        const {reader, state} = await fixture(); reader.fail = stage;
        await state.start();
        if (state.busy) { reader.callback('enroll-completed', true); await state.pending; }
        assert.equal(state.busy, false); assert.equal(state.claimed, false);
        if (['stop-enroll', 'release'].includes(stage)) assert.ok(reader.calls.includes('disconnect'));
    });
}
test('closing during a pending claim cleans up and suppresses later rendering', async () => {
    const {reader, state} = await fixture(); reader.block = {name: 'claim', ...deferred()};
    const start = state.start(); const close = state.close(); reader.block.resolve();
    await Promise.all([start, close]);
    assert.ok(reader.calls.includes('release')); assert.equal(reader.calls.at(-1), 'disconnect');
    await state.start(); assert.equal(reader.calls.includes('start-enroll'), false);
});
test('saved finger race and verify-without-enrollment are refused', async () => {
    const {reader, state} = await fixture(); await state.start('verify');
    assert.deepEqual(reader.calls, []);
    reader.saved = [state.state.finger]; await state.start();
    assert.equal(reader.calls.includes('start-enroll'), false); assert.ok(reader.calls.includes('release'));
});
test('friendly errors cover permission, busy and unavailable readers', () => {
    assert.match(friendlyError(new Error('PermissionDenied')), /local desktop/);
    assert.match(friendlyError(new Error('AlreadyInUse')), /busy/);
    assert.match(friendlyError(new Error('NoSuchDevice')), /No supported/);
});

for (const status of ['verify-retry-scan', 'verify-swipe-too-short', 'verify-finger-not-centered', 'verify-remove-and-retry']) {
    test(`${status} keeps verification active without starting another scan`, async () => {
        const {reader, state} = await fixture();
        reader.saved = [state.state.finger]; state.emit({enrolled: [...reader.saved]});
        await state.start('verify'); reader.callback(status, false);
        assert.equal(state.state.phase, 'verifying'); assert.equal(state.busy, true);
        assert.equal(state.state.mode, 'verify'); await state.cancel();
        assert.ok(reader.calls.includes('verify-stop') || reader.calls.includes('stop-verify'));
    });
}
for (const status of ['verify-no-match', 'verify-disconnected', 'verify-unknown-error']) {
    test(`${status} fails safely with Stop before Release`, async () => {
        const {reader, state} = await fixture();
        reader.saved = [state.state.finger]; state.emit({enrolled: [...reader.saved]});
        await state.start('verify'); reader.callback(status, true); await state.pending;
        assert.equal(state.state.phase, 'error'); assert.equal(state.busy, false);
        assert.deepEqual(reader.calls.slice(-3), ['unsubscribe', 'stop-verify', 'release']);
    });
}
test('cancelling a just-completed enrollment refreshes saved fingers instead of claiming it was undone', async () => {
    const {reader, state} = await fixture(); await state.start();
    reader.block = {name: 'stop-enroll', ...deferred()};
    reader.saved = [state.state.finger]; reader.callback('enroll-completed', true);
    await Promise.resolve(); const cancelled = state.cancel(); reader.block.resolve(); await cancelled;
    assert.deepEqual(state.state.enrolled, reader.saved);
    assert.match(state.state.message, /may remain saved/);
});
