# Development environment

Status: **Implemented controller setup**. Requires jq on PATH for output-default fixtures and Python 3.12+ for the pinned Ansible controller. Target Python support follows the pinned ansible-core requirements. No Python application is deployed.

Fingerprint controller fixtures require Node.js 20+ on the controller (`node --test`). The
target application uses GJS/GTK 4 and fprintd; Node is never installed on a target by Qubix.

From the repository root, create local tooling using uv (if installed):

```bash
python3 -m venv .venv
UV_CACHE_DIR=.cache/uv uv pip sync --python .venv/bin/python requirements-dev.txt
source .venv/bin/activate
ansible-playbook --version
ansible-lint --version
yamllint --version
shellcheck --version
jq --version
```

Alternatively use `python3 -m venv .venv` and `.venv/bin/python -m pip install -r requirements-dev.txt`. `shellcheck-py` supplies the ShellCheck binary without installing system packages. `requirements-dev.in` pins direct tooling; `requirements-dev.txt` locks transitive dependencies. Update intentionally with `UV_CACHE_DIR=.cache/uv uv pip compile --python .venv/bin/python requirements-dev.in -o requirements-dev.txt` and rerun all checks. `requirements.yml` records that no external Ansible collection is needed.

Power-panel fixtures also require the controller-only [Luau 0.742 CLI](https://github.com/luau-lang/luau/releases/tag/0.742).
Put `luau` on PATH, extract it to `.cache/luau/luau`, or set `LUAU_BIN` to its executable path.
CI downloads the versioned Ubuntu archive and verifies its SHA256; the locally tested macOS archive
has SHA256 `bdd415766fbe03bc090b65fa6141531a4a54608db95a5350a5a0b49862bdac83`.
This interpreter is never installed on a target; Noctalia supplies the production plugin runtime.

`ansible.cfg` sets the explicit local inventory and roles path; run from the root so it is loaded. Host-key checking stays enabled. No automatic `sudo`, target package installation, or privilege escalation occurs during tooling setup.

Use an existing CachyOS Niri disposable VM for live inspection and later desktop tests. macOS can run controller/static/fixture tests but cannot prove graphical or boot behaviour. [Testing](testing.md) lists equivalent local validation commands.
