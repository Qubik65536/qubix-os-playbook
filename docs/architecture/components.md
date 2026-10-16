# Component boundaries

Status: **Candidate components Implemented; packages/system automation Planned; native acceptance pending**. See [status](../project/status.md) for evidence.

| Component | Responsibility | Ownership | Required dependencies |
|---|---|---|---|
| Discovery | Read identity, binaries, package and service evidence | Preserved | Host Python |
| Branding | Qubix-named assets under `/usr/share/qubix/` | Managed | Supported platform |
| Niri | Separate explicit system session defaults; future personal adoption | Default; existing files Preserved | Installed Niri; syntax validation |
| Appearance | Wallpaper and companion settings | Default | Branding; measured companions |
| Shell/terminal | Additive defaults and optional personal adoption | Default; personal files Preserved | Detected applications |
| Login | Supported active-manager appearance or inactive Noctalia preparation | Default; authentication Preserved | Measured SDDM/Breeze or Noctalia Greeter/greetd prerequisites |
| Bootloader | Minimal appearance configuration | Managed theme; boot entries Preserved | Selected proven GRUB/Limine adapter |
| Plymouth | Splash installation and selection | Managed theme; unrelated settings Preserved | Installed Plymouth; initramfs adapter |
| Packages/system (Planned) | Narrow explicitly required dependencies/defaults | Managed named resources | CachyOS adapter |
| State/recovery | Revision manifest, backups, verified restoration | Managed manifest | Resource ownership records |

```mermaid
flowchart LR
    Discovery --> Validation
    Validation --> Branding
    Branding --> Niri
    Branding --> Appearance
    Niri --> Appearance
    Validation --> Shell
    Validation --> Login
    Branding --> Login
    Branding --> Bootloader
    Branding --> Plymouth
    Plymouth --> Initramfs
    Branding --> State
    Niri --> State
    Bootloader --> State
    Initramfs --> State
```

Bootloader and Plymouth are independent selections. Neither gates the first desktop milestone. Components report installation, syntax validation, session validation, and boot validation separately. A disabled component performs no writes. Unsupported enabled components fail before any component writes.

Detailed contracts: [branding](../components/branding.md), [Niri](../components/niri.md), [bootloader](../components/bootloader.md), [Plymouth](../components/plymouth.md), [shell](../components/shell.md), [login](../components/login.md), and [remaining components](../components/remaining.md).

Optional fingerprint enrollment and private UI clients belong to the existing Niri/login components;
[their contract](login-refinement.md) defines exact dependencies and ownership. Separate explicit
preparation playbooks install native prerequisites; general package/system automation remains Planned.
Display-only Limine naming preserves boot payloads and uses the existing baseline engine plus the
native enrollment-policy guard. It does not enable boot/image components during a UI deployment.
