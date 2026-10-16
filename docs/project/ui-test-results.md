# Compact UI and fingerprint setup evidence

Status: **Implemented; controller, source build, native simulated adapter and UI rendering Tested;
installation/activation In Progress**. Contract: [compact login and enrollment](../architecture/login-refinement.md).

## Source and environment

Qubix candidate based on `3ca8049`; this change contains the exact application, configuration,
source patches and comparison images. Native CachyOS Niri target, Noctalia package 5.3.0-1.1,
Greeter 1.6.0-1, fprintd 1.94.5, GJS/GTK 4. Native source variants use released Noctalia
`v5.3.0` and Greeter `v1.6.0`; exact archive and patch SHA256 are in the
[source manifest](../../assets/ui/manifest.yml). Source builds run as the ordinary user with two
compiler jobs, no upstream install hooks, and retain native package executables/assets.
The initial preparation passes 76 tasks/23 changes, including the missing GJS/build package
transaction. Native package hooks add Snapper entries; these are package effects, not Qubix
menu-label changes. A subsequent prepared-cache/provenance reapplication passes 72 tasks/zero
changes. Final provenance additionally checks the compiled binary checksum and real cache ancestry.

## Controller and native checks

- 32 JavaScript tests cover finger selection, progress bounds, confirmed saved enrollment,
  verification/retries/failures, concurrent starts, permission errors, cancellation during
  Claim/List/Start and completion, stale signals, Stop/Release errors and close cleanup.
- Profile/discovery fixture: 727 tasks, zero changes, 40 profile/11 host/seven identity cases.
  Desktop regression: 69 tasks, zero changes, seven expected refusals. Greeter regression:
  512 tasks/39 temporary changes, sixteen expected refusals. Check-mode results are separate.
  Global greeter check mode passes 381 tasks/25 temporary changes with the same sixteen refusals.
- Compact/provenance fixture: 77 tasks/seven temporary changes in normal and global check mode,
  with three expected refusals for changed source/native/private client provenance. It proves an
  exact command-only greetd edit and retains terminal, account and initial-session bytes.
- The native GJS test exports fake fprintd on a private, non-activating session bus; both test
  bus addresses must match before calls. It exercises real Gio variant/property unpacking,
  Claim/Start/Stop/Release, enrollment/verification signals, cancellation and service disappearance.
  No physical reader operation occurs. An early fixture correctly refuses mismatched bus addresses;
  argument expansion is disabled and no service directories are exposed in the corrected fixture.
- Final native rendering workflow passes 137 tasks/seven temporary changes, compares eight captures,
  preserves the main Niri process and four personal settings hashes, and leaves zero live preview
  processes. The private bus has no service activation directories; system bus/authentication are
  disconnected. No real enrollment, PAM, manager restart, display change or boot check runs.
- Shell fixture tests application/GSettings preservation and selects the updated native binary when
  its bound checksum changes. Native package upgrades of the same version cannot silently retain
  a private older client; both startup fallback and deployment provenance checks apply.

## Native comparisons

All captures are unedited 1272×868 screenshots from the same isolated nested Niri at 100% scale.
Names/hostname are synthetic; no personal application content or enrolled prints are shown.
Niri's blue window outline and the gray background in the GTK captures belong to the minimal
test compositor, not application styling. CPU/RAM/time are live measurements; missing system
services in this isolated environment explain unavailable widgets. These are previews, not live
login, fingerprint authentication or boot acceptance.

| Surface | Reference | Qubix refinement and intentional difference |
|---|---|---|
| Fingerprint setup | [Native GTK stylesheet](../assets/ui/fingerprint-gtk-reference.png) on the new application's identical layout | [Qubix stylesheet](../assets/ui/fingerprint-qubix.png): steel-blue controls, smaller header/typography and a progress card; explicitly simulated three of eight scans. No existing Noctalia enrollment GUI is implied. |
| Greeter | [Previous Qubix appearance on native Greeter 1.6.0](../assets/ui/greeter-before.png) | [Compact client](../assets/ui/greeter-compact.png): 340 px card at this viewport, 36 px avatar, 13/11 px body/captions, 30/34 px controls, tighter spacing and hidden scheme picker. Same palette/wallpaper/session choice. The unavailable-login warning is intentional because no greetd socket is connected. |
| Super+Space | [Native Noctalia 5.3.0 caption](../assets/ui/launcher-native.png) | [Private Qubix caption](../assets/ui/launcher-qubix.png): **QubixOS**; native app results and synthetic user stay intact. |
| Control Center Home | [Native version line](../assets/ui/control-center-native.png) | [Private Qubix version line](../assets/ui/control-center-qubix.png): **QubixOS (Noctalia v5.3.0)**. The packaged native build's revision suffix differs from the released-source build; no system identity is rewritten. |

Limine's OS-title change is a bounded text edit, separately from its existing graphical theme.
The fixture passes 207 normal/85 global check-mode tasks, with 22/ten temporary changes and four
expected refusals in each. It compares every byte outside that title, exercises persistent `TARGET_OS_NAME`,
reapplication and exact original restoration. Console appearance of the renamed menu remains
pending the operator's next boot; no synthetic screenshot is presented as a live boot capture.

## Deployment gate

Before installation, a read-only audit records 85 protected resources, 193 recovery files, no
pending markers and boot ID `284c4a52-4486-4f7a-825d-b815465b4473`. The target now runs greetd and
Niri after the operator's intervening reboot; this is separate from activating the new compact client.
Install only the reviewed desktop/login resources, verify exact installed bytes and zero-change
reapplication, then activate the desktop captions through a guarded Noctalia-only restart. Select
the compact greeter for a future greetd start; never restart it underneath this desktop.
Apply/verify the requested Limine label separately, preserving kernel paths, pins, arguments,
snapshots, default and order. Physical enrollment, login/password fallback and renamed-menu console
acceptance remain operator gates.

The no-write production deployment preview passes 612 tasks with fourteen proposed files and zero
failures. No source/staged initramfs or bootloader resource is selected in this desktop/login run.
