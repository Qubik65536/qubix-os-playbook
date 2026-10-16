# Compact UI and fingerprint setup evidence

Status: **Implemented; controller, source build, native simulated adapter/UI, installation,
zero-change reapplication and desktop-caption activation Tested; physical authentication/boot pending**.
Contract: [compact login and enrollment](../architecture/login-refinement.md).

## Source and environment

Qubix UI revision `fc721e1`, based on `3ca8049`; this change contains the exact application, configuration,
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
The initial fixture passes 207 normal/85 global check-mode tasks. The shared native-enrollment
guard in `14a0339` passes 236/108 tasks, with 23/eleven temporary changes and five expected refusals
in each. The unchanged full graphical adapter passes 726 tasks/45 temporary changes and eight
refusals after extracting that shared guard. The menu fixture compares every byte outside the title,
exercises persistent `TARGET_OS_NAME`,
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

## Installed and live results

Clean `fc721e1` installation passes 779 tasks/44 changes, including fourteen resource changes and
their backup/receipt/state work. Installed verification passes 131 tasks/zero changes. Identical-source
reapplication from a clean detached `fc721e1` checkout passes 764 tasks/zero changes, including the
deployment manifest; no image/font-cache rebuild is selected. The protected manifest remains
`files-verified`, clean revision `fc721e1`, with aggregate session/boot flags false.

A guarded Noctalia-only restart passes seven tasks, preserving Niri PID 1136, all application-window
IDs/PIDs, the original GSettings caller backend and four personal setting hashes. The running shell
changes from native PID 1200 to private-client PID 47126; `/proc/47126/exe` resolves to the installed
Qubix client, its bar is visible and the session remains unlocked. No greetd/SDDM/Niri restart runs.
Native private rendering establishes the displayed captions separately from these live process checks.

The bounded menu task from `14a0339` passes 91 tasks/six changes, installing only the title and native
target setting plus protected recovery records. Exact native inspection confirms that replacing
`/+QubixOS` with `/+CachyOS` returns the pre-install config SHA256;
removing the one added `TARGET_OS_NAME` line returns the original defaults SHA256. Kernel paths,
pins, arguments, ordering, default and snapshot bytes are identical. No generator or reboot runs.
Its native reapplication passes 89 tasks/zero changes.

Installed Greeter TOML parses with sixteen exact desktop palette roles, compact decoration settings
and the original cube wallpaper. Replacing just its wrapper command returns the original greetd
configuration SHA256. Both native client checksums still match build provenance. greetd remains
active, SDDM inactive and boot ID unchanged. The compact client awaits a future greetd start; a
normal future reboot can establish its physical login and renamed-menu appearance. Real enrollment,
reader matching, lockscreen/greeter authentication and password fallback still require the operator.

The final preservation audit finds 81 of 85 protected resources unchanged. The four intentional
differences are the greeter appearance, its launcher command, Limine OS title and native target
setting; exact normalization checks above prove the two configuration edits' narrow scope.
All earlier recovery originals/metadata remain intact: 190 of 193 earlier recovery files are
unchanged and only three applied receipts refresh. There are now 221 recovery files. Boot ID,
native default shell, retired-session backup, native executables, PAM, identity and personal
settings remain preserved; pending markers are absent. The temporary exact-source checkout and
activation helpers are removed. The operator's pre-existing sudo credential file remains private
and is not removed or committed by this task.
