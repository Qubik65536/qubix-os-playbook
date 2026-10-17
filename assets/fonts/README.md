# Qubix boot typography

The committed TTF subset and 8x20 CP437 bitmap derive from **Monaspace Krypton Frozen Regular**,
[GitHub Next Monaspace v1.400](https://github.com/githubnext/monaspace/tree/v1.400), revision
`f31794b6e9e65698a062262e2f826f679dcb7070`. Copyright GitHub, 2023; licensed under the
[SIL Open Font License 1.1](OFL.txt). Modified primary names are **Qubix Boot Mono**, respecting
the upstream reserved font names. No endorsement by GitHub or the type designers is implied.

[manifest.json](manifest.json) records the exact source checksum, all 512 subset codepoints,
derivative sizes/hashes and ten original geometric CP437 symbols that upstream Krypton lacks.
The bitmap contains all 256 IBM CP437 cells, including control graphics and connected box borders;
it is 5120 bytes, not a PSF/TTF file. The TTF covers extended Latin, combining marks, punctuation and
available CP437 characters. Native fallback remains necessary for other scripts; this is not a
complete Monaspace installation. [The contact sheet](cp437-contact-sheet.png) shows the bitmap.
The TTF also embeds the full copyright/OFL text in its name table, so generators that copy only
the selected font into an initramfs retain the notice and license with that copy.

To regenerate from the repository root with optional developer tools:

```bash
uv venv .cache/asset-venv
uv pip install --python .cache/asset-venv/bin/python -r requirements-assets.txt
curl -fL 'https://raw.githubusercontent.com/githubnext/monaspace/f31794b6e9e65698a062262e2f826f679dcb7070/fonts/Frozen%20Fonts/Monaspace%20Krypton/MonaspaceKryptonFrozen-Regular.ttf' -o .cache/reference/MonaspaceKryptonFrozen-Regular.ttf
.cache/asset-venv/bin/python scripts/generate-boot-fonts.py .cache/reference/MonaspaceKryptonFrozen-Regular.ttf
```

Create `.cache/reference/` first if absent. The generator rejects an unexpected source checksum,
renames primary font records, preserves OFL metadata and emits deterministic binaries. Inspect the
contact sheet and review changed hashes before committing. Normal deployment needs none of these
tools or a network download. Integration into the boot roles follows the
[documented design](../../docs/architecture/boot-design.md).

## Complete desktop Monaspace NF

[monaspace-nf.yml](monaspace-nf.yml) pins the official v1.400 NerdFonts archive and
all 210 unmodified OpenType faces across five families, weights, italics and widths.
[Monaspace-NF-LICENSE.txt](Monaspace-NF-LICENSE.txt) is the upstream OFL from the same
revision. These full fonts are separate from the renamed boot subset above.
Run `.venv/bin/ansible-playbook playbooks/prepare-fonts.yml` to populate the ignored
controller cache. The [font component](../../docs/components/fonts.md) defines exact
installation, configurable Krypton selection and recovery; normal deployment is offline.
