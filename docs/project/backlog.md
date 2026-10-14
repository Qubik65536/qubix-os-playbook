# Backlog

Local bootstrap planning; later mirror substantial tasks to GitHub Issues. Categories: Feature, Bug, Documentation, Refactor, Testing, Maintenance. Dependencies are explicit; this is not a duplicate roadmap.

## F01 — Read-only foundation (Feature)

Status: Implemented; fixture contracts Tested. Live CachyOS collection acceptance remains open.

Objective: safely inspect CachyOS Niri and resolve the profile. Scope: schema, read-only evidence, compatibility, verify/deploy preflight, minimal wrapper. Acceptance: supported fixtures pass; unsupported hosts, malformed inputs and planned enabled components fail before writes; ambiguities remain unresolved. Depends on documentation. Tests: real Ansible fixture runs, macOS rejection, syntax/lint. Docs: configuration, deployment, compatibility, status.

## M01 — Tooling and CI (Maintenance)

Objective: repeatable local/CI checks. Scope: pinned controller dependencies, YAML/Ansible/ShellCheck/Markdown consistency checks and Actions. Acceptance: local commands and workflow agree; checks pass. Depends on documentation. Tests: execute available validators and record missing tools explicitly. Docs: environment/testing/installation.

## F02 — Shared artwork (Feature)

Objective: first useful safe mutation. Scope: canonical Qubix assets, attribution/checksums, fixed destination files, read-only verification. Acceptance: isolated install/checksum/idempotency/preview tests, unrelated files preserved, no identity changes. Depends on F01/M01. Tests: temporary filesystem, corruption and absence failures. Docs: branding, restoration and status.

## F03 — CachyOS Niri default activation (Feature)

Objective: begin a usable Qubix desktop on an actual target. Scope: live report, supported KDL candidate, theme include, detected companion commands and preservation policy. Acceptance: `niri validate`, user/system originals preserved, actual wallpaper/launcher/bar/notifications/terminal work in VM, second run unchanged. Depends on F02 and live VM evidence. Tests: parser + preservation + VM graphical session. Docs: Niri, compatibility, user deployment and recovery.

## F04 — Shell/terminal defaults (Feature)

Objective: Qubix terminal experience. Scope: detected applications and additive defaults, no automatic shell change. Acceptance: working terminal/shell with personal files preserved. Depends on F03 target evidence. Tests: parsing/startup/idempotency. Docs: component ownership and user override/recovery.

## F05 — Login theme (Feature)

Objective: brand supported active manager without changing authentication/session. Scope: detected manager's supported theme hooks only. Acceptance: login and Niri startup succeed, PAM unchanged, restoration tested. Depends on F03. Tests: VM login and revert. Docs: manager/version support and recovery.

## F06 — Revision state and recovery (Feature)

Objective: auditable resource-level restoration. Scope: manifests, backups before existing-default mutation, original absence/metadata, revision/config digest and dirty detection. Acceptance: success state only after verify; conflict-safe repeated restoration and interrupted failure diagnosis. Depends on F01; needed before default/boot activation. Tests: fault injection, restore and preservation fixtures. Docs: lifecycle/restoration.

## F07 — GRUB adapter (Feature)

Objective: safe GRUB branding. Scope: active configuration evidence, minimal activation, owned theme and backups. Acceptance: preserved entries/arguments, validated output, boot and recovery in VM. Depends on F02/F06. Tests: independent GRUB VM, idempotency and restoration. Docs: boot compatibility and exact recovery.

## F08 — Limine adapter (Feature)

Objective: safe Limine branding; mandatory MVP. Scope: installed-version-supported settings, active-path validation and minimal edits. Acceptance: unchanged entries/arguments, VM boot and recovery. Depends on F02/F06; independent of F07. Tests: Limine-specific syntax where supported, VM and preservation. Docs: supported directives/versions and recovery.

## F09 — Plymouth with two generators (Feature)

Objective: startup splash independent of loader. Scope: Qubix theme, dracut/mkinitcpio minimal integration and conditional rebuild. Acceptance: resources verified, both combinations boot/show splash, unrelated settings preserved and restore passes. Depends on F02/F06. Tests: two independent generator VM runs, reapplication and recovery. Docs: image selection, compatibility, recovery.

## T01 — MVP acceptance (Testing)

Objective: complete scope evidence. Scope: end-to-end desktop/login/loader/splash, reapplication, configuration preservation, diagnostics and recovery. Acceptance: all [MVP criteria](scope.md) pass with recorded versions and evidence. Depends on F03–F09. Tests: disposable VM matrix. Docs: compatibility/status, release readiness and changelog.
