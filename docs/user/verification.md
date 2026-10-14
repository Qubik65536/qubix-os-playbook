# Verification

Status: **Implemented inspection and branding-file verification, fixture-tested**. Run `./bootstrap.sh verify` after [setup](installation.md); add inventory/overrides as described in [deployment](deployment.md).

The report includes resolved configuration, native CachyOS/version evidence, executable capabilities, relevant package versions, Niri version, desktop/session environment hints, configured display-manager link and systemd activity, existing candidate paths, and installed loader/initramfs tools. Detection never changes host configuration. Unknown/ambiguous active loader and image generator are reported as `unresolved`, even when one tool is installed.

Permission/probe failures stop execution rather than being treated as missing capabilities. Session hints may be unknown under SSH. The initial supported path still needs live CachyOS VM evidence; fixtures exercise production classification/normalization/identity tasks.

Run `./bootstrap.sh verify --tags branding` to check already-installed branding (with inventory/overrides as needed). All five named files must be regular files with expected SHA-256, mode 0644, and ownership; missing/damaged/redirected content fails. Leave branding enabled in the resolved configuration for this check. `verify` without this tag stays useful before installation.

Asset availability is established only by explicit branding checks or successful post-install checks. Niri parser validation, graphical session, bootloader boot and Plymouth boot remain future verification levels. None is established by successful inspection or artwork installation.
