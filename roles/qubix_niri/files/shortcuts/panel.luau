-- Qubix shortcut presenter. Display data is generated from the managed KDL.
local bindings = {}
local query = ""
local inputRevision = 0
local categories = {"Applications", "Windows", "Navigation", "Session", "Media"}
local icons = {Applications = "apps", Windows = "layout", Navigation = "arrows-move",
               Session = "command", Media = "volume"}

local function keyName(key)
    local names = {Mod = "Super", Shift = "Shift", Ctrl = "Ctrl", Alt = "Alt",
        Return = "Enter", Space = "Space", Comma = ",", Slash = "/",
        Left = "←", Right = "→", Up = "↑", Down = "↓", Page_Up = "PgUp", Page_Down = "PgDn",
        XF86AudioRaiseVolume = "Volume ↑", XF86AudioLowerVolume = "Volume ↓",
        XF86AudioMute = "Mute", XF86AudioMicMute = "Mic mute", XF86AudioPlay = "Play",
        XF86AudioPause = "Pause", XF86AudioNext = "Next", XF86AudioPrev = "Previous",
        XF86MonBrightnessUp = "Brightness ↑", XF86MonBrightnessDown = "Brightness ↓"}
    local parts = {}
    for part in string.gmatch(key, "[^+]+") do
        table.insert(parts, names[part] or part)
    end
    return table.concat(parts, " + ")
end

local function matches(item)
    if query == "" then return true end
    local text = item.label .. " " .. table.concat(item.keys, " ")
    for _, key in ipairs(item.keys) do text ..= " " .. keyName(key) end
    return string.find(string.lower(text), string.lower(query), 1, true) ~= nil
end

local function shortcutRow(item)
    local keyChildren = {}
    for index, key in ipairs(item.keys) do
        local cap = ui.row({paddingH = 9, paddingV = 6, radius = 8,
                fill = "#56728b40", border = "#56728b88", borderWidth = 1,
                align = "center"}, {
            ui.label({text = keyName(key), fontFamily = "monospace",
                      fontSize = 11, color = "on_surface", maxWidth = 210}),
        })
        if index == 1 then
            table.insert(keyChildren, cap)
        else
            table.insert(keyChildren, ui.row({gap = 5, align = "center"}, {
                ui.label({text = "or", color = "on_surface_variant", fontSize = 10}), cap,
            }))
        end
    end
    return ui.row({gap = 12, paddingV = 3, align = "center"}, {
        ui.column({gap = 3, align = "start"}, keyChildren),
        ui.label({text = item.label, color = "on_surface", fontSize = 12,
                  flexGrow = 1}),
    })
end

function draw()
    local columns = { {}, {} }
    local heights = {0, 0}
    local count = 0
    for _, category in ipairs(categories) do
        local rows = {}
        for _, item in ipairs(bindings) do
            if item.category == category and matches(item) then
                table.insert(rows, shortcutRow(item))
                count += 1
            end
        end
        if #rows > 0 then
            local content = {
                ui.row({gap = 8, align = "center"}, {
                    ui.glyph({name = icons[category], size = 18, color = "secondary"}),
                    ui.label({text = category, fontSize = 14, fontWeight = "bold", color = "on_surface"}),
                }),
                ui.separator({color = "#56728b66", spacing = 4}),
            }
            for _, row in ipairs(rows) do table.insert(content, row) end
            local side = heights[1] <= heights[2] and 1 or 2
            table.insert(columns[side], ui.column({gap = 6, padding = 14, radius = 14,
                         fill = "surface_variant", border = "#56728b55", borderWidth = 1}, content))
            heights[side] += #rows + 2
        end
    end
    local body
    if count == 0 then
        body = ui.column({padding = 32, align = "center", gap = 12}, {
            ui.glyph({name = "search", size = 32, color = "secondary"}),
            ui.label({text = "No shortcuts match. Try launcher, window or volume.",
                      color = "on_surface_variant", maxLines = 2}),
        })
    else
        body = ui.row({gap = 14, align = "start"}, {
            ui.column({gap = 14, flexGrow = 1}, columns[1]),
            ui.column({gap = 14, flexGrow = 1}, columns[2]),
        })
    end
    panel.render(ui.column({gap = 14, padding = 8, flexGrow = 1}, {
        ui.row({gap = 12, align = "center"}, {
            ui.glyph({name = "keyboard", size = 32, color = "secondary"}),
            ui.column({gap = 3, flexGrow = 1}, {
                ui.label({text = "Keyboard shortcuts", fontSize = 25, fontWeight = "bold",
                          color = "on_surface"}),
                ui.label({text = "QUBIX  /  NIRI", fontSize = 11, color = "secondary"}),
            }),
            ui.button({text = "Close", glyph = "x", variant = "ghost", onClick = "closePanel"}),
        }),
        ui.input({key = "shortcut-search-" .. tostring(inputRevision), value = query, placeholder = "Find an action or key…",
                  onChange = "onSearch", focus = true}),
        ui.scroll({flexGrow = 1}, {body}),
        ui.label({text = tostring(count) .. (count == 1 and " shortcut" or " shortcuts")
                         .. (query ~= "" and " matching “" .. query .. "”" or "")
                         .. "  ·  Super = desktop modifier  ·  Esc to close",
                  fontSize = 11, color = "on_surface_variant"}),
        ui.label({text = "Your apps keep their own shortcuts, including Ctrl+C and Ctrl+V.",
                  fontSize = 10, color = "on_surface_variant"}),
    }))
end

local function loadBindings()
    local raw, readError = noctalia.readFile(noctalia.pluginDir() .. "/bindings.json")
    assert(raw, readError or "Shortcut data is unavailable")
    local data, decodeError = noctalia.json.decode(raw)
    assert(type(data) == "table", decodeError or "Shortcut data is invalid")
    bindings = {}
    local byLabel = {}
    for _, binding in ipairs(data) do
        local category, label = string.match(binding[2], "^(.-) / (.+)$")
        assert(category and icons[category], "Unknown shortcut category")
        local item = byLabel[binding[2]]
        if not item then
            item = {category = category, label = label, keys = {}}
            byLabel[binding[2]] = item
            table.insert(bindings, item)
        end
        table.insert(item.keys, binding[1])
    end
end

function onOpen(context)
    loadBindings()
    query = tostring(context or "")
    inputRevision += 1
    draw()
end

function onSearch(value)
    query = tostring(value or "")
    draw()
end

function onIpc(event, payload)
    if event == "search" then
        -- Inputs keep typed text across renders; replace only for an external search.
        inputRevision += 1
        onSearch(payload)
    end
end

function closePanel()
    panel.close()
end
