# Agent Instructions

Routing: Read this file fully before repo changes to find the canonical instruction discovery path and load-report requirements.

Load repository instructions from `.github/agent_instructions/` before
making code, documentation, data-layout, or Git changes in this repo.
Before making changes, report the instruction files read for this task.

## Discovery Paths

Generic repo-first agents should start here:

```text
AGENTS.md
  -> .github/agent_instructions/agent.md
  -> .github/agent_instructions/README.md
  -> .github/agent_instructions/global/README.md
  -> .github/agent_instructions/repo/README.md
  -> task-relevant instruction files
```

GitHub Copilot may start from its platform-specific entrypoint:

```text
.github/copilot-instructions.md
  -> AGENTS.md
  -> .github/agent_instructions/agent.md
  -> .github/agent_instructions/README.md
  -> .github/agent_instructions/global/README.md
  -> .github/agent_instructions/repo/README.md
  -> task-relevant instruction files
```

Both paths must converge on the same instruction tree and explicit load
order.

## Canonical Load Order

1. `.github/agent_instructions/agent.md`
2. `.github/agent_instructions/README.md`
3. `.github/agent_instructions/global/README.md`
4. `.github/agent_instructions/repo/README.md`
5. Task-relevant files referenced by those indexes

## Routing Sentences

Instruction files may begin with a `Routing:` sentence. Agents should
use routing sentences to decide which optional task-relevant files need
full loading, while still fully loading the canonical files above before
repository changes.

## Layer Model

- `global/`: reusable guidance shared across local repositories
- `repo/`: repository-specific context, boundaries, and constraints

Global guidance supplies default decision rules. Repo guidance supplies
local facts and constraints that shape or override those defaults.
