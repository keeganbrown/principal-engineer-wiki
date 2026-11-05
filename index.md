# Principal Engineer Wiki — Index

A field guide to what a Principal Software Engineer should know: principles,
practices, architecture, technology, leadership, coding with AI, and the
pitfalls to avoid.

Start here. Each article takes about five minutes to read and follows the same
shape: the idea → why it matters → how to apply it → an example → common
traps → when it doesn't apply.

**New here?** A good first path:
[[kiss]] → [[yagni]] → [[reversible-decisions]] → [[architecture-trade-offs]] → [[separation-of-concerns]] →
[[coupling-and-cohesion]] → [[functional-core-imperative-shell]] → [[test-driven-development]] →
[[conways-law]] → [[influencing-without-authority]].

**Looking up a word?** The glossary (`glossary.md`, or the Terms tab on the
site) defines the terms used across the wiki in a sentence or two each.

## Principles

Timeless rules of thumb for judging any design.

**Simplicity**
- [[kiss]] — Choose the simplest design that solves today's problem.
- [[yagni]] — Don't build for imagined futures; most guesses are wrong.
- [[dry]] — One home for each piece of knowledge, but don't abstract too early.

**Judgment**
- [[architecture-trade-offs]] — No best design, only the best fit: rank what matters, name what each option costs.
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
- [[continuous-delivery]] — Small batches through one pipeline, rolled out to a few users first.
- [[feature-flags]] — Deploy and release are separate events.
- [[api-versioning]] — An API is a promise; evolve it without breaking callers.
- See also: [[api-styles]], the REST, gRPC, and GraphQL styles being versioned.
- [[expand-and-contract]] — Add the new, migrate, then remove the old.

**Decisions** (see also [[reversible-decisions]])
- [[design-docs]] — Think it through in writing, while flaws are cheap.
- [[architecture-decision-records]] — Record what you decided and why.

**Operating**
- [[observability]] — Systems that explain themselves in production.
- [[service-level-objectives]] — A reliability target users notice, and an error budget to spend.
- [[incident-response]] — One commander, mitigate first, update on a clock.
- [[blameless-postmortems]] — Fix the system that made the mistake easy.
- [[technical-debt]] — Borrow deliberately, pay down on purpose.

**Security**
- [[threat-modeling]] — Find what can go wrong at each trust boundary, while the design is cheap to change.

## Architecture patterns

Proven structures for organizing systems.

**Structuring code**
- [[functional-core-imperative-shell]] — Pure decisions inside, thin I/O outside.
- [[hexagonal-architecture]] — Business logic at the center, plugged in via ports.
- [[domain-driven-design]] — Model the business; split by bounded context.

**Structuring systems**
- [[modular-monolith]] — Clean boundaries without a network.
- [[microservices]] — Independent services, when independence is worth the cost.
- See also: [[distributed-monolith]], what a split without independence looks like.

**Distributed systems** (start with [[cap-theorem]])
- [[event-driven-architecture]] — Announce facts; let others react.
- [[transactional-outbox]] — Save and publish atomically.
- [[cqrs]] — Separate models for writing and reading.
- [[saga-pattern]] — Multi-service workflows with planned undo steps.
- [[idempotency]] — Doing it twice equals doing it once.
- See also: [[message-brokers]], the infrastructure these patterns run on.

**Resilience**
- [[retries-and-timeouts]] — Deadlines on every call; retry with backoff and jitter.
- [[circuit-breaker]] — Fail fast when a dependency is down.
- [[backpressure]] — Push back when work arrives faster than you can handle it.

**Evolving systems**
- [[strangler-fig]] — Replace legacy one slice at a time.
- See also: [[big-bang-rewrite]], the approach the strangler fig replaces.
- See also: [[expand-and-contract]], the same idea for one field or column.

## Technology

The kinds of technology every principal engineer should understand: what each is for, and when to pick something else.

**Storing data**
- [[relational-databases]] — Tables, constraints, and transactions; the default for business data.
- [[nosql-databases]] — Key-value, document, wide-column, and search stores, each for a specific access pattern.
- [[caching]] — Faster reads in exchange for deciding how stale is acceptable.
- [[object-storage]] — Cheap, durable storage for files, referenced from the database.

**Moving data**
- [[message-brokers]] — Queues to hand off work; logs to keep a replayable stream of events.
- [[api-styles]] — REST, gRPC, and GraphQL, and which callers each suits.
- [[load-balancers-and-cdns]] — The front door: spreading traffic and serving content close to users.

**Running software**
- [[containers-and-kubernetes]] — Package once, run anywhere; orchestrate when you have many services.
- [[infrastructure-as-code]] — Infrastructure defined in reviewed, version-controlled files.
- See also: [[reproducible-dev-environments]], the same container idea for development.

**AI**
- [[large-language-models]] — What LLMs are good at, how they fail, and how to build around them.
- See also: the Coding with AI section below.

## Leadership

The non-code half of the principal role.

- [[influencing-without-authority]] — Lead through trust, framing, and clear writing.
- [[technical-strategy]] — Diagnose the real problem, choose an approach that rules things out, act.
- [[paved-roads]] — Make the right way the easy way, and maintain it.
- See also: [[reversible-decisions]], [[design-docs]], [[blameless-postmortems]], [[adopting-coding-agents]], [[hero-culture]], [[bikeshedding]], [[metric-fixation]].

## Coding with AI

Working well with coding agents, as an engineer and as a team. The research here is early and mixed, so these articles treat findings as signals to check against your own team, not forecasts. Start with [[large-language-models]] for how the underlying models behave.

**For the team**
- [[adopting-coding-agents]] — Shared norms, peer-led rollout, and outcome metrics.
- [[agent-guardrails]] — Least access, sandboxes, and assuming input can lie.

**Setting up the codebase**
- [[agent-instruction-files]] — A short, reviewed briefing the agent rereads every session.
- [[feedback-loops-for-agents]] — Fast, trustworthy checks are the agent's real teacher, and every unattended run needs one to stop.
- [[reproducible-dev-environments]] — One command, same tools for every human, CI job, and agent.
- [[shared-agent-configuration]] — Permissions, hooks, and commands checked in and reviewed.
- [[navigable-codebases]] — Structure an agent can find its way around with search alone.

**For each change**
- [[spec-first-agent-tasks]] — Explore, plan, then build in small slices.
- [[reviewing-ai-generated-code]] — You open the PR, you own the code.

## Pitfalls and antipatterns

Tempting moves that reliably make things worse: how to spot each one, how to climb out, and when it's actually the right call.

**Code and system structure**
- [[big-ball-of-mud]] — No enforced boundaries; everything calls everything.
- [[god-object]] — One class or service that every change has to touch.
- [[distributed-monolith]] — Services that still deploy and fail together.

**Change and technology choices**
- [[big-bang-rewrite]] — Rebuilding from scratch and switching over in one day.
- [[golden-hammer]] — One favorite tool for every problem.
- [[cargo-cult-engineering]] — Copying the rituals of successful teams without their conditions.
- [[not-invented-here]] — Building your own when you could adopt, then owning it forever.

**Teams and decisions**
- [[hero-culture]] — Depending on rescuers instead of fixing what needs rescuing.
- [[bikeshedding]] — Debating the smallest decisions most, while big ones slip through.
- [[metric-fixation]] — A measure becomes a target and stops measuring.
