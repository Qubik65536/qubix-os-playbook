# Development environment

Status: **Implemented controller setup**. Requires jq on PATH for output-default fixtures and Python 3.12+ for the pinned Ansible controller. Target Python support follows the pinned ansible-core requirements. No Python application is deployed.

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

`ansible.cfg` sets the explicit local inventory and roles path; run from the root so it is loaded. Host-key checking stays enabled. No automatic `sudo`, target package installation, or privilege escalation occurs during tooling setup.

Use an existing CachyOS Niri disposable VM for live inspection and later desktop tests. macOS can run controller/static/fixture tests but cannot prove graphical or boot behaviour. [Testing](testing.md) lists equivalent local validation commands.
