# Glossary

Short, plain-English definitions of terms used across the wiki. Each entry
links to the article that explains it properly, where one exists. Entries are
alphabetical under each letter; the linter checks the format.

## A

- **ACID** — The four guarantees of a database transaction: atomicity (all or nothing), consistency (rules still hold), isolation (concurrent transactions don't see each other's partial work), and durability (committed data survives a crash). See [[relational-databases]].
- **Agent instruction file** — A Markdown file in the repository, such as `AGENTS.md`, that a coding agent loads at the start of every session: how to build and test, where things live, and what never to do. See [[agent-instruction-files]].
- **Aggregate** — In domain-driven design, a cluster of objects that is changed as one unit through a single root object, which enforces the rules. See [[domain-driven-design]].
- **Antipattern** — A common response to a problem that looks reasonable but reliably makes things worse, with a known better alternative. See [[big-ball-of-mud]] for the classic example.
- **API gateway** — One entry point in front of many services that handles routing, authentication, and rate limits for them. See [[strangler-fig]].
- **Architecture decision record (ADR)** — A short document that records one decision, its context, and its consequences. See [[architecture-decision-records]].
- **At-least-once delivery** — Every message is delivered, but some may arrive more than once, so consumers must handle duplicates. See [[message-brokers]].
- **At-most-once delivery** — Each message is delivered once or not at all: nothing is duplicated, but some messages may be lost. See [[message-brokers]].
- **Authentication and authorization** — Authentication establishes who a caller is; authorization decides what that caller may do, such as whether they may read this particular record. See [[threat-modeling]].
- **Availability (CAP)** — In the CAP theorem, every request to a working node gets a non-error response, even during a network partition. See [[cap-theorem]].
- **Availability (uptime)** — The share of time a system answers requests successfully, often stated in "nines": 99.9% allows about 43 minutes of downtime a month.

## B

- **Backpressure** — Signaling a producer to slow down when a consumer can't keep up, instead of letting work pile up without limit. See [[backpressure]].
- **Big ball of mud** — A system with no enforced structure, where any part may depend on any other. See [[big-ball-of-mud]].
- **Big-bang rewrite** — Rebuilding a system from scratch and switching over all at once, instead of replacing it piece by piece. See [[big-bang-rewrite]].
- **Bikeshedding** — Spending the most discussion on small, easy decisions while big, hard ones get little scrutiny. See [[bikeshedding]].
- **Blast radius** — How much breaks when one component fails or one change goes wrong. Good design and gradual rollouts keep it small. See [[infrastructure-as-code]].
- **Blue-green deployment** — Running the old (blue) and new (green) versions side by side and switching traffic at once, so rolling back is just switching back. See [[load-balancers-and-cdns]].
- **Bounded context** — A boundary inside which one domain model, and its words, have a single consistent meaning. See [[domain-driven-design]].
- **Burn rate** — How fast a service is spending its error budget. A burn rate of 1 uses exactly the budget over the window; a high one pages someone. See [[service-level-objectives]].
- **Bus factor** — How many people would need to be unavailable before a project stalls. A bus factor of one is a risk. See [[hero-culture]].

## C

- **Cache invalidation** — Removing or updating cached copies when the source data changes. See [[caching]].
- **Cache stampede** — Many requests missing the cache at once, usually when a popular entry expires, and all hitting the database together. Also called a thundering herd. See [[caching]].
- **Cache-aside** — The default caching pattern: read the cache, and on a miss read the source and store the result. See [[caching]].
- **Canary release** — Releasing a change to a small slice of traffic first and watching it before rolling it out further. See [[continuous-delivery]].
- **CAP theorem** — During a network partition, a distributed system must choose between staying consistent and staying available. See [[cap-theorem]].
- **Cargo cult engineering** — Copying another team's practices without the problems and conditions that made them work. See [[cargo-cult-engineering]].
- **Change-data-capture (CDC)** — Streaming a database's committed changes to other systems as they happen. See [[transactional-outbox]].
- **Characterization test** — A test that records what existing code actually does, odd parts included, so changes don't silently lose behavior. See [[test-driven-development]].
- **CI/CD** — Continuous integration (merging and testing changes often, automatically) and continuous delivery or deployment (keeping every change releasable, or releasing it automatically). See [[continuous-delivery]].
- **Circuit breaker** — A wrapper that stops calling a failing dependency for a while, so callers fail fast instead of waiting. See [[circuit-breaker]].
- **Coding agent** — An AI tool that reads code, runs commands, and edits files in a loop toward a goal. See [[agent-instruction-files]].
- **Cohesion** — How closely the parts of one module belong together. High cohesion is good. See [[coupling-and-cohesion]].
- **Compensating action** — A step that undoes the business effect of an earlier step, such as a refund for a charge. See [[saga-pattern]].
- **Consensus** — Getting several machines to agree on one value even when some fail; algorithms such as Raft and Paxos do this.
- **Constraint** — A rule the database enforces on every write, such as "stock can't go below zero" or "every order line points to a real product." See [[relational-databases]].
- **Consumer lag** — How far behind the newest message a consumer is. Rising lag is the earliest sign consumers can't keep up. See [[message-brokers]].
- **Container** — An application packaged with its runtime, libraries, and settings into an image that runs the same everywhere. See [[containers-and-kubernetes]].
- **Content delivery network (CDN)** — A worldwide network of servers that keep cached copies of your content near users. See [[load-balancers-and-cdns]].
- **Context window** — The amount of text, measured in tokens, that a large language model can consider in one request. See [[large-language-models]].
- **Conway's law** — Systems tend to mirror the communication structure of the organization that builds them. See [[conways-law]].
- **Coupling** — How much one module depends on another. Loose coupling lets them change independently. See [[coupling-and-cohesion]].
- **CQRS** — Command query responsibility segregation: separate models for changing data and for reading it. See [[cqrs]].

## D

- **Dead-letter queue (DLQ)** — Where messages go after failing repeatedly, so one bad message doesn't block the rest. Someone must own reviewing it. See [[message-brokers]].
- **Defense in depth** — Layering several independent controls so that one failing doesn't expose the system. See [[threat-modeling]].
- **Denormalization** — Storing copies of data in the shape each read needs, trading harder writes for faster reads. See [[nosql-databases]].
- **Dependency inversion** — High-level code defines the interfaces it needs, and low-level code implements them. See [[hexagonal-architecture]].
- **Dev container** — A development environment defined by a `devcontainer.json` file in the repository, so every engineer, CI job, and agent gets the same tools. See [[reproducible-dev-environments]].
- **Distributed monolith** — Services split across the network that still have to change, deploy, and fail together. See [[distributed-monolith]].
- **DORA metrics** — Five delivery measures from Google's DevOps Research and Assessment program: lead time for changes, deployment frequency, change failure rate, failed deployment recovery time, and deployment rework rate. See [[adopting-coding-agents]].
- **Drift** — The gap between what your infrastructure code describes and what actually exists, usually from changes made by hand. See [[infrastructure-as-code]].
- **DRY** — Don't repeat yourself: give each piece of knowledge one authoritative home, but don't abstract too early. See [[dry]].

## E

- **Embedding** — A list of numbers that represents a piece of text, so that texts with similar meanings are close together. It powers semantic search. See [[large-language-models]].
- **Error budget** — The amount of unreliability a service level objective allows. When it's used up, reliability work comes before new features. See [[service-level-objectives]].
- **Evaluation set** — Real examples with known-good answers, used to score every prompt or model change; the test suite for an LLM feature. See [[large-language-models]].
- **Eventual consistency** — If writes stop, all copies of the data converge to the same value, but reads may be stale in the meantime. See [[cap-theorem]].
- **Expand and contract** — Changing a schema or API in safe steps: add the new form, migrate to it, then remove the old one. See [[expand-and-contract]].

## F

- **Fan-out** — One request or event triggering many downstream calls or messages. See [[message-brokers]].
- **Feature flag** — A runtime switch that turns a code path on or off without a deploy. See [[feature-flags]].
- **Flaky test** — A test that sometimes passes and sometimes fails without any code change. See [[feedback-loops-for-agents]].
- **Functional core, imperative shell** — Pure decision-making logic in the middle, with a thin layer of input/output code around it. See [[functional-core-imperative-shell]].

## G

- **God object** — One class or service that knows and does too much, so most changes have to edit it. See [[god-object]].
- **Golden hammer** — Using a familiar or fashionable tool for every problem, whether or not it fits. See [[golden-hammer]].
- **Goodhart's law** — When a measure becomes a target, it stops being a good measure, because people optimize the number instead of the outcome. See [[metric-fixation]].
- **GraphQL** — An API style with one endpoint, where the client sends a query naming exactly the fields it wants. See [[api-styles]].
- **gRPC** — An API style for calling functions on a remote service, with contracts in Protocol Buffers and generated client code. See [[api-styles]].
- **Guiding policy** — The part of a strategy that sets the overall approach and rules some options out. See [[technical-strategy]].

## H

- **Hallucination** — Output from a large language model that is fluent and confident but false. See [[large-language-models]].
- **Health check** — A regular probe a load balancer or orchestrator sends to each server, so traffic stops going to broken ones. See [[load-balancers-and-cdns]].
- **Hero culture** — A team that depends on a few people to rescue it instead of fixing what keeps needing rescue. See [[hero-culture]].
- **Hook (agent)** — A script a coding agent runs automatically at a fixed point, such as after every edit. Unlike an instruction, it always fires. See [[shared-agent-configuration]].
- **Horizontal scaling** — Handling more load by adding machines. Vertical scaling means moving to a bigger machine. See [[load-balancers-and-cdns]].
- **Hot path** — The code that runs on most requests, where performance matters most.

## I

- **Idempotency** — Doing an operation twice has the same effect as doing it once. See [[idempotency]].
- **Idempotency key** — A unique ID a client sends with a request so the server can recognize retries of the same intended action. Distinct from a trace ID. See [[idempotency]].
- **Incident commander** — The person who coordinates an incident response: keeps the overall picture, assigns work, and makes calls, without debugging. See [[incident-response]].
- **Index (database)** — A sorted lookup structure that lets the database find rows without scanning the whole table, at the cost of slower writes. See [[relational-databases]].
- **Infrastructure as code (IaC)** — Defining infrastructure in version-controlled files that a tool applies. See [[infrastructure-as-code]].
- **Isolation level** — How strongly a database shields concurrent transactions from each other. Most defaults allow some anomalies; the strictest level makes transactions behave as if run one at a time. See [[relational-databases]].

## K

- **KISS** — Keep it simple, stupid: choose the simplest design that solves today's problem. See [[kiss]].

## L

- **Large language model (LLM)** — A neural network trained on enormous amounts of text to predict what comes next, then tuned to follow instructions. See [[large-language-models]].
- **Latency** — How long one operation takes. Usually reported as percentiles, because averages hide slow outliers. See [[observability]].
- **Leader election** — Choosing one machine to coordinate work, and choosing a new one if it fails. See [[transactional-outbox]].
- **Least privilege** — Giving each person, service, and job only the permissions it needs, for only as long as it needs them. See [[threat-modeling]].
- **Lethal trifecta** — An agent with private data, exposure to untrusted content, and a way to send data out can be tricked into leaking that data. See [[agent-guardrails]].
- **Load balancer** — A component that spreads incoming requests across several healthy servers behind one address. See [[load-balancers-and-cdns]].
- **Load shedding** — Deliberately rejecting some requests during overload so the rest can succeed. See [[backpressure]].

## M

- **Mean time to restore (MTTR)** — The average time from the start of an incident until service is back. DORA now calls it failed deployment recovery time. See [[incident-response]].
- **Message broker** — Software that holds messages between services, so producers don't wait for consumers. Comes as queues or logs. See [[message-brokers]].
- **Metric fixation** — Turning a measurement into a target, so people optimize the number instead of the outcome. See [[metric-fixation]].
- **Model Context Protocol (MCP)** — An open standard for connecting AI applications to tools and data sources. See [[shared-agent-configuration]].
- **Modular monolith** — One deployable application divided internally into well-bounded modules. See [[modular-monolith]].

## N

- **N+1 query** — Loading a list with one query, then running one more query for each item in it. See [[relational-databases]].
- **NoSQL** — A loose name for databases that don't use the relational table model, such as key-value, document, wide-column, and search stores. See [[nosql-databases]].
- **Not invented here (NIH)** — The reflex to build your own version of something you could adopt. See [[not-invented-here]].

## O

- **Object storage** — Storage for whole files, called objects, in flat buckets addressed by key over HTTP. See [[object-storage]].
- **Observability** — How well you can understand what a system is doing from its outputs: logs, metrics, and traces. See [[observability]].
- **OLTP and OLAP** — Online transaction processing (many small reads and writes, like checkout) versus online analytical processing (large scans and aggregates, like reports). See [[nosql-databases]].
- **Outbox** — A table written in the same transaction as the business data, from which messages are later published reliably. See [[transactional-outbox]].

## P

- **Partition (data)** — A slice of a dataset or message stream, chosen by a key, that can be stored or processed separately. See [[message-brokers]].
- **Partition (network)** — A failure in which parts of a system can't reach each other. See [[cap-theorem]].
- **Paved road** — The supported, easy way to build and run software in an organization. See [[paved-roads]].
- **Percentile (p50, p99)** — The value that a given share of measurements fall at or below. p99 latency is the time that 99% of requests finish within. See [[observability]].
- **Port and adapter** — A port is an interface the core of an application defines; an adapter implements it for one specific technology. See [[hexagonal-architecture]].
- **Pre-signed URL** — A link that grants temporary permission to upload or download one object, so files can skip your servers. See [[object-storage]].
- **Progressive delivery** — Releasing a change to a small slice of users or traffic first, then widening it in steps with automatic checks. See [[continuous-delivery]].
- **Prompt injection** — Text in an AI model's input that the model mistakes for instructions. See [[agent-guardrails]].
- **Pull request (PR)** — A proposed change, reviewed and discussed before it is merged. See [[code-review]].

## Q

- **Quality attribute** — A property a system must have, such as latency, availability, cost, or how fast teams can ship. Architecture choices trade one against another. See [[architecture-trade-offs]].
- **Quorum** — The minimum number of machines that must agree for an operation to count, usually a majority.

## R

- **Rate limiting** — Capping how many requests a client may make in a period of time.
- **Read replica** — A copy of a database that serves reads and lags slightly behind the primary. See [[relational-databases]].
- **Replication lag** — How far a copy of the data is behind its source. See [[cap-theorem]].
- **REST** — Representational state transfer: an API style of resources at URLs acted on with HTTP methods, usually with JSON bodies. See [[api-styles]].
- **Retrieval-augmented generation (RAG)** — Looking up relevant documents and giving them to a language model along with the question. See [[large-language-models]].
- **Retry with backoff and jitter** — Retrying a failed call after growing, randomized delays, so many clients don't retry in lockstep. See [[retries-and-timeouts]].
- **RPO and RTO** — Recovery point objective (how much recent data you can afford to lose) and recovery time objective (how long you can afford to be down). See [[relational-databases]].

## S

- **Saga** — A multi-step workflow across services in which each step has a compensating action. See [[saga-pattern]].
- **Sandbox** — An isolated environment that limits which files, networks, and credentials the code inside it can reach. See [[agent-guardrails]].
- **Second-system effect** — Fred Brooks's observation that a designer's second system tends to be over-designed, carrying every idea held back from the first. See [[big-bang-rewrite]].
- **Separation of concerns** — Splitting a system into parts that each handle one kind of job. See [[separation-of-concerns]].
- **Sharding** — Splitting data across several databases by key, so that each holds a part. See [[relational-databases]].
- **Single point of failure (SPOF)** — A component whose failure takes the whole system down. See [[load-balancers-and-cdns]].
- **SLI, SLO, SLA** — Service level indicator (what you measure, such as success rate), objective (the target, such as 99.9%), and agreement (the promise to customers, with consequences if broken). See [[service-level-objectives]].
- **SOLID** — Five heuristics for object-oriented design that keep code safe to change. See [[solid-principles]].
- **State file** — The record an infrastructure-as-code tool keeps of which real resources match which code. It often holds secrets, so store it remotely, locked, and encrypted. See [[infrastructure-as-code]].
- **Strangler fig** — Replacing a legacy system one piece at a time behind a routing layer. See [[strangler-fig]].
- **STRIDE** — A checklist of six threat types: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege. See [[threat-modeling]].

## T

- **Tail latency** — The slowest requests, such as the p99 or p99.9. Often what users remember. See [[observability]].
- **Technical debt** — The future cost of shortcuts and outdated design in today's code. See [[technical-debt]].
- **Technical strategy** — A short written plan with a diagnosis of the real problem, a guiding policy, and a few coherent actions. See [[technical-strategy]].
- **Threat modeling** — Asking at design time what could go wrong security-wise at each trust boundary, and deciding what to do about each threat. See [[threat-modeling]].
- **Throughput** — How much work a system completes per unit of time. See [[backpressure]].
- **Time-to-live (TTL)** — How long a cached copy is kept before it expires and is fetched again. See [[caching]].
- **Timeout** — A deadline after which a caller stops waiting for an answer. See [[retries-and-timeouts]].
- **Toil** — Manual, repetitive operational work that grows with the system and could be automated.
- **Token** — A chunk of text a language model reads or writes, roughly three-quarters of an English word. See [[large-language-models]].
- **Trace ID** — An ID that follows one request through every service it touches, also called a correlation ID. See [[observability]].
- **Transaction** — A group of database changes that succeed or fail together. See [[relational-databases]].
- **Trunk-based development** — Merging short-lived branches into the main branch at least daily, with unfinished work hidden behind feature flags. See [[continuous-delivery]].
- **Trust boundary** — A place where data passes from a less-trusted party into a more-trusted part of the system, such as the internet calling your API. See [[threat-modeling]].
- **Two-phase commit (2PC)** — A protocol in which a coordinator asks every participant to prepare, then tells them all to commit. Correct, but participants are stuck if the coordinator fails mid-way. See [[saga-pattern]].

## U

- **Ubiquitous language** — In domain-driven design, the shared vocabulary that the business and the code both use, within one bounded context. See [[domain-driven-design]].
- **Unattended agent run** — A coding agent rerun on a schedule or repository event, with nobody watching, until a task is done. It needs a stop condition a machine can check, a spending cap, a human handoff, and a sandbox. See [[feedback-loops-for-agents]].

## Y

- **YAGNI** — You aren't gonna need it: don't build for imagined future requirements. See [[yagni]].

## Z

- **Zero-downtime deployment** — Releasing a new version without users seeing errors, using rolling or blue-green deploys and backward-compatible changes. See [[load-balancers-and-cdns]].
