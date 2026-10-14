# SDDM login branding

Status: Implemented candidate; cloned-UI and unsupported-manager fixtures Tested; native preview/login needs VM.

`login.enabled` remains opt-in. `backend: auto` accepts only measured already-active SDDM; `theme_source: breeze` requires an installed non-symlinked Breeze tree with supported background/type options. The source authentication QML and resources are cloned unchanged into `/usr/share/sddm/themes/qubix/`. Qubix changes only the supported background override and Current theme selection. Existing source theme, PAM, manager and session startup remain preserved.

A backed-up drop-in activates the clone; if `/etc/sddm.conf` already sets Current with higher precedence, only that one setting is minimally replaced with backup. Ambiguous Current declarations or incompatible source themes fail. No service restart is performed. On the VM, preview `sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/qubix` where available, then verify actual login into both native and Qubix sessions. File-copy success does not establish a working login. Restore uses the shared first-baseline engine.
