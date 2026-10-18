"""Repository-only documentation and definition consistency checks; not a runtime app."""
from pathlib import Path
import hashlib
import configparser
import json
import re
import tomllib
import shlex
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load(relative):
    return yaml.safe_load((ROOT / relative).read_text())


def main():
    documents = list(ROOT.glob("*.md"))
    for directory in ("docs", "assets", ".github"):
        documents.extend((ROOT / directory).rglob("*.md"))
    for path in documents:
        body = path.read_text()
        assert body.endswith("\n"), f"{path}: missing final newline"
        assert body.count("```") % 2 == 0, f"{path}: unclosed code fence"
        assert all(line == line.rstrip() for line in body.splitlines()), f"{path}: trailing whitespace"
        for link in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in link or link.startswith("#"):
                continue
            target = link.split("#", 1)[0]
            assert (path.parent / target).exists(), f"{path}: missing local link {link}"

    schema = load("roles/qubix_profile/vars/main.yml")["qubix_profile_keys"]
    defaults = load("config/defaults.yml")
    assert set(defaults) == {"profile", *schema}, "Default components differ from the schema"
    for name, keys in schema.items():
        assert set(defaults[name]) == set(keys), f"Default keys differ for {name}"
    assert defaults["bootloader"]["confirm_active"] is False, "Never ship loader confirmation"
    assert defaults["plymouth"]["confirm_active"] is False, "Never ship image-generator confirmation"
    for path in (ROOT / "config/profiles").glob("*.yml"):
        profile = yaml.safe_load(path.read_text())
        assert profile["profile"] == path.stem, f"{path}: profile identity mismatch"
        assert set(profile) <= set(defaults), f"{path}: unknown component"
        for name in set(profile) - {"profile"}:
            assert set(profile[name]) <= set(schema[name]), f"{path}: unknown option"

    profile = load("config/profiles/cachyos-niri.yml")
    expected = {name: options | profile.get(name, {}) for name, options in defaults.items() if name != "profile"}
    expected["profile"] = profile["profile"]
    documentation = (ROOT / "docs/architecture/configuration.md").read_text()
    example = re.search(r"```yaml\n(.*?)```", documentation, re.S)
    assert example, "Missing authoritative configuration example"
    assert yaml.safe_load(example[1])["qubix"] == expected, "Documented defaults differ from the profile"
    documented_inputs = set(re.findall(r"^\| `([^`]+)` \|", documentation, re.M))
    effective_inputs = {"profile"} | {
        f"{component}.{key}" for component, keys in schema.items() for key in keys
    }
    assert documented_inputs == effective_inputs, "Every effective default needs an explanation"
    # Every implemented component ships enabled; machine-specific confirmations remain explicit.
    for component in schema:
        assert expected[component]["enabled"] is True, (
            f"{component}: default-on feature policy violated"
        )
    assert expected["bootloader"]["confirm_active"] is False
    assert expected["plymouth"]["confirm_active"] is False
    assert expected["bootloader"]["config_path"] == ""
    assert expected["plymouth"]["images"] == []
    manifest = load("assets/branding/manifest.yml")
    assert manifest["license"] == "Apache-2.0"
    assert len(manifest["revision"]) == 40
    names = [asset["filename"] for asset in manifest["files"]]
    assert len(names) == len(set(names)), "Duplicate managed asset filename"
    assert set(names) == {"logo.svg", "logo.png", "banner.svg", "LICENSE", "NOTICE"}
    for asset in manifest["files"]:
        source = Path(asset["source"])
        assert not source.is_absolute() and ".." not in source.parts, "Unsafe source asset path"
        assert Path(asset["filename"]).name == asset["filename"], "Unsafe destination filename"
        digest = hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
        assert digest == asset["sha256"], f"Changed source asset without manifest update: {source}"
    wallpaper = load("assets/wallpaper/manifest.yml")
    assert hashlib.sha256((ROOT / "assets/wallpaper/qubix.png").read_bytes()).hexdigest() == wallpaper["sha256"]
    fonts = json.loads((ROOT / 'assets/fonts/manifest.json').read_text())
    assert fonts['family'] == 'Qubix Boot Mono' and fonts['license'] == 'OFL-1.1'
    assert fonts['bitmap_cell'] == [8, 20] and fonts['bitmap_glyphs'] == 256
    assert set(fonts['geometric_cp437_fallbacks']) == {3, 4, 5, 6, 13, 14, 23, 127, 244, 245}
    for asset in fonts['files']:
        data = (ROOT / 'assets/fonts' / asset['filename']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == asset['sha256'] and len(data) == asset['bytes']
    nf = load('assets/fonts/monaspace-nf.yml')
    assert nf['revision'] == 'f31794b6e9e65698a062262e2f826f679dcb7070'
    assert len(nf['files']) == 210 and len({item['filename'] for item in nf['files']}) == 210
    assert {item['filename'].split('NF-')[0] for item in nf['files']} == {
        'MonaspaceArgon', 'MonaspaceKrypton', 'MonaspaceNeon', 'MonaspaceRadon', 'MonaspaceXenon'}
    assert hashlib.sha256((ROOT / 'assets/fonts/Monaspace-NF-LICENSE.txt').read_bytes()).hexdigest() == nf['license_sha256']
    bitmap = (ROOT / 'assets/fonts/QubixBootMono-8x20.bin').read_bytes()
    assert len(bitmap) == 5120
    assert all(any(bitmap[i * 20:(i + 1) * 20]) for i in set(range(256)) - {0, 32, 255})
    vertical = bitmap[0xB3 * 20:0xB4 * 20]
    assert vertical[0] == vertical[-1] != 0, 'Boot menu vertical borders must join cells'
    assert any(row & 0x81 == 0x81 for row in bitmap[0xC4 * 20:0xC5 * 20])
    assert all(code in fonts['subset_codepoints'] for code in range(32, 127))
    boot_art = load('assets/boot/manifest.yml')
    assert boot_art['license'] == 'Apache-2.0'
    assert hashlib.sha256((ROOT / 'assets/boot/wallpaper.png').read_bytes()).hexdigest() == boot_art['sha256']
    assert '<text' not in (ROOT / 'assets/boot/wallpaper.svg').read_text(), 'Boot lettering must be outlined'
    assert '<text' not in (ROOT / 'assets/plymouth/watermark.svg').read_text(), 'Splash lettering must be outlined'
    splash = load('assets/plymouth/manifest.yml')
    assert splash['license'] == 'GPL-3.0-only' and len(splash['revision']) == 40
    assert {asset['filename'] for asset in splash['files']} == {
        'qubix.plymouth', 'watermark.png', 'background.png', 'COPYING', 'NOTICE', 'bullet.png', 'entry.png',
        'capslock.png', 'lock.png', 'keyboard.png', 'keymap-render.png',
        *(f'throbber-{index:04}.png' for index in range(1, 31))}
    for asset in splash['files']:
        assert asset['source'] == 'assets/plymouth/theme/' + asset['filename']
        assert hashlib.sha256((ROOT / asset['source']).read_bytes()).hexdigest() == asset['sha256']
    native = configparser.ConfigParser()
    native.read(ROOT / 'assets/plymouth/theme/qubix.plymouth')
    assert native['Plymouth Theme']['ModuleName'] == 'two-step'
    assert native['two-step']['ImageDir'] == '/usr/share/plymouth/themes/qubix'
    assert native['two-step']['Font'] == 'Qubix Boot Mono 12'
    assert native['two-step'].getboolean('ScaleBackgroundImage')
    for mode in ('boot-up', 'shutdown', 'reboot'):
        assert not native[mode].getboolean('UseFirmwareBackground') and not native[mode].getboolean('UseEndAnimation')
    desktop = ROOT / 'roles/qubix_niri/templates'
    ui_sources = load('assets/ui/manifest.yml')
    for component, spec in ui_sources.items():
        patch = (ROOT / 'assets/ui' / f'{component}.patch').read_bytes()
        assert hashlib.sha256(patch).hexdigest() == spec['patch_sha256'], 'UI patch checksum mismatch'
        paths = set(re.findall(r'^\+\+\+ b/(.+)$', patch.decode(), re.M))
        expected_paths = ({'src/shell/launcher/launcher_panel.cpp', 'src/shell/control_center/tabs/home_tab.cpp'}
                          if component == 'noctalia' else {'src/ui/style.h', 'src/greeter/greeter_surface.cpp'})
        assert paths == expected_paths, 'UI patch touches an unreviewed source area'
    shell = tomllib.loads((desktop / 'noctalia.toml.j2').read_text())
    assert not shell['theme']['templates']['enable_builtin_templates']
    assert not shell['theme']['templates']['enable_community_templates']
    assert not shell['dock']['enabled'] and not shell['dock']['reserve_space']
    launcher = shell['shell']['launcher']
    assert launcher['providers']['session']['global']
    actions = shell['shell']['session']['actions']
    assert [entry['action'] for entry in actions] == ['lock', 'logout', 'lock_and_suspend', 'reboot', 'shutdown']
    assert [entry['shortcut'] for entry in actions] == list('12345'), 'Keep the original power-menu number keys'
    assert actions[-1]['variant'] == 'destructive', 'Retain native shutdown emphasis'
    assert all(entry['countdown_seconds'] == 5 for entry in actions), 'Every power-menu action needs a countdown'
    assert all(entry.get('enabled', True) and 'command' not in entry for entry in actions), 'Keep native power handlers'
    power_entry = configparser.ConfigParser(interpolation=None)
    power_entry.read(desktop / 'power.desktop.j2')
    power = power_entry['Desktop Entry']
    assert Path('qubix-power.desktop').stem in launcher['pinned'], 'Power menu must be available without typing'
    assert power['Type'] == 'Application' and power['Terminal'] == 'false'
    assert shlex.split(power['Exec']) == [power['TryExec'], 'msg', 'panel-toggle', 'qubix/power:menu'], 'Power entry must only open the guarded menu'
    plugin_dir = ROOT / 'roles/qubix_niri/files/shortcuts'
    plugin = tomllib.loads((plugin_dir / 'plugin.toml').read_text())
    panel = plugin['panel'][0]
    assert (plugin_dir / panel['entry']).is_file(), 'Shortcut panel entry is missing'
    assert shell['plugins']['enabled'] == [plugin['id'], 'qubix/power']
    assert shell['plugins']['auto_update'] == 'none'
    assert all(source['kind'] == 'path' for source in shell['plugins']['source'])
    panel_id = plugin['id'] + ':' + panel['id']
    assert panel_id in (desktop / 'config.kdl.j2').read_text()
    assert panel_id in shell['widget']['shortcuts']['actions']['left']
    power_plugin_dir = ROOT / 'roles/qubix_niri/files/power'
    power_plugin = tomllib.loads((power_plugin_dir / 'plugin.toml').read_text())
    power_panel = power_plugin['panel'][0]
    assert power_plugin['plugin_api'] == 26
    assert (power_plugin_dir / power_panel['entry']).is_file()
    assert power_panel['capture_keys'] == list('12345') and power_panel['keyboard_focus'] == 'exclusive'
    power_panel_id = power_plugin['id'] + ':' + power_panel['id']
    assert power_panel_id in (desktop / 'config.kdl.j2').read_text()
    assert power_panel_id in shell['widget']['session']['actions']['left']
    palette = json.loads((desktop / 'palette.json.j2').read_text())['dark']
    roles = {'mPrimary', 'mOnPrimary', 'mSecondary', 'mOnSecondary', 'mTertiary', 'mOnTertiary',
             'mError', 'mOnError', 'mSurface', 'mOnSurface', 'mSurfaceVariant', 'mOnSurfaceVariant',
             'mOutline', 'mShadow', 'mHover', 'mOnHover'}
    assert set(palette) == roles | {'terminal'}, 'Incomplete Noctalia 5.2 palette causes silent fallback'
    assert all(re.fullmatch(r'#[0-9a-fA-F]{6}', palette[key]) for key in roles)
    focus = re.search(r'active-color "(#[0-9a-fA-F]+)"', (desktop / 'theme.kdl.j2').read_text())[1]
    assert focus.lower() == palette['mPrimary'].lower(), 'Compositor and shell accents differ'
    for name in ('foreground', 'background'):
        assert re.fullmatch(r'#[0-9a-fA-F]{6}', palette['terminal'][name])
    for kind in ('normal', 'bright'):
        assert set(palette['terminal'][kind]) == {
            'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'}
        assert all(re.fullmatch(r'#[0-9a-fA-F]{6}', value)
                   for value in palette['terminal'][kind].values())
    wezterm_source = ROOT / 'assets/wezterm/source'
    provenance = load('assets/wezterm/provenance.json')
    for name, digest in provenance['sha256'].items():
        if name != 'wezterm.lua':
            assert hashlib.sha256((wezterm_source / name).read_bytes()).hexdigest() == digest
    canonical = ROOT / 'roles/qubix_niri/files/wezterm/wezterm.lua'
    assert list((ROOT / 'assets').rglob('wezterm.lua')) + list((ROOT / 'roles').rglob('wezterm.lua')) == [canonical]
    for name in ('KAMSuperuser.toml', 'oxocarbon-dark.toml'):
        original = (wezterm_source / 'colors' / name).read_text()
        shipped = (ROOT / 'roles/qubix_niri/files/wezterm/colors' / name).read_text()
        assert tomllib.loads(original) == tomllib.loads(shipped)
    wezterm = (ROOT / 'roles/qubix_niri/files/wezterm/wezterm.lua').read_text()
    assert 'config.color_scheme = "Oxocarbon Dark"' in wezterm
    assert 'config.window_background_opacity = 0.75' in wezterm
    assert 'config.send_composed_key_when_left_alt_is_pressed = true' not in wezterm
    assert 'apple%-darwin' in wezterm
    assert 'wezterm.home_dir .. "/.config/wezterm/colors"' in wezterm
    print(f"Repository consistency passed ({len(documents)} Markdown files, profile/default/schema agreement).")


if __name__ == "__main__":
    main()
