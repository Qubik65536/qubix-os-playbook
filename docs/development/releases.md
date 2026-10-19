# Packaging and releases

Status: **Implemented; local static/archive/recovery checks Tested; remote Actions pending**. Focused task: distribute the complete committed playbook as a
source archive through CI artifacts and an explicitly triggered GitHub prerelease.
Acceptance: validation gates packaging/publication; the archive contains tracked roles,
playbooks, assets, licenses, tests and guides, preserves executable modes and records its
commit; ignored machine configuration/caches and Git history are excluded; checksums and
extracted-source state recording pass locally. Remote Actions/publication is a separate check.

## Contract

`scripts/package.sh [COMMIT]` archives `HEAD` by default with `git archive` and reproducible gzip headers.
It packages committed files only, even in a dirty checkout. Output is under ignored
`.cache/dist`: `qubix-os-playbook-COMMIT.tar.gz` and `SHA256SUMS`. The archive has one
matching top-level directory. `SOURCE_REVISION` uses Git export substitution to record
the full commit. No package downloads, compiled private clients, font cache, credentials,
local inventory or local overrides are bundled. This is the entire tracked playbook,
not an offline installation kit, operating-system image or backup of the target.

Git checkouts record revision and dirty status as before. Extracted archives record
`source_kind: archive`, the exported revision and `dirty: null`: without Git there is
no trustworthy dirty-tree comparison. A missing/malformed revision fails state recording.
The outer SHA256 verifies the downloaded package before extraction; it is not a signature.
Keep extracted sources unchanged and retain the checksum/revision with deployment evidence.
User deployment extracts and runs the archive directly on the destination machine;
SSH/controller deployment is reserved for [developer tests](ssh-testing.md).

## CI artifact

[Validate](../../.github/workflows/validate.yml) runs on push, pull request and manual
invocation, and is reusable by Release. After static checks, fixtures and the archive
smoke test pass, it uploads the tarball and `SHA256SUMS` as `qubix-os-playbook-SHA`
for 14 days. Download the artifact from the successful Actions run and unzip that
artifact container before following the [deployment guide](../user/deployment.md).
Artifacts are test candidates; passing controller CI does not establish native acceptance.

Local equivalent, after controller setup:

```bash
./scripts/validate.sh
./scripts/test.sh
./scripts/package.sh
bash tests/shell/package.sh
```

## Manual GitHub prerelease

Once these workflows are on the default branch, open **Actions → Release → Run workflow**.
Select the reviewed branch/tag and enter an unused prerelease tag such as `v0.1.0-rc.1`.
The selected source is validated again; a dependent job with `contents: write` packages
that exact commit and uses GitHub CLI to create its tag and prerelease with both files.
Inputs go through environment variables and tag-format validation. Existing remote tags
are rejected; existing releases are never overwritten. No personal token is needed.
Repository Actions policy must permit the job's write token.

The workflow always publishes a **prerelease**, never marks it latest, and includes the
source commit, changelog and native-acceptance caveat in its notes. This allows candidate
distribution while MVP gates are open. A stable MVP release still requires independent
GRUB/Limine and dracut/mkinitcpio acceptance, target/version evidence, recovery procedures
and a curated changelog. Stable publishing remains Planned.

Running the workflow is the publishing authorization. Adding it does not publish or tag
anything; no workflow is dispatched as part of this implementation. See the
[GitHub CLI release interface](https://cli.github.com/manual/gh_release_create).

## Local evidence (2026-10-18)

`./scripts/validate.sh` passes, including syntax, lint, ShellCheck, 82-document local-link
consistency/default agreement and 32 JavaScript cases. Existing local YAML and Limine
Jinja-spacing warnings remain unrelated to packaging. The extracted-source fixture
passes 12 tasks/four disposable changes, then rejects its malformed-revision control.
Contents, SHA256 and executable-mode checks pass. Git-source recovery/state regression
passes 233 tasks/18 disposable changes, with two expected rescued refusals. Shell-default
precedence passes too. Restricted local RPC required running the disposable Ansible
fixtures outside the sandbox; no target was contacted.

These establish file/state and parser/static behavior. No graphical session or boot
check is added, and no remote Actions execution or publication is claimed. Next:
authorized push, download/verify a successful CI artifact, then explicitly trigger and
inspect a candidate release when desired.
