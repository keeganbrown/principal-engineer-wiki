# Principal Engineer Wiki — Index

Start here. Each article takes about five minutes to read and follows the same
shape: the idea → why it matters → how to apply it → an example → common
traps → when it doesn't apply.

**New here?** A good first path:
[[kiss]] → [[yagni]] → [[reversible-decisions]] → [[separation-of-concerns]] →
[[coupling-and-cohesion]] → [[functional-core-imperative-shell]] → [[test-driven-development]] →
[[conways-law]] → [[influencing-without-authority]].

## Principles

Timeless rules of thumb for judging any design.

**Simplicity**
- [[kiss]] — Choose the simplest design that solves today's problem.
- [[yagni]] — Don't build for imagined futures; most guesses are wrong.
- [[dry]] — One home for each piece of knowledge, but don't abstract too early.

**Judgment**
- [[reversible-decisions]] — Move fast on two-way doors; slow down on one-way doors.

**Structure**
- [[separation-of-concerns]] — Each part handles one kind of job.
- [[coupling-and-cohesion]] — Keep related things together, unrelated things apart.
- [[solid-principles]] — Five heuristics for code that's safe to change.
- [[conways-law]] — Systems mirror the teams that build them.

**Distributed data**
- [[cap-theorem]] — In a network split, choose consistency or availability. The foundation for the distributed-systems patterns below.

## Practices

Habits that make teams faster and systems safer.

**Testing**
- [[test-driven-development]] — Red, green, refactor, in tight loops.
- [[testing-pyramid]] — Many fast tests, few slow ones.
- [[contract-testing]] — Catch breaking API changes in CI, not production.

**Shipping change**
- [[code-review]] — Small changes, read by a peer, focused on what matters.
- [[feature-flags]] — Deploy and release are separate events.
- [[api-versioning]] — An API is a promise; evolve it without breaking callers.
- [[expand-and-contract]] — Add the new, migrate, then remove the old.

**Decisions** (see also [[reversible-decisions]])
- [[design-docs]] — Think it through in writing, while flaws are cheap.
- [[architecture-decision-records]] — Record what you decided and why.

**Operating**
- [[observability]] — Systems that explain themselves in production.
- [[blameless-postmortems]] — Fix the system that made the mistake easy.
- [[technical-debt]] — Borrow deliberately, pay down on purpose.

## Architecture patterns

Proven structures for organizing systems.

**Structuring code**
- [[functional-core-imperative-shell]] — Pure decisions inside, thin I/O outside.
- [[hexagonal-architecture]] — Business logic at the center, plugged in via ports.
- [[domain-driven-design]] — Model the business; split by bounded context.

**Structuring systems**
- [[modular-monolith]] — Clean boundaries without a network.
- [[microservices]] — Independent services, when independence is worth the cost.

**Distributed systems** (start with [[cap-theorem]])
- [[event-driven-architecture]] — Announce facts; let others react.
- [[transactional-outbox]] — Save and publish atomically.
- [[cqrs]] — Separate models for writing and reading.
- [[saga-pattern]] — Multi-service workflows with planned undo steps.
- [[idempotency]] — Doing it twice equals doing it once.

**Resilience**
- [[retries-and-timeouts]] — Deadlines on every call; retry with backoff and jitter.
- [[circuit-breaker]] — Fail fast when a dependency is down.
- [[backpressure]] — Push back when work arrives faster than you can handle it.

**Evolving systems**
- [[strangler-fig]] — Replace legacy one slice at a time.
- See also: [[expand-and-contract]], the same idea for one field or column.

## Leadership

The non-code half of the principal role.

- [[influencing-without-authority]] — Lead through trust, framing, and clear writing.
- [[paved-roads]] — Make the right way the easy way, and maintain it.
- See also: [[reversible-decisions]], [[design-docs]], [[blameless-postmortems]].

## Coding with AI

Working well with coding agents, as an engineer and as a team.

**For the team**
- [[adopting-coding-agents]] — Shared norms, peer-led rollout, and outcome metrics.
- [[agent-guardrails]] — Least access, sandboxes, and assuming input can lie.

**Setting up the codebase**
- [[agent-instruction-files]] — A short, reviewed briefing the agent rereads every session.
- [[feedback-loops-for-agents]] — Fast, trustworthy checks are the agent's real teacher.
- [[reproducible-dev-environments]] — One command, same tools for every human, CI job, and agent.
- [[shared-agent-configuration]] — Permissions, hooks, and commands checked in and reviewed.
- [[navigable-codebases]] — Structure an agent can find its way around with search alone.

**For each change**
- [[spec-first-agent-tasks]] — Explore, plan, then build in small slices.
- [[reviewing-ai-generated-code]] — You open the PR, you own the code.
