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
