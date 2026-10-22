# Slack Huddle session and microphone repair

Date: 2026-10-22. Environment: the operator-selected CachyOS Niri ThinkPad,
ordinary desktop account over developer SSH. No camera, screenshot, screen content
or microphone sample is retained. Contract and acceptance:
[native session lifecycle](../components/niri.md#native-session-lifecycle-and-huddles-repair).
Source base: `3f0e42ed070deb0da55bb930a9ca6246821e6557`, with the accompanying
session-entry change. Native upstream context:
[Niri screencasting requirements](https://github.com/niri-wm/niri/blob/main/docs/wiki/Screencasting.md).

## Diagnosis and implementation

The installed Qubix desktop entry directly runs `niri --session --config ...`.
Niri imports the graphical environment, but native `niri.service` and
`graphical-session.target` are inactive. GNOME portal 51.0 has
`Requisite=graphical-session.target`; its startup fails with dependency errors on
each Slack screen-share attempt. Slack 4.52.178 reports invalid capture constraints.
The packaged Niri launcher instead starts the native service, whose `BindsTo`
activates the graphical target, then shuts down that target on logout.
The corrected entry supplies `NIRI_CONFIG` to this native launcher; no native unit
or personal configuration changes.

Slack reports microphone permission granted and successful audio-device selection.
Both native PipeWire sources are present and unmuted. A bounded PulseAudio capture
probe initially opens each source but receives zero samples, reproducing a stalled
audio path independently of Slack. Restarting only `pipewire-pulse.service` restores
capture: each source returns 32,000 signed 16-bit samples during a four-second
probe. Digital microphone peak/RMS are 32,768/5,125.2; stereo microphone 54/10.5.
These are ambient signal statistics, not speech intelligibility or participant
reception acceptance. Samples are processed and discarded entirely on the target;
only counts/levels return over SSH. Input defaults, mute and volume are unchanged.
The underlying cause of the stalled compatibility service remains undetermined.

## Installation, parser and session evidence

- **Current session Tested:** a transient user service, `qubix-live-session`, runs
  `tail --pid=1145 --follow /dev/null`, with `BindsTo=graphical-session.target` and
  `Before=graphical-session.target`. This anchors the target to the existing main
  compositor without restarting it. No enablement or dependency override is saved.
  At compositor exit the watcher exits; the otherwise unneeded target can stop.
  Then GNOME portal starts successfully with its existing dependencies unchanged.
- **Portal API Tested:** GNOME ScreenCast v5 reports available source/cursor types
  7. A public `org.freedesktop.portal.ScreenCast.CreateSession` request returns
  response 0 and its session closes successfully. No sources are selected and no
  screen stream starts. This tests the frontend/backend path beyond introspection.
- **Parser Tested with limit:** the core desktop entry passes
  `desktop-file-validate` after omitting `DesktopNames` from a temporary parser
  copy. The validator rejects that pre-existing display-manager session key;
  the actual candidate retains `DesktopNames=niri` for portal selection.
- **Persistent installation Tested:** the operator installs the staged
  `~/.cache/qubix-huddle/qubix-niri.desktop` with local sudo. The installed
  `/usr/share/wayland-sessions/qubix-niri.desktop` has SHA256
  `7a76a9a9988182955715b28b8dd5e6a6d28d012db1154adaa0efe1205e52a1fc`.
  Remote verification confirms mode 0644/root:root and the numbered backup
  `qubix-niri.desktop.~1~`. Installation does not restart the desktop or prove a
  fresh login. This scoped manual install does not update deployment receipts;
  normal playbook reconciliation manages the same resource through its existing
  baseline/receipt lifecycle, preserving original recovery baselines.
- **Controller Tested:** `scripts/validate.sh` passes. The desktop fixture passes
  normal/check modes, each 86 tasks, zero changes and eight expected refusals.
  The initial sandboxed fixture fails to start Ansible RPC; authorized execution
  outside the sandbox passes. No runtime package changes occur.
- **Preservation:** primary Niri PID 1145 and boot identity
  `be7bf359-b534-4227-9947-f34d2b63936d` stay unchanged. No compositor, login
  manager, PipeWire core or WirePlumber restart; no boot writes/reboot. Only the
  PulseAudio compatibility service restarts and a transient session watcher starts.

## Remaining acceptance

The first operator retry after service repair fails: joining a Huddle shows a
"Microphone Muted" message and Huddle windows turn black until force quit.
The system default microphone remains unmuted. Slack logs report its renderer
was killed; they do not establish why its windows turned black. This supersedes
any inference that successful backend probes establish usable Slack Huddles.
Reopened the closed app with `--disable-gpu` for a temporary software-rendering
diagnostic; saved Slack preferences and launch entries remain unchanged. The
operator then confirms the microphone works and identifies the earlier message
as a small desktop popup. A live PulseAudio source-output also confirms Slack's
capture stream. The operator subsequently confirms normal window rendering and
working screen sharing, while reporting occasional repeated source-chooser prompts.

During the same retry, `wpctl status` shows an active Niri video output linked to
Slack's video input, alongside active microphone capture and speaker playback.
This establishes a live sharing connection without inspecting screen content;
it does not establish the recipient's image or correct Huddle window rendering.

After that confirmation, installed a new account-only
`~/.local/share/applications/slack.desktop`, copied from the packaged entry with
only `--disable-gpu` added to `Exec`. Exclusive file creation preserves any existing
personal entry; none existed. Native desktop validation passes, mode is 0644, and
Gio desktop lookup selects the new account entry. The native package entry and
saved Slack preferences remain unchanged. An initial candidate validation through
`/dev/stdin` stops before writes; validating an ordinary temporary file succeeds.
The new launcher applies on future menu/deep-link launches; a direct `slack` command
still needs `--disable-gpu`. To recover, remove only this newly added account entry
and refresh the account desktop cache. No current Huddle or application restart is
needed for installation. GPU acceleration is disabled only for this app/account,
with a potential CPU cost; this is not a new global profile default.

The repeated chooser is consistent with Electron's
[reported redundant Wayland share dialogs affecting Slack](https://github.com/electron/electron/issues/30652)
and its [PipeWire source-selection API constraints](https://www.electronjs.org/docs/latest/api/desktop-capturer#linux).
This is an inference from upstream reports and the observed successful live stream,
not a proven Slack-internal root cause or a resolved issue. The portal also logs
parent-window association warnings and nonfatal Vulkan `VK_SUBOPTIMAL_KHR` messages.
No portal permissions are bypassed and no Slack application code is patched.

Original microphone/rendering/screen-sharing symptoms are operator-confirmed
resolved with the above changes. Repeated chooser prompts remain a known limitation;
track an upstream Slack/Electron correction. Explicit remote-participant reception
is not separately recorded. Verify a convenient
fresh Qubix login starts `niri.service` and `graphical-session.target`, selects
the Qubix config and shuts down the target on logout. Do not restart the current
desktop merely to obtain this evidence. If audio stalls again, collect service
logs and investigate the compatibility-service failure rather than periodically
restarting it. No new visual customization or boot acceptance is claimed.

## GPU-enabled comparison and repeated chooser trace

Follow-up on 2026-10-22, source base `910137f`. This supersedes the earlier
inference that disabling GPU acceleration was necessary. The operator reports
previously successful terminal launches; the narrowly filtered Slack command
history confirms both:

```bash
slack --enable-features=WebRTCPipeWireCapturer --ozone-platform-hint=auto
slack --enable-features=WebRTCPipeWireCapturer,WaylandWindowCapturer --ozone-platform-hint=auto
```

Tested the first combination with native `--gtk-version=3`, without `--disable-gpu`.
The initial launch request reuses the existing process and is **not** comparison
evidence. An initial process check misses Slack because it flattens its process
title into one argv entry; checking `comm` and splitting that entry detects the
old `--disable-gpu` process. After the operator fully quits Slack, the guarded
relaunch establishes a new main PID 247533 with the intended flags. Its GPU
process selects `--ozone-platform=wayland`; fresh startup telemetry reports
`gpu_compositing: enabled` and `webgl: enabled`. The saved
`useHwAcceleration` preference is true and remains unchanged.

The operator confirms rendering and microphone work, while reporting multiple
choosers and one desktop sharing-stopped message. An active Niri-to-Slack video
link remains afterward. These results establish that the earlier software-rendering
workaround is unnecessary for this retry. They do not isolate which flag, audio
recovery or clean application restart explains the original improvement. Slack's
child-process flags already enabled `WebRTCPipeWireCapturer` during the prior run.
The second command's additional `WaylandWindowCapturer` is not tested or needed
for the demonstrated result.

Installed the validated GPU-enabled account launcher only after that confirmation.
It replaces only the exact Qubix-created content; unexpected personal edits or a
symlink would stop replacement. The earlier file is backed up at
`~/.cache/qubix-huddle/slack-disable-gpu-20261022T232216Z.desktop`. Native
`desktop-file-validate` and Gio desktop lookup pass, with mode 0644. The saved Exec
retains `-s %U` and the native GTK selection, adding only the two tested flags.
Native package entry and saved preferences remain preserved. No current-call
restart is performed for installation. Direct terminal launches may use the
tested command above; removing the new account override restores native launch.

A three-minute transient diagnostic service pipes `dbus-monitor` into a filter
that retains only ScreenCast method headers, discarding all argument lines and
screen content. The clean-retry trace records four public `CreateSession`, four
`SelectSources`, four `Start` and three `OpenPipeWireRemote` calls. Their sender
is the same bus connection, `:1.353`; `GetConnectionUnixProcessID` maps it to
Slack main PID 247533. Backend calls mirror the four frontend requests.

| Session | Public CreateSession timestamp (EDT) | Start requested | PipeWire remote opened |
|---|---|---|---|
| 1 | 19:20:48.666 | Yes | Yes |
| 2 | 19:20:52.681 | Yes | Not observed |
| 3 | 19:20:53.689 | Yes | Yes |
| 4 | 19:20:55.471 | Yes | Yes |

This establishes multiple separate requests from Slack, rather than the host
spontaneously reopening one chooser. Inspection of the native packaged
`app.asar` finds a preview/listing helper using `desktopCapturer.getSources` and
a Wayland `setDisplayMediaRequestHandler` which calls
`getSources({types:["window","screen"]})` before invoking the callback with the
selected source. This corroborates the application-level extra-session explanation
in [Electron issue 30652](https://github.com/electron/electron/issues/30652).
It does not prove which compiled call site initiated each recorded request.
No application package is modified. The metadata trace omits Session.Close and
response arguments, so the operator's stopped message cannot be conclusively
assigned to a preview ending, a cancellation or an actual share interruption.

The portal stays running and the final video link is active. Existing parent-window
association and nonfatal Vulkan swapchain warnings remain. No verified launcher
flag or portal setting suppresses Slack's redundant requests. The application-side
fix must avoid/reuse unnecessary capture sessions while retaining the intended
chooser. Repeated prompts and the stopped message remain unresolved, with explicit
participant reception and next-login lifecycle acceptance still separate.
[Current Slack release notes](https://slack.com/release-notes/linux) list 4.52.182
after installed 4.52.178, but do not document a repeated-chooser fix; no package
upgrade is performed or claimed as a solution.
