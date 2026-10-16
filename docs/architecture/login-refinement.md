# Compact login and enrollment

Status: **Implemented; controller, native isolated rendering, installation, zero-change reapplication
and desktop-caption activation Tested; physical fingerprint/login/boot acceptance pending**.
See [evidence and comparisons](../project/ui-test-results.md). Focused task: provide a compact fingerprint enrollment window,
reduce the greeter's visual weight and show **QubixOS** in the launcher, Control Center
and the selected Limine operating-system menu. This explicitly requested display naming
does not change `/etc/os-release`, accounts, kernel arguments or boot entry IDs.

## Responsibilities and boundaries

- An additive GTK 4/GJS application, **Fingerprint setup**, communicates directly with
  fprintd on the system bus as the current ordinary user. It offers ten named fingers,
  enrolled-state indicators, measured scan progress, actionable retry text, cancellation
  and an explicit verification test. It never deletes/replaces an enrolled finger, changes
  PAM/Polkit policy, stores biometric data itself or starts enrollment on launch.
- The enrollment controller owns one fprintd claim/operation at a time. Stop precedes
  release on completion, failure and window closure. A scan completed just before cancellation
  can remain saved; cancellation refreshes the listing and never claims to undo completion.
  Async replies cannot start a scan
  after cancellation. Permission denial, occupied/disconnected readers, duplicate prints,
  failed scans and missing readers remain visible and recoverable. Success requires the
  completed signal and a subsequent enrolled-finger listing.
- The window uses the existing dark steel-blue palette, compact typography and one primary
  action. It is available through an application entry in Super+Space. Password fallback
  and service-specific login setup remain in the [fingerprint guide](../user/fingerprint.md).
- Noctalia 5.3.0 hardcodes its distribution/version captions. A narrowly scoped, pinned
  source patch changes only launcher/Control Center presentation in a separately installed
  Qubix binary. Native package binaries and system identity stay intact. Package upgrades
  require a matching reviewed rebuild; source/native/private binary checksums are bound in
  root-owned provenance. Unsupported versions or changed native builds fail before activation.
  Startup falls back to the updated native client with a diagnostic if its binary changes.
- Greeter 1.6.0 has no independent UI-size setting. A separate pinned UI-only build reduces
  panel width, avatar, typography and spacing without changing display geometry, keyboard,
  authentication or session logic. Hide the decorative scheme selector; retain compact
  power/session controls, password entry and the existing palette/wallpaper. Keep the native
  compositor and wrapper. Installation and selecting the private client are distinct gates.
- Limine menu naming must use measured native generator controls and change labels only.
  Preserve entry IDs, ordering, payload paths/digests, defaults, snapshots and arguments.
  The user's explicit label request is the exception to the normal preserved entry-title
  policy; it is not permission to regenerate arbitrary boot content or reboot.
  The separate `menu-label.yml` task preserves the generic first baseline, changes only the
  machine-bound OS title and native `TARGET_OS_NAME`, and supports reversing the title before
  generic boot restoration. It does not broaden the normal restore guard to ignore other changes.
  Reuse the full adapter's native enrollment-policy probe; enabled/ambiguous EFI config enrollment
  must fail before even the persistent target setting is written.

## Acceptance

Controller tests cover enrollment/verification success, all retry/failure states, permission
denial, cancellation during each async stage, duplicate starts, cleanup and stale signals.
Native parser/runtime checks and sanitized reference/custom screenshots establish UI evidence;
mocked scans must be labelled as previews. Use no real enrollment in automated checks.
Source patches must apply exactly to checksum-pinned releases and touch presentation only.
Installed verification and identical reapplication must pass separately from session activation.
Native account/settings/PAM/boot preservation is audited before/after deployment. No manager
restart, reboot or physical authentication acceptance is implied by a successful preview.
