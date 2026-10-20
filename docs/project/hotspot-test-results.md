# Native Wi-Fi hotspot test results

Date: 2026-10-19 (America/Toronto). Source: `65f3aed` plus the GUI executable
correction in this change. Operator-selected physical ThinkPad T14 Gen 1 AMD,
CachyOS kernel `7.2.9-2-cachyos`; Intel AX200, `iwlwifi`.
Developer SSH transport; no boot/session restart or regulatory changes.

## Package and executable correction

Reviewed the AUR `linux-wifi-hotspot` 5.0.0-1 recipe/install hooks, fetched its
versioned source and verified SHA256
`1c4310e30c2a28f5c9d48d0387e4ebd5287ac528e7fdb1dd4c3811498945733d`.
Built as the ordinary user, including the package's desktop-file check, then installed
the built archive and missing `hostapd` 2.12-2.1 using task-scoped sudo.
Existing `iw` 6.17, `dnsmasq` 2.93 and `iptables` 1.8.13 satisfy the other probes.
Native package hooks create Snapper snapshots; no service was enabled or started by
package installation. `create_ap`, `hostapd` and `dnsmasq` services remain inactive;
`create_ap` remains disabled.

The AUR recipe deliberately removes `/usr/bin/wihotspot`; it installs
`/usr/bin/wihotspot-gui`. Corrected both the launcher and prerequisite to this measured
binary, with matching fixture/documentation updates. Package files stay untouched.

## Installation, parser and GUI

Focused real-role deployment of only the hotspot launcher passes 28 tasks/three
changes. Native `desktop-file-validate` passes. Installed-file checksum/mode verification
passes; identical reapplication passes 27 tasks/zero changes. The generic backup
engine records original absence and the applied receipt without replacing existing
state or configuring other components.

Protected install/restore in an isolated target temporary root passes 47 tasks/eight
disposable changes. Restoration removes the originally absent launcher; the temporary
root is removed. The live launcher and unrelated existing backups remain intact.

A bounded eight-second native GUI launch with the existing Wayland display stays
running, emits no diagnostics and exits on the timeout's TERM (124 expected).
No GUI settings were saved and no GUI start button was pressed. This verifies native
startup, not physical button interaction or a client connection.

Controller normal/check fixtures each pass 16 tasks/zero changes with two expected
prerequisite refusals. YAML/Ansible lint and repository consistency checks pass.

## Radio and runtime

`iw list` advertises one managed plus one AP interface, with one shared channel.
The initial upstream channel 52 / 5260 MHz is marked no IR. A bounded backend attempt
creates `ap0`, refuses transmission on channel 52 and cleans it up, preserving upstream.
No kernel/firmware patch, regulatory override or upstream reconnection was performed.

The upstream subsequently uses channel 161 / 5805 MHz, which permits transmission.
A bounded test on that observed channel uses a random temporary WPA2 key in a mode-0600
root-only runtime configuration, virtual interface enabled and NAT through `wlan0`.
It reaches `AP-ENABLED`; both native hostapd and dnsmasq run while the upstream stays
connected. An HTTPS request bound to `wlan0` returns HTTP 200 during AP operation.
Timeout stops the backend and its processes; `ap0` is removed. No key is recorded in
source, this evidence or command arguments; temporary credentials are removed.

Preservation compares upstream state, boot ID, Niri PIDs, saved NetworkManager profile
hashes, IPv4 firewall rules/policies and forwarding before/after. Firewall comparison
normalizes generated timestamps and packet/byte counters, which change during normal
traffic; earlier raw-hash comparisons reported false changes. Final checks require
all comparisons and backend cleanup to pass.

## Remaining acceptance

No second physical client was available: association, WPA2 authentication, DHCP lease,
client DNS and routed Internet access still require the operator's test. Open **Share
Wi-Fi**, select `wlan0` for WiFi and Internet, choose an SSID/password and start on a
permitted upstream channel; join from another device, browse, then stop sharing.
The test AP is stopped; the installed launcher/package remain available.
