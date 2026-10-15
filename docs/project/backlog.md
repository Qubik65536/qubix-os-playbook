# Backlog

Local bootstrap planning; later mirror substantial tasks to GitHub Issues. Categories: Feature, Bug, Documentation, Refactor, Testing, Maintenance. Dependencies are explicit; this is not a duplicate roadmap.

## F01 — Read-only foundation (Feature)

Status: Implemented; fixture contracts and actual CachyOS read-only collection Tested. Protected boot metadata requires explicit privilege; the live run reports zero changes.

Objective: safely inspect CachyOS Niri and resolve the profile. Scope: schema, read-only evidence, compatibility, verify/deploy preflight, minimal wrapper. Acceptance: supported fixtures pass; unsupported hosts, malformed inputs and unsupported enabled selections fail before writes; ambiguities remain unresolved. Depends on documentation. Tests: real Ansible fixture runs, macOS rejection, syntax/lint. Docs: configuration, deployment, compatibility, status.

## M01 — Tooling and CI (Maintenance)

Status: Implemented; local scripts Tested. GitHub workflow execution pending.

Objective: repeatable local/CI checks. Scope: pinned controller dependencies, YAML/Ansible/ShellCheck/Markdown consistency checks and Actions. Acceptance: local commands and workflow agree; checks pass. Depends on documentation. Tests: execute available validators and record missing tools explicitly. Docs: environment/testing/installation.

## F02 — Shared artwork (Feature)

Status: Implemented; isolated filesystem and normal/check-mode acceptance Tested. Native CachyOS installation, verification, idempotency and original-absence restoration pass.

Objective: first useful safe mutation. Scope: canonical Qubix assets, attribution/checksums, fixed destination files, read-only verification. Acceptance: isolated install/checksum/idempotency/preview tests, unrelated files preserved, no identity changes. Depends on F01/M01. Tests: temporary filesystem, corruption and absence failures. Docs: branding, restoration and status.

## F03 — CachyOS Niri default activation (Feature)

Status: Noctalia redesign Implemented; native grammar, version fixtures, nested rendering, deployment, preservation and zero-change reapplication Tested; primary startup after operator-authorized native-entry retirement/reboot Tested; interaction/recovery acceptance pending. Separate widget capsules and the generated searchable shortcut panel pass native preview, installation, verification and zero-change reapplication, including configuration/compositor preservation and cleanup. Compact bar/dock removal, pinned launcher power controls and resizing pass native preview, deployment, zero-change reapplication and installed verification from bbea600; the existing Qubix primary session reloads with unchanged process IDs. Current native/personal snapshots and earlier baseline hashes remain preserved. The [logo/bar visibility correction](desktop-test-results.md#bar-visibility-and-logo-correction) passes native comparison, live reload, installed verification and zero-change reapplication from ce72276. Earlier classic restoration evidence remains historical; new Noctalia restoration and primary-session gates remain open.

Objective: begin a usable Qubix desktop on an actual target. Scope: live report, supported KDL candidate, theme include, detected companion commands and preservation policy. Acceptance: `niri validate`, user/system originals preserved, actual wallpaper/launcher/bar/notifications/terminal work in VM, second run unchanged. Depends on F02, F06 backup preparation for default activation, and live VM evidence. Tests: parser + preservation + VM graphical session. Docs: Niri, compatibility, user deployment and recovery.

## F04 — Shell/terminal defaults (Feature)

Status: Implemented; shell precedence fixtures and temporary-home native Bash/Starship initialization Tested; normal account startup gate open.

Objective: Qubix terminal experience. Scope: detected applications and additive defaults, no automatic shell change. Acceptance: working terminal/shell with personal files preserved. Depends on F03 target evidence. Tests: parsing/startup/idempotency. Docs: component ownership and user override/recovery.

## F05 — Login theme (Feature)

Status: Implemented SDDM candidate; cloning/activity fixtures Tested; authentication/restore gate open.

Objective: brand supported active manager without changing authentication/session. Scope: detected manager's supported theme hooks only. Acceptance: login and Niri startup succeed, PAM unchanged, restoration tested. Depends on F03. Tests: VM login and revert. Docs: manager/version support and recovery.

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
Clean 87e824b deployment, zero-change reapplication and normal-kernel reboot pass. The operator requests higher contrast, smaller menu text and the detailed desktop cube wallpaper; deploy/observe that correction. Independent native recovery remains open.

Objective: safe Limine branding; mandatory MVP. Scope: installed-version-supported settings, active-path validation and minimal edits. Acceptance: unchanged entries/arguments, VM boot and recovery. Depends on F02/F06; independent of F07. Tests: Limine-specific syntax where supported, VM and preservation. Docs: supported directives/versions and recovery.

## F09 — Plymouth with two generators (Feature)

Status: Implemented; simulated dispatch/archive/font/preview/kernel guards and preservation of literal snapshot-hook appends Tested. Native isolated boot/shutdown/reboot circular rendering and synthetic prompt pass with preservation/cleanup. Native mkinitcpio generation and exact active-image contents pass; normal-kernel startup/reboot visuals confirmed; poweroff, LTS, dracut, encryption and restore remain open; see the [activation proposal](plymouth-test-plan.md).

Objective: startup splash independent of loader. Scope: Qubix theme, dracut/mkinitcpio minimal integration and conditional rebuild. Acceptance: resources verified, both combinations boot/show splash, unrelated settings preserved and restore passes. Depends on F02/F06. Tests: two independent generator VM runs, reapplication and recovery. Docs: image selection, compatibility, recovery.

Native-style correction: source replaces the rejected scripted layout with two-step, a small spinner and bottom watermark. Active Limine image synchronization and normal-kernel startup/reboot observations pass for e7e652a. The requested midnight palette, vector ring and Krypton-derived wordmark/prompt subset are now Implemented in source; native preview selects the exact font and passes animation/prompt/preservation/cleanup checks. The two-generator fixture passes 409 tasks with five expected refusals. Clean 87e824b deployment/reapplication/reboot pass; the operator requests higher contrast and removal of captions. Deploy/observe that correction; real encryption, LTS and recovery remain open.

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
