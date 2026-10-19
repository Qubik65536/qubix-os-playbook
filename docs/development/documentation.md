# Documentation maintenance

Design precedes substantial features. Small bug fixes and mechanical edits need no new design document, but affected behavioural documentation still changes with the fix.

Authoritative locations: scope for acceptance; architecture for interfaces/ownership; component pages for responsibilities and restoration; user pages for executable procedures; status for actual evidence; backlog for next actions; ADRs for consequential rationale. Link rather than duplicate contracts.

Use Planned, In Progress, Implemented, Tested, Deprecated. Specify the level of testing. Proposed commands must be labelled separately from executable commands. Update status after significant functionality, and remove stale claims. Every Markdown file must have a purpose; templates do not justify filler pages.

Review local links, examples, default values, safety language, MVP requirements, and current commands before each logical commit. Preserve ADR history; supersede a decision when it changes materially.

User onboarding starts at `docs/user/getting-started.md` and runs playbooks directly
on the destination machine with `inventory/local.ini`, as the desktop account with
task-scoped sudo. Developer onboarding starts at `docs/development/getting-started.md`;
controller setup, SSH access, remote VM execution and fixture development live there.
Keep historical remote test evidence intact, but do not turn it into user deployment
instructions. See the [deployment contract](../architecture/deployment.md#user-deployment-and-developer-transport).
