---
title: Feedback Loops for Agents
category: coding-with-ai
summary: Coding agents are only as good as the feedback your codebase gives them, so invest in fast, trustworthy checks — tests, types, linters — that tell an agent within seconds whether its change is right.
tags: [ai, coding-agents, testing, feedback-loops, developer-experience]
---

# Feedback Loops for Agents

> **In one sentence:** Coding agents are only as good as the feedback your codebase gives them, so invest in fast, trustworthy checks — tests, types, linters — that tell an agent within seconds whether its change is right.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. It writes plausible code quickly, but it can't *know* the code works. It finds out the same way you do: by running something and reading the result.

So the agent's real teacher is your **feedback loop**: the checks that run after a change and say pass or fail. A codebase with a 20-second test suite, strict types, and clear error messages lets an agent try, fail, and fix many times per task. A codebase with a 40-minute flaky suite leaves it guessing — and guessing agents produce confident, wrong code.

Google's DORA (DevOps Research and Assessment) program found the same pattern at the organizational level in its 2025 report: AI acts as an **amplifier**, magnifying a team's existing strengths and weaknesses rather than fixing them.

## Why it matters

- **Verification is the bottleneck, not typing.** Agents generate code faster than anyone can read it. Automated checks are the only reviewer that keeps up.
- **Fast checks let the agent fix its own mistakes.** Each failed test the agent sees and fixes is one fewer bug a human has to find in review.
- **The same investment helps humans.** Fast tests, clear errors, and one-command builds were already good engineering. Agents just make its absence expensive faster.

The limit: checks only catch what they check. An agent can make every test pass while doing the wrong thing, if the tests don't describe the right thing. Fast feedback narrows the gap; human review of *intent* still closes it ([[reviewing-ai-generated-code]]).

## How to apply it

- **Make every check one command.** `make test`, `make check`. If running the tests needs a wiki page, the agent will run them wrong.
- **Make tests fast and deterministic.** Aim for a unit suite that runs in seconds. A **flaky test** — one that fails at random — is worse with agents than without, because the agent "fixes" code that wasn't broken.
- **Turn conventions into checks.** Types, linters, formatters, and architecture tests ("nothing in `core/` imports the database") enforce rules every time. Prose rules in an instruction file are only followed most of the time ([[agent-instruction-files]]).
- **Write error messages for a reader with no context.** "Expected Cents, got float in `refund()`" lets an agent fix the bug. "AssertionError" makes it guess.
- **Keep modules small, with clear boundaries.** An agent changing a 300-line module with a clear interface does better than one wading through a 5,000-line file. This is [[separation-of-concerns]] paying off again.
- **Leave good examples to copy.** Agents imitate what's nearby. One well-written endpoint, test, and migration teaches more than a page of rules.
- **Protect the tests themselves.** An agent stuck on a failing test may weaken or delete it to make it pass. Review test changes closely, and treat a deleted assertion as a red flag.

## Example

A team tries agents on a service whose test suite takes 35 minutes and fails randomly about one run in ten. Agents either skip running tests or chase random failures, and reviewers find basic bugs in most agent PRs (pull requests). The team concludes "agents don't work on our code."

Instead of giving up, they spend two weeks on the loop:

- Split out a unit suite of pure business-logic tests that runs in 15 seconds, using [[functional-core-imperative-shell]] where the logic was tangled with I/O.
- Quarantine the flaky tests and fix the top five causes (shared state, real clocks, network calls).
- Add strict type checking to the core module and one architecture test.

Agents now run the fast suite after every edit and fix most of their own failures before anyone looks. Review shifts from "does it even run?" to "is this the right design?" The cost was real — two engineers for two weeks, plus ongoing work to keep the fast suite fast — and it paid off for the humans too.

## Common traps

- **Blaming the model for a slow loop.** If a person couldn't get a change right without a 40-minute wait, neither can an agent.
- **Trusting green checks too much.** Passing tests prove the code does what the tests say, nothing more. Agents are good at satisfying the letter of a check.
- **Letting agents write both the code and the only tests for it.** The tests then encode the same misunderstanding as the code. Start from tests a human wrote or reviewed ([[test-driven-development]]).
- **Big-bang cleanups.** You don't need a perfect codebase before using agents. Fix the loop for the areas agents work in most, first.
- **Tests that do real damage.** A test that runs real shell commands or touches real files can do harm when an agent runs it with a bug in it. Use fakes for anything destructive ([[agent-guardrails]]).

## When it doesn't apply

Some work has no fast automated check: visual design, research spikes, performance tuning against production traffic. There, keep agents to drafts and exploration, and keep the human loop tight. And for a small throwaway prototype, the setup cost of strict checks may exceed the benefit — just don't let the prototype quietly become production.

## Related

- [[testing-pyramid]] — the shape of a suite that's fast enough for agent loops.
- [[test-driven-development]] — human-written failing tests are the clearest spec an agent can get.
- [[agent-instruction-files]] — where the one-command checks get written down.
- [[spec-first-agent-tasks]] — the other half: agreeing on what "right" means before the agent starts.
- [[technical-debt]] — slow, flaky feedback is debt that agents make more expensive.
