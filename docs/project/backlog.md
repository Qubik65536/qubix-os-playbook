# Backlog

Local bootstrap planning; later mirror substantial tasks to GitHub Issues. Categories: Feature, Bug, Documentation, Refactor, Testing, Maintenance. Dependencies are explicit; this is not a duplicate roadmap.

## F01 — Read-only foundation (Feature)

Status: Implemented; fixture contracts Tested. Live CachyOS collection acceptance remains open.

Objective: safely inspect CachyOS Niri and resolve the profile. Scope: schema, read-only evidence, compatibility, verify/deploy preflight, minimal wrapper. Acceptance: supported fixtures pass; unsupported hosts, malformed inputs and unsupported enabled selections fail before writes; ambiguities remain unresolved. Depends on documentation. Tests: real Ansible fixture runs, macOS rejection, syntax/lint. Docs: configuration, deployment, compatibility, status.

## M01 — Tooling and CI (Maintenance)

Status: Implemented; local scripts Tested. GitHub workflow execution pending.

Objective: repeatable local/CI checks. Scope: pinned controller dependencies, YAML/Ansible/ShellCheck/Markdown consistency checks and Actions. Acceptance: local commands and workflow agree; checks pass. Depends on documentation. Tests: execute available validators and record missing tools explicitly. Docs: environment/testing/installation.

## F02 — Shared artwork (Feature)

Status: Implemented; isolated filesystem and normal/check-mode acceptance Tested. Live target deployment remains unverified.

Objective: first useful safe mutation. Scope: canonical Qubix assets, attribution/checksums, fixed destination files, read-only verification. Acceptance: isolated install/checksum/idempotency/preview tests, unrelated files preserved, no identity changes. Depends on F01/M01. Tests: temporary filesystem, corruption and absence failures. Docs: branding, restoration and status.

## F03 — CachyOS Niri default activation (Feature)

Status: Implemented candidate; native parser/session/preservation/idempotency gate open.

Objective: begin a usable Qubix desktop on an actual target. Scope: live report, supported KDL candidate, theme include, detected companion commands and preservation policy. Acceptance: `niri validate`, user/system originals preserved, actual wallpaper/launcher/bar/notifications/terminal work in VM, second run unchanged. Depends on F02, F06 backup preparation for default activation, and live VM evidence. Tests: parser + preservation + VM graphical session. Docs: Niri, compatibility, user deployment and recovery.

## F04 — Shell/terminal defaults (Feature)

Status: Implemented; shell precedence fixture Tested; native interactive startup gate open.

Objective: Qubix terminal experience. Scope: detected applications and additive defaults, no automatic shell change. Acceptance: working terminal/shell with personal files preserved. Depends on F03 target evidence. Tests: parsing/startup/idempotency. Docs: component ownership and user override/recovery.

## F05 — Login theme (Feature)

Status: Implemented SDDM candidate; cloning/activity fixtures Tested; authentication/restore gate open.

Objective: brand supported active manager without changing authentication/session. Scope: detected manager's supported theme hooks only. Acceptance: login and Niri startup succeed, PAM unchanged, restoration tested. Depends on F03. Tests: VM login and revert. Docs: manager/version support and recovery.

## F06 — Revision state and recovery (Feature)

Status: Implemented; fault/drift/restore/state fixtures Tested; live recovery gate open.

Objective: auditable resource-level restoration. Scope: manifests, backups before existing-default mutation, original absence/metadata, revision/config digest and dirty detection. Acceptance: success state only after verify; conflict-safe repeated restoration and interrupted failure diagnosis. Depends on F01; needed before default/boot activation. Tests: fault injection, restore and preservation fixtures. Docs: lifecycle/restoration.

## F07 — GRUB adapter (Feature)

Status: Implemented; independent preservation/private-mode/reapplication/file-restoration fixtures Tested; native checker/reboot/restore open.

Objective: safe GRUB branding. Scope: active configuration evidence, minimal activation, owned theme and backups. Acceptance: preserved entries/arguments, validated output, boot and recovery in VM. Depends on F02/F06. Tests: independent GRUB VM, idempotency and restoration. Docs: boot compatibility and exact recovery.

## F08 — Limine adapter (Feature)

Status: Implemented 8–12 candidate; independent version/preservation fixtures Tested; reboot/restore open.

Objective: safe Limine branding; mandatory MVP. Scope: installed-version-supported settings, active-path validation and minimal edits. Acceptance: unchanged entries/arguments, VM boot and recovery. Depends on F02/F06; independent of F07. Tests: Limine-specific syntax where supported, VM and preservation. Docs: supported directives/versions and recovery.

## F09 — Plymouth with two generators (Feature)

Status: Implemented; simulated dispatch/archive/preview/kernel guards Tested; native generation/splash/restore open.

Objective: startup splash independent of loader. Scope: Qubix theme, dracut/mkinitcpio minimal integration and conditional rebuild. Acceptance: resources verified, both combinations boot/show splash, unrelated settings preserved and restore passes. Depends on F02/F06. Tests: two independent generator VM runs, reapplication and recovery. Docs: image selection, compatibility, recovery.

## T01 — MVP acceptance (Testing)

Status: In Progress; test machine available, SSH details pending. Next gate is native acceptance, not new adapter implementation.

Objective: complete scope evidence. Scope: end-to-end desktop/login/loader/splash, reapplication, configuration preservation, diagnostics and recovery. Acceptance: all [MVP criteria](scope.md) pass with recorded versions and evidence. Depends on F03–F09. Tests: disposable VM matrix. Docs: compatibility/status, release readiness and changelog.

## D01 — Human onboarding (Documentation)

Status: Implemented; links/syntax checked, VM walkthrough pending.

Objective: make the candidate usable/reviewable. Scope: operator/developer guides, target collector, recovery/checklist. Acceptance: desktop independent of boot, opt-ins/evidence clear. Depends on candidate contracts. Tests: static links, ShellCheck, collector help/controller refusal; native walkthrough pending. Docs: README/onboarding/status.
