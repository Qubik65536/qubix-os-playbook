"""Repository-only documentation and definition consistency checks; not a runtime app."""
from pathlib import Path
import hashlib
import re
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
    print(f"Repository consistency passed ({len(documents)} Markdown files, profile/default/schema agreement).")


if __name__ == "__main__":
    main()
