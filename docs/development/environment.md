# Development environment

Status: **Planned tooling**. Use a repository-local Python virtual environment for Ansible, ansible-lint, and yamllint; Ansible targets require Python. ShellCheck is an independent developer/CI dependency. No Python application is deployed onto the target.

Bootstrap will provide pinned development dependencies, local validation commands, and a minimal Bash wrapper for inventory-based verification/deployment. It will not automatically install host packages or run `sudo`. Installation instructions will be published with working tooling.

Use an existing CachyOS Niri disposable VM for live inspection and later desktop tests. The macOS bootstrap host can run controller/static/fixture tests but cannot prove Niri sessions, boot or initramfs behaviour.
