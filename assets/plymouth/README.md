# Native spinner assets

The theme adapts the native CachyOS two-step layout, retaining its black/firmware background,
32 px white spinner and standard input controls. Qubix supplies a modest bottom watermark.
Plymouth renders the firmware image when available; the private X11 preview uses a black fallback.

The unmodified spinner/input PNGs and adapted definition originate from
[CachyOS/cachyos-plymouth-theme](https://github.com/CachyOS/cachyos-plymouth-theme),
revision `27c453a1d65597d9773af349836bd67665267e87`, under GPL-3.0-only.
The source credits Jimmac/Plymouth. [COPYING](theme/COPYING), [NOTICE](theme/NOTICE)
and the checksum [manifest](manifest.yml) accompany the deployed files.

The watermark combines the Apache-2.0 [Qubix logo](../branding/README.md) with a wordmark
in [watermark.svg](watermark.svg). To export it with Inkscape from the repository root:

```bash
inkscape --export-type=png --export-area-page --export-filename=assets/plymouth/theme/watermark.png assets/plymouth/watermark.svg
```

Inkscape is an optional asset-development tool, not a deployment dependency. Update the manifest
after intentional asset changes, run static checks and the [native preview](../../docs/user/plymouth.md).
Do not substitute the CachyOS-branded watermark or its optional end animation.
