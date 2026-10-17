# Monaspace NF fonts

Status: **Implemented; fixtures/native rendering Tested; installation acceptance In Progress**. This contract defines installation separately from UI selection.

## Scope and interface

`qubix.fonts.enabled` installs GitHub Next's unmodified Monaspace NF v1.400 desktop
OpenType families (Argon, Krypton, Neon, Radon and Xenon), all supplied weights,
italics and widths. `qubix.fonts.krypton_ui` selects `Monaspace Krypton NF` for
Fontconfig's `sans-serif`, `sans`, `system-ui` and `monospace` defaults, Qubix
Noctalia shell text. Generic greeter text follows the Fontconfig defaults; explicit
operator-selected greeter fonts retain precedence. Both are enabled by the
CachyOS Niri profile. Disable `krypton_ui` to retain the fonts while restoring
generic shell text and removing the system alias preference on reapplication.
The switch requires fonts enabled; disabling the component performs no writes.

Fontconfig aliases inherit the matched family's binding strength (`binding="same"`),
so generic requests prefer Krypton without promoting weak generic fallbacks over
explicit application families. See the [Fontconfig binding contract](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html).
Fontconfig preferences preserve explicit application family requests, fallback for
missing glyphs and personal font settings. They cannot force a family in applications
with their own font selection. No dconf user values, GTK/Qt personal files, terminal dotfiles,
boot typography, initramfs or authentication settings are changed. Existing Qubix
Noctalia GUI overrides retain precedence. No greeter configuration or manager restart is required.

## Sources, ownership and activation

The separate `playbooks/prepare-fonts.yml` downloads the official release into the
controller's ignored cache and checks the pinned SHA256 before extracting it.
Deployment has no network dependency and rejects missing/changed cached source files
before target writes. `assets/fonts/monaspace-nf.yml` records archive provenance and
exact file checksums. The upstream OFL accompanies the installed fonts.

Fonts under `/usr/share/fonts/qubix-monaspace-nf/` are Managed resources. The additive
`/etc/fonts/conf.d/60-qubix-krypton.conf` is a Default, backed up with the shared
resource engine before first activation. It remains a valid empty Fontconfig
fragment with the switch off, allowing safe reapplication without deleting fonts.
The additive `/usr/share/glib-2.0/schemas/90-qubix-krypton.gschema.override` sets
GTK interface and monospace schema defaults to Krypton 11 when selected, and is
comment-only when disabled. Saved user preferences keep precedence; document fonts
are preserved. The native compiler strictly rebuilds derived `gschemas.compiled`
after changed inputs and recovery. Both compiler and interface schema must exist
before writes. Shared recovery restores originals/absence. Font caches are derived state and are
refreshed after changed font/toolkit inputs and restoration. Installed verification checks
exact resources and native font resolution. File installation, parser/font validation,
running-session activation and graphical acceptance are reported separately.
New applications read defaults; an existing shell may require reload/restart and
other applications may require reopening. No logout, reboot or session restart is
part of ordinary deployment.

## Acceptance criteria

- Strict boolean schema, recursive defaults, switch-off and disabled behavior pass;
  unsupported switch combinations and absent/damaged sources fail before writes.
- The official font files and license install with checksums and explicit modes;
  disposable-root install/reapply/restore and check-mode fixtures preserve unrelated files.
- Native Fontconfig validates the fonts and resolves Krypton NF; native Noctalia and
  GTK schema parsers accept selected defaults. No silent fallback counts as success.
- Commit sanitized reference/Krypton native comparison screenshots, identifying source,
  environment and preview versus live activation. Preserve personal settings and compositor.
- Run repository checks; document any native deployment/session gate blocked by access.
