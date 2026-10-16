# Configuration contract

Status: **Implemented and fixture-tested schema**. `qubix` is the operator input; resolved configuration is an internal fact. Only profile `cachyos-niri` is initially allowed.

```yaml
qubix:
  profile: cachyos-niri
  branding:
    enabled: true
  niri:
    enabled: true
    user_config: preserve
    fingerprint_setup: false
    presentation: native
  shell:
    enabled: true
    change_default_shell: false
  login:
    enabled: false
    backend: auto
    theme_source: breeze
    activation: existing
    compact: false
  bootloader:
    enabled: false
    backend: auto
    config_path: ''
    confirm_active: false
    limine_version: 0
  plymouth:
    enabled: false
    initramfs_backend: auto
    confirm_active: false
    force_rebuild: false
    early_graphics: preserve
    images: []
    presets: []
```

The current profile enables branding, an additional Qubix Niri session and shell defaults. Its [desktop design](desktop-design.md) uses measured standalone Noctalia with separate Qubix defaults and GUI state; desktop shell selection is fixed for this initial profile. All candidate components have implementations; unsupported selections still fail explicitly. Bootloader and Plymouth remain opt-in until VM testing. No fallback from a mistyped profile or backend.

Booleans must be YAML booleans, not strings. Each nested mapping allows only documented keys. `user_config` initially accepts only `preserve`; an adoption interface requires its own consent and recovery design. `change_default_shell` must be false during bootstrap. Login backend allows `auto`, `sddm`, `greetd`, `gdm`, `lightdm`; bootloader allows `auto`, `grub`, `limine`; initramfs allows `auto`, `dracut`, `mkinitcpio`. Allowing a value in the schema does not implement an adapter.

## Ownership

| Policy | Meaning | Examples |
|---|---|---|
| Managed | Qubix reconciles content in a Qubix namespace | `/usr/share/qubix/branding/` |
| Default | Operator selects supplied defaults; explicit Qubix session does not inherit personal Niri settings | `/etc/niri/qubix/` defaults and terminal defaults |
| Preserved | Detect and report without modifying | Dotfiles, boot entries, kernel arguments, encryption, `/usr/lib/os-release` |

Existing non-Qubix system defaults require backup and an explicit activation policy before replacement. Additive fragments are preferred. A file's presence does not prove the application loaded it.

Login supports already-active SDDM with `theme_source: breeze`, `activation: existing` and
validated background/type options. Its native authentication QML is copied unchanged.
Noctalia Greeter uses explicit `backend: greetd`, `theme_source: noctalia` and
`activation: prepare|existing`. Preparation requires greetd inactive and stages its appearance;
existing requires only greetd active and the measured native wrapper already selected.
Both preserve PAM, services and session startup. See the authoritative
[login component contract](../components/login.md) and [operator guide](../user/login.md).

`niri.fingerprint_setup: true` installs the optional GTK 4/GJS enrollment application;
installed `gjs`, `gtk4` and `fprintd` are required before writes. `niri.presentation: qubix`
selects a prepared private Noctalia 5.3.0 UI build for display captions. `native` keeps the
distribution binary. `login.compact: true` requires Noctalia Greeter 1.6.0, a prepared private
UI build and an already-selected Noctalia launcher, then backs up/replaces only that launcher
command with a wrapper around the native compositor. All three options default off/native.
See the [presentation/enrollment contract](login-refinement.md); preparation, file installation,
session activation and actual authentication are separate gates.

Boot activation requires `backend: grub|limine`, confirmed `config_path` and `confirm_active: true`. Limine additionally requires the observed booted major `limine_version` (8–12). Auto/unknown configurations fail before writes. Native configs and boot entries remain preserved except minimal supported appearance changes.

Plymouth needs a confirmed generator, explicit images (path, kernel version and kernel_image), and mkinitcpio preset names. All selected preset outputs must be mapped. force_rebuild is an explicit repair override, normally false. Plain initramfs images are supported; UKI signing and encrypted/hardware/kernel arguments remain outside ownership.

`plymouth.early_graphics` accepts `preserve` (default) or `simpledrm`. The latter explicitly selects
the existing firmware framebuffer through native Plymouth configuration on a supported daemon;
it does not alter kernel arguments or GPU modules. See the [early graphics contract](../components/plymouth.md#early-graphics-repair).

Active-image binding: each image may additionally declare both limine_image and limine_kernel_image for the existing native cache pair. These require the confirmed Limine config/backend and exact file/reference/kernel validation. Verified generated images are staged at content-addressed Qubix paths before updating only the bound module aliases/checksums; native cache/snapshot images remain preserved. See the [component contract](../components/plymouth.md#active-limine-image-repair). Without a valid active-image binding, cached Limine startup branding must fail explicitly.
