# Share the connected Wi-Fi

On the CachyOS machine, as the normal desktop account, prepare the native application:

```bash
paru -S linux-wifi-hotspot
```

Review the AUR build as usual. This is separate package preparation, not a deployment
task. The package supplies the GUI/backend and dependencies; do not enable its
`create_ap` service. `hotspot.enabled` defaults true in the CachyOS Niri profile.
To opt out, add `hotspot: {enabled: false}` under `qubix` in your local overrides.
Then use the ordinary [local deployment procedure](deployment.md).

Open **Share Wi-Fi** in the application launcher. Select the currently connected Wi-Fi
interface as both **WiFi Interface** and **Internet Interface**, choose an SSID and a
password of at least eight characters, then start and authorize sharing. Stop it in
the same window when finished. Saved passwords belong to the native application;
do not put them in playbook YAML or command arguments.

Single-adapter sharing requires simultaneous client/AP support. Inspect `iw list`
for AP mode and valid interface combinations; use the existing connection's channel
where the radio allows only one channel. Firmware/regulatory restrictions can prevent
AP operation even when modes are listed. Try a compatible upstream band/channel or
select a second AP-capable USB Wi-Fi adapter. Do not disable regulatory safeguards.
The ThinkPad T14 Gen 1 AMD is not automatically certified by its model name.

Test from another device: connect, obtain an address, resolve DNS and browse while
the laptop remains connected upstream. Stop sharing and verify upstream still works.
See the [component contract](../components/hotspot.md) for ownership and acceptance.

The tested AX200 supports one shared channel: channel 52 was refused, while channel
161 reached AP-ENABLED. See [measured evidence](../project/hotspot-test-results.md).
