# Native spinner assets

The theme uses the native two-step renderer and input controls with a midnight-blue gradient,
an original 32 px near-white vector spinner and a compact, outlined Krypton-derived Qubix wordmark.
The darker gradient and brighter shaded cube improve contrast; decorative captions are omitted.
Boot, reboot and shutdown share this composition. Firmware-background rendering is disabled within
the theme; firmware data, graphics hardware settings and kernel arguments are preserved.

The unmodified input PNGs and adapted definition originate from
[CachyOS/cachyos-plymouth-theme](https://github.com/CachyOS/cachyos-plymouth-theme),
revision `27c453a1d65597d9773af349836bd67665267e87`, under GPL-3.0-only.
The source credits Jimmac/Plymouth. [COPYING](theme/COPYING), [NOTICE](theme/NOTICE)
and the checksum [manifest](manifest.yml) accompany the deployed files.

The watermark recolours the Apache-2.0 [Qubix logo](../branding/README.md) while retaining face shading.
The [Krypton-derived font](../fonts/README.md) supplies outlined lettering, so this asset does not
depend on runtime font discovery. Native prompts use the attributed Qubix Boot Mono subset;
the installed font resolver must select its exact file before image generation. Early native
freetype prompts have the subset's documented Latin coverage; other scripts are not validated.
The normal root filesystem retains its native fonts; do not infer complete initramfs font fallback.

To export the wordmark, wallpaper and vector animation with Inkscape and optional asset tools:

```bash
.cache/asset-venv/bin/python scripts/generate-boot-art.py
```

Inkscape is an optional asset-development tool, not a deployment dependency. Update the manifest
after intentional asset changes, run static checks and the [native preview](../../docs/user/plymouth.md).
Do not substitute the CachyOS-branded watermark or its optional end animation.
