# Remaining component contracts

All components here are **Planned**. [Component boundaries](../architecture/components.md) specify ownership and dependency relationships.

| Component | Concrete next requirement | Verification and restoration |
|---|---|---|
| Shell/terminal | Detect installed applications; additive Qubix defaults; `shell.enabled`; never automatically change login shell | Parser/application startup; personal-file checksums unchanged; remove named defaults or restore backed-up system integration |
| Login | Detect active manager; `login.enabled` and validated `backend`; supported theme hook only; no PAM/session changes or manager replacement | Actual login and Niri session startup; revert theme setting and backed-up resources |
| Packages/system | Only explicitly required companion packages/settings; Pacman remains native | Package evidence and application behaviour; document package removal separately from configuration restoration |
| State/recovery | Pre-change content, metadata, absence records; Git revision and effective-config digest after verification | Fault injection, conflict detection, repeated restoration; never remove unowned resources |

## Component design template

For a substantial new component, document purpose/responsibility, supported platforms, dependencies, options, owned/default/preserved resources, deployment order, verification evidence, restoration, limitations, and implementation status. Use a dedicated document when there is concrete design to review. Avoid creating empty roles or repetitive placeholders merely to mirror a diagram.
