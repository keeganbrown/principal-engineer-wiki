---
title: Shared Agent Configuration
category: coding-with-ai
summary: Check the team's coding-agent setup — permissions, automatic hooks, reusable commands, and tool connections — into the repository and review it like code, while keeping personal preferences and secrets out of it.
tags: [ai, coding-agents, configuration, hooks, team-practices]
---

# Shared Agent Configuration

> **In one sentence:** Check the team's coding-agent setup — permissions, automatic hooks, reusable commands, and tool connections — into the repository and review it like code, while keeping personal preferences and secrets out of it.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. Beyond the instruction file that briefs it ([[agent-instruction-files]]), most agents can be configured in four more ways:

- **Permissions** — which commands and file paths the agent may use without asking, must ask about, or may never touch.
- **Hooks** — scripts that run automatically at fixed points, such as after every file edit or before a command runs. Unlike instructions, hooks always fire.
- **Reusable commands** — saved prompts or workflows the team invokes by name ("review this PR against our checklist," "write a migration"). Tools call them commands, skills, or recipes.
- **Tool connections** — extra tools the agent can call, such as an issue tracker, a database browser, or internal docs, often through the Model Context Protocol (MCP), an open standard for plugging tools into AI applications.

Each of these changes what every engineer's agent does. Left on individual laptops, they drift apart. Checked into the repository, they become a shared, reviewed team setup. Most tools support exactly this split: a project file that's committed and a personal file that's ignored by Git. In Claude Code, for example, these are `.claude/settings.json` and `.claude/settings.local.json`, with project tool connections in `.mcp.json`.

## Why it matters

- **It turns good habits into defaults.** One engineer's useful hook or command helps everyone the moment it's merged.
- **Hooks enforce what instructions only request.** "Run the formatter after editing" in an instruction file is followed most of the time. A hook that runs the formatter after every edit runs every time.
- **Review catches risky changes.** A permission that allows `git push`, or a new tool connection with database access, is a security decision. In the repository, it goes through a pull request (PR) like any other.
- **Behavior becomes explainable.** When an agent does something odd, the team can read the shared configuration instead of comparing ten private setups.

The cost: shared configuration is code to maintain. Hooks can slow every edit or break in confusing ways, and each tool connection is another dependency with its own risks.

## How to apply it

- **Split team settings from personal ones.** Team rules go in the committed file; personal preferences, experiments, and anything with credentials go in the ignored file. Never commit secrets — reference environment variables instead.
- **Use hooks for anything that must always happen.** Formatting after edits, blocking edits to generated files, running a fast lint before the agent stops. Keep each hook fast and give it a clear error message, since the agent reads that message ([[feedback-loops-for-agents]]).
- **Save repeated workflows as commands.** If people keep typing the same multi-step prompt, save it in the repository with a name. Write it like a short runbook, and review changes to it.
- **Vet tool connections like dependencies.** Prefer official or internally built servers, pin their versions, and give each the narrowest access it needs. Tool descriptions and tool output are untrusted input — a malicious or compromised server can use them to inject instructions ([[agent-guardrails]]).
- **Give it an owner and a changelog.** Someone reviews changes to the agent setup. Note why each hook or permission exists, so it can be removed safely later.
- **Prune regularly.** Every hook, command, and connection costs speed and attention. Delete the ones nobody uses.

## Example

A team notices three recurring problems in agent PRs: unformatted files, edits to generated API clients that get overwritten on the next build, and agents running the full 10-minute integration suite after every small change.

They add to the shared configuration:

```
hooks:
  afterEdit:   run "make fmt" on the edited file
  beforeEdit:  block paths under api/gen/ with message
               "Generated code. Edit api/schema.yaml, then run make codegen."
permissions:
  allow: make test, make check, git status, git diff
  ask:   make integration, git push
  deny:  reading .env files
commands:
  /new-endpoint: steps for adding an endpoint, its contract test, and docs
```

The formatting complaints in review stop the week the hook is merged. Edits to generated code stop too, and the block message teaches the agent the right workflow. The cost shows up later: the format hook adds a second to every edit, and when the formatter is upgraded, a version mismatch breaks the hook for everyone until someone fixes it. The team adds the hook scripts to CI so breakage shows up in one place.

## Common traps

- **Committing personal preferences.** One person's favorite permissions become everyone's. Keep the shared file to rules the team agreed on.
- **Secrets in shared configuration.** Tokens for tool connections belong in each person's environment or a secrets manager, never the repository.
- **Hook sprawl.** Ten slow hooks make every edit sluggish, and people start disabling them. Keep hooks few, fast, and focused.
- **Installing tool connections casually.** A connection that can read your database and the internet at once recreates the risky combination guardrails try to prevent.
- **Duplicating rules in three places.** If a rule is in the instruction file, a hook, *and* the linter, they'll drift. Enforce it in one place and mention it in at most one other.

## When it doesn't apply

A solo project or a short spike doesn't need shared configuration — personal settings are fine until a second person joins. And if a team uses several different agent tools, there may be no shared format for hooks and commands. Then keep the rules in tool-neutral places — the linter, CI, scripts in the repository — and keep each tool's config a thin wrapper around them.

## Related

- [[agent-instruction-files]] — the advice layer; this article covers the enforcement and automation layer.
- [[agent-guardrails]] — permissions and sandboxing in depth.
- [[reproducible-dev-environments]] — the environment the configuration runs in.
- [[adopting-coding-agents]] — shared setup is how a team's agreement becomes real.
- [[paved-roads]] — make the shared setup the easiest one to use.
