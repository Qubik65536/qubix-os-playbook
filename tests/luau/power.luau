-- No-effect host: the production panel runs against these APIs, never real IPC.
local test = {calls = {}, errors = {}, ticks = false, locking = true, started = true}
noctalia = {
    getSetting = function(path)
        assert(path == "lockscreen.enabled")
        return test.locking
    end,
    runAsync = function(argv, callback)
        table.insert(test.calls, argv)
        test.callback = callback
        return test.started
    end,
    notifyError = function(title, body) table.insert(test.errors, {title, body}) end,
}
panel = {
    render = function(tree) test.tree = tree end,
    setNeedsFrameTick = function(enabled) test.ticks = enabled end,
    close = function()
        test.closeRequested = true
        if not test.deferClose then onClose() end
    end,
}
ui = {}
for _, kind in ipairs({"button", "column", "row", "glyph", "label", "progress"}) do
    ui[kind] = function(props, children) return {kind = kind, props = props, children = children} end
end

-- INCLUDE_PRODUCTION_PANEL

local function reset(locking)
    onClose()
    test.calls = {}
    test.errors = {}
    test.locking = locking ~= false
    test.started = true
    test.deferClose = false
    test.closeRequested = false
    onOpen()
end

local function tick(count, delta)
    for _ = 1, count do
        -- Noctalia 5.2 delivers the frame delta as a string.
        if test.ticks then onFrameTick(tostring(delta or 100)) end
    end
end

local function idle()
    assert(#test.calls == 0, "Unexpected action")
end

local function invoked(action)
    assert(#test.calls == 1, "Action must run exactly once")
    local argv = test.calls[1]
    assert(#argv == 4 and argv[1] == "/usr/share/qubix/bin/qubix-noctalia"
        and argv[2] == "msg" and argv[3] == "session" and argv[4] == action,
        "Only fixed native IPC argument arrays may execute")
end

for index, action in ipairs({"lock", "logout", "lock-and-suspend", "reboot", "shutdown"}) do
    local key = tostring(index)
    reset()
    onKey(key, true)
    tick(29)
    idle()
    onKey(key, false)
    tick(100)
    idle() -- Early release must discard elapsed time for every action.
    onKey(key, true)
    tick(29)
    idle()
    onKey(key, true) -- Repeat cannot immediately confirm or reset the timer.
    idle()
    tick(1)
    invoked(action)
    onFrameTick(10000)
    onKey(key, true)
    clickAction(index)
    invoked(action) -- Stale events after dispatch are inert.
end

reset()
onKey("1", true)
tick(20)
onKey("2", true)
tick(100)
idle()
onKey("1", false)
tick(100)
idle() -- Releasing one overlapping key cannot rearm the other.
onKey("2", false)
onKey("5", true)
tick(30)
invoked("shutdown")

reset()
onKey("4", true)
tick(29)
onKey("5", false)
tick(1)
invoked("reboot") -- An unrelated release does not cancel the active hold.

reset()
onKey("4", true)
tick(29)
onTileHover("true", "4")
onTileHover("false", "4")
idle() -- Pointer feedback cannot confirm or reset a keyboard hold.
tick(1)
invoked("reboot")

for index, action in ipairs({"lock", "logout", "lock-and-suspend", "reboot", "shutdown"}) do
    reset()
    -- Exercise the actual rendered click callback rather than a duplicate dispatcher.
    test.tree.children[1].children[index].props.onClick()
    tick(49)
    idle()
    tick(1)
    invoked(action)
end

reset()
clickAction(5)
tick(49)
clickAction(5)
tick(100)
idle() -- A second click cancels; no immediate confirmation bypass.
clickAction(4)
tick(49)
clickAction(5)
tick(49)
idle()
tick(1)
invoked("shutdown") -- Changing action starts a fresh timer.

reset()
onKey("4", true)
tick(29)
clickAction(4)
tick(100)
idle() -- Mouse cannot finish a keyboard hold.
onKey("4", false)
clickAction(4)
tick(49)
onKey("5", true)
tick(29)
idle() -- A keyboard hold replaces the click timer without inheriting elapsed time.
onKey("5", false)
tick(100)
idle()

for _, kind in ipairs({"hold", "click"}) do
    for _, close in ipairs({onClose, closePanel}) do
        reset()
        if kind == "hold" then onKey("5", true) else clickAction(5) end
        tick(20)
        close() -- Host Escape/outside click/replacement and explicit Cancel.
        onFrameTick(10000)
        onOpen()
        tick(100)
        idle() -- Reopen does not retain a pending action or held key.
        onKey("5", true)
        tick(30)
        invoked("shutdown")
    end
end

reset(false)
assert(test.tree.children[1].children[1].props.onClick == nil)
assert(test.tree.children[1].children[3].props.onClick == nil)
for _, key in ipairs({"1", "3"}) do
    onKey(key, true)
    tick(100)
    onKey(key, false)
    clickAction(tonumber(key))
    tick(100)
    idle() -- Never silently downgrade Lock & Suspend to unlocked suspend.
end

reset()
onKey("5", true)
onFrameTick(100000)
idle() -- A stalled renderer must not skip the hold interval.
onKey("5", false)
tick(100)
idle()

reset()
onKey("3", true)
tick(29)
test.locking = false
tick(100)
idle() -- Locking disabled during a hold cannot become an unlocked suspend.

-- Model the native animated close: completion arrives later than the timer callback.
for _, action in ipairs({{1, "lock"}, {3, "lock-and-suspend"}, {5, "shutdown"}}) do
    reset()
    test.deferClose = true
    clickAction(action[1])
    tick(50)
    assert(test.closeRequested, "Confirmation must request closure")
    idle() -- Never lock while a final countdown frame is still visible.
    onFrameTick(10000)
    onKey(tostring(action[1]), true)
    idle()
    onClose() -- Host surface destruction/animation completion.
    invoked(action[2])
    onClose()
    invoked(action[2]) -- Exactly once, including duplicate close notifications.
end
reset()
test.deferClose = true
clickAction(5)
tick(50)
closePanel() -- A late Cancel callback must discard the latched action.
onClose()
idle()

reset()
test.deferClose = true
clickAction(3)
tick(50)
test.locking = false
onClose()
idle()
assert(#test.errors == 1, "Recheck locking after the close animation")

reset()
test.started = false
clickAction(4)
tick(50)
assert(#test.errors == 1, "Failed dispatch must be visible")
reset()
clickAction(4)
tick(50)
test.callback({exitCode = 0, stdout = "error: native backend unavailable"})
assert(#test.errors == 1, "Native IPC errors must be visible even with exit code zero")
print("Power panel: hold/release, repeat, overlap, mouse, mixed input, lifecycle, locking, stall and dispatch checks passed.")
