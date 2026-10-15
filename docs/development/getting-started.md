# Get started as a human developer

This guide assumes you want to understand, change and test Qubix OS Playbook. You need Git, Python 3.12+ and basic Ansible/YAML familiarity. A Linux VM is necessary for native desktop/boot acceptance; macOS is a supported controller for repository checks.

## Set up a checkout

Use the existing local checkout for this candidate; its commits have not been pushed. Once published, ordinary Git cloning is sufficient. Work from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
source .venv/bin/activate
./scripts/validate.sh
./scripts/test.sh
```

If uv is installed, the [environment guide](environment.md) provides a locked sync command. The repository needs no external Ansible collections. Scripts prefer `.venv/bin` and put caches/logs in ignored `.cache`. Avoid system-wide pip installation. The complete fixture suite takes several minutes and requires local Ansible IPC; restricted execution environments may need approval.

Read [CONTRIBUTING](../../CONTRIBUTING.md), [AGENTS](../../AGENTS.md), [status](../project/status.md), [architecture](../architecture/overview.md) and the component document relevant to your task. Pick an acceptance criterion from the [backlog](../project/backlog.md); do not implement Fedora/KDE ahead of CachyOS acceptance.

## Follow a deployment through the code

| Path | What to read/change |
|---|---|
| `config/defaults.yml`, `config/profiles/cachyos-niri.yml` | Default options and profile overrides |
| `roles/qubix_profile/` | Allowlisted schema, types, merge order and safety restrictions |
| `roles/qubix_discovery/`, `config/platforms/cachyos.yml` | Read-only native evidence and classification |
| `playbooks/tasks/plan.yml` | Prerequisites, ordered per-component resource definitions |
| `roles/qubix_niri/`, `roles/qubix_shell/` | Desktop templates and additive shell defaults |
| `roles/qubix_login/` | Active SDDM source cloning and precedence checks |
| `roles/qubix_bootloader/tasks/` | Independent ordinary GRUB/Limine adapter task files |
| `roles/qubix_plymouth/tasks/` | Generator preparation, conditional regeneration and archive checks |
| `roles/qubix_files/` | Path guards, original baselines, atomic copy validation, receipts and restore |
| `roles/qubix_state/` | Pending/failure diagnostics and last-success revision/configuration digest |
| `playbooks/`, `bootstrap.sh` | Public verify/deploy/restore orchestration |

Component roles normally prepare a list of named resources rather than writing directly. A resource has a logical absolute path, component name, content or source, and optional mode/checksum/native validation. The shared file engine owns safe reconciliation and restoration. Plymouth-generated images are exceptional resources: back them up before native generation and record receipts only after archive verification.

Native system/user configuration remains Preserved unless a documented narrow change is necessary. The separate Qubix Niri session is deliberate: explicit session selection grants consent without overwriting dotfiles. Enabled unsupported combinations fail before component writes.

## Make a focused change

1. State the problem, scope and observable acceptance criteria. Update substantial design/interface documentation first.
2. Implement one coherent component or adapter change with ordinary Ansible; use FQCN modules, named tasks, explicit modes and justified probes.
3. Add meaningful tests for failure handling, preservation or behaviour changes. Simple mechanical fixes need appropriate existing checks, not mirror-image tests.
4. Run focused tests, then the shared validation commands. Keep documentation, CHANGELOG, status and backlog accurate in the same logical commit.
5. Inspect the diff and stage only the related files. Use a Conventional Commit; do not push, amend history or tag without authorization.

For example, changing a Niri binding needs a valid KDL candidate and its user-visible description. Changing backup semantics needs fault/restore fixtures. A boot change needs adapter-specific VM acceptance before being called Tested on a real platform.

## Understand test evidence

`./scripts/validate.sh` runs YAML lint, production Ansible lint, entry/fixture syntax checks, ShellCheck, basic Markdown/local-link checks, profile/default/schema consistency, imported asset hashes and whitespace checks.

`./scripts/test.sh` runs production roles against synthetic evidence and isolated filesystem roots under `.cache/tests`. It covers profile rejection, identity/discovery, branding preview/reapplication, backups/drift/restoration/failure state, desktop definitions, SDDM cloning, both loader plans, both image-generator dispatches, incomplete rebuilds, kernel-aware restore and Plymouth no-write preview.

Plymouth fixtures use **fake executable tools** and fake archive listings. They prove orchestration and guards, not a real initramfs. Desktop fixtures do not run the native Niri/Foot/Noctalia parsers. All fixtures must avoid actual host `/etc`, `/boot` and personal configuration. Logs identify expected rescued failures; unexpected failures stop the suite. See [testing](testing.md).

For a focused run:

```bash
mkdir -p .cache/tests
ansible-playbook tests/playbooks/desktop.yml
ansible-playbook tests/playbooks/login.yml
ansible-playbook tests/playbooks/bootloader.yml
ansible-playbook tests/playbooks/plymouth.yml
ansible-playbook tests/playbooks/plymouth-preview.yml --check
```

## Test on the VM

Follow the [user getting-started guide](../user/getting-started.md), and collect [target evidence](../user/collecting-target-info.md) first. Keep host inventory and overrides ignored. Never run boot deployment against the development controller.

Test desktop first. Capture native parser output, preserved-file checksums, actual companion behaviour and the second deployment recap. With Noctalia/Foot installed and a main Niri compositor running, the optional native smoke workflow renders the production candidates into temporary paths, opens a nested window and saves evidence without changing the main session. Direct SDDM launches and user-service launches are supported:

```bash
ansible-playbook tests/integration/niri.yml -i inventory/target.local.ini -e @config/local.yml --ask-pass --ask-become-pass
ansible-playbook tests/integration/desktop.yml -i inventory/target.local.ini -e @config/local.yml --ask-pass --ask-become-pass
```

Omit --ask-pass with SSH keys. Include qubix_discovery_privileged: true in local overrides for private /boot metadata. See the [test contract and limits](testing.md). Then test supported SDDM without changing authentication. Both already-installed GRUB and Limine need independent VM boot/restoration tests, and both dracut and mkinitcpio need native generation/splash/restoration evidence. Snapshots allow recovery without pretending file restoration is whole-system rollback.

Record target versions, exact Git revision/configuration, commands, results and failures in project status/compatibility. A candidate is implemented and ready to test; an accepted MVP satisfies the entire [scope](../project/scope.md). Do not turn fixture success into a compatibility claim.

## Collaborate and release

Use local planning documents during bootstrap, then GitHub Issues/PRs when collaboration is enabled. A substantial issue specifies objective, scope, acceptance criteria, dependencies, required tests and documentation changes. Keep review descriptions focused on the final behaviour and relevant validation.

[Git workflow](git-workflow.md), [adding components](adding-components.md), [adding adapters](adding-adapters.md), [documentation maintenance](documentation.md) and [release process](releases.md) define the next steps. Release tags require the acceptance matrix and explicit authorization.
