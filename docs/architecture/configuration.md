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
  shell:
    enabled: true
    change_default_shell: false
  login:
    enabled: false
    backend: auto
    theme_source: breeze
  bootloader:
    enabled: false
    backend: auto
    config_path: ''
    confirm_active: false
    limine_version: 0
  plymouth:
    enabled: false
    initramfs_backend: auto
```

The eventual desktop profile enables validated desktop components. The current profile enables branding, an additional Qubix Niri session and shell defaults. During bootstrap planned components stay disabled and enabling them must fail clearly. Bootloader and Plymouth remain opt-in until VM testing. No fallback from a mistyped profile or backend.

Booleans must be YAML booleans, not strings. Each nested mapping allows only documented keys. `user_config` initially accepts only `preserve`; an adoption interface requires its own consent and recovery design. `change_default_shell` must be false during bootstrap. Login backend allows `auto`, `sddm`, `greetd`, `gdm`, `lightdm`; bootloader allows `auto`, `grub`, `limine`; initramfs allows `auto`, `dracut`, `mkinitcpio`. Allowing a value in the schema does not implement an adapter.

## Ownership

| Policy | Meaning | Examples |
|---|---|---|
| Managed | Qubix reconciles content in a Qubix namespace | `/usr/share/qubix/branding/` |
| Default | Operator accepts a supplied default; personal override wins | Future `/etc/niri/` defaults and terminal defaults |
| Preserved | Detect and report without modifying | Dotfiles, boot entries, kernel arguments, encryption, `/usr/lib/os-release` |

Existing non-Qubix system defaults require backup and an explicit activation policy before replacement. Additive fragments are preferred. A file's presence does not prove the application loaded it.

Login currently supports already-active SDDM with `theme_source: breeze` and validated background/type options. Other managers and incompatible source themes are rejected before configuration writes. Native authentication QML is copied unchanged; no PAM or service replacement/restart occurs.

Boot activation requires `backend: grub|limine`, confirmed `config_path` and `confirm_active: true`. Limine additionally requires the observed booted major `limine_version` (8–12). Auto/unknown configurations fail before writes. Native configs and boot entries remain preserved except minimal supported appearance changes.
