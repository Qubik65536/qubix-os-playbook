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
    assert defaults["bootloader"]["enabled"] is False, "Bootloader must remain opt-in"
    assert defaults["plymouth"]["enabled"] is False, "Plymouth must remain opt-in"
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
        'qubix.plymouth', 'watermark.png', 'COPYING', 'NOTICE', 'bullet.png', 'entry.png',
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
    for mode in ('boot-up', 'shutdown', 'reboot'):
        assert not native[mode].getboolean('UseFirmwareBackground') and not native[mode].getboolean('UseEndAnimation')
    desktop = ROOT / 'roles/qubix_niri/templates'
    shell = tomllib.loads((desktop / 'noctalia.toml.j2').read_text())
    assert not shell['theme']['templates']['enable_builtin_templates']
    assert not shell['theme']['templates']['enable_community_templates']
    assert not shell['dock']['enabled'] and not shell['dock']['reserve_space']
    launcher = shell['shell']['launcher']
    assert launcher['providers']['session']['global']
    power_entry = configparser.ConfigParser(interpolation=None)
    power_entry.read(desktop / 'power.desktop.j2')
    power = power_entry['Desktop Entry']
    assert Path('qubix-power.desktop').stem in launcher['pinned'], 'Power menu must be available without typing'
    assert power['Type'] == 'Application' and power['Terminal'] == 'false'
    assert shlex.split(power['Exec']) == [power['TryExec'], 'msg', 'panel-toggle', 'session'], 'Power entry must only open the menu'
    plugin_dir = ROOT / 'roles/qubix_niri/files/shortcuts'
    plugin = tomllib.loads((plugin_dir / 'plugin.toml').read_text())
    panel = plugin['panel'][0]
    assert (plugin_dir / panel['entry']).is_file(), 'Shortcut panel entry is missing'
    assert shell['plugins']['enabled'] == [plugin['id']]
    assert shell['plugins']['auto_update'] == 'none'
    assert all(source['kind'] == 'path' for source in shell['plugins']['source'])
    panel_id = plugin['id'] + ':' + panel['id']
    assert panel_id in (desktop / 'config.kdl.j2').read_text()
    assert panel_id in shell['widget']['shortcuts']['actions']['left']
    palette = json.loads((desktop / 'palette.json.j2').read_text())['dark']
    roles = {'mPrimary', 'mOnPrimary', 'mSecondary', 'mOnSecondary', 'mTertiary', 'mOnTertiary',
             'mError', 'mOnError', 'mSurface', 'mOnSurface', 'mSurfaceVariant', 'mOnSurfaceVariant',
             'mOutline', 'mShadow', 'mHover', 'mOnHover'}
    assert set(palette) == roles | {'terminal'}, 'Incomplete Noctalia 5.2 palette causes silent fallback'
    assert all(re.fullmatch(r'#[0-9a-fA-F]{6}', palette[key]) for key in roles)
    focus = re.search(r'active-color "(#[0-9a-fA-F]+)"', (desktop / 'theme.kdl.j2').read_text())[1]
    assert focus.lower() == palette['mPrimary'].lower(), 'Compositor and shell accents differ'
    foot = configparser.ConfigParser()
    foot.read(desktop / 'foot.ini.j2')
    for name in ('foreground', 'background'):
        assert palette['terminal'][name] == '#' + foot['colors-dark'][name]
    for index, name in enumerate(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')):
        for kind, prefix in (('normal', 'regular'), ('bright', 'bright')):
            assert palette['terminal'][kind][name] == '#' + foot['colors-dark'][prefix + str(index)]
    print(f"Repository consistency passed ({len(documents)} Markdown files, profile/default/schema agreement).")


if __name__ == "__main__":
    main()
