# Glossary

Short, plain-English definitions of terms used across the wiki. Each entry
links to the article that explains it properly. Entries are alphabetical
under each letter; the linter checks the format.

## A

- **ACID** — The four guarantees of a database transaction: atomicity (all or nothing), consistency (rules still hold), isolation (concurrent transactions don't see each other's partial work), and durability (committed data survives a crash). See [[relational-databases]].
- **ADR** — Architecture decision record: a short document that records one decision, its context, and its consequences. See [[architecture-decision-records]].
- **Aggregate** — In domain-driven design, a cluster of objects that is changed as one unit through a single root object, which enforces the rules. See [[domain-driven-design]].
- **API gateway** — One entry point in front of many services that handles routing, authentication, and rate limits for them. See [[microservices]].
- **At-least-once delivery** — Every message is delivered, but some may arrive more than once, so consumers must handle duplicates. See [[idempotency]].
- **At-most-once delivery** — Each message is delivered once or not at all: nothing is duplicated, but some messages may be lost. See [[message-brokers]].
- **Availability** — The share of time a system answers requests successfully, often stated in "nines": 99.9% allows about 43 minutes of downtime a month. See [[observability]].

## B

- **Backpressure** — Signaling a producer to slow down when a consumer can't keep up, instead of letting work pile up without limit. See [[backpressure]].
- **Blast radius** — How much breaks when one component fails or one change goes wrong. Good design and gradual rollouts keep it small. See [[feature-flags]].
- **Blue-green deployment** — Running the old (blue) and new (green) versions side by side and switching traffic at once, so rolling back is just switching back. See [[load-balancers-and-cdns]].
- **Bounded context** — A boundary inside which one domain model, and its words, have a single consistent meaning. See [[domain-driven-design]].

## C

- **Cache invalidation** — Removing or updating cached copies when the source data changes. See [[caching]].
- **Canary release** — Releasing a change to a small slice of traffic first and watching it before rolling it out further. See [[feature-flags]].
- **CAP theorem** — During a network partition, a distributed system must choose between staying consistent and staying available. See [[cap-theorem]].
- **CDC** — Change-data-capture: streaming a database's committed changes to other systems as they happen. See [[transactional-outbox]].
- **CI/CD** — Continuous integration (merging and testing changes often, automatically) and continuous delivery or deployment (keeping every change releasable, or releasing it automatically). See [[testing-pyramid]].
- **Circuit breaker** — A wrapper that stops calling a failing dependency for a while, so callers fail fast instead of waiting. See [[circuit-breaker]].
- **Coding agent** — An AI tool that reads code, runs commands, and edits files in a loop toward a goal. See [[agent-instruction-files]].
- **Cohesion** — How closely the parts of one module belong together. High cohesion is good. See [[coupling-and-cohesion]].
- **Compensating action** — A step that undoes the business effect of an earlier step, such as a refund for a charge. See [[saga-pattern]].
- **Consensus** — Getting several machines to agree on one value even when some fail; algorithms such as Raft and Paxos do this. See [[cap-theorem]].
- **Context window** — The amount of text, measured in tokens, that a large language model can consider in one request. See [[large-language-models]].
- **Conway's law** — Systems tend to mirror the communication structure of the organization that builds them. See [[conways-law]].
- **Coupling** — How much one module depends on another. Loose coupling lets them change independently. See [[coupling-and-cohesion]].
- **CQRS** — Command query responsibility segregation: separate models for changing data and for reading it. See [[cqrs]].

## D

- **Dead-letter queue (DLQ)** — Where messages go after failing repeatedly, so one bad message doesn't block the rest. Someone must own reviewing it. See [[message-brokers]].
- **Denormalization** — Storing copies of data in the shape each read needs, trading harder writes for faster reads. See [[nosql-databases]].
- **Dependency inversion** — High-level code defines the interfaces it needs, and low-level code implements them. See [[hexagonal-architecture]].
- **DORA metrics** — Four delivery measures from Google's DevOps Research and Assessment program: deployment frequency, lead time for changes, change failure rate, and time to restore service. See [[adopting-coding-agents]].
- **DRY** — Don't repeat yourself: give each piece of knowledge one authoritative home, but don't abstract too early. See [[dry]].

## E

- **Embedding** — A list of numbers that represents a piece of text, so that texts with similar meanings are close together. Powers semantic search. See [[large-language-models]].
- **Error budget** — The amount of unreliability a service level objective allows. When it's used up, reliability work comes before new features. See [[observability]].
- **Eventual consistency** — If writes stop, all copies of the data converge to the same value, but reads may be stale in the meantime. See [[cap-theorem]].
- **Expand and contract** — Changing a schema or API in safe steps: add the new form, migrate to it, then remove the old one. See [[expand-and-contract]].

## F

- **Fan-out** — One request or event triggering many downstream calls or messages. See [[event-driven-architecture]].
- **Feature flag** — A runtime switch that turns a code path on or off without a deploy. See [[feature-flags]].
- **Functional core, imperative shell** — Pure decision-making logic in the middle, with a thin layer of input/output code around it. See [[functional-core-imperative-shell]].

## H

- **Hallucination** — Output from a large language model that is fluent and confident but false. See [[large-language-models]].
- **Horizontal scaling** — Handling more load by adding machines. Vertical scaling means moving to a bigger machine. See [[load-balancers-and-cdns]].
- **Hot path** — The code that runs on most requests, where performance matters most. See [[caching]].

## I

- **Idempotency** — Doing an operation twice has the same effect as doing it once. See [[idempotency]].
- **Idempotency key** — A unique ID a client sends with a request so the server can recognize retries of the same intended action. Distinct from a trace ID. See [[idempotency]].
- **Infrastructure as code (IaC)** — Defining infrastructure in version-controlled files that a tool applies. See [[infrastructure-as-code]].

## K

- **KISS** — Keep it simple, stupid: choose the simplest design that solves today's problem. See [[kiss]].

## L

- **Latency** — How long one operation takes. Usually reported as percentiles, because averages hide slow outliers. See [[observability]].
- **Leader election** — Choosing one machine to coordinate work, and choosing a new one if it fails. See [[cap-theorem]].
- **Load shedding** — Deliberately rejecting some requests during overload so the rest can succeed. See [[backpressure]].

## M

- **MCP** — Model Context Protocol: an open standard for connecting AI applications to tools and data sources. See [[shared-agent-configuration]].
- **Modular monolith** — One deployable application divided internally into well-bounded modules. See [[modular-monolith]].
- **MTTR** — Mean time to restore: the average time from the start of an incident until service is back. See [[blameless-postmortems]].

## N

- **N+1 query** — Loading a list with one query, then running one more query for each item in it. See [[relational-databases]].

## O

- **Observability** — How well you can understand what a system is doing from its outputs: logs, metrics, and traces. See [[observability]].
- **OLTP and OLAP** — Online transaction processing (many small reads and writes, like checkout) versus online analytical processing (large scans and aggregates, like reports). See [[nosql-databases]].
- **Outbox** — A table written in the same transaction as the business data, from which messages are later published reliably. See [[transactional-outbox]].

## P

- **Partition (data)** — A slice of a dataset or message stream, chosen by a key, that can be stored or processed separately. See [[message-brokers]].
- **Partition (network)** — A failure in which parts of a system can't reach each other. See [[cap-theorem]].
- **Paved road** — The supported, easy way to build and run software in an organization. See [[paved-roads]].
- **Percentile (p50, p99)** — The value that a given share of measurements fall below. p99 latency is slower than 99% of requests. See [[observability]].
- **Port and adapter** — A port is an interface the core of an application defines; an adapter implements it for one specific technology. See [[hexagonal-architecture]].
- **Prompt injection** — Text in an AI model's input that the model mistakes for instructions. See [[agent-guardrails]].
- **Pull request (PR)** — A proposed change, reviewed and discussed before it is merged. See [[code-review]].

## Q

- **Quorum** — The minimum number of machines that must agree for an operation to count, usually a majority. See [[cap-theorem]].

## R

- **RAG** — Retrieval-augmented generation: looking up relevant documents and giving them to a language model along with the question. See [[large-language-models]].
- **Rate limiting** — Capping how many requests a client may make in a period of time. See [[backpressure]].
- **Read replica** — A copy of a database that serves reads and lags slightly behind the primary. See [[relational-databases]].
- **Replication lag** — How far a copy of the data is behind its source. See [[cap-theorem]].
- **Retry with backoff and jitter** — Retrying a failed call after growing, randomized delays, so many clients don't retry in lockstep. See [[retries-and-timeouts]].
- **RPO and RTO** — Recovery point objective (how much recent data you can afford to lose) and recovery time objective (how long you can afford to be down). See [[relational-databases]].

## S

- **Saga** — A multi-step workflow across services in which each step has a compensating action. See [[saga-pattern]].
- **Sandbox** — An isolated environment that limits which files, networks, and credentials the code inside it can reach. See [[agent-guardrails]].
- **Separation of concerns** — Splitting a system into parts that each handle one kind of job. See [[separation-of-concerns]].
- **Sharding** — Splitting data across several databases by key, so that each holds a part. See [[relational-databases]].
- **Single point of failure (SPOF)** — A component whose failure takes the whole system down. See [[load-balancers-and-cdns]].
- **SLI, SLO, SLA** — Service level indicator (what you measure, such as success rate), objective (the target, such as 99.9%), and agreement (the promise to customers, with consequences if broken). See [[observability]].
- **SOLID** — Five heuristics for object-oriented design that keep code safe to change. See [[solid-principles]].
- **Strangler fig** — Replacing a legacy system one piece at a time behind a routing layer. See [[strangler-fig]].

## T

- **Tail latency** — The slowest requests, such as the p99 or p99.9. Often what users remember. See [[retries-and-timeouts]].
- **Technical debt** — The future cost of shortcuts and outdated design in today's code. See [[technical-debt]].
- **Throughput** — How much work a system completes per unit of time. See [[backpressure]].
- **Timeout** — A deadline after which a caller stops waiting for an answer. See [[retries-and-timeouts]].
- **Toil** — Manual, repetitive operational work that grows with the system and could be automated. See [[paved-roads]].
- **Token** — A chunk of text a language model reads or writes, roughly three-quarters of an English word. See [[large-language-models]].
- **Trace ID** — An ID that follows one request through every service it touches, also called a correlation ID. See [[observability]].
- **Transaction** — A group of database changes that succeed or fail together. See [[relational-databases]].
- **Two-phase commit (2PC)** — A protocol in which a coordinator asks every participant to prepare, then tells them all to commit. Correct, but participants are stuck if the coordinator fails mid-way. See [[saga-pattern]].

## Y

- **YAGNI** — You aren't gonna need it: don't build for imagined future requirements. See [[yagni]].

## Z

- **Zero-downtime deployment** — Releasing a new version without users seeing errors, using rolling or blue-green deploys and backward-compatible changes. See [[expand-and-contract]].
