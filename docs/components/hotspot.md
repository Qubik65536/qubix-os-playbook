# Wi-Fi connection sharing

Status: Implemented; native hardware/session acceptance pending.

The `hotspot` component adds a **Share Wi-Fi** application launcher for the native
Linux WiFi Hotspot GUI (`wihotspot`, backed by `create_ap`). It supports sharing a
connected Wi-Fi interface using a virtual AP when the kernel driver and radio permit
simultaneous managed/AP operation. CPU and laptop model do not prove support.
The upstream application owns runtime adapter/channel validation and error reporting.
A second AP-capable adapter can be selected when one radio cannot do both jobs.

Ownership: one Managed desktop entry, `/usr/share/applications/qubix-hotspot.desktop`,
installed/restored through the ordinary protected file lifecycle. Package files,
NetworkManager profiles, personal settings and saved credentials remain Preserved.
Enabling installs only the launcher, never starts a hotspot, enables a service,
changes regulatory settings, disconnects Wi-Fi or edits network/firewall configuration.
The GUI asks for authorization when starting; its backend owns temporary AP, DHCP,
NAT and cleanup while sharing. Normal default-route/VPN behavior applies; this is
not a promise of VPN isolation. Stop sharing in the same GUI before restoration.
Disabling stops reconciling files; use normal restoration to remove the owned entry.

Prerequisites: separately install `linux-wifi-hotspot` and its dependencies on the
CachyOS target. Enabled deployment validates executable `wihotspot`, `create_ap`,
`iw`, `hostapd`, `dnsmasq` and `iptables` before any resource writes. Deployment does
not start daemons or run network commands. Hardware without AP support can still
install the option; starting it reports the native unsupported-adapter error.

Acceptance: strict boolean enablement/default/opt-out; missing prerequisites fail
before writes; launcher uses the native GUI without arguments or credentials;
protected installation, verification, reapplication and restoration remain available.
Native acceptance separately requires opening the GUI, selecting the connected Wi-Fi
interface for both WiFi and Internet, a password of at least eight characters,
starting on a legal compatible channel, joining from a second device, checking DHCP,
DNS and Internet access while upstream stays connected, then stopping and confirming
upstream still works. Single-radio combinations/channel restrictions and firmware
failures are runtime constraints, not established by file installation.

References: [upstream application](https://github.com/lakinduakash/linux-wifi-hotspot),
[Linux virtual interfaces](https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw/vif.html).
See [user instructions](../user/hotspot.md).
