# Monaspace NF and Krypton UI test results

Status: **Implemented; controller fixtures, native rendering/installation, active shell and zero-change reapplication Tested**.
The [font contract](../components/fonts.md) owns scope and acceptance.

## Native comparison

2026-10-16, CachyOS Niri 26.04 (`8ed0da4`), Noctalia 5.3.0, native Pango and Fontconfig
2.18.3. The preview uses the installed private Qubix Noctalia client for both cases,
with the same managed configuration, palette and wallpaper. The only intentional
configuration difference is `shell.font_family`: the measured native Noto Sans baseline
versus `Monaspace Krypton NF`. Live hardware readings/time can change between captures.
Monaspace source: official v1.400, revision `f31794b6e9e65698a062262e2f826f679dcb7070`;
the [manifest](../../assets/fonts/monaspace-nf.yml) pins all exact file bytes.
The final native comparison uses clean source `d38d479`; the production
Noctalia template SHA256 is `0fac7dd93f88fa756a94ec5bf8844ec232095697e00767eaa6b29a8f84f981f7`.

These are **isolated native previews**, not live activation captures. Synthetic
`preview` identity, private state/cache, a private D-Bus and nested Niri exclude
personal content and authentication operations. The 1280-by-900 requested nested
window yields 1272-by-868 captures inside the parent frame. Actual font resolution,
warning-free native TOML parsing, distinct rendered images, preserved personal settings
and main compositor, and zero remaining preview processes pass. No real biometric,
power or boot action runs. Krypton's wider text changes line lengths and causes
native ellipsizing in fixed-width tiles; icons continue through font fallback.

| Surface | Generic reference | Krypton default |
|---|---|---|
| Launcher | ![Native Noto Sans launcher preview](../assets/fonts/launcher-reference.png) | ![Krypton NF launcher preview](../assets/fonts/launcher-krypton.png) |
| Control Center | ![Native Noto Sans Control Center preview](../assets/fonts/control-center-reference.png) | ![Krypton NF Control Center preview](../assets/fonts/control-center-krypton.png) |

## Controller and installation evidence

`./scripts/validate.sh` passes YAML, Ansible syntax/lint, shell checks, repository
consistency, JavaScript checks and diff whitespace. The framework fixture passes
827 tasks/zero changes with expected refusals; desktop ownership/version regression
passes 69 tasks/zero changes with seven expected refusals.

`tests/playbooks/fonts.yml` uses disposable synthetic font bytes and no-effect native
tools, independently of the large source download. Normal mode passes 313 tasks/33 disposable changes; global check mode passes 128
tasks/14 setup/cleanup changes, with one expected source refusal in each. They prove checksum
refusal, both Noctalia/Fontconfig selections, exact installation/verification,
unchanged reapplication and original-absence restoration. They do not prove native font validity.
`playbooks/prepare-fonts.yml` accepts the pinned archive and extracts the source;
all 210 manifest checksums match. The complete focused native plan passes 92 tasks,
zero changes, before installation. GTK defaults are additionally validated by strict
private schema compilation and a transient GSettings backend in the native workflow
(66 tasks, ten temporary changes; preserved main Niri/settings and zero leftover processes).
A focused native alias/orthography fixture passes six tasks/four temporary changes:
all four generic requests select Krypton while an explicit Noto Sans request retains Noto.
The aliases inherit matched binding strength; CLI probes escape hyphens because Fontconfig
pattern syntax otherwise parses `system-ui` as family `system` and a size suffix.
Future comparisons request the measured Noto Sans baseline explicitly, so installing the
system aliases cannot turn both comparison cases into Krypton.

## Deployment execution

The target uses a temporary user-owned controller checkout of exact clean `d38d479`,
Python 3.14.8 and the repository's pinned Ansible 2.21.5 runtime. It installs no native
system packages. Source and archive transfer/preparation are confined to a dedicated
`/tmp/qubix-font-controller.*` directory; the temporary environment and credential are
removed after acceptance; guarded cleanup passes five tasks and confirms the directory
is absent. The local temporary sudo-password file is also removed. Earlier serial runs are stopped before changing execution mode;
all first-baseline records and completed receipts are reused, with no overlapping attempts.

One bounded orchestration imports the unchanged production plan, begins one attempt,
then applies eight disjoint slices of the 210 `.otf` resources through the original
`qubix_files` role. The already-existing font/backup directories are shared; file and
baseline/receipt paths are unique to each worker. Every worker must complete before
any dependent defaults are applied. The remaining 31 ordered resources, original font
cache/parser verification and source/state recording run once on the coordinator.
The same procedure verifies unchanged reapplication. No loader, manager, package or
image task runs; virtual worker names schedule local file operations on the same
explicitly authorized target. The standard `deploy.yml` remains the serial production
entrypoint and uses these same component/file/cache/state tasks.

## Installed and running-session results

The resumed source deployment completes 4,375 tasks/411 changes across the coordinator
and eight disjoint file workers, zero failures. All 210 exact font files, license and
default fragments pass the shared engine's checksum/mode checks. Native `fc-validate`
accepts every face; exact Krypton Regular resolution, all four generic aliases and
strict GTK compilation/default selection pass. Production `verify.yml --tags installed`
passes 107 tasks/zero changes, including native Niri and warning-free Noctalia parsing.

A guarded Noctalia-only restart activates the installed defaults: PID 1193 becomes
159388 while Niri remains PID 1126. The helper verifies identical application-window
IDs/PIDs and personal configuration hashes, preserves the original GSettings caller
backend and confirms an unlocked visible bar. The effective merged Noctalia family is
`Monaspace Krypton NF`; the actual user's GTK UI and monospace settings both resolve to
`Monaspace Krypton NF 11`. The real installed count is 210. Boot ID remains
`dfd53a15-6435-468f-9b30-13f054fbf4c2`. Other already-running applications may need reopening.

Identical-source reapplication passes 4,238 tasks/zero changes and zero failures.
Both font-cache refresh and GTK schema compilation are skipped; installed native
validation/resolution still runs. The final read-only audit preserves all 85 protected
resources, the retired session entry, login shell and boot ID. All earlier original
backup bytes/metadata remain intact: 220 of the 221 earlier recovery files are identical,
with only the expected Noctalia configuration receipt refreshed. Exactly 426 new
font/default baseline/receipt files are added, for 647 total. Pending markers are absent,
and the deployment records clean source `d38d479` with the expected three components.

File installation, native parser validation, current-session activation and preservation
are Tested separately above. Native full-project restoration remains a separate VM gate;
the disposable font fixture proves original-absence restoration without touching the host.
Next: optional native font/default restoration acceptance and application-specific font
preference checks. The configured defaults retain saved user choices.
No boot check is required for desktop fonts; boot font/image selections are preserved.
