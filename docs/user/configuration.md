# User configuration

Status: **Planned procedure**. The [configuration contract](../architecture/configuration.md) is authoritative for keys and defaults.

Operator overrides use a YAML mapping named `qubix` and recursive merging with the selected profile. Prefer a small overrides file so new safe defaults are inherited. Unknown keys and malformed types will fail before writes. Never put credentials in committed configuration.

Personal configuration is preserved. Bootstrap supports no user-file adoption or default-shell change. Enabling planned components will report an error rather than silently succeed. Backend names express intent but do not establish active boot-chain evidence.
