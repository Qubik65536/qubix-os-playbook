# Repository conventions

Definitions live under `config/`, deployments under `playbooks/`, and ordinary Ansible roles under `roles/`. Shared imported artwork lives in `assets/` with provenance and licenses. Tests live under `tests/`; small shell helpers under `scripts/`. Do not populate empty role/adapter directories.

YAML uses two spaces, document starts, explicit booleans, and quoted file modes. Ansible tasks have descriptive names, FQCN modules, narrow responsibilities, and explicit command change/failure semantics. Variables use a `qubix_` prefix; internal role facts use the role prefix. Avoid handler-triggered boot operations unless inputs, validation, and authorization are explicitly designed.

Use Jinja2 only for genuine parameterization. Prefer copy for static content, argv for commands, and built-in modules over shell pipelines. Comments explain rationale or safety boundaries. Unknown configuration keys and unsupported capabilities fail explicitly.

English Markdown is required. Paths, commands, statuses, and ownership must match the implementation. [Documentation maintenance](documentation.md) defines updates.
