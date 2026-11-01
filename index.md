# Principal Engineer Wiki — Index

Start here. Each article takes about five minutes to read and follows the same
shape: the idea → why it matters → how to apply it → an example → common
traps → when it doesn't apply.

**New here?** A good first path:
[[kiss]] → [[coupling-and-cohesion]] → [[separation-of-concerns]] →
[[functional-core-imperative-shell]] → [[test-driven-development]] →
[[conways-law]].

## Principles

Timeless rules of thumb for judging any design.

- [[kiss]] — Choose the simplest design that solves today's problem.
- [[yagni]] — Don't build for imagined futures; most guesses are wrong.
- [[dry]] — One home for each piece of knowledge, but don't abstract too early.
- [[separation-of-concerns]] — Each part handles one kind of job.
- [[coupling-and-cohesion]] — Keep related things together, unrelated things apart.
- [[solid-principles]] — Five heuristics for code that's safe to change.
- [[conways-law]] — Systems mirror the teams that build them.

## Practices

Habits that make teams faster and systems safer.

- [[test-driven-development]] — Red, green, refactor, in tight loops.
- [[testing-pyramid]] — Many fast tests, few slow ones.
- [[code-review]] — Small changes, read by a peer, focused on what matters.
- [[architecture-decision-records]] — Write down why, not just what.
- [[observability]] — Systems that explain themselves in production.
- [[technical-debt]] — Borrow deliberately, pay down on purpose.
- [[feature-flags]] — Deploy and release are separate events.

## Architecture patterns

Proven structures for organizing systems.

**Structuring code**
- [[functional-core-imperative-shell]] — Pure decisions inside, thin I/O outside.
- [[hexagonal-architecture]] — Business logic at the center, plugged in via ports.
- [[modular-monolith]] — Clean boundaries without a network.

**Distributed systems**
- [[event-driven-architecture]] — Announce facts; let others react.
- [[cqrs]] — Separate models for writing and reading.
- [[idempotency]] — Doing it twice equals doing it once.
- [[circuit-breaker]] — Fail fast when a dependency is down.

**Evolving systems**
- [[strangler-fig]] — Replace legacy one slice at a time.
