# Configuration contract

Status: **Planned**. `qubix` is the operator input; resolved configuration is an internal fact. Only profile `cachyos-niri` is initially allowed.

```yaml
qubix:
  profile: cachyos-niri
  branding:
    enabled: true
  niri:
    enabled: false
    user_config: preserve
  shell:
    enabled: false
    change_default_shell: false
  login:
    enabled: false
    backend: auto
  bootloader:
    enabled: false
    backend: auto
  plymouth:
    enabled: false
    initramfs_backend: auto
```

The eventual desktop profile enables validated desktop components. During bootstrap planned components stay disabled and enabling them must fail clearly. Bootloader and Plymouth remain opt-in until VM testing. No fallback from a mistyped profile or backend.

Booleans must be YAML booleans, not strings. Each nested mapping allows only documented keys. `user_config` initially accepts only `preserve`; an adoption interface requires its own consent and recovery design. `change_default_shell` must be false during bootstrap. Login backend allows `auto`, `sddm`, `greetd`, `gdm`, `lightdm`; bootloader allows `auto`, `grub`, `limine`; initramfs allows `auto`, `dracut`, `mkinitcpio`. Allowing a value in the schema does not implement an adapter.

## Ownership

| Policy | Meaning | Examples |
|---|---|---|
| Managed | Qubix reconciles content in a Qubix namespace | `/usr/share/qubix/branding/` |
| Default | Operator accepts a supplied default; personal override wins | Future `/etc/niri/` defaults and terminal defaults |
| Preserved | Detect and report without modifying | Dotfiles, boot entries, kernel arguments, encryption, `/usr/lib/os-release` |

Existing non-Qubix system defaults require backup and an explicit activation policy before replacement. Additive fragments are preferred. A file's presence does not prove the application loaded it.
