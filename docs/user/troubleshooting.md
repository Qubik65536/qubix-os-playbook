# Troubleshooting

Status: **Implemented inspection diagnostics**; use [project status](../project/status.md) for actual support.

| Symptom | Interpretation and next step |
|---|---|
| Local RPC server fails in a restricted sandbox | Allow the non-destructive fixture/inspection process to use local IPC; do not change target compatibility checks |
| Unsupported host | Confirm exact CachyOS identity, Linux/systemd, executable Pacman and Niri; Fedora/KDE are not yet supported |
| Planned component enabled | Disable it and consult the backlog; do not treat schema support as implementation |
| Unknown or invalid option | Compare overrides to the configuration contract; use YAML booleans |
| Bootloader ambiguity | Stop boot customization; provide active-chain evidence when an adapter exists |
| Files installed but appearance unchanged | Check personal override precedence and actual application/session loading |
| Probe permission failure | Supply readable evidence/target permissions; do not interpret failure as absence |

Include source Git revision, command, effective options, target version, and redacted error output in an Issue. Do not include credentials. Never repair an appearance problem by overwriting boot entries, personal files, or distribution identity.
