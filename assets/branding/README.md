# Branding provenance

The three artwork files are unmodified copies from [Qubix OS BlueBuild revision `56c57ac`](https://github.com/Qubik65536/qubix-os-bluebuild/tree/56c57acafb9c3305b201a83255c0007cf4b398bd). The reference repository publishes them under Apache-2.0. [LICENSE](../../LICENSE) and [NOTICE](../../NOTICE) accompany deployment. [Manifest](manifest.yml) is authoritative for original paths and full SHA-256 values; static checks detect changed bytes without a manifest update.

| Local file | Original path under `files/system/usr/share/pixmaps/` | SHA-256 prefix |
|---|---|---|
| `logo.svg` | `qubixos-logo.svg` | `3ccc88c39203` |
| `logo.png` | `qubixos-logo.png` | `f7448d0339ba` |
| `banner.svg` | `qubixos-banner.svg` | `46d7526f6658` |

No image-build recipes, upstream logo overrides, fonts, KDE assets, GRUB activation script, or Plymouth spinner overrides were imported. Installed artwork is inert until a later component points an application to it. See the [branding contract](../../docs/components/branding.md).
