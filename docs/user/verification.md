# Verification

Status: **Implemented inspection, fixture-tested**. Run `./bootstrap.sh verify` after [setup](installation.md); add inventory/overrides as described in [deployment](deployment.md).

The report includes resolved configuration, native CachyOS/version evidence, executable capabilities, relevant package versions, Niri version, desktop/session environment hints, configured display-manager link and systemd activity, existing candidate paths, and installed loader/initramfs tools. Detection never changes host configuration. Unknown/ambiguous active loader and image generator are reported as `unresolved`, even when one tool is installed.

Permission/probe failures stop execution rather than being treated as missing capabilities. Session hints may be unknown under SSH. The initial supported path still needs live CachyOS VM evidence; fixtures exercise production classification/normalization/identity tasks.

Asset installation, Niri parser validation, graphical session, bootloader boot, and Plymouth boot are separate future verification levels. None is established by successful inspection. There is no managed-resource verification at this revision.
