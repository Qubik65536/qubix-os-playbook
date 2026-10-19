# User configuration

Status: **Implemented and fixture-tested**. The [configuration contract](../architecture/configuration.md) is authoritative for keys and defaults.

Write optional overrides to ignored `config/local.yml`:

```yaml
qubix:
  profile: cachyos-niri
  branding:
    enabled: false
```

Run `./bootstrap.sh verify -i inventory/local.ini -e @config/local.yml` on this machine. Defaults, allowlisted profile, then overrides are recursively merged. Unknown keys, malformed types, unsupported profiles and unsupported enabled combinations fail before host configuration writes. Omitted siblings retain defaults; YAML booleans must be unquoted.

Branding is enabled by the profile. The override above disables branding; default inspection remains read-only with desktop selections enabled. The profile enables fonts, Niri, shell, fingerprint setup, private captions, compact Noctalia/greetd login, KWallet, bootloader appearance and Plymouth. Omitted options stay enabled: a branding-only deployment must explicitly disable the other components, both font options, fingerprint setup and compact login, and choose native presentation. See the [complete defaults](../architecture/configuration.md#every-effective-default) and [deployment preparation](deployment.md). Personal configuration is preserved apart from the documented three-file WezTerm account exception. There is no adoption mechanism or automatic default-shell change. Backend names express intent; they do not establish active boot-chain evidence. Never commit credentials.

For the default Noctalia Greeter use the [login guide](login.md); it separates package preparation,
appearance deployment and an operator-reviewed manager transition. Fingerprint enrollment and
password fallback are described in the [fingerprint guide](fingerprint.md); fingerprint setup preserves PAM. The separate KWallet component owns only its measured keyring hooks.

The profile installs official GitHub Monaspace NF and selects Krypton UI defaults.
To install all five families while keeping generic UI defaults:

```yaml
qubix:
  fonts:
    enabled: true
    krypton_ui: false
```

Set both values false to omit fonts on a new installation. Disabling a component
leaves already-installed resources untouched; to switch back after deployment,
keep `enabled: true`, set `krypton_ui: false` and deploy again. Personal/application
font overrides retain precedence. See [fonts](../components/fonts.md) for scope and recovery.
