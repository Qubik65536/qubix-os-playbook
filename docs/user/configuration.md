# User configuration

Status: **Implemented and fixture-tested**. The [configuration contract](../architecture/configuration.md) is authoritative for keys and defaults.

Write optional overrides to ignored `config/local.yml`:

```yaml
qubix:
  profile: cachyos-niri
  branding:
    enabled: false
```

Run `./bootstrap.sh verify -e @config/local.yml` (add `-i inventory.ini` for remote targets). Defaults, allowlisted profile, then overrides are recursively merged. Unknown keys, malformed types, unsupported profiles and unsupported enabled combinations fail before host configuration writes. Omitted siblings retain defaults; YAML booleans must be unquoted.

Branding is enabled by the profile. The override above disables branding; default inspection remains read-only with desktop selections enabled. The profile also enables Niri and shell; disable those explicitly for a branding-only deployment. Login/boot/Plymouth remain disabled. Personal configuration is preserved. There is no adoption mechanism or automatic default-shell change. Backend names express intent; they do not establish active boot-chain evidence. Never commit credentials.

For optional Noctalia Greeter use the [login guide](login.md); it separates package preparation,
appearance deployment and an operator-reviewed manager transition. Fingerprint enrollment and
password fallback are described in the [fingerprint guide](fingerprint.md); PAM is preserved.
