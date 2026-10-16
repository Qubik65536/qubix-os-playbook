-- Noctalia owns input focus and native power backends; this panel owns confirmation.
local actions = {
    {action = "lock", label = "Lock", glyph = "lock", needsLock = true},
    {action = "logout", label = "Log Out", glyph = "logout"},
    {action = "lock-and-suspend", label = "Lock & Suspend", glyph = "suspend", needsLock = true},
    {action = "reboot", label = "Reboot", glyph = "reboot"},
    {action = "shutdown", label = "Shut Down", glyph = "shutdown"},
}
local opened = false
local locking = false
local held = {}
local pending = nil
local hovered = nil
local confirmed = nil
local message = "Hold 1–5 for 3s · Click for 5s · Esc cancels"

local function available(index)
    return actions[index] ~= nil and (not actions[index].needsLock or locking)
end

local function cancel()
    pending = nil
    panel.setNeedsFrameTick(false)
end

local function draw()
    if not opened then return end
    local tiles = {}
    for index, entry in ipairs(actions) do
        local active = pending and pending.index == index
        local enabled = available(index)
        local destructive = entry.action == "shutdown"
        local highlight = active or (hovered == index and enabled)
        local fill = destructive and "error" or (active and "primary" or (highlight and "hover" or "surface_variant"))
        local foreground = destructive and "on_error" or (active and "on_primary" or (highlight and "on_hover" or "on_surface"))
        local seconds = active and math.ceil((pending.duration - pending.elapsed) / 1000) or nil
        local icon = active
            and ui.label({text = tostring(seconds), fontSize = 28, fontWeight = "bold", color = foreground})
            or ui.glyph({name = entry.glyph, size = 28, color = foreground})
        table.insert(tiles, ui.column({key = tostring(index), width = 152, height = 112,
            paddingH = 4, paddingV = 0, gap = 0, align = "center", justify = "center",
            fill = fill, radius = 12, border = "outline", borderWidth = 1,
            opacity = enabled and 1 or 0.4,
            onClick = enabled and function() clickAction(index) end or nil,
            onHover = "onTileHover", tooltip = message}, {
                ui.row({justify = "end", align = "end", width = 144, height = 24}, {
                    ui.column({width = 20, height = 20, align = "center", justify = "center", radius = 3, fill = foreground .. "/0.85"}, {
                        ui.label({text = tostring(index), fontSize = 10, color = fill}),
                    }),
                }),
                ui.column({gap = 8, height = 64, align = "center", justify = "center"}, {
                    icon,
                    ui.label({text = entry.label, fontSize = 15, color = foreground, textAlign = "center"}),
                }),
                ui.column({height = 24, align = "center", justify = "center"}, {
                    ui.progress({progress = active and pending.elapsed / pending.duration or 0,
                        width = 128, height = 3, fill = foreground, track = "outline/0.15",
                        opacity = active and 1 or 0}),
                }),
            }))
    end
    local prompt = message
    if pending then
        prompt = actions[pending.index].label .. " in "
            .. tostring(math.ceil((pending.duration - pending.elapsed) / 1000)) .. "s"
            .. (pending.kind == "hold" and " · Release to cancel" or " · Click again to cancel")
    end
    panel.render(ui.column({gap = 12}, {
        ui.row({gap = 12, align = "stretch"}, tiles),
        ui.row({gap = 8, align = "center"}, {
            ui.label({text = prompt, fontSize = 11, color = "on_surface_variant", flexGrow = 1}),
            ui.button({text = "Cancel", glyph = "x", variant = "ghost", controlSize = "sm", onClick = "closePanel"}),
        }),
    }))
end

function onTileHover(state, key)
    local index = tonumber(key)
    local nextHover = state == "true" and index or nil
    if state ~= "true" and hovered ~= index then return end
    if hovered == nextHover then return end
    hovered = nextHover
    draw()
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
    message = "Cancelled · Hold a number or click to try again"
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
            message = "Cancelled on release · Hold the number to try again"
            draw()
        end
        return
    end
    if held[chord] then return end -- Ignore repeats; they never confirm or restart a hold.
    held[chord] = true
    cancel()
    for other in pairs(held) do
        if other ~= chord then
            message = "Cancelled · Release all number keys before trying again"
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
    opened = false -- Ignore stale input while the host finishes its close animation.
    confirmed = index
    panel.close()
end

local function dispatch(index)
    -- Noctalia can otherwise downgrade Lock & Suspend to an unlocked suspend.
    if actions[index].needsLock and noctalia.getSetting("lockscreen.enabled") ~= true then
        noctalia.notifyError("Power action cancelled", "Noctalia locking is disabled.")
        return
    end
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
    confirmed = nil
    cancel()
    held = {}
    hovered = nil
    locking = noctalia.getSetting("lockscreen.enabled") == true
    opened = true
    message = "Hold 1–5 for 3s · Click for 5s · Esc cancels"
    draw()
end

function onClose()
    local index = confirmed
    confirmed = nil -- Consume before dispatch; duplicate close callbacks must be inert.
    opened = false
    held = {}
    hovered = nil
    cancel()
    -- Native onClose is queued by destroyPanel after the close animation completes.
    if index then dispatch(index) end
end

function closePanel()
    confirmed = nil
    onClose()
    panel.close()
end
