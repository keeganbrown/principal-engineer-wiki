---
title: Agent Guardrails
category: coding-with-ai
summary: Give coding agents the least access that gets the job done, enforce limits with sandboxes and permissions rather than instructions, and assume anything the agent reads could be trying to steer it.
tags: [ai, coding-agents, security, least-privilege, prompt-injection]
---

# Agent Guardrails

> **In one sentence:** Give coding agents the least access that gets the job done, enforce limits with sandboxes and permissions rather than instructions, and assume anything the agent reads could be trying to steer it.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. It runs with whatever access *you* have: your files, your shell, your cloud credentials. That makes it both useful and dangerous. It can delete the wrong folder, run a migration against the wrong database, or follow instructions hidden in a web page it was asked to read.

**Guardrails** are the limits placed *around* the agent, so that its mistakes stay small. They come in two layers that do different jobs:

- **Permissions** — decide what the agent is allowed to *try*: which commands run without asking, which need your approval, which are denied.
- **Sandboxing** — limits what an attempt can *reach*: which files it can see, which network hosts it can call. If something tricks the agent into trying something bad, the sandbox stops it from working.

The key threat is **prompt injection**: text in the agent's input — a README, an issue comment, a web page, a dependency's docs — that the model reads as instructions. Simon Willison, who coined the term in 2022, later (2025) named the **lethal trifecta**: an agent with access to private data, exposure to untrusted content, and a way to send data out (a web request, a pushed commit, a comment on a public issue) can be tricked into leaking that data. Remove any one of the three and the leak path closes.

## Why it matters

- **Instructions are not limits.** "Never touch production" in an instruction file is a request the model will usually honor. A sandbox with no production credentials is a guarantee.
- **Agent mistakes happen at machine speed.** A human hesitates before `rm -rf`. An agent in a loop runs the command and moves on.
- **Untrusted content is everywhere in coding work.** Issues, dependencies, logs, and docs are written by strangers. An agent that reads them and also holds your secrets is an attack surface.

## How to apply it

- **Start restrictive and widen on evidence.** Allow read-only commands and your test and lint commands by default. Require approval for anything that installs, deletes, pushes, or deploys. Widen only when the approval requests are clearly noise. Remember that allowing `make test` allows whatever the agent writes into the tests and the Makefile: the allow list cuts down interruptions, and only the sandbox actually limits damage.
- **Run unattended agents in a sandbox.** Fully autonomous runs belong in a container or virtual machine where the repository is the only part of your machine it can see, with no production credentials and with network access limited to what the task needs.
- **Break the trifecta deliberately.** If the agent must read untrusted content, keep secrets out of its environment *or* cut its outbound network. Don't hand all three to one session. This is hard: for most coding agents the private repository *is* the private data, and an allowlisted host such as a package registry can still carry data out. Treat a network allowlist as narrowing the leak path, not closing it, and keep what's at stake small.
- **Keep production credentials away from agents.** Agents work against development and test environments. Changes reach production through the same reviewed pipeline as human changes.
- **Make tests safe to run by anyone, including an agent.** Code that deletes files, runs shell commands, or calls paid APIs gets a **fake** or **spy** in tests — a stand-in that records the call instead of doing it ([[hexagonal-architecture]]).
- **Check permission settings into the repository.** Team-wide allow and deny rules belong in version control, reviewed like code, so every engineer's agent has the same limits ([[shared-agent-configuration]]).
- **Keep an audit trail.** Log what agents ran and changed, especially in shared or CI (continuous integration) environments, so you can reconstruct what happened.

## Example

An engineer is test-driving a cleanup feature with an agent. The agent writes a failing test first, as asked — but the test calls the real file-deletion function, and a bug in the path argument makes it resolve to the user's home directory. The agent runs the test suite, as it should. The test deletes files before anyone reads it.

The agent wasn't malicious; it followed good practice. The failure was that a test could do real damage, and that the agent ran with full access to the home directory.

The team adds three guardrails:

- **Destructive operations go through an interface.** File deletion and shell execution sit behind a small interface (a *port*); tests inject a spy that records "would delete X" and asserts on that.
- **Agents run in a sandbox scoped to the repository.** Even a bad path can't reach the home directory.
- **A permission rule asks before deleting files outside the repository.** It's a backstop, not the main defense.

Each guardrail has a cost: the port is one more abstraction, the sandbox blocks some legitimate tools until it's configured, and the prompts slow the agent down — small costs next to losing a home directory.

## Common traps

- **Approving every prompt on autopilot.** By the fiftieth "allow this command?" people click yes unread. Too many prompts is a guardrail failure; fix the allow list.
- **Running "skip all permissions" mode on your laptop.** In that mode the agent runs every command without asking. Full autonomy is reasonable inside a disposable sandbox and reckless on a machine with your credentials.
- **Trusting the agent to spot injection.** Models resist injected instructions better each year, but none does so reliably. Design as if the injection works.
- **Secrets in the agent's environment variables.** Anything in the agent's own shell environment can end up in its output, its logs, or a request it makes. Credentials for a tool connection belong in that tool's process or a secrets manager, where the agent can use the tool without reading the token ([[shared-agent-configuration]]).
- **Guardrails only on laptops.** Agents in CI pipelines, review bots, and scheduled jobs need the same limits, often stricter, because nobody is watching them live.

## When it doesn't apply

A disposable environment with nothing valuable in it — a fresh container, a scratch repository, no credentials — can safely run an agent with few limits; the sandbox *is* the guardrail. And for a small personal project with no secrets, a few deny rules on destructive commands may be enough. Scale the guardrails to what the agent can reach.

## Related

- [[agent-instruction-files]] — for advice; guardrails are for rules that must hold.
- [[hexagonal-architecture]] — ports make destructive operations swappable for fakes in tests.
- [[reviewing-ai-generated-code]] — the human check on what the agent produced.
- [[paved-roads]] — a shared, pre-configured sandbox is the easy, safe default.
- [[blameless-postmortems]] — when an agent causes damage, fix the system that allowed it.
- [[reproducible-dev-environments]] — a container-defined environment makes the sandbox easy.
- [[large-language-models]] — why models can't reliably tell instructions from data.
