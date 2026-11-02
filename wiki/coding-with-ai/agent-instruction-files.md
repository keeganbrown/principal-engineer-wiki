---
title: Agent Instruction Files
category: coding-with-ai
summary: Give coding agents a short, version-controlled briefing file in the repository — commands, conventions, and hard rules — and maintain it like code, because the agent rereads it every session and remembers nothing else.
tags: [ai, coding-agents, documentation, onboarding]
---

# Agent Instruction Files

> **In one sentence:** Give coding agents a short, version-controlled briefing file in the repository — commands, conventions, and hard rules — and maintain it like code, because the agent rereads it every session and remembers nothing else.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. Unlike a human teammate, it starts every session with no memory of the last one ([[large-language-models]] explains why). Whatever it knows about *your* project, it learns from what's in front of it.

An **agent instruction file** is a Markdown file in the repository that the agent loads automatically at the start of each session. Think of it as the onboarding note you'd give a capable contractor on day one: how to build and test, where things live, which conventions matter, and what never to do.

The common names are `AGENTS.md`, an open convention many tools read (now stewarded by the Linux Foundation's Agentic AI Foundation), and tool-specific files such as Claude Code's `CLAUDE.md`. The idea matters more than the file name.

## Why it matters

- **Agents repeat the same mistakes without it.** Each session rediscovers that tests need a flag, or that one folder is generated code. A two-line note fixes that for everyone.
- **It makes team conventions explicit.** Most teams carry their rules in people's heads. Writing them for an agent forces the team to agree on them, and new humans benefit too.
- **Everyone's agent behaves the same way.** One shared, reviewed file beats ten personal prompt habits, each with different rules.
- **Watch whether it tracks cleaner agent code.** A 2026 Stanford and Carnegie Mellon study of 509 repositories found commit volume rose about a third after agent adoption, whether or not the repository had committed agent configuration, such as an instruction file. In agent-heavy repositories, code complexity, as scored by a static-analysis tool, rose about 27% with that configuration versus 53% without. It's observational: disciplined teams may simply write these files more often, and the authors treat it as a hypothesis to test.

The limit: an instruction file is *advice*, not enforcement. The agent usually follows it, but nothing guarantees that. Rules that must hold belong in tools — tests, linters, type checks, permission settings — where breaking them fails loudly.

## How to apply it

- **Lead with the commands.** Exact build, test, lint, and run commands come first. An agent that can check its own work does far better than one that can't ([[feedback-loops-for-agents]]).
- **Write what the code can't tell you.** Skip what the agent can read from the code itself. Include the non-obvious: "the `legacy/` folder is frozen," "money is always integer cents," "never edit generated files in `api/gen/`."
- **Keep it short.** The whole file is sent to the model in every session and uses up part of its limited working memory (its *context window*, see [[large-language-models]]), so a long file buries the rules that matter. If you'd struggle to read it aloud in five minutes, cut it.
- **Put rules near the code they govern.** Most tools also read instruction files in subfolders. Keep the root file general and put "how the payments module works" in `payments/` ([[navigable-codebases]]).
- **Review changes to it like code.** It shapes every agent-written change in the repository, so it goes through pull requests (PRs), with an owner.
- **Turn repeated corrections into lines.** When you correct the agent for the same thing twice, add a line. When a rule could be checked by a tool, move it to the tool and delete the line.
- **Prune when behavior goes wrong.** Contradictory or stale instructions are a common cause of odd agent behavior. Read the file before you blame the model.

## Example

A team's first `AGENTS.md` is 400 lines pasted from its wiki: architecture history, a style guide, onboarding links. Agents ignore half of it, and nobody can say which half.

They rewrite it to about 40 lines:

```
## Commands
- Test: make test        # ~20s; run after every change
- Lint + types: make check
- One test: make test ARGS="-k name"

## Rules
- Money is integer cents (type Cents). Never use floats for money.
- Don't edit api/gen/ — run `make codegen` instead.
- New endpoints need a contract test (see tests/contracts/README.md).

## Where things live
- Domain logic: core/   (no input/output imports — make check enforces it)
- Adapters: adapters/   (database, HTTP, queue)
```

The style guide moves into the linter config, so it's enforced rather than requested. Two months later, a new lint rule catches floats for money, and the line shrinks to a pointer: "floats for money fail `make check`" — so the agent learns the rule before writing code, not after a failed check. The hard part is keeping it this short as people add "just one more" rule; the team reviews the file each quarter and cuts as much as it adds.

## Common traps

- **Writing an essay.** Long files dilute every rule. Link to deeper docs instead of pasting them.
- **Treating it as enforcement.** "Always run the tests" in a file is a hope. A CI (continuous integration) check that fails without tests is a guarantee.
- **Letting it rot.** A file that names a command you renamed last month teaches the agent wrong things with confidence. The Stanford and Carnegie Mellon study found about three-quarters of committed agent configuration files were never edited after their first commit, within its roughly 14-month window. Give it an owner and touch it when the build changes.
- **Personal files for team rules.** Rules that only live in one person's local config split the team into different behaviors. Shared rules go in the shared file.
- **Putting secrets or private data in it.** It's checked into the repository and sent to the model every session.

## When it doesn't apply

For a throwaway script or a solo spike, a file is overhead — tell the agent what it needs in the prompt. And an instruction file can't rescue a codebase with no tests and no clear structure: it can describe the mess, but the agent still has nothing to check its work against. Fix the feedback loop first.

## Related

- [[feedback-loops-for-agents]] — the commands at the top of this file only help if they're fast and trustworthy.
- [[adopting-coding-agents]] — the shared instruction file is part of how a team aligns.
- [[architecture-decision-records]] — instruction files say *what* the rule is; architecture decision records (ADRs) record *why*.
- [[paved-roads]] — a good instruction file is a paved road for agents.
- [[agent-guardrails]] — what to enforce with permissions instead of instructions.
- [[shared-agent-configuration]] — hooks and permissions enforce what this file can only ask for.
