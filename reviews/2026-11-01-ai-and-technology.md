# Review: Coding with AI, Technology, and the glossary (2026-11-01)

**Scope:** the 9 articles in `wiki/coding-with-ai/`, the 10 in `wiki/technology/`,
and `glossary.md`. All five reviewers took part; `wiki-gardener` covered the
whole wiki.
**Outcome:** we applied every must-fix and most should-fix items in the same
change, and we applied the deferred items listed at the end. Lint, the Python
tests and the JavaScript tests pass.

## Must-fix (all applied)

| Where | Finding | Reviewers |
| --- | --- | --- |
| glossary | About 20 entries linked to articles that never mention the term (blue-green, hot path, RPO/RTO, OLTP/OLAP, MTTR, quorum, toil, and others). | newcomer, accuracy, skeptic, style, gardener (all 5) |
| glossary | The DORA metrics entry listed four metrics; DORA has used five since 2024. | accuracy, skeptic |
| glossary | "Availability" linked to observability, but CAP uses the word differently. Split into Availability (CAP) and Availability (uptime). | gardener |
| shared-agent-configuration | The `.env` read-deny example implied full protection. Scripts the agent runs can still read the file; only a sandbox blocks that. | accuracy |
| large-language-models | "The remaining 7% are handed to humans" implied the system knows which answers are wrong. | skeptic (style agreed) |

## Should-fix, by theme (applied)

- **Research caveats.** METR, Microsoft and Anthropic claims now give sample sizes and scope.
  - The DORA metric names are current.
  - "Seven capabilities" now names two of them and uses DORA's framing that they *amplify* AI's benefits.
  - The pilot example admits a confound.
  - Spend tracking was added. *(accuracy, skeptic, newcomer)*
- **Guardrails overstated.**
  - An allow list isn't a boundary, because allowing `make test` allows whatever the agent writes into the tests.
  - A network allowlist narrows the leak path but doesn't close it.
  - The two articles' secrets advice now agrees.
  - A committed hook is code that runs on every teammate's machine. *(skeptic, accuracy)*
- **Examples that skipped the hard part:**
  - The visibility-timeout race in message-brokers.
  - The cache-aside delete race.
  - The CDN purge cost.
  - The flash-sale lock hotspot in relational-databases.
  - The cost of a mixed REST/gRPC estate.
  - The trap of trusting the agent's own exploration report.
  - *(skeptic, accuracy)*
- **Absolutes softened:**
  - Surviving a cold cache.
  - Banning agents from sensitive code.
  - One name per concept, now limited to within a bounded context.
  - Console lockdown, now with a break-glass role.
  - CPU limits.
  - NoSQL as a first choice.
  - *(skeptic, accuracy)*
- **Accuracy:**
  - Where instruction-following comes from (post-training).
  - ACID isolation levels.
  - The Bigtable origin.
  - Cache latency figures.
  - Retry arithmetic: three attempts per layer, matching retries-and-timeouts.
  - The Pacific round-trip figure.
  - Terraform's licence.
  - Kafka 4.2 share groups.
  - S3 blocking public access by default.
  - Structured-output modes.
- **Undefined terms** now defined at first use:
  - image, Dockerfile, Nix
  - port, MCP server, context window
  - acknowledge, topic, wide-column, CDC
  - Layer 4/7, terminate TLS
  - manifests and Helm charts, pets
  - cursor pagination, the string-built registry
  - OpenAPI, GraphQL caching
  - jitter, stampede
  - *(newcomer, style)*
- **Style:**
  - Inverted "PRs (pull requests)".
  - Unexpanded CI, ADR and REST.
  - A non-canonical *coding agent* definition.
  - Credits moved to the end of "The idea" in api-styles and containers-and-kubernetes.
  - The "Fake REST" lead-in.
  - Fragment lead-ins.
  - A five-sentence paragraph.
  - Acronym glossary entries renamed to the `Full name (ACRONYM)` form.
- **Links** *(gardener)*:
  - Older articles now link into Technology: event-driven-architecture, transactional-outbox, cqrs, cap-theorem, reversible-decisions, microservices, api-versioning, contract-testing, idempotency, paved-roads, ADRs, design-docs and circuit-breaker.
  - large-language-models, api-styles and navigable-codebases now have inbound links.
  - Index cross-pointers were added between AI and Technology.
- **Overlap:**
  - event-driven-architecture now links message-brokers for DLQs, delivery and partitioning.
  - feedback-loops-for-agents dropped its duplicate "leave good examples" bullet.
  - reviewing-ai-generated-code now links to the Microsoft study instead of repeating it. *(gardener, style)*
- **Glossary:** 29 terms added, bringing it from 87 to 116 entries. Among them: cache-aside, stampede, TTL, CDN, consumer lag, container, dev container, drift, evaluation set, flaky test, health check, hook, index, isolation level, LLM, lethal trifecta, load balancer, message broker, NoSQL, pre-signed URL, REST/gRPC/GraphQL, state file and ubiquitous language. Where no article explains a term (consensus, quorum, toil, hot path, rate limiting, uptime), the entry no longer has a "See" link.

## Deferred (not applied)

- **New articles proposed by the gardener:**
  - `secrets-management` (mentioned about 12 times across the new sections)
  - `progressive-delivery` (proposed earlier too; would give canary, blue-green and zero-downtime a home)
  - `backups-and-disaster-recovery` (RPO and RTO)
- **Index:**
  - A second starter path: "Using coding agents?"
  - Reordering Coding with AI to "For each change" → "Setting up" → "For the team".
- **Remaining copies of DORA's "amplifier" finding** in feedback-loops-for-agents and spec-first-agent-tasks. These are already one clause each.
- **Glossary entries for older terms:** anti-corruption layer, kill switch, service mesh.
- **Low-value links** from testing-pyramid and blameless-postmortems.
- **A possible linter rule:** fail when a glossary entry's linked article never mentions the term. This was the root cause of the main must-fix, but matching term variants is fuzzy, so it needs design first.
