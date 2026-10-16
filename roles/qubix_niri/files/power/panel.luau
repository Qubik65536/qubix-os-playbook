-- Noctalia owns input focus and native power backends; this panel owns confirmation.
local actions = {
    {action = "lock", label = "Lock", glyph = "lock", needsLock = true},
    {action = "logout", label = "Log out", glyph = "logout"},
    {action = "lock-and-suspend", label = "Lock & Suspend", glyph = "suspend", needsLock = true},
    {action = "reboot", label = "Reboot", glyph = "reboot"},
    {action = "shutdown", label = "Shut down", glyph = "shutdown"},
}
local opened = false
local locking = false
local held = {}
local pending = nil
local message = "Hold a number for 3 seconds, or click for a 5-second countdown."

local function available(index)
    return actions[index] ~= nil and (not actions[index].needsLock or locking)
end

local function cancel()
    pending = nil
    panel.setNeedsFrameTick(false)
end

local function draw()
    if not opened then return end
    local rows = {}
    for index, entry in ipairs(actions) do
        table.insert(rows, ui.button({key = tostring(index), text = tostring(index) .. "  ·  " .. entry.label,
            glyph = entry.glyph, contentAlign = "start", controlSize = "lg", enabled = available(index),
            variant = pending and pending.index == index and "primary" or "outline",
            onClick = function() clickAction(index) end}))
    end
    local status = message
    local progress = 0
    if pending then
        progress = pending.elapsed / pending.duration
        status = actions[pending.index].label .. " in "
            .. tostring(math.ceil((pending.duration - pending.elapsed) / 1000)) .. "s"
            .. (pending.kind == "hold" and " · Keep holding; release to cancel." or " · Click again to cancel.")
    end
    panel.render(ui.column({gap = 12, padding = 12}, {
        ui.label({text = "Power options", fontSize = 25, fontWeight = "bold", color = "on_surface"}),
        ui.column({gap = 8}, rows),
        ui.progress({progress = progress, height = 5, fill = "primary", track = "surface_variant"}),
        ui.label({text = status, fontSize = 12, maxLines = 3, color = "on_surface_variant"}),
        ui.button({text = "Cancel", glyph = "x", variant = "ghost", onClick = "closePanel"}),
    }))
end

local function arm(index, kind)
    pending = {index = index, kind = kind, elapsed = 0, duration = kind == "hold" and 3000 or 5000}
    panel.setNeedsFrameTick(true)
    draw()
end

function clickAction(index)
    if not opened or not available(index) then return end
    local same = pending and pending.kind == "click" and pending.index == index
    cancel()
    message = "Cancelled. Hold a number or click to try again."
    -- A mouse activation cannot confirm a keyboard hold, even when its timer is nearly done.
    if next(held) == nil and not same then arm(index, "click") else draw() end
end

function onKey(chord, pressed)
    if not opened then return end
    local index = tonumber(chord)
    if not index or not actions[index] then return end
    if not pressed then
        held[chord] = nil
        if pending and pending.kind == "hold" and pending.index == index then
            cancel()
            message = "Cancelled on release. Hold the number to try again."
            draw()
        end
        return
    end
    if held[chord] then return end -- Ignore repeats; they never confirm or restart a hold.
    held[chord] = true
    cancel()
    for other in pairs(held) do
        if other ~= chord then
            message = "Cancelled. Release all number keys before trying again."
            draw()
            return
        end
    end
    if available(index) then arm(index, "hold") else draw() end
end

function onFrameTick(deltaMs)
    if not opened or not pending then return end
    -- Fail slowly after a stalled renderer; never credit an unobserved multi-second gap.
    pending.elapsed = pending.elapsed + math.clamp(tonumber(deltaMs) or 0, 0, 100)
    if pending.elapsed < pending.duration then draw(); return end
    local index = pending.index
    if pending.kind == "hold" and not held[tostring(index)] then cancel(); draw(); return end
    -- Recheck at dispatch: IPC otherwise downgrades Lock & Suspend when locking was disabled.
    locking = noctalia.getSetting("lockscreen.enabled") == true
    if not available(index) then
        cancel()
        message = "Cancelled: Noctalia locking is disabled."
        draw()
        return
    end
    cancel()
    opened = false -- Latch before dispatch: stale input/ticks cannot invoke twice.
    panel.close()
    local started = noctalia.runAsync({"/usr/share/qubix/bin/qubix-noctalia", "msg", "session", actions[index].action},
        function(result)
            if result.exitCode ~= 0 or string.match(result.stdout or "", "^error:") then
                local detail = result.stdout
                if not detail or detail == "" then detail = result.stderr end
                noctalia.notifyError("Power action failed", detail or "Noctalia rejected the action.")
            end
        end)
    if not started then noctalia.notifyError("Power action failed", "Could not contact Noctalia.") end
end

function onOpen()
    cancel()
    held = {}
    locking = noctalia.getSetting("lockscreen.enabled") == true
    opened = true
    message = "Hold a number for 3 seconds, or click for a 5-second countdown."
    draw()
end

function onClose()
    opened = false
    held = {}
    cancel()
end

function closePanel()
    onClose()
    panel.close()
end
