# Verification and VM acceptance

Status: Inspection and installed-resource verification Implemented; controller fixtures Tested. **Native nested rendering and desktop recovery Tested; primary-session/reboot acceptance pending.**

Default `verify` reports configuration, identity/version, binaries/packages, Niri, manager activity, kernel arguments and candidates without writes. Active loader/generator stay unresolved until operator confirmation. SSH session hints may be absent.

After deployment use `./bootstrap.sh verify -i inventory/target.local.ini -e @config/local.yml --tags installed`; add `--ask-become-pass` for login/boot/splash selections. It checks selected file hashes/modes, Niri syntax and image archive resources without regeneration. `--tags branding` checks only branding, including ownership.

## Acceptance checklist

Record exact revision, resolved options, target/package/kernel/loader/generator versions, commands/exit statuses and observations. Save pre-test native/personal file and boot-entry checksums. Use independent snapshots/installations.

| Area | Required result |
|---|---|
| Desktop | Niri/Foot/Noctalia validators pass; wallpaper, bar, launcher, notifications, terminal, navigation work |
| Authentication | Existing login, GUI privilege and encrypted-root paths work; no PAM/encryption changes |
| Preservation | Native/personal files and identity unchanged; unowned files survive |
| Idempotency | Same revision/options second deploy has zero managed changes; unchanged images skip rebuild |
| Login | Supported SDDM or greetd password authentication, Qubix session and recovery succeed; preview alone is insufficient |
| GRUB | Native custom-hook checker, branded menu, original entries/arguments and restored boot succeed |
| Limine | Confirmed supported version, branded menu, original entries/arguments and restored boot succeed |
| dracut | Real generation/archive/splash/unlock/preservation/restoration succeed |
| mkinitcpio | All mapped preset outputs, preserved hooks/settings, real generation/splash/unlock/restoration succeed |
| Recovery/state | Pending failure visible alongside last success; baseline/snapshot recovery works; revision/digest/dirty flag accurate |

On the VM, run `niri validate --config /etc/niri/qubix/config.kdl` and `foot --check-config --config /etc/qubix/foot.ini` plus `noctalia config validate /etc/qubix/noctalia/config.toml` for direct native parser evidence. Greeter/session checks require an actual display.

Reapply before restoring. Verify original behaviour after baseline recovery. Archive presence cannot prove rendering/authentication/boot. Fixtures do not satisfy these native gates. Record outcomes in [status](../project/status.md) and [compatibility](../architecture/compatibility.md).

Before installing the desktop, you can test native KDL using `.venv/bin/ansible-playbook tests/integration/niri.yml -i inventory/target.local.ini`. For a private /boot, add `-e '{"qubix_discovery_privileged": true}' --ask-become-pass`. This creates/removes private temporary config files only; companion availability and graphical appearance are separate checks.

The optional [native nested workflow](../development/testing.md#native-desktop-smoke-test) provides repeatable companion evidence without replacing the existing Niri compositor. The [native results](../project/desktop-test-results.md) record file lifecycle, preservation, screenshots and remaining gates.
