-- Pull in the wezterm API
local wezterm = require("wezterm")

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices
config.font = wezterm.font_with_fallback({
	"Monaspace Krypton NF",
	"IBM Plex Math",
	"IBM Plex Mono",
	"IBM Plex Sans",
	"IBM Plex Sans SC",
	"IBM Plex Sans TC",
	"IBM Plex Sans JP",
})
config.color_scheme_dirs = { "/etc/qubix/wezterm/colors" }
config.color_scheme = "Oxocarbon Dark"
config.use_fancy_tab_bar = false
config.window_decorations = "RESIZE"
config.hide_tab_bar_if_only_one_tab = true
config.window_background_opacity = 0.75
if wezterm.target_triple:find("apple%-darwin") then
	config.macos_window_background_blur = 75
end
config.send_composed_key_when_left_alt_is_pressed = false
config.send_composed_key_when_right_alt_is_pressed = true

-- and finally, return the configuration to wezterm
return config
