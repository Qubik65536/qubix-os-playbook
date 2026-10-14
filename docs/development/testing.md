# Testing strategy

Status: **Planned tooling**. Bootstrap CI and equivalent local commands will run YAML lint, Ansible syntax/lint, ShellCheck, basic Markdown/link checks, and configuration consistency checks. No privileged deployment belongs in CI.

Meaningful fixture tests must exercise discovery classification, profile merging, invalid profile/options/types, unsupported platforms, missing Niri/Pacman, and planned enabled components. Tests may inject evidence into classification task files, but production discovery must read the host. Fictional fixture facts cannot establish real host compatibility.

Additive branding tests use a temporary filesystem, exact source/installed checksums, repeated application with zero changes, check-mode no-write evidence, and damaged/missing asset rejection. No fixtures point to `/boot`, a real `/etc`, or personal dotfiles.

Future integration matrix: CachyOS Niri session; login; GRUB; Limine; Plymouth+dracut; Plymouth+mkinitcpio; idempotency; preserved configuration; revision tracking; restoration and interrupted deployment. Each boot combination requires a disposable VM reboot and recovery test.

Record exact commands and outcomes in [status](../project/status.md). Broaden tests when failures or changed assumptions justify it. File installation, parsing, graphical verification, and boot acceptance are separate results.
