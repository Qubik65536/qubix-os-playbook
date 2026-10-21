# Backlog

Local bootstrap planning; later mirror substantial tasks to GitHub Issues. Categories: Feature, Bug, Documentation, Refactor, Testing, Maintenance. Dependencies are explicit; this is not a duplicate roadmap.

## F01 — Read-only foundation (Feature)

Status: Implemented; fixture contracts and actual CachyOS read-only collection Tested. Protected boot metadata requires explicit privilege; the live run reports zero changes.

Objective: safely inspect CachyOS Niri and resolve the profile. Scope: schema, read-only evidence, compatibility, verify/deploy preflight, minimal wrapper. Acceptance: supported fixtures pass; unsupported hosts, malformed inputs and unsupported enabled selections fail before writes; ambiguities remain unresolved. Depends on documentation. Tests: real Ansible fixture runs, macOS rejection, syntax/lint. Docs: configuration, deployment, compatibility, status.

## M01 — Tooling and CI (Maintenance)

Status: Implemented; local static/dispatch/core checks Tested; remote timing pending.
Earlier remote runs passed,
but slower runners exhausted the serial 30-minute limit. Four isolated fixture groups
now run alongside static validation within 30-minute jobs, preserving every test/mode.
Acceptance: [CI validation time budget](../development/testing.md#ci-validation-time-budget).
Mocked execution confirms all 38 original invocations and failure propagation;
static validation and the real core group pass.
Next: after an authorized push, measure full Validate/Release validation completion,
verify per-group diagnostic logs and the archive gated on all matrix jobs.

Objective: repeatable local/CI checks. Scope: pinned controller dependencies, YAML/Ansible/ShellCheck/Markdown consistency checks and Actions. Acceptance: local commands and workflow agree; checks pass. Depends on documentation. Tests: execute available validators and record missing tools explicitly. Docs: environment/testing/installation.

## M02 — Source distribution and manual candidate releases (Maintenance)

Status: Implemented; static/archive/recovery checks Tested locally; remote Actions pending.
Scope and acceptance: [release contract](../development/releases.md). CI packages the
tracked source only after checks; manual publication always creates a prerelease.
Next: after authorized push, run Validate, download/verify its artifact, then manually
publish an authorized candidate and verify its assets. Stable MVP publication remains
blocked on the independent native acceptance matrix, not on source packaging.

## M04 — Automatic candidate release versions (Maintenance)

Status: Implemented; eight mocked workflow-shell cases and static checks Tested; remote publication pending.
Scope/acceptance: [automatic versioning](../development/releases.md#automatic-versioning-acceptance).
Next: after an authorized push, manually dispatch Release with the tag empty and verify
its generated UTC version/title, exact source commit and packaged assets. Do not treat
calendar numbering as stable MVP acceptance.

## D02 — Separate local user onboarding and developer SSH testing (Documentation)

Status: Implemented; static/link/example checks and local inventory inspection Tested.
Acceptance: [deployment transport contract](../architecture/deployment.md#user-deployment-and-developer-transport).
User commands run on the destination machine as its desktop account; SSH is developer
VM testing. Preserve preparation/default/boot confirmation and recovery requirements.
Next: walk through the packaged user-local procedure in an explicitly authorized
CachyOS Niri disposable VM; record file/parser/session/boot evidence separately.
Historical SSH success does not establish that local walkthrough.

## M03 — Remove unused alternative-shell references (Maintenance)

Status: Implemented; static/discovery checks and operator-selected SSH target audit Tested.
Scope/acceptance: [discovery cleanup](../architecture/compatibility.md#unused-shell-discovery-cleanup).
The target has no related package/process/startup installation; zero target changes
are required. Next: keep platform evidence limited to supported dependencies when
adding components; retain native Niri/Noctalia checks in the normal acceptance matrix.

## F02 — Shared artwork (Feature)

Status: Implemented; isolated filesystem and normal/check-mode acceptance Tested. Native CachyOS installation, verification, idempotency and original-absence restoration pass.

Objective: first useful safe mutation. Scope: canonical Qubix assets, attribution/checksums, fixed destination files, read-only verification. Acceptance: isolated install/checksum/idempotency/preview tests, unrelated files preserved, no identity changes. Depends on F01/M01. Tests: temporary filesystem, corruption and absence failures. Docs: branding, restoration and status.

## F03 — CachyOS Niri default activation (Feature)

Status: Noctalia redesign Implemented; native grammar, version fixtures, nested rendering, deployment, preservation and zero-change reapplication Tested; primary startup after operator-authorized native-entry retirement/reboot Tested; interaction/recovery acceptance pending. Separate widget capsules and the generated searchable shortcut panel pass native preview, installation, verification and zero-change reapplication, including configuration/compositor preservation and cleanup. Compact bar/dock removal, pinned launcher power controls and resizing pass native preview, deployment, zero-change reapplication and installed verification from bbea600; the existing Qubix primary session reloads with unchanged process IDs. Current native/personal snapshots and earlier baseline hashes remain preserved. The [logo/bar visibility correction](desktop-test-results.md#bar-visibility-and-logo-correction) passes native comparison, live reload, installed verification and zero-change reapplication from ce72276. Earlier classic restoration evidence remains historical; new Noctalia restoration and primary-session gates remain open.

Objective: begin a usable Qubix desktop on an actual target. Scope: live report, supported KDL candidate, theme include, detected companion commands and preservation policy. Acceptance: `niri validate`, user/system originals preserved, actual wallpaper/launcher/bar/notifications/terminal work in VM, second run unchanged. Depends on F02, F06 backup preparation for default activation, and live VM evidence. Tests: parser + preservation + VM graphical session. Docs: Niri, compatibility, user deployment and recovery.

### F03a — Power confirmation (Feature)

Status: Implemented; no-effect Luau behavior fixtures, static checks and the 69-task desktop
ownership/version fixture (normal/check mode, zero changes, seven expected refusals each) Tested.
Native parsing/plugin lint, rendering, installation, live reload and zero-change reapplication
from clean d415856 are [Tested](desktop-test-results.md#power-confirmation-deployment).
Scope and acceptance are in the [power confirmation contract](../architecture/desktop-design.md#power-action-countdown).
Next: operator checks of early-release/Escape and click cancellation, followed by newer-resource recovery acceptance.
The Control Center's separate native menu retains tap-based countdown semantics.

Footer/lock-close correction: Implemented; deferred-close/native no-effect regressions pass.
Reference/footer/countdown/live screenshots accompany the docs. Clean e80b697 installation, installed
verification, live footer and zero-change reapplication Tested, with preserved settings/recovery
records. Next: physical lock/unlock and cancellation acceptance.

Native-layout correction: Implemented; content centring, footer removal and destructive Shut Down
styling pass controller/native/live comparison checks. Clean 78cc3e1 installation, installed verification
and zero-change reapplication Tested; preservation and credential cleanup pass. Next: physical
hold/release and click/Escape acceptance, then newer-resource recovery.

Native-style refinement: Implemented; behavior/ownership checks, native comparison, installation
and zero-change reapplication from clean f1a28b1 Tested. A Noctalia-only restart is required to refresh
cached manifest geometry; the live row is inspected with Niri/apps and GUI state preserved.
See the [activation evidence](desktop-test-results.md#native-style-power-menu). Next: physical
early-release/click/Escape acceptance and newer-resource recovery; keep the current native tile layout.

## F03b — Monaspace NF and configurable Krypton UI (Feature)

Status: Implemented; fixtures, native comparison/installation, active shell and zero-change reapplication Tested.
Install pinned official GitHub Monaspace NF fonts and independently select Krypton UI defaults. Scope, ownership and acceptance are authoritative in the
[font contract](../components/fonts.md). Source preparation and disposable fixtures are independent of target activation.
The [test evidence](font-test-results.md) records clean d38d479, exact installed/native defaults,
preserved user/boot/recovery resources and zero-change reapplication. Next: optional native
font/default restoration in a disposable VM and safe reduction of large-asset serial-controller
overhead; preserve the shared first-baseline and receipt contracts.

## F04 — Shell/terminal defaults (Feature)

Status: Implemented; shell precedence fixtures and temporary-home native Bash/Starship initialization Tested; normal account startup gate open.

Objective: Qubix terminal experience. Scope: detected applications and additive defaults, no automatic shell change. Acceptance: working terminal/shell with personal files preserved. Depends on F03 target evidence. Tests: parsing/startup/idempotency. Docs: component ownership and user override/recovery.

## F05 — Login theme (Feature)

Status: Implemented SDDM candidate and Noctalia Greeter; fixtures, native UI/file installation,
unchanged reapplication and approved next-boot selection Tested; real login/recovery pending.

The [Noctalia contract](../components/login.md) adds explicit inactive preparation and existing-greetd
appearance, a separate package preparation playbook and operator guides for manager cutover and
fingerprints. It shares Qubix's desktop palette/wallpaper while preserving PAM, native services,
session/keyboard/output/auth settings and mutable sync state. The target is selected for greetd
on its next boot, with the current SDDM desktop still active. See [login test results](login-test-results.md).
Native package setup integrates a session module into fresh greetd PAM; no pre-existing PAM or
fingerprint authentication is changed. Next: operator reboot and physical password login/Niri
return, local fingerprint enrollment/fallback and recovery.
Keep boot entry identities and native distribution identity preserved. The explicitly requested
presentation captions and OS menu title are tracked separately below.

Objective: brand supported active manager without changing authentication/session. Scope: detected manager's supported theme hooks only. Acceptance: login and Niri startup succeed, PAM unchanged, restoration tested. Depends on F03. Tests: VM login and revert. Docs: manager/version support and recovery.

### F05a — Compact login, fingerprint enrollment and display names (Feature)

Status: Implemented; controller/provenance fixtures, native simulated rendering, installation,
zero-change reapplication and desktop-caption activation Tested. The [contract](../architecture/login-refinement.md) owns
responsibilities/acceptance; [comparison evidence](ui-test-results.md) records actual checks.
Provide a GTK/fprintd enrollment application, smaller steel-blue greeter and explicit QubixOS
launcher/Control Center/Limine OS captions. Preserve native packages, authentication, identity,
boot IDs and payloads. Clean `fc721e1` installation/verification/reapplication and live process
activation pass. Native byte checks establish the bounded menu change from `14a0339`.
Next: operator enrollment/test, password fallback, future compact-greeter startup
and renamed-menu console acceptance remain open.

## F06 — Revision state and recovery (Feature)

Status: Implemented; fault/drift/restore/state fixtures plus native desktop absence/state lifecycle Tested; boot/image recovery gate open.

Objective: auditable resource-level restoration. Scope: manifests, backups before existing-default mutation, original absence/metadata, revision/config digest and dirty detection. Acceptance: success state only after verify; conflict-safe repeated restoration and interrupted failure diagnosis. Depends on F01; needed before default/boot activation. Tests: fault injection, restore and preservation fixtures. Docs: lifecycle/restoration.

## F07 — GRUB adapter (Feature)

Status: Implemented; independent preservation/private-mode/reapplication/absent-hook/stale-restoration fixtures Tested; native checker/reboot/restore open.

Objective: safe GRUB branding. Scope: active configuration evidence, minimal activation, owned theme and backups. Acceptance: preserved entries/arguments, validated output, boot and recovery in VM. Depends on F02/F06. Tests: independent GRUB VM, idempotency and restoration. Docs: boot compatibility and exact recovery.

## F08 — Limine adapter (Feature)

Status: Implemented 8–12 candidate; independent version/preservation/stale-restoration fixtures Tested; native Limine 12 normal-kernel reboot/menu confirmed; restore open.

Appearance follow-up: the version-12 adapter now supplies a boot-accessible Qubix wallpaper and supported palette/margins/font scaling. Preservation, reapplication, restoration and three unsafe-input fixtures pass; deployment and zero-change native reapplication pass. The operator confirms the menu after a controlled normal-kernel reboot. Requested typography/palette refinement and native recovery remain open.

The requested Krypton refinement is Implemented in source: complete 8x20 CP437 font, midnight cube
wallpaper and explicit heading/help/selection colours. The reviewed 15-key graphical ownership
upgrade retains first-original bytes and unrelated metadata; normal lifecycle passes 726 tasks with
eight expected refusals, and a global check-mode control passes 21 tasks with no metadata writes.
Clean 87e824b deployment, zero-change reapplication and normal-kernel reboot pass. The operator requests higher contrast, smaller menu text and the detailed desktop cube wallpaper; the correction is now deployed from clean f626188 with exact image/pin checks and zero-change reapplication. Obtain renewed console feedback; independent native recovery remains open.

Objective: safe Limine branding; mandatory MVP. Scope: installed-version-supported settings, active-path validation and minimal edits. Acceptance: unchanged entries/arguments, VM boot and recovery. Depends on F02/F06; independent of F07. Tests: Limine-specific syntax where supported, VM and preservation. Docs: supported directives/versions and recovery.

## F09 — Plymouth with two generators (Feature)

Startup fallback repair Implemented and normal startup Tested: the operator reported blank startup followed by the
three-square text fallback, superseding prior appearance acceptance for the current revision.
The measured early simpledrm/native GPU gap motivates an explicit early graphics opt-in and
required DRM archive checks. See the [repair acceptance criteria](../components/plymouth.md#early-graphics-repair).
Focused fixtures pass 521 tasks with ten expected refusals; schema, global check-mode and Limine
lifecycle checks pass. Native results follow; the operator confirms repaired startup.

Native deployment from clean 0324e27, installed verification, exact four-image/font/DRM/pin checks
and unchanged reapplication now pass. All earlier recovery bytes and native boot files remain
intact; the preboot desktop session remains active and the temporary inhibitor is removed. The
operator subsequently confirms the Qubix splash appears and the desktop returns after the requested
normal reboot. Next: independent LTS, poweroff, encryption, dracut and recovery acceptance;
post-reboot SSH preservation is not independently audited for this repair.

Current visual correction is deployed from clean e3bf16b: preserve original logo colours and add a native scaled
desktop-cube background. Scope: artwork/definition, plugin capability preflight and archive inclusion;
keep mappings/recovery ownership fixed. Acceptance: canonical logo crop matches pixel-for-pixel,
all-mode/native-prompt preview renders the picture, active images contain exact resources and
reapplication skips regeneration. Native visual acceptance remains separate; see the
[design contract](../architecture/boot-design.md#original-colour-logo-and-picture-background-correction).

Status: Implemented; simulated dispatch/archive/font/preview/kernel guards and preservation of literal snapshot-hook appends Tested. Native isolated boot/shutdown/reboot circular rendering and synthetic prompt pass with preservation/cleanup. Native mkinitcpio generation and exact active-image contents pass; normal-kernel startup/reboot visuals confirmed; poweroff, LTS, dracut, encryption and restore remain open; see the [activation proposal](plymouth-test-plan.md).

Objective: startup splash independent of loader. Scope: Qubix theme, dracut/mkinitcpio minimal integration and conditional rebuild. Acceptance: resources verified, both combinations boot/show splash, unrelated settings preserved and restore passes. Depends on F02/F06. Tests: two independent generator VM runs, reapplication and recovery. Docs: image selection, compatibility, recovery.

Native-style correction: source replaces the rejected scripted layout with two-step, a small spinner and bottom watermark. Active Limine image synchronization and normal-kernel startup/reboot observations pass for e7e652a. The requested midnight palette, vector ring and Krypton-derived wordmark/prompt subset are now Implemented in source; native preview selects the exact font and passes animation/prompt/preservation/cleanup checks. The two-generator fixture passes 409 tasks with five expected refusals. Clean 87e824b deployment/reapplication/reboot pass; the operator requests higher contrast and removal of captions. The correction is deployed from clean f626188 with exact image/pin checks and zero-change reapplication. Obtain renewed console feedback; real encryption, LTS and recovery remain open.

Active-image repair: explicit Limine 12 cache/kernel bindings, content-addressed staging, atomic
module/pin replacement, exact active-archive checks and config-first recovery are Implemented.
Binding refusal/check-mode fixtures and earlier-baseline alias enrollment/FAT mode fixtures pass;
the 767-task nested-entry lifecycle and 1077-task target no-write preview pass. Native deployment passes
1542 tasks; installed verification passes 284 tasks with zero changes. Exact four-image extraction/pins,
19 native boot resources and 32 earlier baseline hashes pass. After two connectivity interruptions,
same-source reapplication passes 1490 tasks with zero changes and skips both rebuilds; installed
verification again passes 284 tasks/zero changes and pending state clears. The guarded reboot returns
SSH/SDDM/Qubix at 100% scale; the operator confirms menu/startup/reboot branding.
Future maintenance: design reviewed ownership/recovery rebasing after kernel updates or
expanding a narrower text/splash-only appearance baseline; current guards refuse unsafe transitions.

## T01 — MVP acceptance (Testing)

Status: In Progress; SSH details supplied, connected after service/firewall setup; privileged read-only discovery passes. Approved physical desktop deployment, reapplication, earlier absence restoration, nested rendering and primary startup/reload pass; physical interaction, newer Noctalia recovery, login and VM boot tests remain pending. Next gate is native acceptance of the Noctalia redesign plus the remaining independent login/boot tests.

Objective: complete scope evidence. Scope: end-to-end desktop/login/loader/splash, reapplication, configuration preservation, diagnostics and recovery. Acceptance: all [MVP criteria](scope.md) pass with recorded versions and evidence. Depends on F03–F09. Tests: disposable VM matrix. Docs: compatibility/status, release readiness and changelog.

## D01 — Human onboarding (Documentation)

Status: Implemented; links/syntax checked and native desktop procedure Tested; main-session/VM walkthrough pending.

Objective: make the candidate usable/reviewable. Scope: operator/developer guides, target collector, recovery/checklist. Acceptance: desktop independent of boot, opt-ins/evidence clear. Depends on candidate contracts. Tests: static links, ShellCheck, collector help/controller refusal; native desktop CLI walkthrough passes; main-session/boot walkthrough pending. Docs: README/onboarding/status.

## T02 — Physical desktop test authorization (Testing)

Status: Desktop preparation/file lifecycle/nested rendering Tested; primary-session acceptance In Progress. See [results](desktop-test-results.md) and [authorized plan](live-test-plan.md).

Objective: test the desktop while preserving the physical host. Scope: approved native package preparation and branding/Niri/shell only; preserve existing Noctalia/Alacritty and personal files. Acceptance: native Foot/Niri validation, observed companions, original hashes, zero managed changes on reapplication and restoration. Operator authorization included native Snapper/Limine package-hook effects. Remaining tests require operator-selected main-session evidence. Tests: preview, target verification and operator-selected session; no boot/splash activation. Docs: status, compatibility and acceptance evidence.

## V01 — Subtle Plymouth wordmark (Feature)

Status: Implemented; local asset validation Tested; native gates pending. Reduce and lower the logo/text group, widen its gap and use the theme's
steel-blue text accent. See the authoritative [design and acceptance](../architecture/boot-design.md#subtle-bottom-wordmark-refinement).
Complete deterministic asset validation, native preview, exact image installation/reapplication and
console observation on the already authorized target; preserve original logo colours and prompt controls.

## F05b — KWallet password storage (Feature)

Status: Implemented; native PAM/Secret Service and KDE API roundtrips, live three-entry
migration, installation, installed verification, zero-change reapplication and disposable recovery Tested. Scope and acceptance are in the [keyring contract](../components/keyring.md).
Opt in through `keyring.enabled`, prepare native packages separately and preserve original
encrypted stores. Retain GNOME Keyring while required by the CachyOS desktop package;
no forced package removals. Next: operator password logout/login acceptance; retain both encrypted stores for recovery. See
[test evidence](keyring-test-results.md) and the [guide](../user/keyring.md).

## F10 — Final-deployment defaults and fresh-machine preparation (Feature)

Status: Implemented; controller fixtures/static validation Tested. Promote implemented desktop/login/storage features into the supported
profile, document every effective default and require new implemented features to default on
unless directed otherwise. Acceptance is in the [configuration contract](../architecture/configuration.md).
Keep explicit boot/machine confirmations and personal preservation. Validate resolved defaults,
recursive opt-outs and unsupported-combination failures before writes. Normal/check-mode
framework runs each pass 860 tasks/zero changes; all 28 default inputs are explained and checked.

## F11 — Automatic fresh-machine onboarding (Feature)

Status: Planned. Automatic fresh-machine onboarding requires a separate implementation: current package/build preparation playbooks
are separate commands; manager selection and migration of existing secrets require operator
steps. A future workflow needs its own documented privileged preparation/activation contract;
profile defaults alone must never claim automatic installation or manager cutover.

## F12 — Boot and splash default selection (Feature)

Status: Implemented; controller normal/check-mode gates Tested (46 tasks/zero changes,
two expected refusals each); schema/discovery regression 882 tasks/zero changes.
Default both components on as requested; preserve explicit target
confirmations and mappings. Acceptance: resolved defaults/opt-outs and first-task adapter
refusals in normal/check mode, plus static documentation agreement. No physical boot change.

## F — CachyOS package managers and WezTerm acceptance (Testing)

Status: Native existing-manager preservation, installation/removal, terminal rendering,
parser checks, active-shell selection and zero-change reapplication Tested on the
operator-authorized SSH instance. See [evidence and comparison captures](package-management-test-results.md).
Remaining: exercise fresh Homebrew bootstrap, incomplete-prefix recovery and dependency-blocked
removal in a disposable CachyOS VM; confirm physical shortcuts and terminal-launching
application actions. Follow the [component acceptance contract](../components/package-management.md).

## F — Supplied WezTerm appearance (Feature/Testing)

Status: Implemented; source/provenance, supplied palettes, personal-config precedence,
exact native file installation, font selection, parser controls, rendering, activation
and reapplication Tested on the authorized SSH instance. See [comparison/evidence](wezterm-test-results.md)
and the [component contract](../components/wezterm.md). Remaining manual gates: physical
shortcuts and launcher selection, both Alt keys, transparency over the chosen background,
and fallback glyph coverage. Do not treat this as new login/boot acceptance.

## F — WezTerm home configuration and actual scene transparency (Feature/Testing)

Primary-session correction: the 2026-10-18 nested result did not prove live activation;
the focused deployment missed the rendered session configuration. See the
[repair acceptance and evidence](wezterm-home-test-results.md#primary-session-repair-2026-10-20).
Next: retain the installed-configuration gate when repeating native acceptance;
physical input and fullscreen appearance remain manual checks.

Status: Implemented and Tested. One canonical Lua, backed-up home deployment, scoped
compositor fill correction, contrasting composed scenes/pixel controls, exact account
ownership/bytes, native parser controls, reapplication and app/session/boot preservation
pass. See [native evidence](wezterm-home-test-results.md).
See the [contract](../components/wezterm.md). Account-file recovery uses timestamped
copy backups; integration into generic system restoration is Planned separately.

## F16 — Wi-Fi hotspot sharing (Feature)

Status: Implemented; native installation/parser/GUI/backend startup Tested; second-client acceptance pending.
Scope/acceptance: [hotspot contract](../components/hotspot.md).
Native installation/reapplication/isolated restoration and timed AP startup pass;
see [evidence](hotspot-test-results.md). Next: test association, DHCP, DNS and Internet
from a second physical client on a permitted shared channel, then stop sharing.
