# Midnight boot artwork

Qubix supplies the restrained geometric cube wallpaper in [wallpaper.svg](wallpaper.svg).
Its outlined lettering uses the attributed [Krypton-derived subset](../fonts/README.md).
The committed PNG is exported with Inkscape; deployment does not need an SVG renderer or fonts.
The blue gradient, fine geometry and lower-right identifier leave the menu area quiet.

With the optional tools from requirements-assets.txt and Inkscape available, regenerate boot artwork,
the Plymouth watermark and vector spinner frames from the repository root:

```bash
.cache/asset-venv/bin/python scripts/generate-boot-art.py
```

On macOS, permit Inkscape's desktop renderer if the process sandbox prevents startup; use
`INKSCAPE_PROFILE_DIR="$PWD/.cache/inkscape"` to keep its profile local. Refresh the boot and Plymouth
manifests after intentional changes, inspect the PNGs and run the native preview before activation.
The original desktop wallpaper stays separate. See the [design contract](../../docs/architecture/boot-design.md).
