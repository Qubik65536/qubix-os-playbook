# Git workflow

Use Issues and PRs for long-term collaboration. Bootstrap uses local planning documents and local commits; it does not need GitHub API writes.

Use `<type>(<optional-scope>): <description>` with feat, fix, docs, refactor, test, build, ci, chore, perf. Each commit represents one complete understandable change with related implementation, tests and documentation. Do not split required docs from code just to increase commit count.

Before committing inspect diff, stage only relevant files, run checks, inspect staged diff and whitespace. After committing verify its hash and message. Do not invent author identity, rewrite prior history, push, or tag during bootstrap. Leave unrelated work intact. PR descriptions explain the trigger and resulting behaviour, evidence, and real limitations.
