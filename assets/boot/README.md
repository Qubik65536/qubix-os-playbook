# Midnight boot artwork

The boot [wallpaper.svg](wallpaper.svg) reuses the canonical detailed [desktop cube wallpaper](../wallpaper/qubix.png).
It adds no lettering or slogans; the native menu provides the Qubix OS heading.
The committed PNG is exported with Inkscape; deployment does not need an SVG renderer or fonts.
The detailed cube stays on the right; near-white menu text sits over a dark translucent surface.

With the optional tools from requirements-assets.txt and Inkscape available, regenerate boot artwork,
the Plymouth watermark and vector spinner frames from the repository root:

```bash
.cache/asset-venv/bin/python scripts/generate-boot-art.py
```

On macOS, permit Inkscape's desktop renderer if the process sandbox prevents startup; use
`INKSCAPE_PROFILE_DIR="$PWD/.cache/inkscape"` to keep its profile local. Refresh the boot and Plymouth
manifests after intentional changes, inspect the PNGs and run the native preview before activation.
The original desktop wallpaper remains unchanged. See the [design contract](../../docs/architecture/boot-design.md).
