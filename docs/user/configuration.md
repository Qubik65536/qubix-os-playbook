# User configuration

Status: **Implemented and fixture-tested**. The [configuration contract](../architecture/configuration.md) is authoritative for keys and defaults.

Write optional overrides to ignored `config/local.yml`:

```yaml
qubix:
  profile: cachyos-niri
  branding:
    enabled: false
```

Run `./bootstrap.sh verify -e @config/local.yml` (add `-i inventory.ini` for remote targets). Defaults, allowlisted profile, then overrides are recursively merged. Unknown keys, malformed types, unsupported profiles and enabled Planned components fail before host configuration writes. Omitted siblings retain defaults; YAML booleans must be unquoted.

Branding is enabled by the profile. The override above disables it for inspection/preflight-only use. All other components are disabled and Planned. Personal configuration is preserved. There is no adoption mechanism or automatic default-shell change. Backend names express intent; they do not establish active boot-chain evidence. Never commit credentials.
