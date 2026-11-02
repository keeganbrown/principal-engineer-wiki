---
title: Spec-First Agent Tasks
category: coding-with-ai
summary: Before a coding agent writes code, have it explore and propose a plan, agree on what "done" means, and hand it work in small slices — because a wrong plan executed quickly is still wrong.
tags: [ai, coding-agents, planning, small-batches, workflow]
---

# Spec-First Agent Tasks

> **In one sentence:** Before a coding agent writes code, have it explore and propose a plan, agree on what "done" means, and hand it work in small slices — because a wrong plan executed quickly is still wrong.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. Give it a one-line request and it will start typing at once, filling every gap in the request with a guess. Some guesses are wrong, and you discover which ones only after reading a large diff.

Spec-first means splitting the work into phases you can check:

1. **Explore.** The agent reads the relevant code and reports what it found, changing nothing.
2. **Plan.** It proposes an approach: files to touch, the design, the tests that will prove it works. You correct the plan, which is cheap.
3. **Implement.** It builds one slice at a time, running checks as it goes.
4. **Verify and commit.** The checks pass, you review, and the slice lands as a small commit or pull request (PR).

Anthropic's guidance for Claude Code describes the same explore–plan–code–commit loop, and most agent tools now have a read-only "plan mode" for the first two steps.

## Why it matters

- **Correcting a plan is cheaper than correcting code.** A wrong assumption caught in a ten-line plan costs a sentence. Caught in an 800-line diff, it costs the diff.
- **Small slices keep review possible.** Agents make it easy to produce huge changes that nobody can review well. DORA (DevOps Research and Assessment) names working in small batches as one of seven capabilities that make AI-assisted teams succeed.
- **A clear "done" lets the agent check itself.** "Add rate limiting" is vague. "Requests over 100 per minute per API key get HTTP 429 with a `Retry-After` header; a test proves it" is something the agent can verify.

The limit: planning has a cost too. For a one-line fix, a planning phase is ceremony.

## How to apply it

- **Write acceptance criteria before implementation.** State what must be true when it's done, ideally as tests. A failing test is the most precise spec you can give an agent ([[test-driven-development]]).
- **Ask for the plan in writing, then edit it.** Look for wrong assumptions, missing edge cases, and files it shouldn't touch. Push back on the plan the way you would in a [[design-docs|design review]], at a smaller scale.
- **Size tasks to one reviewable PR.** If the plan has six independent steps, that's six tasks. A reviewer should be able to understand a slice in one sitting.
- **Point at examples and constraints.** "Follow the pattern in `orders/refund.py`; don't change the public API" removes whole categories of guesses.
- **Restart instead of arguing.** If you've corrected the agent twice on the same task and it's still off, stop. Write a better spec and start a fresh session; a long session full of failed attempts tends to make results worse, not better.
- **Decide the design yourself on one-way doors.** Let the agent explore options for decisions that are hard to undo, but make the call yourself and record it ([[reversible-decisions]]).

## Example

A request: "Add rate limiting to the public API."

**Without a plan,** the agent adds an in-memory counter in the web framework's middleware. Tests pass. In review, someone notices the service runs on eight instances, so each one counts separately and the real limit is eight times too high. The agent also changed the error format for every endpoint. The PR is 900 lines, and most of it gets thrown away.

**Spec-first:**

- **Explore first.** "Read the middleware, the deployment config, and the error handling. Don't change anything; tell me what you found." The agent reports eight instances and an existing Redis cluster.
- **Then plan.** It proposes a shared Redis counter. The engineer adds two corrections: the limit is per API key, not per IP address, and don't touch the existing error format.
- **Implement in three PRs.** (1) a rate-limit module with unit tests and a fake clock; (2) wiring for one endpoint behind a [[feature-flags|feature flag]]; (3) rollout to the rest.

The hard part is the wait: twenty minutes of exploring and planning before any code feels slow. It's still faster than reviewing and discarding 900 lines.

## Common traps

- **Approving plans without reading them.** A rubber-stamped plan is just a slower way to skip planning.
- **Over-specifying.** Writing the code in prose ("on line 40, add…") wastes your time and the agent's strengths. Specify behavior and constraints, not keystrokes.
- **One giant task.** "Migrate the service to the new framework" in one session produces a change nobody can review. Break it up, perhaps with [[strangler-fig]].
- **Letting the agent define "done."** If the agent writes the acceptance tests *and* the code with no human check in between, it is marking its own homework.
- **Losing the plan.** Plans that only live in a chat session vanish. Save important ones in the PR description or an issue so the reasoning is reviewable later.

## When it doesn't apply

Small, well-understood changes — a typo, a one-line fix, a rename the tools can do safely — don't need a plan; just ask and check. Exploratory spikes, where the goal is to learn rather than to ship, can skip the spec too, as long as the spike's code is thrown away rather than merged.

## Related

- [[feedback-loops-for-agents]] — fast checks are what make "done" verifiable.
- [[reviewing-ai-generated-code]] — small, planned slices are what make review possible.
- [[design-docs]] — the same "think in writing first" idea at team scale.
- [[test-driven-development]] — tests as the spec.
- [[yagni]] — an agent will happily build features you didn't ask for; the plan is where you say no.
