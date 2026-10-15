# Native spinner assets

The theme uses the native two-step renderer and input controls with a blue-charcoal cube background,
an original 32 px near-white vector spinner and a compact, outlined Krypton-derived Qubix wordmark.
The picture derives from the desktop wallpaper and scales using the native renderer; a gradient is
retained as fallback. The canonical cube retains its original colours; decorative captions are omitted.
Boot, reboot and shutdown share this composition. Firmware-background rendering is disabled within
the theme; firmware data, graphics hardware settings and kernel arguments are preserved.

The unmodified input PNGs and adapted definition originate from
[CachyOS/cachyos-plymouth-theme](https://github.com/CachyOS/cachyos-plymouth-theme),
revision `27c453a1d65597d9773af349836bd67665267e87`, under GPL-3.0-only.
The source credits Jimmac/Plymouth. [COPYING](theme/COPYING), [NOTICE](theme/NOTICE)
and the checksum [manifest](manifest.yml) accompany the deployed files.

The watermark embeds the Apache-2.0 [Qubix logo](../branding/README.md) without tint, colour filters or
opacity changes. Asset generation compares the logo crop pixel-for-pixel against a separate canonical
render at the same size. Text and surrounding colours may change; the logo colours must remain original.
The [Krypton-derived font](../fonts/README.md) supplies outlined lettering, so this asset does not
depend on runtime font discovery. Native prompts use the attributed Qubix Boot Mono subset;
the installed font resolver must select its exact file before image generation. Early native
freetype prompts have the subset's documented Latin coverage; other scripts are not validated.
The normal root filesystem retains its native fonts; do not infer complete initramfs font fallback.

The Apache-2.0 background embeds the canonical desktop cube wallpaper beneath a restrained blue
treatment. Native two-step scales it to each output; other aspect ratios may stretch the picture.
The deployment preflight requires background.png/ScaleBackgroundImage support in the installed plugin.

To export the wordmark, backgrounds and vector animation with Inkscape and optional asset tools:

```bash
.cache/asset-venv/bin/python scripts/generate-boot-art.py
```

Inkscape is an optional asset-development tool, not a deployment dependency. Update the manifest
after intentional asset changes, run static checks and the [native preview](../../docs/user/plymouth.md).
Do not substitute the CachyOS-branded watermark or its optional end animation.
