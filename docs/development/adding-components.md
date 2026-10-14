# Adding a component

Start from the [component design template](../components/remaining.md). Declare ownership and activation/restoration behaviour. Define dependencies and schema keys before implementing. Add defaults conservatively; planned components must not silently execute or appear supported.

Implement one coherent role using built-ins and explicit modes. Discovery and profile validation run before mutation. Keep checks usable without writes. Update orchestration, the capability allowlist, schema validation, tests, component/user documents, changelog, status, and backlog in the same logical change.

Acceptance must include actual application behaviour where needed, idempotency and preservation, not merely task success. Boot-critical components use VM evidence.
